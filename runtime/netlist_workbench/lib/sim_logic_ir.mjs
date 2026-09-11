/**
 * logic_ir_v1 → 组合逻辑求值 / 真值表
 * 时序门（DFF/LATCH/JK…）标记为 unsupported
 */
const SEQ = new Set([
  "DFF", "JKFF", "SRFF", "TFF", "LATCH_SR", "LATCH_D",
  "COUNTER", "SHIFT_REG",
]);

const MSI = new Set([
  "MUX", "DEMUX", "DECODER", "ENCODER",
  "TRISTATE_BUF", "TRISTATE_INV", "OPEN_DRAIN", "SCHMITT",
]);

function normType(t) {
  return String(t || "").toUpperCase().replace(/\d+$/, (m, off, s) => {
    // AND3 → AND, keep base
    if (/^(AND|OR|NAND|NOR|XOR|XNOR)\d+$/.test(s)) return "";
    return m;
  });
}

function gateArityType(type) {
  const t = String(type || "").toUpperCase();
  const m = t.match(/^(AND|OR|NAND|NOR|XOR|XNOR)(\d+)?$/);
  if (m) return { base: m[1], n: m[2] ? +m[2] : null };
  return { base: t, n: null };
}

function evalGate(type, args) {
  const { base } = gateArityType(type);
  const a = args.map(Boolean);
  switch (base) {
    case "AND":
      return a.every(Boolean) ? 1 : 0;
    case "OR":
      return a.some(Boolean) ? 1 : 0;
    case "NAND":
      return a.every(Boolean) ? 0 : 1;
    case "NOR":
      return a.some(Boolean) ? 0 : 1;
    case "NOT":
      return a[0] ? 0 : 1;
    case "BUF":
      return a[0] ? 1 : 0;
    case "XOR":
      return a.reduce((x, y) => x ^ y, 0);
    case "XNOR":
      return a.reduce((x, y) => x ^ y, 0) ? 0 : 1;
    default:
      throw new Error(`unsupported gate type for sim: ${type}`);
  }
}

function topoOrder(ir) {
  const gates = ir.gates || {};
  const inputs = new Set(ir.inputs || []);
  const visiting = new Set();
  const visited = new Set();
  const order = [];
  let cyclic = false;

  function visit(id) {
    if (visited.has(id) || inputs.has(id)) return;
    if (!gates[id]) return;
    if (visiting.has(id)) {
      cyclic = true;
      return;
    }
    visiting.add(id);
    for (const src of gates[id].inputs || []) visit(src);
    visiting.delete(id);
    visited.add(id);
    order.push(id);
  }
  for (const id of Object.keys(gates)) visit(id);
  return { order, cyclic };
}

export function classifyIr(ir) {
  const types = Object.values(ir.gates || {}).map((g) => String(g.type).toUpperCase());
  const hasSeq = types.some((t) => SEQ.has(t) || SEQ.has(gateArityType(t).base));
  const hasMsi = types.some((t) => MSI.has(t));
  return { hasSeq, hasMsi, combinational: !hasSeq && !hasMsi };
}

export function evalIr(ir, assignment) {
  const { order, cyclic } = topoOrder(ir);
  if (cyclic) throw new Error("cyclic combinational loop");
  const vals = { ...assignment };
  for (const name of ir.inputs || []) {
    if (!(name in vals)) throw new Error(`missing input ${name}`);
    vals[name] = vals[name] ? 1 : 0;
  }
  for (const id of order) {
    const g = ir.gates[id];
    const args = (g.inputs || []).map((s) => {
      if (!(s in vals)) throw new Error(`unknown net ${s} for gate ${id}`);
      return vals[s];
    });
    vals[id] = evalGate(g.type, args);
  }
  const outs = {};
  for (const [port, src] of Object.entries(ir.outputs || {})) {
    if (!(src in vals)) throw new Error(`output ${port} drives unknown ${src}`);
    outs[port] = vals[src];
  }
  return { nets: vals, outputs: outs };
}

export function truthTable(ir, maxRows = 256) {
  const cls = classifyIr(ir);
  if (!cls.combinational) {
    return {
      ok: false,
      reason: cls.hasSeq ? "sequential_unsupported" : "msi_unsupported",
      rows: [],
    };
  }
  const inputs = ir.inputs || [];
  const n = inputs.length;
  if (n === 0) {
    const { outputs } = evalIr(ir, {});
    return {
      ok: true,
      reason: "ok",
      rows: [{ inputs: {}, outputs }],
      inputs,
      outputs: Object.keys(ir.outputs || {}),
      total: 1,
    };
  }
  if (n > 12) {
    return { ok: false, reason: "too_many_inputs", rows: [], n };
  }
  const { cyclic } = topoOrder(ir);
  if (cyclic) {
    return { ok: false, reason: "cyclic_combinational", rows: [], inputs, outputs: Object.keys(ir.outputs || {}) };
  }
  const total = 1 << n;
  const rows = [];
  const step = total <= maxRows ? 1 : Math.ceil(total / maxRows);
  for (let mask = 0; mask < total; mask += step) {
    const assignment = {};
    for (let i = 0; i < n; i++) assignment[inputs[i]] = (mask >> (n - 1 - i)) & 1;
    const { outputs } = evalIr(ir, assignment);
    rows.push({ inputs: assignment, outputs });
  }
  return {
    ok: true,
    reason: step === 1 ? "ok" : "sampled_full_space",
    rows,
    inputs,
    outputs: Object.keys(ir.outputs || {}),
    total,
    sampled: step > 1,
  };
}

/** 抽样几行给人看 */
export function sampleTruth(ir, limit = 8) {
  const tt = truthTable(ir);
  if (!tt.ok) return tt;
  const step = Math.max(1, Math.floor(tt.rows.length / limit));
  const samples = [];
  for (let i = 0; i < tt.rows.length && samples.length < limit; i += step) {
    samples.push(tt.rows[i]);
  }
  return { ...tt, samples, total: tt.total ?? tt.rows.length };
}
