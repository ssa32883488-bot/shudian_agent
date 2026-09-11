"""Tier-B：真值表 / 七段数码管 / 特性曲线（教材风）。"""

from __future__ import annotations

from app.tools.gateway import ToolResult, wrap_err, wrap_ok

_FONT = "Microsoft YaHei, PingFang SC, Noto Sans SC, Segoe UI, sans-serif"


def draw_truth_table(
    *,
    inputs: list[str],
    outputs: list[str],
    rows: list[list[int]],
    title: str = "真值表",
) -> ToolResult:
    if not inputs or not outputs or not rows:
        return wrap_err("inputs/outputs/rows 不能为空", tier="B", engine="svg_table")
    cols = inputs + outputs
    cw, rh = 48, 28
    ox, oy = 40, 50
    w = ox + len(cols) * cw + 20
    h = oy + (len(rows) + 1) * rh + 30
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{ox}" y="28" font-size="15" font-weight="700" fill="#0f172a" '
        f'font-family="{_FONT}">{title}</text>',
    ]
    for i, name in enumerate(cols):
        x = ox + i * cw
        parts.append(
            f'<rect x="{x}" y="{oy}" width="{cw}" height="{rh}" fill="#e2e8f0" stroke="#64748b"/>'
            f'<text x="{x + cw / 2}" y="{oy + 18}" text-anchor="middle" font-size="12">{name}</text>'
        )
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            x = ox + c * cw
            y = oy + (r + 1) * rh
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cw}" height="{rh}" fill="#fff" stroke="#94a3b8"/>'
                f'<text x="{x + cw / 2}" y="{y + 18}" text-anchor="middle" font-size="12">{val}</text>'
            )
    parts.append("</svg>")
    return wrap_ok(
        svg="".join(parts),
        tier="B",
        engine="svg_table",
        prefix="truth",
        meta={"inputs": inputs, "outputs": outputs, "n_rows": len(rows)},
    )


def draw_seven_seg(*, digit: int = 8, title: str = "七段数码管") -> ToolResult:
    """共阴七段点亮示意 · 白底教材风（段亮=红，段灭=浅灰描边）。"""
    if digit < 0 or digit > 9:
        return wrap_err("digit 须为 0-9", tier="B", engine="svg_seven_seg")
    seg_map = {
        0: "abcdef",
        1: "bc",
        2: "abdeg",
        3: "abcdg",
        4: "bcfg",
        5: "acdfg",
        6: "acdefg",
        7: "abc",
        8: "abcdefg",
        9: "abcdfg",
    }
    on = set(seg_map[digit])
    # 标题区 y≤40；段体从 y=56 起，避免挡字
    segs = {
        "a": (36, 56, 68, 10),
        "b": (104, 66, 10, 44),
        "c": (104, 118, 10, 44),
        "d": (36, 162, 68, 10),
        "e": (26, 118, 10, 44),
        "f": (26, 66, 10, 44),
        "g": (36, 108, 68, 10),
    }
    labels = {
        "a": (70, 52),
        "b": (122, 88),
        "c": (122, 140),
        "d": (70, 182),
        "e": (12, 140),
        "f": (12, 88),
        "g": (70, 102),
    }
    w, h = 140, 200
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">',
        f'<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{w/2}" y="18" text-anchor="middle" font-size="13" font-weight="700" '
        f'fill="#1a1814" font-family="{_FONT}">{title}</text>',
        f'<text x="{w/2}" y="34" text-anchor="middle" font-size="11" '
        f'fill="#64748b" font-family="{_FONT}">显示数字 {digit} · 共阴</text>',
        # 外框（数码管外形）· 顶部留空避开标题
        f'<rect x="18" y="46" width="104" height="134" rx="4" fill="#fafafa" '
        f'stroke="#cbd5e1" stroke-width="1.2"/>',
    ]
    for name, (x, y, ww, hh) in segs.items():
        lit = name in on
        fill = "#c62828" if lit else "#eceff1"
        stroke = "#374151" if lit else "#9ca3af"
        sw = 1.4 if lit else 1.0
        parts.append(
            f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="2" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
    # 段名标注（教材风小字）
    for name, (lx, ly) in labels.items():
        parts.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9" '
            f'fill="#94a3b8" font-family="Consolas,monospace">{name}</text>'
        )
    parts.append("</svg>")
    return wrap_ok(
        svg="".join(parts),
        tier="B",
        engine="svg_seven_seg",
        prefix="7seg",
        meta={"digit": digit, "segments": sorted(on), "style": "textbook_white"},
    )


def draw_char_curve(*, curve: str = "ttl_vtc", title: str = "特性曲线") -> ToolResult:
    """委托 Matplotlib 渲染（MATLAB 风格开源栈）。"""
    from app.tools.draw.char_curve_mpl import draw_char_curve as _mpl

    return _mpl(curve=curve, title=title)
