"""LangGraph checkpointer：优先 Redis，失败则进程内 MemorySaver。"""

from __future__ import annotations

import logging
from typing import Any, Optional

from app.config import get_settings

logger = logging.getLogger(__name__)

_checkpointer: Any = None


def get_checkpointer() -> Any:
    """返回可传入 graph.compile(checkpointer=...) 的对象。"""
    global _checkpointer
    if _checkpointer is not None:
        return _checkpointer

    settings = get_settings()
    if settings.redis_url:
        try:
            from langgraph.checkpoint.redis import RedisSaver  # type: ignore

            saver = RedisSaver.from_conn_string(settings.redis_url)
            # 部分版本需 setup()
            setup = getattr(saver, "setup", None)
            if callable(setup):
                setup()
            _checkpointer = saver
            logger.info("LangGraph checkpointer: Redis (%s)", settings.redis_url)
            return _checkpointer
        except Exception as exc:
            logger.warning("Redis checkpointer 不可用，回退 MemorySaver: %s", exc)

    try:
        from langgraph.checkpoint.memory import MemorySaver

        _checkpointer = MemorySaver()
        logger.info("LangGraph checkpointer: MemorySaver (进程内)")
    except Exception as exc:
        logger.warning("无法创建 checkpointer: %s", exc)
        _checkpointer = None
    return _checkpointer


def curriculum_thread_id(student_id: int, outline_node_id: str) -> str:
    return f"curriculum:{student_id}:{outline_node_id}"
