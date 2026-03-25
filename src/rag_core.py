import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        return False


def _load_env_file_fallback(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def bootstrap_env() -> None:
    project_env = Path(__file__).resolve().parents[1] / ".env"
    loaded = False
    try:
        loaded = bool(load_dotenv(dotenv_path=project_env, override=False))
    except TypeError:
        loaded = bool(load_dotenv())
    if not loaded:
        _load_env_file_fallback(project_env)


bootstrap_env()


OUTPUT_SCHEMA_HINT = """
请只返回 JSON，字段结构如下：
{
  "answer": "给用户的最终答复，优先使用中文。",
  "citations": [
    {"source_file":"来源文件名","chunk_id":"分段ID","quote":"证据片段"}
  ],
  "confidence": "high|medium|low",
  "need_handoff": true,
  "handoff_reason": "需要人工处理时给出原因；不需要时返回空字符串"
}
不要用 markdown 代码块包裹 JSON。
"""


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Environment variable `{name}` is missing.")
    return value


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_index_path(persist_dir: str, collection: str) -> Path:
    return Path(persist_dir) / f"{collection}.json"


def _normalize_model_name(name: str) -> str:
    raw = (name or "").strip()
    if raw.startswith("models/"):
        return raw[len("models/") :]
    return raw


def _is_embedding_model_unavailable_error(msg: str) -> bool:
    text = msg.lower()
    return (
        "not_found" in text
        or '"code": 404' in text
        or "is not found" in text
        or "not supported for embedcontent" in text
    )


def _is_generate_model_unavailable_error(msg: str) -> bool:
    text = msg.lower()
    return (
        "not_found" in text
        or '"code": 404' in text
        or "is not found" in text
        or "not supported for generatecontent" in text
    )


def _should_fallback_to_single_embedding(msg: str) -> bool:
    text = msg.lower()
    return "not supported for batchembedcontents" in text or "method not found" in text


def _parse_retry_delay_seconds(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    cleaned = value.strip().rstrip(".")
    if cleaned.endswith("s"):
        cleaned = cleaned[:-1]
    try:
        return float(cleaned)
    except ValueError:
        return None


def _extract_seconds_from_text(text: str) -> Optional[float]:
    if not text:
        return None
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)s\b", text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _extract_retry_delay_seconds(detail: str) -> Optional[float]:
    try:
        payload = json.loads(detail)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, dict):
        error = payload.get("error", {})
        if isinstance(error, dict):
            for item in error.get("details", []):
                if not isinstance(item, dict):
                    continue
                delay = _parse_retry_delay_seconds(item.get("retryDelay"))
                if delay is not None:
                    return delay
            delay = _extract_seconds_from_text(str(error.get("message", "")))
            if delay is not None:
                return delay

    return _extract_seconds_from_text(detail)


def _is_retryable_http_error(status_code: int, detail: str) -> bool:
    text = detail.lower()
    return status_code in {429, 500, 503} or "resource_exhausted" in text or "unavailable" in text


def _gemini_request(path: str, payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    api_key = get_env("GEMINI_API_KEY")
    base = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
    url = f"{base}/{path}?key={urllib.parse.quote(api_key)}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    retry_limit = max(0, int(os.getenv("GEMINI_API_MAX_RETRIES", "6")))

    req = urllib.request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    attempt = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            if attempt < retry_limit and _is_retryable_http_error(exc.code, detail):
                attempt += 1
                delay = _extract_retry_delay_seconds(detail)
                if delay is None:
                    delay = min(60.0, float(2 ** attempt))
                delay = max(1.0, delay)
                print(
                    f"[WARN] Gemini API throttled on `{path}`; retrying in {delay:.1f}s "
                    f"({attempt}/{retry_limit}).",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(f"Gemini API error HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Gemini API network error: {exc}") from exc


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return -1.0
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for a, b in zip(vec_a, vec_b):
        dot += a * b
        norm_a += a * a
        norm_b += b * b
    if norm_a == 0 or norm_b == 0:
        return -1.0
    return dot / math.sqrt(norm_a * norm_b)


def embed_texts(texts: List[str], embedding_model: str, batch_size: int = 64) -> List[List[float]]:
    get_env("GEMINI_API_KEY")
    requested_model = _normalize_model_name(embedding_model)
    fallback_model = _normalize_model_name(os.getenv("EMBEDDING_FALLBACK_MODEL", "gemini-embedding-001"))

    candidates = [requested_model]
    if fallback_model and fallback_model not in candidates:
        candidates.append(fallback_model)

    last_error: Optional[Exception] = None
    for model in candidates:
        try:
            vectors: List[List[float]] = []
            for start in range(0, len(texts), batch_size):
                batch = texts[start : start + batch_size]
                try:
                    response = _gemini_request(
                        path=f"models/{model}:batchEmbedContents",
                        payload={
                            "requests": [
                                {
                                    "model": f"models/{model}",
                                    "content": {"parts": [{"text": text}]},
                                }
                                for text in batch
                            ]
                        },
                    )
                    embeddings = response.get("embeddings", [])
                    if len(embeddings) != len(batch):
                        raise RuntimeError(
                            "Gemini batch embedding response size mismatch: "
                            f"expected {len(batch)}, got {len(embeddings)}"
                        )
                    vectors.extend(item["values"] for item in embeddings)
                except RuntimeError as exc:
                    if "GEMINI_API_KEY" in str(exc):
                        raise
                    if not _should_fallback_to_single_embedding(str(exc)):
                        raise
                    # Fall back only when the batch endpoint itself is unsupported.
                    for text in batch:
                        response = _gemini_request(
                            path=f"models/{model}:embedContent",
                            payload={
                                "model": f"models/{model}",
                                "content": {"parts": [{"text": text}]},
                            },
                        )
                        embedding = response.get("embedding", {}).get("values")
                        if not embedding:
                            raise RuntimeError(f"Gemini embedding response missing `embedding.values`: {response}")
                        vectors.append(embedding)

            if model != requested_model:
                print(
                    f"[WARN] embedding model `{requested_model}` unavailable, auto-fallback to `{model}`.",
                    file=sys.stderr,
                )
            return vectors
        except Exception as exc:
            last_error = exc
            if model == requested_model and _is_embedding_model_unavailable_error(str(exc)):
                continue
            raise

    if last_error:
        raise last_error
    raise RuntimeError("No embedding model candidate could be executed.")


def load_index(persist_dir: str, collection: str) -> Dict[str, Any]:
    index_path = get_index_path(persist_dir, collection)
    if not index_path.exists():
        raise FileNotFoundError(
            f"Index not found: {index_path.resolve()}. Run ingest first: python src/ingest.py"
        )
    data = json.loads(index_path.read_text(encoding="utf-8"))
    chunks = data.get("chunks", [])
    if not chunks:
        raise RuntimeError(f"Index exists but has no chunks: {index_path.resolve()}")
    return data


def save_index(index: Dict[str, Any], persist_dir: str, collection: str) -> Path:
    persist_path = Path(persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)
    index_path = get_index_path(persist_dir, collection)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_path


def _score_bucket(score: Optional[float]) -> str:
    if score is None:
        return "medium"
    if score >= 0.75:
        return "high"
    if score >= 0.55:
        return "medium"
    return "low"


def retrieve_evidence(
    question: str,
    index: Dict[str, Any],
    top_k: int,
    embedding_model: str,
) -> List[Dict[str, Any]]:
    query_vec = embed_texts([question], embedding_model=embedding_model)[0]

    scored = []
    for chunk in index["chunks"]:
        score = cosine_similarity(query_vec, chunk["embedding"])
        scored.append(
            {
                "score": score,
                "source_file": chunk["source_file"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def build_context(evidence: List[Dict[str, Any]]) -> str:
    lines = []
    for item in evidence:
        # Keep full chunk text to avoid losing key facts due to aggressive truncation.
        full_text = item["text"].strip()
        lines.append(
            f"- [{item['source_file']} | {item['chunk_id']} | score={item['score']:.3f}]\n{full_text}"
        )
    return "\n".join(lines)


def extract_json(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise


def call_chat_model(prompt: str, model_name: str) -> str:
    requested_model = _normalize_model_name(model_name)
    env_fallbacks = [
        _normalize_model_name(item)
        for item in os.getenv(
            "GEMINI_MODEL_FALLBACKS",
            "gemini-2.0-flash,gemini-1.5-pro,gemini-pro",
        ).split(",")
        if item.strip()
    ]
    candidates = [requested_model]
    for item in env_fallbacks:
        if item not in candidates:
            candidates.append(item)

    last_error: Optional[Exception] = None
    for model in candidates:
        try:
            response = _gemini_request(
                path=f"models/{model}:generateContent",
                payload={
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0,
                        "responseMimeType": "application/json",
                    },
                },
            )

            raw_candidates = response.get("candidates", [])
            if not raw_candidates:
                raise RuntimeError(f"Gemini response has no candidates: {response}")

            parts = raw_candidates[0].get("content", {}).get("parts", [])
            texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
            output = "\n".join(t for t in texts if t).strip()
            if not output:
                raise RuntimeError(f"Gemini response has empty text content: {response}")

            if model != requested_model:
                print(
                    f"[WARN] generation model `{requested_model}` unavailable, auto-fallback to `{model}`.",
                    file=sys.stderr,
                )
            return output
        except Exception as exc:
            last_error = exc
            if model == requested_model and _is_generate_model_unavailable_error(str(exc)):
                continue
            if model in env_fallbacks and _is_generate_model_unavailable_error(str(exc)):
                continue
            raise

    if last_error:
        raise last_error
    raise RuntimeError("No generation model candidate could be executed.")


def _build_citations(evidence: List[Dict[str, Any]], limit: int = 2) -> List[Dict[str, Any]]:
    citations = []
    for item in evidence[:limit]:
        quote = item["text"].replace("\n", " ").strip()
        citations.append(
            {
                "source_file": item["source_file"],
                "chunk_id": item["chunk_id"],
                "quote": quote[:180] + ("..." if len(quote) > 180 else ""),
            }
        )
    return citations


def _build_retrieval_meta(
    evidence: List[Dict[str, Any]],
    index: Dict[str, Any],
    top_k: int,
) -> Dict[str, Any]:
    top_score = evidence[0]["score"] if evidence else None
    return {
        "top_k": top_k,
        "top_score": top_score,
        "evidence_count": len(evidence),
        "index_updated_at": index.get("updated_at"),
    }


def _fallback_answer(reason: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    top_score = evidence[0]["score"] if evidence else None
    return {
        "mode": "llm",
        "answer": "模型输出解析失败，建议转人工处理。",
        "citations": _build_citations(evidence, limit=2),
        "confidence": _score_bucket(top_score),
        "need_handoff": True,
        "handoff_reason": reason,
    }


def _no_evidence_answer() -> Dict[str, Any]:
    return {
        "mode": "llm",
        "answer": "知识库中没有找到可用证据，建议转人工处理。",
        "citations": [],
        "confidence": "low",
        "need_handoff": True,
        "handoff_reason": "知识库检索为空。",
    }


def _vector_only_answer(
    evidence: List[Dict[str, Any]],
    index: Dict[str, Any],
    top_k: int,
) -> Dict[str, Any]:
    top_score = evidence[0]["score"] if evidence else None
    confidence = _score_bucket(top_score)

    preview_lines = ["仅向量模式：不调用生成模型，只展示按相似度召回的原始片段。"]
    for idx, item in enumerate(evidence, start=1):
        snippet = item["text"].strip().replace("\r\n", "\n")
        if len(snippet) > 220:
            snippet = snippet[:220].rstrip() + "..."
        preview_lines.append(
            f"[{idx}] {item['source_file']} | {item['chunk_id']} | score={item['score']:.3f}\n{snippet}"
        )

    return {
        "mode": "vector_only",
        "answer": "\n\n".join(preview_lines),
        "citations": _build_citations(evidence, limit=min(3, len(evidence))),
        "confidence": confidence,
        "need_handoff": confidence == "low",
        "handoff_reason": "" if confidence != "low" else "向量检索置信度较低。",
        "retrieval": _build_retrieval_meta(evidence=evidence, index=index, top_k=top_k),
    }


def answer_question(
    question: str,
    persist_dir: str = "data/chroma",
    collection: str = "kb",
    top_k: int = 4,
    model: Optional[str] = None,
    embedding_model: Optional[str] = None,
    vector_only: bool = False,
) -> Dict[str, Any]:
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    embed_model = embedding_model or os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

    index = load_index(persist_dir=persist_dir, collection=collection)
    evidence = retrieve_evidence(
        question=question,
        index=index,
        top_k=top_k,
        embedding_model=embed_model,
    )

    if not evidence:
        return _no_evidence_answer()

    if vector_only:
        return _vector_only_answer(evidence=evidence, index=index, top_k=top_k)

    top_score = evidence[0]["score"]
    score_hint = _score_bucket(top_score)
    context = build_context(evidence)

    prompt = f"""
你是企业知识库问答助手。
你只能依据下面给出的证据回答，不要编造信息。
如果证据不足，或者用户问题本身不够明确，请设置 need_handoff=true。
回答要简洁、可执行，answer 字段优先使用中文。

问题：{question}

证据：
{context}

检索置信提示：{score_hint}

{OUTPUT_SCHEMA_HINT}
""".strip()

    text = call_chat_model(prompt=prompt, model_name=model_name)
    try:
        data = extract_json(text)
    except Exception as exc:
        return _fallback_answer(f"模型输出不是合法 JSON: {exc}", evidence)

    data.setdefault("mode", "llm")
    data.setdefault("answer", "")
    data.setdefault("citations", [])
    data.setdefault("confidence", _score_bucket(top_score))
    data.setdefault("need_handoff", data.get("confidence") == "low")
    data.setdefault("handoff_reason", "" if not data["need_handoff"] else "证据不足。")

    if not isinstance(data["citations"], list):
        data["citations"] = []

    if not data["citations"]:
        data["citations"] = _build_citations(evidence, limit=1)

    data["retrieval"] = _build_retrieval_meta(evidence=evidence, index=index, top_k=top_k)
    return data
