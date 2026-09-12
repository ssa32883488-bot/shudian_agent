# -*- coding: utf-8 -*-
"""出图循环：生成脚本 → 结构校验 → 驱动工具 → 失败则反馈重试（最多 max_retries 次）。"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

from app.tools.draw_workflow.catalog import get_kind
from app.tools.draw_workflow.llm_script import generate_script_sync
from app.tools.draw_workflow.runners import dispatch_runner
from app.tools.draw_workflow.verify import parse_script, verify_structure
from app.tools.draw_workflow.truth_fallback import fallback_truth_table_script
from app.tools.draw_workflow.wave_fallback import fallback_timing_wave_script
from app.tools.draw_workflow.logic_fallback import fallback_logic_dag_script
from app.tools.gateway import ToolResult, wrap_err

logger = logging.getLogger(__name__)


def _deterministic_fallback(kind: str, brief: str, slots: dict[str, Any]) -> Optional[str]:
    if kind == "timing_wave":
        return fallback_timing_wave_script(brief=brief, slots=slots)
    if kind == "truth_table":
        return fallback_truth_table_script(brief=brief, slots=slots)
    if kind == "logic_dag":
        return fallback_logic_dag_script(brief=brief, slots=slots)
    return None


def _slots_as_script(kind: str, slots: dict[str, Any]) -> Optional[str]:
    """若 slots 已含足够字段，可跳过 LLM。"""
    if not slots:
        return None
    # 完整 IR 已在 slots
    if kind == "logic_dag" and slots.get("gates") and slots.get("inputs"):
        return json.dumps(slots, ensure_ascii=False)
    if kind == "timing_wave" and slots.get("signals"):
        return json.dumps(slots, ensure_ascii=False)
    if kind == "state_machine" and slots.get("states") and slots.get("transitions"):
        return json.dumps(slots, ensure_ascii=False)
    if kind == "truth_table" and slots.get("rows"):
        return json.dumps(slots, ensure_ascii=False)
    if kind == "kmap" and slots.get("minterms") is not None:
        return json.dumps(slots, ensure_ascii=False)
    if kind == "seven_seg" and "digit" in slots:
        return json.dumps(slots, ensure_ascii=False)
    if kind == "char_curve" and slots.get("curve"):
        return json.dumps(slots, ensure_ascii=False)
    if kind == "msi_design":
        # 完整网表可跳过 LLM；禁止「空 template」短路
        if slots.get("components") and slots.get("connections"):
            return json.dumps(slots, ensure_ascii=False)
        if slots.get("logic_first") and slots.get("components") and slots.get("connections"):
            return json.dumps(slots, ensure_ascii=False)
        return None
    return None


def run_draw_loop(
    *,
    kind: str,
    brief: str,
    slots: dict[str, Any],
    script: Optional[str] = None,
    max_retries: int = 3,
) -> ToolResult:
    spec = get_kind(kind)
    if not spec:
        return wrap_err(f"未注册图类：{kind}", tier="W", engine="draw_workflow")

    feedback: Optional[str] = None
    last_err = "未知错误"
    attempts_log: list[dict[str, Any]] = []
    used_fallback = False

    # 首次：优先显式 script → slots 完备 → 确定性兜底 → LLM
    pending_script = (script or "").strip() or _slots_as_script(kind, slots)
    if not pending_script:
        fb = _deterministic_fallback(kind, brief, slots)
        if fb:
            pending_script = fb
            used_fallback = True
            logger.info("%s using deterministic fallback IR", kind)

    # 含首次在内最多 max_retries 次尝试（默认 3；调用方 clamp 到 1..3）
    for attempt in range(max_retries):
        if pending_script:
            raw = pending_script
            pending_script = None
            if used_fallback and attempt == 0:
                source = "fallback"
                used_fallback = False
            else:
                source = "given" if attempt == 0 and script else "slots"
        else:
            try:
                raw = generate_script_sync(
                    skill_file=spec.skill_file,
                    kind=kind,
                    brief=brief,
                    slots=slots,
                    error_feedback=feedback,
                )
                source = "llm"
            except Exception as e:  # noqa: BLE001
                logger.exception("script generation failed")
                fb = _deterministic_fallback(kind, brief, slots)
                if fb:
                    raw = fb
                    source = "fallback"
                else:
                    return wrap_err(
                        f"脚本生成失败：{e}",
                        tier="W",
                        engine="draw_workflow",
                    )

        parsed = parse_script(raw)
        if not parsed.ok:
            feedback = parsed.feedback
            last_err = feedback
            attempts_log.append({"attempt": attempt, "source": source, "error": feedback})
            if source != "fallback":
                fb = _deterministic_fallback(kind, brief, slots)
                if fb:
                    pending_script = fb
                    used_fallback = True
            continue

        checked = verify_structure(kind, parsed.data or {})
        if not checked.ok:
            feedback = checked.feedback
            last_err = feedback
            attempts_log.append({"attempt": attempt, "source": source, "error": feedback})
            if source != "fallback":
                fb = _deterministic_fallback(kind, brief, slots)
                if fb:
                    pending_script = fb
                    used_fallback = True
            continue

        payload = dict(checked.data or {})
        payload["_brief"] = brief or ""
        res = dispatch_runner(kind, payload)
        if res.ok:
            res.meta = dict(res.meta or {})
            res.meta.update(
                {
                    "workflow": "draw_with_workflow",
                    "kind": kind,
                    "attempt": attempt,
                    "source": source,
                    "brief": (brief or "")[:200],
                    "attempts": attempts_log,
                }
            )
            return res

        feedback = res.error or "出图失败"
        last_err = feedback
        attempts_log.append({"attempt": attempt, "source": source, "error": feedback})
        logger.info("draw loop retry kind=%s attempt=%s err=%s", kind, attempt, feedback)
        if source != "fallback":
            fb = _deterministic_fallback(kind, brief, slots)
            if fb:
                pending_script = fb
                used_fallback = True

    return wrap_err(
        f"draw_with_workflow({kind}) 经 {max_retries} 次检验仍失败：{last_err}",
        tier="W",
        engine="draw_workflow",
    )
