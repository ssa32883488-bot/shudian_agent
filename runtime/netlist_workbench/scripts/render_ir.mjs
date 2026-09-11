/**
 * 单次渲染：logic_ir JSON → netlistsvg SVG
 * 用法: node scripts/render_ir.mjs <ir.json> <out.svg>
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import { logicIrToYosysJson } from "../lib/ir_to_yosys_json.mjs";

const require = createRequire(import.meta.url);
const netlistsvg = require("netlistsvg");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SKIN = path.join(ROOT, "skins", "textbook.svg");

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function renderYosys(yosysJson) {
  const skin = fs.readFileSync(SKIN, "utf8");
  return new Promise((resolve, reject) => {
    netlistsvg.render(skin, yosysJson, (err, svg) => {
      if (err) reject(err);
      else resolve(svg);
    });
  });
}

async function main() {
  const irPath = process.argv[2];
  const outPath = process.argv[3];
  if (!irPath || !outPath) {
    console.error("usage: node render_ir.mjs <ir.json> <out.svg>");
    process.exit(2);
  }
  const ir = readJson(irPath);
  if (ir.diagram_type && ir.diagram_type !== "logic") {
    throw new Error("diagram_type 必须为 logic");
  }
  const yosysBundle = logicIrToYosysJson(ir, "WF");
  const svg = await renderYosys(yosysBundle.json);
  fs.writeFileSync(outPath, svg, "utf8");
}

main().catch((e) => {
  console.error(String(e && e.stack ? e.stack : e));
  process.exit(1);
});
