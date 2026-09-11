"""学情画像读写（聚合态 · 硬信号）。"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models_ext import StudentProfile

# 兼容旧粗标签；新摘要优先写 concept 名（可与 KG id 同形）
DEFAULT_MASTERY = {
    "逻辑代数": 0.6,
    "组合逻辑": 0.55,
    "时序逻辑": 0.5,
    "卡诺图": 0.45,
    "数制编码": 0.65,
}


def get_or_create_profile(db: Session, student_id: int) -> StudentProfile:
    p = db.get(StudentProfile, student_id)
    if p:
        # 兼容旧行缺字段
        if p.basics is None:
            p.basics = {}
        if p.chapter_progress is None:
            p.chapter_progress = {}
        if not p.mastery:
            p.mastery = dict(DEFAULT_MASTERY)
        return p
    p = StudentProfile(
        student_id=student_id,
        basics={},
        mastery=dict(DEFAULT_MASTERY),
        practice_stats={"total_solves": 0, "weekly_minutes": [0] * 7},
        weak_points=["卡诺图", "时序逻辑"],
        chapter_progress={},
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def bump_after_solve(
    db: Session, student_id: int, *, hit: bool, tags: list[str] | None = None
) -> StudentProfile:
    from app.db.models import User
    from app.services.memory import schedule_class_rollup

    p = get_or_create_profile(db, student_id)
    mastery = dict(p.mastery or DEFAULT_MASTERY)
    delta = 0.03 if hit else -0.01
    for tag in tags or ["逻辑代数"]:
        mastery[tag] = max(0.0, min(1.0, float(mastery.get(tag, 0.5)) + delta))
    stats = dict(p.practice_stats or {})
    stats["total_solves"] = int(stats.get("total_solves", 0)) + 1
    week = list(stats.get("weekly_minutes") or [0] * 7)
    idx = datetime.now(timezone.utc).weekday()
    if len(week) < 7:
        week = (week + [0] * 7)[:7]
    week[idx] = int(week[idx]) + 5
    stats["weekly_minutes"] = week
    weak = sorted(mastery, key=lambda k: mastery[k])[:5]
    p.mastery = mastery
    p.practice_stats = stats
    p.weak_points = weak
    p.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(p)
    user = db.get(User, student_id)
    if user and user.class_code:
        schedule_class_rollup(user.class_code)
    return p
