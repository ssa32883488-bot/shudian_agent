"""学生自适应练习：抽题落库 → 文字/图片作答 → AI 逐题判卷 → 可回看记录。"""

from __future__ import annotations

import base64
import logging
import random
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import QuestionBank, User
from app.db.models_ext import PracticeAnswer, PracticeSession
from app.services.mistakes import add_mistake
from app.services.mimo import get_mimo
from app.services.profile import bump_after_solve, get_or_create_profile
from app.services.reflow import save_reflow_stem_image
from app.tools.gateway import artifact_dir

logger = logging.getLogger(__name__)

MAX_PRACTICE = 20
MAX_IMAGES_PER_Q = 4
PASS_SCORE = 0.6


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").strip().lower())


def tags_list(tags: Any) -> list[str]:
    if not tags:
        return []
    if isinstance(tags, dict):
        raw = tags.get("tags") or tags.get("concepts") or tags.get("name")
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
        if isinstance(raw, str) and raw.strip():
            return [raw.strip()]
        out: list[str] = []
        for k, v in tags.items():
            if str(k) in {"id", "qid"}:
                continue
            if isinstance(v, (list, tuple)):
                out.extend(str(x).strip() for x in v if str(x).strip())
            elif isinstance(v, str) and v.strip() and v.strip().lower() not in {"true", "false"}:
                out.append(v.strip())
            elif k and not isinstance(v, (int, float, dict)):
                out.append(str(k).strip())
        return [x for x in out if x]
    if isinstance(tags, (list, tuple)):
        return [str(x).strip() for x in tags if str(x).strip()]
    s = str(tags).strip()
    return [s] if s else []


def _tag_hit(tags: Any, weak: list[str]) -> bool:
    if not tags or not weak:
        return False
    blob = " ".join(tags_list(tags)).lower()
    if isinstance(tags, dict):
        blob = (
            blob
            + " "
            + " ".join(str(v) for v in tags.values())
            + " "
            + " ".join(tags.keys())
        ).lower()
    elif not blob:
        blob = str(tags).lower()
    return any(w and w.lower() in blob for w in weak)


def _mistake_tags(db: Session, student_id: int) -> list[str]:
    from app.db.models_ext import Mistake

    rows = list(
        db.scalars(
            select(Mistake).where(
                Mistake.student_id == student_id, Mistake.deleted_at.is_(None)
            )
        ).all()
    )
    freq: dict[str, int] = {}
    for m in rows:
        for t in tags_list(m.knowledge_tags):
            if t and t != "未标注":
                freq[t] = freq.get(t, 0) + 1
    return sorted(freq, key=lambda k: (-freq[k], k))


def _save_answer_images(raw_list: list[Any] | None) -> list[str]:
    paths: list[str] = []
    for item in (raw_list or [])[:MAX_IMAGES_PER_Q]:
        s = str(item or "").strip()
        if not s:
            continue
        if s.startswith("/media/artifacts/"):
            paths.append(s)
            continue
        saved = save_reflow_stem_image(s)
        if saved:
            # 改名前缀便于区分加练作答图
            try:
                src = artifact_dir() / Path(saved).name
                if src.exists() and src.name.startswith("reflow_"):
                    new_name = "practice_" + src.name[len("reflow_") :]
                    dest = artifact_dir() / new_name
                    src.rename(dest)
                    paths.append(f"/media/artifacts/{new_name}")
                else:
                    paths.append(saved)
            except Exception:
                paths.append(saved)
    return paths


def _media_path_to_data_url(path: str) -> str | None:
    try:
        name = Path(path).name
        if ".." in name or "/" in name or "\\" in name:
            return None
        fp = artifact_dir() / name
        if not fp.is_file():
            return None
        data = fp.read_bytes()
        ext = fp.suffix.lower().lstrip(".") or "jpg"
        mime = {
            "png": "image/png",
            "webp": "image/webp",
            "gif": "image/gif",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
        }.get(ext, "image/jpeg")
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


def _answer_dict(row: PracticeAnswer) -> dict[str, Any]:
    return {
        "id": row.id,
        "question_id": row.question_id,
        "order_no": row.order_no,
        "content": row.question_snapshot,
        "question_snapshot": row.question_snapshot,
        "knowledge_tags": row.knowledge_tags,
        "answer_text": row.answer_text or "",
        "answer_images": list(row.answer_images or []),
        "correct": row.correct,
        "ai_score": row.ai_score,
        "ai_comment": row.ai_comment,
        "reference_answer": row.reference_answer,
        "analysis": row.analysis,
        "grade_method": row.grade_method,
    }


def _session_summary(sess: PracticeSession) -> dict[str, Any]:
    return {
        "id": sess.id,
        "title": sess.title,
        "mode": sess.mode,
        "source": sess.source,
        "weak_points": list(sess.weak_points or []),
        "status": sess.status,
        "item_count": sess.item_count,
        "correct_count": sess.correct_count,
        "accuracy": sess.accuracy,
        "report_notes": list(sess.report_notes or []),
        "created_at": sess.created_at.isoformat() if sess.created_at else None,
        "submitted_at": sess.submitted_at.isoformat() if sess.submitted_at else None,
    }


def generate_practice(
    db: Session,
    *,
    student_id: int,
    count: int = 8,
    mode: str = "auto",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    count = max(1, min(int(count or 8), MAX_PRACTICE))
    mode = (mode or "auto").strip().lower()
    if mode not in {"auto", "probe", "focus", "review"}:
        mode = "auto"
    focus = [t.strip() for t in (tags or []) if t and str(t).strip()]
    profile = get_or_create_profile(db, student_id)
    rows = list(
        db.scalars(select(QuestionBank).where(QuestionBank.status == "active")).all()
    )
    if not rows:
        raise HTTPException(status_code=400, detail="题库暂无可用题目，请先由管理员维护题库")

    if mode == "probe":
        used: list[str] = []
        pool = list(rows)
        source = "probe"
        title = "摸底练习"
    elif mode == "review":
        used = focus or _mistake_tags(db, student_id)
        preferred = [q for q in rows if _tag_hit(q.knowledge_tags, used)] if used else []
        pool = preferred if preferred else list(rows)
        source = "review" if preferred else "random_bank"
        title = "错题回炉"
    else:
        used = focus or list(profile.weak_points or [])
        preferred = [q for q in rows if _tag_hit(q.knowledge_tags, used)] if used else []
        pool = preferred if preferred else list(rows)
        source = "focus" if preferred else "random_bank"
        if mode == "focus" and used:
            title = f"针对加练：{used[0]}"
        else:
            title = "学情自适应练习"
        if mode == "auto" and preferred:
            source = "weak_tags"

    random.shuffle(pool)
    picked = pool[:count]

    sess = PracticeSession(
        student_id=student_id,
        title=title,
        mode=mode,
        source=source,
        weak_points=used[:8],
        status="in_progress",
        item_count=len(picked),
    )
    db.add(sess)
    db.flush()

    items: list[dict[str, Any]] = []
    for i, q in enumerate(picked):
        ans = PracticeAnswer(
            session_id=sess.id,
            question_id=q.id,
            order_no=i + 1,
            question_snapshot=q.content or "",
            reference_answer=q.answer,
            analysis=q.analysis,
            knowledge_tags=q.knowledge_tags if isinstance(q.knowledge_tags, dict) else None,
            grade_method="pending",
        )
        db.add(ans)
        items.append(
            {
                "question_id": q.id,
                "order_no": i + 1,
                "content": q.content,
                "knowledge_tags": q.knowledge_tags,
            }
        )
    db.commit()
    db.refresh(sess)

    return {
        "ok": True,
        "session_id": sess.id,
        "title": title,
        "mode": mode,
        "weak_points": used[:8],
        "source": source,
        "count": len(items),
        "items": items,
    }


async def grade_practice(
    db: Session,
    *,
    student: User,
    session_id: int,
    answers: list[dict[str, Any]],
    write_mistakes: bool = True,
) -> dict[str, Any]:
    """逐题 AI 判卷（题干 + 文字 + 全部作答图），写入场次记录。"""
    sess = db.get(PracticeSession, session_id)
    if not sess or sess.student_id != student.id:
        raise HTTPException(status_code=404, detail="加练场次不存在")
    if sess.status == "submitted":
        return get_practice_session(db, student_id=student.id, session_id=session_id)

    rows = list(
        db.scalars(
            select(PracticeAnswer)
            .where(PracticeAnswer.session_id == sess.id)
            .order_by(PracticeAnswer.order_no.asc())
        ).all()
    )
    payload_by_qid = {
        int(a.get("question_id") or 0): a
        for a in answers
        if a.get("question_id") is not None
    }

    mimo = get_mimo()
    correct_n = 0
    session_tags: list[str] = []
    missed_tags: list[str] = []
    results: list[dict[str, Any]] = []

    for row in rows:
        raw = payload_by_qid.get(row.question_id) or {}
        text = str(raw.get("answer_text") or "").strip()
        img_inputs = raw.get("images") or raw.get("answer_images") or []
        if not isinstance(img_inputs, list):
            img_inputs = [img_inputs] if img_inputs else []
        image_paths = _save_answer_images(img_inputs)
        row.answer_text = text
        row.answer_images = image_paths

        q_tags = tags_list(row.knowledge_tags)
        session_tags.extend(q_tags)

        if not text and not image_paths:
            row.correct = False
            row.ai_score = 0.0
            row.ai_comment = "未作答"
            row.grade_method = "unanswered"
            missed_tags.extend(q_tags)
            if q_tags:
                bump_after_solve(db, student.id, hit=False, tags=q_tags)
            results.append(_answer_dict(row))
            continue

        # 无图且与参考答案完全一致：规则快判，仍记 method
        ref = (row.reference_answer or "").strip()
        if text and not image_paths and ref and _norm(text) == _norm(ref):
            ok = True
            score = 1.0
            comment = "与参考答案一致"
            method = "rule"
        else:
            data_urls: list[str] = []
            if image_paths:
                for p in image_paths:
                    url = _media_path_to_data_url(p)
                    if url:
                        data_urls.append(url)
            else:
                for item in img_inputs:
                    s = str(item or "").strip()
                    if s.startswith("data:image"):
                        data_urls.append(s)
            try:
                judged = await mimo.grade_student_answer(
                    question=row.question_snapshot or "",
                    reference_answer=row.reference_answer or "",
                    student_text=text,
                    image_data_urls=data_urls[:MAX_IMAGES_PER_Q],
                )
                score = float(judged.get("score") or 0.0)
                if judged.get("correct") is None:
                    ok = score >= PASS_SCORE
                else:
                    ok = bool(judged.get("correct"))
                comment = str(judged.get("comment") or "")
                method = "ai"
            except Exception as exc:
                logger.warning("AI 判卷失败 q=%s: %s", row.question_id, exc)
                ok = bool(text and ref and _norm(text) == _norm(ref))
                score = 1.0 if ok else 0.4
                comment = f"AI 判卷暂不可用，已回退规则比对（{exc.__class__.__name__}）"
                method = "rule"

        row.correct = ok
        row.ai_score = round(score, 3)
        row.ai_comment = comment[:800]
        row.grade_method = method

        if ok:
            correct_n += 1
        else:
            missed_tags.extend(q_tags)
            if write_mistakes and (text or image_paths):
                reason = comment or "加练 AI 判卷未通过"
                if image_paths:
                    reason = f"{reason}｜附图 {len(image_paths)} 张"
                add_mistake(
                    db,
                    student_id=student.id,
                    question_snapshot=row.question_snapshot,
                    answer_snapshot=row.reference_answer,
                    reason=f"练习作答：{(text or '（图片作答）')[:180]}｜{reason[:120]}",
                    question_id=row.question_id,
                    add_source="practice",
                    knowledge_tags=row.knowledge_tags
                    if isinstance(row.knowledge_tags, dict)
                    else None,
                )
        if q_tags:
            bump_after_solve(db, student.id, hit=ok, tags=q_tags)
        results.append(_answer_dict(row))

    total = len(rows) or 1
    accuracy = round(correct_n / total, 3)
    uniq_session = list(dict.fromkeys(session_tags))
    uniq_missed = list(dict.fromkeys(missed_tags))

    # 报告笔记
    tag_map: dict[str, dict[str, int]] = {}
    for row in rows:
        keys = tags_list(row.knowledge_tags) or ["未标注"]
        for t in keys:
            cur = tag_map.setdefault(t, {"ok": 0, "bad": 0})
            if row.correct:
                cur["ok"] += 1
            else:
                cur["bad"] += 1
    notes: list[str] = []
    for tag, s in tag_map.items():
        if s["bad"] and not s["ok"]:
            notes.append(f"{tag}：错/未作答 {s['bad']} 题 → 仍列薄弱")
        elif s["bad"]:
            notes.append(f"{tag}：对 {s['ok']} / 错 {s['bad']} → 仍需加练")
        else:
            notes.append(f"{tag}：全对")

    now = datetime.now(timezone.utc)
    sess.status = "submitted"
    sess.correct_count = correct_n
    sess.accuracy = accuracy
    sess.report_notes = notes
    sess.submitted_at = now

    p = get_or_create_profile(db, student.id)
    stats = dict(p.practice_stats or {})
    week_q = list(stats.get("weekly_solves") or [0] * 7)
    if len(week_q) < 7:
        week_q = (week_q + [0] * 7)[:7]
    week_q[now.weekday()] = int(week_q[now.weekday()]) + len(rows)
    stats["weekly_solves"] = week_q
    stats["accuracy"] = accuracy
    stats["last_session"] = {
        "session_id": sess.id,
        "correct": correct_n,
        "total": len(rows),
        "accuracy": accuracy,
        "tags": uniq_session[:8],
        "missed_tags": uniq_missed[:8],
        "at": now.isoformat(),
    }
    # 错题标签分布（供学情可视化）
    from app.db.models_ext import Mistake

    mrows = list(
        db.scalars(
            select(Mistake).where(
                Mistake.student_id == student.id, Mistake.deleted_at.is_(None)
            )
        ).all()
    )
    tag_freq: dict[str, int] = {}
    for m in mrows:
        for t in tags_list(m.knowledge_tags):
            if t and t != "未标注":
                tag_freq[t] = tag_freq.get(t, 0) + 1
    top_tags = [
        {"name": k, "count": v}
        for k, v in sorted(tag_freq.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
    ]
    stats["mistake_stats"] = {"count": len(mrows), "top_tags": top_tags}
    radar = [{"name": k, "value": round(float(v) * 100)} for k, v in (p.mastery or {}).items()]
    stats["knowledge_radar"] = radar
    p.practice_stats = stats
    if uniq_missed:
        # 错点前置进薄弱列表
        weak = list(dict.fromkeys([*uniq_missed, *(p.weak_points or [])]))[:8]
        p.weak_points = weak
    db.commit()

    return {
        "ok": True,
        "session_id": sess.id,
        "total": len(rows),
        "correct": correct_n,
        "accuracy": accuracy,
        "report_notes": notes,
        "results": results,
        "last_session": stats["last_session"],
        "session": _session_summary(sess),
    }


def list_practice_sessions(
    db: Session, *, student_id: int, limit: int = 30
) -> dict[str, Any]:
    limit = max(1, min(int(limit or 30), 100))
    rows = list(
        db.scalars(
            select(PracticeSession)
            .where(
                PracticeSession.student_id == student_id,
                PracticeSession.status == "submitted",
            )
            .order_by(PracticeSession.submitted_at.desc(), PracticeSession.id.desc())
            .limit(limit)
        ).all()
    )
    return {"ok": True, "items": [_session_summary(r) for r in rows]}


def get_practice_session(
    db: Session, *, student_id: int, session_id: int
) -> dict[str, Any]:
    sess = db.get(PracticeSession, session_id)
    if not sess or sess.student_id != student_id:
        raise HTTPException(status_code=404, detail="加练场次不存在")
    answers = list(
        db.scalars(
            select(PracticeAnswer)
            .where(PracticeAnswer.session_id == sess.id)
            .order_by(PracticeAnswer.order_no.asc())
        ).all()
    )
    return {
        "ok": True,
        "session": _session_summary(sess),
        "items": [_answer_dict(a) for a in answers],
        "total": sess.item_count,
        "correct": sess.correct_count,
        "accuracy": sess.accuracy,
        "report_notes": list(sess.report_notes or []),
        "results": [_answer_dict(a) for a in answers],
    }
