"""本地 bge-reranker 精排。

真实模型：sentence-transformers CrossEncoder → FlagReranker；
否则用 embedding 余弦相似度占位。
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from app.config import Settings, get_settings
from app.services.embedding import get_embedding_service

logger = logging.getLogger(__name__)


class RerankService:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._model = None
        self._backend = "mock"  # mock | st | flag | embed
        self.mode = "mock"
        if self.settings.bge_use_real_model and self.settings.bge_rerank_via_embed:
            # 降级：不加载 CrossEncoder，直接用真实 embedding 余弦
            self._backend = "embed"
            self.mode = "embed_cosine"
            logger.info("Rerank 降级模式：真实 embedding 余弦（省 CrossEncoder 内存）")
            return
        if self.settings.bge_use_real_model:
            self._try_load_real()

    def _try_load_real(self) -> None:
        name = self.settings.bge_reranker_model
        device = self.settings.bge_device
        try:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(name, device=device)
            self._backend = "st"
            self.mode = "bge-reranker-v2-m3"
            logger.info("已加载 Reranker(CrossEncoder): %s @ %s", name, device)
            return
        except Exception as exc:
            logger.warning("CrossEncoder 加载失败: %s", exc)

        try:
            from FlagEmbedding import FlagReranker  # type: ignore

            self._model = FlagReranker(name, use_fp16=False, device=device)
            self._backend = "flag"
            self.mode = "bge-reranker-v2-m3"
            logger.info("已加载 Reranker(FlagEmbedding): %s", name)
            return
        except Exception as exc:
            logger.warning("Reranker 加载失败，回退 mock: %s", exc)
            self._model = None
            self._backend = "mock"
            self.mode = "mock"

    def rerank(
        self, query: str, documents: list[str], top_k: int = 5
    ) -> list[tuple[int, float]]:
        if not documents:
            return []

        if self._model is not None and self._backend == "st":
            pairs = [[query, doc] for doc in documents]
            scores = self._model.predict(pairs, convert_to_numpy=True)
            if hasattr(scores, "tolist"):
                scores = scores.tolist()
            if isinstance(scores, (int, float)):
                scores = [float(scores)]
            ranked = sorted(
                enumerate(float(s) for s in scores), key=lambda x: x[1], reverse=True
            )
            return ranked[:top_k]

        if self._model is not None and self._backend == "flag":
            pairs = [[query, doc] for doc in documents]
            scores = self._model.compute_score(pairs, normalize=True)
            if isinstance(scores, (int, float)):
                scores = [float(scores)]
            ranked = sorted(
                enumerate(float(s) for s in scores), key=lambda x: x[1], reverse=True
            )
            return ranked[:top_k]

        # mock 或 embed 降级：用 embedding 余弦
        emb = get_embedding_service()
        qv = np.array(emb.embed_one(query), dtype=np.float32)
        dvs = np.array(emb.embed(documents), dtype=np.float32)
        # 防止零向量
        qn = np.linalg.norm(qv) + 1e-9
        dn = np.linalg.norm(dvs, axis=1) + 1e-9
        sims = (dvs @ qv) / (dn * qn)
        ranked = sorted(enumerate(sims.tolist()), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


_rerank: Optional[RerankService] = None


def get_rerank_service() -> RerankService:
    global _rerank
    if _rerank is None:
        _rerank = RerankService()
    return _rerank


def reset_rerank_service() -> None:
    global _rerank
    _rerank = None
