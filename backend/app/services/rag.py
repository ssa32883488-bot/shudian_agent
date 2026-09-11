"""课本向量检索（供答疑链路 RAG 工具使用）。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from app.config import get_settings
from app.services.embedding import get_embedding_service
from app.services.rerank import get_rerank_service

logger = logging.getLogger(__name__)

# 课本向量集合（离线 data/ 脚本写入）
TEXTBOOK_COLLECTION = "textbook_chunks"


def _is_stale_collection_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "does not exist" in msg or "collection [" in msg


class TextbookRAG:
    def __init__(self) -> None:
        settings = get_settings()
        persist = Path(settings.chroma_persist_dir)
        persist.mkdir(parents=True, exist_ok=True)
        import chromadb

        self._client = chromadb.PersistentClient(path=str(persist))
        self._col = self._client.get_or_create_collection(
            name=TEXTBOOK_COLLECTION, metadata={"hnsw:space": "cosine"}
        )

    def _alive(self):
        try:
            self._col.count()
            return self._col
        except Exception as exc:  # noqa: BLE001
            if not _is_stale_collection_error(exc):
                raise
            logger.warning("教材 Chroma 集合句柄失效，正在重连: %s", exc)
            self._col = self._client.get_or_create_collection(
                name=TEXTBOOK_COLLECTION, metadata={"hnsw:space": "cosine"}
            )
            return self._col

    def search(
        self,
        query: str,
        top_k: int = 5,
        *,
        min_score: Optional[float] = None,
    ) -> list[dict]:
        """向量召回 → 按相似度门槛过滤 → 精排；综合分 = max(向量, 精排)。"""
        settings = get_settings()
        if min_score is None:
            min_score = float(settings.textbook_rag_score_threshold)

        try:
            col = self._alive()
            if col.count() == 0:
                return _fallback_chunks(query)

            emb = get_embedding_service().embed_one(query)
            fetch_n = min(max(top_k * 3, 8), col.count())
            r = col.query(
                query_embeddings=[emb],
                n_results=fetch_n,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("教材 RAG 检索失败，回退占位: %s", exc)
            return _fallback_chunks(query)

        docs = (r.get("documents") or [[]])[0]
        metas = (r.get("metadatas") or [[]])[0]
        dists = (r.get("distances") or [[]])[0]

        candidates: list[dict] = []
        for i, doc in enumerate(docs):
            dist = float(dists[i]) if i < len(dists) else 1.0
            vec_score = 1.0 - dist
            if vec_score < min_score:
                continue
            meta = metas[i] if i < len(metas) else {}
            candidates.append(
                {
                    "content": doc,
                    "metadata": meta or {},
                    "score": vec_score,
                    "vector_score": vec_score,
                }
            )

        if not candidates:
            return []

        ranked = get_rerank_service().rerank(
            query, [x["content"] for x in candidates], top_k=len(candidates)
        )
        out: list[dict] = []
        for idx, rr_score in ranked:
            if idx >= len(candidates):
                continue
            item = candidates[idx]
            final = max(float(item.get("vector_score") or 0.0), float(rr_score))
            if final < min_score:
                continue
            out.append({**item, "score": final, "rerank_score": float(rr_score)})
            if len(out) >= top_k:
                break
        return out


def _fallback_chunks(query: str) -> list[dict]:
    """无离线数据时的占位引用。"""
    _ = query
    return [
        {
            "content": "组合逻辑电路的输出仅由当前输入决定，不含存储元件。（教材·第3章）",
            "metadata": {"chapter": "第3章", "source": "占位数据"},
            "score": 0.0,
        },
        {
            "content": "卡诺图化简时，圈选必须成 2 的幂次方个 1，且尽量大。（教材·第4章）",
            "metadata": {"chapter": "第4章", "source": "占位数据"},
            "score": 0.0,
        },
    ]
