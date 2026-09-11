"""LangChain @tool 包装：助学导师可调用工具集（绘图仅 draw_with_workflow）。"""

from __future__ import annotations

import json
from typing import Any, Optional

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.tools.draw_workflow import draw_with_workflow
from app.tools.retrieve import (
    tool_graph_query,
    tool_retrieve_multi_rerank,
    tool_search_question_bank,
)

_DB_HOLDER: dict[str, Any] = {"db": None, "user_id": None}


def set_tool_db(db: Any, user_id: Optional[int] = None) -> None:
    _DB_HOLDER["db"] = db
    if user_id is not None:
        _DB_HOLDER["user_id"] = int(user_id)


class DrawWorkflowArgs(BaseModel):
    brief: str = Field(..., description="出图需求")
    diagram_kind: str = Field(
        "",
        description=(
            "图类，可空（空则按 brief 关键词路由）。"
            "八选一："
            "logic_dag=门级逻辑图；"
            "timing_wave=时序波形；"
            "state_machine=状态转换图；"
            "truth_table=真值表；"
            "kmap=卡诺图(≤4变量)；"
            "seven_seg=七段数码管；"
            "char_curve=TTL/CMOS特性曲线；"
            "msi_design=芯片原理图(74系列/555/CMOS/DAC等)。"
        ),
    )
    slots_json: str = Field(
        "",
        description="可选；部分结构化字段的 JSON 字符串，供工作流补全 IR",
    )
    script: str = Field(
        "",
        description="可选；已写好的完整 IR/参数 JSON 字符串，有则跳过 LLM 生成",
    )
    max_retries: int = Field(
        3, ge=1, le=3, description="结构校验失败后的尝试上限（含首次，默认3）"
    )


class SearchArgs(BaseModel):
    query: str = Field(
        ...,
        description="已整理清晰的题干/题意（勿塞整段闲聊）；用于题库向量检索",
    )
    top_k: int = Field(
        1,
        ge=1,
        le=3,
        description="内部召回宽度；最终只可能返回校验通过的最高分 1 题",
    )


class GraphArgs(BaseModel):
    concept: str
    top_k: int = 6


class RagArgs(BaseModel):
    question: str
    top_k: int = 4


class ReadProfileArgs(BaseModel):
    student_id: int = Field(
        0, description="学生 id；0 表示当前登录学生（由系统绑定）"
    )


class MemorySearchArgs(BaseModel):
    query: str = Field("", description="检索关键词；空则按重要度返回近期条目")
    kind: str = Field(
        "",
        description="可选过滤：preference|fact|weakness|note|episodic",
    )
    limit: int = Field(8, ge=1, le=20)


class MemoryUpsertArgs(BaseModel):
    text: str = Field(..., description="要记住的自然语言内容")
    kind: str = Field(
        "note",
        description="preference|fact|weakness|note|episodic",
    )
    importance: float = Field(0.6, ge=0, le=1)
    memory_id: int = Field(0, description="若更新已有条目则传入 id")


class MemoryForgetArgs(BaseModel):
    memory_id: int = Field(0, description="要遗忘的条目 id")
    query: str = Field("", description="无 id 时按关键词软删匹配条目")


def _json(res: Any) -> str:
    if hasattr(res, "to_tool_message"):
        return res.to_tool_message()
    return json.dumps(res, ensure_ascii=False, default=str)


def _bound_user_id(explicit: int = 0) -> Optional[int]:
    if explicit:
        return int(explicit)
    uid = _DB_HOLDER.get("user_id")
    return int(uid) if uid else None


def _tool_read_profile(student_id: int = 0) -> dict[str, Any]:
    from app.db.models import User
    from app.services.memory import profile_public_dict
    from app.services.profile import get_or_create_profile

    db = _DB_HOLDER.get("db")
    if db is None:
        return {"ok": False, "error": "db not bound"}
    sid = _bound_user_id(student_id)
    if not sid:
        return {"ok": False, "error": "student_id required"}
    user = db.get(User, sid)
    if not user:
        return {"ok": False, "error": "student not found"}
    p = get_or_create_profile(db, sid)
    return profile_public_dict(user, p)


def _tool_memory_search(query: str = "", kind: str = "", limit: int = 8) -> dict[str, Any]:
    from app.services.long_term_memory import memory_public_dict, memory_search

    db = _DB_HOLDER.get("db")
    uid = _bound_user_id()
    if db is None or not uid:
        return {"ok": False, "error": "user context not bound"}
    rows = memory_search(
        db, uid, query, kind=kind or None, limit=limit
    )
    return {"ok": True, "items": [memory_public_dict(r) for r in rows]}


def _tool_memory_upsert(
    text: str,
    kind: str = "note",
    importance: float = 0.6,
    memory_id: int = 0,
) -> dict[str, Any]:
    from app.services.long_term_memory import memory_public_dict, memory_upsert

    db = _DB_HOLDER.get("db")
    uid = _bound_user_id()
    if db is None or not uid:
        return {"ok": False, "error": "user context not bound"}
    try:
        row = memory_upsert(
            db,
            uid,
            text=text,
            kind=kind,
            importance=importance,
            source="tool",
            memory_id=memory_id or None,
        )
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "item": memory_public_dict(row)}


def _tool_memory_forget(memory_id: int = 0, query: str = "") -> dict[str, Any]:
    from app.services.long_term_memory import memory_forget

    db = _DB_HOLDER.get("db")
    uid = _bound_user_id()
    if db is None or not uid:
        return {"ok": False, "error": "user context not bound"}
    return memory_forget(
        db, uid, memory_id=memory_id or None, query=query
    )


def _draw_with_workflow(
    brief: str,
    diagram_kind: str = "",
    slots_json: str = "",
    script: str = "",
    max_retries: int = 3,
) -> str:
    slots: dict[str, Any] = {}
    if slots_json and slots_json.strip():
        try:
            slots = json.loads(slots_json)
        except json.JSONDecodeError:
            slots = {}
    return _json(
        draw_with_workflow(
            brief=brief,
            diagram_kind=diagram_kind or "",
            slots=slots,
            script=script or None,
            max_retries=max_retries,
        )
    )


def build_tutor_tools() -> list[StructuredTool]:
    return [
        StructuredTool.from_function(
            name="draw_with_workflow",
            description=(
                "唯一绘图工具。流程：选定图类 → 生成/校验 IR → 出 SVG（失败最多重试 max_retries 次）。"
                "diagram_kind 八选一（可空，由 brief 推断）："
                "logic_dag 门级逻辑图；"
                "timing_wave 时序波形；"
                "state_machine 状态转换图；"
                "truth_table 真值表；"
                "kmap 卡诺图（≤4变量）；"
                "seven_seg 七段数码管；"
                "char_curve 特性曲线（TTL/CMOS VTC）；"
                "msi_design 芯片级原理图（74系列计数/译码/选择、555、CMOS、DAC/ADC等）。"
                "brief 必填；slots_json/script 可选（已有结构化数据或完整 IR 时传入）。"
                "出图后在解答对应步骤写 <<<DRAW kind=\"图类\" desc=\"说明\">>>，勿编造图片 URL。"
            ),
            func=_draw_with_workflow,
            args_schema=DrawWorkflowArgs,
        ),
        StructuredTool.from_function(
            name="search_question_bank",
            description=(
                "查正式题库是否有原题。传入你整理好的题干。"
                "仅当向量分≥0.95 且「同题+答案能解决问题」校验通过时，"
                "返回该题 content/answer；否则 message=「无」，请继续自主解题。"
            ),
            func=lambda query, top_k=1: _json(
                tool_search_question_bank(_DB_HOLDER["db"], query, top_k)
            ),
            args_schema=SearchArgs,
        ),
        StructuredTool.from_function(
            name="graph_query",
            description="查询知识图谱：前置路径、逻辑链、相关练习题。",
            func=lambda concept, top_k=6: _json(tool_graph_query(concept, top_k)),
            args_schema=GraphArgs,
        ),
        StructuredTool.from_function(
            name="retrieve_multi_rerank",
            description=(
                "教材多路召回+精排。返回课本摘录与插图占位块 <<<FIGURE id path desc>>>："
                "图片本身不进模型，仅文字描述；最终回答须原样保留需要的 FIGURE 块（可整块删除不需要的）。"
            ),
            func=lambda question, top_k=4: _json(
                tool_retrieve_multi_rerank(question, top_k)
            ),
            args_schema=RagArgs,
        ),
        StructuredTool.from_function(
            name="read_profile",
            description="读取学生学情聚合画像（掌握度/薄弱点/练习统计）。非对话摘要。",
            func=lambda student_id=0: _json(_tool_read_profile(int(student_id or 0))),
            args_schema=ReadProfileArgs,
        ),
        StructuredTool.from_function(
            name="memory_search",
            description=(
                "检索当前学生的长期记忆（偏好/事实/易错点/笔记/情节）。"
                "规划需要个性化上下文时调用。"
            ),
            func=lambda query="", kind="", limit=8: _json(
                _tool_memory_search(query=query, kind=kind, limit=limit)
            ),
            args_schema=MemorySearchArgs,
        ),
        StructuredTool.from_function(
            name="memory_upsert",
            description=(
                "写入或更新一条长期记忆。学生表达偏好、已学范围、易错点、笔记时使用。"
            ),
            func=lambda text, kind="note", importance=0.6, memory_id=0: _json(
                _tool_memory_upsert(
                    text=text,
                    kind=kind,
                    importance=importance,
                    memory_id=memory_id,
                )
            ),
            args_schema=MemoryUpsertArgs,
        ),
        StructuredTool.from_function(
            name="memory_forget",
            description="按 id 或关键词软删长期记忆（学生要求「忘掉」时使用）。",
            func=lambda memory_id=0, query="": _json(
                _tool_memory_forget(memory_id=memory_id, query=query)
            ),
            args_schema=MemoryForgetArgs,
        ),
    ]
