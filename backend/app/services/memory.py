"""记忆层：对话摘要入库（隐私）→ 沉淀学情画像（非隐私）→ 班级 rollup。"""

from __future__ import annotations

import json
import logging
import re
import threading
import time
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.models_ext import ClassRollup, MemorySummary, Mistake, StudentProfile
from app.services.mimo import get_mimo
from app.services.profile import get_or_create_profile

logger = logging.getLogger(__name__)

SUMMARY_EVERY_N = 10
KEEP_RECENT_K = 6
ROLLUP_DEBOUNCE_SEC = 30.0

_rollup_timers: dict[str, threading.Timer] = {}
_rollup_lock = threading.Lock()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def profile_public_dict(user: User, p: StudentProfile) -> dict[str, Any]:
    """师生同构的学情视图（不含摘要原文）。"""
    basics = p.basics or {}
    stats = p.practice_stats or {}
    return {
        "ok": True,
        "student_id": user.id,
        "nickname": user.nickname,
        "class_code": user.class_code,
        "basics": basics,
        "mastery": p.mastery or {},
        "practice_stats": stats,
        "weak_points": p.weak_points or [],
        "chapter_progress": p.chapter_progress or {},
        "mistake_stats": stats.get("mistake_stats") or {},
        "knowledge_radar": stats.get("knowledge_radar") or [],
        "recommendations": basics.get("recommendations") or [],
        "recent_topics": basics.get("recent_topics") or [],
        "topic_freq": basics.get("topic_freq") or {},
        "last_summary_at": p.last_summary_at.isoformat() if p.last_summary_at else None,
        "last_rebuild_at": (
            p.last_rebuild_at.isoformat() if getattr(p, "last_rebuild_at", None) else None
        ),
        "rebuild_status": getattr(p, "rebuild_status", None) or "idle",
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        "privacy_note": "对话摘要属隐私；本画像为聚合学情，可在学情总览展示。",
    }


def _parse_json_block(text: str) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return {}
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return {}


def _normalize_qa_pairs(raw: Any) -> list[dict[str, Any]]:
    """规范化记忆压缩抽出的题干+答案对。"""
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        q = str(item.get("question") or item.get("stem") or "").strip()
        ans = str(item.get("answer") or "").strip()
        if len(q) < 8 or len(ans) < 2:
            continue
        try:
            conf = float(item.get("confidence") if item.get("confidence") is not None else 0.7)
        except (TypeError, ValueError):
            conf = 0.7
        tags = item.get("tags") or []
        if not isinstance(tags, list):
            tags = [tags] if tags else []
        out.append(
            {
                "question": q[:8000],
                "answer": ans[:12000],
                "confidence": max(0.0, min(1.0, conf)),
                "tags": [str(t) for t in tags if str(t).strip()][:8],
            }
        )
    return out[:5]


async def summarize_turns(
    turns: list[dict[str, str]],
    *,
    agent: str = "student",
) -> dict[str, Any]:
    """将待总结轮次交给后端模型，返回结构化摘要（不落原文）+ 可选题库候选 QA。"""
    compact = []
    for t in turns:
        role = t.get("role") or "user"
        content = (t.get("content") or "").strip()
        if not content:
            continue
        compact.append(f"{role}: {content[:800]}")
    blob = "\n".join(compact)[:6000]
    if not blob:
        return {
            "summary_text": "（无有效对话内容）",
            "topics": [],
            "mastery_hints": [],
            "mistakes_hints": [],
            "qa_pairs": [],
        }

    prompt = (
        "你是数电教学助教的记忆压缩器。根据对话片段输出 JSON（不要 Markdown）：\n"
        "{\n"
        '  "summary_text": "教学语义摘要，禁止逐字粘贴对话原文",\n'
        '  "topics": ["知识点或 concept 标签"],\n'
        '  "mastery_hints": [{"concept":"标签","delta":-0.05到0.05,"evidence":"一句依据"}],\n'
        '  "mistakes_hints": [{"question_snapshot":"题意摘要","reason":"错因","tags":["标签"]}],\n'
        '  "qa_pairs": [\n'
        '    {"question":"自洽完整题干（合并多轮补丁后的终态题面）",'
        '"answer":"标准答案或终态正确解答（不含寒暄/溯源）",'
        '"confidence":0.0到1.0,"tags":["知识点"]}\n'
        "  ]\n"
        "}\n"
        "qa_pairs 抽取规则：\n"
        "1. 仅当对话中出现明确习题（计算/化简/画图/判断/设计）且助手给出了可用解答时才抽取；\n"
        "2. 纯概念闲聊、追问讲解碎片、无终态答案的不要进 qa_pairs；\n"
        "3. 多轮澄清时 question 用合并后的终态题干，answer 用纠错后的最终答案；\n"
        "4. 不要粘贴整段对话；每条要能独立入库；最多 5 条。\n"
        f"agent={agent}\n对话片段：\n{blob}"
    )
    mimo = get_mimo()
    raw = ""
    try:
        raw = await mimo.chat(
            [
                {"role": "system", "content": "只输出合法 JSON。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
    except Exception as exc:
        logger.warning("摘要 LLM 调用失败，回退启发式: %s", exc)
        raw = ""
    data = _parse_json_block(raw)
    if not data:
        # mock / 失败回退：从文本粗提取
        topics = []
        for kw in ("卡诺图", "时序逻辑", "组合逻辑", "逻辑代数", "数制", "触发器", "JK"):
            if kw in blob:
                topics.append(kw)
        if not topics:
            topics = ["逻辑代数"]
        data = {
            "summary_text": f"【摘要】讨论了 {', '.join(topics)}；保留未解决问题与偏好供画像沉淀。",
            "topics": topics,
            "mastery_hints": [
                {"concept": topics[0], "delta": -0.02, "evidence": "对话中仍有疑点"}
            ],
            "mistakes_hints": [],
            "qa_pairs": [],
        }
    return {
        "summary_text": str(data.get("summary_text") or "（摘要生成失败）"),
        "topics": list(data.get("topics") or []),
        "mastery_hints": list(data.get("mastery_hints") or []),
        "mistakes_hints": list(data.get("mistakes_hints") or []),
        "qa_pairs": _normalize_qa_pairs(data.get("qa_pairs")),
    }


def distill_profile_from_summary(
    db: Session,
    user_id: int,
    summary: MemorySummary,
    *,
    soft_weight: float = 0.5,
) -> StudentProfile:
    """从摘要沉淀画像；软信号权重低于练习/考试硬信号。"""
    p = get_or_create_profile(db, user_id)
    mastery = dict(p.mastery or {})
    for hint in summary.mastery_hints or []:
        if not isinstance(hint, dict):
            continue
        concept = str(hint.get("concept") or hint.get("tag") or "").strip()
        if not concept:
            continue
        try:
            delta = float(hint.get("delta") or 0) * soft_weight
        except (TypeError, ValueError):
            delta = 0.0
        cur = float(mastery.get(concept, 0.5))
        mastery[concept] = max(0.0, min(1.0, cur + delta))

    for mh in summary.mistakes_hints or []:
        if not isinstance(mh, dict):
            continue
        snap = str(mh.get("question_snapshot") or "").strip()
        if not snap:
            continue
        tags = mh.get("tags") or summary.topics or []
        db.add(
            Mistake(
                student_id=user_id,
                question_snapshot=snap[:2000],
                reason=str(mh.get("reason") or "对话摘要沉淀")[:1000],
                add_source="memory_summary",
                knowledge_tags={"tags": tags} if tags else None,
            )
        )

    basics = dict(p.basics or {})
    topics = summary.topics or []
    if topics:
        recent = list(basics.get("recent_topics") or [])
        freq = dict(basics.get("topic_freq") or {})
        for t in topics:
            key = str(t).strip()
            if not key:
                continue
            freq[key] = int(freq.get(key, 0) or 0) + 1
            if key not in recent:
                recent.insert(0, key)
        basics["recent_topics"] = recent[:12]
        basics["topic_freq"] = freq

    weak = sorted(mastery, key=lambda k: float(mastery.get(k, 0.5)))[:5]
    p.mastery = mastery
    p.basics = basics
    p.weak_points = weak
    p.last_summary_at = _now()
    p.updated_at = _now()
    db.commit()
    db.refresh(p)
    return p


def ingest_summary(
    db: Session,
    *,
    user: User,
    agent: str,
    session_id_client: str,
    summary_text: str,
    topics: list[Any],
    mastery_hints: list[Any],
    mistakes_hints: list[Any],
    source_turn_range: Optional[dict[str, Any]] = None,
    qa_pairs: Optional[list[dict[str, Any]]] = None,
) -> tuple[MemorySummary, StudentProfile, list[Any]]:
    """写入隐私摘要 → 沉淀画像；旁路将 qa_pairs 注入回流候选队列（供管理端审核）。"""
    row = MemorySummary(
        user_id=user.id,
        agent=agent,
        session_id_client=session_id_client or "",
        summary_text=summary_text,
        topics=topics,
        mastery_hints=mastery_hints,
        mistakes_hints=mistakes_hints,
        source_turn_range=source_turn_range,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    profile = distill_profile_from_summary(db, user.id, row)

    reflow_items: list[Any] = []
    pairs = _normalize_qa_pairs(qa_pairs or [])
    if pairs and agent in ("student", "curriculum", ""):
        try:
            from app.services.reflow import enqueue_memory_qa_pairs

            reflow_items = enqueue_memory_qa_pairs(
                db,
                pairs,
                summary_id=row.id,
                session_id_client=session_id_client or "",
            )
        except Exception as exc:
            logger.warning("记忆抽题写入回流失败 summary_id=%s: %s", row.id, exc)

    if user.class_code:
        schedule_class_rollup(user.class_code)
    return row, profile, reflow_items


def compute_class_rollup(db: Session, class_code: str) -> ClassRollup:
    from app.db.models_ext import Mistake, PracticeSession

    students = list(
        db.scalars(
            select(User).where(User.role == "student", User.class_code == class_code)
        ).all()
    )
    student_ids = [s.id for s in students]
    mastery_sums: dict[str, float] = {}
    mastery_cnt: dict[str, int] = {}
    weak_freq: dict[str, int] = {}
    chapter_done = 0
    for s in students:
        p = db.get(StudentProfile, s.id)
        if not p:
            continue
        for k, v in (p.mastery or {}).items():
            mastery_sums[k] = mastery_sums.get(k, 0.0) + float(v)
            mastery_cnt[k] = mastery_cnt.get(k, 0) + 1
        for w in p.weak_points or []:
            weak_freq[str(w)] = weak_freq.get(str(w), 0) + 1
        prog = p.chapter_progress or {}
        if prog.get("completed_chapters"):
            chapter_done += len(prog.get("completed_chapters") or [])

    mistake_freq: dict[str, int] = {}
    if student_ids:
        mistakes = list(
            db.scalars(
                select(Mistake).where(
                    Mistake.student_id.in_(student_ids),
                    Mistake.deleted_at.is_(None),
                )
            ).all()
        )
        for m in mistakes:
            tags = m.knowledge_tags or {}
            raw = tags.get("tags") if isinstance(tags, dict) else None
            if isinstance(raw, list) and raw:
                for t in raw:
                    name = str(t).strip()
                    if name:
                        mistake_freq[name] = mistake_freq.get(name, 0) + 1
            else:
                mistake_freq["未标注"] = mistake_freq.get("未标注", 0) + 1

    practice_sessions = 0
    practice_students: set[int] = set()
    acc_sum = 0.0
    acc_n = 0
    if student_ids:
        sessions = list(
            db.scalars(
                select(PracticeSession).where(
                    PracticeSession.student_id.in_(student_ids),
                    PracticeSession.status == "submitted",
                )
            ).all()
        )
        practice_sessions = len(sessions)
        for sess in sessions:
            practice_students.add(int(sess.student_id))
            if sess.accuracy is not None:
                acc_sum += float(sess.accuracy)
                acc_n += 1

    mastery_avg = {
        k: round(mastery_sums[k] / max(1, mastery_cnt[k]), 3) for k in mastery_sums
    }
    weak_top = sorted(weak_freq.items(), key=lambda x: (-x[1], x[0]))[:8]
    mistake_top = sorted(mistake_freq.items(), key=lambda x: (-x[1], x[0]))[:8]
    content = {
        "mastery_avg": mastery_avg,
        "weak_top": [{"name": n, "count": c} for n, c in weak_top],
        "progress": {
            "n_students": len(students),
            "chapter_completion_events": chapter_done,
        },
        "exam_signals": {
            "mistake_top": [{"name": n, "count": c} for n, c in mistake_top],
            "practice": {
                "n_sessions": practice_sessions,
                "n_students": len(practice_students),
                "avg_accuracy": round(acc_sum / acc_n, 3) if acc_n else None,
            },
        },
    }
    row = db.get(ClassRollup, class_code)
    if not row:
        row = ClassRollup(class_code=class_code)
        db.add(row)
    row.n_students = len(students)
    row.mastery_avg = content["mastery_avg"]
    row.weak_top = content["weak_top"]
    row.progress = content["progress"]
    row.exam_signals = content["exam_signals"]
    row.computed_at = _now()
    db.commit()
    db.refresh(row)
    return row


def schedule_class_rollup(class_code: str) -> None:
    """事件驱动 + 防抖 30s。"""
    if not class_code:
        return

    def _fire() -> None:
        from app.db import SessionLocal

        with _rollup_lock:
            _rollup_timers.pop(class_code, None)
        db = SessionLocal()
        try:
            compute_class_rollup(db, class_code)
            logger.info("class_rollup refreshed: %s", class_code)
        except Exception as exc:
            logger.warning("class_rollup failed %s: %s", class_code, exc)
        finally:
            db.close()

    with _rollup_lock:
        old = _rollup_timers.get(class_code)
        if old:
            old.cancel()
        t = threading.Timer(ROLLUP_DEBOUNCE_SEC, _fire)
        t.daemon = True
        _rollup_timers[class_code] = t
        t.start()


def list_own_summaries(db: Session, user_id: int, limit: int = 20) -> list[MemorySummary]:
    return list(
        db.scalars(
            select(MemorySummary)
            .where(MemorySummary.user_id == user_id)
            .order_by(MemorySummary.created_at.desc())
            .limit(limit)
        ).all()
    )


def get_class_rollup(db: Session, class_code: str, *, refresh: bool = False) -> ClassRollup:
    row = db.get(ClassRollup, class_code)
    if refresh or not row:
        row = compute_class_rollup(db, class_code)
    return row


REBUILD_COOLDOWN_SEC = 600.0  # 手动重建限流：10 分钟


def rebuild_student_profile(db: Session, user_id: int) -> StudentProfile:
    """夜间批跑与学情总览「更新」共用：摘要 + 错题 + 练习 → 写回画像（无对话原文）。"""
    from app.services.profile import DEFAULT_MASTERY

    p = get_or_create_profile(db, user_id)
    p.rebuild_status = "running"
    db.commit()

    try:
        mastery = dict(DEFAULT_MASTERY)
        mastery.update(dict(p.mastery or {}))

        summaries = list(
            db.scalars(
                select(MemorySummary)
                .where(MemorySummary.user_id == user_id)
                .order_by(MemorySummary.created_at.desc())
                .limit(40)
            ).all()
        )
        topic_freq: dict[str, int] = {}
        for s in summaries:
            for hint in s.mastery_hints or []:
                if not isinstance(hint, dict):
                    continue
                concept = str(hint.get("concept") or hint.get("tag") or "").strip()
                if not concept:
                    continue
                try:
                    delta = float(hint.get("delta") or 0) * 0.35
                except (TypeError, ValueError):
                    delta = 0.0
                cur = float(mastery.get(concept, 0.5))
                mastery[concept] = max(0.0, min(1.0, cur + delta))
            for t in s.topics or []:
                key = str(t).strip()
                if key:
                    topic_freq[key] = topic_freq.get(key, 0) + 1

        mistakes = list(
            db.scalars(
                select(Mistake).where(
                    Mistake.student_id == user_id, Mistake.deleted_at.is_(None)
                )
            ).all()
        )
        tag_freq: dict[str, int] = {}
        for m in mistakes:
            tags = []
            if isinstance(m.knowledge_tags, dict):
                raw = m.knowledge_tags.get("tags") or m.knowledge_tags.get("concepts")
                if isinstance(raw, list):
                    tags = [str(x) for x in raw if x]
                elif isinstance(raw, str) and raw:
                    tags = [raw]
            for t in tags or ["未标注"]:
                tag_freq[t] = tag_freq.get(t, 0) + 1
                # 错题对掌握度施加硬惩罚
                if t != "未标注":
                    mastery[t] = max(0.0, float(mastery.get(t, 0.5)) - 0.04)

        # 长期记忆 weakness / fact
        from app.services.long_term_memory import list_active_by_kinds

        ltm_rows = list_active_by_kinds(
            db, user_id, ["weakness", "fact", "preference"], limit=24
        )
        for row in ltm_rows:
            key = str(row.kind)
            snippet = (row.text or "").strip()[:80]
            if not snippet:
                continue
            if key == "weakness":
                # 弱项文本本身作为标签
                tag = snippet.split("：")[0].split(":")[0][:32]
                tag_freq[tag] = tag_freq.get(tag, 0) + 2
                mastery[tag] = max(0.0, float(mastery.get(tag, 0.5)) - 0.05)
                topic_freq[snippet[:40]] = topic_freq.get(snippet[:40], 0) + 1
            elif key == "fact":
                topic_freq[snippet[:40]] = topic_freq.get(snippet[:40], 0) + 2
            elif key == "preference":
                basics_pref = dict(p.basics or {})
                prefs = list(basics_pref.get("preferences") or [])
                if snippet not in prefs:
                    prefs.append(snippet)
                basics_pref["preferences"] = prefs[-8:]
                p.basics = basics_pref

        weak = sorted(mastery, key=lambda k: float(mastery.get(k, 0.5)))[:6]
        recent_topics = sorted(topic_freq, key=lambda k: (-topic_freq[k], k))[:12]
        radar = [
            {"name": k, "value": round(float(mastery.get(k, 0.5)), 3)}
            for k in sorted(mastery, key=lambda x: -float(mastery.get(x, 0.5)))[:8]
        ]
        top_mistake_tags = sorted(tag_freq.items(), key=lambda x: (-x[1], x[0]))[:8]
        recommendations: list[dict[str, Any]] = []
        for w in weak[:3]:
            recommendations.append(
                {
                    "type": "practice",
                    "label": f"针对薄弱点「{w}」加练",
                    "payload": {"concept": w},
                }
            )
        for t, _ in top_mistake_tags[:2]:
            if t == "未标注":
                continue
            recommendations.append(
                {
                    "type": "review",
                    "label": f"复盘错题标签「{t}」",
                    "payload": {"tag": t},
                }
            )

        basics = dict(p.basics or {})
        basics["recent_topics"] = recent_topics
        basics["topic_freq"] = topic_freq
        basics["recommendations"] = recommendations[:6]

        stats = dict(p.practice_stats or {})
        stats["mistake_stats"] = {
            "count": len(mistakes),
            "top_tags": [{"name": n, "count": c} for n, c in top_mistake_tags],
        }
        stats["knowledge_radar"] = radar

        p.mastery = mastery
        p.weak_points = weak
        p.basics = basics
        p.practice_stats = stats
        p.last_rebuild_at = _now()
        p.rebuild_status = "idle"
        p.updated_at = _now()
        db.commit()
        db.refresh(p)

        user = db.get(User, user_id)
        if user and user.class_code:
            schedule_class_rollup(user.class_code)
        return p
    except Exception:
        p.rebuild_status = "failed"
        db.commit()
        raise


def rebuild_all_active_profiles(db: Session, *, days: int = 30) -> int:
    """夜间批跑：重建近期有摘要或画像的学生。"""
    from datetime import timedelta

    cutoff = _now() - timedelta(days=days)
    user_ids = set(
        db.scalars(
            select(MemorySummary.user_id).where(MemorySummary.created_at >= cutoff)
        ).all()
    )
    # 也覆盖已有画像的学生（增量兜底）
    for sid in db.scalars(select(StudentProfile.student_id)).all():
        user_ids.add(int(sid))
    n = 0
    for uid in sorted(user_ids):
        try:
            rebuild_student_profile(db, int(uid))
            n += 1
        except Exception as exc:
            logger.warning("nightly rebuild failed user=%s: %s", uid, exc)
    return n
