"""Mock / 真实 ChatModel：支持 bind_tools，供 LangGraph ReAct 使用。"""

from __future__ import annotations

import json
import re
import uuid
from typing import Any, Optional, Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import BaseTool
from pydantic import Field

from app.tools.draw.kmap import parse_sum_of_minterms


class MockTutorChatModel(BaseChatModel):
    """无 Key 时：启发式决定 tool_calls，再生成最终解答。"""

    tools: list[BaseTool] = Field(default_factory=list)
    bound_tools: list[Any] = Field(default_factory=list)

    @property
    def _llm_type(self) -> str:
        return "mock-tutor-react"

    def bind_tools(self, tools: Sequence[BaseTool], **kwargs: Any) -> MockTutorChatModel:
        return self.model_copy(update={"tools": list(tools), "bound_tools": list(tools)})

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # 若已有 ToolMessage，则产出最终答案
        tool_msgs = [m for m in messages if isinstance(m, ToolMessage)]
        if tool_msgs:
            urls = []
            notes = []
            for tm in tool_msgs:
                try:
                    data = json.loads(tm.content)
                    if data.get("artifact_url"):
                        urls.append(data["artifact_url"])
                    if data.get("meta"):
                        notes.append(json.dumps(data["meta"], ensure_ascii=False)[:200])
                    if data.get("results"):
                        notes.append(f"题库命中 {len(data['results'])} 条")
                    if data.get("hits"):
                        notes.append(f"教材摘录 {len(data['hits'])} 条")
                except Exception:
                    notes.append(str(tm.content)[:120])

            # 用 DRAW 占位定位置，系统 finalize 再回填真实图
            from app.services.draw_blocks import (
                infer_kind_from_artifact,
                make_draw_marker,
            )

            user_q = ""
            for m in reversed(messages):
                if isinstance(m, HumanMessage):
                    user_q = str(m.content)
                    break
            markers: list[str] = []
            for tm in tool_msgs:
                try:
                    data = json.loads(tm.content)
                    url = data.get("artifact_url")
                    if not url:
                        continue
                    kind = infer_kind_from_artifact(
                        "",
                        url,
                        tm.name or "",
                    )
                    desc = (
                        (data.get("meta") or {}).get("title")
                        or (data.get("meta") or {}).get("desc")
                        or "本题配图"
                    )
                    markers.append(make_draw_marker(kind, str(desc)))
                except Exception:
                    continue

            if any("kmap" in (mk or "") for mk in markers) or "卡诺" in user_q:
                mk = next((x for x in markers if "kmap" in x), None) or (
                    make_draw_marker("kmap", "本题卡诺图") if urls else ""
                )
                answer = (
                    f"## 卡诺图化简\n\n"
                    f"### 第一步：审题\n{user_q[:120] or '（见题面）'}\n\n"
                    f"### 第二步：画卡诺图并圈组\n"
                    f"按下图填入最小项并圈组：\n\n{mk}\n\n"
                    f"### 第三步：圈组分析\n根据圈组写出乘积项并合并。\n\n"
                    f"### 第四步：化简结果\n写出最简与或式；本回答为 Mock，仅供联调。"
                )
            elif markers:
                answer = (
                    "【ReAct·Mock】已调用工具完成分析。\n\n"
                    + ("\n".join(f"- {n}" for n in notes) if notes else "- （无附加元数据）")
                    + "\n\n### 图示\n\n"
                    + "\n\n".join(markers)
                    + "\n\n请结合图示与教材核对；本回答为 AI 现解，仅供参考。"
                )
            else:
                answer = (
                    "【ReAct·Mock】已调用工具完成分析。\n\n"
                    + ("\n".join(f"- {n}" for n in notes) if notes else "- （无附加元数据）")
                    + "\n\n请结合图示与教材核对；本回答为 AI 现解，仅供参考。"
                )
            msg = AIMessage(content=answer)
            return ChatResult(generations=[ChatGeneration(message=msg)])

        # 首轮：根据用户题面规划工具
        user_text = ""
        for m in reversed(messages):
            if isinstance(m, HumanMessage):
                user_text = str(m.content)
                break

        calls = self._plan_tools(user_text)
        if calls:
            msg = AIMessage(content="需要调用工具辅助解答。", tool_calls=calls)
        else:
            msg = AIMessage(
                content=(
                    f"【ReAct·Mock】针对「{user_text[:60]}」："
                    "未触发专用绘图工具，给出文字分步提示。"
                    "1) 审题 2) 定位知识点 3) 推导 4) 校验。"
                )
            )
        return ChatResult(generations=[ChatGeneration(message=msg)])

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        return self._generate(messages, stop=stop, **kwargs)

    def _plan_tools(self, text: str) -> list[dict[str, Any]]:
        t = text or ""
        calls: list[dict[str, Any]] = []
        tool_names = {x.name for x in self.tools}

        def add(name: str, args: dict[str, Any]) -> None:
            if name not in tool_names:
                return
            calls.append(
                {
                    "name": name,
                    "args": args,
                    "id": f"call_{uuid.uuid4().hex[:10]}",
                    "type": "tool_call",
                }
            )

        # 卡诺图
        if any(k in t for k in ("卡诺图", "K 图", "Kmap", "kmap", "化简", "Σm", "sigma")):
            vc, mins = parse_sum_of_minterms(t)
            if not mins:
                # 默认示例最小项，保证能出图演示
                mins = [0, 2, 5, 7]
                vc = 3
            add(
                "draw_with_workflow",
                {
                    "brief": "画出卡诺图并化简",
                    "diagram_kind": "kmap",
                    "script": json.dumps(
                        {
                            "minterms": mins,
                            "var_count": vc,
                            "auto_group": True,
                            "title": "卡诺图化简",
                        },
                        ensure_ascii=False,
                    ),
                },
            )

        if "真值表" in t:
            add(
                "draw_with_workflow",
                {
                    "brief": "画出或门真值表",
                    "diagram_kind": "truth_table",
                    "script": json.dumps(
                        {
                            "inputs": ["A", "B"],
                            "outputs": ["F"],
                            "rows": [
                                [0, 0, 0],
                                [0, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1],
                            ],
                            "title": "或门真值表",
                        },
                        ensure_ascii=False,
                    ),
                },
            )

        if "七段" in t or "数码管" in t:
            m = re.search(r"[显示为为]?\s*([0-9])", t)
            digit = int(m.group(1)) if m else 8
            add(
                "draw_with_workflow",
                {
                    "brief": f"画出七段数码管点亮 {digit}",
                    "diagram_kind": "seven_seg",
                    "script": json.dumps(
                        {"digit": digit, "title": f"七段数码管显示{digit}"},
                        ensure_ascii=False,
                    ),
                },
            )

        if "特性曲线" in t or "电压传输" in t:
            curve = "cmos_vtc" if "CMOS" in t.upper() else "ttl_vtc"
            add(
                "draw_with_workflow",
                {
                    "brief": f"画出 {curve} 特性曲线",
                    "diagram_kind": "char_curve",
                    "script": json.dumps(
                        {"curve": curve, "title": "特性曲线"},
                        ensure_ascii=False,
                    ),
                },
            )

        if any(
            k in t
            for k in (
                "逻辑图",
                "门电路",
                "状态图",
                "原理图",
                "全加器",
                "NAND",
                "与非",
                "异或",
                "XOR",
                "同或",
                "波形",
                "时序",
                "设计电路",
                "置零",
                "计数器",
            )
        ):
            kind = "logic_dag"
            if "波形" in t or "时序" in t:
                kind = "timing_wave"
            elif "状态" in t:
                kind = "state_machine"
            elif any(
                k in t
                for k in ("设计电路", "置零", "加载", "555", "DAC", "计数器芯片", "74163")
            ):
                kind = "msi_design"
            add(
                "draw_with_workflow",
                {
                    "brief": t[:200],
                    "diagram_kind": kind,
                },
            )
        # 检索三工具：概念题尽量都走
        if any(k in t for k in ("教材", "课本", "什么是", "简述", "解释", "原理")):
            add("retrieve_multi_rerank", {"question": t[:200], "top_k": 4})
            add("graph_query", {"concept": t[:40], "top_k": 6})

        if any(k in t for k in ("题库", "搜题", "原题", "化简", "求", "计算", "分析", "设计")):
            add("search_question_bank", {"query": t[:200], "top_k": 1})

        # 去掉 C 档时序：不再规划 draw_timing_sft
        return calls[:3]


def build_chat_model(*, mock: bool, api_key: str, base_url: str, model: str):
    """真实 MiMo（OpenAI 兼容）或 Mock。"""
    if mock or not api_key:
        return MockTutorChatModel()
    from langchain_openai import ChatOpenAI

    # MiMo OpenAI 兼容：base 形如 https://api.xiaomimimo.com/v1
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url.rstrip("/"),
        temperature=0.2,
        timeout=120,
        max_retries=2,
        max_tokens=2048,
        streaming=True,
        # MiMo v2.5：关闭深度思考，便于稳定 tool calling
        extra_body={"thinking": {"type": "disabled"}},
    )
