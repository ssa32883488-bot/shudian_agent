#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
vis = json.loads((ROOT / "reports/qb_vision_full_audit.json").read_text(encoding="utf-8"))
txt = json.loads((ROOT / "reports/qb_text_only_audit.json").read_text(encoding="utf-8"))

by_id = {}
for r in vis["results"]:
    by_id[r["id"]] = r
results = list(by_id.values())
fails = [r for r in results if not r["verdict"].get("pass")]
passes = [r for r in results if r["verdict"].get("pass")]
empty = [
    r
    for r in fails
    if any("无法解析" in str(i) for i in (r["verdict"].get("issues") or []))
]
real = [r for r in fails if r not in empty]

cats: Counter[str] = Counter()
for r in real:
    issues = " ".join(r["verdict"].get("issues") or [])
    if any(k in issues for k in ("误挂", "无关", "不属于", "他题")):
        cats["wrong_or_irrelevant_fig"] += 1
    elif any(k in issues for k in ("一张图", "多道", "挤了", "多题", "连图")):
        cats["multi_qa_collage"] += 1
    elif any(k in issues for k in ("缺", "少", "未提供", "缺失")):
        cats["missing_incomplete"] += 1
    elif any(k in issues for k in ("不符", "不匹配", "不一致", "错误")):
        cats["stem_answer_mismatch"] += 1
    else:
        cats["other"] += 1

ok = len(passes) + txt["pass"]
unknown = len(empty)
bad = len(real) + txt["fail"]

lines = [
    "# 题库全量深度复检报告",
    "",
    f"- 总题数: **309**（章末习题 227 + 例题 82）",
    f"- 含图识图复检: **{len(results)}**",
    f"- 无图文本复检: **{txt['n']}**",
    f"- 识图通过: **{len(passes)}**",
    f"- 识图实质未过关: **{len(real)}**",
    f"- 识图 API 空返回未判定: **{len(empty)}** → {[x['eid'] for x in empty]}",
    f"- 无图通过: **{txt['pass']}**（警告提及图但无MD图: {txt['warn_fig_mention']}）",
    f"- **可判定通过率**: {ok}/{309 - unknown} = **{ok / (309 - unknown):.1%}**",
    f"- **整体过关（未判定计未过）**: {ok}/309 = **{ok / 309:.1%}**",
    "",
    "## 未过关分类",
]
for k, v in cats.most_common():
    lines.append(f"- {k}: {v}")
lines.append("")
lines.append("## 未过关清单")
for r in real:
    iss = "；".join(r["verdict"].get("issues") or [])[:160]
    lines.append(
        f"- {r['eid']} (id={r['id']}, score={r['verdict'].get('score')}): {iss}"
    )

(ROOT / "reports/qb_full_deep_audit_summary.md").write_text(
    "\n".join(lines), encoding="utf-8"
)
summary = {
    "total": 309,
    "vision_n": len(results),
    "vision_pass": len(passes),
    "vision_fail_real": len(real),
    "vision_unknown": len(empty),
    "text_n": txt["n"],
    "text_pass": txt["pass"],
    "text_fail": txt["fail"],
    "pass_rate_decidable": round(ok / (309 - unknown), 4),
    "pass_rate_strict": round(ok / 309, 4),
    "fail_categories": dict(cats),
    "fail_eids": [r["eid"] for r in real],
    "unknown_eids": [r["eid"] for r in empty],
    "fail_details": [
        {
            "eid": r["eid"],
            "id": r["id"],
            "score": r["verdict"].get("score"),
            "issues": r["verdict"].get("issues"),
        }
        for r in real
    ],
}
(ROOT / "reports/qb_full_deep_audit_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({k: summary[k] for k in summary if k != "fail_details"}, ensure_ascii=False, indent=2))
