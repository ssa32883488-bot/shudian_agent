"""语义路由：数据结构、会话短指令识别、感知摘要；不做规则拆题。

约定（产品）：
- 必须先读懂上传内容再路由（OCR/文件文本由 perceive-route 完成）。
- **拆题只由** `intent_router.route_task_smart`（大模型）完成。
- 本模块 `route_task` 仅在 LLM 不可用时降级为「整段一条任务」，绝不按题号切开。
- 单回合 TaskList 执行上限 5（截断，不是拆题）。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Optional

TaskMode = Literal["react_short", "plan_execute"]
TaskType = Literal[
    "solve_one",
    "solve_many",
    "explain",
    "outline_plan",
    "syllabus_expand",
    "chat",
    "unknown",
]

MAX_ATOMIC_PER_TURN = 5

_CONTINUE_HINTS = ("继续", "做后半", "下一题", "下一批", "继续任务", "接着做", "下一道")
_CONFIRM_HINTS = ("确认", "开始", "执行", "好的", "可以", "同意", "开干", "就这样")
_CANCEL_HINTS = ("取消", "终止", "停止", "不要了", "取消任务", "结束任务", "关掉")


@dataclass
class TaskItem:
    id: str
    title: str
    kind: str  # mcq_batch | simplify | big | explain | outline | generate_quiz | chat
    text: str
    allow_draw: bool = False
    status: str = "pending"  # pending | running | done | skipped


@dataclass
class RouteResult:
    task_type: TaskType
    task_mode: TaskMode
    difficulty: str
    capacity_fit: str  # ok | split | soft_refuse
    estimated_items: int
    reason: str
    needs_hitl: bool
    plan_summary: str
    items: list[TaskItem] = field(default_factory=list)
    this_turn_ids: list[str] = field(default_factory=list)
    continuation_hint: str = ""
    answer_this_round: int = 0
    total_detected: int = 0
    source: str = "heuristic"  # heuristic | llm
    blocked: bool = False
    block_message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def looks_like_continue(text: str) -> bool:
    t = (text or "").strip()
    return any(k in t for k in _CONTINUE_HINTS) and len(t) < 40


def looks_like_confirm(text: str) -> bool:
    t = (text or "").strip()
    if not t or len(t) > 24:
        return False
    return any(k in t for k in _CONFIRM_HINTS)


def looks_like_cancel(text: str) -> bool:
    t = (text or "").strip()
    if not t or len(t) > 24:
        return False
    return any(k in t for k in _CANCEL_HINTS)


def classify_plan_user_utterance(
    text: str,
) -> Literal["confirm", "continue", "cancel", "side_qa"]:
    t = (text or "").strip()
    if looks_like_cancel(t):
        return "cancel"
    if looks_like_continue(t):
        return "continue"
    if looks_like_confirm(t):
        return "confirm"
    return "side_qa"


def _escape_md_noise(text: str) -> str:
    """避免 OCR/题干里的 $ _ * \\( 等触发 Markdown/KaTeX（错误公式会整段变红）。"""
    s = re.sub(r"\s+", " ", (text or "").strip())
    s = s.replace("$$", "＄＄").replace("$", "＄")
    s = s.replace("\\(", "(").replace("\\)", ")")
    s = s.replace("\\[", "[").replace("\\]", "]")
    s = s.replace("\\", "＼")
    s = s.replace("*", "∗").replace("_", "＿").replace("`", "'")
    return s


def _plain_preview(text: str, limit: int = 160) -> str:
    preview = re.sub(r"\s+", " ", (text or "").strip())[:limit]
    if len((text or "").strip()) > limit:
        preview += "…"
    return preview.replace("```", "'''")


def build_perception_summary(
    *,
    perceived_text: str,
    has_image: bool,
    has_file: bool,
    file_kind: Optional[str],
    route: RouteResult,
) -> str:
    sources: list[str] = []
    if has_image:
        sources.append("图片识读")
    if has_file:
        sources.append(f"文件（{file_kind or '附件'}）")
    if (perceived_text or "").strip() and not has_image and not has_file:
        sources.append("文字输入")
    if not sources:
        sources.append("用户输入")
    preview = _plain_preview(perceived_text, 160)
    n = route.total_detected or route.estimated_items
    k = route.answer_this_round or len(route.this_turn_ids)
    is_plan = route.task_mode == "plan_execute"
    mode = "Plan 长任务" if is_plan else "短任务 ReAct"
    from_llm = getattr(route, "source", "") == "llm"
    if from_llm and is_plan:
        source = "大模型理解拆题"
    elif from_llm:
        source = "意图判定 → 直达 ReAct"
    else:
        source = "降级（整段一条）"

    lines = [
        f"**已读取**：{' + '.join(sources)}",
        "**内容摘要**：",
        "```text",
        preview,
        "```",
        f"**执行模式**：{mode}",
        f"**路由**：{source}",
    ]
    # 短任务不强调「拆题/题量」；长任务才展示清单规模
    if is_plan:
        lines.insert(-2, f"**识别题量**：约 {n} 道")
        lines.insert(-2, f"**本次解答**：{k} 道（任务列表上限 {MAX_ATOMIC_PER_TURN}）")
        if n > k:
            lines.append(f"**说明**：其余 {n - k} 道可在本回合完成后继续。")
    return "\n".join(lines)


def route_task(
    text: str,
    *,
    has_image: bool = False,
    has_file: bool = False,
    file_kind: Optional[str] = None,
    user_intent_hint: Optional[str] = None,
) -> RouteResult:
    """LLM 不可用时的降级：整段作为一条任务，**绝不按规则拆题**。"""
    _ = (has_image, has_file, file_kind, user_intent_hint)
    raw = (text or "").strip()
    if not raw:
        return RouteResult(
            task_type="unknown",
            task_mode="react_short",
            difficulty="low",
            capacity_fit="ok",
            estimated_items=0,
            reason="未能读出有效题面",
            needs_hitl=False,
            plan_summary="未识别到内容",
            answer_this_round=0,
            total_detected=0,
            source="heuristic",
        )

    if len(raw) < 24 and any(k in raw for k in ("你好", "你是谁", "介绍", "能做什么")):
        return RouteResult(
            task_type="chat",
            task_mode="react_short",
            difficulty="low",
            capacity_fit="ok",
            estimated_items=1,
            reason="寒暄短回复（降级）",
            needs_hitl=False,
            plan_summary="简短回复",
            items=[TaskItem(id="t1", title="寒暄", kind="chat", text=raw)],
            this_turn_ids=["t1"],
            answer_this_round=1,
            total_detected=1,
            source="heuristic",
        )

    title = re.sub(r"\s+", " ", raw.splitlines()[0])[:48] or "整段任务"
    item = TaskItem(
        id="t1",
        title=title,
        kind="big",
        text=raw[:8000],
        allow_draw=False,
    )
    # 长文/文件场景仍进 Plan，但只有 1 项——等 LLM 恢复后再正确拆题
    longish = len(raw) >= 800 or has_file
    return RouteResult(
        task_type="solve_one",
        task_mode="plan_execute" if longish else "react_short",
        difficulty="mid",
        capacity_fit="ok",
        estimated_items=1,
        reason="路由降级：未调用大模型拆题，整段作为一条任务",
        needs_hitl=bool(longish),
        plan_summary="降级整段任务（未拆题）",
        items=[item],
        this_turn_ids=["t1"],
        answer_this_round=1,
        total_detected=1,
        source="heuristic",
    )
