"""Agent 防死循环断路器 + 多题/整卷难度分流。

设计取舍（对照常见 ReAct 防护清单）：
- 采用：max_iterations、全局/空闲超时、输出长度上限、重复动作检测、
  工具调用配额、轨迹日志字段（不再按题号规则裁剪）
- 暂缓：Token 预算精确计量（需各厂商 usage 统一）、语义相似度无进展检测、
  运行中动态升温、完整 Checkpoint 时光倒流（已有 Redis/MemorySaver 预留）
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from app.config import get_settings

logger = logging.getLogger(__name__)


# ---------- 多题 / 整卷（已取消规则裁剪）----------


@dataclass
class TaskScope:
    """题面体量信息；不再按题号规则切分文本。"""

    original_text: str
    scoped_text: str
    estimated_items: int
    answered_items: int
    is_heavy: bool
    reason: str
    notice: str = ""


def estimate_and_scope_question(text: str) -> TaskScope:
    """原样透传题面。拆题/分批只由上游 LLM Plan 负责，此处不做规则切分。"""
    raw = (text or "").strip()
    return TaskScope(
        original_text=raw,
        scoped_text=raw,
        estimated_items=1,
        answered_items=1,
        is_heavy=False,
        reason="passthrough_no_rule_split",
        notice="",
    )


# ---------- 重复动作 / 工具配额 ----------


def _stable_args_key(args: Any) -> str:
    try:
        if isinstance(args, str):
            raw = args
        else:
            raw = json.dumps(args, ensure_ascii=False, sort_keys=True, default=str)
    except Exception:
        raw = str(args)
    return hashlib.md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]


@dataclass
class CircuitBreaker:
    """运行时断路器状态（单次解题会话）。"""

    tool_history: list[tuple[str, str]] = field(default_factory=list)
    tool_counts: dict[str, int] = field(default_factory=dict)
    draw_calls: int = 0
    retrieve_calls: int = 0
    search_calls: int = 0
    nudge_injected: bool = False
    stop_reason: str = ""

    def record_tool(self, name: str, args: Any = None) -> Optional[str]:
        """记录工具调用；若应熔断返回原因字符串。"""
        settings = get_settings()
        key = _stable_args_key(args)
        name = name or "tool"
        self.tool_history.append((name, key))
        self.tool_counts[name] = self.tool_counts.get(name, 0) + 1

        if name.startswith("draw") or name == "draw_with_workflow":
            self.draw_calls += 1
            if self.draw_calls > int(settings.agent_max_draw_calls):
                self.stop_reason = f"绘图工具超额（>{settings.agent_max_draw_calls}）"
                return self.stop_reason

        if name in {"retrieve_multi_rerank"}:
            self.retrieve_calls += 1
            if self.retrieve_calls > int(settings.agent_max_retrieve_calls):
                self.stop_reason = f"教材检索超额（>{settings.agent_max_retrieve_calls}）"
                return self.stop_reason

        if name in {"search_question_bank"}:
            self.search_calls += 1
            if self.search_calls > int(settings.agent_max_search_calls):
                self.stop_reason = f"题库检索超额（>{settings.agent_max_search_calls}）"
                return self.stop_reason

        # 连续 N 次完全相同动作
        n = max(2, int(settings.agent_repeat_action_limit))
        if len(self.tool_history) >= n:
            window = self.tool_history[-n:]
            if len(set(window)) == 1:
                self.stop_reason = f"重复动作检测：连续 {n} 次调用 {name}"
                return self.stop_reason
        return None

    def loop_nudge_message(self) -> str:
        return (
            "系统提示：你已多次重复调用同一工具且参数相同，或工具配额已用尽。"
            "请立刻停止重复工具调用，基于已有信息给出最终中文解答；不要再调用工具。"
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "tool_history": list(self.tool_history[-12:]),
            "tool_counts": dict(self.tool_counts),
            "draw_calls": self.draw_calls,
            "retrieve_calls": self.retrieve_calls,
            "search_calls": self.search_calls,
            "stop_reason": self.stop_reason,
        }


def guard_limits() -> dict[str, Any]:
    s = get_settings()
    return {
        "max_iterations": s.agent_max_iterations,
        "wall_timeout_sec": s.agent_wall_timeout_sec,
        "idle_timeout_sec": s.agent_idle_timeout_sec,
        "max_output_chars": s.agent_max_output_chars,
        "max_draw_calls": s.agent_max_draw_calls,
        "max_retrieve_calls": s.agent_max_retrieve_calls,
        "max_search_calls": s.agent_max_search_calls,
        "repeat_action_limit": s.agent_repeat_action_limit,
        "multi_question_answer_limit": s.multi_question_answer_limit,
    }
