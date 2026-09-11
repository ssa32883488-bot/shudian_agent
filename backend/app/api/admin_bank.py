"""管理·题库维护 API。"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db import get_db
from app.db.models import QuestionBank, User
from app.services.graph_kg import (
    list_concepts as _legacy_list_concepts,
    match_concepts_from_text,
    problems_for_concept,
    _load_full_graph,
)
from app.services.practice import _tag_hit
from app.services.question_bank import search_question_bank, sync_question_to_chroma

router = APIRouter(prefix="/api/admin/bank", tags=["管理·题库"])

DEFAULT_LATEST = 20
MAX_LIMIT = 50


class BankCreate(BaseModel):
    content: str
    answer: str
    analysis: Optional[str] = None
    knowledge_tags: Optional[dict] = None
    source: Optional[str] = None


class BankUpdate(BankCreate):
    status: Optional[str] = None


def _row_to_item(q: QuestionBank, *, score: Optional[float] = None, match_via: Optional[str] = None) -> dict[str, Any]:
    tags = q.knowledge_tags if isinstance(q.knowledge_tags, dict) else {}
    item: dict[str, Any] = {
        "id": q.id,
        "content": q.content,
        "answer": q.answer,
        "analysis": q.analysis,
        "knowledge_tags": q.knowledge_tags,
        "source": q.source,
        "status": q.status,
        "needs_kg_review": bool(tags.get("needs_kg_review")),
    }
    if score is not None:
        item["score"] = round(float(score), 4)
    if match_via:
        item["match_via"] = match_via
    return item


def _latest_rows(db: Session, *, limit: int, status: str) -> list[QuestionBank]:
    stmt = select(QuestionBank).order_by(QuestionBank.id.desc()).limit(limit)
    if status != "all":
        stmt = stmt.where(QuestionBank.status == status)
    return list(db.scalars(stmt).all())


def _keyword_rows(db: Session, q: str, *, limit: int, status: str) -> list[QuestionBank]:
    needle = (q or "").strip()[:60]
    if not needle:
        return []
    stmt = (
        select(QuestionBank)
        .where(
            or_(
                QuestionBank.content.ilike(f"%{needle}%"),
                QuestionBank.answer.ilike(f"%{needle}%"),
                QuestionBank.source.ilike(f"%{needle}%"),
            )
        )
        .order_by(QuestionBank.id.desc())
        .limit(limit)
    )
    if status != "all":
        stmt = stmt.where(QuestionBank.status == status)
    return list(db.scalars(stmt).all())


def _concept_names(prefix: str = "", limit: int = 40) -> list[str]:
    """图谱 Concept 名称（含别名命中）。"""
    try:
        g = _load_full_graph()
        concepts = (g.get("nodes") or {}).get("Concept") or []
    except Exception:
        # 兼容旧图结构
        try:
            return [n for n in _legacy_list_concepts() if not prefix or prefix in n][:limit]
        except Exception:
            return []

    p = (prefix or "").strip()
    out: list[str] = []
    seen: set[str] = set()
    for c in concepts:
        name = (c.get("name") or "").strip()
        if not name or name in seen:
            continue
        aliases = [str(a) for a in (c.get("aliases") or []) if a]
        if p and p not in name and not any(p in a for a in aliases):
            continue
        seen.add(name)
        out.append(name)
        if len(out) >= limit:
            break
    return out


def _kg_problem_ids(concept: str, *, limit: int = 40) -> list[str]:
    rows = problems_for_concept(concept, limit=limit)
    return [str(r.get("problem_id") or "").strip() for r in rows if r.get("problem_id")]


def _rows_for_concept(db: Session, concept: str, *, limit: int, status: str) -> list[tuple[QuestionBank, float]]:
    """知识点 → 题库题：图谱 problem_id / 标签命中。"""
    concept = (concept or "").strip()
    if not concept:
        return []

    pid_set = set(_kg_problem_ids(concept, limit=80))
    weak = [concept]
    # 也纳入别名匹配到的规范名
    matched = match_concepts_from_text(concept, top_k=5)
    for m in matched:
        name = (m.get("name") or "").strip()
        if name and name not in weak:
            weak.append(name)
            pid_set.update(_kg_problem_ids(name, limit=40))

    stmt = select(QuestionBank).order_by(QuestionBank.id.desc()).limit(400)
    if status != "all":
        stmt = stmt.where(QuestionBank.status == status)
    pool = list(db.scalars(stmt).all())

    scored: list[tuple[QuestionBank, float]] = []
    for row in pool:
        tags = row.knowledge_tags if isinstance(row.knowledge_tags, dict) else {}
        pid = str(tags.get("problem_id") or tags.get("exercise_id") or tags.get("example_id") or "").strip()
        score = 0.0
        via_graph = bool(pid and pid in pid_set)
        via_tag = _tag_hit(tags, weak)
        if via_graph:
            score += 0.92
        if via_tag:
            score += 0.75
        # 题干里直接出现知识点名
        blob = f"{row.content or ''}\n{row.source or ''}"
        if any(w and w in blob for w in weak):
            score += 0.35
        if score <= 0:
            continue
        scored.append((row, min(score, 0.99)))

    scored.sort(key=lambda x: (-x[1], -x[0].id))
    return scored[:limit]


def _search_bank(
    db: Session,
    *,
    q: str,
    concept: Optional[str],
    limit: int,
    status: str,
) -> tuple[list[dict[str, Any]], list[str], str]:
    """返回 (items, matched_concepts, mode_label)。"""
    q = (q or "").strip()
    concept = (concept or "").strip() or None
    limit = max(1, min(int(limit or DEFAULT_LATEST), MAX_LIMIT))

    if not q and not concept:
        rows = _latest_rows(db, limit=limit, status=status)
        return [_row_to_item(r) for r in rows], [], "latest"

    matched_concepts: list[str] = []
    if concept:
        matched_concepts = [concept]
    elif q:
        matched_concepts = [m["name"] for m in match_concepts_from_text(q, top_k=6) if m.get("name")]

    # 合并：语义检索 + 关键词 + 图谱知识点
    by_id: dict[int, dict[str, Any]] = {}

    if q:
        try:
            sem = search_question_bank(db, q, top_k=limit)
        except Exception:
            sem = []
        for hit in sem:
            qid = int(hit.get("question_id") or 0)
            if not qid:
                continue
            row = db.get(QuestionBank, qid)
            if not row:
                continue
            if status != "all" and row.status != status:
                continue
            by_id[qid] = _row_to_item(
                row,
                score=float(hit.get("score") or 0.0),
                match_via="semantic",
            )

        for row in _keyword_rows(db, q, limit=limit, status=status):
            prev = by_id.get(row.id)
            if prev:
                prev["score"] = max(float(prev.get("score") or 0), 0.55)
                if prev.get("match_via") != "semantic":
                    prev["match_via"] = "keyword"
            else:
                by_id[row.id] = _row_to_item(row, score=0.55, match_via="keyword")

    concepts_to_query = list(dict.fromkeys(([concept] if concept else []) + matched_concepts + ([q] if q else [])))
    for cname in concepts_to_query:
        if not cname:
            continue
        for row, score in _rows_for_concept(db, cname, limit=limit, status=status):
            prev = by_id.get(row.id)
            if prev:
                prev["score"] = max(float(prev.get("score") or 0), float(score))
                via = prev.get("match_via") or ""
                if "concept" not in via:
                    prev["match_via"] = f"{via}+concept".strip("+")
            else:
                by_id[row.id] = _row_to_item(row, score=score, match_via="concept")

    items = sorted(
        by_id.values(),
        key=lambda x: (-float(x.get("score") or 0), -int(x.get("id") or 0)),
    )[:limit]
    mode = "concept" if concept and not q else "search"
    return items, matched_concepts[:8], mode


@router.get("/concepts")
def suggest_concepts(
    q: str = Query("", description="知识点前缀/片段"),
    limit: int = Query(20, ge=1, le=50),
    user: User = Depends(require_admin),
):
    """图谱知识点建议（供搜索栏联想）。"""
    _ = user
    names = _concept_names(q, limit=limit)
    return {"ok": True, "items": names}


@router.get("")
def list_bank(
    q: Optional[str] = Query(None, description="关键词或自然语言；空则返回最新入库"),
    concept: Optional[str] = Query(None, description="指定知识点（图谱搜索）"),
    limit: int = Query(DEFAULT_LATEST, ge=1, le=MAX_LIMIT),
    status: str = Query("active", description="active|disabled|all"),
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """题库列表：默认最新入库；带 q/concept 时做关键词+向量+图谱联合检索。"""
    _ = user
    if status not in {"active", "disabled", "all"}:
        status = "active"
    items, matched_concepts, mode = _search_bank(
        db, q=q or "", concept=concept, limit=limit, status=status
    )
    return {
        "ok": True,
        "mode": mode,
        "query": q or "",
        "concept": concept,
        "matched_concepts": matched_concepts,
        "limit": limit,
        "items": items,
    }


@router.post("")
def create_bank(
    req: BankCreate, user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    _ = user
    q = QuestionBank(**req.model_dump(), status="active")
    db.add(q)
    db.flush()
    sync_question_to_chroma(q)
    db.commit()
    db.refresh(q)
    return {"ok": True, "id": q.id}


@router.put("/{question_id}")
def update_bank(
    question_id: int,
    req: BankUpdate,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    _ = user
    q = db.get(QuestionBank, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    sync_question_to_chroma(q)
    db.commit()
    return {"ok": True}


@router.delete("/{question_id}")
def delete_bank(
    question_id: int, user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    _ = user
    q = db.get(QuestionBank, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="题目不存在")
    q.status = "disabled"
    sync_question_to_chroma(q)
    db.commit()
    return {"ok": True}
