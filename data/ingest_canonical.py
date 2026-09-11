#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 canonical chunks.jsonl 写入 ChromaDB textbook_chunks。

- 使用真实 chunk_id 作为向量 id
- media_urls 按 MEDIA_BASE_URL 重写为可公网访问地址（需先 upload_textbook_images）

用法（在 shudian_agent 项目根目录）:
  python data/ingest_canonical.py
  python data/ingest_canonical.py --chapters 1 2 3
  python data/ingest_canonical.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.config import get_settings  # noqa: E402
from app.services.embedding import get_embedding_service  # noqa: E402
from scripts.textbook.media_urls import rewrite_media_urls  # noqa: E402

COLLECTION = "textbook_chunks"
CANONICAL = BACKEND / "data" / "canonical"
BATCH = 64


def _scalar_meta(chunk: dict, media_urls: list[str]) -> dict:
    """Chroma metadata 仅接受标量。"""
    fids = chunk.get("figure_ids") or []
    return {
        "chunk_id": str(chunk.get("chunk_id") or ""),
        "chapter": str(chunk.get("chapter") or ""),
        "chapter_num": int(chunk.get("chapter_num") or 0),
        "section_id": str(chunk.get("section_id") or ""),
        "block_type": str(chunk.get("block_type") or ""),
        "figure_ids": ",".join(str(x) for x in fids),
        "media_urls": ",".join(media_urls),
        "example_id": str(chunk.get("example_id") or ""),
        "exercise_id": str(chunk.get("exercise_id") or ""),
        "source_type": str(chunk.get("source_type") or ""),
    }


def load_chunks(chapters: list[int] | None) -> list[dict]:
    nums = chapters or list(range(1, 9))
    out: list[dict] = []
    for n in nums:
        path = CANONICAL / f"ch{n:02d}" / "chunks.jsonl"
        if not path.exists():
            print(f"[skip] 缺少 {path}")
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def ingest(chapters: list[int] | None, *, dry_run: bool = False, reset: bool = False) -> None:
    settings = get_settings()
    media_base = os.getenv("MEDIA_BASE_URL", settings.media_base_url).rstrip("/")
    chunks = load_chunks(chapters)
    print(f"加载 {len(chunks)} 条 chunk；MEDIA_BASE_URL={media_base}")

    ids: list[str] = []
    docs: list[str] = []
    metas: list[dict] = []
    for c in chunks:
        cid = c.get("chunk_id")
        text = (c.get("text_content") or "").strip()
        if not cid or not text:
            continue
        urls = rewrite_media_urls(c.get("media_urls") or [], media_base)
        ids.append(str(cid))
        docs.append(text)
        metas.append(_scalar_meta(c, urls))

    with_media = sum(1 for m in metas if m.get("media_urls"))
    print(f"可入库 {len(ids)} 条（含图 {with_media}）；示例 media: "
          f"{next((m['media_urls'] for m in metas if m['media_urls']), '')[:120]}")

    if dry_run:
        return

    import chromadb

    persist = Path(settings.chroma_persist_dir)
    persist.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist))
    if reset:
        try:
            client.delete_collection(COLLECTION)
            print(f"已删除旧集合 {COLLECTION}")
        except Exception:  # noqa: BLE001
            pass
    col = client.get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )

    emb = get_embedding_service()
    total = 0
    for i in range(0, len(ids), BATCH):
        sl = slice(i, i + BATCH)
        batch_docs = docs[sl]
        vectors = emb.embed(batch_docs)
        col.upsert(
            ids=ids[sl],
            embeddings=vectors,
            documents=batch_docs,
            metadatas=metas[sl],
        )
        total += len(batch_docs)
        print(f"  upsert {total}/{len(ids)}")

    print(f"完成 → Chroma collection={COLLECTION} count≈{col.count()} dir={persist}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", type=int, nargs="*", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--reset", action="store_true", help="删除旧 textbook_chunks 再写入")
    args = parser.parse_args()
    ingest(args.chapters, dry_run=args.dry_run, reset=args.reset)


if __name__ == "__main__":
    main()
