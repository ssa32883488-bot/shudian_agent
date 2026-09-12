# -*- coding: utf-8 -*-
"""工具配图占位：模型在正文指定位置写入 DRAW 块，交付用户前替换为 Markdown 图。

约定（发给大模型）：
  <<<DRAW kind="kmap" desc="本题卡诺图">>>

- 模型在「该图应出现的步骤」写入占位，禁止把图堆到文末
- 禁止手写 ![ ](url)；系统用工具产物 artifact_url 回填
- kind 用于匹配多张图；desc 作为图片 alt
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional

DRAW_MARKER_RE = re.compile(
    r'<<<DRAW\s+kind="(?P<kind>[^"]*)"(?:\s+desc="(?P<desc>[^"]*)")?\s*>>>',
    re.IGNORECASE,
)

DRAW_MARKER_TMPL = '<<<DRAW kind="{kind}" desc="{desc}">>>'

# kind 别名 → 规范名
_KIND_ALIASES: dict[str, str] = {
    "kmap": "kmap",
    "karnaugh": "kmap",
    "卡诺": "kmap",
    "卡诺图": "kmap",
    "timing": "timing",
    "timing_wave": "timing",
    "wave": "timing",
    "波形": "timing",
    "时序": "timing",
    "时序图": "timing",
    "波形图": "timing",
    "truth": "truth",
    "truth_table": "truth",
    "真值表": "truth",
    "state": "state",
    "状态图": "state",
    "seven": "seven",
    "seven_seg": "seven",
    "七段": "seven",
    # 旧 xor 占位 → logic（异或逻辑图走 logic_dag）
    "xor": "logic",
    "xor_basic": "logic",
    "异或": "logic",
    "gate": "gate",
    "logic": "logic",
    "logic_dag": "logic",
    "电路": "circuit",
    "电路图": "circuit",
    "逻辑图": "logic",
    "char_curve": "curve",
    "curve": "curve",
    "特性曲线": "curve",
    "msi_design": "circuit",
    "msi": "circuit",
    "auto": "auto",
    "any": "auto",
    "": "auto",
}

DRAW_SYSTEM_RULES = """
工具配图嵌入规则（必须遵守）：
1. 绘图只用 draw_with_workflow；必须先成功调工具拿到图，再写解答。
2. 在图应出现的正文位置写单行占位（勿堆文末、勿编造 URL）：
   <<<DRAW kind="logic_dag" desc="本题逻辑图">>>
3. kind 与 diagram_kind 一致，八选一：logic_dag / timing_wave / state_machine /
   truth_table / kmap / seven_seg / char_curve / msi_design。
4. 一张图一个 DRAW；多图多个占位，放在对应讲解步骤里。
5. 禁止在未调用 draw_with_workflow（或调用失败）时写入 DRAW 占位。
6. 系统会把 DRAW 换成真实图片；你只需定位置与 kind。
""".strip()

_DRAW_HINTS = (
    "画",
    "绘制",
    "作图",
    "画出",
    "作出",
    "示意",
    "示意图",
    "波形",
    "时序图",
    "真值表",
    "状态图",
    "状态转换",
    "逻辑图",
    "逻辑符号",
    "逻辑符号图",
    "符号图",
    "电路图",
    "卡诺图",
    "卡诺",
    "karnaugh",
    "kmap",
    "七段",
    "数码管",
    "特性曲线",
    "传输特性",
    "VTC",
    "门符号",
    "与门",
    "或门",
    "与非",
    "或非",
    "门电路",
)


def wants_drawing_tools(question: str) -> bool:
    """题面是否明确/隐含需要调用绘图工具。"""
    q = question or ""
    return any(k in q for k in _DRAW_HINTS)


@dataclass
class DrawArtifact:
    alt: str
    url: str
    kind: str = "auto"
    tool_name: str = ""

    def to_markdown(self, desc: str = "") -> str:
        label = (desc or self.alt or "本题配图").strip() or "本题配图"
        return f"![{label}]({self.url})"


def normalize_draw_kind(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s in _KIND_ALIASES:
        return _KIND_ALIASES[s]
    for key, norm in _KIND_ALIASES.items():
        if key and key in s:
            return norm
    return s or "auto"


def infer_kind_from_artifact(
    alt: str = "",
    url: str = "",
    tool_name: str = "",
) -> str:
    blob = f"{tool_name} {alt} {url}".lower()
    checks = (
        ("kmap", "kmap"),
        ("卡诺", "kmap"),
        ("timing", "timing"),
        ("wave", "timing"),
        ("波形", "timing"),
        ("truth", "truth"),
        ("真值", "truth"),
        ("state", "state"),
        ("状态", "state"),
        ("seven", "seven"),
        ("七段", "seven"),
        ("xor", "logic"),
        ("异或", "logic"),
        ("char_curve", "curve"),
        ("curve", "curve"),
        ("特性", "curve"),
        ("gate", "gate"),
        ("logic", "logic"),
        ("电路", "circuit"),
    )
    for needle, kind in checks:
        if needle in blob:
            return kind
    return "auto"


def make_draw_marker(kind: str, desc: str = "") -> str:
    return DRAW_MARKER_TMPL.format(
        kind=normalize_draw_kind(kind),
        desc=(desc or "本题配图").replace('"', "'").replace("\n", " ").strip(),
    )


def artifacts_from_pairs(
    generated: list[tuple[str, str]],
    *,
    tool_hints: Optional[list[str]] = None,
) -> list[DrawArtifact]:
    out: list[DrawArtifact] = []
    hints = tool_hints or []
    for i, (alt, url) in enumerate(generated):
        if not url:
            continue
        tname = hints[i] if i < len(hints) else ""
        out.append(
            DrawArtifact(
                alt=alt or "本题配图",
                url=url,
                kind=infer_kind_from_artifact(alt, url, tname),
                tool_name=tname,
            )
        )
    return out


def list_draw_markers(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for m in DRAW_MARKER_RE.finditer(text or ""):
        found.append(
            {
                "kind": normalize_draw_kind(m.group("kind") or "auto"),
                "desc": (m.group("desc") or "").strip(),
                "raw": m.group(0),
            }
        )
    return found


def _pick_artifact(
    pool: list[DrawArtifact],
    want_kind: str,
) -> Optional[DrawArtifact]:
    if not pool:
        return None
    want = normalize_draw_kind(want_kind)
    if want != "auto":
        for i, art in enumerate(pool):
            if art.kind == want or want in art.kind or art.kind in want:
                return pool.pop(i)
        # kind 对不上时不强行占用，留给后续 auto / 启发式
        return None
    return pool.pop(0)


def replace_draw_markers(
    text: str,
    artifacts: list[DrawArtifact],
) -> tuple[str, list[DrawArtifact], int]:
    """按正文中 DRAW 占位顺序/kind 回填图片。

    返回：(新正文, 未使用的产物, 成功回填数量)
    """
    pool = list(artifacts)
    filled = 0

    def _sub(m: re.Match[str]) -> str:
        nonlocal filled
        want = normalize_draw_kind(m.group("kind") or "auto")
        desc = (m.group("desc") or "").strip()
        art = _pick_artifact(pool, want)
        if art is None and want != "auto":
            # 指定 kind 暂无匹配时，允许用剩余第一张（避免占位空白）
            art = _pick_artifact(pool, "auto")
        if art is None:
            return m.group(0)
        filled += 1
        return art.to_markdown(desc)

    new_text = DRAW_MARKER_RE.sub(_sub, text or "")
    return new_text, pool, filled


def strip_unfilled_draw_markers(text: str) -> str:
    """未回填占位改为可见缺图提示（不再静默删除，便于拦截回流）。"""
    def _sub(m: re.Match[str]) -> str:
        kind = normalize_draw_kind(m.group("kind") or "auto")
        desc = (m.group("desc") or "本题配图").strip() or "本题配图"
        return f"\n\n> **【配图未生成：{desc} / {kind}】** 本题要求配图但工具未产出，请重试或人工补图。\n\n"

    cleaned = DRAW_MARKER_RE.sub(_sub, text or "")
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def has_draw_markers(text: str) -> bool:
    return bool(DRAW_MARKER_RE.search(text or ""))


_TOOL_ARTIFACT_RE = re.compile(
    r"!\[[^\]]*\]\(([^)]*(?:/media/artifacts/|kmap_|timing_|wave_|truth_|xor_|"
    r"7seg_|seven|char_curve|gate_|state_|logic_)[^)]*)\)",
    re.IGNORECASE,
)

_DRAW_FAIL_NOTE_RE = re.compile(r"【配图未生成")


def answer_has_tool_drawing(answer: str) -> bool:
    """答案是否已嵌入工具产物图（非教材 FIGURE 口头描述）。"""
    return bool(_TOOL_ARTIFACT_RE.search(answer or ""))


def answer_has_draw_failure_note(answer: str) -> bool:
    return bool(_DRAW_FAIL_NOTE_RE.search(answer or ""))


def drawing_requirement_met(question: str, answer: str) -> bool:
    """题面要图时，答案须有工具产物；否则视为未满足。"""
    if not wants_drawing_tools(question or ""):
        return True
    if answer_has_draw_failure_note(answer or ""):
        return False
    return answer_has_tool_drawing(answer or "")


def unused_as_pairs(artifacts: list[DrawArtifact]) -> list[tuple[str, str]]:
    return [(a.alt, a.url) for a in artifacts]
