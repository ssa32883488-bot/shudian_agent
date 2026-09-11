#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识图谱质量自检：能否进项目。"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KG = ROOT / "data" / "kg"
sys.path.insert(0, str(ROOT / "backend"))

from app.services.graph_kg import (  # noqa: E402
    concepts_for_problem,
    find_similar_problems,
    list_concepts,
    recommend_path,
)


def main() -> None:
    g = json.loads((KG / "knowledge_graph_v0.2.json").read_text(encoding="utf-8"))
    chapters = g["nodes"]["Chapter"]
    concepts = g["nodes"]["Concept"]
    problems = g["nodes"]["Problem"]
    tests = g["edges"]["TESTS"]
    belongs = g["edges"]["BELONGS_TO"]
    prereqs = g["edges"]["PRE_REQUISITE_OF"]
    similar = g["edges"].get("SIMILAR_TO") or []

    issues: list[str] = []
    warns: list[str] = []
    score = 100

    report: dict = {"scale": {}, "tests": {}, "prereq": {}, "api": {}, "samples": {}}

    # scale
    report["scale"] = {
        "chapters": len(chapters),
        "concepts": len(concepts),
        "problems": len(problems),
        "tests": len(tests),
        "belongs_to": len(belongs),
        "prereq": len(prereqs),
        "similar": len(similar),
    }

    cnames = {c["name"] for c in concepts}
    pids = {p["id"] for p in problems}
    if len(cnames) != len(concepts):
        issues.append("Concept 存在重名")
        score -= 10

    # TESTS
    bad_from = sum(1 for e in tests if e["from"] not in pids)
    bad_to = sum(1 for e in tests if e["to"] not in cnames)
    tested = {e["from"] for e in tests}
    cover = len(tested) / max(len(problems), 1)
    by_kind = Counter(p["kind"] for p in problems)
    cov_kind: dict[str, set] = defaultdict(set)
    for e in tests:
        cov_kind[str(e.get("problem_kind"))].add(e["from"])
    force_n = sum(1 for e in tests if e.get("evidence") == "force_map")
    per = Counter(e["from"] for e in tests)

    concept_ch = {c["name"]: set(c.get("chapter_ids") or []) for c in concepts}
    cross = 0
    for e in tests:
        if e.get("evidence") == "force_map":
            continue
        p = next(x for x in problems if x["id"] == e["from"])
        want = f"ch{int(p['chapter_num']):02d}"
        if want not in concept_ch.get(e["to"], set()):
            cross += 1

    report["tests"] = {
        "coverage": f"{len(tested)}/{len(problems)}",
        "rate": round(cover, 4),
        "by_kind": {k: f"{len(cov_kind[k])}/{by_kind[k]}" for k in by_kind},
        "confidence": dict(Counter(e.get("confidence") for e in tests)),
        "force_map_ratio": round(force_n / max(len(tests), 1), 4),
        "avg_per_problem": round(sum(per.values()) / max(len(per), 1), 2),
        "max_per_problem": max(per.values()) if per else 0,
        "cross_chapter_non_force": cross,
        "bad_refs": bad_from + bad_to,
    }
    if bad_from or bad_to:
        issues.append("TESTS 悬空引用")
        score -= 20
    if cover < 0.98:
        issues.append(f"TESTS 覆盖不足 {cover:.1%}")
        score -= 15
    if force_n / max(len(tests), 1) > 0.03:
        warns.append(f"force_map 占比 {force_n/len(tests):.1%}（可接受但宜继续规则化）")
        score -= 3
    if cross > 20:
        warns.append(f"跨章 TESTS {cross}")
        score -= 5

    # PRE
    bad_p = sum(1 for e in prereqs if e["from"] not in cnames or e["to"] not in cnames)
    adj: dict[str, list[str]] = defaultdict(list)
    for e in prereqs:
        adj[e["from"]].append(e["to"])
    visiting, done = set(), set()
    cycles: list[str] = []

    def dfs(u: str, stack: list[str]) -> None:
        visiting.add(u)
        stack.append(u)
        for v in adj[u]:
            if v in visiting:
                cycles.append(" → ".join(stack[stack.index(v) :] + [v]))
            elif v not in done:
                dfs(v, stack)
        stack.pop()
        visiting.discard(u)
        done.add(u)

    for n in list(adj):
        if n not in done:
            dfs(n, [])

    has_in = {e["to"] for e in prereqs}
    has_out = {e["from"] for e in prereqs}
    isolated = [c["name"] for c in concepts if c["name"] not in has_in and c["name"] not in has_out]
    curated = sum(1 for e in prereqs if e.get("evidence") == "curated")

    report["prereq"] = {
        "edges": len(prereqs),
        "curated": curated,
        "confidence": dict(Counter(e.get("confidence") for e in prereqs)),
        "cycles": len(cycles),
        "cycle_samples": cycles[:3],
        "isolated_concepts": len(isolated),
        "isolated_ratio": round(len(isolated) / max(len(concepts), 1), 4),
        "bad_refs": bad_p,
    }
    if cycles:
        issues.append(f"前置有环 {len(cycles)}")
        score -= 25
    if bad_p:
        issues.append("PRE 悬空引用")
        score -= 15
    # 孤立概念：允许存在（不强行连边）；仅作信息，不因孤立扣分
    if curated < 30:
        warns.append("人工 curated 前置偏少（主干依赖）")
        score -= 5

    # —— 题侧图谱质量（核心）——
    per_edges: dict[str, list] = defaultdict(list)
    for e in tests:
        per_edges[e["from"]].append(e)
    solid = 0  # 至少 1 条 medium/high
    weak_all_low = 0
    for pid, es in per_edges.items():
        if any(x.get("confidence") in {"high", "medium"} for x in es):
            solid += 1
        elif es:
            weak_all_low += 1
    solid_rate = solid / max(len(problems), 1)
    report["problem_graph"] = {
        "problems_with_solid_tests": solid,
        "solid_rate": round(solid_rate, 4),
        "all_low_only": weak_all_low,
        "avg_tests": round(len(tests) / max(len(problems), 1), 2),
        "isolated_concepts_info": len(isolated),
        "note": "孤立概念不强制连边；优先保证题↔考点",
    }
    if solid_rate < 0.75:
        issues.append(f"题侧扎实挂接不足 {solid_rate:.0%}（需 medium/high TESTS）")
        score -= 15
    elif solid_rate < 0.90:
        warns.append(f"题侧扎实挂接 {solid_rate:.0%}，可继续提升")
        score -= 5
    if weak_all_low / max(len(problems), 1) > 0.25:
        warns.append(f"仅 low TESTS 的题偏多 {weak_all_low}/{len(problems)}")
        score -= 6

    # concept quality
    conf_c = Counter(c.get("confidence") for c in concepts)
    noise = [
        c["name"]
        for c in concepts
        if re.search(r"[\$\\]|\\\\Rightarrow|系列$|^公式$", c["name"] or "")
    ]
    low_kept = conf_c.get("low_kept", 0)
    report["concepts"] = {
        "confidence": dict(conf_c),
        "noise_names": noise[:10],
        "noise_count": len(noise),
        "low_kept_ratio": round(low_kept / max(len(concepts), 1), 4),
    }
    if noise:
        warns.append(f"噪声概念名 {len(noise)}: {noise[:5]}")
        score -= 5
    if low_kept / max(len(concepts), 1) > 0.55:
        warns.append(f"low_kept 占比高 {low_kept/len(concepts):.0%}（信息项，不阻断）")
        score -= 3

    # runtime graph
    runtime = ROOT / "backend" / "data" / "knowledge_graph.json"
    rt_nodes = rt_edges = 0
    if runtime.exists():
        rt = json.loads(runtime.read_text(encoding="utf-8"))
        rt_nodes = len(rt.get("nodes") or {})
        rt_edges = len(rt.get("edges") or [])
    report["runtime"] = {"path": str(runtime), "nodes": rt_nodes, "edges": rt_edges, "ok": rt_nodes >= 100}
    if rt_nodes < 100:
        issues.append(f"运行时图谱过小 nodes={rt_nodes}，需 ingest_graph")
        score -= 20

    # API smoke
    api_ok = True
    samples = {}
    for q in ["卡诺图", "触发器", "计数器", "D/A 转换器", "组合逻辑电路"]:
        r = recommend_path(q)
        samples[q] = {
            "resolved": r.get("resolved"),
            "path_len": len(r.get("path") or []),
            "path": r.get("path"),
            "suggestion": r.get("suggestion"),
        }
        if not r.get("resolved"):
            api_ok = False
            issues.append(f"路径解析失败: {q}")
            score -= 5
        elif len(r.get("path") or []) < 2:
            warns.append(f"路径过短: {q}")
            score -= 2

    # problem linkage smoke
    p_sample = ["题4.1", "例2.6.1", "R4.4.1", "题5.1"]
    link = {}
    for pid in p_sample:
        cs = concepts_for_problem(pid)
        sims = find_similar_problems(pid, 3)
        link[pid] = {"concepts": cs, "similar": [s.get("problem_id") for s in sims]}
        if not cs:
            warns.append(f"{pid} 无 TESTS")
            score -= 3
    report["api"] = {"path_ok": api_ok, "list_concepts": len(list_concepts()), "samples": samples, "problem_link": link}

    # qualitative path check: 触发器 should include 锁存/组合, not random
    trig = samples.get("触发器", {}).get("path") or []
    if "触发器" in trig and not any("锁存" in x or "组合" in x for x in trig):
        warns.append("触发器路径缺少锁存/组合等合理前置")
        score -= 5

    # similar edges sanity: same chapter mostly
    pm = {p["id"]: p for p in problems}
    sim_cross = 0
    for e in similar[:500]:
        a, b = pm.get(e["from"]), pm.get(e["to"])
        if a and b and a.get("chapter_num") != b.get("chapter_num"):
            sim_cross += 1
    report["similar"] = {"sample_cross_chapter_in_500": sim_cross}

    score = max(0, min(100, score))
    if score >= 85 and not issues:
        verdict = "PASS_WITH_NOTES" if warns else "PASS"
        ready = True
    elif score >= 70 and not any("悬空" in i or "有环" in i or "运行时" in i for i in issues):
        verdict = "CONDITIONAL"
        ready = True  # 可进项目但标 beta
    else:
        verdict = "NOT_READY"
        ready = False

    report["score"] = score
    report["verdict"] = verdict
    report["ready_for_project"] = ready
    report["issues"] = issues
    report["warnings"] = warns
    report["recommendation"] = (
        "题侧图谱可支撑拍题/问点/复杂意图；孤立概念允许存在。"
        if ready
        else "需先修复 issues 再接入。"
    )

    out = KG / "kg_quality_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== 知识图谱质量自检 ===")
    print(f"评分: {score}/100  结论: {verdict}  进项目: {ready}")
    print(f"规模: C={len(concepts)} P={len(problems)} TESTS={len(tests)} PRE={len(prereqs)}")
    print(f"TESTS覆盖: {report['tests']['coverage']} {report['tests']['by_kind']}")
    pg = report.get("problem_graph") or {}
    print(
        f"题侧扎实: {pg.get('problems_with_solid_tests')}/{len(problems)} "
        f"({pg.get('solid_rate')})  all_low={pg.get('all_low_only')}  isolated(info)={len(isolated)}"
    )
    print(f"前置: curated={curated} cycles={len(cycles)}")
    print(f"运行时: nodes={rt_nodes} edges={rt_edges}")
    if issues:
        print("阻断项:")
        for i in issues:
            print("  -", i)
    if warns:
        print("风险项:")
        for w in warns:
            print("  -", w)
    print("路径抽样:")
    for q, s in samples.items():
        print(f"  {q}: {' → '.join(s.get('path') or [])}")
    print(f"详情: {out}")


if __name__ == "__main__":
    main()
