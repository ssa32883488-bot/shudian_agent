"""回流审核。"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import QuestionBank, ReflowQueue
from app.services.question_bank import find_near_duplicates, sync_question_to_chroma


def _item_dict(r: ReflowQueue, *, near_dups: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
    dups = near_dups if near_dups is not None else []
    tags = getattr(r, "knowledge_tags", None)
    return {
        "id": r.id,
        "question": r.question,
        "ai_answer": r.ai_answer,
        "validate_score": r.validate_score,
        "source": r.source,
        "image_path": getattr(r, "image_path", None),
        "knowledge_tags": tags if isinstance(tags, dict) else None,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "from_memory": bool(r.source and str(r.source).startswith("memory_summary")),
        "near_dups": dups,
        "has_near_dup": bool(dups),
    }


def list_pending(db: Session, *, with_near_dup: bool = True) -> list[dict[str, Any]]:
    rows = list(
        db.scalars(
            select(ReflowQueue)
            .where(ReflowQueue.validate_status == "pending")
            .order_by(ReflowQueue.created_at.desc())
        ).all()
    )
    out: list[dict[str, Any]] = []
    for r in rows:
        dups: list[dict[str, Any]] = []
        if with_near_dup and (r.question or "").strip():
            try:
                dups = find_near_duplicates(db, r.question)
            except Exception:
                dups = []
        out.append(_item_dict(r, near_dups=dups))
    return out


def approve(
    db: Session,
    reflow_id: int,
    *,
    force: bool = False,
) -> dict[str, Any]:
    """审核入库。若存在 ≥0.95 近重且未 force，返回 needs_confirm 供管理端二次确认。"""
    item = db.get(ReflowQueue, reflow_id)
    if not item or item.validate_status != "pending":
        raise ValueError("记录不存在或已处理")

    near_dups = find_near_duplicates(db, item.question or "")
    if near_dups and not force:
        return {
            "ok": False,
            "needs_confirm": True,
            "near_dups": near_dups,
            "threshold": get_settings().hit_score_threshold,
            "message": (
                f"题库中存在相似度 ≥ {get_settings().hit_score_threshold} 的相近题目，"
                "请确认仍要入库（不会自动拦截，需管理员确认）。"
            ),
        }

    content = item.question or ""
    img = (item.image_path or "").strip()
    if img and img not in content:
        content = f"![题干原图]({img})\n\n{content}"

    source = "reflow_approved"
    if item.source and str(item.source).startswith("memory_summary"):
        source = "memory_reflow_approved"

    qb = QuestionBank(
        content=content,
        answer=item.ai_answer,
        source=source,
        status="active",
        knowledge_tags=getattr(item, "knowledge_tags", None),
    )
    db.add(qb)
    db.flush()
    sync_question_to_chroma(qb)
    item.validate_status = "approved"
    db.commit()
    db.refresh(qb)
    return {
        "ok": True,
        "needs_confirm": False,
        "question_id": qb.id,
        "near_dups": near_dups,
        "knowledge_tags": qb.knowledge_tags,
    }


def reject(db: Session, reflow_id: int) -> ReflowQueue:
    item = db.get(ReflowQueue, reflow_id)
    if not item:
        raise ValueError("记录不存在")
    item.validate_status = "rejected"
    db.commit()
    db.refresh(item)
    return item
