#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建 Concept 间 PRE_REQUISITE_OF，并导出供路径 API 使用的兼容图。

输入：data/kg/knowledge_graph_v0.1.json
输出：
  - relationships_prereq.jsonl
  - knowledge_graph_v0.2.json（含前置）
  - path_graph.json（graph_kg / ingest_graph 用）
  - kg_prereq_review.md

用法:
  python data/build_kg_prereqs.py
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KG = ROOT / "data" / "kg"
SRC = KG / "knowledge_graph_v0.1.json"

# 跨章/跨主题人工前置（from 是 to 的前置）。
# 原则：只录「教学上明确的主干依赖」，不为降低孤立率硬凑叶子概念。
CURATED: list[tuple[str, str]] = [
    # 数制 → 逻辑
    ("二进制算术运算", "反码、补码和补码运算"),
    ("反码、补码和补码运算", "逻辑代数中的三种基本运算"),
    # 逻辑代数主干
    ("逻辑代数中的三种基本运算", "异或与同或"),
    ("逻辑代数中的三种基本运算", "基本公式"),
    ("基本公式", "代入定理"),
    ("基本公式", "反演定理"),
    ("基本公式", "对偶定理"),
    ("逻辑代数中的三种基本运算", "逻辑函数"),
    ("逻辑函数", "逻辑函数的描述方法"),
    ("逻辑函数的描述方法", "逻辑函数的两种标准形式"),
    ("逻辑函数的两种标准形式", "最小项与最大项"),
    ("逻辑函数的两种标准形式", "公式化简"),
    ("基本公式", "公式化简"),
    ("公式化简", "卡诺图"),
    ("逻辑函数的两种标准形式", "卡诺图"),
    ("卡诺图", "奎恩-麦克拉斯基化简法 (Q-M 法)"),
    ("卡诺图", "约束项、任意项和逻辑函数式中的无关项"),
    ("约束项、任意项和逻辑函数式中的无关项", "无关项在化简逻辑函数中"),
    ("卡诺图", "多输出逻辑函数的化简"),
    ("卡诺图", "逻辑函数形式的变换"),
    # 门电路主干
    ("MOS 管的开关特性", "CMOS反相器"),
    ("CMOS反相器", "CMOS数字集成电路"),
    ("二极管与门", "TTL"),
    ("CMOS反相器", "漏极开路输出(OD)"),
    ("TTL", "集电极开路输出(OC)"),
    ("CMOS反相器", "三态输出"),
    # 组合逻辑主干
    ("逻辑代数中的三种基本运算", "组合逻辑电路"),
    ("卡诺图", "组合逻辑电路设计"),
    ("组合逻辑电路", "组合逻辑电路设计"),
    ("组合逻辑电路", "编码器"),
    ("组合逻辑电路", "译码器"),
    ("组合逻辑电路", "数据选择器"),
    ("组合逻辑电路", "加法器"),
    ("组合逻辑电路", "数值比较器"),
    ("组合逻辑电路", "竞争-冒险现象"),
    ("竞争-冒险现象", "检查竞争-冒险现象"),
    ("组合逻辑电路设计", "硬件描述语言"),
    # 触发器 / 时序主干
    ("组合逻辑电路", "SR 锁存器"),
    ("SR 锁存器", "触发器"),
    ("触发器", "触发器按逻辑功能的分类"),
    ("触发器", "寄存器"),
    ("触发器", "存储器"),
    ("存储器", "存储器容量的扩展"),
    ("组合逻辑电路", "时序逻辑与组合逻辑的区别"),
    ("触发器", "同步时序与异步时序"),
    ("同步时序与异步时序", "同步时序逻辑电路"),
    ("同步时序与异步时序", "异步时序逻辑电路"),
    ("触发器", "移位寄存器"),
    ("触发器", "计数器"),
    ("同步时序逻辑电路", "时序逻辑电路的自启动设计"),
    ("同步时序逻辑电路", "复杂时序逻辑电路的设计"),
    ("硬件描述语言", "用硬件描述语言 Verilog HDL 描述时序逻辑电路"),
    # 脉冲 / 555 主干
    ("触发器", "施密特触发电路"),
    ("施密特触发电路", "单稳态电路"),
    ("施密特触发电路", "多谐振荡电路"),
    ("555定时器的电路结构与功能", "用 555 定时器接成的施密特触发电路"),
    # DAC/ADC 主干（具体型别留给节序/题侧挂接，不强行全连）
    ("加法器", "D/A 转换器"),
    ("D/A 转换器", "权电阻网络 D/A 转换器"),
    ("D/A 转换器", "倒 T 形电阻网络 D/A 转换器"),
    ("D/A 转换器", "A/D 转换的基本原理"),
    ("A/D 转换的基本原理", "取样-保持电路"),
]


def load() -> dict:
    return json.loads(SRC.read_text(encoding="utf-8"))


def section_tuple(code: str) -> tuple[int, ...]:
    parts = []
    for p in (code or "").split("."):
        if p.isdigit():
            parts.append(int(p))
    return tuple(parts)


def pick_hub(concepts: list[dict]) -> dict | None:
    if not concepts:
        return None
    # 优先 high/seed，名称更短
    def key(c: dict):
        conf = {"high": 0, "seed": 1, "medium": 2, "low_kept": 3}.get(str(c.get("confidence")), 9)
        return (conf, len(c.get("name") or ""), c.get("name") or "")

    return sorted(concepts, key=key)[0]


def build_section_prereqs(concepts: list[dict]) -> list[dict]:
    """章内：按 section 主号顺序，前一节 hub → 后一节 hub；节 hub → 同节细目。"""
    edges: list[dict] = []
    by_ch: dict[int, list[dict]] = defaultdict(list)
    for c in concepts:
        if c.get("skip_section_prereq"):
            continue
        if not c.get("section_codes"):
            continue
        if c.get("confidence") not in {"high", "seed", "medium"}:
            continue
        by_ch[int(c.get("primary_chapter_num") or 0)].append(c)

    for ch, items in by_ch.items():
        # major key = first two components (e.g. 2.6)
        buckets: dict[tuple[int, ...], list[dict]] = defaultdict(list)
        for c in items:
            code = c["section_codes"][0]
            t = section_tuple(code)
            if not t:
                continue
            major = t[:2] if len(t) >= 2 else t
            buckets[major].append(c)

        majors = sorted(buckets.keys())
        hubs = {m: pick_hub(buckets[m]) for m in majors}
        for a, b in zip(majors, majors[1:]):
            ha, hb = hubs[a], hubs[b]
            if ha and hb and ha["name"] != hb["name"]:
                edges.append(
                    {
                        "from": ha["name"],
                        "to": hb["name"],
                        "type": "PRE_REQUISITE_OF",
                        "confidence": "medium",
                        "evidence": f"section_order:ch{ch:02d}:{'.'.join(map(str,a))}→{'.'.join(map(str,b))}",
                    }
                )
        # hub → 同节其他概念
        for m, lst in buckets.items():
            hub = hubs[m]
            if not hub:
                continue
            for c in lst:
                if c["name"] == hub["name"]:
                    continue
                edges.append(
                    {
                        "from": hub["name"],
                        "to": c["name"],
                        "type": "PRE_REQUISITE_OF",
                        "confidence": "low",
                        "evidence": f"section_hub:ch{ch:02d}:{'.'.join(map(str,m))}",
                    }
                )
    return edges


def resolve_name(name: str, by_name: dict[str, dict], by_alias: dict[str, dict]) -> str | None:
    if name in by_name:
        return name
    if name in by_alias:
        return by_alias[name]["name"]
    # 仅允许「查询名是概念名的前缀/别名」的唯一命中，避免长名被收成短名
    hits = [c["name"] for c in by_name.values() if c["name"].startswith(name) or name == c["name"]]
    if len(hits) == 1:
        return hits[0]
    return None


def build_curated(concepts: list[dict]) -> list[dict]:
    by_name = {c["name"]: c for c in concepts}
    by_alias: dict[str, dict] = {}
    for c in concepts:
        for a in c.get("aliases") or []:
            by_alias.setdefault(a, c)
    edges = []
    for frm, to in CURATED:
        f = resolve_name(frm, by_name, by_alias)
        t = resolve_name(to, by_name, by_alias)
        if not f or not t or f == t:
            continue
        edges.append(
            {
                "from": f,
                "to": t,
                "type": "PRE_REQUISITE_OF",
                "confidence": "high",
                "evidence": "curated",
            }
        )
    return edges


def dedupe_edges(edges: list[dict]) -> list[dict]:
    best: dict[tuple[str, str], dict] = {}
    rank = {"high": 0, "medium": 1, "low": 2}
    for e in edges:
        key = (e["from"], e["to"])
        if key not in best or rank.get(e.get("confidence", "low"), 9) < rank.get(best[key].get("confidence", "low"), 9):
            best[key] = e
    # 去自环
    return [e for e in best.values() if e["from"] != e["to"]]


def has_cycle(edges: list[dict]) -> list[str]:
    graph: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        graph[e["from"]].append(e["to"])
    visiting, done = set(), set()
    cycles = []

    def dfs(u: str, stack: list[str]) -> None:
        visiting.add(u)
        stack.append(u)
        for v in graph.get(u, []):
            if v in visiting:
                cycles.append(" → ".join(stack[stack.index(v) :] + [v]))
            elif v not in done:
                dfs(v, stack)
        stack.pop()
        visiting.discard(u)
        done.add(u)

    for n in list(graph):
        if n not in done:
            dfs(n, [])
    return cycles


def ancestors(target: str, edges: list[dict], limit: int = 20) -> list[str]:
    """返回 target 的全部前置（BFS，from→to 表示 from 是 to 的前置）。"""
    rev: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        rev[e["to"]].append(e["from"])
    seen = set()
    order = []
    q = deque([target])
    while q and len(order) < limit:
        cur = q.popleft()
        for p in rev.get(cur, []):
            if p not in seen and p != target:
                seen.add(p)
                order.append(p)
                q.append(p)
    return order


def topo_path(target: str, edges: list[dict]) -> list[str]:
    """前置拓扑序 + target。"""
    pre = ancestors(target, edges)
    if not pre:
        return [target]
    # Kahn on subgraph
    nodes = set(pre) | {target}
    indeg = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        if e["from"] in nodes and e["to"] in nodes:
            adj[e["from"]].append(e["to"])
            indeg[e["to"]] += 1
    q = deque([n for n, d in indeg.items() if d == 0])
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if target not in out:
        out.append(target)
    # 仅保留通向 target 的链：简单截到 target
    if target in out:
        out = out[: out.index(target) + 1]
    return out


def to_path_compat(concepts: list[dict], prereqs: list[dict], chapters: list[dict]) -> dict:
    ch_map = {c["id"]: c["name"] for c in chapters}
    nodes = {}
    for c in concepts:
        ch = ""
        for cid in c.get("chapter_ids") or []:
            ch = ch_map.get(cid, cid)
            break
        nodes[c["name"]] = {"id": c["id"], "chapter": ch, "chapter_ids": c.get("chapter_ids") or []}
    edges = [
        {
            "from": e["from"],
            "to": e["to"],
            "type": "PRE_REQUISITE_OF",
            "confidence": e.get("confidence", "medium"),
            "evidence": e.get("evidence", ""),
        }
        for e in prereqs
    ]
    return {"nodes": nodes, "edges": edges}


def write_review(prereqs: list[dict], concepts: list[dict], path: Path) -> None:
    lines = [
        "# 知识图谱前置关系审阅（PRE_REQUISITE_OF）",
        "",
        f"- 前置边: **{len(prereqs)}**",
        f"- 置信度: {dict(Counter(e.get('confidence') for e in prereqs))}",
        f"- 证据: {dict(Counter((e.get('evidence') or '').split(':')[0] for e in prereqs))}",
        "",
        "## 人工 curated 抽样",
        "",
    ]
    for e in [x for x in prereqs if x.get("evidence") == "curated"][:40]:
        lines.append(f"- **{e['from']}** → {e['to']}")
    lines.append("")
    lines.append("## 路径示例")
    lines.append("")
    samples = ["卡诺图", "触发器", "计数器", "D/A 转换器", "竞争-冒险现象"]
    name_set = {c["name"] for c in concepts}
    for s in samples:
        if s not in name_set:
            continue
        path_nodes = topo_path(s, prereqs)
        lines.append(f"- `{s}`: {' → '.join(path_nodes)}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    g = load()
    concepts = g["nodes"]["Concept"]
    chapters = g["nodes"]["Chapter"]

    section_edges = build_section_prereqs(concepts)
    curated_edges = build_curated(concepts)
    prereqs = dedupe_edges(section_edges + curated_edges)

    cycles = has_cycle(prereqs)
    # 若有环，丢掉 low 节 hub 边再试
    if cycles:
        prereqs = dedupe_edges([e for e in prereqs if not str(e.get("evidence", "")).startswith("section_hub")] + curated_edges)
        cycles = has_cycle(prereqs)

    (KG / "relationships_prereq.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in prereqs) + "\n", encoding="utf-8"
    )

    g2 = json.loads(json.dumps(g, ensure_ascii=False))  # copy
    g2["version"] = "0.2"
    g2["edges"]["PRE_REQUISITE_OF"] = prereqs
    path_compat = to_path_compat(concepts, prereqs, chapters)
    g2["path_compat"] = path_compat
    g2["stats"]["prereq"] = len(prereqs)
    g2["stats"]["prereq_by_confidence"] = dict(Counter(e.get("confidence") for e in prereqs))
    g2["stats"]["prereq_cycles"] = len(cycles)

    (KG / "knowledge_graph_v0.2.json").write_text(
        json.dumps(g2, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (KG / "path_graph.json").write_text(
        json.dumps(path_compat, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_review(prereqs, concepts, KG / "kg_prereq_review.md")

    audit = {
        "prereq_edges": len(prereqs),
        "curated": sum(1 for e in prereqs if e.get("evidence") == "curated"),
        "section_order": sum(1 for e in prereqs if str(e.get("evidence", "")).startswith("section_order")),
        "section_hub": sum(1 for e in prereqs if str(e.get("evidence", "")).startswith("section_hub")),
        "cycles": cycles[:5],
        "concepts_in_path_graph": len(path_compat["nodes"]),
        "sample_paths": {
            s: topo_path(s, prereqs)
            for s in ["卡诺图", "触发器", "计数器", "D/A 转换器"]
            if s in path_compat["nodes"]
        },
        "pass": len(cycles) == 0 and len(prereqs) >= 30,
    }
    (KG / "kg_prereq_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    print(f"\n审阅: {KG / 'kg_prereq_review.md'}")
    print(f"图谱: {KG / 'knowledge_graph_v0.2.json'}")
    print(f"路径图: {KG / 'path_graph.json'}")


if __name__ == "__main__":
    main()
