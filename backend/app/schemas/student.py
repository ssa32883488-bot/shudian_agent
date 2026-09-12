"""请求/响应 Schema。"""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    """学生解题请求：文字或图片二选一或同时（图片优先走 OCR）。"""

    text: Optional[str] = Field(None, description="题目文字")
    image_base64: Optional[str] = Field(
        None, description="题目图片 base64（可含 data URL 前缀）"
    )
    student_id: Optional[int] = Field(None, description="学生 ID（P1 占位）")
    thread_id: Optional[str] = Field(
        None, description="会话线程 id（短期记忆服务端权威）"
    )
    client_message_id: Optional[str] = Field(
        None, description="用户消息幂等 id（写入 chat_messages）"
    )
    # Plan 子题回流：用干净子题干入库，解题上下文仍用 text
    reflow_stem: Optional[str] = Field(
        None, description="回流待审题干（缺省则用归一化 question_text）"
    )
    reflow_image_path: Optional[str] = Field(
        None, description="已落盘的原题图片路径，如 /media/artifacts/reflow_xxx.jpg"
    )
    # 兼容前端字段名
    image: Optional[str] = Field(None, description="同 image_base64（兼容）")

    def resolved_image(self) -> Optional[str]:
        return self.image_base64 or self.image


class SolveResponse(BaseModel):
    ok: bool = True
    trust_level: Literal["authoritative", "ai_reference"] = Field(
        ..., description="信任分级：题库命中=authoritative；AI现解=ai_reference"
    )
    trust_label: str = Field(..., description="前端展示角标文案")
    question_text: str = Field(..., description="归一化后的题面")
    answer: str
    analysis: Optional[str] = None
    hit: bool = Field(..., description="是否命中正式题库")
    hit_question_id: Optional[int] = None
    hit_score: Optional[float] = None
    reflowed: bool = Field(False, description="是否写入回流问答表")
    reflow_id: Optional[int] = None
    validate_passed: Optional[bool] = None
    validate_score: Optional[float] = None
    source: Literal["text", "image", "mixed"] = "text"
    trace: list[str] = Field(default_factory=list, description="流程节点日志，便于回溯")
    kg_context: Optional[dict[str, Any]] = Field(
        None, description="知识图谱锚定：关键词、逻辑链、相关题"
    )
    images: list[str] = Field(
        default_factory=list,
        description="工具产物图片 URL（如卡诺图 SVG）",
    )
    provenance: Optional[dict[str, Any]] = Field(
        None,
        description="溯源：题库/知识图谱/教材/工具等结论来源说明",
    )


class SearchResponse(BaseModel):
    ok: bool = True
    query: str
    results: list[dict[str, Any]] = Field(default_factory=list)
