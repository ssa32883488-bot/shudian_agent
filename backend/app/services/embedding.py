"""本地 BGE Embedding。

BGE_USE_REAL_MODEL=true 时优先加载真实模型：
1) sentence-transformers（本机已装）
2) FlagEmbedding BGEM3FlagModel
失败才回退确定性 mock 向量（仅开发兜底，生产应保证真模型可用）。
"""

from __future__ import annotations

import hashlib
import logging
from typing import Optional

import numpy as np

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)

_DIM = 1024  # BGE-M3 默认维度


class EmbeddingService:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self._model = None
        self._backend = "mock"  # mock | st | flag
        self.mode = "mock"
        if self.settings.bge_use_real_model:
            self._try_load_real()

    def _try_load_real(self) -> None:
        name = self.settings.bge_embedding_model
        device = self.settings.bge_device
        # 本地目录优先（ModelScope 缓存等），避免 Hub SSL/墙导致卡死
        from pathlib import Path

        local = Path(name)
        if local.is_dir():
            name = str(local)
        # 1) sentence-transformers
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(name, device=device)
            self._backend = "st"
            self.mode = "bge-real"
            logger.info("已加载 Embedding(sentence-transformers): %s @ %s", name, device)
            return
        except Exception as exc:
            logger.warning("sentence-transformers 加载 Embedding 失败: %s", exc)

        # 2) FlagEmbedding
        try:
            from FlagEmbedding import BGEM3FlagModel  # type: ignore

            self._model = BGEM3FlagModel(name, use_fp16=False, device=device)
            self._backend = "flag"
            self.mode = "bge-m3"
            logger.info("已加载 Embedding(FlagEmbedding): %s @ %s", name, device)
            return
        except Exception as exc:
            logger.warning("FlagEmbedding 加载失败，回退 mock 向量: %s", exc)
            self._model = None
            self._backend = "mock"
            self.mode = "mock"

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        if self._model is not None and self._backend == "st":
            vecs = self._model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            return [v.tolist() if hasattr(v, "tolist") else list(v) for v in vecs]
        if self._model is not None and self._backend == "flag":
            out = self._model.encode(texts, return_dense=True)
            dense = out["dense_vecs"]
            return [v.tolist() if hasattr(v, "tolist") else list(v) for v in dense]
        return [self._mock_embed(t) for t in texts]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]

    @staticmethod
    def _mock_embed(text: str) -> list[float]:
        seed = int(hashlib.md5(text.strip().encode("utf-8")).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(_DIM).astype(np.float32)
        vec /= np.linalg.norm(vec) + 1e-9
        return vec.tolist()


_embedding: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    global _embedding
    if _embedding is None:
        _embedding = EmbeddingService()
    return _embedding


def reset_embedding_service() -> None:
    global _embedding
    _embedding = None
