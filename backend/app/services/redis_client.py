"""可选 Redis 连接：登录 Token 等；未配置或连不上时返回 None。"""

from __future__ import annotations

import logging
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)

_client = None
_client_failed = False


def get_redis():
    """懒加载 Redis；失败则缓存失败态，避免每次请求重试炸日志。"""
    global _client, _client_failed
    if _client is not None:
        return _client
    if _client_failed:
        return None
    settings = get_settings()
    url = (settings.redis_url or "").strip()
    if not url:
        _client_failed = True
        return None
    try:
        import redis

        c = redis.Redis.from_url(url, decode_responses=True, socket_connect_timeout=2)
        c.ping()
        _client = c
        logger.info("Redis 已连接: %s", url.split("@")[-1])
        return _client
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis 不可用，回退内存: %s", exc)
        _client_failed = True
        return None


def redis_info() -> dict:
    c = get_redis()
    if not c:
        return {"enabled": False, "ok": False}
    try:
        c.ping()
        return {"enabled": True, "ok": True}
    except Exception as exc:  # noqa: BLE001
        return {"enabled": True, "ok": False, "error": str(exc)[:120]}
