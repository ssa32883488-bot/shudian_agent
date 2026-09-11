"""P2–P4 扩展数据模型。"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Mistake(Base):
    """错题本。"""

    __tablename__ = "mistakes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    question_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("question_bank.id"), nullable=True
    )
    question_snapshot: Mapped[str] = mapped_column(Text, nullable=False)
    answer_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    add_source: Mapped[str] = mapped_column(
        String(32), nullable=False, default="manual"
    )
    knowledge_tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class StudentProfile(Base):
    """学情聚合画像（非流水；非对话隐私）。"""

    __tablename__ = "student_profiles"

    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    basics: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict, comment="基础画像：专业/年级/目标/偏好"
    )
    mastery: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict, comment="知识点掌握度（concept_id 或粗标签）"
    )
    practice_stats: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict, comment="练习频率/时长聚合"
    )
    weak_points: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    chapter_progress: Mapped[dict] = mapped_column(
        JSON, nullable=False, default=dict, comment="系统学章/节进度快照"
    )
    last_summary_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_rebuild_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="上次画像重建"
    )
    rebuild_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="idle", comment="idle|running|failed"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class MemorySummary(Base):
    """长期情节式记忆：对话摘要（属隐私，教师不可读原文）。"""

    __tablename__ = "memory_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    agent: Mapped[str] = mapped_column(
        String(32), nullable=False, default="student", comment="student|teacher|curriculum"
    )
    session_id_client: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    topics: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    mastery_hints: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    mistakes_hints: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    source_turn_range: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ClassRollup(Base):
    """班级学情聚合（由个人画像 / 错题 / 练习汇总；管理端学情看板读取）。"""

    __tablename__ = "class_rollups"

    class_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    n_students: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mastery_avg: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    weak_top: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    progress: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    exam_signals: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ChatThread(Base):
    """短期会话线程（服务端权威；浏览器本地缓存）。"""

    __tablename__ = "chat_threads"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    agent: Mapped[str] = mapped_column(String(32), nullable=False, default="student")
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="新会话")
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    summarized_until: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ChatMessageRecord(Base):
    """短期会话消息（UI 历史；≠ LangGraph Checkpoint）。"""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("chat_threads.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_format: Mapped[str] = mapped_column(String(16), nullable=False, default="md")
    attachments: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    trust_label: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    client_message_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class LongTermMemory(Base):
    """长期记忆条目：决策者按需 Tool 读写。"""

    __tablename__ = "long_term_memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="note",
        comment="preference|fact|weakness|note|episodic",
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    importance: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    source: Mapped[str] = mapped_column(
        String(32), nullable=False, default="tool", comment="tool|summary_distill|manual"
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ChatHistory(Base):
    """遗留扁平对话表（已由 chat_threads/chat_messages 替代；保留兼容）。"""

    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    agent: Mapped[str] = mapped_column(String(32), nullable=False, default="student")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class PracticeSession(Base):
    """个性化加练场次（可回看）。"""

    __tablename__ = "practice_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="加练")
    mode: Mapped[str] = mapped_column(String(32), nullable=False, default="auto")
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    weak_points: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="in_progress", comment="in_progress|submitted"
    )
    item_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    accuracy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    report_notes: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class PracticeAnswer(Base):
    """加练单题作答 + AI 判卷快照。"""

    __tablename__ = "practice_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("practice_sessions.id"), nullable=False, index=True
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("question_bank.id"), nullable=False
    )
    order_no: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    question_snapshot: Mapped[str] = mapped_column(Text, nullable=False, default="")
    answer_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answer_images: Mapped[Optional[list]] = mapped_column(
        JSON, nullable=True, comment="[/media/artifacts/...]"
    )
    correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    ai_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ai_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reference_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    knowledge_tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    grade_method: Mapped[str] = mapped_column(
        String(16), nullable=False, default="pending", comment="pending|rule|ai|unanswered"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class SystemSetting(Base):
    """管理端可改运行时配置（覆盖环境变量默认值）。"""

    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class AgentTrace(Base):
    """解题流程节点日志（题面/答案摘要 + 代码级流程，供系统观测）。"""

    __tablename__ = "agent_traces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )
    thread_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    question_preview: Mapped[str] = mapped_column(String(240), nullable=False, default="")
    steps: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    hit: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # ok | bank_hit | validate_fail | error | ai_reference
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ok", index=True)
    # intent / trust / validate / answer_preview / tool_trace / error 等
    detail: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
