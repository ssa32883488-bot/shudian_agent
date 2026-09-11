# -*- coding: utf-8 -*-
"""批量喂试卷图到 /api/student/solve，落盘答案与配图，汇总 Markdown。

用法（不要依赖命令行中文参数）：
  python -u scripts/batch_exam_solve.py
  python -u scripts/batch_exam_solve.py --paper 1
  python -u scripts/batch_exam_solve.py --paper 2
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

import httpx

ROOT = Path(r"F:\code\揭榜挂帅-单学科教育智能体")
PAPER_ROOT = ROOT / "_archive" / "课本" / "试卷"
OUT = ROOT / "shudian_agent" / "reports" / "exam_batch"
BASE = "http://127.0.0.1:8001"
PHONE = "13800000001"
PASSWORD = "123456"
TIMEOUT = 240.0

PAPERS = {
    "1": "第一套",
    "2": "第二套",
    "第一套": "第一套",
    "第二套": "第二套",
}

LOG = OUT / "batch.log"


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def login(client: httpx.Client) -> str:
    r = client.post(
        f"{BASE}/api/auth/login",
        json={"phone": PHONE, "password": PASSWORD},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    tok = data.get("token")
    if not tok:
        raise RuntimeError(f"login failed: {data}")
    return tok


def list_paper_images(paper: str) -> list[Path]:
    d = PAPER_ROOT / paper
    if not d.is_dir():
        raise FileNotFoundError(f"paper dir missing: {d}")
    files = [
        p
        for p in d.iterdir()
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]
    return sorted(files, key=lambda p: p.name)


def b64_image(path: Path) -> str:
    raw = path.read_bytes()
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def download(client: httpx.Client, url: str, dest: Path) -> Path | None:
    if not url:
        return None
    try:
        if url.startswith("/"):
            url = BASE + url
        r = client.get(url, timeout=60)
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        return dest
    except Exception as exc:  # noqa: BLE001
        log(f"  download fail {url}: {exc}")
        return None


def solve_one(client: httpx.Client, token: str, img: Path) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    body = {"image_base64": b64_image(img), "text": None}
    t0 = time.time()
    try:
        r = client.post(
            f"{BASE}/api/student/solve",
            headers=headers,
            json=body,
            timeout=TIMEOUT,
        )
        elapsed = time.time() - t0
        if r.status_code != 200:
            return {
                "ok": False,
                "status": r.status_code,
                "error": r.text[:800],
                "elapsed": elapsed,
                "source_image": str(img),
            }
        data = r.json()
        data["ok"] = True
        data["elapsed"] = elapsed
        data["source_image"] = str(img)
        return data
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed": time.time() - t0,
            "source_image": str(img),
            "traceback": traceback.format_exc(),
        }


def has_draw_fail(answer: str) -> bool:
    a = answer or ""
    return ("配图未生成" in a) or ("Agent 未产生文本回答" in a) or ("未产生文本回答" in a)


def rewrite_images_in_md(md: str, mapping: dict[str, str]) -> str:
    def sub(m: re.Match) -> str:
        alt, url = m.group(1), m.group(2)
        local = mapping.get(url) or mapping.get(url.split("?")[0])
        if local:
            return f"![{alt}]({local})"
        return m.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", sub, md or "")


def process_paper(client: httpx.Client, token: str, paper: str) -> Path:
    images = list_paper_images(paper)
    paper_out = OUT / paper
    img_out = paper_out / "images"
    img_out.mkdir(parents=True, exist_ok=True)
    results_path = paper_out / "results.jsonl"
    md_path = paper_out / f"{paper}-答案.md"
    state_path = paper_out / "state.json"

    # resume support：仅跳过「成功且无配图失败」的题；--force 时全量重跑
    force = bool(getattr(process_paper, "_force", False))
    done_names: set[str] = set()
    results: list[dict] = []
    if results_path.is_file() and not force:
        for line in results_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            src = Path(row.get("source_image") or "").name
            ans = str(row.get("answer") or "")
            if src and row.get("ok") and not has_draw_fail(ans):
                done_names.add(src)
                results.append(row)

    log(
        f"======== {paper} 共 {len(images)} 图；可跳过 {len(done_names)} "
        f"force={force} ========"
    )

    mode = "a" if results else "w"
    with results_path.open(mode, encoding="utf-8") as jf:
        for i, img in enumerate(images, 1):
            if img.name in done_names:
                log(f"[{paper} {i}/{len(images)}] SKIP {img.name}")
                continue

            log(f"[{paper} {i}/{len(images)}] START {img.name}")
            stem_name = f"q{i:02d}_stem{img.suffix.lower()}"
            shutil.copy2(img, img_out / stem_name)

            data = solve_one(client, token, img)
            if (not data.get("ok")) or has_draw_fail(str(data.get("answer") or "")):
                log(
                    f"  soft-fail → retry  err={str(data.get('error') or 'draw_fail')[:160]}"
                )
                time.sleep(2)
                data2 = solve_one(client, token, img)
                if data2.get("ok"):
                    a2 = str(data2.get("answer") or "")
                    a1 = str(data.get("answer") or "")
                    if (not has_draw_fail(a2)) or len(a2) > len(a1):
                        data = data2

            url_map: dict[str, str] = {}
            saved_imgs: list[str] = []
            urls = list(data.get("images") or [])
            for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", str(data.get("answer") or "")):
                urls.append(m.group(1))
            seen: set[str] = set()
            for j, url in enumerate(urls, 1):
                if not url or url in seen:
                    continue
                seen.add(url)
                ext = ".svg" if ".svg" in url.lower() else Path(url).suffix or ".png"
                if ext not in {".svg", ".png", ".jpg", ".jpeg", ".webp"}:
                    ext = ".png"
                dest = img_out / f"q{i:02d}_fig{j}{ext}"
                got = download(client, url, dest)
                if got:
                    rel = f"images/{got.name}"
                    url_map[url] = rel
                    saved_imgs.append(rel)

            data["_index"] = i
            data["_stem"] = f"images/{stem_name}"
            data["_saved_images"] = saved_imgs
            data["_url_map"] = url_map
            slim = {
                k: v
                for k, v in data.items()
                if k not in {"trace", "kg_context"}
            }
            jf.write(json.dumps(slim, ensure_ascii=False) + "\n")
            jf.flush()
            results.append(data)

            ans = str(data.get("answer") or "")
            log(
                f"  DONE ok={data.get('ok')} elapsed={float(data.get('elapsed') or 0):.1f}s "
                f"trust={data.get('trust_label')} hit={data.get('hit')} "
                f"draw_fail={has_draw_fail(ans)} imgs={len(saved_imgs)} ans_len={len(ans)}"
            )
            if not data.get("ok"):
                log(f"  ERROR: {data.get('error')}")

            state_path.write_text(
                json.dumps(
                    {"paper": paper, "last_index": i, "last_image": img.name},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

    # rebuild markdown from all jsonl rows (re-read)
    rows: list[dict] = []
    for line in results_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    # keep last result per source image
    by_src: dict[str, dict] = {}
    for r in rows:
        by_src[Path(r.get("source_image") or "").name or str(r.get("_index"))] = r
    ordered = sorted(by_src.values(), key=lambda r: int(r.get("_index") or 0))

    lines = [
        f"# {paper} 答案（学灵伴自动求解）",
        "",
        f"> 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"> 题目图数：{len(ordered)}  ",
        f"> 接口：`POST {BASE}/api/student/solve`",
        "",
    ]
    for data in ordered:
        i = data.get("_index")
        lines.append(f"## 第 {i} 题（图）")
        lines.append("")
        lines.append("**原题图片**：")
        lines.append("")
        lines.append(f"![题干]({data.get('_stem')})")
        lines.append("")
        qtext = (data.get("question_text") or "").strip()
        if qtext:
            lines.append("**识别题面**：")
            lines.append("")
            lines.append(qtext)
            lines.append("")
        trust = data.get("trust_label") or ("OK" if data.get("ok") else "失败")
        hit = f"（题库 #{data.get('hit_question_id')}）" if data.get("hit") else ""
        lines.append(f"**可信度**：{trust}{hit}")
        lines.append("")
        if not data.get("ok"):
            lines.append(f"**错误**：{data.get('error')}")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue
        ans = rewrite_images_in_md(str(data.get("answer") or ""), data.get("_url_map") or {})
        lines.append("### 解答")
        lines.append("")
        lines.append(ans.strip() or "_（空回答）_")
        lines.append("")
        analysis = (data.get("analysis") or "").strip()
        if analysis:
            lines.append("<details><summary>决策/匹配摘要</summary>")
            lines.append("")
            lines.append(analysis[:2000])
            lines.append("")
            lines.append("</details>")
            lines.append("")
        lines.append("---")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Wrote {md_path}")
    return md_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", action="append", default=[], help="1/2/第一套/第二套；可重复")
    ap.add_argument(
        "--force",
        action="store_true",
        help="忽略已有成功缓存，全量重跑该卷",
    )
    args = ap.parse_args()
    keys = args.paper or ["1", "2"]
    papers: list[str] = []
    for k in keys:
        name = PAPERS.get(k)
        if not name:
            log(f"unknown paper key: {k}")
            return 2
        if name not in papers:
            papers.append(name)

    OUT.mkdir(parents=True, exist_ok=True)
    process_paper._force = bool(args.force)  # type: ignore[attr-defined]
    log(f"batch start papers={papers} force={args.force}")
    with httpx.Client() as client:
        # health
        try:
            h = client.get(f"{BASE}/docs", timeout=10)
            log(f"backend docs status={h.status_code}")
        except Exception as exc:  # noqa: BLE001
            log(f"backend unreachable: {exc}")
            return 1
        token = login(client)
        log("login ok")
        for paper in papers:
            process_paper(client, token, paper)
    log("ALL DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
