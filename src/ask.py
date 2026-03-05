import argparse
import json

from rag_core import answer_question


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask one question to your RAG knowledge bot.")
    parser.add_argument("question", help="User question")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--top_k", type=int, default=4)
    parser.add_argument("--model", default=None)
    parser.add_argument("--embedding_model", default=None)
    args = parser.parse_args()

    result = answer_question(
        question=args.question,
        persist_dir=args.persist_dir,
        collection=args.collection,
        top_k=args.top_k,
        model=args.model,
        embedding_model=args.embedding_model,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
