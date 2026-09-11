"""学生·自适应练习 API（替代原在线考试）。"""

from typing import Any, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.services.practice import (
    generate_practice,
    get_practice_session,
    grade_practice,
    list_practice_sessions,
)

router = APIRouter(prefix="/api/student/practice", tags=["学生·自适应练习"])


class PracticeGenerateRequest(BaseModel):
    count: int = Field(default=5, ge=1, le=20)
    mode: str = Field(default="auto")
    tags: list[str] = Field(default_factory=list)


class PracticeAnswerItem(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    images: list[str] = Field(
        default_factory=list,
        description="作答图片：dataURL 或已保存的 /media/artifacts/ 路径",
    )


class PracticeSubmitRequest(BaseModel):
    session_id: int
    answers: list[PracticeAnswerItem]
    write_mistakes: bool = True


@router.post("/generate")
def practice_generate(
    req: PracticeGenerateRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return generate_practice(
        db,
        student_id=user.id,
        count=req.count,
        mode=req.mode,
        tags=req.tags,
    )


@router.post("/submit")
async def practice_submit(
    req: PracticeSubmitRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return await grade_practice(
        db,
        student=user,
        session_id=req.session_id,
        answers=[a.model_dump() for a in req.answers],
        write_mistakes=req.write_mistakes,
    )


@router.get("/sessions")
def practice_sessions(
    limit: int = 30,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return list_practice_sessions(db, student_id=user.id, limit=limit)


@router.get("/sessions/{session_id}")
def practice_session_detail(
    session_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    return get_practice_session(db, student_id=user.id, session_id=session_id)
