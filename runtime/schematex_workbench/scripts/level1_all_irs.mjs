/**
 * Level-1 全量 IR 数据（识图/教材语义；版式不保证 TEXTBOOK_OK）
 * 由 scripts/run_level1_full_batch.mjs 消费
 */

function L(o) {
  return { schema_version: "logic_ir_v1", diagram_type: "logic", style: "iec", ...o };
}
function S(o) {
  return { schema_version: "state_ir_v1", diagram_type: "state", layout: "ring", ...o };
}
function W(o) {
  return { schema_version: "wave_ir_v1", diagram_type: "waveform", ...o };
}

/** 环形计数：states + /Y 输出串（按相邻环边；多余转移另给） */
function ringState(title, states, outs, extra = []) {
  const transitions = [];
  for (let i = 0; i < states.length; i++) {
    transitions.push({
      from: states[i],
      to: states[(i + 1) % states.length],
      label: outs[i] != null ? `/${outs[i]}` : undefined,
    });
  }
  return S({ title, states, transitions: [...transitions, ...extra] });
}

export const IRS = {
  // —— L ——
  L01: L({
    title: "referee",
    inputs: ["A", "B", "C"],
    gates: { G1: { type: "OR", inputs: ["B", "C"] }, G2: { type: "AND", inputs: ["A", "G1"] } },
    outputs: { Y: "G2" },
    notes: "Y=A*(B+C)",
  }),
  L02: L({
    title: "ex_2_5_3",
    inputs: ["A", "B", "C"],
    gates: {
      nB: { type: "NOT", inputs: ["B"] },
      t_bc: { type: "AND", inputs: ["nB", "C"] },
      t_sum: { type: "OR", inputs: ["A", "t_bc"] },
      t_nand: { type: "NOT", inputs: ["t_sum"] },
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      t_ab: { type: "AND", inputs: ["nA", "B"] },
      t_abc: { type: "AND", inputs: ["t_ab", "nC"] },
      t_or: { type: "OR", inputs: ["t_nand", "t_abc"] },
      Y: { type: "OR", inputs: ["t_or", "C"] },
    },
    outputs: { Y: "Y" },
    notes: "Y=(A+B'C)'+A'BC'+C",
  }),
  L03: L({
    title: "xor_nor",
    inputs: ["A", "B"],
    gates: {
      G1: { type: "NOR", inputs: ["A", "B"] },
      nA: { type: "NOT", inputs: ["A"] },
      nB: { type: "NOT", inputs: ["B"] },
      G2: { type: "NOR", inputs: ["nA", "nB"] },
      Y: { type: "NOR", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
    notes: "异或 NOR 展开",
  }),
  L04: L({
    title: "pla_y123_a",
    inputs: ["A", "B", "C", "D"],
    gates: {
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      nD: { type: "NOT", inputs: ["D"] },
      nB: { type: "NOT", inputs: ["B"] },
      a1: { type: "AND", inputs: ["A", "C"] },
      t_acd: { type: "AND", inputs: ["nA", "nC"] },
      a2: { type: "AND", inputs: ["t_acd", "D"] },
      y1a: { type: "OR", inputs: ["B", "a1"] },
      Y1: { type: "OR", inputs: ["y1a", "a2"] },
      a3: { type: "AND", inputs: ["nA", "D"] },
      a4: { type: "AND", inputs: ["B", "nD"] },
      Y2: { type: "OR", inputs: ["a3", "a4"] },
      a5: { type: "AND", inputs: ["nA", "C"] },
      t_abc: { type: "AND", inputs: ["A", "nB"] },
      a6: { type: "AND", inputs: ["t_abc", "nC"] },
      Y3: { type: "OR", inputs: ["a5", "a6"] },
    },
    outputs: { Y1: "Y1", Y2: "Y2", Y3: "Y3" },
    notes: "PLA",
  }),
  L05: L({
    title: "pla_y123_b",
    inputs: ["A", "B", "C", "D"],
    gates: {
      nA: { type: "NOT", inputs: ["A"] },
      nB: { type: "NOT", inputs: ["B"] },
      nC: { type: "NOT", inputs: ["C"] },
      nD: { type: "NOT", inputs: ["D"] },
      g1a: { type: "AND", inputs: ["nA", "nC"] },
      G1: { type: "AND", inputs: ["g1a", "D"] },
      G2: { type: "AND", inputs: ["B", "nD"] },
      g3a: { type: "AND", inputs: ["A", "nB"] },
      G3: { type: "AND", inputs: ["g3a", "C"] },
      g4a: { type: "AND", inputs: ["nA", "C"] },
      G4: { type: "AND", inputs: ["g4a", "D"] },
      Y1: { type: "OR", inputs: ["B", "G1"] },
      y2a: { type: "OR", inputs: ["G1", "G2"] },
      Y2: { type: "OR", inputs: ["y2a", "G4"] },
      y3a: { type: "OR", inputs: ["G2", "G3"] },
      Y3: { type: "OR", inputs: ["y3a", "G4"] },
    },
    outputs: { Y1: "Y1", Y2: "Y2", Y3: "Y3" },
  }),
  L06: L({
    title: "nand_net_2_9_2",
    inputs: ["A", "B", "C"],
    gates: {
      nB: { type: "NOT", inputs: ["B"] },
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      G1: { type: "NAND", inputs: ["A", "nB"] },
      G2: { type: "NAND", inputs: ["nA", "B"] },
      G3: { type: "NOT", inputs: ["G1"] },
      G4: { type: "NOT", inputs: ["G2"] },
      G5: { type: "NAND", inputs: ["G3", "nC"] },
      G6: { type: "NAND", inputs: ["nC", "G4"] },
      Y: { type: "NAND", inputs: ["G5", "G6"] },
    },
    outputs: { Y: "Y" },
  }),
  L07: L({
    title: "xor_and_2_9_3",
    inputs: ["A", "B", "Cn"],
    gates: {
      t1: { type: "XOR", inputs: ["A", "B"] },
      Y: { type: "AND", inputs: ["t1", "Cn"] },
    },
    outputs: { Y: "Y" },
  }),
  L08: L({
    title: "nand_aoi_2_9_4",
    inputs: ["A", "C", "B", "Cn"],
    gates: {
      G1: { type: "NAND", inputs: ["A", "C"] },
      G2: { type: "NAND", inputs: ["B", "Cn"] },
      Y: { type: "NAND", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
  }),
  L09: L({
    title: "nor_aoi_2_9_5",
    inputs: ["B", "C", "A", "Cn"],
    gates: {
      G1: { type: "NOR", inputs: ["B", "C"] },
      G2: { type: "NOR", inputs: ["A", "Cn"] },
      Y: { type: "NOR", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
  }),
  L10: L({
    title: "full_adder_4_1_1",
    inputs: ["A", "B", "CI"],
    gates: {
      s1: { type: "XOR", inputs: ["A", "B"] },
      S: { type: "XOR", inputs: ["s1", "CI"] },
      c1: { type: "AND", inputs: ["A", "B"] },
      c2: { type: "AND", inputs: ["s1", "CI"] },
      nor1: { type: "NOR", inputs: ["c1", "c2"] },
      CO: { type: "NOT", inputs: ["nor1"] },
    },
    outputs: { S: "S", CO: "CO" },
  }),

  // —— C ——
  C01: L({
    title: "ex_4_3_1_andor",
    inputs: ["R", "A", "G"],
    gates: {
      nR: { type: "NOT", inputs: ["R"] },
      nA: { type: "NOT", inputs: ["A"] },
      nG: { type: "NOT", inputs: ["G"] },
      t1: { type: "AND", inputs: ["R", "A"] },
      t2: { type: "AND", inputs: ["A", "G"] },
      t3: { type: "AND", inputs: ["R", "G"] },
      t4a: { type: "AND", inputs: ["nR", "nA"] },
      t4: { type: "AND", inputs: ["t4a", "nG"] },
      u1: { type: "OR", inputs: ["t1", "t2"] },
      u2: { type: "OR", inputs: ["t3", "t4"] },
      Z: { type: "OR", inputs: ["u1", "u2"] },
    },
    outputs: { Z: "Z" },
    notes: "Z=RA+AG+RG+R'A'G'",
  }),
  C02: L({
    title: "ex_4_3_1_nand",
    inputs: ["R", "A", "G"],
    gates: {
      nR: { type: "NOT", inputs: ["R"] },
      nA: { type: "NOT", inputs: ["A"] },
      nG: { type: "NOT", inputs: ["G"] },
      n1: { type: "NAND", inputs: ["R", "A"] },
      n2: { type: "NAND", inputs: ["A", "G"] },
      n3: { type: "NAND", inputs: ["R", "G"] },
      n4a: { type: "NAND", inputs: ["nR", "nA"] },
      n4: { type: "NAND", inputs: ["n4a", "nG"] },
      m1: { type: "NAND", inputs: ["n1", "n2"] },
      m2: { type: "NAND", inputs: ["n3", "n4"] },
      Z: { type: "NAND", inputs: ["m1", "m2"] },
    },
    outputs: { Z: "Z" },
    notes: "全 NAND；n4 课本为三输入",
  }),
  C03: L({
    title: "ex_4_3_1_nor",
    inputs: ["R", "A", "G"],
    gates: {
      nR: { type: "NOT", inputs: ["R"] },
      nA: { type: "NOT", inputs: ["A"] },
      nG: { type: "NOT", inputs: ["G"] },
      a1a: { type: "AND", inputs: ["R", "nA"] },
      a1: { type: "AND", inputs: ["a1a", "nG"] },
      a2a: { type: "AND", inputs: ["nR", "A"] },
      a2: { type: "AND", inputs: ["a2a", "nG"] },
      a3a: { type: "AND", inputs: ["nR", "nA"] },
      a3: { type: "AND", inputs: ["a3a", "G"] },
      o1: { type: "OR", inputs: ["a1", "a2"] },
      o2: { type: "OR", inputs: ["o1", "a3"] },
      Z: { type: "NOT", inputs: ["o2"] },
    },
    outputs: { Z: "Z" },
    notes: "课本三输入 NOR；语义 Z=!(exactly-one)",
  }),
  C04: L({
    title: "encoder_3bit",
    inputs: ["I1", "I2", "I3", "I4", "I5", "I6", "I7"],
    gates: {
      y2a: { type: "OR", inputs: ["I4", "I5"] },
      y2b: { type: "OR", inputs: ["I6", "I7"] },
      Y2: { type: "OR", inputs: ["y2a", "y2b"] },
      y1a: { type: "OR", inputs: ["I2", "I3"] },
      y1b: { type: "OR", inputs: ["I6", "I7"] },
      Y1: { type: "OR", inputs: ["y1a", "y1b"] },
      y0a: { type: "OR", inputs: ["I1", "I3"] },
      y0b: { type: "OR", inputs: ["I5", "I7"] },
      Y0: { type: "OR", inputs: ["y0a", "y0b"] },
    },
    outputs: { Y2: "Y2", Y1: "Y1", Y0: "Y0" },
    notes: "总线型编码器；版式难",
  }),
  C05: L({
    title: "mux2_1",
    inputs: ["A", "SEL", "B"],
    gates: {
      G1: { type: "AND", inputs: ["A", "SEL"] },
      G2: { type: "NOT", inputs: ["SEL"] },
      G3: { type: "AND", inputs: ["G2", "B"] },
      Y: { type: "OR", inputs: ["G1", "G3"] },
    },
    outputs: { Y: "Y" },
  }),
  C06: L({
    title: "half_adder",
    inputs: ["A", "B"],
    gates: {
      S: { type: "XOR", inputs: ["A", "B"] },
      CO: { type: "AND", inputs: ["A", "B"] },
    },
    outputs: { S: "S", CO: "CO" },
  }),
  C07: L({
    title: "full_adder",
    inputs: ["CI", "A", "B"],
    gates: {
      XOR1: { type: "XOR", inputs: ["A", "B"] },
      Sum: { type: "XOR", inputs: ["CI", "XOR1"] },
      AND1: { type: "AND", inputs: ["A", "B"] },
      AND2: { type: "AND", inputs: ["B", "CI"] },
      AND3: { type: "AND", inputs: ["A", "CI"] },
      t1: { type: "OR", inputs: ["AND1", "AND2"] },
      Cout: { type: "OR", inputs: ["t1", "AND3"] },
    },
    outputs: { Sum: "Sum", Cout: "Cout" },
  }),
  C08: L({
    title: "decoder_74hc138_approx",
    inputs: ["A0", "A1", "A2", "S1", "S2n", "S3n"],
    gates: {
      nS1: { type: "NOT", inputs: ["S1"] },
      enA: { type: "AND", inputs: ["nS1", "S2n"] },
      S: { type: "AND", inputs: ["enA", "S3n"] },
      nA0: { type: "NOT", inputs: ["A0"] },
      nA1: { type: "NOT", inputs: ["A1"] },
      nA2: { type: "NOT", inputs: ["A2"] },
      // 仅展开 Y0'/Y7' 示意 + 用 DECODER 主体
      D: { type: "DECODER", inputs: ["A0", "A1", "A2"] },
      y0a: { type: "AND", inputs: ["nA0", "nA1"] },
      y0b: { type: "AND", inputs: ["y0a", "nA2"] },
      Y0n: { type: "NAND", inputs: ["S", "y0b"] },
      y7a: { type: "AND", inputs: ["A0", "A1"] },
      y7b: { type: "AND", inputs: ["y7a", "A2"] },
      Y7n: { type: "NAND", inputs: ["S", "y7b"] },
    },
    outputs: { Y0n: "Y0n", Y7n: "Y7n", D: "D" },
    notes: "138 门级过密；IR 示意 enable+两端译码，完整 8 路建议 C",
    _tier: "C",
  }),
  C09: L({
    title: "decoder_74hc42_approx",
    inputs: ["A0", "A1", "A2", "A3"],
    gates: {
      D: { type: "DECODER", inputs: ["A0", "A1", "A2", "A3"] },
      nA0: { type: "NOT", inputs: ["A0"] },
      nA1: { type: "NOT", inputs: ["A1"] },
      nA2: { type: "NOT", inputs: ["A2"] },
      nA3: { type: "NOT", inputs: ["A3"] },
      y0a: { type: "AND", inputs: ["nA0", "nA1"] },
      y0b: { type: "AND", inputs: ["nA2", "nA3"] },
      Y0n: { type: "NAND", inputs: ["y0a", "y0b"] },
    },
    outputs: { D: "D", Y0n: "Y0n" },
    notes: "BCD 译码器总线图 → C/B",
    _tier: "C",
  }),
  C10: L({
    title: "mux_74hc153_approx",
    inputs: ["A0", "A1", "D0", "D1", "D2", "D3", "Sn"],
    gates: {
      nA0: { type: "NOT", inputs: ["A0"] },
      nA1: { type: "NOT", inputs: ["A1"] },
      nSn: { type: "NOT", inputs: ["Sn"] },
      m0a: { type: "AND", inputs: ["D0", "nA0"] },
      m0: { type: "AND", inputs: ["m0a", "nA1"] },
      m1a: { type: "AND", inputs: ["D1", "A0"] },
      m1: { type: "AND", inputs: ["m1a", "nA1"] },
      m2a: { type: "AND", inputs: ["D2", "nA0"] },
      m2: { type: "AND", inputs: ["m2a", "A1"] },
      m3a: { type: "AND", inputs: ["D3", "A0"] },
      m3: { type: "AND", inputs: ["m3a", "A1"] },
      s01: { type: "OR", inputs: ["m0", "m1"] },
      s23: { type: "OR", inputs: ["m2", "m3"] },
      sum: { type: "OR", inputs: ["s01", "s23"] },
      Y: { type: "AND", inputs: ["sum", "nSn"] },
    },
    outputs: { Y: "Y" },
    notes: "单路 4 选 1（课本双路）；TG 树简化为 AND-OR",
    _tier: "B",
  }),

  // —— F ——
  F01: L({
    title: "nor_latch",
    inputs: ["VI1", "VI2"],
    gates: {
      G1: { type: "NOR", inputs: ["VI1", "G2"] },
      G2: { type: "NOR", inputs: ["VI2", "G1"] },
    },
    outputs: { VO1: "G1", VO2: "G2" },
    notes: "交叉耦合 NOR；版式镜像",
    _tier: "B",
  }),
  F02: L({
    title: "nand_sr_latch",
    inputs: ["SDn", "RDn"],
    gates: {
      G1: { type: "NAND", inputs: ["SDn", "G2"] },
      G2: { type: "NAND", inputs: ["RDn", "G1"] },
    },
    outputs: { Q: "G1", Qn: "G2" },
    _tier: "B",
  }),
  F03: L({
    title: "gated_sr",
    inputs: ["S", "R", "CLK"],
    gates: {
      G3: { type: "NAND", inputs: ["S", "CLK"] },
      G4: { type: "NAND", inputs: ["R", "CLK"] },
      G1: { type: "NAND", inputs: ["G3", "G2"] },
      G2: { type: "NAND", inputs: ["G4", "G1"] },
    },
    outputs: { Q: "G1", Qn: "G2" },
    _tier: "B",
  }),
  F04: L({
    title: "gated_d",
    inputs: ["D", "CLK"],
    gates: {
      nD: { type: "NOT", inputs: ["D"] },
      Sn: { type: "NAND", inputs: ["D", "CLK"] },
      Rn: { type: "NAND", inputs: ["nD", "CLK"] },
      G1: { type: "NAND", inputs: ["Sn", "G2"] },
      G2: { type: "NAND", inputs: ["Rn", "G1"] },
    },
    outputs: { Q: "G1", Qn: "G2" },
    _tier: "B",
  }),
  F05: L({
    title: "ms_d_ff",
    inputs: ["D", "CLK"],
    gates: {
      nCLK: { type: "NOT", inputs: ["CLK"] },
      FF1: { type: "LATCH_D", inputs: ["D", "nCLK"] },
      FF2: { type: "LATCH_D", inputs: ["FF1", "CLK"] },
      Qn: { type: "NOT", inputs: ["FF2"] },
    },
    outputs: { Q: "FF2", Qn: "Qn" },
    notes: "主从用 LATCH_D 近似",
    _tier: "B",
  }),
  F06: L({
    title: "ex_6_2_1_jk",
    inputs: ["CLK"],
    gates: {
      // 简化：用 JKFF 原语 + 组合；反馈用 Q 输出
      FF1: { type: "JKFF", inputs: ["FB", "ONE", "CLK"] },
      nQ1: { type: "NOT", inputs: ["FF1"] },
      ONE: { type: "OR", inputs: ["CLK", "nCLK"] }, // 占位恒 1 近似：用 BUF 链
      nCLK: { type: "NOT", inputs: ["CLK"] },
      NAND_mid: { type: "NAND", inputs: ["nQ1", "FB"] },
      FF2: { type: "JKFF", inputs: ["FF1", "NAND_mid", "CLK"] },
      AND_j3: { type: "AND", inputs: ["FF1", "FF2"] },
      nQ3: { type: "NOT", inputs: ["FF3"] },
      FF3: { type: "JKFF", inputs: ["AND_j3", "nQ3", "CLK"] },
      FB: { type: "NAND", inputs: ["FF2", "FF3"] },
      Y: { type: "NOT", inputs: ["FB"] },
    },
    outputs: { Y: "Y", Q1: "FF1", Q2: "FF2", Q3: "FF3" },
    notes: "例6.2.1 简化；恒1 用 OR(CLK,nCLK)",
    _tier: "B",
  }),
  F07: L({
    title: "ex_6_2_3",
    inputs: ["A", "CLK"],
    gates: {
      nQ1: { type: "NOT", inputs: ["FF1"] },
      FF1: { type: "DFF", inputs: ["nQ1", "CLK"] },
      x1: { type: "XOR", inputs: ["FF1", "A"] },
      D2: { type: "XOR", inputs: ["x1", "FF2"] },
      FF2: { type: "DFF", inputs: ["D2", "CLK"] },
      nA: { type: "NOT", inputs: ["A"] },
      t1a: { type: "AND", inputs: ["nA", "FF1"] },
      t1: { type: "AND", inputs: ["t1a", "FF2"] },
      nQ1b: { type: "NOT", inputs: ["FF1"] },
      nQ2: { type: "NOT", inputs: ["FF2"] },
      t2a: { type: "AND", inputs: ["A", "nQ1b"] },
      t2: { type: "AND", inputs: ["t2a", "nQ2"] },
      Y: { type: "OR", inputs: ["t1", "t2"] },
    },
    outputs: { Y: "Y", Q1: "FF1", Q2: "FF2" },
    _tier: "B",
  }),
  F08: L({
    title: "shift_reg_4",
    inputs: ["DI", "CLK"],
    gates: {
      Q0: { type: "DFF", inputs: ["DI", "CLK"] },
      Q1: { type: "DFF", inputs: ["Q0", "CLK"] },
      Q2: { type: "DFF", inputs: ["Q1", "CLK"] },
      Q3: { type: "DFF", inputs: ["Q2", "CLK"] },
    },
    outputs: { Q0: "Q0", Q1: "Q1", Q2: "Q2", Q3: "Q3" },
    _tier: "B",
  }),
  F09: L({
    title: "sync_bin_counter_T",
    inputs: ["CLK"],
    gates: {
      ONE: { type: "OR", inputs: ["CLK", "nCLK"] },
      nCLK: { type: "NOT", inputs: ["CLK"] },
      Q0: { type: "TFF", inputs: ["ONE", "CLK"] },
      Q1: { type: "TFF", inputs: ["Q0", "CLK"] },
      T2: { type: "AND", inputs: ["Q0", "Q1"] },
      Q2: { type: "TFF", inputs: ["T2", "CLK"] },
      T3a: { type: "AND", inputs: ["Q0", "Q1"] },
      T3: { type: "AND", inputs: ["T3a", "Q2"] },
      Q3: { type: "TFF", inputs: ["T3", "CLK"] },
      Ca: { type: "AND", inputs: ["Q0", "Q1"] },
      Cb: { type: "AND", inputs: ["Q2", "Q3"] },
      C: { type: "AND", inputs: ["Ca", "Cb"] },
    },
    outputs: { Q0: "Q0", Q1: "Q1", Q2: "Q2", Q3: "Q3", C: "C" },
    notes: "对应 fig_6_3_8_01faea9b 计数器",
    _tier: "B",
  }),
  F10: L({
    title: "ex_6_4_3",
    inputs: ["A", "B", "CLK"],
    gates: {
      nA: { type: "NOT", inputs: ["A"] },
      nB: { type: "NOT", inputs: ["B"] },
      nQ1: { type: "NOT", inputs: ["Q1"] },
      nQ0: { type: "NOT", inputs: ["Q0"] },
      d1a: { type: "AND", inputs: ["Q1", "nA"] },
      d1b: { type: "AND", inputs: ["d1a", "nB"] },
      d1c: { type: "AND", inputs: ["nQ1", "nQ0"] },
      d1d: { type: "AND", inputs: ["d1c", "A"] },
      d1e: { type: "AND", inputs: ["Q0", "B"] },
      d1f: { type: "OR", inputs: ["d1b", "d1d"] },
      D1: { type: "OR", inputs: ["d1f", "d1e"] },
      d0a: { type: "AND", inputs: ["nQ1", "nQ0"] },
      d0b: { type: "AND", inputs: ["d0a", "B"] },
      d0c: { type: "AND", inputs: ["Q0", "nA"] },
      d0d: { type: "AND", inputs: ["d0c", "nB"] },
      D0: { type: "OR", inputs: ["d0b", "d0d"] },
      Q1: { type: "DFF", inputs: ["D1", "CLK"] },
      Q0: { type: "DFF", inputs: ["D0", "CLK"] },
      ya: { type: "AND", inputs: ["Q1", "B"] },
      yb: { type: "AND", inputs: ["Q1", "A"] },
      yc: { type: "AND", inputs: ["Q0", "A"] },
      yd: { type: "OR", inputs: ["ya", "yb"] },
      Y: { type: "OR", inputs: ["yd", "yc"] },
      Z: { type: "AND", inputs: ["Q1", "A"] },
    },
    outputs: { Y: "Y", Z: "Z", Q1: "Q1", Q0: "Q0" },
    _tier: "B",
  }),

  // —— S ——
  S01: ringState(
    "fig_6_2_2",
    ["000", "001", "010", "011", "100", "101", "110", "111"],
    ["0", "0", "0", "0", "0", "0", "1", "1"],
    // 修正环：110→000 而非 110→111；111→000
    []
  ),
  S02: S({
    title: "fig_6_2_4",
    states: ["00", "01", "10", "11"],
    transitions: [
      { from: "00", to: "01", label: "0/0" },
      { from: "00", to: "11", label: "1/1" },
      { from: "01", to: "10", label: "0/0" },
      { from: "01", to: "00", label: "1/0" },
      { from: "10", to: "11", label: "0/0" },
      { from: "10", to: "01", label: "1/0" },
      { from: "11", to: "00", label: "0/1" },
      { from: "11", to: "10", label: "1/0" },
    ],
  }),
  S03: (() => {
    const states = [];
    for (let i = 0; i < 10; i++) states.push(i.toString(2).padStart(4, "0"));
    // 加自启动相关态
    ["1010", "1011", "1100", "1101", "1110", "1111"].forEach((s) => {
      if (!states.includes(s)) states.push(s);
    });
    const transitions = [];
    for (let i = 0; i < 9; i++) {
      transitions.push({
        from: states[i],
        to: states[i + 1],
        label: "/0",
      });
    }
    transitions.push({ from: "1001", to: "0000", label: "/1" });
    transitions.push({ from: "1010", to: "1011", label: "/0" });
    transitions.push({ from: "1011", to: "0100", label: "/1" });
    transitions.push({ from: "1100", to: "1101", label: "/0" });
    transitions.push({ from: "1101", to: "0100", label: "/1" });
    transitions.push({ from: "1110", to: "1111", label: "/0" });
    transitions.push({ from: "1111", to: "0000", label: "/1" });
    return S({ title: "fig_6_2_11", states, transitions });
  })(),
  S04: (() => {
    const states = [];
    for (let i = 0; i < 16; i++) states.push(i.toString(2).padStart(4, "0"));
    const transitions = [];
    for (let i = 0; i < 15; i++) {
      transitions.push({ from: states[i], to: states[i + 1], label: "/0" });
    }
    transitions.push({ from: "1111", to: "0000", label: "/1" });
    return S({ title: "fig_6_3_9", states, transitions });
  })(),
  S05: (() => {
    const states = Array.from({ length: 13 }, (_, i) => `S${i}`);
    const transitions = [];
    for (let i = 0; i < 12; i++) {
      transitions.push({ from: `S${i}`, to: `S${i + 1}`, label: "/0" });
    }
    transitions.push({ from: "S12", to: "S0", label: "/1" });
    return S({ title: "fig_6_4_2", states, transitions });
  })(),
  S06: S({
    title: "fig_6_4_7",
    states: ["S0", "S1", "S2", "S3"],
    transitions: [
      { from: "S0", to: "S0", label: "0/0" },
      { from: "S0", to: "S1", label: "1/0" },
      { from: "S1", to: "S0", label: "0/0" },
      { from: "S1", to: "S2", label: "1/0" },
      { from: "S2", to: "S0", label: "0/0" },
      { from: "S2", to: "S3", label: "1/1" },
      { from: "S3", to: "S0", label: "0/0" },
      { from: "S3", to: "S3", label: "1/1" },
    ],
  }),
  S07: S({
    title: "fig_6_4_8",
    states: ["S0", "S1", "S2"],
    transitions: [
      { from: "S0", to: "S0", label: "0/0" },
      { from: "S0", to: "S1", label: "1/0" },
      { from: "S1", to: "S0", label: "0/0" },
      { from: "S1", to: "S2", label: "1/0" },
      { from: "S2", to: "S0", label: "0/0" },
      { from: "S2", to: "S2", label: "1/1" },
    ],
  }),
  S08: S({
    title: "fig_6_4_14",
    states: ["S0", "S1", "S2"],
    transitions: [
      { from: "S0", to: "S0", label: "00/00" },
      { from: "S0", to: "S1", label: "01/00" },
      { from: "S0", to: "S2", label: "10/00" },
      { from: "S1", to: "S1", label: "00/00" },
      { from: "S1", to: "S2", label: "01/00" },
      { from: "S1", to: "S0", label: "10/10" },
      { from: "S2", to: "S2", label: "00/00" },
      { from: "S2", to: "S0", label: "01/10" },
      { from: "S2", to: "S0", label: "10/11" },
    ],
  }),
  S09: S({
    title: "fig_6_4_19",
    states: ["001", "100", "010", "101", "110", "111", "011"],
    transitions: [
      { from: "001", to: "100", label: "/0" },
      { from: "100", to: "010", label: "/0" },
      { from: "010", to: "101", label: "/0" },
      { from: "101", to: "110", label: "/0" },
      { from: "110", to: "111", label: "/0" },
      { from: "111", to: "011", label: "/0" },
      { from: "011", to: "001", label: "/1" },
    ],
  }),
  S10: S({
    title: "fig_6_4_26",
    states: ["100", "010", "001", "000", "110", "011", "111", "101"],
    transitions: [
      { from: "100", to: "010", label: "" },
      { from: "010", to: "001", label: "" },
      { from: "001", to: "100", label: "" },
      { from: "000", to: "100", label: "" },
      { from: "110", to: "011", label: "" },
      { from: "011", to: "001", label: "" },
      { from: "111", to: "011", label: "" },
      { from: "101", to: "010", label: "" },
    ],
  }),

  // —— W ——
  W01: W({
    title: "fig_2_5_3",
    signals: [
      { name: "A", wave: "00001111" },
      { name: "B", wave: "00110011" },
      { name: "C", wave: "01010101" },
      { name: "Y", wave: "00000111" },
    ],
  }),
  W02: W({
    title: "fig_2_5_6",
    signals: [
      { name: "A", wave: "0000111100001111" },
      { name: "B", wave: "0011001100110011" },
      { name: "C", wave: "0101010101010101" },
      { name: "Y", wave: "0110011001100110" },
    ],
  }),
  W03: W({
    title: "fig_5_2_3_wave_approx",
    signals: [
      { name: "SDn", wave: "011111110111" },
      { name: "RDn", wave: "111101111111" },
      { name: "Q", wave: "001111000111" },
      { name: "Qn", wave: "110000111000" },
    ],
    notes: "原 JPG 仅电路；波形为示意",
  }),
  W04: W({
    title: "fig_5_3_3",
    signals: [
      { name: "CLK", wave: "01110001110000" },
      { name: "S", wave: "11000000000100" },
      { name: "R", wave: "00000111110000" },
      { name: "Q", wave: "01111110000000" },
      { name: "Qn", wave: "10000001111111" },
    ],
  }),
  W05: W({
    title: "fig_5_3_6",
    signals: [
      { name: "CLK", wave: "0011100011111000" },
      { name: "D", wave: "1110000001011100" },
      { name: "Q", wave: "0010000001011111" },
      { name: "Qn", wave: "1101111110100000" },
    ],
  }),
  W06: W({
    title: "fig_5_3_9",
    signals: [
      { name: "CLK", wave: "0101010101" },
      { name: "D", wave: "0110001011" },
      { name: "Q", wave: "0011000011" },
    ],
  }),
  W07: W({
    title: "fig_5_3_11",
    signals: [
      { name: "CLK", wave: "011100011100" },
      { name: "S", wave: "001100000000" },
      { name: "R", wave: "000001100000" },
      { name: "Q1", wave: "001110000000" },
      { name: "Q", wave: "000011100000" },
    ],
  }),
  W08: W({
    title: "fig_5_3_14",
    signals: [
      { name: "CLK", wave: "01010101010101" },
      { name: "J", wave: "01100110000000" },
      { name: "K", wave: "10011000011111" },
      { name: "Q", wave: "00110011110000" },
      { name: "Qn", wave: "11001100001111" },
    ],
  }),
  W09: W({
    title: "fig_6_3_2",
    signals: [
      { name: "DI", wave: "1011" },
      { name: "Q0", wave: "1011" },
      { name: "Q1", wave: "0101" },
      { name: "Q2", wave: "0010" },
      { name: "Q3", wave: "0001" },
    ],
  }),
  W10: W({
    title: "fig_6_3_7",
    signals: [
      { name: "S1", wave: "11100000" },
      { name: "S0", wave: "11111111" },
      { name: "CLK1", wave: "01010101" },
      { name: "CLK2", wave: "01010000" },
    ],
  }),
};

/** S01 环边修正：110→000 而非进 111 */
IRS.S01 = S({
  title: "fig_6_2_2",
  states: ["000", "001", "010", "011", "100", "101", "110", "111"],
  transitions: [
    { from: "000", to: "001", label: "/0" },
    { from: "001", to: "010", label: "/0" },
    { from: "010", to: "011", label: "/0" },
    { from: "011", to: "100", label: "/0" },
    { from: "100", to: "101", label: "/0" },
    { from: "101", to: "110", label: "/0" },
    { from: "110", to: "000", label: "/1" },
    { from: "111", to: "000", label: "/1" },
  ],
});
