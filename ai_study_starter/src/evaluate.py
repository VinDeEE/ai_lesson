import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from rag_core import answer_question


def load_dataset(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at line {idx}: {exc}") from exc
    return rows


def score_case(result: Dict[str, Any], expected_keywords: List[str], expect_handoff: bool) -> Dict[str, Any]:
    answer_text = str(result.get("answer", "")).lower()
    keyword_hit = True
    if expected_keywords:
        keyword_hit = all(k.lower() in answer_text for k in expected_keywords)

    handoff_hit = bool(result.get("need_handoff", False)) == bool(expect_handoff)
    case_score = int(keyword_hit) + int(handoff_hit)

    return {
        "keyword_hit": keyword_hit,
        "handoff_hit": handoff_hit,
        "case_score": case_score,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run quick regression for RAG bot.")
    parser.add_argument("--dataset", default="eval/qa_samples.jsonl")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--top_k", type=int, default=4)
    parser.add_argument("--model", default=None)
    parser.add_argument("--embedding_model", default=None)
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path.resolve()}")

    rows = load_dataset(dataset_path)
    if not rows:
        raise RuntimeError("Dataset is empty.")

    total_cases = 0
    total_points = 0
    max_points = 0

    print(f"[INFO] Loaded {len(rows)} eval cases from {dataset_path}")

    for idx, row in enumerate(rows, start=1):
        question = row["question"]
        expected_keywords = row.get("expected_keywords", [])
        expect_handoff = bool(row.get("expect_handoff", False))

        result = answer_question(
            question=question,
            persist_dir=args.persist_dir,
            collection=args.collection,
            top_k=args.top_k,
            model=args.model,
            embedding_model=args.embedding_model,
        )
        score = score_case(result, expected_keywords, expect_handoff)

        total_cases += 1
        total_points += score["case_score"]
        max_points += 2

        print(
            json.dumps(
                {
                    "case": idx,
                    "question": question,
                    "keyword_hit": score["keyword_hit"],
                    "handoff_hit": score["handoff_hit"],
                    "confidence": result.get("confidence"),
                    "need_handoff": result.get("need_handoff"),
                },
                ensure_ascii=False,
            )
        )

    final_rate = 100.0 * total_points / max_points if max_points else 0.0
    print(f"[SUMMARY] cases={total_cases} score={total_points}/{max_points} pass_rate={final_rate:.1f}%")


if __name__ == "__main__":
    main()
