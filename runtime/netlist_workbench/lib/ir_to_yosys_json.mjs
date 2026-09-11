/**
 * logic_ir_v1 → Yosys JSON（供 netlistsvg）
 * 优先多输入单符号；skin 无对应 arity 时降级二元树
 */
const SEQ_TYPE = {
  DFF: "$_DFF_P_",
  DFF_P: "$_DFF_P_",
  DFF_N: "$_DFF_N_",
};

const MSI_STUB = new Set([
  "DECODER", "ENCODER", "MUX", "DEMUX",
  "TRISTATE_BUF", "TRISTATE_INV", "OPEN_DRAIN", "SCHMITT",
]);

const BIN_TYPE = {
  AND: "$_AND_",
  OR: "$_OR_",
  NAND: "$_NAND_",
  NOR: "$_NOR_",
  XOR: "$_XOR_",
  XNOR: "$_XNOR_",
  NOT: "$_NOT_",
};

/** skin 已提供的多输入类型（arity → alias） */
const MULTI_OK = new Set(["AND", "OR", "NAND", "NOR"]);
const MULTI_MAX = 4;
const PORT_IN = ["A", "B", "C", "D", "E", "F", "G", "H"];

function baseType(type) {
  const t = String(type || "").toUpperCase();
  const m = t.match(/^(AND|OR|NAND|NOR|XOR|XNOR|NOT|BUF)(\d+)?$/);
  if (m) return m[1];
  return t;
}

function multiAlias(base, arity) {
  return `$_${base}${arity}_`;
}

export function logicIrToYosysJson(ir, moduleName = "top", opts = {}) {
  const preferMulti = opts.preferMulti !== false;
  const multiMax = opts.multiMax ?? MULTI_MAX;

  let nextBit = 2;
  const netBit = new Map();

  function bitOf(name) {
    if (!netBit.has(name)) netBit.set(name, nextBit++);
    return netBit.get(name);
  }

  for (const inp of ir.inputs || []) bitOf(inp);
  for (const id of Object.keys(ir.gates || {})) bitOf(id);

  const ports = {};
  for (const inp of ir.inputs || []) {
    ports[inp] = { direction: "input", bits: [bitOf(inp)] };
  }
  for (const [outName, src] of Object.entries(ir.outputs || {})) {
    const portName = ports[outName] ? `${outName}_o` : outName;
    ports[portName] = { direction: "output", bits: [bitOf(src)] };
  }

  const cells = {};
  let cellSeq = 0;
  const gateMeta = [];

  function addUnary(yosysType, a, yName) {
    const id = `c${cellSeq++}`;
    cells[id] = {
      type: yosysType,
      port_directions: { A: "input", Y: "output" },
      connections: { A: [bitOf(a)], Y: [bitOf(yName)] },
    };
    return id;
  }

  function addBinary(yosysType, a, b, yName) {
    const id = `c${cellSeq++}`;
    cells[id] = {
      type: yosysType,
      port_directions: { A: "input", B: "input", Y: "output" },
      connections: { A: [bitOf(a)], B: [bitOf(b)], Y: [bitOf(yName)] },
    };
    return id;
  }

  function addMulti(yosysType, sources, yName) {
    const id = `c${cellSeq++}`;
    const port_directions = { Y: "output" };
    const connections = { Y: [bitOf(yName)] };
    sources.forEach((src, i) => {
      const p = PORT_IN[i];
      port_directions[p] = "input";
      connections[p] = [bitOf(src)];
    });
    cells[id] = { type: yosysType, port_directions, connections };
    return id;
  }

  function addDff(yosysType, d, clk, qName) {
    const id = `c${cellSeq++}`;
    cells[id] = {
      type: yosysType,
      port_directions: { D: "input", CLK: "input", Q: "output" },
      connections: { D: [bitOf(d)], CLK: [bitOf(clk)], Q: [bitOf(qName)] },
    };
    return id;
  }

  function reduceBinaryTree(yosysType, sources, outName) {
    let cur = sources[0];
    const cellIds = [];
    for (let i = 1; i < sources.length; i++) {
      const isLast = i === sources.length - 1;
      const y = isLast ? outName : `${outName}_t${i}`;
      if (!isLast) bitOf(y);
      cellIds.push(addBinary(yosysType, cur, sources[i], y));
      cur = y;
    }
    return cellIds;
  }

  for (const [gid, g] of Object.entries(ir.gates || {})) {
    const base = baseType(g.type);
    const rawType = String(g.type || "").toUpperCase();
    const srcs = g.inputs || [];
    const n = srcs.length;

    if (MSI_STUB.has(rawType) || MSI_STUB.has(base)) {
      for (const src of srcs) bitOf(src);
      bitOf(gid);
      gateMeta.push({ id: gid, base: rawType, arity: n, mode: "msi_stub", cells: 0 });
      continue;
    }

    if (SEQ_TYPE[rawType] || SEQ_TYPE[base]) {
      const yType = SEQ_TYPE[rawType] || SEQ_TYPE[base];
      if (srcs.length < 2) throw new Error(`seq gate ${gid} needs D and CLK`);
      addDff(yType, srcs[0], srcs[1], gid);
      gateMeta.push({ id: gid, base: rawType, arity: n, mode: "seq", cells: 1 });
      continue;
    }

    if (base === "NOT") {
      addUnary(BIN_TYPE.NOT, srcs[0], gid);
      gateMeta.push({ id: gid, base, arity: n, mode: "multi", cells: 1 });
      continue;
    }
    if (base === "BUF" || (n === 1 && base !== "NOT")) {
      netBit.set(gid, bitOf(srcs[0]));
      gateMeta.push({ id: gid, base, arity: n, mode: "alias", cells: 0 });
      continue;
    }

    const canMulti =
      preferMulti &&
      MULTI_OK.has(base) &&
      n >= 3 &&
      n <= multiMax;

    if (canMulti) {
      addMulti(multiAlias(base, n), srcs, gid);
      gateMeta.push({ id: gid, base, arity: n, mode: "multi", cells: 1 });
      continue;
    }

    if (n === 2 && BIN_TYPE[base]) {
      addBinary(BIN_TYPE[base], srcs[0], srcs[1], gid);
      gateMeta.push({ id: gid, base, arity: n, mode: "binary", cells: 1 });
      continue;
    }

    // 降级：二元树
    if (!BIN_TYPE[base]) {
      throw new Error(`no yosys mapping for gate ${gid} type ${g.type}`);
    }
    const ids = reduceBinaryTree(BIN_TYPE[base], srcs, gid);
    gateMeta.push({
      id: gid,
      base,
      arity: n,
      mode: "fallback_split",
      cells: ids.length,
      reason: n > multiMax ? "arity_gt_max" : "no_multi_skin",
    });
  }

  const netnames = {};
  for (const [name, bit] of netBit.entries()) {
    netnames[name] = { bits: [bit] };
  }

  const json = {
    creator: "netlist_workbench logic_ir_to_yosys",
    modules: {
      [moduleName]: { ports, cells, netnames },
    },
  };

  return {
    json,
    meta: {
      preferMulti,
      multiMax,
      gateMeta,
      cellCount: Object.keys(cells).length,
      multiGates: gateMeta.filter((g) => g.mode === "multi" && g.arity >= 3).length,
      fallbackSplits: gateMeta.filter((g) => g.mode === "fallback_split"),
    },
  };
}
