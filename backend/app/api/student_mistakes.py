"""学生·错题本 API。"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.services.mistakes import (
    add_mistake,
    delete_mistake,
    export_word,
    import_from_exam,
    list_mistakes,
    update_mistake,
)

router = APIRouter(prefix="/api/student/mistakes", tags=["学生·错题本"])


class MistakeCreate(BaseModel):
    question_snapshot: str
    answer_snapshot: Optional[str] = None
    reason: Optional[str] = None
    question_id: Optional[int] = None
    knowledge_tags: Optional[dict] = None
    add_source: Optional[str] = "manual"


class MistakeUpdate(BaseModel):
    reason: Optional[str] = None
    answer_snapshot: Optional[str] = None


class ImportItem(BaseModel):
    question: str
    answer: Optional[str] = None
    reason: Optional[str] = None
    question_id: Optional[int] = None
    knowledge_tags: Optional[dict] = None


class ImportRequest(BaseModel):
    items: list[ImportItem] = Field(default_factory=list)


@router.get("")
def get_mistakes(
    user: User = Depends(require_student), db: Session = Depends(get_db)
) -> dict[str, Any]:
    rows = list_mistakes(db, user.id)
    return {
        "ok": True,
        "items": [
            {
                "id": m.id,
                "question_snapshot": m.question_snapshot,
                "answer_snapshot": m.answer_snapshot,
                "reason": m.reason,
                "add_source": m.add_source,
                "knowledge_tags": m.knowledge_tags,
                "added_at": m.added_at.isoformat() if m.added_at else None,
            }
            for m in rows
        ],
    }


@router.post("")
def create_mistake(
    req: MistakeCreate,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    m = add_mistake(db, student_id=user.id, **req.model_dump())
    return {"ok": True, "id": m.id}


@router.put("/{mistake_id}")
def patch_mistake(
    mistake_id: int,
    req: MistakeUpdate,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    m = update_mistake(db, mistake_id, user.id, **req.model_dump(exclude_unset=True))
    return {"ok": True, "id": m.id}


@router.delete("/{mistake_id}")
def remove_mistake(
    mistake_id: int,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    delete_mistake(db, mistake_id, user.id)
    return {"ok": True}


@router.post("/import")
def import_mistakes(
    req: ImportRequest,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    items = [i.model_dump() for i in req.items]
    rows = import_from_exam(db, user.id, items)
    return {"ok": True, "count": len(rows)}


@router.get("/export-word")
def export_mistakes_word(
    user: User = Depends(require_student), db: Session = Depends(get_db)
):
    try:
        data = export_word(db, user.id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=mistakes.docx"},
    )
