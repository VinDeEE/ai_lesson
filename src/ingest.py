import argparse
from pathlib import Path
from typing import Dict, List

from rag_core import embed_texts, now_iso, save_index


def read_documents(docs_dir: Path) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for path in docs_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        docs.append({"text": text, "source": str(path), "source_file": path.name})
    return docs


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    content = text.replace("\r\n", "\n").strip()
    if not content:
        return []

    separators = ["\n\n", "\n", "。", "！", "？", ".", "!", "?", "；", ";", " "]
    chunks: List[str] = []
    start = 0
    n = len(content)

    while start < n:
        end = min(start + chunk_size, n)
        split_end = end
        search_from = start + int(chunk_size * 0.6)

        for sep in separators:
            idx = content.rfind(sep, search_from, end)
            if idx != -1:
                split_end = idx + len(sep)
                break

        chunk = content[start:split_end].strip()
        if chunk:
            chunks.append(chunk)

        if split_end >= n:
            break
        start = max(split_end - chunk_overlap, start + 1)

    return chunks


def build_chunks(raw_docs: List[Dict[str, str]], chunk_size: int, chunk_overlap: int) -> List[Dict[str, str]]:
    chunks: List[Dict[str, str]] = []
    counter: Dict[str, int] = {}
    for doc in raw_docs:
        source_file = doc["source_file"]
        pieces = split_text(doc["text"], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for piece in pieces:
            counter[source_file] = counter.get(source_file, 0) + 1
            chunks.append(
                {
                    "source": doc["source"],
                    "source_file": source_file,
                    "chunk_id": f"{Path(source_file).stem}#{counter[source_file]}",
                    "text": piece,
                }
            )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build local JSON vector index from markdown/txt docs.")
    parser.add_argument("--docs_dir", default="docs")
    parser.add_argument("--persist_dir", default="data/chroma")
    parser.add_argument("--collection", default="kb")
    parser.add_argument("--chunk_size", type=int, default=600)
    parser.add_argument("--chunk_overlap", type=int, default=120)
    parser.add_argument("--embedding_model", default="gemini-embedding-001")
    parser.add_argument("--batch_size", type=int, default=64)
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        raise FileNotFoundError(f"docs_dir not found: {docs_dir.resolve()}")

    raw_docs = read_documents(docs_dir)
    if not raw_docs:
        raise RuntimeError(f"No .md/.txt documents found under: {docs_dir.resolve()}")

    chunks = build_chunks(raw_docs, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
    if not chunks:
        raise RuntimeError("No chunks generated. Check source docs or chunk parameters.")

    vectors = embed_texts(
        texts=[chunk["text"] for chunk in chunks],
        embedding_model=args.embedding_model,
        batch_size=args.batch_size,
    )

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector

    index = {
        "collection": args.collection,
        "embedding_model": args.embedding_model,
        "updated_at": now_iso(),
        "raw_docs_count": len(raw_docs),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }
    index_path = save_index(index=index, persist_dir=args.persist_dir, collection=args.collection)

    print(f"[OK] raw docs: {len(raw_docs)}")
    print(f"[OK] chunks: {len(chunks)}")
    print(f"[OK] embedding model: {args.embedding_model}")
    print(f"[OK] index: {index_path.resolve()}")


if __name__ == "__main__":
    main()
