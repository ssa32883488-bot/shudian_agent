"""Tier-B 特性曲线：Matplotlib（MATLAB 风格开源绘图栈）渲染 VTC 等。"""

from __future__ import annotations

import io
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from app.tools.gateway import ToolResult, wrap_err, wrap_ok

_MPL_RC = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "PingFang SC", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "svg.fonttype": "none",
}

# 课本图 3.4.10 · VCC=5V，坐标轴为实际电压（V）
_TTL_VOH = 3.4
_TTL_VOL = 0.2
_TTL_V_AB = 0.6
_TTL_V_BC = 1.3
_TTL_V_CD = 1.5
_TTL_VTH = 1.4
_TTL_VO_BC_END = 1.75  # BC 线性区末端输出（示意）


def _smoothstep(t: np.ndarray) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _ttl_vo(vi: np.ndarray) -> np.ndarray:
    """TTL 反相器 VTC（伏特）：AB 平台 · BC 缓降 · CD 陡降 · DE 低电平。"""
    vo = np.empty_like(vi)
    voh, vol = _TTL_VOH, _TTL_VOL
    v_ab, v_bc, v_cd = _TTL_V_AB, _TTL_V_BC, _TTL_V_CD
    vo_end = _TTL_VO_BC_END

    for i, v in enumerate(vi):
        if v <= v_ab:
            vo[i] = voh
        elif v <= v_bc:
            t = (v - v_ab) / (v_bc - v_ab)
            vo[i] = voh - (voh - vo_end) * t
        elif v <= v_cd:
            t = (v - v_bc) / (v_cd - v_bc)
            s = _smoothstep(np.array([t]))[0]
            vo[i] = vo_end * (1.0 - s) + vol * s
        else:
            vo[i] = vol
    return vo


def _cmos_vo(vi: np.ndarray) -> np.ndarray:
    """CMOS 反相器 VTC（伏特，VDD=5V）。"""
    vdd = 5.0
    t = (vi - 0.35 * vdd) / (0.30 * vdd)
    s = _smoothstep(t)
    return vdd * (1.0 - s)


_CURVE_FN: dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "ttl_vtc": _ttl_vo,
    "cmos_vtc": _cmos_vo,
}


def _annotate_ttl(ax, vi: np.ndarray, vo: np.ndarray) -> None:
    pts = {
        "A": (0.08, _TTL_VOH),
        "B": (_TTL_V_AB, _TTL_VOH),
        "C": (_TTL_V_BC, float(np.interp(_TTL_V_BC, vi, vo))),
        "D": (_TTL_V_CD, _TTL_VOL),
    }
    for name, (px, py) in pts.items():
        ax.plot(px, py, "o", color="#1d4ed8", markersize=4.5, zorder=5)
        ax.text(
            px + 0.04,
            py + (0.12 if name in ("A", "B") else -0.18),
            name,
            fontsize=11,
            fontstyle="italic",
            color="#1e293b",
        )
    ax.axvline(_TTL_VTH, color="#cbd5e1", linestyle=(0, (3, 3)), linewidth=0.8)
    ax.text(_TTL_VTH, -0.22, r"$V_{TH}$", ha="center", fontsize=10, color="#475569")


def _render_ttl_svg(*, title: str) -> str:
    vi = np.linspace(0.0, 1.65, 512)
    vo = _ttl_vo(vi)

    with plt.rc_context(_MPL_RC):
        fig, ax = plt.subplots(figsize=(4.6, 3.4), dpi=100)
        ax.plot(vi, vo, color="#1d4ed8", linewidth=2.0, solid_capstyle="round")
        _annotate_ttl(ax, vi, vo)

        ax.set_xlim(0, 1.65)
        ax.set_ylim(0, 3.55)
        ax.set_xlabel(r"$v_I$/V", fontsize=12)
        ax.set_ylabel(r"$v_O$/V", fontsize=12)
        ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
        ax.set_xticks([0, 0.5, 1.0, 1.5])
        ax.set_xticklabels(["0", "0.5", "1.0", "1.5"])
        ax.set_yticks([0, 1.0, 2.0, 3.0])
        ax.set_yticklabels(["0", "1.0", "2.0", "3.0"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="in", length=4)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="svg", bbox_inches="tight")
        plt.close(fig)
        return buf.getvalue().decode("utf-8")


def _render_cmos_svg(*, title: str) -> str:
    vdd = 5.0
    vi = np.linspace(0.0, vdd, 512)
    vo = _cmos_vo(vi)

    with plt.rc_context(_MPL_RC):
        fig, ax = plt.subplots(figsize=(4.6, 3.4), dpi=100)
        ax.plot(vi, vo, color="#1d4ed8", linewidth=2.0, solid_capstyle="round")
        half = vdd / 2
        ax.axhline(half, color="#94a3b8", linestyle=(0, (4, 3)), linewidth=0.9)
        ax.axvline(half, color="#94a3b8", linestyle=(0, (4, 3)), linewidth=0.9)
        ax.plot(half, half, "o", color="#1d4ed8", markersize=5)

        ax.set_xlim(0, vdd * 1.05)
        ax.set_ylim(0, vdd * 1.05)
        ax.set_xlabel(r"$v_I$/V", fontsize=12)
        ax.set_ylabel(r"$v_O$/V", fontsize=12)
        ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
        ax.set_xticks([0, 2.5, 5.0])
        ax.set_xticklabels(["0", "2.5", "5.0"])
        ax.set_yticks([0, 2.5, 5.0])
        ax.set_yticklabels(["0", "2.5", "5.0"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="in", length=4)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="svg", bbox_inches="tight")
        plt.close(fig)
        return buf.getvalue().decode("utf-8")


def _render_vtc_svg(*, curve: str, title: str) -> str:
    if curve == "ttl_vtc":
        return _render_ttl_svg(title=title)
    return _render_cmos_svg(title=title)


def draw_char_curve(
    *,
    curve: str = "ttl_vtc",
    title: str = "特性曲线",
) -> ToolResult:
    if curve not in _CURVE_FN:
        return wrap_err(
            f"curve 不支持: {curve}，可选 {list(_CURVE_FN)}",
            tier="B",
            engine="matplotlib_vtc",
        )
    svg = _render_vtc_svg(curve=curve, title=title)
    return wrap_ok(
        svg=svg,
        tier="B",
        engine="matplotlib_vtc",
        prefix="curve",
        meta={"curve": curve, "backend": "matplotlib", "style": "textbook_vtc_volts"},
        warnings=["教材级示意曲线（Matplotlib 参数模型），非器件实测"],
    )
