"""长期记忆 Store + memory_brief 组装。"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models_ext import LongTermMemory, MemorySummary, StudentProfile


KIND_VALUES = frozenset({"preference", "fact", "weakness", "note", "episodic"})


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_kind(kind: str) -> str:
    k = (kind or "note").strip().lower()
    return k if k in KIND_VALUES else "note"


def memory_public_dict(row: LongTermMemory) -> dict[str, Any]:
    return {
        "id": row.id,
        "kind": row.kind,
        "text": row.text,
        "importance": row.importance,
        "source": row.source,
        "active": row.active,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        "expires_at": row.expires_at.isoformat() if row.expires_at else None,
    }


def memory_search(
    db: Session,
    user_id: int,
    query: str = "",
    *,
    kind: Optional[str] = None,
    limit: int = 8,
) -> list[LongTermMemory]:
    q = select(LongTermMemory).where(
        LongTermMemory.user_id == user_id,
        LongTermMemory.active.is_(True),
    )
    if kind:
        q = q.where(LongTermMemory.kind == _normalize_kind(kind))
    # 过期过滤
    now = _now()
    q = q.where(
        or_(LongTermMemory.expires_at.is_(None), LongTermMemory.expires_at > now)
    )

    rows = list(db.scalars(q.order_by(LongTermMemory.importance.desc()).limit(80)).all())
    query = (query or "").strip()
    if not query:
        return rows[:limit]

    tokens = [t for t in re.split(r"[\s,，。；;]+", query.lower()) if t]
    scored: list[tuple[float, LongTermMemory]] = []
    for row in rows:
        text_l = (row.text or "").lower()
        hit = sum(1 for t in tokens if t in text_l)
        if hit <= 0 and query.lower() not in text_l:
            continue
        score = hit + float(row.importance or 0)
        scored.append((score, row))
    scored.sort(key=lambda x: (-x[0], -(x[1].updated_at.timestamp() if x[1].updated_at else 0)))
    return [r for _, r in scored[:limit]]


def memory_upsert(
    db: Session,
    user_id: int,
    *,
    text: str,
    kind: str = "note",
    importance: float = 0.5,
    source: str = "tool",
    memory_id: Optional[int] = None,
) -> LongTermMemory:
    text = (text or "").strip()
    if not text:
        raise ValueError("text required")
    kind_n = _normalize_kind(kind)
    imp = max(0.0, min(1.0, float(importance)))

    row: Optional[LongTermMemory] = None
    if memory_id:
        row = db.get(LongTermMemory, int(memory_id))
        if row and row.user_id != user_id:
            row = None

    # 同 kind + 近似文本合并
    if row is None:
        candidates = memory_search(db, user_id, text[:40], kind=kind_n, limit=5)
        for c in candidates:
            if c.text.strip() == text or text in c.text or c.text in text:
                row = c
                break

    if row is None:
        row = LongTermMemory(
            user_id=user_id,
            kind=kind_n,
            text=text[:2000],
            importance=imp,
            source=(source or "tool")[:32],
            active=True,
            created_at=_now(),
            updated_at=_now(),
        )
        db.add(row)
    else:
        row.kind = kind_n
        row.text = text[:2000]
        row.importance = max(float(row.importance or 0), imp)
        row.source = (source or row.source or "tool")[:32]
        row.active = True
        row.updated_at = _now()

    db.commit()
    db.refresh(row)
    return row


def memory_forget(
    db: Session,
    user_id: int,
    *,
    memory_id: Optional[int] = None,
    query: str = "",
) -> dict[str, Any]:
    forgotten: list[int] = []
    if memory_id:
        row = db.get(LongTermMemory, int(memory_id))
        if row and row.user_id == user_id and row.active:
            row.active = False
            row.updated_at = _now()
            forgotten.append(row.id)
    elif (query or "").strip():
        for row in memory_search(db, user_id, query, limit=12):
            row.active = False
            row.updated_at = _now()
            forgotten.append(row.id)
    else:
        return {"ok": False, "error": "memory_id or query required", "forgotten": []}

    db.commit()
    return {"ok": True, "forgotten": forgotten, "count": len(forgotten)}


def list_active_by_kinds(
    db: Session, user_id: int, kinds: list[str], *, limit: int = 20
) -> list[LongTermMemory]:
    kinds_n = [_normalize_kind(k) for k in kinds]
    q = (
        select(LongTermMemory)
        .where(
            LongTermMemory.user_id == user_id,
            LongTermMemory.active.is_(True),
            LongTermMemory.kind.in_(kinds_n),
        )
        .order_by(LongTermMemory.importance.desc())
        .limit(limit)
    )
    return list(db.scalars(q).all())


def build_memory_brief(
    db: Session,
    user_id: int,
    *,
    max_chars: int = 900,
) -> str:
    """回合开始注入：近期摘要 + 长期摘录 + 弱项一行。"""
    parts: list[str] = []

    summaries = list(
        db.scalars(
            select(MemorySummary)
            .where(MemorySummary.user_id == user_id)
            .order_by(MemorySummary.created_at.desc())
            .limit(2)
        ).all()
    )
    for s in summaries:
        line = (s.summary_text or "").strip().replace("\n", " ")
        if line:
            parts.append(f"[摘要] {line[:220]}")

    ltm = memory_search(db, user_id, "", limit=6)
    for row in ltm:
        parts.append(f"[{row.kind}] {row.text.strip()[:160]}")

    profile = db.get(StudentProfile, user_id)
    if profile:
        weak = profile.weak_points or []
        if isinstance(weak, list) and weak:
            names = [str(w) for w in weak[:4]]
            parts.append(f"[弱项] {', '.join(names)}")

    if not parts:
        return ""

    brief = "；".join(parts)
    if len(brief) > max_chars:
        brief = brief[: max_chars - 1] + "…"
    return brief
