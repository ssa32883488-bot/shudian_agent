#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 canonical 抽取知识图谱实体（Chapter / Problem / Concept 候选）。

本阶段只抽实体、不做 TESTS/前置关系，便于人工审阅后再构图。

用法（在 shudian_agent 根目录）:
  python data/extract_kg_entities.py
  python data/extract_kg_entities.py --chapters 1 2 3
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
CANONICAL = BACKEND / "data" / "canonical"
OUT = ROOT / "data" / "kg"

REVIEW_ID_RE = re.compile(r"\bR(\d+(?:\.\d+)+)\b")
SECTION_NUM_TITLE_RE = re.compile(
    r"^\*?\s*(\d+(?:\.\d+)*)\s+(.+)$"
)
# 辅导册「一、xxx」类小节
CN_ENUM_TITLE_RE = re.compile(r"^[一二三四五六七八九十]+[、.．]\s*(.+)$")

META_SECTION_KEYWORDS = (
    "概述",
    "本章重点",
    "难点释疑",
    "习题类型",
    "解题方法",
    "本章小结",
    "内容提要",
    "章末习题",
    "复习思考题",
    "方法和步骤",
    "顶层设计",
    "同步状态转换模块",
)

NOISE_TITLE_RE = re.compile(
    r"^(为什么|怎样|如何|是否|能否|检查所设计|则开始|用增加|解ex)"
)


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _bc_tail(bc) -> str:
    if isinstance(bc, list) and bc:
        return str(bc[-1]).strip()
    return ""


def _is_meta_title(title: str) -> bool:
    t = title.strip()
    if not t or len(t) < 2:
        return True
    if any(k in t for k in META_SECTION_KEYWORDS):
        return True
    if NOISE_TITLE_RE.search(t):
        return True
    if t.startswith("//") or t.startswith("* 2 ") or "=>" in t:
        return True
    return False


def _clean_concept_name(raw: str) -> str:
    name = raw.strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r"[（(]\s*$", "", name)
    # 去掉末尾多余标点
    name = name.strip(" ：:，,。；;")
    return name


def extract_chapters(chapter_nums: list[int]) -> list[dict]:
    out = []
    for n in chapter_nums:
        report = CANONICAL / f"ch{n:02d}" / "pilot_report.json"
        if report.exists():
            data = json.loads(report.read_text(encoding="utf-8"))
            title = data.get("chapter") or f"第{n:02d}章"
        else:
            title = f"第{n:02d}章"
        out.append(
            {
                "id": f"ch{n:02d}",
                "type": "Chapter",
                "name": title,
                "chapter_num": n,
            }
        )
    return out


def extract_problems(chapter_nums: list[int]) -> list[dict]:
    problems: dict[str, dict] = {}

    def upsert(pid: str, **fields: object) -> None:
        if pid in problems:
            # 合并 source_chunk_ids
            old = problems[pid]
            ids = list(dict.fromkeys((old.get("source_chunk_ids") or []) + (fields.get("source_chunk_ids") or [])))  # type: ignore
            old.update({k: v for k, v in fields.items() if k != "source_chunk_ids" and v})
            old["source_chunk_ids"] = ids
            if fields.get("stem_preview") and len(str(fields["stem_preview"])) > len(str(old.get("stem_preview") or "")):
                old["stem_preview"] = fields["stem_preview"]
        else:
            problems[pid] = {"id": pid, **fields}

    for n in chapter_nums:
        ch_id = f"ch{n:02d}"
        chunks = _load_jsonl(CANONICAL / ch_id / "chunks.jsonl")
        exercises = _load_jsonl(CANONICAL / ch_id / "exercises_merged.jsonl")

        # 章末习题
        for e in exercises:
            eid = e.get("exercise_id") or ""
            if not eid:
                continue
            stem = (e.get("stem") or "").strip().replace("\n", " ")
            upsert(
                eid,
                type="Problem",
                kind="chapter_exercise",
                name=eid,
                chapter_id=ch_id,
                chapter_num=n,
                has_answer=bool(e.get("has_answer")),
                stem_preview=stem[:160],
                source_chunk_ids=[],
            )

        for c in chunks:
            cid = c.get("chunk_id") or ""
            bt = c.get("block_type")
            text = (c.get("text_content") or "").strip()
            preview = re.sub(r"\s+", " ", text)[:160]

            if bt == "example" and c.get("example_id"):
                eid = c["example_id"]
                upsert(
                    eid,
                    type="Problem",
                    kind="example",
                    name=eid,
                    chapter_id=ch_id,
                    chapter_num=n,
                    section_id=c.get("section_id") or "",
                    stem_preview=preview,
                    source_chunk_ids=[cid],
                )
            elif bt == "review":
                m = REVIEW_ID_RE.search(text)
                if not m:
                    # 整块可能含多道 R 题，按行拆
                    for m2 in REVIEW_ID_RE.finditer(text):
                        rid = f"R{m2.group(1)}"
                        # 截取该题附近预览
                        start = max(0, m2.start() - 0)
                        snippet = re.sub(r"\s+", " ", text[start : start + 180])
                        upsert(
                            rid,
                            type="Problem",
                            kind="review",
                            name=rid,
                            chapter_id=ch_id,
                            chapter_num=n,
                            section_id=c.get("section_id") or "",
                            stem_preview=snippet,
                            source_chunk_ids=[cid],
                        )
                    continue
                rid = f"R{m.group(1)}"
                upsert(
                    rid,
                    type="Problem",
                    kind="review",
                    name=rid,
                    chapter_id=ch_id,
                    chapter_num=n,
                    section_id=c.get("section_id") or "",
                    stem_preview=preview,
                    source_chunk_ids=[cid],
                )
            elif bt == "exercise_merged" and c.get("exercise_id"):
                eid = c["exercise_id"]
                upsert(
                    eid,
                    type="Problem",
                    kind="chapter_exercise",
                    name=eid,
                    chapter_id=ch_id,
                    chapter_num=n,
                    section_id=c.get("section_id") or "",
                    stem_preview=preview if not problems.get(eid, {}).get("stem_preview") else problems[eid].get("stem_preview"),
                    source_chunk_ids=[cid],
                )

    # 稳定排序
    order = {"example": 0, "review": 1, "chapter_exercise": 2, "drill": 3}
    return sorted(
        problems.values(),
        key=lambda x: (x.get("chapter_num", 0), order.get(str(x.get("kind")), 9), str(x.get("id"))),
    )


def extract_concepts(chapter_nums: list[int]) -> list[dict]:
    """从章节标题结构抽取 Concept 候选（规则法，供审阅）。"""
    concepts: dict[str, dict] = {}
    title_counter: Counter[str] = Counter()

    def add(name: str, *, chapter_num: int, source: str, section_code: str = "", confidence: str = "medium") -> None:
        name = _clean_concept_name(name)
        if not name or _is_meta_title(name) or len(name) > 40:
            return
        # 过滤过短无信息
        if len(name) < 2:
            return
        key = name
        title_counter[name] += 1
        ch_id = f"ch{chapter_num:02d}"
        if key in concepts:
            ent = concepts[key]
            if ch_id not in ent["chapter_ids"]:
                ent["chapter_ids"].append(ch_id)
            if source not in ent["sources"]:
                ent["sources"].append(source)
            if section_code and section_code not in ent.get("section_codes", []):
                ent.setdefault("section_codes", []).append(section_code)
            # 提升置信度：多章或编号小节
            if confidence == "high":
                ent["confidence"] = "high"
        else:
            slug = re.sub(r"[^\w\u4e00-\u9fff]+", "_", name)[:40]
            concepts[key] = {
                "id": f"concept_ch{chapter_num:02d}_{slug}",
                "type": "Concept",
                "name": name,
                "chapter_ids": [ch_id],
                "primary_chapter_num": chapter_num,
                "section_codes": [section_code] if section_code else [],
                "sources": [source],
                "confidence": confidence,
            }

    for n in chapter_nums:
        ch_id = f"ch{n:02d}"
        seen_tails: set[str] = set()
        for c in _load_jsonl(CANONICAL / ch_id / "chunks.jsonl"):
            tail = _bc_tail(c.get("breadcrumb"))
            if not tail or tail in seen_tails:
                continue
            seen_tails.add(tail)

            m = SECTION_NUM_TITLE_RE.match(tail)
            if m:
                code, title = m.group(1), m.group(2)
                # 编号越深通常越像知识点；1 级概述已在 meta 过滤
                conf = "high" if code.count(".") >= 1 else "medium"
                add(title, chapter_num=n, source="section_title", section_code=code, confidence=conf)
                continue

            m2 = CN_ENUM_TITLE_RE.match(tail)
            if m2:
                add(m2.group(1), chapter_num=n, source="guide_enum_title", confidence="low")
                continue

            # 其它非元数据短标题
            if not _is_meta_title(tail) and 2 <= len(tail) <= 30 and not tail.startswith("第"):
                add(tail, chapter_num=n, source="breadcrumb_tail", confidence="low")

    # 稳定 id：若跨章，用首次章号 id 保留，另记 chapters
    out = list(concepts.values())
    out.sort(key=lambda x: (x.get("primary_chapter_num", 0), x.get("name", "")))
    return out


def write_review_md(
    chapters: list[dict],
    problems: list[dict],
    concepts: list[dict],
    path: Path,
) -> None:
    kind_cnt = Counter(p.get("kind") for p in problems)
    conf_cnt = Counter(c.get("confidence") for c in concepts)
    lines: list[str] = []
    lines.append("# 知识图谱实体抽取审阅稿")
    lines.append("")
    lines.append("本文件仅含**实体**，尚未构建 TESTS / 前置关系。请重点看：Concept 是否过碎/过空，Problem 种类是否齐全。")
    lines.append("")
    lines.append("## 汇总")
    lines.append("")
    lines.append(f"- Chapter: **{len(chapters)}**")
    lines.append(f"- Problem: **{len(problems)}** （{dict(kind_cnt)}）")
    lines.append(f"- Concept 候选: **{len(concepts)}** （置信度 {dict(conf_cnt)}）")
    lines.append("- 小练(drill): **0**（辅导材料中未检出独立「小练」块；若书中有，需另补解析）")
    lines.append("")
    lines.append("## Chapter")
    lines.append("")
    for ch in chapters:
        lines.append(f"- `{ch['id']}` {ch['name']}")
    lines.append("")
    lines.append("## Problem 抽样（每章每种最多 5 条）")
    lines.append("")
    by_ch: dict[int, list[dict]] = defaultdict(list)
    for p in problems:
        by_ch[int(p.get("chapter_num") or 0)].append(p)
    for n in sorted(by_ch):
        lines.append(f"### 第{n:02d}章")
        for kind in ("example", "review", "chapter_exercise"):
            items = [p for p in by_ch[n] if p.get("kind") == kind][:5]
            if not items:
                continue
            lines.append(f"- **{kind}** ×{sum(1 for p in by_ch[n] if p.get('kind')==kind)}")
            for p in items:
                lines.append(f"  - `{p['id']}`: {p.get('stem_preview','')[:100]}")
        lines.append("")
    lines.append("## Concept 候选（按章，high/medium 优先）")
    lines.append("")
    by_cch: dict[int, list[dict]] = defaultdict(list)
    for c in concepts:
        by_cch[int(c.get("primary_chapter_num") or 0)].append(c)
    for n in sorted(by_cch):
        lines.append(f"### 第{n:02d}章")
        items = sorted(by_cch[n], key=lambda x: ({"high":0,"medium":1,"low":2}.get(str(x.get("confidence")),9), x["name"]))
        for c in items:
            codes = ",".join(c.get("section_codes") or []) or "—"
            lines.append(
                f"- [{c.get('confidence')}] **{c['name']}**  "
                f"`{c['id']}`  section={codes}  sources={','.join(c.get('sources') or [])}"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", type=int, nargs="*", default=None)
    args = parser.parse_args()
    nums = args.chapters or list(range(1, 9))

    OUT.mkdir(parents=True, exist_ok=True)
    chapters = extract_chapters(nums)
    problems = extract_problems(nums)
    concepts = extract_concepts(nums)

    (OUT / "entities_chapters.json").write_text(
        json.dumps(chapters, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "entities_problems.jsonl").write_text(
        "\n".join(json.dumps(p, ensure_ascii=False) for p in problems) + "\n",
        encoding="utf-8",
    )
    (OUT / "entities_concepts.json").write_text(
        json.dumps(concepts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    summary = {
        "chapters": len(chapters),
        "problems": len(problems),
        "problems_by_kind": dict(Counter(p.get("kind") for p in problems)),
        "concepts": len(concepts),
        "concepts_by_confidence": dict(Counter(c.get("confidence") for c in concepts)),
        "drill_note": "未检出小练实体；辅导册需另确认是否有独立练习块",
        "outputs": {
            "chapters": str(OUT / "entities_chapters.json"),
            "problems": str(OUT / "entities_problems.jsonl"),
            "concepts": str(OUT / "entities_concepts.json"),
            "review_md": str(OUT / "entities_review.md"),
        },
    }
    (OUT / "entities_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_review_md(chapters, problems, concepts, OUT / "entities_review.md")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n审阅请打开: {OUT / 'entities_review.md'}")


if __name__ == "__main__":
    main()
