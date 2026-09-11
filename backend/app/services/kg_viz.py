"""知识图谱可视化与问询：JSON / Neo4j 统一出口。"""

from __future__ import annotations

from typing import Any

from app.services.graph_kg import (
    _load_full_graph,
    _load_graph,
    knowledge_network,
    list_concepts,
    recommend_path,
)
from app.services.neo4j_client import is_neo4j_ready
from app.config import get_settings


def kg_status() -> dict[str, Any]:
    settings = get_settings()
    path_g = _load_graph()
    full = _load_full_graph()
    nodes = path_g.get("nodes") or {}
    edges = path_g.get("edges") or []
    chapters = []
    full_nodes = full.get("nodes") or {}
    if isinstance(full_nodes, dict):
        for ch in full_nodes.get("Chapter") or []:
            chapters.append(
                {
                    "id": ch.get("id"),
                    "name": ch.get("name"),
                    "num": ch.get("chapter_num") or ch.get("num"),
                }
            )
    chapters.sort(key=lambda x: (x.get("num") is None, x.get("num") or 99, x.get("id") or ""))
    return {
        "ok": True,
        "neo4j_enabled": bool(settings.neo4j_enabled),
        "neo4j_ready": bool(settings.neo4j_enabled and is_neo4j_ready()),
        "engine": path_g.get("_engine") or "unknown",
        "source": path_g.get("_source"),
        "concept_count": len(nodes) if isinstance(nodes, dict) else 0,
        "edge_count": len(edges) if isinstance(edges, list) else 0,
        "chapters": chapters,
        "agent_tool": "graph_query",
        "hint": (
            "答疑智能体可通过 graph_query 工具查询本图谱；"
            "在图谱页选中知识点后可一键带到 AI 答疑。"
        ),
    }


def _chapter_of(meta: Any) -> str:
    if isinstance(meta, dict):
        ch = meta.get("chapter") or ""
        if ch:
            return str(ch)
        ids = meta.get("chapter_ids") or []
        if ids:
            return str(ids[0])
    return ""


def _match_chapter(meta: Any, chapter: str) -> bool:
    if not chapter:
        return True
    if isinstance(meta, dict):
        ids = [str(x) for x in (meta.get("chapter_ids") or [])]
        if chapter in ids:
            return True
        ch = str(meta.get("chapter") or "")
        if chapter == ch or chapter in ch:
            return True
    return chapter in _chapter_of(meta)


def viz_graph(
    *,
    chapter: str | None = None,
    q: str | None = None,
    focus: str | None = None,
    limit: int = 80,
    depth: int = 1,
) -> dict[str, Any]:
    """返回 ECharts / 前端力导向图所需 nodes + links。"""
    g = _load_graph()
    nodes_raw = g.get("nodes") or {}
    edges_raw = g.get("edges") or []
    if not isinstance(nodes_raw, dict):
        nodes_raw = {}
    if not isinstance(edges_raw, list):
        edges_raw = []

    chapter = (chapter or "").strip()
    q = (q or "").strip().lower()
    focus = (focus or "").strip()
    limit = max(10, min(int(limit or 80), 200))
    depth = max(0, min(int(depth or 1), 2))

    # 邻域模式：以 focus 为中心展开
    if focus and focus in nodes_raw:
        keep = {focus}
        frontier = {focus}
        for _ in range(depth):
            nxt: set[str] = set()
            for e in edges_raw:
                a, b = e.get("from"), e.get("to")
                if a in frontier and b:
                    nxt.add(str(b))
                if b in frontier and a:
                    nxt.add(str(a))
            keep |= nxt
            frontier = nxt
        names = [n for n in keep if n in nodes_raw]
    else:
        names = list(nodes_raw.keys())
        if chapter:
            names = [n for n in names if _match_chapter(nodes_raw.get(n), chapter)]
        if q:
            names = [n for n in names if q in n.lower()]
        # 优先保留有边的节点
        degree: dict[str, int] = {n: 0 for n in names}
        for e in edges_raw:
            a, b = e.get("from"), e.get("to")
            if a in degree:
                degree[a] += 1
            if b in degree:
                degree[b] += 1
        names.sort(key=lambda n: (-degree.get(n, 0), n))
        names = names[:limit]

    name_set = set(names)
    nodes = []
    for n in names:
        meta = nodes_raw.get(n) or {}
        ch = _chapter_of(meta)
        nodes.append(
            {
                "id": n,
                "name": n,
                "category": ch or "未分章",
                "symbolSize": 42 if n == focus else 28,
                "chapter": ch,
            }
        )

    links = []
    for e in edges_raw:
        a, b = e.get("from"), e.get("to")
        if a in name_set and b in name_set:
            links.append(
                {
                    "source": a,
                    "target": b,
                    "relation": e.get("type") or "PRE_REQUISITE_OF",
                    "confidence": e.get("confidence") or "",
                }
            )

    categories = sorted({n["category"] for n in nodes})
    return {
        "ok": True,
        "engine": g.get("_engine"),
        "source": g.get("_source"),
        "focus": focus or None,
        "categories": [{"name": c} for c in categories],
        "nodes": nodes,
        "links": links,
        "stats": {"nodes": len(nodes), "links": len(links)},
    }


def concept_detail(name: str) -> dict[str, Any]:
    name = (name or "").strip()
    if not name:
        return {"ok": False, "detail": "缺少概念名"}
    path_info = recommend_path(name)
    net = knowledge_network(concepts=[name], top_k=6, problems_per_concept=5)
    # 邻域子图
    sub = viz_graph(focus=name, depth=1, limit=40)
    return {
        "ok": True,
        "name": name,
        "resolved": path_info.get("resolved"),
        "path": path_info.get("path") or [],
        "suggestion": path_info.get("suggestion"),
        "learning_chain": net.get("learning_chain") or [],
        "related_problems": net.get("related_problems") or [],
        "prompt_block": net.get("prompt_block"),
        "subgraph": sub,
        "ask_seed": f"请结合知识图谱讲解「{name}」：先说明它在逻辑链中的位置，再讲核心要点，并给一道相关例题思路。",
    }


def ask_kg(text: str, *, top_k: int = 6) -> dict[str, Any]:
    text = (text or "").strip()
    if not text:
        return {"ok": False, "detail": "请输入问题或知识点"}
    net = knowledge_network(text=text, top_k=top_k, problems_per_concept=4)
    keywords = net.get("keywords") or []
    focus = keywords[0] if keywords else None
    sub = viz_graph(focus=focus, depth=1, limit=36) if focus else viz_graph(q=text[:20], limit=36)
    return {
        "ok": True,
        "query": text,
        "network": net,
        "subgraph": sub,
        "ask_seed": (
            f"结合知识图谱回答：{text}\n"
            f"已知考点：{'、'.join(keywords[:6]) or '（待识别）'}\n"
            f"逻辑链：{' → '.join((net.get('learning_chain') or [])[:10]) or '—'}"
        ),
    }


def search_concepts(q: str, limit: int = 20) -> list[str]:
    q = (q or "").strip().lower()
    all_names = list_concepts()
    if not q:
        return all_names[:limit]
    return [n for n in all_names if q in n.lower()][:limit]
