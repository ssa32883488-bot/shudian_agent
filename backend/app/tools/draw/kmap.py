"""Tier-B：带圈卡诺图（确定性 SVG）。

圈选规则对齐教材：按 2 的幂次相邻（含左右/上下环绕）画彩色圆角框，
而不是给每个 1 单独画小圆。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.tools.gateway import ToolResult, wrap_err, wrap_ok

_GRAY2 = [0, 1, 3, 2]

# 教材风格多色圈（描边）
_GROUP_COLORS = [
    "#0d9488",  # teal
    "#2563eb",  # blue
    "#dc2626",  # red
    "#b45309",  # brown
    "#7c3aed",  # violet
    "#db2777",  # pink
]


@dataclass(frozen=True)
class KGroup:
    minterms: frozenset[int]
    term: str


def _cell_xy(var_count: int, minterm: int) -> tuple[int, int]:
    if var_count == 2:
        return (minterm >> 1) & 1, minterm & 1
    if var_count == 3:
        ab = minterm >> 1
        c = minterm & 1
        col = _GRAY2.index(ab) if ab in _GRAY2 else ab
        return c, col
    ab = (minterm >> 2) & 0b11
    cd = minterm & 0b11
    return _GRAY2.index(ab), _GRAY2.index(cd)


def _minterm_at(var_count: int, row: int, col: int) -> int:
    for m in range(1 << var_count):
        r, c = _cell_xy(var_count, m)
        if r == row and c == col:
            return m
    raise ValueError(f"no minterm at ({row},{col})")


def _grid_size(var_count: int) -> tuple[int, int]:
    if var_count == 2:
        return 2, 2
    if var_count == 3:
        return 2, 4
    return 4, 4


def _axis_bits(var_count: int) -> tuple[list[str], list[str], str, str]:
    """行标签、列标签、行变量名、列变量名。"""
    g = ["00", "01", "11", "10"]
    if var_count == 2:
        return ["0", "1"], ["0", "1"], "A", "B"
    if var_count == 3:
        return ["0", "1"], g, "C", "AB"
    return g, g, "AB", "CD"


def _is_cube(minterms: list[int]) -> bool:
    n = len(minterms)
    if n == 0 or (n & (n - 1)) != 0:
        return False
    uniq = set(minterms)
    if len(uniq) != n:
        return False
    base = minterms[0]
    mask = 0
    for m in minterms:
        mask |= base ^ m
    free = bin(mask).count("1")
    return (1 << free) == n


def _term_from_cube(minterms: list[int], var_count: int) -> str:
    names = ["A", "B", "C", "D"][:var_count]
    base = minterms[0]
    mask = 0
    for m in minterms:
        mask |= base ^ m
    parts: list[str] = []
    for i, name in enumerate(names):
        bit = var_count - 1 - i
        if mask & (1 << bit):
            continue
        parts.append(name if (base & (1 << bit)) else f"{name}'")
    return "".join(parts) if parts else "1"


def _pow2_upto(n: int) -> list[int]:
    out = []
    x = 1
    while x <= n:
        out.append(x)
        x <<= 1
    return out


def _find_all_cubes(
    var_count: int,
    ones: set[int],
    dont_cares: set[int],
) -> list[KGroup]:
    """枚举 Gray 网格上合法立方体圈（含环绕）。"""
    rows, cols = _grid_size(var_count)
    coverable = ones | dont_cares
    found: dict[frozenset[int], str] = {}

    for h in _pow2_upto(rows):
        for w in _pow2_upto(cols):
            for r0 in range(rows):
                for c0 in range(cols):
                    cells: list[int] = []
                    ok = True
                    for dr in range(h):
                        for dc in range(w):
                            r = (r0 + dr) % rows
                            c = (c0 + dc) % cols
                            m = _minterm_at(var_count, r, c)
                            if m not in coverable:
                                ok = False
                                break
                            cells.append(m)
                        if not ok:
                            break
                    if not ok:
                        continue
                    if not any(m in ones for m in cells):
                        continue
                    if not _is_cube(cells):
                        continue
                    key = frozenset(cells)
                    if key not in found:
                        found[key] = _term_from_cube(cells, var_count)
    return [KGroup(minterms=k, term=t) for k, t in found.items()]


def _maximal_groups(groups: list[KGroup]) -> list[KGroup]:
    out: list[KGroup] = []
    for g in sorted(groups, key=lambda x: -len(x.minterms)):
        if any(g.minterms < h.minterms for h in groups if h is not g):
            continue
        out.append(g)
    return out


def _cover_ones(groups: list[KGroup], ones: set[int]) -> list[KGroup]:
    """本质蕴涵项 + 贪心覆盖，得到教材上常见的一组圈。"""
    maximal = _maximal_groups(groups)
    if not ones:
        return []

    uncovered = set(ones)
    selected: list[KGroup] = []

    # 本质：某个 1 只被一个极大圈覆盖
    for m in list(uncovered):
        covers = [g for g in maximal if m in g.minterms]
        if len(covers) == 1:
            g = covers[0]
            if g not in selected:
                selected.append(g)
                uncovered -= g.minterms

    while uncovered:
        ranked = sorted(
            maximal,
            key=lambda g: (len(g.minterms & uncovered), len(g.minterms)),
            reverse=True,
        )
        best = ranked[0] if ranked else None
        if not best or not (best.minterms & uncovered):
            # 回退：用任意含该点的立方体
            fallback = [
                g
                for g in groups
                if g.minterms & uncovered
            ]
            if not fallback:
                break
            best = max(fallback, key=lambda g: (len(g.minterms & uncovered), len(g.minterms)))
        if best in selected:
            # 防止死循环：强制吃掉一个点
            uncovered -= best.minterms
            continue
        selected.append(best)
        uncovered -= best.minterms

    return selected


def _split_axis(idxs: set[int], n: int) -> list[list[int]]:
    """环绕时拆成多段连续区间，便于分块画框。"""
    if not idxs:
        return []
    s = sorted(idxs)
    if len(s) == n:
        return [s]
    comps: list[list[int]] = []
    cur = [s[0]]
    for x in s[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            comps.append(cur)
            cur = [x]
    comps.append(cur)
    return comps


def _group_draw_segments(
    minterms: frozenset[int],
    var_count: int,
) -> list[tuple[int, int, int, int]]:
    """返回若干 (r0,r1,c0,c1) 闭区间矩形（不跨环绕）。"""
    rows, cols = _grid_size(var_count)
    positions = [_cell_xy(var_count, m) for m in minterms]
    row_set = {r for r, _ in positions}
    col_set = {c for _, c in positions}
    # 合法立方体在网格上应是行集合 × 列集合
    row_parts = _split_axis(row_set, rows)
    col_parts = _split_axis(col_set, cols)
    segs: list[tuple[int, int, int, int]] = []
    for rp in row_parts:
        for cp in col_parts:
            segs.append((rp[0], rp[-1], cp[0], cp[-1]))
    return segs


def _simplify_expr(groups: list[KGroup], ones: list[int], var_count: int) -> str:
    if not ones:
        return "F = 0"
    if len(ones) == (1 << var_count):
        return "F = 1"
    if not groups:
        terms = " + ".join(f"m{i}" for i in sorted(ones))
        return f"F = {terms}"
    # 稳定排序：先大圈后小圈，同尺寸按 term
    ordered = sorted(groups, key=lambda g: (-len(g.minterms), g.term))
    return "F = " + " + ".join(g.term for g in ordered)


def render_kmap_svg(
    *,
    var_count: int,
    ones: list[int],
    dont_cares: Optional[list[int]] = None,
    title: str = "卡诺图",
    auto_group: bool = True,
) -> tuple[str, list[KGroup], str]:
    dont_cares = dont_cares or []
    rows, cols = _grid_size(var_count)
    cell = 56
    ox, oy = 80, 78
    pad_r, pad_b = 28, 52
    w = ox + cols * cell + pad_r
    h = oy + rows * cell + pad_b
    one_set = set(ones)
    dc_set = set(dont_cares)

    groups: list[KGroup] = []
    if auto_group and one_set:
        all_cubes = _find_all_cubes(var_count, one_set, dc_set)
        groups = _cover_ones(all_cubes, one_set)

    expr = _simplify_expr(groups, ones, var_count)

    # —— 格子 ——
    cells_svg: list[str] = []
    for r in range(rows):
        for c in range(cols):
            idx = _minterm_at(var_count, r, c)
            x = ox + c * cell
            y = oy + r * cell
            val = "X" if idx in dc_set else ("1" if idx in one_set else "")
            # 空格表示 0，更接近教材图二
            fill = "#fff"
            if val == "1":
                fill = "#fff"
            elif val == "X":
                fill = "#fff7ed"
            show = val if val else ""
            cells_svg.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'fill="{fill}" stroke="#1e293b" stroke-width="1.4"/>'
                f'<text x="{x + cell / 2}" y="{y + cell / 2 + 6}" text-anchor="middle" '
                f'font-size="18" font-family="Segoe UI,sans-serif" font-weight="600" '
                f'fill="#0f172a">{show}</text>'
            )

    # —— 圈组（画在格子之上）——
    # 大圈靠外、小圈/后圈靠内，错开内缩，避免多圈贴边叠成「双边框」
    loops_svg: list[str] = []
    draw_order = sorted(
        enumerate(groups),
        key=lambda ig: (-len(ig[1].minterms), ig[0]),
    )
    for draw_i, (gi, g) in enumerate(draw_order):
        color = _GROUP_COLORS[gi % len(_GROUP_COLORS)]
        segs = _group_draw_segments(g.minterms, var_count)
        fragmented = len(segs) > 1  # 环绕拆段（左右/四角）
        for r0, r1, c0, c1 in segs:
            single = r0 == r1 and c0 == c1
            # 基础错开 + 环绕单格段再内缩一点，减少与外圈贴合
            inset = 3 + draw_i * 5
            if fragmented and single:
                inset += 4
            inset = min(inset, max(3, cell // 2 - 10))
            radius = max(6, 13 - draw_i * 2)
            x = ox + c0 * cell + inset
            y = oy + r0 * cell + inset
            rw = (c1 - c0 + 1) * cell - 2 * inset
            rh = (r1 - r0 + 1) * cell - 2 * inset
            if rw < 8 or rh < 8:
                continue
            loops_svg.append(
                f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" '
                f'rx="{radius}" ry="{radius}" fill="none" stroke="{color}" '
                f'stroke-width="2.6" opacity="0.95"/>'
            )


    # —— 坐标轴 ——
    row_labs, col_labs, row_name, col_name = _axis_bits(var_count)
    axis_svg: list[str] = []
    # 左上角变量标注
    axis_svg.append(
        f'<text x="{ox - 8}" y="{oy - 14}" text-anchor="end" font-size="12" '
        f'font-family="Segoe UI,sans-serif" fill="#334155">{row_name}</text>'
        f'<text x="{ox + 8}" y="{oy - 14}" font-size="12" '
        f'font-family="Segoe UI,sans-serif" fill="#334155">{col_name}</text>'
        f'<line x1="{ox - 22}" y1="{oy - 22}" x2="{ox - 2}" y2="{oy - 4}" '
        f'stroke="#64748b" stroke-width="1"/>'
    )
    for c, lab in enumerate(col_labs[:cols]):
        axis_svg.append(
            f'<text x="{ox + c * cell + cell / 2}" y="{oy - 8}" text-anchor="middle" '
            f'font-size="12" font-family="Consolas,monospace" fill="#334155">{lab}</text>'
        )
    for r, lab in enumerate(row_labs[:rows]):
        axis_svg.append(
            f'<text x="{ox - 10}" y="{oy + r * cell + cell / 2 + 4}" text-anchor="end" '
            f'font-size="12" font-family="Consolas,monospace" fill="#334155">{lab}</text>'
        )

    header = (
        f'<text x="{ox}" y="26" font-size="15" font-weight="700" '
        f'font-family="Segoe UI,sans-serif" fill="#0f172a">{title}</text>'
    )
    footer = (
        f'<text x="{ox}" y="{oy + rows * cell + 28}" font-size="14" font-weight="700" '
        f'font-family="Segoe UI,sans-serif" fill="#0f172a">{expr}</text>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f"{header}{''.join(axis_svg)}{''.join(cells_svg)}{''.join(loops_svg)}{footer}"
        f"</svg>"
    )
    return svg, groups, expr


def draw_kmap(
    *,
    minterms: list[int],
    var_count: int = 4,
    dont_cares: Optional[list[int]] = None,
    auto_group: bool = True,
    title: str = "卡诺图化简",
) -> ToolResult:
    if var_count not in (2, 3, 4):
        return wrap_err("var_count 仅支持 2/3/4", tier="B", engine="svg_kmap")
    max_m = 1 << var_count
    ones = [int(m) for m in minterms if 0 <= int(m) < max_m]
    dcs = [int(m) for m in (dont_cares or []) if 0 <= int(m) < max_m]
    if not ones and not dcs:
        return wrap_err("minterms 为空", tier="B", engine="svg_kmap")

    svg, groups, expr = render_kmap_svg(
        var_count=var_count,
        ones=ones,
        dont_cares=dcs,
        title=title,
        auto_group=auto_group,
    )
    warnings: list[str] = []
    if not auto_group:
        warnings.append("未启用自动圈选，仅填格")
    elif ones and not groups:
        warnings.append("未能自动圈选，请检查最小项")

    return wrap_ok(
        svg=svg,
        tier="B",
        engine="svg_kmap",
        prefix="kmap",
        meta={
            "var_count": var_count,
            "minterms": ones,
            "dont_cares": dcs,
            "auto_group": auto_group,
            "groups": [
                {"minterms": sorted(g.minterms), "term": g.term} for g in groups
            ],
            "simplified": expr,
        },
        warnings=warnings,
    )


def parse_sum_of_minterms(expr: str) -> tuple[int, list[int]]:
    """从 Σm(0,2,5) / F=Σm(...) 解析。默认 4 变量。"""
    import re

    m = re.search(r"[ΣSs](?:igma)?\s*m\s*\(([^)]+)\)", expr, re.I)
    if not m:
        m = re.search(r"m\s*\(([^)]+)\)", expr, re.I)
    if not m:
        return 4, []
    parts = re.split(r"[,，\s]+", m.group(1).strip())
    nums = [int(p) for p in parts if p.isdigit()]
    vmax = max(nums) if nums else 0
    if vmax <= 3:
        vc = 2
    elif vmax <= 7:
        vc = 3
    else:
        vc = 4
    return vc, nums
