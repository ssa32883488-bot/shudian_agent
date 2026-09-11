#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精炼 Concept + 构建 Problem→Concept 的 TESTS 边（规则法 v0.1）。

输入：data/kg/entities_*.json(l)
输出：
  - concepts_refined.json
  - relationships_tests.jsonl
  - relationships_belongs_to.jsonl
  - knowledge_graph_v0.1.json
  - kg_v0.1_review.md

用法（shudian_agent 根目录）:
  python data/build_kg_tests.py
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KG = ROOT / "data" / "kg"

SUFFIXES = (
    "及其成因",
    "的方法和步骤",
    "的基本方法和步骤",
    "的电路结构和工作原理",
    "的结构和工作原理",
    "的工作原理",
    "的基本原理",
    "的基本结构",
    "的动态特性",
    "的静态特性",
    "的输入特性",
    "的输出特性",
    "的各种系列",
    "的基本设计方法",
    "的分析方法",
    "的设计方法",
    "的特点",
    "的应用",
    "的步骤",
    "的方法",
    "化简法",
)

DROP_NAME_RE = re.compile(
    r"(习题类型|解题方法|本章重点|难点释疑|概述|内容提要|本章小结|"
    r"顶层设计|同步状态|则开始|检查所设计|工艺设计|"
    r"用.*组成|用.*设计|用.*接成|用.*构成|"
    r"\\\\Rightarrow|\$|系列$|^公式$|^电路$|^波形图$|^逻辑图$)"
)

# strip_suffixes 后过短/过泛的名称：重命名，避免「公式化简法」→「公式」
AFTER_STRIP_RENAMES = {
    "公式": "公式化简",
}

EXAMPLE_ID_RE = re.compile(r"^例(\d+(?:\.\d+)+)$")
REVIEW_ID_RE = re.compile(r"^R(\d+(?:\.\d+)+)$")
EXERCISE_ID_RE = re.compile(r"^题(\d+)\.(\d+)$")
FIG_REF_RE = re.compile(r"图\s*(P?\d+(?:\.\d+)*)", re.IGNORECASE)

# 仅靠这些短别名命中时置信度要克制（题干常顺带出现）
GENERIC_ALIASES = {
    "二进制",
    "八进制",
    "十六进制",
    "十进制",
    "电路",
    "逻辑",
    "函数",
    "波形",
    "设计",
    "分析",
}

# 难用关键词覆盖的题：显式挂点（名称对齐精炼后 Concept.name）
FORCE_TESTS: dict[str, list[str]] = {
    "R1.5.3": ["ASCII代码"],
    "题3.3": ["异或与同或", "CMOS反相器"],
    "题5.20": ["触发器", "寄存器"],
    "题5.26": ["触发器", "SR 锁存器"],
    "题6.23": ["计数器", "同步计数器"],
    "题6.30": ["时序逻辑电路的自启动设计", "复杂时序逻辑电路的设计"],
    "题8.9": ["ROM", "D/A 转换器"],
    "题8.10": ["D/A 转换器", "权电阻网络 D/A 转换器"],
}

# 概念名包含左侧片段时，追加右侧别名（补挂习题用）
MANUAL_ALIAS_RULES: list[tuple[str, list[str]]] = [
    ("进制", ["二进制", "八进制", "十六进制", "十进制", "数制", "进制转换", "十-二转换", "二-十转换"]),
    ("十-二转换", ["十-二转换", "二-十转换", "整数部分", "小数部分"]),
    ("三种基本运算", ["异或", "同或", "与门", "或门", "非门", "与运算", "或运算", "非运算", "与非", "或非"]),
    ("两种标准形式", ["最小项", "最大项", "最小项之和", "最大项之积"]),
    ("十进制代码", ["8421", "2421", "5211", "余3", "余 3", "BCD"]),
    ("ASCII", ["ASCII", "ascii"]),
    ("格雷码", ["格雷码", "Gray码"]),
    ("反码、补码", ["原码", "反码", "补码", "补码运算"]),
    ("二进制算术运算", ["算术运算", "加减运算"]),
    ("卡诺图", ["卡诺图", "K图"]),
    ("公式化简", ["公式化简", "公式法", "代数化简"]),
    ("代入定理", ["代入定理"]),
    ("反演定理", ["反演定理", "求反"]),
    ("对偶定理", ["对偶定理", "对偶"]),
    ("CMOS反相器", ["CMOS反相器", "CMOS 反相器"]),
    ("CMOS", ["CMOS", "74HC", "HC系列"]),
    ("TTL", ["TTL", "74LS", "LS系列", "74系列TTL", "74系列"]),
    ("二极管与门", ["二极管与门", "与门"]),
    ("二极管或门", ["二极管或门", "或门"]),
    ("漏极开路", ["OD", "OD门", "OD输出", "漏极开路"]),
    ("集电极开路", ["OC", "OC门", "OC输出", "集电极开路"]),
    ("三态", ["三态", "高阻", "TS", "三态输出"]),
    ("接口", ["接口", "上拉电阻", "电平转换"]),
    ("编码器", ["编码", "优先编码", "74HC148"]),
    ("译码器", ["译码", "74HC138", "74LS154", "74HC42"]),
    ("数据选择器", ["数据选择", "MUX", "多路选择"]),
    ("加法器", ["全加器", "半加器", "加法器"]),
    ("数值比较器", ["比较器", "74HC85"]),
    ("竞争", ["竞争", "冒险", "竞争冒险", "竞争-冒险"]),
    ("触发器", ["触发器", "FF", "边沿触发"]),
    ("锁存器", ["锁存", "SR锁存"]),
    ("寄存器", ["寄存器", "移位寄存器"]),
    ("计数器", ["计数器", "模"]),
    ("ROM", ["ROM", "只读存储器"]),
    ("SRAM", ["SRAM"]),
    ("DRAM", ["DRAM"]),
    ("施密特", ["施密特"]),
    ("单稳态", ["单稳态"]),
    ("多谐振荡", ["多谐振荡", "振荡器"]),
    ("555", ["555", "定时器"]),
    ("D/A", ["D/A", "DAC", "数模"]),
    ("A/D", ["A/D", "ADC", "模数"]),
    ("硬件描述语言", ["Verilog", "HDL", "verilog", "Verilog HDL"]),
    ("组合逻辑电路的基本设计", ["多数表决", "表决电路", "代码转换"]),
    ("层次化和模块化", ["扩展", "接成"]),
    ("存储器容量的扩展", ["2114", "位扩展", "字扩展", "容量扩展"]),
    ("SRAM", ["2114", "RAM"]),
    ("同步时序逻辑电路的设计", ["自启动", "状态机", "数字钟", "序列检测", "串行数据"]),
    ("异步时序", ["异步时序"]),
    ("同步时序", ["同步时序"]),
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def strip_suffixes(name: str) -> str:
    n = name.strip()
    changed = True
    while changed:
        changed = False
        for suf in SUFFIXES:
            if n.endswith(suf) and len(n) > len(suf) + 1:
                n = n[: -len(suf)].rstrip("的")
                changed = True
                break
    return n.strip() or name.strip()


def make_aliases(name: str) -> list[str]:
    aliases = []
    for cand in {name, strip_suffixes(name), name.replace("－", "-").replace("—", "-")}:
        cand = cand.strip()
        if cand and cand not in aliases:
            aliases.append(cand)
        # 竞争-冒险 / 竞争冒险
        if "-" in cand or "－" in cand:
            flat = re.sub(r"[\-－]", "", cand)
            if flat not in aliases:
                aliases.append(flat)
        if "D/A" in cand:
            aliases.append(cand.replace("D/A", "DAC"))
        if "A/D" in cand:
            aliases.append(cand.replace("A/D", "ADC"))
    # 长名取核心：去掉括号内容
    core = re.sub(r"[（(][^）)]*[）)]", "", name).strip()
    if core and core not in aliases:
        aliases.append(core)
        s2 = strip_suffixes(core)
        if s2 not in aliases:
            aliases.append(s2)
    return [a for a in aliases if len(a) >= 2]


def refine_concepts(raw: list[dict]) -> list[dict]:
    """保留 high/medium；丢弃明显噪声 low；规范化名称与别名。"""
    kept: list[dict] = []
    for c in raw:
        conf = c.get("confidence") or "low"
        name = (c.get("name") or "").strip()
        if conf == "low":
            # low 仅保留短且像术语、且不在 drop 模式里的
            if len(name) > 12 or DROP_NAME_RE.search(name):
                continue
            if c.get("sources") == ["breadcrumb_tail"]:
                continue
            # 辅导枚举短标题可留作补充
            if "guide_enum_title" not in (c.get("sources") or []):
                continue
            if len(name) < 2:
                continue
        else:
            if DROP_NAME_RE.search(name):
                continue

        display = strip_suffixes(name)
        display = AFTER_STRIP_RENAMES.get(display, display)
        if DROP_NAME_RE.search(display):
            continue
        display = re.sub(r"\s+", "", display) if re.fullmatch(r"[A-Za-z0-9\-/\u4e00-\u9fff\s]+", display) and "反相器" in display else display
        # CMOS 反相器 统一去多余空格变体在合并 key 时处理
        display_key = re.sub(r"\s+", "", display)
        # 仍过长的方法类标题再压一档
        if len(display) > 24 and conf != "high":
            continue

        aliases = make_aliases(name)
        if display not in aliases:
            aliases.insert(0, display)
        if display_key not in aliases and display_key != display:
            aliases.append(display_key)

        kept.append(
            {
                "id": c["id"],
                "type": "Concept",
                "name": display,
                "raw_name": name,
                "aliases": aliases,
                "chapter_ids": c.get("chapter_ids") or [],
                "primary_chapter_num": c.get("primary_chapter_num"),
                "section_codes": c.get("section_codes") or [],
                "confidence": conf if conf != "low" else "low_kept",
                "sources": c.get("sources") or [],
            }
        )

    # 按 display name + primary chapter 去重（空格不敏感）
    merged: dict[tuple, dict] = {}
    for c in kept:
        key = (c["primary_chapter_num"], re.sub(r"\s+", "", c["name"]))
        if key not in merged:
            merged[key] = c
        else:
            old = merged[key]
            old["section_codes"] = list(dict.fromkeys((old.get("section_codes") or []) + (c.get("section_codes") or [])))
            old["aliases"] = list(dict.fromkeys((old.get("aliases") or []) + (c.get("aliases") or [])))
            old["chapter_ids"] = list(dict.fromkeys((old.get("chapter_ids") or []) + (c.get("chapter_ids") or [])))
            if c.get("confidence") == "high":
                old["confidence"] = "high"
            if len(c["name"]) < len(old["name"]):
                old["name"] = c["name"]
            if (c.get("section_codes") and not old.get("section_codes")) or (
                c.get("confidence") == "high" and old.get("confidence") != "high"
            ):
                old["id"] = c["id"]
                old["raw_name"] = c.get("raw_name", old.get("raw_name"))

    out = list(merged.values())
    # 追加人工别名
    for c in out:
        name = c.get("name") or ""
        raw = c.get("raw_name") or ""
        extra: list[str] = []
        for frag, aliases in MANUAL_ALIAS_RULES:
            if frag in name or frag in raw:
                extra.extend(aliases)
        if extra:
            c["aliases"] = list(dict.fromkeys((c.get("aliases") or []) + extra))

    # 习题高频但标题未单列的微概念
    seeds = [
        {
            "id": "concept_ch01_数制与进制转换",
            "type": "Concept",
            "name": "数制与进制转换",
            "raw_name": "数制与进制转换",
            "aliases": [
                "数制",
                "进制",
                "进制转换",
                "二进制",
                "八进制",
                "十六进制",
                "十进制",
                "十-二转换",
                "二-十转换",
            ],
            "chapter_ids": ["ch01"],
            "primary_chapter_num": 1,
            "section_codes": ["1.2", "1.3"],
            "confidence": "seed",
            "sources": ["seed"],
            # 不参与章内 section_order hub，避免串进全书前置链
            "skip_section_prereq": True,
        },
        {
            "id": "concept_ch01_ASCII代码",
            "type": "Concept",
            "name": "ASCII代码",
            "raw_name": "ASCII代码",
            "aliases": ["ASCII", "ascii"],
            "chapter_ids": ["ch01"],
            "primary_chapter_num": 1,
            "section_codes": ["1.5"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch02_异或与同或",
            "type": "Concept",
            "name": "异或与同或",
            "raw_name": "异或与同或",
            "aliases": ["异或", "同或", "异或运算", "同或运算"],
            "chapter_ids": ["ch02"],
            "primary_chapter_num": 2,
            "section_codes": ["2.2"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch02_最小项与最大项",
            "type": "Concept",
            "name": "最小项与最大项",
            "raw_name": "最小项与最大项",
            "aliases": ["最小项", "最大项", "最小项之和", "最大项之积"],
            "chapter_ids": ["ch02"],
            "primary_chapter_num": 2,
            "section_codes": ["2.5.3"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch03_集电极开路输出OC",
            "type": "Concept",
            "name": "集电极开路输出(OC)",
            "raw_name": "集电极开路输出(OC)",
            "aliases": ["OC", "OC门", "集电极开路", "OC输出"],
            "chapter_ids": ["ch03"],
            "primary_chapter_num": 3,
            "section_codes": ["3.4"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch03_漏极开路输出OD",
            "type": "Concept",
            "name": "漏极开路输出(OD)",
            "raw_name": "漏极开路输出(OD)",
            "aliases": ["OD", "OD门", "漏极开路", "OD输出"],
            "chapter_ids": ["ch03"],
            "primary_chapter_num": 3,
            "section_codes": ["3.3"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch03_三态输出",
            "type": "Concept",
            "name": "三态输出",
            "raw_name": "三态输出",
            "aliases": ["三态", "高阻", "三态输出", "TS"],
            "chapter_ids": ["ch03"],
            "primary_chapter_num": 3,
            "section_codes": ["3.3"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch06_时序与组合区别",
            "type": "Concept",
            "name": "时序逻辑与组合逻辑的区别",
            "raw_name": "时序逻辑与组合逻辑的区别",
            "aliases": ["时序逻辑电路", "组合逻辑电路", "逻辑功能与电路结构"],
            "chapter_ids": ["ch06"],
            "primary_chapter_num": 6,
            "section_codes": ["6.1"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch06_同步与异步",
            "type": "Concept",
            "name": "同步时序与异步时序",
            "raw_name": "同步时序与异步时序",
            "aliases": ["同步时序", "异步时序", "同步时序电路", "异步时序电路"],
            "chapter_ids": ["ch06"],
            "primary_chapter_num": 6,
            "section_codes": ["6.1", "6.2"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch04_组合逻辑设计",
            "type": "Concept",
            "name": "组合逻辑电路设计",
            "raw_name": "组合逻辑电路设计",
            "aliases": ["设计一个", "逻辑电路", "多数表决", "代码转换", "电灯"],
            "chapter_ids": ["ch04"],
            "primary_chapter_num": 4,
            "section_codes": ["4.3"],
            "confidence": "seed",
            "sources": ["seed"],
        },
        {
            "id": "concept_ch02_逻辑等式证明",
            "type": "Concept",
            "name": "逻辑等式证明",
            "raw_name": "逻辑等式证明",
            "aliases": ["证明下列", "逻辑恒等式", "互相排斥", "恒等式"],
            "chapter_ids": ["ch02"],
            "primary_chapter_num": 2,
            "section_codes": ["2.3"],
            "confidence": "seed",
            "sources": ["seed"],
        },
    ]
    existing = {re.sub(r"\s+", "", c["name"]) for c in out}
    for s in seeds:
        if re.sub(r"\s+", "", s["name"]) not in existing:
            out.append(s)

    out.sort(key=lambda x: (x.get("primary_chapter_num") or 0, x.get("name") or ""))
    return out


def enrich_problem_stems(problems: list[dict]) -> None:
    """用 exercises_merged / chunks 全文加长题干，便于关键词命中。"""
    backend = ROOT / "backend" / "data" / "canonical"
    full: dict[str, str] = {}
    for n in range(1, 9):
        ch = backend / f"ch{n:02d}"
        for e in load_jsonl(ch / "exercises_merged.jsonl"):
            eid = e.get("exercise_id")
            if eid:
                full[eid] = (e.get("stem") or "").strip()
        for c in load_jsonl(ch / "chunks.jsonl"):
            text = (c.get("text_content") or "").strip()
            if c.get("example_id"):
                full[c["example_id"]] = text
            if c.get("block_type") == "review":
                for m in re.finditer(r"\bR(\d+(?:\.\d+)+)\b", text):
                    rid = f"R{m.group(1)}"
                    # 取该题起 400 字
                    snippet = text[m.start() : m.start() + 400]
                    if rid not in full or len(snippet) > len(full[rid]):
                        full[rid] = snippet
    for p in problems:
        pid = p.get("id") or ""
        if pid in full and full[pid]:
            p["stem_full"] = re.sub(r"\s+", " ", full[pid])[:1200]
        else:
            p["stem_full"] = p.get("stem_preview") or ""


def section_prefix_from_problem_id(pid: str) -> str | None:
    m = EXAMPLE_ID_RE.match(pid) or REVIEW_ID_RE.match(pid)
    if m:
        return m.group(1)  # e.g. 4.4.1
    return None


def extract_figure_codes(stem: str) -> list[str]:
    codes = []
    for m in FIG_REF_RE.finditer(stem or ""):
        raw = m.group(1)
        raw = raw[1:] if raw.upper().startswith("P") else raw
        if raw and raw not in codes:
            codes.append(raw)
    return codes


def code_matches(problem_code: str, concept_codes: list[str]) -> bool:
    """例/R/图号 与概念 section_codes 前缀匹配。"""
    if not problem_code or not concept_codes:
        return False
    for code in concept_codes:
        if not code:
            continue
        if problem_code == code or problem_code.startswith(code + ".") or code.startswith(problem_code + "."):
            return True
        pc = problem_code.split(".")
        cc = code.split(".")
        if len(pc) >= 2 and len(cc) >= 2 and pc[0] == cc[0] and pc[1] == cc[1]:
            return True
        # 图3.2.5 ↔ 概念 3.2.x
        if len(pc) >= 3 and len(cc) >= 2 and pc[0] == cc[0] and pc[1] == cc[1]:
            return True
    return False


def score_tests(problem: dict, concept: dict) -> tuple[int, str]:
    stem = " ".join(
        [
            problem.get("stem_full") or "",
            problem.get("stem_preview") or "",
            problem.get("name") or "",
        ]
    )
    stem_norm = stem.replace(" ", "")
    score = 0
    evidence: list[str] = []

    ch_id = f"ch{int(problem.get('chapter_num') or 0):02d}"
    same_chapter = ch_id in (concept.get("chapter_ids") or [])
    if same_chapter:
        score += 5
        evidence.append("same_chapter")

    # 优先挂到教材主干概念，而不是碎片 low_kept 名
    conf = concept.get("confidence") or "low"
    if conf in {"high", "seed"}:
        score += 8
        evidence.append(f"tier:{conf}")
    elif conf == "medium":
        score += 3

    pcode = section_prefix_from_problem_id(str(problem.get("id") or ""))
    if pcode and code_matches(pcode, concept.get("section_codes") or []):
        score += 60
        evidence.append(f"section:{pcode}")

    # 题干中的教材图号 → 节号
    for fcode in extract_figure_codes(stem):
        if code_matches(fcode, concept.get("section_codes") or []):
            score += 45
            evidence.append(f"figure:{fcode}")
            break

    # 章末题「题N.M」尝试用 N.M 对齐节号
    m_ex = EXERCISE_ID_RE.match(str(problem.get("id") or ""))
    if m_ex:
        ex_code = f"{m_ex.group(1)}.{m_ex.group(2)}"
        if code_matches(ex_code, concept.get("section_codes") or []):
            score += 35
            evidence.append(f"exercise_id:{ex_code}")

    aliases = sorted(concept.get("aliases") or [concept.get("name")], key=len, reverse=True)
    alias_hit = ""
    alias_hits = 0
    for alias in aliases:
        if len(alias) < 2:
            continue
        if alias in stem or alias in stem_norm:
            bonus = 10 + min(len(alias), 12)
            if len(alias) <= 2:
                bonus = 6
            if alias in {"TTL", "CMOS", "OC", "OD", "异或", "最小项", "最大项", "三态", "卡诺图", "JK", "SR"}:
                bonus += 8
            if alias in GENERIC_ALIASES:
                bonus = max(4, bonus - 6)
            score += bonus
            if not alias_hit:
                alias_hit = alias
            alias_hits += 1
            evidence.append(f"alias:{alias}")
            if alias_hits >= 3:
                break

    if alias_hits >= 2:
        score += 6
        evidence.append("multi_alias")

    # 同章 + 有效别名：抬到 medium 地板，避免「语义对但全标 low」
    has_struct = any(x.startswith(("section:", "figure:", "exercise_id:")) for x in evidence)
    if same_chapter and alias_hit and len(alias_hit) >= 3:
        floor = 40 if has_struct or conf in {"high", "seed"} else 24
        if score < floor:
            score = floor
            evidence.append("floor_medium")

    # 跨章：较强别名，或白名单短术语
    CROSS_OK = {"格雷码", "ASCII", "Verilog", "74HC138", "RAM", "2114", "卡诺图"}
    if not same_chapter:
        ok = (alias_hit and len(alias_hit) >= 4) or (alias_hit in CROSS_OK)
        if not ok:
            return 0, ""
        if score < 20:
            return 0, ""

    return score, ",".join(evidence)


def build_tests(problems: list[dict], concepts: list[dict]) -> list[dict]:
    by_ch: dict[int, list[dict]] = defaultdict(list)
    for c in concepts:
        by_ch[int(c.get("primary_chapter_num") or 0)].append(c)
        for cid in c.get("chapter_ids") or []:
            m = re.match(r"ch(\d+)", cid)
            if m:
                by_ch[int(m.group(1))].append(c)

    for k, lst in list(by_ch.items()):
        uniq = {}
        for c in lst:
            uniq[c["id"]] = c
        by_ch[k] = list(uniq.values())

    edges: list[dict] = []
    for p in problems:
        n = int(p.get("chapter_num") or 0)
        cands = by_ch.get(n, [])
        scored: list[tuple[int, str, dict]] = []
        min_score = 12 if p.get("kind") == "chapter_exercise" else 15
        for c in cands:
            s, ev = score_tests(p, c)
            if s >= min_score:
                scored.append((s, ev, c))
        # 同分时优先 high/seed、更短更像考点的名字
        scored.sort(
            key=lambda x: (
                -x[0],
                0 if x[2].get("confidence") in {"high", "seed"} else 1,
                len(x[2].get("name") or ""),
                x[2]["name"],
            )
        )

        if not scored:
            continue
        top = scored[0][0]
        picked = []
        used_sections: set[tuple] = set()
        for s, ev, c in scored:
            if len(picked) >= 4:
                break
            if s < min_score:
                break
            if s < top * 0.35 and len(picked) >= 1:
                break
            # 同节细目去重：已选过同 section 的 high 后，跳过同分碎片名
            codes = tuple((c.get("section_codes") or [])[:1])
            if codes and codes in used_sections and s < top * 0.85 and c.get("confidence") == "low_kept":
                continue
            picked.append((s, ev, c))
            if codes:
                used_sections.add(codes)

        for s, ev, c in picked:
            conf = "high" if s >= 55 else ("medium" if s >= 22 else "low")
            edges.append(
                {
                    "from": p["id"],
                    "from_type": "Problem",
                    "to": c["name"],
                    "to_id": c["id"],
                    "to_type": "Concept",
                    "type": "TESTS",
                    "score": s,
                    "confidence": conf,
                    "evidence": ev,
                    "problem_kind": p.get("kind"),
                    "chapter_num": n,
                }
            )

    # 强制补挂：仅补仍偏弱的题，且单题总数不超过 4
    by_name = {c["name"]: c for c in concepts}
    have = {(e["from"], e["to"]) for e in edges}
    per_count: dict[str, int] = Counter(e["from"] for e in edges)
    solid_pids = {
        e["from"] for e in edges if e.get("confidence") in {"high", "medium"}
    }
    for pid, names in FORCE_TESTS.items():
        if pid in solid_pids and per_count.get(pid, 0) >= 2:
            continue
        p = next((x for x in problems if x["id"] == pid), None)
        if not p:
            continue
        for name in names:
            if per_count.get(pid, 0) >= 4:
                break
            c = by_name.get(name)
            if not c:
                c = next((x for x in concepts if name in x["name"] or x["name"] in name), None)
            if not c:
                continue
            key = (pid, c["name"])
            if key in have:
                continue
            edges.append(
                {
                    "from": pid,
                    "from_type": "Problem",
                    "to": c["name"],
                    "to_id": c["id"],
                    "to_type": "Concept",
                    "type": "TESTS",
                    "score": 80,
                    "confidence": "high",
                    "evidence": "force_map",
                    "problem_kind": p.get("kind"),
                    "chapter_num": int(p.get("chapter_num") or 0),
                }
            )
            have.add(key)
            per_count[pid] = per_count.get(pid, 0) + 1
    return edges


def build_belongs_to(chapters: list[dict], concepts: list[dict], problems: list[dict]) -> list[dict]:
    ch_name = {c["id"]: c["name"] for c in chapters}
    edges = []
    for c in concepts:
        for cid in c.get("chapter_ids") or []:
            edges.append(
                {
                    "from": c["name"],
                    "from_id": c["id"],
                    "from_type": "Concept",
                    "to": ch_name.get(cid, cid),
                    "to_id": cid,
                    "to_type": "Chapter",
                    "type": "BELONGS_TO",
                }
            )
    for p in problems:
        cid = p.get("chapter_id") or f"ch{int(p.get('chapter_num') or 0):02d}"
        edges.append(
            {
                "from": p["id"],
                "from_type": "Problem",
                "to": ch_name.get(cid, cid),
                "to_id": cid,
                "to_type": "Chapter",
                "type": "BELONGS_TO",
            }
        )
    return edges


def write_review(
    concepts: list[dict],
    tests: list[dict],
    problems: list[dict],
    path: Path,
) -> None:
    uncovered = []
    tested = {e["from"] for e in tests}
    for p in problems:
        if p["id"] not in tested:
            uncovered.append(p)

    lines = [
        "# 知识图谱 v0.1 审阅（Concept 精炼 + TESTS）",
        "",
        "## 汇总",
        "",
        f"- Concept 精炼后: **{len(concepts)}**（{dict(Counter(c.get('confidence') for c in concepts))}）",
        f"- TESTS 边: **{len(tests)}**（覆盖题目 {len(tested)}/{len(problems)}）",
        f"- 未挂知识点的题: **{len(uncovered)}**",
        f"- TESTS 置信度: {dict(Counter(e.get('confidence') for e in tests))}",
        "",
        "## Concept 精炼结果（按章）",
        "",
    ]
    by_ch: dict[int, list] = defaultdict(list)
    for c in concepts:
        by_ch[int(c.get("primary_chapter_num") or 0)].append(c)
    for n in sorted(by_ch):
        lines.append(f"### 第{n:02d}章（{len(by_ch[n])}）")
        for c in by_ch[n]:
            aliases = "/".join((c.get("aliases") or [])[:3])
            codes = ",".join(c.get("section_codes") or []) or "—"
            lines.append(f"- **{c['name']}** [{c.get('confidence')}] codes={codes} aliases={aliases}")
        lines.append("")

    lines.append("## TESTS 抽样（每章 8 条）")
    lines.append("")
    by_t: dict[int, list] = defaultdict(list)
    for e in tests:
        by_t[int(e.get("chapter_num") or 0)].append(e)
    for n in sorted(by_t):
        lines.append(f"### 第{n:02d}章")
        for e in by_t[n][:8]:
            lines.append(
                f"- `{e['from']}` ({e.get('problem_kind')}) → **{e['to']}**  "
                f"score={e['score']} conf={e['confidence']} evid={e['evidence']}"
            )
        lines.append("")

    lines.append("## 未覆盖题目抽样（每章最多 5）")
    lines.append("")
    by_u: dict[int, list] = defaultdict(list)
    for p in uncovered:
        by_u[int(p.get("chapter_num") or 0)].append(p)
    for n in sorted(by_u):
        lines.append(f"### 第{n:02d}章")
        for p in by_u[n][:5]:
            lines.append(f"- `{p['id']}` ({p.get('kind')}): {(p.get('stem_preview') or '')[:80]}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def self_check(
    problems: list[dict],
    concepts: list[dict],
    tests: list[dict],
    belongs: list[dict],
) -> dict:
    """覆盖率 / 一致性自检。"""
    prob_ids = {p["id"] for p in problems}
    concept_names = {c["name"] for c in concepts}
    tested = {e["from"] for e in tests}
    uncovered = [p for p in problems if p["id"] not in tested]

    issues: list[str] = []
    # TESTS 指向存在的题与概念
    bad_from = [e for e in tests if e["from"] not in prob_ids]
    bad_to = [e for e in tests if e["to"] not in concept_names]
    if bad_from:
        issues.append(f"TESTS.from 无效: {len(bad_from)}")
    if bad_to:
        issues.append(f"TESTS.to 无效: {len(bad_to)}")

    # 每题 TESTS 数量
    per = Counter(e["from"] for e in tests)
    over = sum(1 for _, n in per.items() if n > 4)
    if over:
        issues.append(f"单题 TESTS>4: {over}")

    # 同章约束：TESTS 边 chapter 应一致（force/白名单跨章单独计数，不阻断 pass）
    concept_ch = {c["name"]: set(c.get("chapter_ids") or []) for c in concepts}
    cross = 0
    cross_ids = []
    for e in tests:
        if e.get("evidence") == "force_map":
            continue
        pid = e["from"]
        p = next((x for x in problems if x["id"] == pid), None)
        if not p:
            continue
        want = f"ch{int(p.get('chapter_num') or 0):02d}"
        if want not in concept_ch.get(e["to"], set()):
            cross += 1
            cross_ids.append(f"{pid}->{e['to']}")
    if cross:
        issues.append(f"跨章 TESTS(非force): {cross} {cross_ids[:5]}")

    cover_by_kind = {}
    kinds = Counter(p["kind"] for p in problems)
    covered_kind: dict[str, set] = defaultdict(set)
    for e in tests:
        covered_kind[str(e.get("problem_kind"))].add(e["from"])
    for k, n in kinds.items():
        cover_by_kind[k] = {"covered": len(covered_kind.get(k, ())), "total": n}

    report = {
        "problems": len(problems),
        "concepts": len(concepts),
        "tests": len(tests),
        "belongs_to": len(belongs),
        "coverage": {
            "problems": f"{len(tested)}/{len(problems)}",
            "rate": round(len(tested) / max(len(problems), 1), 4),
            "by_kind": cover_by_kind,
        },
        "uncovered_count": len(uncovered),
        "uncovered_ids": [p["id"] for p in uncovered],
        "tests_by_confidence": dict(Counter(e.get("confidence") for e in tests)),
        "evidence_has_figure": sum(1 for e in tests if "figure:" in (e.get("evidence") or "")),
        "evidence_has_alias": sum(1 for e in tests if "alias:" in (e.get("evidence") or "")),
        "evidence_has_section": sum(1 for e in tests if "section:" in (e.get("evidence") or "")),
        "issues": issues,
        "pass": len(uncovered) == 0 and not bad_from and not bad_to,
        "pass_soft": len(uncovered) <= 5 and not bad_from and not bad_to and cross == 0,
    }
    return report


def main() -> None:
    chapters = load_json(KG / "entities_chapters.json")
    problems = load_jsonl(KG / "entities_problems.jsonl")
    raw_concepts = load_json(KG / "entities_concepts.json")

    concepts = refine_concepts(raw_concepts)
    enrich_problem_stems(problems)
    tests = build_tests(problems, concepts)
    belongs = build_belongs_to(chapters, concepts, problems)

    (KG / "concepts_refined.json").write_text(
        json.dumps(concepts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (KG / "relationships_tests.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in tests) + "\n", encoding="utf-8"
    )
    (KG / "relationships_belongs_to.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in belongs) + "\n", encoding="utf-8"
    )

    # 兼容旧 path API 的概念图 + 完整 v0.1
    path_nodes = {c["name"]: {"id": c["id"], "chapter": next((ch["name"] for ch in chapters if ch["id"] in c["chapter_ids"]), "")} for c in concepts}
    graph = {
        "version": "0.1",
        "nodes": {
            "Chapter": chapters,
            "Concept": concepts,
            "Problem": problems,
        },
        "edges": {
            "TESTS": tests,
            "BELONGS_TO": belongs,
            "PRE_REQUISITE_OF": [],  # 下一步再做
        },
        # 供现有 graph_kg 过渡（仅概念名）
        "path_compat": {
            "nodes": path_nodes,
            "edges": [],
        },
        "stats": {
            "concepts": len(concepts),
            "problems": len(problems),
            "tests": len(tests),
            "tests_cover_problems": len({e["from"] for e in tests}),
            "belongs_to": len(belongs),
            "tests_by_confidence": dict(Counter(e.get("confidence") for e in tests)),
            "concepts_by_confidence": dict(Counter(c.get("confidence") for c in concepts)),
        },
    }
    (KG / "knowledge_graph_v0.1.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_review(concepts, tests, problems, KG / "kg_v0.1_review.md")

    # SIMILAR_TO：本章内共享 high/medium 知识点
    concept_of: dict[str, set[str]] = defaultdict(set)
    for e in tests:
        if e.get("confidence") in {"high", "medium"}:
            concept_of[e["from"]].add(e["to"])
    prob_map = {p["id"]: p for p in problems}
    similar: list[dict] = []
    ids = [i for i in concept_of if i in prob_map]
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            if prob_map[a].get("chapter_num") != prob_map[b].get("chapter_num"):
                continue
            shared = concept_of[a] & concept_of[b]
            if not shared:
                continue
            score = float(len(shared))
            if prob_map[a].get("kind") != prob_map[b].get("kind"):
                score += 0.5
            if len(shared) >= 2 or score >= 1.5:
                similar.append(
                    {
                        "from": a,
                        "to": b,
                        "type": "SIMILAR_TO",
                        "shared": sorted(shared),
                        "score": score,
                    }
                )
    similar.sort(key=lambda x: -x["score"])
    similar = similar[:2000]
    (KG / "relationships_similar.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in similar) + ("\n" if similar else ""),
        encoding="utf-8",
    )
    graph["edges"]["SIMILAR_TO"] = similar
    graph["stats"]["similar_to"] = len(similar)

    audit = self_check(problems, concepts, tests, belongs)
    audit["similar_to"] = len(similar)
    graph["stats"]["audit_pass"] = audit["pass"]
    graph["stats"]["uncovered_count"] = audit["uncovered_count"]
    (KG / "kg_tests_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (KG / "knowledge_graph_v0.1.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 刷新审阅中的未覆盖列表
    write_review(concepts, tests, problems, KG / "kg_v0.1_review.md")

    print(json.dumps(graph["stats"], ensure_ascii=False, indent=2))
    print("\n=== 自检 ===")
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    print(f"\n审阅: {KG / 'kg_v0.1_review.md'}")
    print(f"自检: {KG / 'kg_tests_audit.json'}")
    print(f"图谱: {KG / 'knowledge_graph_v0.1.json'}")


if __name__ == "__main__":
    main()
