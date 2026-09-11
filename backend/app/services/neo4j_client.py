"""Neo4j 驱动封装。"""

from __future__ import annotations

import logging
from typing import Any, Optional

from app.config import get_settings

logger = logging.getLogger(__name__)

_driver = None
_ready: Optional[bool] = None


def get_neo4j_driver():
    global _driver, _ready
    settings = get_settings()
    if not settings.neo4j_enabled:
        _ready = False
        return None
    if _driver is not None:
        return _driver
    try:
        from neo4j import GraphDatabase

        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        _driver.verify_connectivity()
        _ready = True
        logger.info("Neo4j 已连接: %s", settings.neo4j_uri)
        return _driver
    except Exception as exc:
        logger.warning("Neo4j 连接失败: %s", exc)
        _driver = None
        _ready = False
        return None


def is_neo4j_ready() -> bool:
    global _ready
    if _ready is True:
        return True
    if _ready is False and get_settings().neo4j_enabled:
        # 允许重试
        _ready = None
    d = get_neo4j_driver()
    return d is not None


def close_neo4j() -> None:
    global _driver, _ready
    if _driver is not None:
        try:
            _driver.close()
        except Exception:  # noqa: BLE001
            pass
    _driver = None
    _ready = None


def run_cypher(query: str, **params: Any) -> list[dict[str, Any]]:
    driver = get_neo4j_driver()
    if driver is None:
        raise RuntimeError("Neo4j 不可用")
    with driver.session() as session:
        result = session.run(query, **params)
        return [dict(r) for r in result]
