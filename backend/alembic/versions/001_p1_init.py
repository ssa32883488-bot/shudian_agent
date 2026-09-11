"""P1 初始化：users / question_bank / reflow_queue

Revision ID: 001_p1_init
Revises:
Create Date: 2026-08-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_p1_init"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "question_bank",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("content", sa.Text(), nullable=False, comment="题干"),
        sa.Column("answer", sa.Text(), nullable=False, comment="权威答案"),
        sa.Column("analysis", sa.Text(), nullable=True, comment="解析"),
        sa.Column("knowledge_tags", sa.JSON(), nullable=True, comment="知识点标签"),
        sa.Column("source", sa.String(length=256), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "reflow_queue",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("ai_answer", sa.Text(), nullable=False),
        sa.Column("validate_status", sa.String(length=32), nullable=False),
        sa.Column("validate_score", sa.String(length=32), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reflow_queue")
    op.drop_table("question_bank")
    op.drop_table("users")
