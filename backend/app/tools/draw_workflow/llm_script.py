# -*- coding: utf-8 -*-
"""按 Skill 提示调用 LLM，输出可解析的脚本 JSON（IR 或 Tier-B 参数）。"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

from app.tools.draw_workflow.skill_loader import load_skill

logger = logging.getLogger(__name__)


def _strip_fences(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        t = "\n".join(lines).strip()
    return t


def _extract_json(text: str) -> str:
    t = _strip_fences(text)
    if t.startswith("{") or t.startswith("["):
        return t
    m = re.search(r"\{[\s\S]*\}", t)
    return m.group(0) if m else t


def build_messages(
    *,
    skill_md: str,
    kind: str,
    brief: str,
    slots: dict[str, Any],
    error_feedback: Optional[str] = None,
) -> list[dict[str, str]]:
    system = (
        "你是数电教材绘图脚本生成器。严格按 skill 的输出格式只输出 JSON，"
        "不要 Markdown 解释，不要代码围栏外的文字。\n\n"
        f"## Skill\n{skill_md}"
    )
    user_parts = [
        f"diagram_kind={kind}",
        f"需求：{brief or '(空)'}",
    ]
    if slots:
        user_parts.append(f"slots={json.dumps(slots, ensure_ascii=False)}")
    if error_feedback:
        user_parts.append(
            "上次脚本校验/出图失败，请输出修正后的完整 JSON。\n"
            f"错误与建议：{error_feedback}"
        )
    user_parts.append("现在只输出 JSON。")
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n".join(user_parts)},
    ]


async def generate_script_async(
    *,
    skill_file: str,
    kind: str,
    brief: str,
    slots: dict[str, Any],
    error_feedback: Optional[str] = None,
) -> str:
    from app.services.mimo import get_mimo

    skill_md = load_skill(skill_file)
    messages = build_messages(
        skill_md=skill_md,
        kind=kind,
        brief=brief,
        slots=slots,
        error_feedback=error_feedback,
    )
    raw = await get_mimo().chat(messages, temperature=0.1)
    return _extract_json(raw)


def _run_generate_script_async(
    *,
    skill_file: str,
    kind: str,
    brief: str,
    slots: dict[str, Any],
    error_feedback: Optional[str] = None,
) -> str:
    import asyncio

    return asyncio.run(
        generate_script_async(
            skill_file=skill_file,
            kind=kind,
            brief=brief,
            slots=slots,
            error_feedback=error_feedback,
        )
    )


def generate_script_sync(
    *,
    skill_file: str,
    kind: str,
    brief: str,
    slots: dict[str, Any],
    error_feedback: Optional[str] = None,
) -> str:
    """同步生成脚本。

    ReAct 工具/强制补图常在已有事件循环内调用；此时不能 ``asyncio.run``，
    改到独立线程里跑 async LLM，避免退回空 ``{}`` 导致 timing_wave 永远缺 signals。
    """
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    kwargs = dict(
        skill_file=skill_file,
        kind=kind,
        brief=brief,
        slots=slots,
        error_feedback=error_feedback,
    )
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return _run_generate_script_async(**kwargs)

    logger.info("generate_script_sync inside running loop; run LLM in worker thread")
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(_run_generate_script_async, **kwargs)
            return fut.result(timeout=120)
    except Exception as exc:  # noqa: BLE001
        logger.warning("threaded script generation failed: %s; fallback slots/empty", exc)
        if slots:
            return json.dumps(slots, ensure_ascii=False)
        return "{}"
