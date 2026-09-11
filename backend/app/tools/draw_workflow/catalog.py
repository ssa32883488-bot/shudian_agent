# -*- coding: utf-8 -*-
"""图类目录：仅工作流主路径可出图的种类。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class KindSpec:
    kind: str
    title_zh: str
    aliases: tuple[str, ...]
    skill_file: str
    runner: str
    description: str
    keywords: tuple[str, ...]


KINDS: dict[str, KindSpec] = {
    "logic_dag": KindSpec(
        kind="logic_dag",
        title_zh="逻辑符号图",
        aliases=("logic", "logic_dag", "门级", "逻辑图"),
        skill_file="logic_dag.md",
        runner="logic_netlist",
        description="门级逻辑图：logic_ir_v1 → netlistsvg",
        keywords=(
            "逻辑图",
            "门级",
            "全加",
            "半加",
            "与非",
            "或非",
            "logic",
            "NAND",
            "XOR",
            "异或",
            "表达式画图",
            "门电路",
        ),
    ),
    "timing_wave": KindSpec(
        kind="timing_wave",
        title_zh="时序波形图",
        aliases=("timing", "wave", "waveform", "timing_wave"),
        skill_file="timing_wave.md",
        runner="wave",
        description="多信号高低电平时间轴：wave_ir_v1 → wave_ir_to_svg",
        keywords=("时序", "波形", "waveform", "timing", "wave", "时钟波形"),
    ),
    "state_machine": KindSpec(
        kind="state_machine",
        title_zh="状态转换图",
        aliases=("state", "state_machine", "fsm"),
        skill_file="state_machine.md",
        runner="state",
        description="圆形状态+转移：state_ir_v1 → state_ir_to_svg",
        keywords=("状态图", "状态转换", "状态机", "FSM", "次态"),
    ),
    "truth_table": KindSpec(
        kind="truth_table",
        title_zh="真值表",
        aliases=("truth", "truth_table", "功能表"),
        skill_file="truth_table.md",
        runner="tier_b",
        description="真值表 SVG（工作流 runner）",
        keywords=("真值表", "功能表", "truth"),
    ),
    "kmap": KindSpec(
        kind="kmap",
        title_zh="卡诺图",
        aliases=("kmap", "karnaugh", "卡诺"),
        skill_file="kmap.md",
        runner="tier_b",
        description="带圈卡诺图 2/3/4 变量（工作流 runner）",
        keywords=("卡诺", "kmap", "Σm", "Sigma m", "最小项化简"),
    ),
    "seven_seg": KindSpec(
        kind="seven_seg",
        title_zh="七段数码管",
        aliases=("seven_seg", "7seg", "数码管"),
        skill_file="seven_seg.md",
        runner="tier_b",
        description="共阴点亮示意（工作流 runner）",
        keywords=("七段", "数码管", "段码", "显示数字"),
    ),
    "char_curve": KindSpec(
        kind="char_curve",
        title_zh="特性曲线",
        aliases=("curve", "char_curve", "vtc"),
        skill_file="char_curve.md",
        runner="tier_b",
        description="VTC 特性曲线 Matplotlib（工作流 runner）",
        keywords=("特性曲线", "传输特性", "VTC", "电压传输"),
    ),
    "msi_design": KindSpec(
        kind="msi_design",
        title_zh="设计电路（MSI/555/CMOS/DAC）",
        aliases=(
            "msi_design",
            "digital_msi",
            "mod7",
            "74163",
            "74160",
            "74161",
            "置零法",
            "加载法",
            "同步清零",
            "同步加载",
            "555",
            "NE555",
            "AD7520",
            "设计电路",
            "msi",
        ),
        skill_file="msi_design.md",
        runner="digital_dig",
        description=(
            "设计电路：74 MSI / 555 / CMOS / DAC·ADC；"
            "skill→IR→校验→Digital 布局"
        ),
        keywords=(
            "设计电路",
            "置零法",
            "加载法",
            "同步清零",
            "同步加载",
            "同步置零",
            "555",
            "NE555",
            "多谐",
            "单稳",
            "施密特",
            "AD7520",
            "DAC",
            "CC4069",
            "74163",
            "74LS163",
            "74HC163",
            "74160",
            "74161",
            "74138",
            "74151",
            "74LS",
            "74HC",
            "译码器",
            "数据选择器",
            "MSI",
            "中规模",
            "模7",
            "模Ｎ",
            "模N",
            "七进制",
            "进制计数",
            "计数器芯片",
            "进位输出",
            "设计计数器",
            "detect state",
            "预置数",
        ),
    ),
}


def get_kind(kind: str) -> Optional[KindSpec]:
    k = (kind or "").strip().lower()
    if k in KINDS:
        return KINDS[k]
    for spec in KINDS.values():
        if k in spec.aliases:
            return spec
    return None
