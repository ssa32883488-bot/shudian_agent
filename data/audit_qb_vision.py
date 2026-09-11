#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""鍏ㄩ噺棰樺簱閰嶅浘瑙嗚澶嶆锛氶€愰璋冪敤瑙嗚妯″瀷鍒ゆ柇閰嶅浘鏄惁杩囧叧銆?""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(BACKEND / ".env")

from openai import OpenAI  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.db import SessionLocal  # noqa: E402
from app.db.models import QuestionBank  # noqa: E402

MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

CHAPTER_IMG = (
    ROOT.parent
    / "璇炬湰"
    / "璇炬湰鍔犱範棰樺唽"
    / "markdown_浜戠瑙ｆ瀽"
    / "鎸夌珷鑺傛媶鍒?
    / "images"
)
GUIDE_IMG = (
    ROOT.parent
    / "璇炬湰"
    / "璇炬湰鍔犱範棰樺唽"
    / "markdown_浜戠瑙ｆ瀽"
    / "瀛︿範杈呭鎸夌珷鑺傛媶鍒?
    / "images"
)


def resolve_local(url: str) -> Path | None:
    name = Path(url.replace("\\", "/")).name
    if not name:
        return None
    if "/guide/" in url.replace("\\", "/"):
        p = GUIDE_IMG / name
        if p.exists():
            return p
    if "/chapters/" in url.replace("\\", "/"):
        p = CHAPTER_IMG / name
        if p.exists():
            return p
    for root in (CHAPTER_IMG, GUIDE_IMG):
        p = root / name
        if p.exists():
            return p
    return None


def b64_image(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    ext = path.suffix.lower().lstrip(".") or "jpeg"
    if ext == "jpg":
        ext = "jpeg"
    return ext, base64.standard_b64encode(raw).decode("ascii")


def strip_md_images(text: str) -> str:
    return MD_IMG_RE.sub("[閰嶅浘]", text or "")


def build_client() -> tuple[OpenAI, str]:
    base = os.getenv("MIMO_API_BASE", "https://api.deepseek.com/v1").rstrip("/")
    key = os.getenv("DEEPSEEK_KEY", "")
    model = os.getenv("MIMO_OCR_MODEL") or os.getenv("MIMO_MODEL") or "deepseek-v4-flash-vision-exp"
    if not key:
        raise SystemExit("DEEPSEEK_KEY 鏈厤缃?)
    return OpenAI(base_url=base, api_key=key), model


PROMPT = """浣犳槸鏁板瓧鐢靛瓙鎶€鏈搴撹川妫€鍛樸€傝缁撳悎銆愰骞层€戙€愮瓟妗堛€戜笌閰嶅浘锛屼弗鏍煎垽鏂湰棰橀厤鍥炬槸鍚﹁繃鍏炽€?

妫€鏌ヨ鐐癸細
1. 姣忓紶鍥炬槸鍚﹀睘浜庢湰棰橈紙涓嶆槸浠栭鐢佃矾/娉㈠舰璇寕锛?
2. 鏄惁鍑虹幇銆屼竴寮犲浘閲屾尋浜嗗閬撻鎴栧娈电瓟妗堛€嶄笖鏈媶寮€
3. 棰樺共鍐欍€屽鍥俱€嶄絾鍥句笌鏂囧瓧鏉′欢鏄庢樉涓嶇
4. 绛旀鍥炬槸鍚﹀儚瑙ｇ瓟鍥撅紙鐪熷€艰〃/娉㈠舰/鍖栫畝缁撴灉锛夛紝鑰岄潪瀹屽叏鏃犲叧

鍙緭鍑?JSON锛堜笉瑕?Markdown锛夛細
{
  "pass": true/false,
  "score": 0.0鍒?.0,
  "issues": ["涓枃闂锛屾棤鍒欑┖鏁扮粍"],
  "per_image": [{"alt":"鍥惧彿鎴栫┖","ok":true/false,"note":"涓€鍙ヨ鏄?}]
}
"""


def judge_one(
    client: OpenAI,
    model: str,
    *,
    eid: str,
    source: str,
    stem: str,
    answer: str,
    images: list[dict[str, Any]],
) -> dict[str, Any]:
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                f"{PROMPT}\n\n銆愰鐩爣璇嗐€憑eid} / {source}\n\n"
                f"銆愰骞层€慭n{strip_md_images(stem)[:1800]}\n\n"
                f"銆愮瓟妗堛€慭n{strip_md_images(answer)[:1800]}\n"
            ),
        }
    ]
    used = 0
    for im in images[:4]:
        path = im.get("path")
        if not path:
            continue
        ext, b64 = b64_image(Path(path))
        content.append(
            {
                "type": "text",
                "text": f"閰嶅浘 alt={im.get('alt') or ''} kind={im.get('kind') or ''}",
            }
        )
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/{ext};base64,{b64}"},
            }
        )
        used += 1
    if used == 0:
        return {
            "pass": False,
            "score": 0.0,
            "issues": ["閰嶅浘鏂囦欢鏈湴缂哄け锛屾棤娉曡瘑鍥?],
            "per_image": [],
            "vision_skipped": True,
        }

    last_raw = ""
    for attempt in range(3):
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "鍙緭鍑哄悎娉?JSON 瀵硅薄锛屼笉瑕?Markdown 浠ｇ爜鍧楋紝涓嶈瑙ｉ噴銆?,
                },
                {"role": "user", "content": content},
            ],
            temperature=0.1,
            max_tokens=1200,
        )
        raw = (resp.choices[0].message.content or "").strip()
        last_raw = raw
        if not raw:
            time.sleep(0.8 * (attempt + 1))
            continue
        data: dict[str, Any] = {}
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            m = re.search(r"\{[\s\S]*\}", raw)
            if m:
                try:
                    data = json.loads(m.group(0))
                except json.JSONDecodeError:
                    data = {}
        if data:
            return {
                "pass": bool(data.get("pass")),
                "score": float(data.get("score") or 0.0),
                "issues": list(data.get("issues") or []),
                "per_image": list(data.get("per_image") or []),
                "attempts": attempt + 1,
            }
        time.sleep(0.8 * (attempt + 1))
    return {
        "pass": False,
        "score": 0.0,
        "issues": [f"瑙嗚妯″瀷杩斿洖鏃犳硶瑙ｆ瀽: {last_raw[:200]}"],
        "per_image": [],
        "raw": last_raw[:500],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="浠呮祴鍓?N 閬撳惈鍥鹃锛?=鍏ㄩ噺")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.4)
    ap.add_argument("--out", type=str, default=str(ROOT / "reports" / "qb_vision_full_audit.json"))
    ap.add_argument("--resume", action="store_true", help="璺宠繃宸叉湁缁撴灉")
    ap.add_argument(
        "--eids-file",
        type=str,
        default="",
        help="鍙璁¤鏂囦欢涓殑棰樺彿锛堟瘡琛屼竴涓紝濡?棰?.6 / 渚?.6.8锛?,
    )
    ap.add_argument(
        "--eids",
        type=str,
        default="",
        help="閫楀彿鍒嗛殧棰樺彿锛屽彧瀹¤杩欎簺棰?,
    )
    args = ap.parse_args()

    client, model = build_client()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prev: dict[str, Any] = {"results": []}
    done_ids: set[int] = set()
    if args.resume and out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        done_ids = {int(x["id"]) for x in prev.get("results") or [] if "id" in x}

    want_eids: set[str] = set()
    if args.eids:
        want_eids.update(x.strip() for x in args.eids.split(",") if x.strip())
    if args.eids_file:
        p = Path(args.eids_file)
        want_eids.update(
            ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()
        )

    def _row_eid(r: QuestionBank) -> str:
        m = re.search(r"绗琝d+绔犅?.+)$", r.source or "")
        return m.group(1) if m else ""

    db = SessionLocal()
    rows = list(
        db.scalars(
            select(QuestionBank)
            .where(QuestionBank.status == "active", QuestionBank.source.like("璇炬湰路%"))
            .order_by(QuestionBank.id)
        ).all()
    )
    db.close()

    queue: list[QuestionBank] = []
    for r in rows:
        eid = _row_eid(r)
        if want_eids and eid not in want_eids:
            continue
        if want_eids or MD_IMG_RE.search((r.content or "") + "\n" + (r.answer or "")):
            queue.append(r)
    queue = queue[args.offset :]
    if args.limit and args.limit > 0:
        queue = queue[: args.limit]

    results = list(prev.get("results") or [])
    missing_files = 0
    t0 = time.time()
    for i, r in enumerate(queue):
        if r.id in done_ids:
            continue
        imgs_meta = []
        for alt, url in MD_IMG_RE.findall((r.content or "") + "\n" + (r.answer or "")):
            kind = "guide" if "/guide/" in url else "chapters" if "/chapters/" in url else "unk"
            loc = resolve_local(url)
            if not loc:
                missing_files += 1
            imgs_meta.append(
                {
                    "alt": alt,
                    "url": url,
                    "kind": kind,
                    "path": str(loc) if loc else None,
                }
            )
        eid = ""
        m = re.search(r"绗琝d+绔犅?.+)$", r.source or "")
        if m:
            eid = m.group(1)
        try:
            verdict = judge_one(
                client,
                model,
                eid=eid,
                source=r.source or "",
                stem=r.content or "",
                answer=r.answer or "",
                images=imgs_meta,
            )
        except Exception as exc:  # noqa: BLE001
            verdict = {
                "pass": False,
                "score": 0.0,
                "issues": [f"璋冪敤澶辫触: {exc}"],
                "per_image": [],
                "error": str(exc),
            }
        rec = {
            "id": r.id,
            "source": r.source,
            "eid": eid,
            "n_imgs": len(imgs_meta),
            "resolved": sum(1 for x in imgs_meta if x["path"]),
            "verdict": verdict,
        }
        results.append(rec)
        done_ids.add(r.id)
        # 澧為噺钀界洏
        summary = {
            "model": model,
            "total_queued": len(queue),
            "done": len(results),
            "pass": sum(1 for x in results if (x.get("verdict") or {}).get("pass")),
            "fail": sum(1 for x in results if not (x.get("verdict") or {}).get("pass")),
            "missing_files_events": missing_files,
            "elapsed_sec": round(time.time() - t0, 1),
            "results": results,
        }
        out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        status = "PASS" if verdict.get("pass") else "FAIL"
        print(
            f"[{len(results)}/{len(queue)+args.offset}] {status} id={r.id} {eid} "
            f"score={verdict.get('score')} issues={verdict.get('issues')[:2]}"
        )
        if args.sleep > 0:
            time.sleep(args.sleep)
