"""数据库会话与引擎。"""

from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
_connect_args = {}
if settings.database_url.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    pool_pre_ping=not settings.database_url.startswith("sqlite"),
    echo=settings.debug,
    connect_args=_connect_args,
)

if settings.database_url.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def _sqlite_enable_fk(dbapi_conn, _connection_record):  # noqa: ANN001
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_sqlite_columns() -> None:
    """SQLite 下 create_all 不改旧表，补齐增量列。"""
    if not settings.database_url.startswith("sqlite"):
        return
    from sqlalchemy import text

    alters = [
        ("student_profiles", "basics", "TEXT DEFAULT '{}'"),
        ("student_profiles", "chapter_progress", "TEXT DEFAULT '{}'"),
        ("student_profiles", "last_summary_at", "DATETIME"),
        ("student_profiles", "last_rebuild_at", "DATETIME"),
        ("student_profiles", "rebuild_status", "VARCHAR(16) DEFAULT 'idle'"),
        ("reflow_queue", "image_path", "VARCHAR(512)"),
        ("reflow_queue", "knowledge_tags", "JSON"),
        ("agent_traces", "status", "VARCHAR(32) DEFAULT 'ok'"),
        ("agent_traces", "detail", "TEXT DEFAULT '{}'"),
    ]
    with engine.begin() as conn:
        for table, col, decl in alters:
            rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
            names = {r[1] for r in rows}
            if col not in names:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {decl}"))


def init_db() -> None:
    """开发期便捷建表；正式环境用 Alembic。"""
    from pathlib import Path

    from app.db import models  # noqa: F401
    from app.db import models_ext  # noqa: F401

    if settings.database_url.startswith("sqlite:///"):
        db_path = settings.database_url.replace("sqlite:///", "", 1)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()
