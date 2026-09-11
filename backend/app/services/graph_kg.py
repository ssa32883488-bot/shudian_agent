"""知识图谱查询——路径、考点匹配、题↔概念、刷题计划。"""

from __future__ import annotations

import json
import re
from collections import defaultdict, deque
from functools import lru_cache
from pathlib import Path
from typing import Any

BACKEND = Path(__file__).resolve().parents[2]
ROOT = BACKEND.parent
CANDIDATES = [
    BACKEND / "data" / "knowledge_graph.json",
    ROOT / "data" / "kg" / "path_graph.json",
    ROOT / "data" / "kg" / "knowledge_graph_v0.2.json",
    ROOT / "data" / "sample" / "knowledge_graph.json",
]
FULL_GRAPH_CANDIDATES = [
    ROOT / "data" / "kg" / "knowledge_graph_v0.2.json",
    ROOT / "data" / "kg" / "knowledge_graph_v0.1.json",
]

# 及格向：优先主干概念（覆盖核心章）
PASS_FOCUS = [
    "逻辑代数中的三种基本运算",
    "逻辑函数的两种标准形式",
    "卡诺图",
    "组合逻辑电路",
    "编码器",
    "译码器",
    "加法器",
    "触发器",
    "寄存器",
    "计数器",
    "D/A 转换器",
    "A/D 转换的基本原理",
]


def _normalize_graph(raw: dict) -> dict:
    """统一为 {nodes: {name: meta}, edges: [{from,to,type,confidence?}]}。"""
    if "path_compat" in raw and isinstance(raw["path_compat"], dict):
        raw = raw["path_compat"]

    nodes = raw.get("nodes") or {}
    edges = raw.get("edges") or []

    if isinstance(nodes, dict) and nodes and isinstance(next(iter(nodes.values()), None), list):
        concept_list = nodes.get("Concept") or []
        norm_nodes = {}
        for c in concept_list:
            name = c.get("name")
            if not name:
                continue
            ch = ""
            ids = c.get("chapter_ids") or []
            if ids:
                ch = ids[0]
            norm_nodes[name] = {"id": c.get("id"), "chapter": ch}
        prereq = edges.get("PRE_REQUISITE_OF") if isinstance(edges, dict) else []
        return {
            "nodes": norm_nodes,
            "edges": [
                {
                    "from": e["from"],
                    "to": e["to"],
                    "type": "PRE_REQUISITE_OF",
                    "confidence": e.get("confidence", "medium"),
                }
                for e in (prereq or [])
            ],
        }

    if isinstance(edges, dict):
        edges = edges.get("PRE_REQUISITE_OF") or []
    return {"nodes": nodes, "edges": edges}


@lru_cache(maxsize=1)
def _load_graph() -> dict:
    neo = _load_path_graph_from_neo4j()
    if neo is not None:
        return neo
    for path in CANDIDATES:
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            g = _normalize_graph(raw)
            g["_source"] = str(path)
            g["_engine"] = "json"
            return g
    return {
        "nodes": {
            "卡诺图": {"chapter": "第4章"},
            "逻辑代数": {"chapter": "第2章"},
            "组合逻辑": {"chapter": "第3章"},
            "时序逻辑": {"chapter": "第5章"},
            "D触发器": {"chapter": "第5章"},
        },
        "edges": [
            {"from": "逻辑代数", "to": "卡诺图", "type": "PRE_REQUISITE_OF"},
            {"from": "逻辑代数", "to": "组合逻辑", "type": "PRE_REQUISITE_OF"},
            {"from": "组合逻辑", "to": "时序逻辑", "type": "PRE_REQUISITE_OF"},
            {"from": "时序逻辑", "to": "D触发器", "type": "PRE_REQUISITE_OF"},
        ],
        "_source": "builtin_fallback",
        "_engine": "builtin",
    }


@lru_cache(maxsize=1)
def _load_full_graph() -> dict[str, Any]:
    neo = _load_full_graph_from_neo4j()
    if neo is not None:
        return neo
    for path in FULL_GRAPH_CANDIDATES:
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["_source"] = str(path)
            raw["_engine"] = "json"
            return raw
    return {"nodes": {}, "edges": {}, "_source": "empty", "_engine": "empty"}


def _load_path_graph_from_neo4j() -> dict | None:
    try:
        from app.config import get_settings
        from app.services.neo4j_client import is_neo4j_ready, run_cypher

        if not get_settings().neo4j_enabled or not is_neo4j_ready():
            return None
        concepts = run_cypher(
            "MATCH (c:Concept) RETURN c.name AS name, c.chapter_ids AS chapter_ids"
        )
        if not concepts:
            return None
        edges = run_cypher(
            """
            MATCH (a:Concept)-[r:PRE_REQUISITE_OF]->(b:Concept)
            RETURN a.name AS `from`, b.name AS `to`,
                   coalesce(r.confidence, 'medium') AS confidence
            """
        )
        nodes = {}
        for c in concepts:
            name = c.get("name")
            if not name:
                continue
            ch_ids = list(c.get("chapter_ids") or [])
            ch = ch_ids[0] if ch_ids else ""
            nodes[name] = {"chapter": ch, "chapter_ids": ch_ids}
        return {
            "nodes": nodes,
            "edges": [
                {
                    "from": e["from"],
                    "to": e["to"],
                    "type": "PRE_REQUISITE_OF",
                    "confidence": e.get("confidence") or "medium",
                }
                for e in edges
                if e.get("from") and e.get("to")
            ],
            "_source": "neo4j",
            "_engine": "neo4j",
        }
    except Exception:
        return None


def _load_full_graph_from_neo4j() -> dict[str, Any] | None:
    try:
        from app.config import get_settings
        from app.services.neo4j_client import is_neo4j_ready, run_cypher

        if not get_settings().neo4j_enabled or not is_neo4j_ready():
            return None

        concept_rows = run_cypher(
            """
            MATCH (c:Concept)
            RETURN c.id AS id, c.name AS name, c.aliases AS aliases,
                   c.chapter_ids AS chapter_ids,
                   c.primary_chapter_num AS primary_chapter_num,
                   c.confidence AS confidence
            """
        )
        if not concept_rows:
            return None

        problem_rows = run_cypher(
            """
            MATCH (p:Problem)
            RETURN p.id AS id, p.kind AS kind, p.stem AS stem,
                   p.chapter_id AS chapter_id
            """
        )
        chapter_rows = run_cypher(
            "MATCH (ch:Chapter) RETURN ch.id AS id, ch.name AS name, ch.num AS num"
        )
        prereq = run_cypher(
            """
            MATCH (a:Concept)-[r:PRE_REQUISITE_OF]->(b:Concept)
            RETURN a.name AS `from`, b.name AS `to`,
                   coalesce(r.confidence,'medium') AS confidence,
                   coalesce(r.evidence,'') AS evidence
            """
        )
        tests = run_cypher(
            """
            MATCH (p:Problem)-[r:TESTS]->(c:Concept)
            RETURN p.id AS `from`, c.name AS `to`,
                   coalesce(r.confidence,'') AS confidence,
                   coalesce(r.evidence,'') AS evidence
            """
        )
        belongs = run_cypher(
            """
            MATCH (n)-[:BELONGS_TO]->(ch:Chapter)
            RETURN coalesce(n.name, n.id) AS `from`, ch.id AS `to`
            """
        )
        similar = run_cypher(
            """
            MATCH (a:Problem)-[r:SIMILAR_TO]->(b:Problem)
            RETURN a.id AS `from`, b.id AS `to`,
                   coalesce(r.score, 0.0) AS score,
                   coalesce(r.shared, '') AS shared
            """
        )

        concepts = []
        for c in concept_rows:
            concepts.append(
                {
                    "id": c.get("id") or c.get("name"),
                    "type": "Concept",
                    "name": c.get("name"),
                    "aliases": list(c.get("aliases") or []),
                    "chapter_ids": list(c.get("chapter_ids") or []),
                    "primary_chapter_num": int(c.get("primary_chapter_num") or 0),
                    "confidence": c.get("confidence") or "",
                }
            )
        problems = []
        for p in problem_rows:
            problems.append(
                {
                    "id": p.get("id"),
                    "type": "Problem",
                    "kind": p.get("kind") or "",
                    "stem_preview": (p.get("stem") or "")[:160],
                    "stem_full": p.get("stem") or "",
                    "chapter_id": p.get("chapter_id") or "",
                }
            )
        chapters = [
            {
                "id": ch.get("id"),
                "type": "Chapter",
                "name": ch.get("name") or ch.get("id"),
                "num": int(ch.get("num") or 0),
            }
            for ch in chapter_rows
        ]

        return {
            "nodes": {
                "Chapter": chapters,
                "Concept": concepts,
                "Problem": problems,
            },
            "edges": {
                "PRE_REQUISITE_OF": [
                    {
                        "from": e["from"],
                        "to": e["to"],
                        "type": "PRE_REQUISITE_OF",
                        "confidence": e.get("confidence"),
                        "evidence": e.get("evidence"),
                    }
                    for e in prereq
                ],
                "TESTS": [
                    {
                        "from": e["from"],
                        "to": e["to"],
                        "type": "TESTS",
                        "confidence": e.get("confidence"),
                        "evidence": e.get("evidence"),
                    }
                    for e in tests
                ],
                "BELONGS_TO": [
                    {"from": e["from"], "to": e["to"], "type": "BELONGS_TO"}
                    for e in belongs
                ],
                "SIMILAR_TO": [
                    {
                        "from": e["from"],
                        "to": e["to"],
                        "type": "SIMILAR_TO",
                        "score": e.get("score"),
                        "shared": e.get("shared"),
                    }
                    for e in similar
                ],
            },
            "_source": "neo4j",
            "_engine": "neo4j",
        }
    except Exception:
        return None


def reload_graphs() -> None:
    _load_graph.cache_clear()
    _load_full_graph.cache_clear()
    _alias_index.cache_clear()


def _resolve_concept(name: str, nodes: dict) -> str | None:
    if name in nodes:
        return name
    hits = [n for n in nodes if name in n or n in name]
    if len(hits) == 1:
        return hits[0]
    compact = name.replace(" ", "")
    for n in nodes:
        if n.replace(" ", "") == compact:
            return n
    return None


def _prereq_closure(target: str, edges: list[dict], limit: int = 30) -> list[str]:
    rev: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        if e.get("type", "PRE_REQUISITE_OF") == "PRE_REQUISITE_OF":
            rev[e["to"]].append(e["from"])
    seen: set[str] = set()
    order: list[str] = []
    q = deque([target])
    while q and len(order) < limit:
        cur = q.popleft()
        for p in rev.get(cur, []):
            if p not in seen and p != target:
                seen.add(p)
                order.append(p)
                q.append(p)
    return order


def _topo_path(target: str, prereqs: list[str], edges: list[dict]) -> list[str]:
    nodes = set(prereqs) | {target}
    indeg = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        if e.get("type", "PRE_REQUISITE_OF") != "PRE_REQUISITE_OF":
            continue
        u, v = e["from"], e["to"]
        if u in nodes and v in nodes:
            adj[u].append(v)
            indeg[v] += 1
    q = deque([n for n, d in indeg.items() if d == 0])
    out: list[str] = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if target in out:
        return out[: out.index(target) + 1]
    return [p for p in out if p != target] + [target]


def recommend_path(concept: str) -> dict:
    g = _load_graph()
    nodes = g.get("nodes") or {}
    edges = g.get("edges") or []
    resolved = _resolve_concept(concept, nodes)
    if not resolved:
        return {
            "target": concept,
            "resolved": None,
            "missing_prerequisites": [],
            "path": [concept],
            "suggestion": f"未找到知识点「{concept}」，请换一个概念名（如：卡诺图、触发器）",
            "source": g.get("_source"),
        }

    high_edges = [
        e
        for e in edges
        if e.get("type", "PRE_REQUISITE_OF") == "PRE_REQUISITE_OF"
        and e.get("confidence", "high") in {"high", None, ""}
    ]
    if not high_edges:
        high_edges = edges

    prereqs_all = _prereq_closure(resolved, edges)
    prereqs_high = _prereq_closure(resolved, high_edges)
    path = _topo_path(resolved, prereqs_high, high_edges)
    if len(path) > 10:
        direct = [e["from"] for e in high_edges if e.get("to") == resolved]
        path = direct + [resolved] if direct else path[-8:]
    direct = [e["from"] for e in edges if e.get("to") == resolved]
    return {
        "target": concept,
        "resolved": resolved,
        "direct_prerequisites": direct,
        "missing_prerequisites": prereqs_high or prereqs_all,
        "all_prerequisites": prereqs_all,
        "path": path,
        "suggestion": (
            f"建议学习路径：{' → '.join(path)}" if len(path) > 1 else "前置知识已具备或暂无录入前置边"
        ),
        "source": g.get("_source"),
    }


def list_concepts() -> list[str]:
    return sorted((_load_graph().get("nodes") or {}).keys())


@lru_cache(maxsize=1)
def _alias_index() -> list[tuple[str, str, int]]:
    """[(alias_lower_or_raw, concept_name, len)] 按别名长度降序，便于最长匹配。"""
    g = _load_full_graph()
    concepts = (g.get("nodes") or {}).get("Concept") or []
    items: list[tuple[str, str, int]] = []
    seen: set[tuple[str, str]] = set()
    for c in concepts:
        name = c.get("name") or ""
        if not name:
            continue
        aliases = list(dict.fromkeys([name, *(c.get("aliases") or [])]))
        for a in aliases:
            a = (a or "").strip()
            if len(a) < 2:
                continue
            key = (a, name)
            if key in seen:
                continue
            seen.add(key)
            items.append((a, name, len(a)))
    items.sort(key=lambda x: -x[2])
    return items


def match_concepts_from_text(text: str, top_k: int = 8) -> list[dict[str, Any]]:
    """从题面/大纲文本抽取知识点关键词（最长别名优先，去重）。"""
    if not (text or "").strip():
        return []
    hits: dict[str, dict[str, Any]] = {}
    for alias, name, alen in _alias_index():
        if alias not in text:
            continue
        prev = hits.get(name)
        score = alen + (2 if alias == name else 0)
        if not prev or score > prev["score"]:
            hits[name] = {"name": name, "matched": alias, "score": score}
    ranked = sorted(hits.values(), key=lambda x: -x["score"])
    return ranked[:top_k]


def _concept_name_to_id() -> dict[str, str]:
    g = _load_full_graph()
    concepts = (g.get("nodes") or {}).get("Concept") or []
    out: dict[str, str] = {}
    for c in concepts:
        name = (c.get("name") or "").strip()
        cid = (c.get("id") or "").strip()
        if name and cid:
            out[name] = cid
    return out


def resolve_knowledge_tags(
    raw_tags: list[str] | None = None,
    *,
    stem: str = "",
    source: str = "memory_summary",
) -> dict[str, Any]:
    """自由文本标签 + 题干 → 规范 tags / concept_ids；映射不上的原文保留在 tags。"""
    raw = [str(t).strip() for t in (raw_tags or []) if str(t).strip()][:8]
    blob_parts = list(raw)
    if (stem or "").strip():
        blob_parts.append(stem.strip()[:2000])
    blob = "\n".join(blob_parts)

    matched = match_concepts_from_text(blob, top_k=8) if blob.strip() else []
    name_to_id = _concept_name_to_id()

    tags: list[str] = []
    concept_ids: list[str] = []
    seen_names: set[str] = set()
    seen_ids: set[str] = set()
    matched_tokens: set[str] = set()

    for m in matched:
        name = str(m.get("name") or "").strip()
        alias = str(m.get("matched") or "").strip()
        if alias:
            matched_tokens.add(alias)
        if name:
            matched_tokens.add(name)
            if name not in seen_names:
                seen_names.add(name)
                tags.append(name)
            cid = name_to_id.get(name)
            if cid and cid not in seen_ids:
                seen_ids.add(cid)
                concept_ids.append(cid)

    for t in raw:
        if t in matched_tokens or t in seen_names:
            continue
        tags.append(t)

    return {
        "tags": tags[:12],
        "concept_ids": concept_ids[:12],
        "source": source,
        "raw_tags": raw,
    }


def concepts_for_problem(problem_id: str) -> list[str]:
    g = _load_full_graph()
    tests = (g.get("edges") or {}).get("TESTS") or []
    return [e["to"] for e in tests if e.get("from") == problem_id]


def problem_kind_label(kind: str | None, problem_id: str | None = None) -> str:
    """习题类型中文标签：例题 / 复习思考题 / 章末习题。"""
    k = (kind or "").strip().lower()
    if k in {"example", "例题", "eg", "ex"}:
        return "例题"
    if k in {"review", "复习", "复习思考题"}:
        return "复习思考题"
    if k in {"chapter_exercise", "exercise", "习题", "课后习题", "章末习题"}:
        return "章末习题"
    pid = str(problem_id or "")
    if pid.startswith("例"):
        return "例题"
    if pid.startswith("R"):
        return "复习思考题"
    if pid.startswith("题"):
        return "章末习题"
    return "习题"


def problems_for_concept(concept: str, limit: int = 20) -> list[dict[str, Any]]:
    """Concept → 相关习题（TESTS 反查）。"""
    g = _load_full_graph()
    nodes = (g.get("nodes") or {}).get("Concept") or []
    by_name = {c["name"]: c for c in nodes}
    resolved = concept if concept in by_name else None
    if not resolved:
        for c in nodes:
            aliases = c.get("aliases") or []
            if concept in aliases or concept in (c.get("name") or ""):
                resolved = c["name"]
                break
            if (c.get("name") or "") in concept:
                resolved = c["name"]
                break
    if not resolved:
        return []

    tests = (g.get("edges") or {}).get("TESTS") or []
    problems = {(p.get("id") or p.get("name")): p for p in ((g.get("nodes") or {}).get("Problem") or [])}
    out: list[dict[str, Any]] = []
    for e in tests:
        if e.get("to") != resolved:
            continue
        pid = e.get("from")
        meta = problems.get(pid) or {}
        kind = meta.get("kind")
        out.append(
            {
                "problem_id": pid,
                "kind": kind,
                "kind_label": problem_kind_label(kind, pid),
                "stem": (meta.get("stem_full") or meta.get("stem_preview") or meta.get("stem") or "")[:160],
                "chapter_id": meta.get("chapter_id"),
                "confidence": e.get("confidence"),
                "evidence": e.get("evidence"),
            }
        )
    conf_rank = {"high": 0, "medium": 1, "low": 2}
    kind_pref = {"example": 0, "review": 1, "chapter_exercise": 2}
    out.sort(
        key=lambda x: (
            kind_pref.get(str(x.get("kind")), 9),
            conf_rank.get(str(x.get("confidence")), 9),
            x.get("problem_id") or "",
        )
    )
    return out[:limit]


def find_similar_problems(problem_id: str, limit: int = 5) -> list[dict]:
    g = _load_full_graph()
    edges = (g.get("edges") or {}).get("SIMILAR_TO") or []
    out = []
    for e in edges:
        if e.get("from") == problem_id:
            out.append({"problem_id": e["to"], "shared": e.get("shared"), "score": e.get("score")})
        elif e.get("to") == problem_id:
            out.append({"problem_id": e["from"], "shared": e.get("shared"), "score": e.get("score")})
    out.sort(key=lambda x: -(x.get("score") or 0))
    return out[:limit]


def knowledge_network(
    *,
    text: str | None = None,
    concepts: list[str] | None = None,
    problem_id: str | None = None,
    top_k: int = 6,
    problems_per_concept: int = 3,
) -> dict[str, Any]:
    """复原知识点网络：关键词 + 前置路径 + 相关题 + 相似题。"""
    keywords = list(concepts or [])
    matched: list[dict[str, Any]] = []
    if text:
        matched = match_concepts_from_text(text, top_k=top_k)
        for m in matched:
            if m["name"] not in keywords:
                keywords.append(m["name"])
    if problem_id:
        for c in concepts_for_problem(problem_id):
            if c not in keywords:
                keywords.append(c)

    keywords = keywords[:top_k]
    paths = []
    related_problems: list[dict[str, Any]] = []
    seen_p: set[str] = set()
    for name in keywords:
        path_info = recommend_path(name)
        paths.append(
            {
                "concept": name,
                "resolved": path_info.get("resolved"),
                "path": path_info.get("path") or [],
                "suggestion": path_info.get("suggestion"),
            }
        )
        for p in problems_for_concept(name, limit=problems_per_concept):
            pid = p["problem_id"]
            if pid in seen_p:
                continue
            seen_p.add(pid)
            related_problems.append(p)

    similar = find_similar_problems(problem_id, limit=5) if problem_id else []

    # 合并学习链：按首次出现顺序去重
    chain: list[str] = []
    for p in paths:
        for n in p.get("path") or []:
            if n not in chain:
                chain.append(n)

    prompt_block = _format_kg_prompt(keywords, chain, related_problems)
    return {
        "keywords": keywords,
        "matched": matched,
        "paths": paths,
        "learning_chain": chain,
        "related_problems": related_problems[:15],
        "similar_problems": similar,
        "prompt_block": prompt_block,
        "source": _load_full_graph().get("_source"),
    }


def _format_kg_prompt(
    keywords: list[str], chain: list[str], problems: list[dict[str, Any]]
) -> str:
    lines = ["【知识图谱依据】"]
    if keywords:
        lines.append("考点关键词：" + "、".join(keywords))
    if chain:
        lines.append("知识逻辑链：" + " → ".join(chain[:12]))
    if problems:
        bits = []
        for p in problems[:8]:
            label = p.get("kind_label") or problem_kind_label(p.get("kind"), p.get("problem_id"))
            bits.append(f"{label}·{p['problem_id']}")
        lines.append("相关习题：" + "、".join(bits))
    return "\n".join(lines)


def detect_intent(text: str, goal: str | None = None) -> str:
    """轻量意图识别：复杂多模态请求的分流标签。"""
    if goal:
        g = goal.lower().strip()
        if g in {"pass", "及格", "期末及格", "study_plan", "plan"}:
            return "study_plan"
        if g in {"syllabus", "大纲"}:
            return "syllabus"
        if g in {"full", "冲刺", "全覆盖"}:
            return "study_plan"
        if g in {"solve", "解题"}:
            return "solve"
        if g in {"explain", "讲解"}:
            return "explain"
    t = text or ""
    if any(k in t for k in ("大纲", "考试范围", "考点表", "教学进度", "复习提纲")):
        return "syllabus"
    if any(k in t for k in ("及格", "刷题", "练习题", "怎么学", "复习计划", "学习路径", "帮我筛选")):
        return "study_plan"
    if any(k in t for k in ("化简", "计算", "画出", "分析电路", "求输出", "写出逻辑", "填卡诺", "设计一个")):
        return "solve"
    if any(k in t for k in ("什么是", "区别", "原理", "如何理解", "讲解", "总结")):
        return "explain"
    return "mixed"


def find_problems_by_text(text: str, limit: int = 5) -> list[dict[str, Any]]:
    """题干关键词召回教材习题（多模态拍题/粘贴题面时用）。"""
    if not (text or "").strip():
        return []
    g = _load_full_graph()
    problems = (g.get("nodes") or {}).get("Problem") or []
    tests = (g.get("edges") or {}).get("TESTS") or []
    concepts_by_pid: dict[str, list[str]] = defaultdict(list)
    for e in tests:
        concepts_by_pid[e["from"]].append(e["to"])

    # 抽一点有辨识度的片段：连续汉字 / 字母数字
    compact = re.sub(r"\s+", "", text)
    tokens = re.findall(r"[\u4e00-\u9fff]{3,}|[A-Za-z][A-Za-z0-9\-_/]{2,}", compact)
    tokens = sorted(set(tokens), key=len, reverse=True)[:16]
    if not tokens:
        return []

    # 教材高频考点短词（即使不足 4 字）
    for kw in ("卡诺图", "触发器", "计数器", "译码器", "编码器", "加法器", "锁存器", "寄存器"):
        if kw in compact and kw not in tokens:
            tokens.append(kw)

    scored: list[tuple[int, dict]] = []
    for p in problems:
        stem = (p.get("stem_full") or p.get("stem_preview") or "")[:800]
        if not stem:
            continue
        stem_c = stem.replace(" ", "")
        hit = 0
        for tok in tokens:
            if tok in stem_c:
                hit += min(len(tok), 12)
        if hit < 4:
            continue
        pid = p.get("id") or ""
        scored.append(
            (
                hit,
                {
                    "problem_id": pid,
                    "kind": p.get("kind"),
                    "stem": stem[:160],
                    "chapter_id": p.get("chapter_id"),
                    "concepts": concepts_by_pid.get(pid, [])[:4],
                    "score": hit,
                },
            )
        )
    scored.sort(key=lambda x: -x[0])
    return [x[1] for x in scored[:limit]]


def assist_complex(
    *,
    text: str,
    goal: str | None = None,
    limit: int = 12,
) -> dict[str, Any]:
    """多模态复杂请求统一入口：文本/大纲/目标 → 意图 + 知识网 + 可选刷题计划。

    「及格冲刺」只是 study_plan 意图下的一种偏好，不是单独产品能力。
    """
    intent = detect_intent(text, goal)
    net = knowledge_network(text=text, top_k=8, problems_per_concept=4)
    similar_by_stem = find_problems_by_text(text, limit=5)

    # 若题面召回了教材题，用其 TESTS 补强关键词
    for sp in similar_by_stem:
        for c in sp.get("concepts") or []:
            if c not in net["keywords"]:
                net["keywords"].append(c)
        if sp["problem_id"] not in {p["problem_id"] for p in net.get("related_problems") or []}:
            net.setdefault("related_problems", []).insert(0, sp)

    practice = None
    if intent in {"study_plan", "syllabus"}:
        practice = practice_plan(
            text,
            goal=("pass" if intent == "study_plan" and (not goal or "大纲" not in (goal or "")) else (goal or intent)),
            limit=limit,
        )

    hints = {
        "solve": ["先点明考点关键词", "按知识逻辑链分步推导", "对照相关例题校验"],
        "explain": ["先给图谱位置与前置链", "再讲清概念", "附相关练习题号"],
        "study_plan": ["按学习链分阶段", "每阶段给例题+复习题", "最后用章末题自测"],
        "syllabus": ["按大纲命中概念排序", "补齐缺失前置", "输出可执行刷题清单"],
        "mixed": ["先澄清用户目标", "同时给出知识网与可练习题目"],
    }

    prompt = net.get("prompt_block") or ""
    if practice and practice.get("prompt_block"):
        prompt = prompt + "\n" + practice["prompt_block"]
    if similar_by_stem:
        prompt += "\n题面近邻习题：" + "、".join(p["problem_id"] for p in similar_by_stem[:5])

    return {
        "intent": intent,
        "keywords": net.get("keywords") or [],
        "learning_chain": net.get("learning_chain") or [],
        "knowledge_network": net,
        "similar_problems": similar_by_stem,
        "practice": practice,
        "reply_hints": hints.get(intent, hints["mixed"]),
        "prompt_block": prompt,
        "suggestion": (practice or {}).get("suggestion")
        or (
            f"识别为「{intent}」：考点 {'、'.join((net.get('keywords') or [])[:5])}"
            if net.get("keywords")
            else "未能从输入锚定足够考点，请补充题干/大纲片段"
        ),
        "source": net.get("source"),
    }


def practice_plan(
    text: str,
    *,
    goal: str = "pass",
    limit: int = 12,
) -> dict[str, Any]:
    """根据学习目标或考试大纲文本，筛选刷题路径与题目。

    goal:
      - pass / study_plan: 主干优先（及格向只是选题偏好）
      - syllabus: 完全按大纲命中概念
      - full: 大纲命中加宽
    """
    matched = match_concepts_from_text(text, top_k=20)
    from_text = [m["name"] for m in matched]

    goal_l = (goal or "pass").lower()
    if goal_l in {"pass", "及格", "期末及格", "study_plan", "plan"}:
        # 用户提到的概念优先，再用主干补齐——不硬塞无关章
        focus = list(from_text)
        for c in PASS_FOCUS:
            if c not in focus:
                focus.append(c)
        focus = focus[:10]
        mode = "study_plan"
    elif goal_l in {"full", "冲刺", "全覆盖"}:
        focus = from_text or list(PASS_FOCUS)[:8]
        mode = "full"
    else:
        focus = from_text or list(PASS_FOCUS)[:8]
        mode = "syllabus"

    chain: list[str] = []
    path_details = []
    for name in focus:
        info = recommend_path(name)
        path_details.append(info)
        for n in info.get("path") or []:
            if n not in chain:
                chain.append(n)

    # 章节配额：每章最多 ceil(limit/3)，避免刷题清单扎堆一章
    kind_pref = {"example": 0, "review": 1, "chapter_exercise": 2}
    per_chapter_cap = max(2, (limit + 2) // 3)
    chapter_count: dict[str, int] = defaultdict(int)
    picked: list[dict[str, Any]] = []
    seen: set[str] = set()
    pool: list[dict[str, Any]] = []
    for name in focus:
        for p in problems_for_concept(name, limit=10):
            pid = p["problem_id"]
            if pid in seen:
                continue
            seen.add(pid)
            pool.append({**p, "via_concept": name})
    pool.sort(
        key=lambda x: (
            kind_pref.get(str(x.get("kind")), 9),
            0 if x.get("confidence") == "high" else 1,
            x.get("problem_id") or "",
        )
    )
    for p in pool:
        ch = str(p.get("chapter_id") or "")
        if chapter_count[ch] >= per_chapter_cap:
            continue
        picked.append(p)
        chapter_count[ch] += 1
        if len(picked) >= limit:
            break

    label = {"study_plan": "目标导向刷题", "syllabus": "大纲刷题", "full": "加宽刷题"}.get(mode, "刷题")
    suggestion = (
        f"{label}建议顺序：{' → '.join(chain[:10])}"
        if chain
        else "暂未匹配到知识点，请提供更明确的大纲或目标概念"
    )
    return {
        "mode": mode,
        "goal": goal,
        "matched_concepts": from_text,
        "focus_concepts": focus,
        "learning_chain": chain,
        "paths": path_details,
        "problems": picked,
        "chapter_quota": dict(chapter_count),
        "suggestion": suggestion,
        "prompt_block": _format_kg_prompt(focus, chain, picked),
        "source": _load_full_graph().get("_source"),
    }


def extract_text_from_upload(filename: str, raw: bytes) -> str:
    """从 docx/pdf/ppt/txt 等提取纯文本；Office/PDF 统一走 MinerU。"""
    from app.services.mineru_parse import parse_upload_to_markdown

    result = parse_upload_to_markdown(filename, raw)
    if result.get("ok") and (result.get("text") or "").strip():
        return str(result["text"])
    err = result.get("error") or "解析失败"
    return f"[{err}]"
