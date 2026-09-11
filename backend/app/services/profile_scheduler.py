"""学情画像夜间批跑：每天 03:00（默认 Asia/Shanghai）。"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

_stop = threading.Event()
_thread: threading.Thread | None = None
_SHANGHAI = timezone(timedelta(hours=8), name="Asia/Shanghai")


def _resolve_tz(tz_name: str = "Asia/Shanghai"):
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(tz_name)
    except Exception:
        # Windows 常缺 tzdata；回退固定 UTC+8
        if tz_name in ("Asia/Shanghai", "Asia/Chongqing", "PRC"):
            return _SHANGHAI
        return timezone.utc


def _seconds_until_next_run(tz_name: str = "Asia/Shanghai", hour: int = 3) -> float:
    tz = _resolve_tz(tz_name)
    now = datetime.now(tz)
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    return max(1.0, (target - now).total_seconds())


def _loop(tz_name: str = "Asia/Shanghai", hour: int = 3) -> None:
    logger.info("profile nightly scheduler started (tz=%s hour=%s)", tz_name, hour)
    while not _stop.is_set():
        try:
            wait = _seconds_until_next_run(tz_name, hour)
        except Exception as exc:
            logger.warning("schedule compute failed, retry in 60s: %s", exc)
            wait = 60.0
        logger.info("next profile rebuild in %.0f s", wait)
        if _stop.wait(wait):
            break
        try:
            from app.db import SessionLocal
            from app.services.memory import rebuild_all_active_profiles

            db = SessionLocal()
            try:
                n = rebuild_all_active_profiles(db)
                logger.info("nightly profile rebuild done: %s students", n)
            finally:
                db.close()
        except Exception as exc:
            logger.warning("nightly profile rebuild error: %s", exc)
        # 防止同一分钟内重复触发
        time.sleep(61)
    logger.info("profile nightly scheduler stopped")


def start_profile_scheduler(*, tz_name: str = "Asia/Shanghai", hour: int = 3) -> None:
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop.clear()
    _thread = threading.Thread(
        target=_loop,
        kwargs={"tz_name": tz_name, "hour": hour},
        name="profile-nightly",
        daemon=True,
    )
    _thread.start()


def stop_profile_scheduler() -> None:
    _stop.set()
