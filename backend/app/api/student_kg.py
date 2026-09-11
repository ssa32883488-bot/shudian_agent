"""学生·知识图谱可视化与问询 API。"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.api.deps import require_student
from app.db.models import User
from app.services import kg_viz

router = APIRouter(prefix="/api/student/kg", tags=["学生·知识图谱"])


class AskRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(6, ge=1, le=20)


@router.get("/status")
def status(_user: User = Depends(require_student)) -> dict[str, Any]:
    return kg_viz.kg_status()


@router.get("/graph")
def graph(
    chapter: Optional[str] = None,
    q: Optional[str] = None,
    focus: Optional[str] = None,
    limit: int = Query(80, ge=10, le=200),
    depth: int = Query(1, ge=0, le=2),
    _user: User = Depends(require_student),
) -> dict[str, Any]:
    return kg_viz.viz_graph(
        chapter=chapter, q=q, focus=focus, limit=limit, depth=depth
    )


@router.get("/concepts")
def concepts(
    q: str = "",
    limit: int = Query(30, ge=1, le=100),
    _user: User = Depends(require_student),
) -> dict[str, Any]:
    return {"ok": True, "items": kg_viz.search_concepts(q, limit=limit)}


@router.get("/concept")
def concept(
    name: str = Query(..., min_length=1),
    _user: User = Depends(require_student),
) -> dict[str, Any]:
    return kg_viz.concept_detail(name)


@router.post("/ask")
def ask(req: AskRequest, _user: User = Depends(require_student)) -> dict[str, Any]:
    """图谱问询：返回逻辑链/相关题/子图，并给出可带到答疑页的 seed。"""
    return kg_viz.ask_kg(req.text, top_k=req.top_k)
