import argparse
from pathlib import Path
from typing import Dict

from ingest import build_chunks, read_documents
from rag_core import embed_texts, now_iso, save_index


PROFILES: Dict[str, Dict[str, int]] = {
    "baseline": {"chunk_size": 600, "chunk_overlap": 120, "batch_size": 64},
    "compact": {"chunk_size": 450, "chunk_overlap": 80, "batch_size": 64},
    "long": {"chunk_size": 800, "chunk_overlap": 160, "batch_size": 32},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Week3 ingest runner with preset profiles")
    parser.add_argument("--docs_dir", default="docs")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--embedding_model", default="gemini-embedding-001")
    parser.add_argument("--profile", choices=sorted(PROFILES.keys()), default="baseline")
    args = parser.parse_args()

    profile = PROFILES[args.profile]
    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        raise FileNotFoundError(f"docs_dir not found: {docs_dir.resolve()}")

    raw_docs = read_documents(docs_dir)
    if not raw_docs:
        raise RuntimeError(f"No .md/.txt documents found under: {docs_dir.resolve()}")

    chunks = build_chunks(
        raw_docs,
        chunk_size=profile["chunk_size"],
        chunk_overlap=profile["chunk_overlap"],
    )
    if not chunks:
        raise RuntimeError("No chunks generated. Check source docs or chunk parameters.")

    vectors = embed_texts(
        texts=[chunk["text"] for chunk in chunks],
        embedding_model=args.embedding_model,
        batch_size=profile["batch_size"],
    )

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector

    index = {
        "collection": args.collection,
        "embedding_model": args.embedding_model,
        "profile": args.profile,
        "chunk_size": profile["chunk_size"],
        "chunk_overlap": profile["chunk_overlap"],
        "updated_at": now_iso(),
        "raw_docs_count": len(raw_docs),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }

    index_path = save_index(index=index, persist_dir=args.persist_dir, collection=args.collection)

    print(f"[OK] profile: {args.profile}")
    print(f"[OK] raw docs: {len(raw_docs)}")
    print(f"[OK] chunks: {len(chunks)}")
    print(f"[OK] index: {index_path.resolve()}")


if __name__ == "__main__":
    main()
