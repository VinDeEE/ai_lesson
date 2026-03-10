import argparse
import json
from typing import Any, Dict, List

from rag_core import load_index, retrieve_evidence


def to_view(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for item in items:
        out.append(
            {
                "source_file": item.get("source_file", ""),
                "chunk_id": item.get("chunk_id", ""),
                "score": round(float(item.get("score", 0.0)), 4),
                "preview": (item.get("text", "") or "")[:180],
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Week3 retrieval debug runner")
    parser.add_argument("question", help="user question")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--top_k", type=int, default=4)
    parser.add_argument("--embedding_model", default=None)
    args = parser.parse_args()

    index = load_index(persist_dir=args.persist_dir, collection=args.collection)
    embed_model = args.embedding_model or index.get("embedding_model", "gemini-embedding-001")

    evidence = retrieve_evidence(
        question=args.question,
        index=index,
        top_k=args.top_k,
        embedding_model=embed_model,
    )

    print(
        json.dumps(
            {
                "question": args.question,
                "top_k": args.top_k,
                "evidence_count": len(evidence),
                "evidence": to_view(evidence),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
