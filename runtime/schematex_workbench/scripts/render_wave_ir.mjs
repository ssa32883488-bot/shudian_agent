/**
 * 单次渲染：wave_ir JSON → SVG
 * 用法: node scripts/render_wave_ir.mjs <ir.json> <out.svg>
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { waveIrToSvg } from "../adapters/wave_ir_to_svg.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function main() {
  const irPath = process.argv[2];
  const outPath = process.argv[3];
  if (!irPath || !outPath) {
    console.error("usage: node render_wave_ir.mjs <ir.json> <out.svg>");
    process.exit(2);
  }
  const ir = readJson(irPath);
  const svg = waveIrToSvg(ir);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, svg, "utf8");
}

try {
  main();
} catch (e) {
  console.error(String(e && e.stack ? e.stack : e));
  process.exit(1);
}
