"""FastAPI 入口：学生解题闭环 P1。"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import api_router
from app.config import get_settings
from app.db import init_db
from app.services.chromadb_client import get_chroma_store
from app.services.embedding import get_embedding_service
from app.services.mimo import get_mimo
from app.services.rerank import get_rerank_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    logger.info("启动 %s v%s", settings.app_name, __version__)
    try:
        init_db()
        logger.info("数据库表已就绪 (%s)", settings.database_url.split(":")[0])
        from app.api.deps import ensure_demo_users
        from app.db import SessionLocal

        db = SessionLocal()
        try:
            ensure_demo_users(db)
            if settings.auth_disabled:
                from app.services.memory import compute_class_rollup

                compute_class_rollup(db, settings.demo_class_code)
        finally:
            db.close()
        if settings.auth_disabled:
            logger.info("AUTH_DISABLED=true：可用 X-Dev-Persona；真实 Token 登录仍优先")
        else:
            logger.info("已开启鉴权：请使用 /login 注册登录")
            logger.info("无登录演示用户已就绪 (class=%s)", settings.demo_class_code)
    except Exception as exc:
        logger.error(
            "数据库初始化失败（请检查 DATABASE_URL）: %s",
            exc,
        )
    # 预热连接（失败不阻断启动，便于先看健康检查）
    try:
        get_chroma_store()
        emb = get_embedding_service()
        rerank = get_rerank_service()
        mimo = get_mimo()
        from app.services.checkpointer import get_checkpointer
        from app.services.object_store import minio_info
        from app.services.redis_client import redis_info

        cp = get_checkpointer()
        ri = redis_info()
        mi = minio_info()
        logger.info(
            "服务就绪: embedding=%s rerank=%s mimo_mock=%s checkpointer=%s "
            "auth_disabled=%s redis=%s minio=%s",
            emb.mode,
            rerank.mode,
            mimo.mock,
            type(cp).__name__ if cp else None,
            settings.auth_disabled,
            ri,
            mi,
        )
    except Exception as exc:
        logger.warning("部分服务预热失败: %s", exc)
    from app.services.profile_scheduler import start_profile_scheduler, stop_profile_scheduler

    start_profile_scheduler()
    yield
    stop_profile_scheduler()
    logger.info("应用关闭")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="数电单学科教育智能体 · P1 学生解题闭环",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    @app.get("/health")
    def health():
        import os

        from app.services.object_store import minio_info
        from app.services.redis_client import redis_info

        s = get_settings()
        db_kind = s.database_url.split(":")[0]
        return {
            "ok": True,
            "version": __version__,
            "mimo_mock": s.mimo_mock,
            "reflow_mode": s.reflow_mode,
            "database": db_kind,
            "redis": redis_info(),
            "minio": minio_info(),
            "listen_hint": os.environ.get("UVICORN_PORT")
            or os.environ.get("PORT")
            or "unknown",
            "instance": "fresh-chroma-reconnect",
        }

    return app


app = create_app()
