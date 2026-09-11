"""P1 数据模型：question_bank / reflow_queue / users。"""

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(32), nullable=False, comment="昵称")
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, comment="手机号")
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    class_code: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True, comment="班级码（选填）"
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="student")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ClassRoom(Base):
    """教师管理员创建的班级（班级码加入）。"""

    __tablename__ = "class_rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="班级名称")
    class_code: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=True, comment="班级码"
    )
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="创建者 users.id")
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="active", comment="active/archived"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class QuestionBank(Base):
    """正式题库：已审核权威问答对。"""

    __tablename__ = "question_bank"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="题干")
    answer: Mapped[str] = mapped_column(Text, nullable=False, comment="权威答案")
    analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="解析")
    knowledge_tags: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="知识点标签"
    )
    source: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True, comment="来源（课本/章节等）"
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="active", comment="active/disabled"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ReflowQueue(Base):
    """回流问答表（待审）：AI 现解校验达标后进入，教师审核后选择性入库。"""

    __tablename__ = "reflow_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    ai_answer: Mapped[str] = mapped_column(Text, nullable=False)
    validate_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="pending",
        comment="pending/approved/rejected/auto_imported",
    )
    validate_score: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True, comment="权威校验分数"
    )
    source: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, comment="来源：text/image/mixed"
    )
    image_path: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
        comment="题干原图相对路径，如 /media/artifacts/reflow_xxx.jpg",
    )
    knowledge_tags: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="知识点标签：tags/concept_ids/raw_tags/source",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
