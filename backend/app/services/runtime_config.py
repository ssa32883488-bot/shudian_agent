"""运行时配置：参数写死在 Settings，不再提供管理端热改。"""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.config import get_settings

# 对外仍暴露这四个键，便于既有调用点（回流 / 记忆 / 权威评审）统一读取
CONFIG_KEYS = (
    "reflow_mode",
    "memory_summary_every_n",
    "memory_keep_recent_k",
    "authority_validate_threshold",
)


def get_runtime_config(db: Session | None = None) -> dict[str, Any]:
    """始终返回代码内固定值；db 参数保留兼容，不读库。"""
    _ = db
    s = get_settings()
    return {
        "reflow_mode": s.reflow_mode,
        "memory_summary_every_n": int(s.memory_summary_every_n),
        "memory_keep_recent_k": int(s.memory_keep_recent_k),
        "authority_validate_threshold": float(s.authority_validate_threshold),
    }


def invalidate_cache() -> None:
    """兼容旧调用；已无缓存。"""
    return None


def update_runtime_config(db: Session, patch: dict[str, Any]) -> dict[str, Any]:
    """管理端热改已取消：忽略 patch，返回写死配置。"""
    _ = (db, patch)
    return get_runtime_config()
