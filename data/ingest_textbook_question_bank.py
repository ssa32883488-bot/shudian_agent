#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""课本习题/例题灌入正式题库 question_bank + Chroma。

权威来源：
  - canonical chXX/chunks.jsonl：
      * block_type=exercise_merged（章末习题）
      * block_type=example（课文例题）
  - 章末习题解答优先取学习辅导 MD【题 x.y】
  - knowledge_graph_v0.2.json 的 TESTS 边 → knowledge_tags

用法（在 shudian_agent 根目录）:
  python data/ingest_textbook_question_bank.py --dry-run --report reports/qb_dryrun.json
  python data/ingest_textbook_question_bank.py --reset-qb --report reports/qb_ingest.json
  python data/ingest_textbook_question_bank.py --kinds example --dry-run
  python data/ingest_textbook_question_bank.py --kinds example --report reports/qb_examples.json
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
REPO = ROOT.parent
sys.path.insert(0, str(BACKEND))

from app.config import get_settings  # noqa: E402
from scripts.textbook.media_urls import (  # noqa: E402
    local_path_to_object_key,
    media_public_url,
    rewrite_media_urls,
)

CANONICAL = BACKEND / "data" / "canonical"
KG_PATH = ROOT / "data" / "kg" / "knowledge_graph_v0.2.json"
CHAPTERS_MD_DIR = (
    REPO / "课本" / "课本加习题册" / "markdown_云端解析" / "按章节拆分"
)
GUIDE_MD_DIR = (
    REPO / "课本" / "课本加习题册" / "markdown_云端解析" / "学习辅导按章节拆分"
)

SOURCE_PREFIX = "课本·"
EXERCISE_ID_RE = re.compile(r"^题(\d+)\.(\d+)$")
EXAMPLE_ID_RE = re.compile(r"^例(\d+(?:\.\d+)+)$")
STEM_ANS_RE = re.compile(
    r"【题\s*(?P<num>[\d.]+)\s*题干】\s*(?P<stem>.*?)\s*"
    r"【题\s*(?P=num)\s*解答】\s*(?P<answer>.*)\s*\Z",
    re.S,
)
GUIDE_Q_RE = re.compile(
    r"【题\s*(?P<num>\d+\.\d+)】\s*(?P<body>.*?)(?=【题\s*\d+\.\d+】|\Z)",
    re.S,
)
EXAMPLE_HEAD_RE = re.compile(r"【例\s*(?P<num>[\d.]+)】\s*(?P<body>.*)\s*\Z", re.S)
EXAMPLE_SOL_RE = re.compile(r"(?m)^解[：:]\s*")
MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
# 仅匹配 Windows 盘符绝对路径，避免误伤 LaTeX 的 \\command
LOCAL_PATH_RE = re.compile(
    r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*"
    r"|[A-Za-z]:/(?:[^/\s)\"']+/)*[^/\s)\"']+"
)
# canonical 解答末尾常见的视觉图注块（可能串题）
VISION_CAPTION_RE = re.compile(
    r"(?m)^\[图\s*(?P<body>P?\d+(?:\.\d+)*(?:\([a-z]\))?)\][^\n]*\n"
    r"(?:\[图[^\]]*描述\][^\n]*\n?)*"
)
# 教材 OCR/排版串入的孤立图注行，如单独一行「图 P7.4」
ORPHAN_FIG_CAPTION_LINE_RE = re.compile(
    r"(?m)^[ \t]*图[ \t]*(?P<body>[PA]?[ \t]*\d+(?:[.\uFF0E]\d+)*(?:\([a-z]\))?)[ \t]*$"
)
# 例题图注行：图2.6.3 例2.6.9的…
EXAMPLE_CAPTION_LINE_RE = re.compile(
    r"(?m)^[ \t]*图[ \t]*(?P<body>\d+(?:[.\uFF0E]\d+)*(?:\([a-z]\))?)[ \t]+"
    r"例[ \t]*(?P<eg>\d+(?:[.\uFF0E]\d+)+)[^\n]*$"
)
FIG_REF_RE = re.compile(
    r"图\s*(?P<body>(?:P?\d+)(?:[\.\-．]\d+)*(?:\([a-z]\))?)",
    re.I,
)
ACCEPTANCE_SEED = 20260903
BREADCRUMB_RE = re.compile(r"^第\d+章[^\n]*\n+")


# ---------------------------------------------------------------------------
# KG
# ---------------------------------------------------------------------------


def load_kg(path: Path = KG_PATH) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"缺少知识图谱: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_tests_index(kg: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    concepts = {c["id"]: c for c in kg.get("nodes", {}).get("Concept", [])}
    edges = kg.get("edges") or {}
    tests = edges.get("TESTS", []) if isinstance(edges, dict) else [
        e for e in edges if isinstance(e, dict) and e.get("type") == "TESTS"
    ]
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: dict[str, set[str]] = defaultdict(set)
    for e in tests:
        frm = e.get("from") or e.get("from_id")
        cid = e.get("to_id") or ""
        cname = e.get("to") or concepts.get(cid, {}).get("name") or ""
        if not frm or not cid:
            continue
        if cid in seen[frm]:
            continue
        seen[frm].add(cid)
        out[frm].append({"concept_id": cid, "name": cname})
    return out


def chapter_exercise_ids(kg: dict[str, Any]) -> set[str]:
    return {
        p["id"]
        for p in kg.get("nodes", {}).get("Problem", [])
        if p.get("kind") == "chapter_exercise" and p.get("id")
    }


# ---------------------------------------------------------------------------
# Guide / chapter MD
# ---------------------------------------------------------------------------


def _chapter_md_path(chapter_num: int) -> Optional[Path]:
    if not CHAPTERS_MD_DIR.is_dir():
        return None
    hits = sorted(CHAPTERS_MD_DIR.glob(f"*第0{chapter_num}章*.md"))
    return hits[0] if hits else None


def _guide_md_path(chapter_num: int) -> Optional[Path]:
    if not GUIDE_MD_DIR.is_dir():
        return None
    hits = sorted(GUIDE_MD_DIR.glob(f"*第0{chapter_num}章*习题解答.md"))
    return hits[0] if hits else None


def load_guide_answers(chapter_num: int) -> dict[str, str]:
    path = _guide_md_path(chapter_num)
    if not path:
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for m in GUIDE_Q_RE.finditer(text):
        num = m.group("num")
        body = label_guide_section_images((m.group("body") or "").strip(), num)
        out[f"题{num}"] = body
    return out


def label_guide_section_images(body: str, q_num: str) -> str:
    """给【题 x.y】段内空 alt 图补标；下一图注属他题则删图，属本题则按组打 图P/A 号。"""
    if not body or not q_num:
        return body

    from collections import defaultdict

    fig_cap_re = re.compile(
        r"图\s*(?P<ap>[AP])?\s*(?P<num>\d+(?:\.\d+)+)(?:\((?P<sub>[a-z])\))?",
        re.I,
    )

    def _next_cap(text: str, pos: int, limit: int = 900) -> re.Match[str] | None:
        return fig_cap_re.search(text[pos : pos + limit])

    out = body
    empty = [m for m in MD_IMG_RE.finditer(out) if not (m.group(1) or "").strip()]
    if not empty:
        return out

    sol = re.search(r"(?m)^解[：:]", out)
    sol_pos = sol.start() if sol else -1

    actions: list[tuple[str, int, int, str, str]] = []
    for em in empty:
        url = em.group(2).strip()
        cm = _next_cap(out, em.end())
        if not cm:
            actions.append(("orphan", em.start(), em.end(), "", url))
            continue
        num = cm.group("num").replace(" ", "").replace("．", ".")
        if num != q_num:
            actions.append(("del", em.start(), em.end(), "", url))
            continue
        ap = (cm.group("ap") or "").upper()
        if ap in ("A", "P"):
            parent = f"图{ap}{num}"
        else:
            kind = "A" if sol_pos >= 0 and em.start() >= sol_pos else "P"
            parent = f"图{kind}{num}"
        actions.append(("grp", em.start(), em.end(), parent, url))

    grp_members: dict[str, list[tuple[int, int, str]]] = defaultdict(list)
    finals: list[tuple[int, int, str, str]] = []
    dels: list[tuple[int, int]] = []
    orphans: list[tuple[int, int, str]] = []
    for kind, start, end, parent, url in actions:
        if kind == "del":
            dels.append((start, end))
        elif kind == "orphan":
            orphans.append((start, end, url))
        else:
            grp_members[parent].append((start, end, url))

    for parent, members in grp_members.items():
        members = sorted(members, key=lambda x: x[0])
        if len(members) == 1:
            finals.append((members[0][0], members[0][1], parent, members[0][2]))
        else:
            for i, (start, end, url) in enumerate(members):
                finals.append(
                    (start, end, f"{parent}({chr(ord('a') + i)})", url)
                )

    used = {normalize_fig_id(lab) for _, _, lab, _ in finals}
    own_caps: list[str] = []
    for m in fig_cap_re.finditer(out):
        num = m.group("num").replace(" ", "")
        ap = (m.group("ap") or "").upper()
        if num != q_num or ap not in ("A", "P"):
            continue
        fid = f"图{ap}{num}"
        if m.group("sub"):
            fid = f"{fid}({m.group('sub')})"
        nf = normalize_fig_id(fid)
        if nf in used:
            continue
        if any(
            nf == normalize_fig_id(p) or nf.startswith(normalize_fig_id(p) + "(")
            for p in grp_members
        ):
            continue
        if fid not in own_caps:
            own_caps.append(fid)

    if orphans and own_caps:
        n = min(len(orphans), len(own_caps))
        for (start, end, url), lab in zip(orphans[:n], own_caps[:n]):
            finals.append((start, end, lab, url))
        for start, end, _ in orphans[n:]:
            dels.append((start, end))
    else:
        for start, end, _ in orphans:
            dels.append((start, end))

    label_map = {start: (lab, url) for start, _end, lab, url in finals}
    del_set = {start for start, _end in dels}
    pieces: list[str] = []
    last = 0
    for em in MD_IMG_RE.finditer(out):
        if (em.group(1) or "").strip():
            continue
        if em.start() in del_set:
            pieces.append(out[last : em.start()])
            last = em.end()
        elif em.start() in label_map:
            lab, url = label_map[em.start()]
            pieces.append(out[last : em.start()])
            pieces.append(f"![{lab}]({url})")
            last = em.end()
    pieces.append(out[last:])
    return re.sub(r"\n{3,}", "\n\n", "".join(pieces)).strip()


def load_guide_labeled_figures(chapter_num: int, media_base: str) -> dict[str, str]:
    """扫描学习辅导整章 MD：图A5.15 / 图P5.15 等标题旁的图片 → 公网 URL。

    辅导 MD 常把「题 5.15 的图」排在下一题标题之后，单靠【题】切段会丢图。
    连排多图 + 多图注时按顺序拆开配对，避免一图挂多题或整组糊到一题。
    """
    path = _guide_md_path(chapter_num)
    if not path:
        return {}
    text = path.read_text(encoding="utf-8")
    catalog: dict[str, str] = {}

    def _put(fid: str, name: str) -> None:
        if fid and name and fid not in catalog:
            catalog[fid] = media_public_url(f"guide/{name}", media_base)

    # 模式 A：单图后紧跟单图注
    for m in re.finditer(
        r"!\[([^\]]*)\]\(([^)]+)\)\s*(?:\n|\\)*\s*(图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?)",
        text,
        flags=re.I,
    ):
        raw_url, caption = m.group(2).strip(), m.group(3)
        _put(normalize_fig_id(caption), Path(raw_url.replace("\\", "/")).name)

    # 模式 B：单图注后紧跟单图
    for m in re.finditer(
        r"(图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?)\s*\n+!\[([^\]]*)\]\(([^)]+)\)",
        text,
        flags=re.I,
    ):
        _put(
            normalize_fig_id(m.group(1)),
            Path(m.group(3).replace("\\", "/")).name,
        )

    # 模式 C：连排多图 + 一行内多个图注 → 按顺序 1:1 拆配
    for m in re.finditer(
        r"((?:!\[[^\]]*\]\([^)]+\)\s*){2,})"
        r"(?:\n|\\)*\s*"
        r"((?:图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?\s*){2,})",
        text,
        flags=re.I,
    ):
        imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", m.group(1))
        caps = re.findall(
            r"图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?", m.group(2), flags=re.I
        )
        for raw_url, cap in zip(imgs, caps):
            _put(normalize_fig_id(cap), Path(raw_url.replace("\\", "/")).name)

    # 模式 D：多图注在前，连排多图在后
    for m in re.finditer(
        r"((?:图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?\s*){2,})"
        r"\s*\n+"
        r"((?:!\[[^\]]*\]\([^)]+\)\s*){2,})",
        text,
        flags=re.I,
    ):
        caps = re.findall(
            r"图\s*[AP]?\d+(?:\.\d+)*(?:\([a-z]\))?", m.group(1), flags=re.I
        )
        imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", m.group(2))
        for cap, raw_url in zip(caps, imgs):
            _put(normalize_fig_id(cap), Path(raw_url.replace("\\", "/")).name)

    # 模式 E：按题段给空 alt 补标后再入库（覆盖 图A2.16(a) 与图分离等情况）
    for m in GUIDE_Q_RE.finditer(text):
        num = m.group("num")
        labeled = label_guide_section_images((m.group("body") or "").strip(), num)
        for alt, raw_url in MD_IMG_RE.findall(labeled):
            alt_n = normalize_fig_id((alt or "").replace(" ", ""))
            if not re.match(rf"^图[AP]{re.escape(num)}(?:\([a-z]\))?$", alt_n):
                continue
            _put(alt_n, Path(raw_url.replace("\\", "/")).name)

    return catalog


def enrich_answer_with_guide_figures(
    answer: str,
    *,
    chapter_num: int,
    q_num: str,
    guide_figs: dict[str, str],
) -> str:
    """若解答提到 图A/Px.y 但无 markdown 图，则从辅导图目录补上。

    空 alt 若 URL 已在本题辅导目录中，先回填图号，避免占住 URL 导致图A挂不上。
    """
    if not guide_figs:
        return answer

    owned_url_to_fid: dict[str, str] = {}
    for fid, url in guide_figs.items():
        if fig_is_answer_sheet(fid, chapter_num, q_num) or fig_belongs_to_exercise(
            fid, chapter_num, q_num
        ):
            # 优先保留更具体的图号（带 (a) 的不覆盖父号已占时仍写入子号）
            if url not in owned_url_to_fid or ("(" in fid and "(" not in owned_url_to_fid[url]):
                owned_url_to_fid[url] = fid

    def _relabel_empty(m: re.Match[str]) -> str:
        alt, url = (m.group(1) or "").strip(), m.group(2).strip()
        if alt:
            return m.group(0)
        fid = owned_url_to_fid.get(url)
        if fid:
            return f"![{fid}]({url})"
        return m.group(0)

    answer = MD_IMG_RE.sub(_relabel_empty, answer or "")
    # 仍空 alt：习题解答里多为串题杂图，直接丢掉
    answer = re.sub(r"!\[\s*\]\([^)]+\)\s*", "", answer)
    answer = re.sub(r"\n{3,}", "\n\n", answer).strip()

    existing_urls = {u for _, u in MD_IMG_RE.findall(answer or "")}
    existing_alts = {
        normalize_fig_id(a) for a, _ in MD_IMG_RE.findall(answer or "") if a.strip()
    }
    refs = find_fig_refs(answer)
    prefer = [
        normalize_fig_id(f"图A{chapter_num}.{q_num}"),
        normalize_fig_id(f"图P{chapter_num}.{q_num}"),
    ]
    ordered = prefer + [
        r
        for r in refs
        if r not in prefer and not foreign_exercise_owner(r, chapter_num, q_num)
    ]
    extra: list[tuple[str, str]] = []
    seen_urls = set(existing_urls)

    def _already_have(ref: str) -> bool:
        if any(fig_matches_ref(ref, a) for a in existing_alts):
            return True
        return any(fig_matches_ref(ref, f) for f, _ in extra)

    for ref in ordered:
        if _already_have(ref):
            continue
        for fid, url in guide_figs.items():
            if foreign_exercise_owner(fid, chapter_num, q_num):
                continue
            if fig_matches_ref(ref, fid) and url not in seen_urls:
                extra.append((fid, url))
                seen_urls.add(url)
                existing_alts.add(normalize_fig_id(fid))
                break

    # 无论前面是否已挂其他图，都必须尽量补齐本题 图A*（含子图）
    for fid in prefer:
        if _already_have(fid):
            # 仍补子图 图A5.8(a)…
            pass
        else:
            url = guide_figs.get(fid)
            if url and url not in seen_urls:
                extra.append((fid, url))
                seen_urls.add(url)
                existing_alts.add(fid)
        for sub_fid, sub_url in guide_figs.items():
            if not fig_matches_ref(fid, sub_fid):
                continue
            if foreign_exercise_owner(sub_fid, chapter_num, q_num):
                continue
            if sub_url in seen_urls or _already_have(sub_fid):
                continue
            extra.append((sub_fid, sub_url))
            seen_urls.add(sub_url)
            existing_alts.add(normalize_fig_id(sub_fid))

    return append_media_markdown(answer, extra)


def strip_bare_and_empty_alt_images(text: str) -> str:
    """去掉空 alt，以及「图2」「图5」这类过短/无小数点的裸图号配图。"""

    def _sub(m: re.Match[str]) -> str:
        alt = (m.group(1) or "").strip().replace(" ", "")
        if not alt:
            return ""
        fid = normalize_fig_id(alt)
        # 图2 / 图5 / 图4 —— 无章节小数点，几乎必是 OCR 截断误标
        if re.fullmatch(r"图\d{1,2}", fid):
            return ""
        return m.group(0)

    cleaned = MD_IMG_RE.sub(_sub, text or "")
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def prefer_guide_media_for_owned(
    content: str,
    answer: str,
    *,
    chapter_num: int,
    q_num: str,
) -> tuple[str, str]:
    """若辅导已提供本题 图P/A，去掉题干里 chapters 侧同题配图（常为「习题」页误切）。"""
    guide_owned = [
        (normalize_fig_id(a), u)
        for a, u in MD_IMG_RE.findall(answer or "")
        if "/guide/" in u
        and (
            fig_belongs_to_exercise(a, chapter_num, q_num)
            or fig_is_answer_sheet(a, chapter_num, q_num)
        )
    ]
    if not guide_owned:
        return content, answer

    def _strip_chapter_owned(m: re.Match[str]) -> str:
        alt = normalize_fig_id((m.group(1) or "").replace(" ", ""))
        url = m.group(2)
        if "/chapters/" not in url:
            return m.group(0)
        if fig_belongs_to_exercise(alt, chapter_num, q_num) or fig_is_answer_sheet(
            alt, chapter_num, q_num
        ):
            return ""
        # 空 alt 的 chapters 图也去掉
        if not (m.group(1) or "").strip():
            return ""
        return m.group(0)

    new_content = MD_IMG_RE.sub(_strip_chapter_owned, content or "")
    new_content = re.sub(r"\n{3,}", "\n\n", new_content).strip()
    # 题干若已无本题图，把 guide 中的 图P* 补到题干
    content_alts = {
        normalize_fig_id(a)
        for a, _ in MD_IMG_RE.findall(new_content)
        if (a or "").strip()
    }
    need_p = not any(
        fig_belongs_to_exercise(a, chapter_num, q_num) for a in content_alts
    )
    if need_p:
        p_figs = [
            (a, u)
            for a, u in guide_owned
            if fig_belongs_to_exercise(a, chapter_num, q_num)
        ]
        if p_figs:
            new_content = append_media_markdown(new_content, p_figs)
            # 解答里去掉已挪到题干的同 URL
            moved = {u for _, u in p_figs}

            def _drop_moved(m: re.Match[str]) -> str:
                return "" if m.group(2).strip() in moved else m.group(0)

            answer = MD_IMG_RE.sub(_drop_moved, answer or "")
            answer = re.sub(r"\n{3,}", "\n\n", answer).strip()
    return new_content, answer


def rewrite_md_images(text: str, media_base: str, *, default_kind: str) -> str:
    """把 ![](images/hash.jpg) / 本地路径 改写为可访问 URL。"""

    def _sub(m: re.Match[str]) -> str:
        alt, raw = m.group(1), m.group(2).strip()
        if raw.startswith("http://") or raw.startswith("https://"):
            return m.group(0)
        # 相对 images/xxx 或仅文件名
        name = Path(raw.replace("\\", "/")).name
        if not name:
            return m.group(0)
        kind = default_kind
        norm = raw.replace("\\", "/")
        if "学习辅导" in norm or "/guide/" in norm.lower():
            kind = "guide"
        elif "按章节拆分" in norm and "学习辅导" not in norm:
            kind = "chapters"
        url = media_public_url(f"{kind}/{name}", media_base)
        return f"![{alt}]({url})"

    return MD_IMG_RE.sub(_sub, text or "")


def strip_local_paths(text: str) -> str:
    """兜底：去掉残留绝对路径片段（保留已是 http 的）。"""
    return LOCAL_PATH_RE.sub("", text or "")


def normalize_fig_id(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
    if not s.startswith("图"):
        s = "图" + s
    return s.replace(" ", "").replace("．", ".").replace("-", ".")


def find_fig_refs(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for m in FIG_REF_RE.finditer(text or ""):
        fid = normalize_fig_id("图" + m.group("body"))
        body = m.group("body") or ""
        if re.fullmatch(r"\d+", body):
            continue
        if fid and fid not in seen:
            seen.add(fid)
            found.append(fid)
    return found


def fig_belongs_to_exercise(fig_id: str, chapter_num: int, q_num: str) -> bool:
    """本题配图：图P4.1 / 图4.1(a) 算；图P4.10 不算。"""
    fid = normalize_fig_id(fig_id)
    for p in (f"图P{chapter_num}.{q_num}", f"图{chapter_num}.{q_num}"):
        if fid == p:
            return True
        if fid.startswith(p) and len(fid) > len(p) and fid[len(p)] in ".(":
            return True
    return False


def fig_is_answer_sheet(fig_id: str, chapter_num: int, q_num: str) -> bool:
    """学习辅导解答图：图A4.1 / 图A4.1(a)。"""
    fid = normalize_fig_id(fig_id)
    base = f"图A{chapter_num}.{q_num}"
    if fid == base:
        return True
    return fid.startswith(base) and len(fid) > len(base) and fid[len(base)] in ".("


def foreign_exercise_owner(fig_id: str, chapter_num: int, q_num: str) -> Optional[str]:
    """若图号明确属于其他习题（图P/A x.y），返回该题号；否则 None。"""
    fid = normalize_fig_id(fig_id)
    m = re.match(r"^图[PA](\d+)\.(\d+)", fid)
    if not m:
        return None
    ch, q = int(m.group(1)), m.group(2)
    if ch == chapter_num and q == q_num:
        return None
    return f"题{ch}.{q}"


def sanitize_pairs_for_exercise(
    pairs: list[tuple[str, str]],
    *,
    chapter_num: int,
    q_num: str,
    stem: str,
    answer: str,
) -> list[tuple[str, str]]:
    """过滤串题图：他题 图P/A 不得挂到本题，除非正文精确引用到该图号。"""
    refs = [normalize_fig_id(r) for r in find_fig_refs(stem) + find_fig_refs(answer)]
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for fid, url in pairs:
        if not url or url in seen:
            continue
        owner = foreign_exercise_owner(fid, chapter_num, q_num)
        if owner:
            # 仅当正文引用精确落到本图（边界匹配）才保留
            if not any(fig_matches_ref(r, fid) for r in refs):
                continue
        seen.add(url)
        out.append((fid, url))
    return out


def strip_orphan_foreign_fig_captions(
    text: str, *, chapter_num: int, q_num: str
) -> str:
    """去掉串题的孤立图注行（整行只有「图 P7.4」这类），保留本题图注。"""

    def _sub(m: re.Match[str]) -> str:
        fid = normalize_fig_id("图" + (m.group("body") or "").replace(" ", ""))
        if foreign_exercise_owner(fid, chapter_num, q_num):
            return ""
        return m.group(0)

    cleaned = ORPHAN_FIG_CAPTION_LINE_RE.sub(_sub, text or "")
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def strip_foreign_example_captions(text: str, *, example_id: str) -> str:
    """去掉图注写明其他例号的行，如「图2.6.3 例2.6.9的卡诺图」。"""
    eg = (example_id or "").replace("例", "").replace(" ", "").strip()

    def _sub(m: re.Match[str]) -> str:
        other = (m.group("eg") or "").replace(" ", "").replace("．", ".")
        if other and other != eg:
            return ""
        return m.group(0)

    cleaned = EXAMPLE_CAPTION_LINE_RE.sub(_sub, text or "")
    # 同步清 canonical 追加的 [图x] 例y… / 描述块
    def _keep_vision(m: re.Match[str]) -> str:
        body = m.group(0)
        om = re.search(r"例\s*(\d+(?:\.\d+)+)", body)
        if om and om.group(1).replace(" ", "") != eg:
            return ""
        return body

    cleaned = VISION_CAPTION_RE.sub(_keep_vision, cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def sanitize_pairs_for_example(
    pairs: list[tuple[str, str]],
    *,
    example_id: str,
    stem: str,
    answer: str,
) -> list[tuple[str, str]]:
    """例题只保留正文引用的图；丢弃未引用的邻节残留与他例图注。"""

    def _prose_refs(text: str) -> list[str]:
        # 去掉 canonical 追加的 [图x] / 描述行，避免图注自引用把对比图留住
        cleaned = VISION_CAPTION_RE.sub("", text or "")
        cleaned = re.sub(r"(?m)^\[图[^\]]*\][^\n]*\n?", "", cleaned)
        return [normalize_fig_id(r) for r in find_fig_refs(cleaned)]

    refs = _prose_refs(stem) + _prose_refs(answer)
    stem_refs = _prose_refs(stem)
    eg = (example_id or "").replace("例", "").replace(" ", "").strip()
    blob = f"{stem or ''}\n{answer or ''}"
    caption_owner: dict[str, str] = {}
    caption_text: dict[str, str] = {}
    for m in re.finditer(
        r"图\s*(\d+(?:\.\d+)*(?:\([a-z]\))?)\s*[^.\n]{0,40}?例\s*(\d+(?:\.\d+)+)",
        blob,
        flags=re.I,
    ):
        fid = normalize_fig_id("图" + m.group(1))
        caption_owner[fid] = m.group(2).replace(" ", "")
        caption_text[fid] = m.group(0)
    for m in re.finditer(
        r"\[(图\s*\d+(?:\.\d+)*(?:\([a-z]\))?)\]\s*([^\n]*)",
        blob,
    ):
        fid = normalize_fig_id(m.group(1))
        cap = (m.group(2) or "").strip()
        caption_text[fid] = cap
        om = re.search(r"例\s*(\d+(?:\.\d+)+)", cap)
        if om:
            caption_owner[fid] = om.group(1).replace(" ", "")

    section_prefix = ""
    parts = eg.split(".")
    if len(parts) >= 2:
        section_prefix = f"图{parts[0]}.{parts[1]}"

    def _in_section(fid: str) -> bool:
        if not section_prefix:
            return True
        nf = normalize_fig_id(fid)
        return nf == section_prefix or nf.startswith(section_prefix + ".") or nf.startswith(
            section_prefix + "("
        )

    def _caption_for(fid: str) -> str:
        nf = normalize_fig_id(fid)
        if nf in caption_text:
            return caption_text[nf]
        parent = re.sub(r"\([a-z]\)$", "", nf)
        if parent in caption_text:
            return caption_text[parent]
        # 父号查子图注：图5.3.12 → 图5.3.12(a)
        for k, v in caption_text.items():
            if k.startswith(nf + "(") or (
                parent != nf and k.startswith(parent + "(")
            ):
                return v
        return ""

    def _owned_by_this(fid: str) -> bool:
        nf = normalize_fig_id(fid)
        owner = caption_owner.get(nf) or caption_owner.get(re.sub(r"\([a-z]\)$", "", nf))
        if owner == eg:
            return True
        cap = _caption_for(fid)
        return bool(cap) and (eg in cap.replace(" ", "") or f"例{eg}" in cap.replace(" ", ""))

    has_section_fig = any(_in_section(f) for f, _ in pairs)
    named_owned_fids = {normalize_fig_id(f) for f, _ in pairs if _owned_by_this(f)}
    has_named_owned = bool(named_owned_fids)

    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for fid, url in pairs:
        if not url or url in seen:
            continue
        nf = normalize_fig_id(fid)
        owner = caption_owner.get(nf) or caption_owner.get(re.sub(r"\([a-z]\)$", "", nf))
        if owner and owner != eg:
            continue
        if refs and not any(fig_matches_ref(r, fid) for r in refs):
            continue
        if not refs:
            continue
        if has_section_fig and not _in_section(fid):
            if not any(fig_matches_ref(r, fid) for r in stem_refs):
                continue
        stem_hit = any(fig_matches_ref(r, fid) for r in stem_refs)
        owned_hit = _owned_by_this(fid)
        ref_hit = any(fig_matches_ref(r, fid) for r in refs)
        if not stem_hit and not owned_hit and not ref_hit:
            cap = _caption_for(fid)
            cap_n = cap.replace(" ", "")
            if len(stem_refs) == 1 and cap and eg not in cap_n:
                continue
            if has_named_owned:
                related = any(
                    re.sub(r"^图", "", of) in cap_n or of in cap_n
                    for of in named_owned_fids
                )
                if eg not in cap_n and not related:
                    continue
        # 正文点名的图：即便有「点名配图集合」也不因图注未写例号而丢掉
        elif not stem_hit and not owned_hit and ref_hit:
            pass
        seen.add(url)
        out.append((fid, url))
    return out


def strip_foreign_md_images(
    text: str,
    *,
    chapter_num: int,
    q_num: str,
    stem: str,
) -> str:
    """去掉解答/正文里他题 图P/A 的 markdown 图（除非题干已引用）。"""
    stem_refs = [normalize_fig_id(r) for r in find_fig_refs(stem)]

    def _sub(m: re.Match[str]) -> str:
        alt = normalize_fig_id((m.group(1) or "").replace(" ", ""))
        if not alt or alt == "图":
            # 空 alt：若无法判断归属则保留（可能是本题无标注图）
            return m.group(0)
        owner = foreign_exercise_owner(alt, chapter_num, q_num)
        if not owner:
            return m.group(0)
        if any(fig_matches_ref(r, alt) for r in stem_refs):
            return m.group(0)
        return ""

    cleaned = MD_IMG_RE.sub(_sub, text or "")
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def partition_stem_answer_figures(
    stem: str,
    answer: str,
    pairs: list[tuple[str, str]],
    *,
    chapter_num: int,
    q_num: str,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """把候选图拆到题干 / 答案：解答图(A*)优先答案，习题图(P*)优先题干；同 URL 不重复挂两侧。"""
    stem_refs = find_fig_refs(stem)
    ans_refs = find_fig_refs(answer)
    stem_out: list[tuple[str, str]] = []
    ans_out: list[tuple[str, str]] = []
    used_urls: set[str] = set()

    def _add(bucket: list[tuple[str, str]], fid: str, url: str) -> None:
        if url and url not in used_urls:
            used_urls.add(url)
            bucket.append((fid, url))

    # 1) 正文显式引用
    for ref in stem_refs:
        for fid, url in pairs:
            if fig_matches_ref(ref, fid):
                _add(stem_out, fid, url)
    for ref in ans_refs:
        for fid, url in pairs:
            if fig_matches_ref(ref, fid):
                _add(ans_out, fid, url)

    # 2) 归属：A* → 答案；P* 本题 → 题干（若题干提到如图/见图/图号）
    need_stem_owned = bool(
        re.search(rf"图\s*P?\s*{chapter_num}\.{q_num}", stem)
        or re.search(r"如图|见图", stem)
        or stem_refs
    )
    for fid, url in pairs:
        if fig_is_answer_sheet(fid, chapter_num, q_num):
            _add(ans_out, fid, url)
        elif need_stem_owned and fig_belongs_to_exercise(fid, chapter_num, q_num):
            _add(stem_out, fid, url)

    return stem_out, ans_out


def clean_canonical_answer(
    answer: str, *, chapter_num: int, q_num: str, stem: str
) -> str:
    """去掉串入的他题视觉图注；保留本题或题干已引用的图。"""
    stem_refs = {normalize_fig_id(x) for x in find_fig_refs(stem)}

    def _keep(m: re.Match[str]) -> str:
        body = m.group("body") or ""
        fid = normalize_fig_id("图" + body)
        if fig_belongs_to_exercise(fid, chapter_num, q_num):
            return m.group(0)
        for ref in stem_refs:
            if fig_matches_ref(ref, fid):
                return m.group(0)
        return ""

    cleaned = VISION_CAPTION_RE.sub(_keep, answer or "")
    # 识图残留：描述行、空配图标题（真图靠 markdown ![]()）
    cleaned = re.sub(r"(?m)^[ \t]*\[图[^\]]*描述\][^\n]*\n?", "", cleaned)
    cleaned = re.sub(r"(?m)^[ \t]*\*\*配图\*\*[ \t]*\n?", "", cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def zip_figures(
    figure_ids: list[str], media_urls: list[str], media_base: str
) -> list[tuple[str, str]]:
    fids = [normalize_fig_id(f) for f in figure_ids if f]
    urls = rewrite_media_urls(media_urls, media_base)
    pairs: list[tuple[str, str]] = []
    if fids and urls and len(fids) == len(urls):
        return list(zip(fids, urls))
    n = max(len(fids), len(urls))
    for i in range(n):
        fid = fids[i] if i < len(fids) else f"图(附{i + 1})"
        url = urls[i] if i < len(urls) else ""
        if url:
            pairs.append((fid, url))
    return pairs


def load_global_figure_catalog(media_base: str) -> dict[str, str]:
    """扫描全部 canonical chunk，建立 图号 → 公网 URL（后写覆盖前写）。"""
    catalog: dict[str, str] = {}
    for n in range(1, 9):
        path = CANONICAL / f"ch{n:02d}" / "chunks.jsonl"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            pairs = zip_figures(
                list(obj.get("figure_ids") or []),
                list(obj.get("media_urls") or []),
                media_base,
            )
            for fid, url in pairs:
                catalog[fid] = url
                parent = re.sub(r"\([a-z]\)$", "", fid)
                # 仅当父号尚未占用时写入，避免 (a) 抢占父图
                if parent != fid and parent not in catalog:
                    catalog[parent] = url
    return catalog


def merge_figure_pairs(
    local: list[tuple[str, str]], catalog: dict[str, str], refs: list[str]
) -> list[tuple[str, str]]:
    """本地 chunk 图 + 全局目录补齐题干/解答引用。"""
    by_id = {fid: url for fid, url in local}
    for ref in refs:
        r = normalize_fig_id(ref)
        if r in by_id:
            continue
        # 精确或子图
        if r in catalog:
            by_id[r] = catalog[r]
            continue
        for fid, url in catalog.items():
            if fig_matches_ref(r, fid):
                by_id[fid] = url
    return list(by_id.items())

def fig_matches_ref(ref: str, fid: str) -> bool:
    """精确对齐图号，避免 图8.6.17 误匹配 图8.6.1。"""
    r = normalize_fig_id(ref)
    f = normalize_fig_id(fid)
    if not r or not f:
        return False
    if f == r:
        return True

    def _prefix_ok(short: str, long: str) -> bool:
        if not long.startswith(short):
            return False
        if len(long) == len(short):
            return True
        return long[len(short)] in ".("

    return _prefix_ok(r, f) or _prefix_ok(f, r)


def select_figures_for_text(
    text: str,
    pairs: list[tuple[str, str]],
    *,
    chapter_num: int,
    q_num: str,
    include_owned: bool,
) -> list[tuple[str, str]]:
    refs = find_fig_refs(text)
    chosen: list[tuple[str, str]] = []
    seen_url: set[str] = set()

    def _add(fid: str, url: str) -> None:
        if url and url not in seen_url:
            seen_url.add(url)
            chosen.append((fid, url))

    for ref in refs:
        for fid, url in pairs:
            if fig_matches_ref(ref, fid):
                _add(fid, url)

    if include_owned:
        for fid, url in pairs:
            if fig_belongs_to_exercise(fid, chapter_num, q_num):
                _add(fid, url)

    return chosen


def append_media_markdown(text: str, figures: list[tuple[str, str]]) -> str:
    body = (text or "").rstrip()
    # 已有相同 URL 则不重复
    existing = set(MD_IMG_RE.findall(body))
    existing_urls = {u for _, u in existing}
    extra: list[str] = []
    for fid, url in figures:
        if url in existing_urls:
            continue
        extra.append(f"![{fid}]({url})")
        existing_urls.add(url)
    if not extra:
        return body
    # 若正文已有图引用但无 markdown 图，在文末加配图区
    block = "\n\n".join(extra)
    if find_fig_refs(body) or "如图" in body or "见图" in body:
        return f"{body}\n\n**配图**\n\n{block}"
    return f"{body}\n\n{block}" if body else block


def parse_exercise_chunk(
    chunk: dict[str, Any],
    *,
    media_base: str,
    guide_answer: Optional[str],
    figure_catalog: Optional[dict[str, str]] = None,
    guide_figs: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    eid = chunk.get("exercise_id") or ""
    m = EXERCISE_ID_RE.match(eid)
    if not m:
        raise ValueError(f"无法解析 exercise_id: {eid}")
    chapter_num = int(chunk.get("chapter_num") or m.group(1))
    q_num = m.group(2)
    text = chunk.get("text_content") or ""
    sm = STEM_ANS_RE.search(text)
    if not sm:
        # 宽松回退
        loose = re.search(
            r"【题\s*[\d.]+\s*题干】(.*?)【题\s*[\d.]+\s*解答】(.*)", text, re.S
        )
        if not loose:
            raise ValueError("缺少【题干】/【解答】标记")
        stem, cans = loose.group(1).strip(), loose.group(2).strip()
    else:
        stem, cans = sm.group("stem").strip(), sm.group("answer").strip()

    # 去掉 breadcrumb 行（若题干前误带）
    stem = re.sub(
        r"^第\d+章[^\n]*\n+",
        "",
        stem,
    ).strip()
    before_bleed = stem
    stem = strip_orphan_foreign_fig_captions(
        stem, chapter_num=chapter_num, q_num=q_num
    )
    cans = strip_orphan_foreign_fig_captions(
        cans, chapter_num=chapter_num, q_num=q_num
    )

    patches: list[str] = []
    if stem != before_bleed:
        patches.append("stripped_orphan_foreign_fig_captions")
    if guide_answer and guide_answer.strip():
        answer = rewrite_md_images(
            guide_answer.strip(), media_base, default_kind="guide"
        )
        patches.append("answer_from_guide_md")
    else:
        answer = clean_canonical_answer(
            cans, chapter_num=chapter_num, q_num=q_num, stem=stem
        )
        answer = rewrite_md_images(answer, media_base, default_kind="guide")
        if answer != cans.strip():
            patches.append("stripped_foreign_vision_captions")
        patches.append("guide_md_missing_fallback_canonical")

    stem = rewrite_md_images(stem, media_base, default_kind="chapters")

    local_pairs = zip_figures(
        list(chunk.get("figure_ids") or []),
        list(chunk.get("media_urls") or []),
        media_base,
    )
    catalog = figure_catalog or {}
    refs = find_fig_refs(stem) + find_fig_refs(answer)
    pairs = merge_figure_pairs(local_pairs, catalog, refs)
    pairs = sanitize_pairs_for_exercise(
        pairs, chapter_num=chapter_num, q_num=q_num, stem=stem, answer=answer
    )
    if catalog and any(r not in {p[0] for p in local_pairs} for r in refs):
        # 题干/解答引用了 chunk 外章内图
        if any(
            normalize_fig_id(r) in catalog
            or any(fig_matches_ref(r, f) for f in catalog)
            for r in refs
            if normalize_fig_id(r) not in {p[0] for p in local_pairs}
        ):
            patches.append("figures_from_global_catalog")

    stem_figs, ans_figs = partition_stem_answer_figures(
        stem, answer, pairs, chapter_num=chapter_num, q_num=q_num
    )
    if stem_figs or ans_figs:
        patches.append("figures_partitioned_stem_answer")

    content = append_media_markdown(stem, stem_figs)
    answer = append_media_markdown(answer, ans_figs)
    before_guide_fig = answer
    answer = enrich_answer_with_guide_figures(
        answer,
        chapter_num=chapter_num,
        q_num=q_num,
        guide_figs=guide_figs or {},
    )
    if answer != before_guide_fig:
        patches.append("guide_labeled_figures_attached")

    before_md = answer + "\n" + content
    answer = strip_foreign_md_images(
        answer, chapter_num=chapter_num, q_num=q_num, stem=stem
    )
    content = strip_foreign_md_images(
        content, chapter_num=chapter_num, q_num=q_num, stem=stem
    )
    content = strip_bare_and_empty_alt_images(content)
    answer = strip_bare_and_empty_alt_images(answer)
    content, answer = _dedupe_md_images_across(content, answer)
    content, answer = prefer_guide_media_for_owned(
        content, answer, chapter_num=chapter_num, q_num=q_num
    )
    if answer + "\n" + content != before_md:
        patches.append("stripped_foreign_or_bare_md_images")

    # 最终清残留本地路径
    if LOCAL_PATH_RE.search(content) or LOCAL_PATH_RE.search(answer):
        content = strip_local_paths(content)
        answer = strip_local_paths(answer)
        patches.append("stripped_local_paths")

    image_urls = sorted(
        {u for _, u in MD_IMG_RE.findall(content + "\n" + answer) if u.startswith("http")}
    )
    return {
        "exercise_id": eid,
        "problem_id": eid,
        "kind": "chapter_exercise",
        "chunk_id": chunk.get("chunk_id") or "",
        "chapter_num": chapter_num,
        "q_num": q_num,
        "content": content.strip(),
        "answer": answer.strip(),
        "analysis": None,
        "image_urls": image_urls,
        "patches": patches,
        "source": f"{SOURCE_PREFIX}第{chapter_num}章·{eid}",
    }


def _attach_figures(
    stem: str,
    answer: str,
    chunk: dict[str, Any],
    *,
    media_base: str,
    figure_catalog: Optional[dict[str, str]],
    chapter_num: int,
    q_num: str,
    patches: list[str],
    owned_figs: bool,
    example_id: Optional[str] = None,
) -> tuple[str, str, list[str]]:
    local_pairs = zip_figures(
        list(chunk.get("figure_ids") or []),
        list(chunk.get("media_urls") or []),
        media_base,
    )
    catalog = figure_catalog or {}
    refs = find_fig_refs(stem) + find_fig_refs(answer)
    pairs = merge_figure_pairs(local_pairs, catalog, refs)
    if example_id:
        pairs = sanitize_pairs_for_example(
            pairs, example_id=example_id, stem=stem, answer=answer
        )
    if catalog and any(
        normalize_fig_id(r) not in {p[0] for p in local_pairs} for r in refs
    ):
        if any(
            normalize_fig_id(r) in catalog
            or any(fig_matches_ref(r, f) for f in catalog)
            for r in refs
            if normalize_fig_id(r) not in {p[0] for p in local_pairs}
        ):
            patches.append("figures_from_global_catalog")

    def _forced(text: str) -> list[tuple[str, str]]:
        out: list[tuple[str, str]] = []
        seen: set[str] = set()
        for ref in find_fig_refs(text):
            for fid, url in pairs:
                if fig_matches_ref(ref, fid) and url not in seen:
                    seen.add(url)
                    out.append((fid, url))
        return out

    stem_figs = select_figures_for_text(
        stem, pairs, chapter_num=chapter_num, q_num=q_num, include_owned=False
    )
    if not stem_figs and (
        re.search(rf"图\s*P?\s*{chapter_num}\.{q_num}", stem)
        or re.search(r"如图|见图", stem)
        or find_fig_refs(stem)
    ):
        stem_figs = _forced(stem)
        if owned_figs and not stem_figs:
            stem_figs = select_figures_for_text(
                stem, pairs, chapter_num=chapter_num, q_num=q_num, include_owned=True
            )

    ans_figs = select_figures_for_text(
        answer, pairs, chapter_num=chapter_num, q_num=q_num, include_owned=owned_figs
    )
    if not ans_figs and find_fig_refs(answer):
        ans_figs = _forced(answer)
    # 例题：仅把「正文已引用且尚在 pairs」的本地图补到解答，禁止整包倾倒
    if example_id and not owned_figs:
        used = {u for _, u in stem_figs + ans_figs}
        for fid, url in pairs:
            if url in used:
                continue
            if any(fig_matches_ref(r, fid) for r in refs):
                ans_figs.append((fid, url))
                used.add(url)

    content = append_media_markdown(stem, stem_figs)
    answer_out = append_media_markdown(answer, ans_figs)
    content = strip_bare_and_empty_alt_images(content)
    answer_out = strip_bare_and_empty_alt_images(answer_out)
    if example_id:
        content = strip_foreign_example_captions(content, example_id=example_id)
        answer_out = strip_foreign_example_captions(answer_out, example_id=example_id)
        # 去重：同一 URL 只保留首次
        content, answer_out = _dedupe_md_images_across(content, answer_out)
    if LOCAL_PATH_RE.search(content) or LOCAL_PATH_RE.search(answer_out):
        content = strip_local_paths(content)
        answer_out = strip_local_paths(answer_out)
        patches.append("stripped_local_paths")
    image_urls = sorted(
        {
            u
            for _, u in MD_IMG_RE.findall(content + "\n" + answer_out)
            if u.startswith("http")
        }
    )
    return content.strip(), answer_out.strip(), image_urls


def _dedupe_md_images_across(stem: str, answer: str) -> tuple[str, str]:
    """题干已出现的 URL 从解答中去掉；同 alt 只保留一张（优先 guide）。"""

    def _dedupe_by_alt(text: str) -> str:
        best: dict[str, tuple[str, str, bool]] = {}  # alt -> (full, url, is_guide)
        order: list[str] = []
        for m in MD_IMG_RE.finditer(text or ""):
            alt = normalize_fig_id((m.group(1) or "").replace(" ", "")) or f"__empty_{m.start()}"
            # 归一：图A7.1(a) 与 图A7.1 若仅一张则后面合并时再处理
            url = m.group(2).strip()
            is_guide = "/guide/" in url
            key = re.sub(r"\([a-z]\)$", "", alt) if alt.startswith("图") else alt
            # 子图各自独立键
            key = alt if "(" in alt else key
            prev = best.get(key)
            if prev is None:
                best[key] = (m.group(0), url, is_guide)
                order.append(key)
            elif is_guide and not prev[2]:
                best[key] = (m.group(0), url, is_guide)
        # 重建：去掉全部 md 图后按 order 追加？会打乱位置。改为替换重复为删除。
        seen: set[str] = set()
        keep_urls = {best[k][1] for k in order}

        def _sub(m: re.Match[str]) -> str:
            alt = normalize_fig_id((m.group(1) or "").replace(" ", ""))
            url = m.group(2).strip()
            key = alt if "(" in alt else (re.sub(r"\([a-z]\)$", "", alt) if alt.startswith("图") else alt)
            if not alt:
                key = url
            wanted = best.get(key) or best.get(alt)
            if wanted and url == wanted[1]:
                if url in seen:
                    return ""
                seen.add(url)
                return m.group(0)
            if wanted and url != wanted[1]:
                return ""  # 同键非优选
            if url in keep_urls:
                if url in seen:
                    return ""
                seen.add(url)
                return m.group(0)
            return m.group(0)

        return re.sub(r"\n{3,}", "\n\n", MD_IMG_RE.sub(_sub, text or "")).strip()

    stem_d = _dedupe_by_alt(stem)
    stem_urls = {u for _, u in MD_IMG_RE.findall(stem_d)}

    def _sub_ans(m: re.Match[str]) -> str:
        if m.group(2).strip() in stem_urls:
            return ""
        return m.group(0)

    ans = MD_IMG_RE.sub(_sub_ans, answer or "")
    ans = _dedupe_by_alt(ans)
    return stem_d, re.sub(r"\n{3,}", "\n\n", ans).strip()


def parse_example_chunk(
    chunk: dict[str, Any],
    *,
    media_base: str,
    figure_catalog: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """课文例题：【例 x.y.z】题干 + 解：…"""
    eid = (chunk.get("example_id") or "").strip()
    m = EXAMPLE_ID_RE.match(eid)
    if not m:
        raise ValueError(f"无法解析 example_id: {eid}")
    chapter_num = int(chunk.get("chapter_num") or m.group(1).split(".")[0])
    q_num = m.group(1)  # 如 1.4.1 / 2.5.6
    text = BREADCRUMB_RE.sub("", (chunk.get("text_content") or "").lstrip(), count=1).strip()

    head = EXAMPLE_HEAD_RE.search(text)
    if not head:
        raise ValueError("缺少【例 …】标记")
    body = (head.group("body") or "").strip()
    patches: list[str] = ["answer_from_canonical_example"]

    sol = EXAMPLE_SOL_RE.split(body, maxsplit=1)
    if len(sol) == 2 and sol[0].strip() and sol[1].strip():
        stem, cans = sol[0].strip(), "解：" + sol[1].strip()
    else:
        # 无独立「解：」行（含解写在公式里 / 代码例题）：首段作题干，其余作解答
        paras = re.split(r"\n\s*\n", body, maxsplit=1)
        if len(paras) == 2 and paras[0].strip() and paras[1].strip():
            stem, cans = paras[0].strip(), paras[1].strip()
            patches.append("example_split_by_paragraph")
        else:
            lines = body.splitlines()
            stem = (lines[0] if lines else body).strip()
            cans = body.strip()
            patches.append("example_stem_first_line_answer_full")

    stem = f"【例 {q_num}】{stem}" if not stem.startswith("【例") else stem
    before_eg = stem + "\n" + cans
    stem = strip_foreign_example_captions(stem, example_id=eid)
    cans = strip_foreign_example_captions(cans, example_id=eid)
    if stem + "\n" + cans != before_eg:
        patches.append("stripped_foreign_example_captions")
    answer = rewrite_md_images(cans, media_base, default_kind="chapters")
    stem = rewrite_md_images(stem, media_base, default_kind="chapters")

    content, answer, image_urls = _attach_figures(
        stem,
        answer,
        chunk,
        media_base=media_base,
        figure_catalog=figure_catalog,
        chapter_num=chapter_num,
        q_num=q_num.split(".")[-1],
        patches=patches,
        owned_figs=False,
        example_id=eid,
    )
    return {
        "exercise_id": eid,  # 兼容旧字段：例题也写入同一键便于检索
        "example_id": eid,
        "problem_id": eid,
        "kind": "example",
        "chunk_id": chunk.get("chunk_id") or "",
        "chapter_num": chapter_num,
        "q_num": q_num,
        "content": content,
        "answer": answer,
        "analysis": None,
        "image_urls": image_urls,
        "patches": patches,
        "source": f"{SOURCE_PREFIX}第{chapter_num}章·{eid}",
    }


# ---------------------------------------------------------------------------
# Validation / load
# ---------------------------------------------------------------------------


def validate_item(item: dict[str, Any], tests: list[dict[str, str]]) -> list[str]:
    errs: list[str] = []
    if not (item.get("content") or "").strip():
        errs.append("empty_content")
    if not (item.get("answer") or "").strip():
        errs.append("empty_answer")
    blob = (item.get("content") or "") + "\n" + (item.get("answer") or "")
    if LOCAL_PATH_RE.search(blob):
        errs.append("local_path_residual")
    for _, url in MD_IMG_RE.findall(blob):
        key = local_path_to_object_key(url) if not url.startswith("http") else ""
        if url.startswith("http"):
            # 可解析出 chapters|guide/hash
            if not re.search(r"/(?:chapters|guide)/[^/\s)]+\.(?:jpg|jpeg|png|gif|webp)(?:\?|$)", url, re.I):
                # 也接受 /media/chapters/...
                if not re.search(r"/(?:media/)?(?:chapters|guide)/", url, re.I):
                    errs.append(f"bad_image_url:{url[:80]}")
        elif not key:
            errs.append(f"unresolvable_image:{url[:80]}")
    if not tests:
        errs.append("needs_kg_review")
    return errs


def load_canonical_chunks(
    chapters: Optional[list[int]],
    *,
    kinds: Optional[set[str]] = None,
) -> list[dict[str, Any]]:
    """kinds: {'exercise','example'} → exercise_merged / example。"""
    want = kinds or {"exercise", "example"}
    type_map = {
        "exercise": "exercise_merged",
        "example": "example",
    }
    allow_bt = {type_map[k] for k in want if k in type_map}
    nums = chapters or list(range(1, 9))
    out: list[dict[str, Any]] = []
    for n in nums:
        path = CANONICAL / f"ch{n:02d}" / "chunks.jsonl"
        if not path.exists():
            print(f"[skip] 缺少 {path}")
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("block_type") in allow_bt:
                out.append(obj)
    return out


def knowledge_tags_payload(
    *,
    problem_id: str,
    chunk_id: str,
    tests: list[dict[str, str]],
    needs_kg_review: bool,
    kind: str,
) -> dict[str, Any]:
    tags: dict[str, Any] = {
        "tags": [t["name"] for t in tests if t.get("name")],
        "concept_ids": [t["concept_id"] for t in tests if t.get("concept_id")],
        "problem_id": problem_id,
        "chunk_id": chunk_id,
        "kg_tests_count": len(tests),
        "kind": kind,
    }
    if kind == "example":
        tags["example_id"] = problem_id
        tags["exercise_id"] = problem_id  # 兼容按 exercise_id 查询
    else:
        tags["exercise_id"] = problem_id
    if needs_kg_review:
        tags["needs_kg_review"] = True
    return tags


# ---------------------------------------------------------------------------
# DB / Chroma
# ---------------------------------------------------------------------------


def _find_existing(db: Any, problem_id: str, source: str) -> Any:
    from app.db.models import QuestionBank

    rows = (
        db.query(QuestionBank)
        .filter(QuestionBank.source == source)
        .all()
    )
    if rows:
        return rows[0]
    for row in db.query(QuestionBank).filter(QuestionBank.source.like(f"{SOURCE_PREFIX}%")):
        tags = row.knowledge_tags or {}
        if not isinstance(tags, dict):
            continue
        if tags.get("exercise_id") == problem_id or tags.get("example_id") == problem_id or tags.get("problem_id") == problem_id:
            return row
    return None


def recreate_chroma_question_bank() -> None:
    """删除并重建 question_bank 集合（避免 mock/真模型维度不一致）。"""
    import chromadb

    import app.services.chromadb_client as chroma_mod
    from app.config import get_settings

    settings = get_settings()
    persist = Path(settings.chroma_persist_dir)
    persist.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist))
    name = settings.chroma_collection_questions
    try:
        client.delete_collection(name)
        print(f"已删除 Chroma 集合 {name}（将按当前 Embedding 维度重建）")
    except Exception:  # noqa: BLE001
        pass
    chroma_mod._store = None


def resync_all_active_questions(db: Any) -> int:
    from app.db.models import QuestionBank
    from app.services.question_bank import sync_question_to_chroma

    rows = db.query(QuestionBank).filter(QuestionBank.status == "active").all()
    for i, row in enumerate(rows, 1):
        sync_question_to_chroma(row)
        if i % 50 == 0 or i == len(rows):
            print(f"  chroma resync {i}/{len(rows)}")
    return len(rows)


def reset_textbook_questions(db: Any) -> int:
    from app.db.models import QuestionBank

    rows = (
        db.query(QuestionBank)
        .filter(QuestionBank.source.like(f"{SOURCE_PREFIX}%"))
        .all()
    )
    n = len(rows)
    for r in rows:
        db.delete(r)
    db.commit()
    return n


def upsert_question(db: Any, item: dict[str, Any], tags: dict[str, Any], *, sync: bool) -> int:
    from app.db.models import QuestionBank
    from app.services.question_bank import sync_question_to_chroma

    pid = item.get("problem_id") or item.get("exercise_id") or ""
    row = _find_existing(db, pid, item["source"])
    if row is None:
        row = QuestionBank(
            content=item["content"],
            answer=item["answer"],
            analysis=item.get("analysis"),
            knowledge_tags=tags,
            source=item["source"],
            status="active",
        )
        db.add(row)
        db.flush()
    else:
        row.content = item["content"]
        row.answer = item["answer"]
        row.analysis = item.get("analysis")
        row.knowledge_tags = tags
        row.source = item["source"]
        row.status = "active"
        db.flush()
    if sync:
        sync_question_to_chroma(row)
    return int(row.id)


# ---------------------------------------------------------------------------
# Reports / acceptance
# ---------------------------------------------------------------------------


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_acceptance_pack(
    db: Any,
    *,
    seed: int = ACCEPTANCE_SEED,
    out_prefix: Path,
) -> dict[str, Any]:
    from app.db.models import QuestionBank

    rows = (
        db.query(QuestionBank)
        .filter(
            QuestionBank.source.like(f"{SOURCE_PREFIX}%"),
            QuestionBank.status == "active",
        )
        .all()
    )
    if len(rows) < 10:
        raise RuntimeError(f"课本题不足 10 道（当前 {len(rows)}），无法抽样验收")

    rng = random.Random(seed)
    sample = rng.sample(rows, 10)

    items: list[dict[str, Any]] = []
    for row in sample:
        tags = row.knowledge_tags if isinstance(row.knowledge_tags, dict) else {}
        eid = tags.get("exercise_id") or ""
        m = EXERCISE_ID_RE.match(str(eid))
        ch = int(m.group(1)) if m else 0
        ch_md = _chapter_md_path(ch)
        g_md = _guide_md_path(ch)
        imgs = sorted({u for _, u in MD_IMG_RE.findall((row.content or "") + "\n" + (row.answer or ""))})
        items.append(
            {
                "exercise_id": eid,
                "db_id": row.id,
                "source": row.source,
                "chapter_num": ch,
                "content": row.content,
                "answer": row.answer,
                "image_urls": imgs,
                "knowledge_tags": tags,
                "textbook_locator": {
                    "chapter_md": str(ch_md.relative_to(REPO)).replace("\\", "/") if ch_md else "",
                    "exercise_marker": f"[题 {m.group(1)}.{m.group(2)}]" if m else "",
                    "guide_md": str(g_md.relative_to(REPO)).replace("\\", "/") if g_md else "",
                    "guide_marker": f"【题 {m.group(1)}.{m.group(2)}】" if m else "",
                },
            }
        )

    md_lines = [
        "# 课本题库人工验收包（抽样 10 题）",
        "",
        f"- 抽样种子：`seed={seed}`（无放回）",
        f"- 生成时间：{datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"- 抽样数：{len(items)} / 库内课本题 active 总数以报告为准",
        "",
        "## 验收说明",
        "",
        "请对照课本正文「习题」与学习辅导「习题解答」填写下表。",
        "",
        "硬错误：缺图导致无法解题、答案结论错、题号错乱、图谱完全跑题。",
        "10 题中任一类硬错误 ≥ 2 题 → 不通过。",
        "",
        "## 空白验收表",
        "",
        "| # | 题号 | 题干完整(Y/N) | 配图齐全(Y/N) | 答案正确(Y/N) | 图谱合理(Y/N) | 备注 |",
        "|---|------|---------------|---------------|---------------|---------------|------|",
    ]
    for i, it in enumerate(items, 1):
        md_lines.append(f"| {i} | {it['exercise_id']} |  |  |  |  |  |")

    md_lines += ["", "---", ""]

    for i, it in enumerate(items, 1):
        tags = it["knowledge_tags"]
        loc = it["textbook_locator"]
        md_lines += [
            f"## {i}. {it['exercise_id']}",
            "",
            f"- DB id：`{it['db_id']}`",
            f"- source：`{it['source']}`",
            f"- 章：第 {it['chapter_num']} 章",
            f"- 课本对照：`{loc['chapter_md']}` → `{loc['exercise_marker']}`",
            f"- 解答对照：`{loc['guide_md']}` → `{loc['guide_marker']}`",
            f"- 图谱概念：{', '.join(tags.get('tags') or []) or '（无）'}",
            f"- concept_ids：{', '.join(tags.get('concept_ids') or []) or '（无）'}",
            f"- TESTS 条数：{tags.get('kg_tests_count', 0)}",
            "",
            "### 题干",
            "",
            it["content"] or "（空）",
            "",
            "### 答案",
            "",
            it["answer"] or "（空）",
            "",
            "### 配图 URL",
            "",
        ]
        if it["image_urls"]:
            for u in it["image_urls"]:
                md_lines.append(f"- {u}")
        else:
            md_lines.append("- （本题无配图 URL）")
        md_lines += ["", "---", ""]

    md_path = Path(str(out_prefix) + ".md")
    json_path = Path(str(out_prefix) + ".json")
    html_path = Path(str(out_prefix) + ".html")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    write_json(json_path, {"seed": seed, "count": len(items), "items": items})
    html_path.write_text(render_acceptance_html(items, seed=seed), encoding="utf-8")
    return {"md": str(md_path), "json": str(json_path), "html": str(html_path), "items": items}


def _resolve_media_file(url_or_path: str) -> Optional[Path]:
    """http(s)/media URL 或相对路径 → 本地图片文件。"""
    raw = (url_or_path or "").strip()
    if not raw:
        return None
    name = Path(raw.replace("\\", "/")).name
    if not name:
        return None
    kind = "guide" if ("/guide/" in raw.replace("\\", "/") or "学习辅导" in raw) else "chapters"
    m = re.search(r"/(chapters|guide)/([^/?#]+)$", raw.replace("\\", "/"))
    if m:
        kind, name = m.group(1), m.group(2)
    base = REPO / "课本" / "课本加习题册" / "markdown_云端解析"
    candidates = [
        base / ("学习辅导按章节拆分" if kind == "guide" else "按章节拆分") / "images" / name,
        base / "按章节拆分" / "images" / name,
        base / "学习辅导按章节拆分" / "images" / name,
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def _media_to_src(url: str) -> str:
    """优先 data URI 内嵌，保证验收 HTML 离线也能看图；否则保留原 URL。"""
    import base64
    import mimetypes

    path = _resolve_media_file(url)
    if path is None:
        return url
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def render_acceptance_html(items: list[dict[str, Any]], *, seed: int) -> str:
    def esc(s: str) -> str:
        return (
            (s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def rich_text_to_html(text: str) -> str:
        """Markdown 图 + LaTeX（$ / $$）保留给 KaTeX；换行转段落。"""
        raw = text or ""
        slots: list[str] = []

        def _park(html: str) -> str:
            slots.append(html)
            return f"\x00SLOT{len(slots) - 1}\x00"

        # 1) markdown 图片 → figure（内嵌 data URI）
        def _img(m: re.Match[str]) -> str:
            alt = esc(m.group(1) or "配图")
            src = _media_to_src(m.group(2).strip())
            # data URI 很大，src 不转义引号问题：base64 无双引号
            return _park(
                f'<figure class="fig"><img src="{src}" alt="{alt}" loading="lazy"/>'
                f"<figcaption>{alt}</figcaption></figure>"
            )

        raw = MD_IMG_RE.sub(_img, raw)

        # 2) 展示公式 $$...$$
        def _display(m: re.Match[str]) -> str:
            body = m.group(1).strip()
            # KaTeX 需要原始 TeX；仅转义 HTML 特殊符
            return _park(f'<div class="math-block">\\[{esc(body)}\\]</div>')

        raw = re.sub(r"\$\$(.+?)\$\$", _display, raw, flags=re.S)

        # 3) 行内公式 $...$（避免单独的 \$）
        def _inline(m: re.Match[str]) -> str:
            body = m.group(1)
            if not body.strip():
                return m.group(0)
            return _park(f'\\({esc(body)}\\)')

        raw = re.sub(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", _inline, raw, flags=re.S)

        # 4) 简单 HTML 表格原样保留（canonical 里偶有 <table>）
        def _table(m: re.Match[str]) -> str:
            return _park(m.group(0))

        raw = re.sub(r"(?is)<table\b.*?</table>", _table, raw)

        # 5) 其余转义 + 段落（块级 figure/math/table 不再包进 <p>）
        t = esc(raw)
        for i, html in enumerate(slots):
            t = t.replace(f"\x00SLOT{i}\x00", html)
        parts = re.split(r"\n\s*\n", t)
        blocks: list[str] = []
        for p in parts:
            p = p.strip()
            if not p:
                continue
            # 整段已是块级 HTML
            if re.fullmatch(
                r"(?:<(?:figure|div|table)\b.*</(?:figure|div|table)>\s*)+",
                p,
                flags=re.S | re.I,
            ):
                blocks.append(p)
                continue
            # 段内混排：块级前后拆开
            pieces = re.split(
                r"(<(?:figure|div|table)\b.*?</(?:figure|div|table)>)",
                p,
                flags=re.S | re.I,
            )
            buf: list[str] = []
            for piece in pieces:
                if not piece or not piece.strip():
                    continue
                if re.match(r"<(?:figure|div|table)\b", piece, flags=re.I):
                    if buf:
                        blocks.append("<p>" + "".join(buf).replace("\n", "<br>\n") + "</p>")
                        buf = []
                    blocks.append(piece)
                else:
                    buf.append(piece)
            if buf:
                blocks.append("<p>" + "".join(buf).replace("\n", "<br>\n") + "</p>")
        return "\n".join(blocks) if blocks else "<p>（空）</p>"

    def image_gallery(urls: list[str]) -> str:
        if not urls:
            return '<p class="muted">（本题无配图）</p>'
        parts = ['<div class="gallery">']
        for u in urls:
            src = _media_to_src(u)
            parts.append(
                f'<figure class="fig"><img src="{src}" alt="配图" loading="lazy"/>'
                f'<figcaption><a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a></figcaption></figure>'
            )
        parts.append("</div>")
        return "\n".join(parts)

    rows_table = []
    for i, it in enumerate(items, 1):
        rows_table.append(
            f"<tr><td>{i}</td><td>{esc(it['exercise_id'])}</td>"
            f"<td></td><td></td><td></td><td></td><td></td></tr>"
        )

    sections = []
    for i, it in enumerate(items, 1):
        tags = it["knowledge_tags"]
        loc = it["textbook_locator"]
        sections.append(
            f"""
<section class="card" id="q{i}">
  <h2>{i}. {esc(it['exercise_id'])}</h2>
  <ul class="meta">
    <li>DB id：<code>{it['db_id']}</code></li>
    <li>source：<code>{esc(it['source'] or '')}</code></li>
    <li>章：第 {it['chapter_num']} 章</li>
    <li>课本对照：<code>{esc(loc['chapter_md'])}</code> → <code>{esc(loc['exercise_marker'])}</code></li>
    <li>解答对照：<code>{esc(loc['guide_md'])}</code> → <code>{esc(loc['guide_marker'])}</code></li>
    <li>图谱：{esc(', '.join(tags.get('tags') or []) or '（无）')}</li>
    <li>concept_ids：<code>{esc(', '.join(tags.get('concept_ids') or []))}</code></li>
    <li>TESTS：{tags.get('kg_tests_count', 0)}</li>
  </ul>
  <h3>题干</h3>
  <div class="body">{rich_text_to_html(it['content'] or '')}</div>
  <h3>答案</h3>
  <div class="body">{rich_text_to_html(it['answer'] or '')}</div>
  <h3>配图</h3>
  {image_gallery(it.get('image_urls') or [])}
</section>
"""
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>课本题库人工验收包（seed={seed}）</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
  onload="renderMathInElement(document.body, {{
    delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '\\\\[', right: '\\\\]', display: true}},
      {{left: '$', right: '$', display: false}},
      {{left: '\\\\(', right: '\\\\)', display: false}}
    ],
    throwOnError: false
  }});"></script>
<style>
:root {{
  --bg: #f6f3ee;
  --ink: #1c1917;
  --muted: #57534e;
  --line: #d6d3d1;
  --card: #fffdf9;
  --accent: #0f766e;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; font-family: "Source Han Sans SC", "Noto Sans SC", "Segoe UI", sans-serif;
  background: linear-gradient(180deg, #e7e5e4 0%, var(--bg) 240px);
  color: var(--ink); line-height: 1.65;
}}
main {{ max-width: 920px; margin: 0 auto; padding: 32px 20px 80px; }}
h1 {{ font-size: 1.75rem; margin: 0 0 8px; letter-spacing: 0.02em; }}
.sub, .muted {{ color: var(--muted); margin-bottom: 24px; }}
.card {{
  background: var(--card); border: 1px solid var(--line);
  border-radius: 12px; padding: 20px 22px; margin: 20px 0;
}}
.meta {{ padding-left: 1.1em; color: var(--muted); font-size: 0.95rem; }}
.body {{
  background: #fafaf9; border-left: 3px solid var(--accent);
  padding: 12px 14px; border-radius: 0 8px 8px 0; overflow-x: auto;
}}
.body p {{ margin: 0.55em 0; }}
.math-block {{ margin: 0.85em 0; overflow-x: auto; text-align: center; }}
.fig {{ margin: 12px 0; }}
.fig img {{ max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 6px; background: #fff; }}
.fig figcaption {{ font-size: 0.85rem; color: var(--muted); word-break: break-all; }}
.gallery {{ display: grid; gap: 12px; }}
table {{ width: 100%; border-collapse: collapse; background: var(--card); }}
.body table {{ width: auto; margin: 8px 0; }}
th, td {{ border: 1px solid var(--line); padding: 8px 10px; text-align: left; font-size: 0.92rem; }}
th {{ background: #f5f5f4; }}
a {{ color: var(--accent); }}
code {{ font-size: 0.88em; }}
.toc a {{ margin-right: 10px; }}
</style>
</head>
<body>
<main>
  <h1>课本题库人工验收包</h1>
  <p class="sub">抽样种子 seed={seed} · 共 {len(items)} 题 · 公式由 KaTeX 渲染，配图已内嵌（无需后端）</p>
  <div class="card">
    <h2>空白验收表</h2>
    <table>
      <thead>
        <tr>
          <th>#</th><th>题号</th><th>题干完整(Y/N)</th><th>配图齐全(Y/N)</th>
          <th>答案正确(Y/N)</th><th>图谱合理(Y/N)</th><th>备注</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows_table)}
      </tbody>
    </table>
  </div>
  <p class="toc">快速跳转：{' '.join(f'<a href="#q{i}">{esc(it["exercise_id"])}</a>' for i, it in enumerate(items, 1))}</p>
  {''.join(sections)}
</main>
</body>
</html>
"""


def regenerate_acceptance_html_from_json(
    json_path: Path, *, html_path: Optional[Path] = None
) -> Path:
    """仅从已有验收 JSON 重渲 HTML（改样式/渲染时用）。"""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    items = data.get("items") or []
    seed = int(data.get("seed") or ACCEPTANCE_SEED)
    out = html_path or json_path.with_suffix(".html")
    out.write_text(render_acceptance_html(items, seed=seed), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run(
    *,
    chapters: Optional[list[int]],
    dry_run: bool,
    reset_qb: bool,
    report_path: Optional[Path],
    acceptance: bool,
    fail_mode: str = "skip",
    kinds: Optional[set[str]] = None,
) -> dict[str, Any]:
    settings = get_settings()
    media_base = os.getenv("MEDIA_BASE_URL", settings.media_base_url).rstrip("/")
    want = kinds or {"exercise", "example"}
    print(f"MEDIA_BASE_URL={media_base}")
    print(f"CHROMA_PERSIST_DIR={settings.chroma_persist_dir}")
    print(f"DATABASE={settings.database_url.split('://', 1)[0]}://***")
    print(f"kinds={sorted(want)}")

    kg = load_kg()
    tests_index = build_tests_index(kg)
    kg_exercise_ids = chapter_exercise_ids(kg)
    kg_example_ids = {
        p["id"]
        for p in kg.get("nodes", {}).get("Problem", [])
        if p.get("kind") == "example" and p.get("id")
    }
    chunks = load_canonical_chunks(chapters, kinds=want)
    n_ex = sum(1 for c in chunks if c.get("block_type") == "exercise_merged")
    n_eg = sum(1 for c in chunks if c.get("block_type") == "example")
    print(
        f"canonical exercise_merged={n_ex} example={n_eg}；"
        f"KG chapter_exercise={len(kg_exercise_ids)} example={len(kg_example_ids)}"
    )
    figure_catalog = load_global_figure_catalog(media_base)
    print(f"全局图号目录 {len(figure_catalog)} 条")

    guide_cache: dict[int, dict[str, str]] = {}
    guide_fig_cache: dict[int, dict[str, str]] = {}
    success: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    needs_kg_review: list[str] = []
    patches_list: list[dict[str, Any]] = []
    per_chapter: Counter[int] = Counter()
    per_kind: Counter[str] = Counter()
    preview: list[dict[str, Any]] = []

    for chunk in chunks:
        bt = chunk.get("block_type")
        ch_num = int(chunk.get("chapter_num") or 0)
        try:
            if bt == "exercise_merged":
                eid = chunk.get("exercise_id") or ""
                if ch_num not in guide_cache:
                    guide_cache[ch_num] = load_guide_answers(ch_num)
                if ch_num not in guide_fig_cache:
                    guide_fig_cache[ch_num] = load_guide_labeled_figures(
                        ch_num, media_base
                    )
                item = parse_exercise_chunk(
                    chunk,
                    media_base=media_base,
                    guide_answer=guide_cache[ch_num].get(eid),
                    figure_catalog=figure_catalog,
                    guide_figs=guide_fig_cache[ch_num],
                )
            elif bt == "example":
                eid = chunk.get("example_id") or ""
                item = parse_example_chunk(
                    chunk,
                    media_base=media_base,
                    figure_catalog=figure_catalog,
                )
            else:
                continue
        except Exception as exc:  # noqa: BLE001
            failed.append(
                {
                    "exercise_id": chunk.get("exercise_id") or chunk.get("example_id"),
                    "errors": [f"parse:{exc}"],
                    "block_type": bt,
                }
            )
            continue

        pid = item.get("problem_id") or item.get("exercise_id") or ""
        tests = tests_index.get(pid, [])
        errs = validate_item(item, tests)
        kg_miss = "needs_kg_review" in errs
        if kg_miss:
            needs_kg_review.append(pid)
            errs = [e for e in errs if e != "needs_kg_review"]

        if errs:
            failed.append(
                {
                    "exercise_id": pid,
                    "errors": errs,
                    "source": item.get("source"),
                    "kind": item.get("kind"),
                }
            )
            if fail_mode == "skip":
                continue

        tags = knowledge_tags_payload(
            problem_id=pid,
            chunk_id=item["chunk_id"],
            tests=tests,
            needs_kg_review=kg_miss,
            kind=str(item.get("kind") or "chapter_exercise"),
        )
        record = {
            **item,
            "knowledge_tags": tags,
            "db_id": None,
            "needs_kg_review": kg_miss,
        }
        if item.get("patches"):
            patches_list.append({"exercise_id": pid, "patches": item["patches"], "kind": item.get("kind")})
        success.append(record)
        per_chapter[item["chapter_num"]] += 1
        per_kind[str(item.get("kind") or "?")] += 1
        if len(preview) < 8:
            preview.append(
                {
                    "exercise_id": pid,
                    "kind": item.get("kind"),
                    "source": item["source"],
                    "content_preview": item["content"][:240],
                    "answer_preview": item["answer"][:240],
                    "tags": tags.get("tags"),
                    "image_urls": item["image_urls"][:5],
                    "patches": item.get("patches"),
                }
            )

    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "dry_run": dry_run,
        "media_base_url": media_base,
        "kinds": sorted(want),
        "total": len(chunks),
        "success": len(success),
        "failed": len(failed),
        "needs_kg_review": needs_kg_review,
        "needs_kg_review_count": len(needs_kg_review),
        "per_chapter_counts": {str(k): per_chapter[k] for k in sorted(per_chapter)},
        "per_kind_counts": dict(per_kind),
        "failed_items": failed,
        "patches": patches_list,
        "preview": preview,
        "kg_chapter_exercise": len(kg_exercise_ids),
        "kg_example": len(kg_example_ids),
        "canonical_exercise_merged": n_ex,
        "canonical_example": n_eg,
    }

    if dry_run:
        if report_path:
            write_json(report_path, report)
            print(f"dry-run 报告 → {report_path}")
        print(
            f"[dry-run] total={report['total']} success={report['success']} "
            f"failed={report['failed']} needs_kg_review={report['needs_kg_review_count']} "
            f"kinds={report['per_kind_counts']}"
        )
        return report

    from app.db import SessionLocal, init_db

    init_db()
    db = SessionLocal()
    try:
        if reset_qb:
            n_del = reset_textbook_questions(db)
            print(f"--reset-qb 已删除旧课本题 {n_del} 道")
            recreate_chroma_question_bank()

        for i, rec in enumerate(success, 1):
            db_id = upsert_question(
                db,
                rec,
                rec["knowledge_tags"],
                sync=False,
            )
            rec["db_id"] = db_id
            if i % 40 == 0 or i == len(success):
                db.commit()
                print(f"  upsert db {i}/{len(success)}")
        db.commit()

        n_sync = resync_all_active_questions(db)
        report["chroma_synced_active"] = n_sync

        from app.db.models import QuestionBank
        from app.services.chromadb_client import get_chroma_store

        active_tb = (
            db.query(QuestionBank)
            .filter(
                QuestionBank.source.like(f"{SOURCE_PREFIX}%"),
                QuestionBank.status == "active",
            )
            .count()
        )
        # 分类型统计
        kind_db: Counter[str] = Counter()
        for row in db.query(QuestionBank).filter(QuestionBank.source.like(f"{SOURCE_PREFIX}%")):
            tags = row.knowledge_tags if isinstance(row.knowledge_tags, dict) else {}
            kind_db[str(tags.get("kind") or ("example" if "·例" in (row.source or "") else "chapter_exercise"))] += 1
        chroma_count = get_chroma_store().collection.count()
        report["db_active_textbook"] = active_tb
        report["db_kind_counts"] = dict(kind_db)
        report["chroma_question_bank_count"] = chroma_count
        report["embedding_note"] = (
            "当前环境无 sentence_transformers/FlagEmbedding，Chroma 使用 mock 向量；"
            "安装真模型后请重跑本脚本或 reindex_chroma_real_bge.py"
        )

        if acceptance:
            acc = build_acceptance_pack(
                db,
                seed=ACCEPTANCE_SEED,
                out_prefix=ROOT / "reports" / "qb_acceptance_sample10",
            )
            report["acceptance"] = {
                "seed": ACCEPTANCE_SEED,
                "paths": {k: acc[k] for k in ("md", "json", "html")},
                "exercise_ids": [x["exercise_id"] for x in acc["items"]],
            }
            print("验收包:", report["acceptance"]["paths"])
    finally:
        db.close()

    if report_path:
        write_json(report_path, report)
        print(f"报告 → {report_path}")
    print(
        f"完成 total={report['total']} success={report['success']} failed={report['failed']} "
        f"db_active_textbook={report.get('db_active_textbook')} "
        f"db_kinds={report.get('db_kind_counts')} "
        f"chroma≈{report.get('chroma_question_bank_count')}"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="课本习题/例题灌入 question_bank")
    parser.add_argument("--chapters", type=int, nargs="*", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--reset-qb",
        action="store_true",
        help="仅清除 source 以「课本·」开头的旧题后再灌",
    )
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument(
        "--no-acceptance",
        action="store_true",
        help="全量写入后不生成验收抽样包",
    )
    parser.add_argument(
        "--kinds",
        nargs="+",
        choices=("exercise", "example"),
        default=None,
        help="灌入类型，默认 exercise+example",
    )
    parser.add_argument(
        "--render-acceptance-html",
        type=Path,
        nargs="?",
        const=ROOT / "reports" / "qb_acceptance_sample10.json",
        default=None,
        help="仅从验收 JSON 重渲 HTML（默认 reports/qb_acceptance_sample10.json）",
    )
    parser.add_argument(
        "--fail-mode",
        choices=("skip",),
        default="skip",
        help="校验失败默认不入库",
    )
    args = parser.parse_args()
    if args.render_acceptance_html is not None:
        out = regenerate_acceptance_html_from_json(args.render_acceptance_html)
        print(f"已重渲验收 HTML → {out} ({out.stat().st_size} bytes)")
        return
    kinds = set(args.kinds) if args.kinds else {"exercise", "example"}
    run(
        chapters=args.chapters,
        dry_run=args.dry_run,
        reset_qb=args.reset_qb,
        report_path=args.report,
        acceptance=not args.dry_run and not args.no_acceptance,
        fail_mode=args.fail_mode,
        kinds=kinds,
    )


if __name__ == "__main__":
    main()
