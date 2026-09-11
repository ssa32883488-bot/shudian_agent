/**
 * 打开对照台，按卡截图，供人工/视觉自检
 * node scripts/shot_card.mjs L01
 */
import { chromium } from "playwright";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import sharp from "sharp";
import { renderTbx, isTbx } from "../renderers/tbx_logic.mjs";
import { waveIrToSvg } from "../adapters/wave_ir_to_svg.mjs";
import { stateIrToSvg } from "../adapters/state_ir_to_svg.mjs";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const { render } = require("schematex");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const id = process.argv[2] || "L01";
const port = process.argv[3] || "5174";
const outDir = path.join(ROOT, "gold", "level1", "shots");
fs.mkdirSync(outDir, { recursive: true });

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

async function rasterCard() {
  const cardDir = path.join(ROOT, "gold", "level1", "cards", id);
  let svg = null;

  for (const name of ["gold.tbx", "from_ir.stx"]) {
    const p = path.join(cardDir, name);
    if (fs.existsSync(p)) {
      const dsl = fs.readFileSync(p, "utf8");
      svg = isTbx(dsl) ? renderTbx(dsl) : render(dsl);
      break;
    }
  }

  if (!svg) {
    const irPath = path.join(cardDir, "ir.json");
    const cardPath = path.join(cardDir, "card.json");
    if (fs.existsSync(irPath)) {
      const ir = readJson(irPath);
      const card = fs.existsSync(cardPath) ? readJson(cardPath) : {};
      if (ir.diagram_type === "waveform" || card.ir_schema === "wave_ir_v1") {
        svg = waveIrToSvg(ir);
      } else if (ir.diagram_type === "state" || card.ir_schema === "state_ir_v1") {
        svg = stateIrToSvg(ir);
      }
    }
  }

  if (!svg) throw new Error("no dsl / wave|state ir");
  fs.writeFileSync(path.join(cardDir, "gen_tbx.svg"), svg, "utf8");
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  const pngPath = path.join(outDir, `${id}_gen.png`);
  fs.writeFileSync(pngPath, png);
  return pngPath;
}

async function browserShot() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 800 } });
  await page.goto(`http://localhost:${port}/?card=${id}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  const shot = path.join(outDir, `${id}_workbench.png`);
  await page.screenshot({ path: shot, fullPage: false });
  await browser.close();
  return shot;
}

const png = await rasterCard();
console.log("raster", png);
try {
  const wb = await browserShot();
  console.log("workbench", wb);
} catch (e) {
  console.log("browser shot skipped:", e.message);
}
