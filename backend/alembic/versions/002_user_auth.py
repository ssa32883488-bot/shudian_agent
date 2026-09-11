"""用户表升级：昵称/手机号/密码/班级码

Revision ID: 002_user_auth
Revises: 001_p1_init
Create Date: 2026-08-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_user_auth"
down_revision: Union[str, None] = "001_p1_init"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # P1 开发期：users 表结构变更直接重建（无生产数据）
    op.drop_table("users")
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nickname", sa.String(length=32), nullable=False),
        sa.Column("phone", sa.String(length=11), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("class_code", sa.String(length=32), nullable=True),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone"),
    )


def downgrade() -> None:
    op.drop_table("users")
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
