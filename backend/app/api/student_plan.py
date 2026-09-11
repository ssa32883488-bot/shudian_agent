"""学生任务规划：感知优先 → 路由 → 气泡内确认 → Plan 串行执行。"""

from __future__ import annotations

import secrets
import time
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.intent_router import route_task_smart
from app.agents.semantic_router import (
    MAX_ATOMIC_PER_TURN,
    build_perception_summary,
    classify_plan_user_utterance,
    looks_like_continue,
)
from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.services.mimo import get_mimo

router = APIRouter(prefix="/api/student/plan", tags=["学生-任务规划"])

# 进程内计划存储（P0）
_PLANS: dict[str, dict[str, Any]] = {}


class PerceiveRouteRequest(BaseModel):
    text: str = Field("", max_length=100_000)
    image_base64: Optional[str] = None
    has_file: bool = False
    file_kind: Optional[str] = Field(None, description="docx|pdf|ppt")
    file_text: Optional[str] = Field(None, max_length=200_000)
    intent_hint: Optional[str] = None
    thread_id: Optional[str] = None


class RouteRequest(BaseModel):
    """兼容旧接口；新前端请走 /perceive-route。"""

    text: str = Field("", max_length=100_000)
    has_image: bool = False
    has_file: bool = False
    file_kind: Optional[str] = None
    intent_hint: Optional[str] = None
    thread_id: Optional[str] = None


class ConfirmRequest(BaseModel):
    plan_id: str
    selected_ids: list[str] = Field(default_factory=list)
    cancel: bool = False


class IntentRequest(BaseModel):
    plan_id: Optional[str] = None
    thread_id: Optional[str] = None
    text: str = ""


def _store_plan(
    user_id: int,
    route: dict[str, Any],
    thread_id: str | None,
    *,
    perceived_text: str = "",
    perception_summary: str = "",
    stem_image_path: str | None = None,
) -> str:
    plan_id = secrets.token_urlsafe(12)
    _PLANS[plan_id] = {
        "user_id": user_id,
        "thread_id": thread_id or "",
        "created_at": time.time(),
        "status": "pending_confirm",  # pending_confirm|running|await_continue|cancelled|completed
        "confirmed": False,
        "cancelled": False,
        "route": route,
        "perceived_text": perceived_text,
        "perception_summary": perception_summary,
        "stem_image_path": stem_image_path or "",
        "done_ids": [],
        "execute_ids": list(route.get("this_turn_ids") or []),
        "cursor": 0,
    }
    return plan_id


def _user_plans(user_id: int) -> list[tuple[str, dict[str, Any]]]:
    rows = [(pid, p) for pid, p in _PLANS.items() if p["user_id"] == user_id]
    rows.sort(key=lambda x: x[1]["created_at"], reverse=True)
    return rows


def _active_plan(user_id: int, thread_id: str | None = None) -> tuple[str, dict[str, Any]] | None:
    for pid, p in _user_plans(user_id):
        if p.get("cancelled") or p.get("status") in ("cancelled", "completed"):
            continue
        if thread_id and p.get("thread_id") and p["thread_id"] != thread_id:
            continue
        if p.get("status") in ("pending_confirm", "running", "await_continue"):
            return pid, p
    return None


async def _perceive_text(req: PerceiveRouteRequest) -> tuple[str, list[str]]:
    """先读懂再路由：合并文字 / 文件文本 / 图片 OCR。"""
    parts: list[str] = []
    sources: list[str] = []
    if (req.text or "").strip():
        parts.append(req.text.strip())
        sources.append("text")
    if (req.file_text or "").strip():
        parts.append(req.file_text.strip())
        sources.append(f"file:{req.file_kind or 'attachment'}")
    perceived = "\n\n".join(parts).strip()
    if req.image_base64:
        ocr = (await get_mimo().ocr_extract_question(req.image_base64) or "").strip()
        if ocr:
            perceived = f"{perceived}\n\n{ocr}".strip() if perceived else ocr
            sources.append("image_ocr")
    return perceived, sources


def _bubble_brief(route: dict[str, Any], perception_summary: str) -> str:
    from app.agents.semantic_router import _escape_md_noise

    _ = perception_summary  # 不再把感知/路由明细塞进气泡
    items = route.get("items") or []
    turn = set(route.get("this_turn_ids") or [])
    listed = [it for it in items if it.get("id") in turn] or items[:MAX_ATOMIC_PER_TURN]
    lines = [
        "**【Plan 模式 · 待确认】**" if route.get("task_mode") == "plan_execute" else "**任务确认**",
        "",
        f"**任务列表（本回合 {len(listed)}/{MAX_ATOMIC_PER_TURN}）**：",
    ]
    for i, it in enumerate(listed, 1):
        st = it.get("status") or "pending"
        draw = " · 可绘图" if it.get("allow_draw") else ""
        title = _escape_md_noise(str(it.get("title") or it.get("id") or ""))
        kind = _escape_md_noise(str(it.get("kind") or ""))
        lines.append(f"{i}. [{st}] {title}（{kind}{draw}）")
    if route.get("continuation_hint"):
        lines.append("")
        lines.append(f"> {_escape_md_noise(str(route['continuation_hint']))}")
    lines.extend(
        [
            "",
            "请点击下方 **确认执行** / **取消任务**，或直接回复「确认」「取消」。",
        ]
    )
    return "\n".join(lines)


@router.post("/perceive-route")
async def api_perceive_route(
    req: PerceiveRouteRequest,
    user: Annotated[User, Depends(require_student)],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, Any]:
    """感知优先：读懂图/文件/文字 → 再判短 ReAct / 长 Plan。"""
    _ = db
    # 若用户在已有 Plan 下发「继续」短句，走续跑提示
    if looks_like_continue(req.text) and not req.image_base64 and not req.file_text:
        active = _active_plan(user.id, req.thread_id)
        if active:
            pid, p = active
            route = p["route"]
            done = set(p.get("done_ids") or [])
            exec_ids = list(p.get("execute_ids") or route.get("this_turn_ids") or [])
            remaining = [i for i in exec_ids if i not in done]
            return {
                "ok": True,
                "continue": True,
                "plan_id": pid,
                "needs_confirm": False,
                "plan_status": p.get("status"),
                "utterance_intent": "continue",
                "perceived_text": p.get("perceived_text") or "",
                "perception_summary": p.get("perception_summary") or "",
                "bubble_markdown": (
                    f"**Plan 模式仍在进行**\n\n剩余 {len(remaining)} 题。"
                    "回复「继续」执行下一题，或「取消任务」结束。"
                ),
                "route": route,
                "next_item": next(
                    (it for it in route.get("items") or [] if it["id"] == remaining[0]),
                    None,
                )
                if remaining
                else None,
                "remaining_count": len(remaining),
            }

    perceived, _sources = await _perceive_text(req)
    result = await route_task_smart(
        perceived,
        has_image=bool(req.image_base64),
        has_file=req.has_file,
        file_kind=req.file_kind,
        user_intent_hint=req.intent_hint,
    )
    data = result.to_dict()
    summary = build_perception_summary(
        perceived_text=perceived,
        has_image=bool(req.image_base64),
        has_file=req.has_file,
        file_kind=req.file_kind,
        route=result,
    )

    if result.blocked:
        msg = result.block_message or "该内容不适合在本助学场景处理。"
        return {
            "ok": True,
            "continue": False,
            "blocked": True,
            "plan_id": None,
            "needs_confirm": False,
            "plan_status": "blocked",
            "perceived_text": perceived,
            "perception_summary": summary,
            "bubble_markdown": msg,
            "max_tasks": MAX_ATOMIC_PER_TURN,
            "route": data,
        }

    needs_confirm = bool(result.needs_hitl or result.task_mode == "plan_execute")
    plan_id = None
    stem_image_path = None
    if req.image_base64:
        from app.services.reflow import save_reflow_stem_image

        stem_image_path = save_reflow_stem_image(req.image_base64)
    if needs_confirm or result.task_mode == "plan_execute":
        plan_id = _store_plan(
            user.id,
            data,
            req.thread_id,
            perceived_text=perceived,
            perception_summary=summary,
            stem_image_path=stem_image_path,
        )

    # 短任务不写感知/路由明细进气泡；长任务只保留待确认任务列表
    bubble = ""
    if needs_confirm and plan_id:
        bubble = _bubble_brief(data, summary)

    return {
        "ok": True,
        "continue": False,
        "blocked": False,
        "plan_id": plan_id,
        "needs_confirm": needs_confirm,
        "plan_status": "pending_confirm" if needs_confirm else "none",
        "perceived_text": perceived,
        "perception_summary": summary,
        "bubble_markdown": bubble,
        "max_tasks": MAX_ATOMIC_PER_TURN,
        "route": data,
    }


@router.post("/route")
async def api_route(
    req: RouteRequest,
    user: Annotated[User, Depends(require_student)],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, Any]:
    """旧路由（无感知）。保留兼容；新链路请用 perceive-route。"""
    _ = db
    if looks_like_continue(req.text):
        active = _active_plan(user.id, req.thread_id)
        if active:
            pid, p = active
            route = p["route"]
            done = set(p.get("done_ids") or [])
            remaining = [
                it for it in route.get("items") or [] if it["id"] not in done
            ]
            turn = remaining[:MAX_ATOMIC_PER_TURN]
            return {
                "ok": True,
                "continue": True,
                "plan_id": pid,
                "needs_hitl": True,
                "needs_confirm": True,
                "route": {
                    **route,
                    "this_turn_ids": [t["id"] for t in turn],
                    "plan_summary": f"续跑：本回合 {len(turn)} 项，剩余 {len(remaining)} 项",
                },
            }

    result = await route_task_smart(
        req.text,
        has_image=req.has_image,
        has_file=req.has_file,
        file_kind=req.file_kind,
        user_intent_hint=req.intent_hint,
    )
    data = result.to_dict()
    if result.blocked:
        return {
            "ok": True,
            "continue": False,
            "blocked": True,
            "plan_id": None,
            "needs_hitl": False,
            "needs_confirm": False,
            "route": data,
            "message": result.block_message,
        }
    plan_id = None
    if result.needs_hitl or result.task_mode == "plan_execute":
        plan_id = _store_plan(user.id, data, req.thread_id, perceived_text=req.text)
    return {
        "ok": True,
        "continue": False,
        "blocked": False,
        "plan_id": plan_id,
        "needs_hitl": result.needs_hitl,
        "needs_confirm": result.needs_hitl,
        "route": data,
    }


@router.post("/confirm")
def api_confirm(
    req: ConfirmRequest,
    user: Annotated[User, Depends(require_student)],
) -> dict[str, Any]:
    plan = _PLANS.get(req.plan_id)
    if not plan or plan["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="计划不存在或已过期")
    if req.cancel:
        plan["cancelled"] = True
        plan["status"] = "cancelled"
        return {
            "ok": True,
            "cancelled": True,
            "execute_ids": [],
            "plan_status": "cancelled",
            "message": "已取消本次 Plan 任务。",
        }

    route = plan["route"]
    allowed = set(
        route.get("this_turn_ids")
        or [i["id"] for i in (route.get("items") or [])[:MAX_ATOMIC_PER_TURN]]
    )
    selected = [i for i in (req.selected_ids or list(allowed)) if i in allowed]
    if not selected:
        selected = list(allowed)[:MAX_ATOMIC_PER_TURN]
    plan["confirmed"] = True
    plan["status"] = "running"
    plan["execute_ids"] = selected
    plan["cursor"] = 0
    plan["done_ids"] = []
    items = [it for it in route.get("items") or [] if it["id"] in selected]
    first = items[0] if items else None
    return {
        "ok": True,
        "cancelled": False,
        "plan_id": req.plan_id,
        "execute_ids": selected,
        "task_mode": route.get("task_mode"),
        "items": items,
        "next_item": first,
        "plan_status": "running",
        "remaining_count": len(selected),
        "message": (
            f"Plan 模式已启动：共 {len(selected)} 道子任务，"
            "将按 ReAct 逐题解答；每题结束后可继续或取消。"
        ),
    }


@router.post("/intent")
def api_intent(
    req: IntentRequest,
    user: Annotated[User, Depends(require_student)],
) -> dict[str, Any]:
    """解析 Plan 进行中用户发言：confirm|continue|cancel|side_qa。"""
    pid = req.plan_id
    plan = _PLANS.get(pid) if pid else None
    if not plan:
        active = _active_plan(user.id, req.thread_id)
        if active:
            pid, plan = active
    if not plan or plan["user_id"] != user.id:
        return {
            "ok": True,
            "has_plan": False,
            "intent": "side_qa",
            "plan_id": None,
        }
    intent = classify_plan_user_utterance(req.text)
    # 待确认时「继续」视作确认
    if intent == "continue" and plan.get("status") == "pending_confirm":
        intent = "confirm"
    return {
        "ok": True,
        "has_plan": True,
        "intent": intent,
        "plan_id": pid,
        "plan_status": plan.get("status"),
        "plan_stays_open": intent == "side_qa",
    }


@router.post("/next")
def api_next(
    payload: dict[str, Any],
    user: Annotated[User, Depends(require_student)],
) -> dict[str, Any]:
    """取下一道待执行子任务（不关闭 Plan）。"""
    plan_id = str(payload.get("plan_id") or "")
    plan = _PLANS.get(plan_id)
    if not plan or plan["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="计划不存在")
    if plan.get("status") in ("cancelled", "completed"):
        return {
            "ok": True,
            "has_more": False,
            "plan_status": plan["status"],
            "next_item": None,
        }
    done = set(plan.get("done_ids") or [])
    exec_ids = list(plan.get("execute_ids") or [])
    remaining = [i for i in exec_ids if i not in done]
    if not remaining:
        plan["status"] = "completed"
        return {
            "ok": True,
            "has_more": False,
            "plan_status": "completed",
            "next_item": None,
            "message": "全部子任务已完成，Plan 模式已结束。",
        }
    plan["status"] = "running"
    nid = remaining[0]
    item = next((it for it in plan["route"].get("items") or [] if it["id"] == nid), None)
    return {
        "ok": True,
        "has_more": True,
        "plan_status": "running",
        "next_item": item,
        "perceived_text": plan.get("perceived_text") or "",
        "stem_image_path": plan.get("stem_image_path") or "",
        "remaining_count": len(remaining),
        "done_count": len(done),
        "total": len(exec_ids),
    }


@router.post("/mark-done")
def api_mark_done(
    payload: dict[str, Any],
    user: Annotated[User, Depends(require_student)],
) -> dict[str, Any]:
    plan_id = str(payload.get("plan_id") or "")
    done_ids = list(payload.get("done_ids") or [])
    plan = _PLANS.get(plan_id)
    if not plan or plan["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="计划不存在")
    cur = set(plan.get("done_ids") or [])
    cur.update(done_ids)
    plan["done_ids"] = list(cur)
    exec_ids = list(plan.get("execute_ids") or [])
    remaining = [i for i in exec_ids if i not in cur]
    if not remaining:
        plan["status"] = "completed"
    else:
        plan["status"] = "await_continue"
    return {
        "ok": True,
        "done_count": len(cur),
        "remaining_ids": remaining,
        "has_more": bool(remaining),
        "plan_status": plan["status"],
        "message": (
            "本回合全部完成，Plan 模式已关闭。"
            if not remaining
            else f"子任务完成。剩余 {len(remaining)} 题：回复「继续」或点继续；「取消任务」可结束 Plan。"
        ),
    }


@router.post("/cancel")
def api_cancel(
    payload: dict[str, Any],
    user: Annotated[User, Depends(require_student)],
) -> dict[str, Any]:
    plan_id = str(payload.get("plan_id") or "")
    plan = _PLANS.get(plan_id)
    if not plan or plan["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="计划不存在")
    plan["cancelled"] = True
    plan["status"] = "cancelled"
    return {"ok": True, "plan_status": "cancelled", "message": "已取消 Plan 模式。"}
