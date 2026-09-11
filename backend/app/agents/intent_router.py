"""意图识别与智能路由节点（LLM）。

感知文本就绪后调用本节点：判意图、拆原子任务清单、拦截无关/敏感内容。
失败或 mock 时回退 `semantic_router.route_task` 启发式。
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

from app.agents.semantic_router import (
    MAX_ATOMIC_PER_TURN,
    RouteResult,
    TaskItem,
    route_task,
)
from app.config import get_settings
from app.services.mimo import get_mimo

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 提示词（权威文案；System+User 合计约 1800 字；改规则优先改这里）
# ---------------------------------------------------------------------------

ROUTER_SYSTEM_PROMPT = """\
你是「数字电子技术」助学智能体的【意图识别与智能路由】节点。输入是已感知文本（OCR/文件抽取/用户打字）及元信息。只输出一个 JSON 对象，不要 Markdown 围栏或其它说明。

# 职责
判定主意图 → 选择短/长执行模式 → 必要时拆出原子任务清单 → 安全拦截。禁止解题、写解析、展开讲课、画图、编造题面中没有的小题。

# 主意图（择一为 task_type）
- explain：问概念/原理/区别/如何理解；没有完整待解算式或作答指令
- solve_one / solve_many：有题面或作答要求（化简、求值、选择填空、真值表、最小项、分析电路、画图解题等）
- outline_plan：大纲/教学进度/考试范围梳理，或复习路径「先补什么」
- syllabus_expand：明确要求按材料出题/出练习（可与梳理拆成两项）
- chat：你好、你是谁、能做什么
- unknown：内容残缺或无法判断——说明缺什么，给可重试动作，勿硬拆
易混：教材讲解页无题号作答→explain；「这题怎么做」+题面→solve；「先讲再做」+完整题面→主类型 solve，text 可注明先讲考点；总题干「用××法化简下列…」是解题共享要求，不是讲解，且不得单独成项。

# 执行模式
- react_short（needs_hitl=false）：寒暄、单点讲解、单题、≤2 个短原子项
- plan_execute（needs_hitl=true）：≥3 个原子项、整卷/多题照片、大纲/出题/长文件
capacity_fit：ok | split（总数超单回合上限仍输出全部 items）| soft_refuse（仅配合拦截）
difficulty：low | mid | high

# 输入形态（类推未穷举情况）
单问文字→短；多概念/多题→拆项，多则长；单题图→solve 短；多题图或试卷文件→solve_many 长；大纲/课件目录→outline 或 syllabus 长；intent_hint 作参考，正文证据优先。

# 拆项铁律
每项 text 必须自包含（下游只拿该项就能执行）；title 短可读。解题：总题干并入各小题，按 (1)(2)… 分项。讲解：一问或一概念一项。大纲：默认 1×outline，出题加 generate_quiz，非用户要求勿逐章拆几十项。识别到 N 项就全放进 items（可超过单回合上限），total_detected=N。
kind：explain | simplify | mcq_batch | big | outline | generate_quiz | chat
allow_draw：需要卡诺图/逻辑电路图/波形/时序/状态图时为 true

# 拦截（blocked=true，items 置空，填写 block_message）
色情与性剥削、暴力仇恨、自伤方法、违法实操、代考或可提交的整份答卷、隐私窃取、政治煽动、明显与学习无关的灌水。寒暄不拦。轻微沾边的电路常识尽量归入讲解/解题。

# 输出字段
blocked, block_message, task_type, task_mode, difficulty, capacity_fit, needs_hitl, reason（分流依据一句）, plan_summary（给学生看的计划一句）, total_detected, items[{title,kind,text,allow_draw}]
"""

ROUTER_USER_TEMPLATE = """\
对下列已感知内容做意图路由。先定主意图，再定模式与清单；讲解勿误判解题；总题干勿单独成项。

元信息：图片OCR={has_image}；文件={has_file}（{file_kind}）；意图提示={intent_hint}；单回合上限={max_per_turn}（仍输出全部原子项）

已感知文本：
\"\"\"
{perceived_text}
\"\"\"

参考：单概念问→explain短；多概念分讲→explain长；单题→solve_one短；总要求+(1)(2)…→solve_many且总要求写入每项；大纲梳理→outline_plan；还要出题→syllabus_expand；代考/敏感/无关灌水→blocked。

只输出 JSON。
"""


def _extract_json_obj(content: str) -> Optional[dict[str, Any]]:
    raw = (content or "").strip()
    if not raw:
        return None
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def _norm_task_type(v: str) -> str:
    allowed = {
        "solve_one",
        "solve_many",
        "explain",
        "outline_plan",
        "syllabus_expand",
        "chat",
        "unknown",
    }
    x = (v or "unknown").strip()
    return x if x in allowed else "unknown"


def _norm_mode(v: str) -> str:
    return "plan_execute" if (v or "").strip() == "plan_execute" else "react_short"


def _norm_kind(v: str) -> str:
    allowed = {
        "mcq_batch",
        "simplify",
        "big",
        "explain",
        "outline",
        "generate_quiz",
        "chat",
    }
    x = (v or "big").strip()
    return x if x in allowed else "big"


def _finalize_caps(result: RouteResult) -> RouteResult:
    """统一本回合 ≤5，并补 continuation_hint。"""
    items = list(result.items or [])
    total = max(int(result.total_detected or 0), len(items), int(result.estimated_items or 0))
    result.total_detected = total
    result.estimated_items = total
    if result.blocked:
        result.items = []
        result.this_turn_ids = []
        result.answer_this_round = 0
        result.capacity_fit = "soft_refuse"
        result.needs_hitl = False
        result.task_mode = "react_short"
        return result

    turn = items[:MAX_ATOMIC_PER_TURN]
    result.items = items
    result.this_turn_ids = [it.id for it in turn]
    result.answer_this_round = len(turn)
    if total > MAX_ATOMIC_PER_TURN:
        result.capacity_fit = "split"
        if not result.continuation_hint:
            result.continuation_hint = (
                f"共约 {total} 道，本回合 TaskList 上限 {MAX_ATOMIC_PER_TURN} 道；"
                "每完成一题后可「继续」或「取消任务」。"
            )
        result.task_mode = "plan_execute"
        result.needs_hitl = True
        # 分批时不要把讲解/大纲误改成 solve_many
        if result.task_type == "solve_one":
            result.task_type = "solve_many"
        elif result.task_type in ("chat", "unknown"):
            if items and all(it.kind == "explain" for it in items):
                result.task_type = "explain"
            elif items and any(it.kind == "generate_quiz" for it in items):
                result.task_type = "syllabus_expand"
            elif items and any(it.kind == "outline" for it in items):
                result.task_type = "outline_plan"
            else:
                result.task_type = "solve_many"
        # explain / outline_plan / syllabus_expand / solve_many：保持原类型
        if result.task_type == "explain":
            result.continuation_hint = (
                f"共约 {total} 个讲解点，本回合上限 {MAX_ATOMIC_PER_TURN} 个；"
                "每完成一项后可「继续」或「取消任务」。"
            )
    elif result.task_mode == "plan_execute":
        result.needs_hitl = True
        result.capacity_fit = result.capacity_fit or "ok"
    else:
        result.capacity_fit = result.capacity_fit if result.capacity_fit in ("ok", "split") else "ok"
    return result


def _items_from_llm(obj: dict[str, Any], fallback_text: str) -> list[TaskItem]:
    """完全信任模型输出的 items，不做规则拆题/题干合并。"""
    raw_items = obj.get("items") or []
    out: list[TaskItem] = []
    if isinstance(raw_items, list):
        for i, it in enumerate(raw_items):
            if not isinstance(it, dict):
                continue
            text = str(it.get("text") or "").strip()
            title = str(it.get("title") or "").strip()
            if not text and not title:
                continue
            if not text:
                text = title
            if not title:
                title = (text.splitlines()[0] if text.splitlines() else f"第 {i+1} 题")[:80]
            out.append(
                TaskItem(
                    id=f"t{i+1}",
                    title=title[:80],
                    kind=_norm_kind(str(it.get("kind") or "big")),
                    text=text[:4000],
                    allow_draw=bool(it.get("allow_draw")),
                    status="pending",
                )
            )
    if not out and (fallback_text or "").strip() and not obj.get("blocked"):
        out = [
            TaskItem(
                id="t1",
                title=(fallback_text.strip().splitlines()[0][:48] or "任务"),
                kind="big",
                text=fallback_text.strip()[:4000],
            )
        ]
    return out


def route_result_from_llm_json(
    obj: dict[str, Any],
    *,
    perceived_text: str,
) -> RouteResult:
    blocked = bool(obj.get("blocked"))
    block_message = str(obj.get("block_message") or "").strip()
    if blocked:
        return _finalize_caps(
            RouteResult(
                task_type="unknown",
                task_mode="react_short",
                difficulty="low",
                capacity_fit="soft_refuse",
                estimated_items=0,
                reason=str(obj.get("reason") or "内容被安全/范围策略拦截"),
                needs_hitl=False,
                plan_summary="无法处理该请求",
                items=[],
                this_turn_ids=[],
                answer_this_round=0,
                total_detected=0,
                source="llm",
                blocked=True,
                block_message=block_message
                or "该内容不适合在本助学场景处理。请换一道数电相关的学习问题。",
            )
        )

    items = _items_from_llm(obj, perceived_text)
    task_mode = _norm_mode(str(obj.get("task_mode") or "react_short"))
    task_type = _norm_task_type(str(obj.get("task_type") or "unknown"))
    # 多题强制 plan；讲解多知识点同样走 plan，但保持 explain
    if len(items) >= 3:
        task_mode = "plan_execute"
        if task_type == "solve_one":
            task_type = "solve_many"
        elif task_type == "unknown":
            # 若全是讲解项，归 explain；否则按解题多题
            if items and all(it.kind == "explain" for it in items):
                task_type = "explain"
            else:
                task_type = "solve_many"
    needs_hitl = bool(obj.get("needs_hitl")) or task_mode == "plan_execute"
    total = int(obj.get("total_detected") or len(items) or 0)

    return _finalize_caps(
        RouteResult(
            task_type=task_type,  # type: ignore[arg-type]
            task_mode=task_mode,  # type: ignore[arg-type]
            difficulty=str(obj.get("difficulty") or "mid"),
            capacity_fit=str(obj.get("capacity_fit") or "ok"),
            estimated_items=total,
            reason=str(obj.get("reason") or "LLM 意图路由"),
            needs_hitl=needs_hitl,
            plan_summary=str(obj.get("plan_summary") or "任务规划"),
            items=items,
            continuation_hint=str(obj.get("continuation_hint") or ""),
            answer_this_round=0,
            total_detected=total,
            source="llm",
            blocked=False,
            block_message="",
        )
    )


async def route_task_smart(
    text: str,
    *,
    has_image: bool = False,
    has_file: bool = False,
    file_kind: Optional[str] = None,
    user_intent_hint: Optional[str] = None,
) -> RouteResult:
    """LLM 意图判定；长任务才拆清单。短任务返回 react_short 后由前端直达 ReAct。"""
    fallback = route_task(
        text,
        has_image=has_image,
        has_file=has_file,
        file_kind=file_kind,
        user_intent_hint=user_intent_hint,
    )
    settings = get_settings()
    mimo = get_mimo()
    if mimo.mock or not getattr(settings, "intent_router_use_llm", True):
        fallback.source = "heuristic"
        return fallback

    perceived = (text or "").strip()
    if not perceived:
        fallback.source = "heuristic"
        return fallback

    user_prompt = ROUTER_USER_TEMPLATE.format(
        has_image=str(bool(has_image)).lower(),
        has_file=str(bool(has_file)).lower(),
        file_kind=file_kind or "none",
        intent_hint=user_intent_hint or "",
        max_per_turn=MAX_ATOMIC_PER_TURN,
        perceived_text=perceived[:12000],
    )
    try:
        content = await mimo.chat(
            [
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )
        obj = _extract_json_obj(content or "")
        if not obj:
            logger.warning("intent router: empty/invalid JSON, fallback heuristic")
            fallback.source = "heuristic"
            return fallback
        result = route_result_from_llm_json(obj, perceived_text=perceived)
        logger.info(
            "intent router llm type=%s mode=%s items=%s blocked=%s",
            result.task_type,
            result.task_mode,
            len(result.items),
            result.blocked,
        )
        return result
    except Exception as exc:
        logger.warning("intent router LLM failed, heuristic: %s", exc)
        fallback.source = "heuristic"
        return fallback
