"""记忆层 API：摘要上传（隐私）→ 画像沉淀；旁路抽题进回流候选。"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import get_settings
from app.db import get_db
from app.db.models import User
from app.services.memory import (
    ingest_summary,
    list_own_summaries,
    profile_public_dict,
    summarize_turns,
)
from app.services.profile import get_or_create_profile

router = APIRouter(prefix="/api/memory", tags=["记忆层"])


class TurnItem(BaseModel):
    role: str
    content: str = ""


class SummarizeIn(BaseModel):
    session_id_client: str = ""
    agent: str = Field("student", description="student|teacher|curriculum")
    turns: list[TurnItem]
    turn_from: Optional[int] = None
    turn_to: Optional[int] = None


class IngestIn(BaseModel):
    """客户端已生成摘要时直接入库（仍不存原文）。"""

    session_id_client: str = ""
    agent: str = "student"
    summary_text: str
    topics: list[Any] = Field(default_factory=list)
    mastery_hints: list[Any] = Field(default_factory=list)
    mistakes_hints: list[Any] = Field(default_factory=list)
    qa_pairs: list[Any] = Field(default_factory=list)
    turn_from: Optional[int] = None
    turn_to: Optional[int] = None


@router.get("/config")
def memory_config(db: Session = Depends(get_db)):
    from app.services.runtime_config import get_runtime_config

    cfg = get_runtime_config(db)
    s = get_settings()
    return {
        "ok": True,
        "summary_every_n": cfg.get("memory_summary_every_n", s.memory_summary_every_n),
        "keep_recent_k": cfg.get("memory_keep_recent_k", s.memory_keep_recent_k),
        "auth_disabled": s.auth_disabled,
    }


@router.post("/summarize")
async def summarize_and_ingest(
    body: SummarizeIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not body.turns:
        raise HTTPException(400, detail="turns 不能为空")
    parsed = await summarize_turns(
        [t.model_dump() for t in body.turns], agent=body.agent
    )
    row, profile, reflow_items = ingest_summary(
        db,
        user=user,
        agent=body.agent,
        session_id_client=body.session_id_client,
        summary_text=parsed["summary_text"],
        topics=parsed["topics"],
        mastery_hints=parsed["mastery_hints"],
        mistakes_hints=parsed["mistakes_hints"],
        source_turn_range={"from": body.turn_from, "to": body.turn_to},
        qa_pairs=parsed.get("qa_pairs") or [],
    )
    from app.services.runtime_config import get_runtime_config

    return {
        "ok": True,
        "summary_id": row.id,
        "summary_text": row.summary_text,
        "topics": row.topics,
        "qa_pairs_enqueued": len(reflow_items),
        "profile": profile_public_dict(user, profile),
        "keep_recent_k": get_runtime_config(db).get(
            "memory_keep_recent_k", get_settings().memory_keep_recent_k
        ),
    }


@router.post("/ingest")
def ingest_only(
    body: IngestIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not body.summary_text.strip():
        raise HTTPException(400, detail="summary_text 不能为空")
    row, profile, reflow_items = ingest_summary(
        db,
        user=user,
        agent=body.agent,
        session_id_client=body.session_id_client,
        summary_text=body.summary_text.strip(),
        topics=body.topics,
        mastery_hints=body.mastery_hints,
        mistakes_hints=body.mistakes_hints,
        source_turn_range={"from": body.turn_from, "to": body.turn_to},
        qa_pairs=body.qa_pairs,
    )
    return {
        "ok": True,
        "summary_id": row.id,
        "qa_pairs_enqueued": len(reflow_items),
        "profile": profile_public_dict(user, profile),
    }


@router.get("/summaries/me")
def my_summaries(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """仅本人可读摘要（对话隐私）。教师端无此接口权限给别人。"""
    rows = list_own_summaries(db, user.id)
    return {
        "ok": True,
        "items": [
            {
                "id": r.id,
                "agent": r.agent,
                "session_id_client": r.session_id_client,
                "summary_text": r.summary_text,
                "topics": r.topics,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ],
    }


@router.get("/profile/me")
def my_profile_via_memory(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    p = get_or_create_profile(db, user.id)
    return profile_public_dict(user, p)
