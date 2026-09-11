"""ChromaDB 连接与题库向量集合。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import chromadb
from chromadb.api.models.Collection import Collection

from app.config import Settings, get_settings
from app.services.embedding import get_embedding_service

logger = logging.getLogger(__name__)


def _is_stale_collection_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "does not exist" in msg or "collection [" in msg


class ChromaQuestionStore:
    def _open_client(self) -> None:
        persist = Path(self.settings.chroma_persist_dir)
        persist.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(persist))
        self._collection = self._open_collection()

    def _open_collection(self) -> Collection:
        return self._client.get_or_create_collection(
            name=self.settings.chroma_collection_questions,
            metadata={"hnsw:space": "cosine"},
        )

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._open_client()
        logger.info(
            "ChromaDB 已连接: dir=%s collection=%s count=%s id=%s",
            self.settings.chroma_persist_dir,
            self.settings.chroma_collection_questions,
            self._safe_count(),
            getattr(self._collection, "id", None),
        )

    def _safe_count(self) -> int:
        try:
            return int(self._collection.count())
        except Exception as exc:  # noqa: BLE001
            if _is_stale_collection_error(exc):
                self._open_client()
                return int(self._collection.count())
            raise

    def _alive(self) -> Collection:
        """句柄失效（wipe/重建后）时自动重连客户端+集合。"""
        try:
            self._collection.count()
            return self._collection
        except Exception as exc:  # noqa: BLE001
            if not _is_stale_collection_error(exc):
                raise
            logger.warning("题库 Chroma 集合句柄失效，正在重建客户端: %s", exc)
            self._open_client()
            return self._collection
    @property
    def collection(self) -> Collection:
        return self._alive()

    def upsert_question(
        self, question_id: int, content: str, metadata: Optional[dict[str, Any]] = None
    ) -> None:
        emb = get_embedding_service().embed_one(content)
        meta = {"question_id": question_id, **(metadata or {})}
        clean_meta = {k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))}
        col = self._alive()
        col.upsert(
            ids=[f"qb_{question_id}"],
            embeddings=[emb],
            documents=[content],
            metadatas=[clean_meta],
        )

    def delete_question(self, question_id: int) -> None:
        try:
            self._alive().delete(ids=[f"qb_{question_id}"])
        except Exception as exc:  # noqa: BLE001
            logger.warning("Chroma 删除 qb_%s 失败: %s", question_id, exc)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        try:
            col = self._alive()
            if col.count() == 0:
                return []
            emb = get_embedding_service().embed_one(query)
            result = col.query(
                query_embeddings=[emb],
                n_results=min(top_k, col.count()),
                include=["documents", "metadatas", "distances"],
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("题库 Chroma 检索失败，返回空: %s", exc)
            return []

        hits: list[dict[str, Any]] = []
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        for i, doc_id in enumerate(ids):
            dist = float(dists[i]) if i < len(dists) else 1.0
            score = 1.0 - dist
            meta = metas[i] if i < len(metas) else {}
            meta = meta or {}
            # 禁用题应从库中删除；残留向量若带 status≠active 则跳过
            st = str(meta.get("status") or "").lower()
            if st and st != "active":
                continue
            hits.append(
                {
                    "chroma_id": doc_id,
                    "content": docs[i] if i < len(docs) else "",
                    "metadata": meta,
                    "score": score,
                    "question_id": meta.get("question_id"),
                }
            )
        return hits


_store: Optional[ChromaQuestionStore] = None


def reset_chroma_store() -> None:
    global _store
    _store = None


def get_chroma_store() -> ChromaQuestionStore:
    global _store
    if _store is None:
        _store = ChromaQuestionStore()
    return _store
