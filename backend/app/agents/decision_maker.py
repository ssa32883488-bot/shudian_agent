"""决策者（Decision Maker）：轻量规划标记（是否可能要图等）。

解题路径：图内 bank_prefetch 查原题；命中权威直出，未命中再进 ReAct。
寒暄/讲解仍走 ReAct，由系统提示约束。
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from app.agents.tutor_react import wants_drawing_tools
from app.config import get_settings
from app.services.graph_kg import detect_intent
from app.services.mimo import get_mimo

logger = logging.getLogger(__name__)

ACTIONS = (
    "scope",
    "graph",
    "retrieve_textbook",
    "solve",
    "validate",
)


@dataclass
class PlanStep:
    action: str
    reason: str


@dataclass
class DecisionPlan:
    intent: str
    summary: str
    steps: list[PlanStep] = field(default_factory=list)
    needs_drawing: bool = False
    allow_bank_answer: bool = True  # 解题图内预检索可权威直出
    source: str = "heuristic"

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "summary": self.summary,
            "steps": [asdict(s) for s in self.steps],
            "needs_drawing": self.needs_drawing,
            "allow_bank_answer": True,
            "source": self.source,
            "actions": [s.action for s in self.steps],
        }

    def has(self, action: str) -> bool:
        return action in {s.action for s in self.steps}

    def status_line(self) -> str:
        acts = " → ".join(s.action for s in self.steps) or "react"
        return f"{self.summary}（{acts}）"


def _heuristic_plan(text: str, *, has_image: bool) -> DecisionPlan:
    intent = detect_intent(text)
    needs_draw = wants_drawing_tools(text)
    if has_image and intent in {"mixed", "explain"} and len((text or "").strip()) > 40:
        intent = "solve"

    t = (text or "").strip()
    casual = len(t) < 24 and any(
        k in t for k in ("你是谁", "你好", "介绍一下", "能做什么", "干什么", "你会什么")
    )
    if casual:
        intent = "chat"

    # 统一交给 ReAct；steps 仅作痕迹/状态文案
    if intent in {"study_plan", "syllabus"}:
        summary = "学习规划类：ReAct 内可用图谱等工具组织回复"
    elif intent == "explain":
        summary = "讲解类：ReAct 内可用教材/图谱工具"
    elif intent == "chat":
        summary = "寒暄/边界说明：ReAct 直接短回"
    else:
        intent = "solve"
        summary = "解题类：先整理题干查题库工具，未命中再自主求解"
        if needs_draw:
            summary += "（可能需要配图）"

    steps = [
        PlanStep("solve", "统一 ReAct 执行"),
        PlanStep("validate", "交付前轻量评审"),
    ]
    if intent == "solve":
        steps = [PlanStep("scope", "必要时裁剪题量")] + steps

    return DecisionPlan(
        intent=intent,
        summary=summary,
        steps=steps,
        needs_drawing=needs_draw and intent == "solve",
        allow_bank_answer=False,
        source="heuristic",
    )


def _normalize_intent(raw: str) -> str:
    s = (raw or "").strip().lower()
    aliases = {
        "greeting": "chat",
        "knowledge_query": "explain",
        "qa": "explain",
        "homework": "solve",
        "problem": "solve",
    }
    return aliases.get(s, s) if s else "solve"


def _plan_from_llm_json(obj: dict[str, Any], fallback: DecisionPlan) -> DecisionPlan:
    intent = _normalize_intent(str(obj.get("intent") or fallback.intent))
    summary = str(obj.get("summary") or fallback.summary).strip() or fallback.summary
    needs_drawing = bool(obj.get("needs_drawing", False)) or bool(fallback.needs_drawing)
    steps_raw = obj.get("steps") or []
    steps: list[PlanStep] = []
    for s in steps_raw:
        if not isinstance(s, dict) or not s.get("action"):
            continue
        act = str(s["action"])
        if act in {"search_bank", "match_judge", "explain", "study_plan"}:
            # 旧动作映射到统一 solve
            act = "solve"
        if act not in ACTIONS:
            continue
        steps.append(PlanStep(act, str(s.get("reason") or "")))
    if not steps:
        steps = list(fallback.steps)
    # 去重且保证有 solve + validate
    seen: set[str] = set()
    cleaned: list[PlanStep] = []
    for s in steps:
        if s.action in seen:
            continue
        seen.add(s.action)
        cleaned.append(s)
    if "solve" not in seen:
        cleaned.insert(0, PlanStep("solve", "统一 ReAct"))
    if "validate" not in seen:
        cleaned.append(PlanStep("validate", "交付前评审"))
    return DecisionPlan(
        intent=intent,
        summary=summary,
        steps=cleaned,
        needs_drawing=needs_drawing,
        allow_bank_answer=False,
        source="llm",
    )


async def make_decision(
    text: str,
    *,
    has_image: bool = False,
) -> DecisionPlan:
    base = _heuristic_plan(text, has_image=has_image)
    settings = get_settings()
    mimo = get_mimo()
    if mimo.mock or not getattr(settings, "decision_maker_use_llm", True):
        logger.info(
            "decision heuristic intent=%s steps=%s",
            base.intent,
            [s.action for s in base.steps],
        )
        return base

    prompt = (
        "你是数电助学系统的「决策者」。只输出轻量规划 JSON，不要解题。\n"
        "说明：寒暄/讲解/解题一律后续走同一 ReAct；题库由工具按需调用，不要规划 search_bank/match_judge。\n"
        "可选 action：scope, graph, retrieve_textbook, solve, validate\n"
        "规则：必须含 solve 与 validate；解题可加 scope；需要画图时 needs_drawing=true。\n"
        '只输出 JSON：{"intent":"solve|explain|chat|study_plan|syllabus",'
        '"summary":"一句中文","needs_drawing":false,'
        '"steps":[{"action":"...","reason":"..."}]}\n\n'
        f"是否含图片：{has_image}\n"
        f"用户输入：\n{(text or '')[:2000]}"
    )
    try:
        content = await mimo.chat(
            [
                {
                    "role": "system",
                    "content": "你只做任务规划，输出严格 JSON。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        m = re.search(r"\{[\s\S]*\}", content or "")
        if not m:
            return base
        obj = json.loads(m.group(0))
        plan = _plan_from_llm_json(obj, base)
        logger.info(
            "decision llm intent=%s steps=%s",
            plan.intent,
            [s.action for s in plan.steps],
        )
        return plan
    except Exception as exc:
        logger.warning("decision LLM failed, heuristic: %s", exc)
        return base


def plan_from_dict(data: Optional[dict[str, Any]]) -> Optional[DecisionPlan]:
    if not data:
        return None
    steps = [
        PlanStep(str(s.get("action")), str(s.get("reason") or ""))
        for s in (data.get("steps") or [])
        if isinstance(s, dict) and s.get("action")
    ]
    return DecisionPlan(
        intent=str(data.get("intent") or "solve"),
        summary=str(data.get("summary") or ""),
        steps=steps,
        needs_drawing=bool(data.get("needs_drawing")),
        allow_bank_answer=False,
        source=str(data.get("source") or "dict"),
    )
