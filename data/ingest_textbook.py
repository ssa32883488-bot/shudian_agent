#!/usr/bin/env python3
"""教材 chunk → ChromaDB（textbook_chunks 集合）。

用法（项目根目录）:
  python data/ingest_textbook.py
  python data/ingest_textbook.py --input data/sample/textbook_chunks.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.embedding import get_embedding_service  # noqa: E402

COLLECTION = "textbook_chunks"


def ingest(input_path: Path) -> None:
    import chromadb

    chunks = json.loads(input_path.read_text(encoding="utf-8"))
    persist = BACKEND / "data" / "chroma"
    persist.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist))
    col = client.get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )

    emb = get_embedding_service()
    texts = [c["content"] for c in chunks]
    vectors = emb.embed(texts)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metas = [c.get("metadata", {}) for c in chunks]
    col.upsert(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
    print(f"已入库 {len(chunks)} 条 → ChromaDB collection={COLLECTION}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=str(ROOT / "data" / "sample" / "textbook_chunks.json"),
    )
    args = parser.parse_args()
    ingest(Path(args.input))


if __name__ == "__main__":
    main()
