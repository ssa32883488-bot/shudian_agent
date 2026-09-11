/**
 * Logic IR → Schematex DSL（不含坐标，style 默认 iec）
 *
 * 用法:
 *   node adapters/logic_ir_to_schematex.mjs ir/examples/fig_2_5_2.ir.json
 *   node adapters/logic_ir_to_schematex.mjs ir/examples/fig_2_5_2.ir.json --out out.stx
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const SIG = /^[A-Za-z_][A-Za-z0-9_]*$/;
const GATES = new Set([
  "AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR", "BUF",
  "MUX", "DEMUX", "DECODER", "ENCODER",
  "DFF", "JKFF", "SRFF", "TFF", "LATCH_SR", "LATCH_D",
  "TRISTATE_BUF", "TRISTATE_INV", "OPEN_DRAIN", "SCHMITT",
  "COUNTER", "SHIFT_REG",
]);

function fail(msg) {
  throw new Error(msg);
}

export function logicIrToSchematex(ir) {
  if (!ir || ir.diagram_type !== "logic") fail("diagram_type 必须为 logic");
  if (ir.schema_version !== "logic_ir_v1") fail("schema_version 必须为 logic_ir_v1");

  const style = ir.style === "ansi" ? "ansi" : "iec";
  const title = (ir.title || "logic").replace(/[^\w\- ]/g, "").slice(0, 40) || "logic";
  const inputs = ir.inputs || [];
  const gates = ir.gates || {};
  const outputs = ir.outputs || {};

  if (!inputs.length) fail("inputs 为空");
  if (!Object.keys(gates).length) fail("gates 为空");
  if (!Object.keys(outputs).length) fail("outputs 为空");

  for (const s of inputs) {
    if (!SIG.test(s)) fail(`非法 input: ${s}`);
  }
  for (const [id, g] of Object.entries(gates)) {
    if (!SIG.test(id)) fail(`非法 gate id: ${id}`);
    if (!g || !GATES.has(String(g.type).toUpperCase())) fail(`非法 gate type: ${id}`);
    if (!Array.isArray(g.inputs) || !g.inputs.length) fail(`gate ${id} inputs 空`);
    for (const inp of g.inputs) {
      if (!SIG.test(inp)) fail(`gate ${id} 非法输入 ${inp}`);
    }
  }
  for (const [out, src] of Object.entries(outputs)) {
    if (!SIG.test(out) || !SIG.test(src)) fail(`非法 output 映射 ${out}<-${src}`);
  }

  // 允许环（锁存器交叉耦合）；有环时按声明顺序输出
  let hasCycle = false;
  const ordered = [];
  const visited = new Set();
  const visiting = new Set();

  function visit(id) {
    if (visited.has(id)) return;
    if (visiting.has(id)) {
      hasCycle = true;
      return;
    }
    if (!gates[id]) return;
    visiting.add(id);
    for (const inp of gates[id].inputs) {
      if (gates[inp]) visit(inp);
    }
    visiting.delete(id);
    visited.add(id);
    ordered.push(id);
  }
  for (const id of Object.keys(gates)) visit(id);
  const emitOrder = hasCycle ? Object.keys(gates) : ordered;

  const lines = [];
  lines.push(`logic "${title}" style: ${style}`);
  lines.push(`input ${inputs.join(", ")}`);
  lines.push(`output ${Object.keys(outputs).join(", ")}`);

  for (const id of emitOrder) {
    const g = gates[id];
    const typ = String(g.type).toUpperCase();
    lines.push(`${id} = ${typ}(${g.inputs.join(", ")})`);
  }

  for (const [out, src] of Object.entries(outputs)) {
    if (out !== src) {
      if (!gates[src] && !inputs.includes(src)) fail(`output ${out} 源 ${src} 不存在`);
      lines.push(`${out} <- ${src}`);
    } else if (!gates[out]) {
      fail(`output ${out} 与门同名但 gates 中无此门`);
    }
  }

  return lines.join("\n") + "\n";
}

function main() {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.error("用法: node logic_ir_to_schematex.mjs <ir.json> [--out file.stx]");
    process.exit(1);
  }
  const irPath = args[0];
  const outIdx = args.indexOf("--out");
  const outPath = outIdx >= 0 ? args[outIdx + 1] : null;
  const ir = JSON.parse(fs.readFileSync(irPath, "utf8"));
  const dsl = logicIrToSchematex(ir);
  if (outPath) {
    fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
    fs.writeFileSync(outPath, dsl, "utf8");
    console.error("wrote", outPath);
  }
  process.stdout.write(dsl);
}

const self = fileURLToPath(import.meta.url);
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(self)) {
  main();
}
