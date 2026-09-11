/**
 * 自检：仿真正确 + 多输入符号未误拆 + 渲染产物基本健全
 * 供 batch / 未来实装流水线共用
 */
import { classifyIr, truthTable, evalIr } from "./sim_logic_ir.mjs";
import { logicIrToYosysJson } from "./ir_to_yosys_json.mjs";

/** 两张卡真值表是否一致（同输入集） */
export function compareTruth(irA, irB) {
  const a = truthTable(irA);
  const b = truthTable(irB);
  if (!a.ok || !b.ok) {
    return { ok: false, reason: `tt_fail:${a.reason}/${b.reason}` };
  }
  if ((irA.inputs || []).join() !== (irB.inputs || []).join()) {
    return { ok: false, reason: "input_mismatch" };
  }
  const outsA = Object.keys(irA.outputs || {});
  const outsB = Object.keys(irB.outputs || {});
  if (outsA.join() !== outsB.join()) {
    return { ok: false, reason: "output_mismatch" };
  }
  for (let i = 0; i < a.rows.length; i++) {
    for (const o of outsA) {
      if (a.rows[i].outputs[o] !== b.rows[i].outputs[o]) {
        return {
          ok: false,
          reason: "value_mismatch",
          at: a.rows[i].inputs,
          out: o,
          got: [a.rows[i].outputs[o], b.rows[i].outputs[o]],
        };
      }
    }
  }
  return { ok: true, rows: a.rows.length };
}

/**
 * @param {object} ir
 * @param {{ svg?: string, yosysMeta?: object, peerIr?: object, peerLabel?: string }} extra
 */
export function selfCheck(ir, extra = {}) {
  const checks = [];
  const cls = classifyIr(ir);

  const tt = truthTable(ir);
  checks.push({
    id: "SIM",
    ok: !!tt.ok,
    detail: tt.ok ? `rows=${tt.total ?? tt.rows.length}` : tt.reason,
  });

  const built = extra.yosysMeta
    ? { meta: extra.yosysMeta }
    : logicIrToYosysJson(ir, "chk");
  const meta = built.meta;
  const splits = meta.fallbackSplits || [];
  const highFan = Object.entries(ir.gates || {}).filter(
    ([, g]) => (g.inputs || []).length >= 3
  );
  const multiOk = highFan.every(([id]) => {
    const m = meta.gateMeta.find((x) => x.id === id);
    return m && m.mode === "multi";
  });
  checks.push({
    id: "SYMBOL_MULTI",
    ok: multiOk && splits.length === 0,
    detail: multiOk
      ? `multi_gates=${meta.multiGates}`
      : `fallback=${splits.map((s) => s.id).join(",") || "none"} high=${highFan.map(([id]) => id).join(",")}`,
  });

  const badMulti = meta.gateMeta.filter(
    (g) => g.mode === "multi" && g.arity >= 3 && g.cells !== 1
  );
  checks.push({
    id: "CELL_COUNT",
    ok: badMulti.length === 0,
    detail: `cells=${meta.cellCount} ir_gates=${Object.keys(ir.gates || {}).length}`,
  });

  if (extra.svg) {
    const missing = [];
    for (const g of meta.gateMeta) {
      if (g.mode !== "multi" || g.arity < 3) continue;
      const tip = g.base.toLowerCase() + g.arity;
      const alias = `$_${g.base}${g.arity}_`;
      if (!extra.svg.includes(alias) && !extra.svg.includes(`s:type="${tip}"`)) {
        missing.push(`${g.id}:${tip}`);
      }
    }
    const hasGeom = /<path |<line /.test(extra.svg);
    checks.push({
      id: "RENDER_SVG",
      ok: hasGeom && missing.length === 0,
      detail: hasGeom
        ? missing.length
          ? `missing_skin=${missing.join(",")}`
          : `bytes=${extra.svg.length}`
        : "empty_or_no_geom",
    });
  } else {
    checks.push({ id: "RENDER_SVG", ok: true, detail: "skipped" });
  }

  if (extra.peerIr) {
    const cmp = compareTruth(ir, extra.peerIr);
    checks.push({
      id: "PEER_EQ",
      ok: cmp.ok,
      detail: cmp.ok
        ? `eq_${extra.peerLabel || "peer"} rows=${cmp.rows}`
        : `${extra.peerLabel || "peer"}:${cmp.reason}`,
    });
  }

  if (cls.combinational && (ir.inputs || []).length > 0 && tt.ok) {
    try {
      const assign = {};
      for (const name of ir.inputs) assign[name] = Math.random() < 0.5 ? 1 : 0;
      evalIr(ir, assign);
      checks.push({ id: "EVAL_SMOKE", ok: true, detail: "ok" });
    } catch (e) {
      checks.push({ id: "EVAL_SMOKE", ok: false, detail: e.message });
    }
  }

  const ok = checks.every((c) => c.ok);
  return {
    ok,
    grade: ok ? "SELF_OK" : "SELF_FAIL",
    checks,
    meta,
    combinational: cls.combinational,
  };
}

export function summarizeChecks(report) {
  return (report.checks || [])
    .map((c) => `${c.ok ? "OK" : "FAIL"}:${c.id}`)
    .join(" ");
}
