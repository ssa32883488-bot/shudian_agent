/**
 * 生成检阅用三栏 HTML：课本原图 | 解析代码 | 渲染结果
 * node scripts/build_review_gallery.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import { renderTbx, isTbx } from "../renderers/tbx_logic.mjs";
import { waveIrToSvg } from "../adapters/wave_ir_to_svg.mjs";
import { stateIrToSvg } from "../adapters/state_ir_to_svg.mjs";

const require = createRequire(import.meta.url);
const { render: renderSchematex } = require("schematex");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const LEVEL1 = path.join(ROOT, "gold", "level1");
const CARDS = path.join(LEVEL1, "cards");
const SHOTS = path.join(LEVEL1, "shots");

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function readText(p) {
  if (!fs.existsSync(p)) return null;
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return t;
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function mimeOf(p) {
  const e = path.extname(p).toLowerCase();
  if (e === ".png") return "image/png";
  if (e === ".jpg" || e === ".jpeg") return "image/jpeg";
  if (e === ".webp") return "image/webp";
  if (e === ".gif") return "image/gif";
  if (e === ".svg") return "image/svg+xml";
  return "application/octet-stream";
}

/** 把本地图片嵌进 HTML，解压单文件即可打开 */
function dataUri(absPath) {
  if (!absPath || !fs.existsSync(absPath)) return null;
  const buf = fs.readFileSync(absPath);
  return `data:${mimeOf(absPath)};base64,${buf.toString("base64")}`;
}

function textbookSrc(card) {
  // card.image 相对 gold/level1（与 review_gallery.html 同级语义）
  const candidates = [
    path.resolve(LEVEL1, card.image || ""),
    path.resolve(ROOT, "textbook_figures", path.basename(card.image || "")),
  ];
  // 也尝试 logic_dag 等子目录原路径
  if (card.image) {
    const m = String(card.image).replace(/^(\.\.\/)+/, "");
    candidates.push(path.resolve(ROOT, m));
  }
  for (const abs of candidates) {
    const uri = dataUri(abs);
    if (uri) return uri;
  }
  console.warn("missing textbook image:", card.id || "?", card.image);
  return "";
}

function isLogicCard(id) {
  return /^[LCF]\d{2}$/.test(id);
}

function renderGenSvg(id, card, irText, tbx, stx) {
  if (isLogicCard(id)) return null;
  try {
    if (tbx && isTbx(tbx)) return renderTbx(tbx);
    if (stx) return renderSchematex(stx);
    if (!irText) return null;
    const ir = JSON.parse(irText);
    if (ir.diagram_type === "waveform" || card.ir_schema === "wave_ir_v1") {
      return waveIrToSvg(ir);
    }
    if (ir.diagram_type === "state" || card.ir_schema === "state_ir_v1") {
      return stateIrToSvg(ir);
    }
  } catch (e) {
    console.warn(`render ${id}:`, e.message);
  }
  return null;
}

function pickGenFallback(id) {
  const dir = path.join(CARDS, id);
  const png = path.join(SHOTS, `${id}_gen.png`);
  if (fs.existsSync(png)) {
    const uri = dataUri(png);
    return `<img src="${uri}" alt="${id} 生成"/>`;
  }
  for (const name of ["gen_netlist.svg", "gen.svg", "gen_tbx.svg"]) {
    const p = path.join(dir, name);
    if (fs.existsSync(p)) {
      const uri = dataUri(p);
      return `<img src="${uri}" alt="${id} 生成"/>`;
    }
  }
  return null;
}

function codeBlock(label, text, lang) {
  if (!text) {
    return `<div class="code-pane empty"><div class="code-label">${label}</div><p class="missing">（无）</p></div>`;
  }
  const lines = text.split("\n").length;
  return `<div class="code-pane">
  <div class="code-label">${label} <span class="meta">${lines} 行 · ${lang}</span></div>
  <pre><code>${esc(text)}</code></pre>
</div>`;
}

const manifest = readJson(path.join(LEVEL1, "manifest.json"));
const ids = manifest.cards.map((c) => c.id);

const sections = [];
for (const id of ids) {
  const dir = path.join(CARDS, id);
  const card = readJson(path.join(dir, "card.json"));
  const ir = readText(path.join(dir, "ir.json"));
  const logic = isLogicCard(id);
  const tbx = logic ? null : readText(path.join(dir, "gold.tbx"));
  const stx = logic ? null : readText(path.join(dir, "from_ir.stx"));
  const inputCode = tbx || stx || "";
  const inputLabel = tbx ? "输入脚本 gold.tbx（已弃用）" : stx ? "输入脚本 from_ir.stx" : "输入脚本";
  const genSvg = renderGenSvg(id, card, ir, tbx, stx);
  const genHtml = genSvg
    ? `<div class="svg-inline">${genSvg}</div>`
    : pickGenFallback(id) || `<p class="missing">无生成图${logic ? "（请先运行 netlist_workbench npm run all）" : ""}</p>`;
  const imgSrc = textbookSrc(card);
  const grade = card.grade || "—";
  const engine = card.render_engine || "—";
  const gradeCls = grade === "TEXTBOOK_OK" ? "ok" : "warn";

  sections.push(`<section class="card" id="${id}">
  <header class="card-hd">
    <h2>${id}</h2>
    <span class="fig">图 ${card.fig_id}</span>
    <span class="grade ${gradeCls}">${grade}</span>
    <span class="engine">${engine}</span>
  </header>
  <p class="caption">${esc(card.caption || "")}</p>
  <div class="tri">
    <figure class="col orig">
      <figcaption>① 课本原图</figcaption>
      <div class="img-wrap">${
        imgSrc
          ? `<img src="${imgSrc}" alt="${id} 课本" loading="lazy"/>`
          : `<p class="missing">无课本图</p>`
      }</div>
    </figure>
    <div class="col codes">
      <figcaption>② 解析 &amp; 输入代码</figcaption>
      ${codeBlock("解析 IR · logic_ir_v1", ir, card.ir_schema || "logic_ir_v1")}
      ${logic ? `<p class="logic-pipe">渲染：<code>logic_ir_v1</code> → 仿真 → yosys JSON → <strong>netlistsvg</strong> 自动布线</p>` : codeBlock(inputLabel, inputCode, tbx ? "tbx" : "schematex")}
    </div>
    <figure class="col gen">
      <figcaption>③ 渲染结果</figcaption>
      <div class="img-wrap">${genHtml}</div>
    </figure>
  </div>
</section>`);
}

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Level-1 检阅 · 50 张三栏对照</title>
<style>
:root {
  --bg: #0f1419;
  --panel: #1a2332;
  --line: #2d3a4d;
  --ink: #e7ecf3;
  --muted: #8b9bb4;
  --ok: #34d399;
  --warn: #fbbf24;
  --mono: "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  --sans: "Microsoft YaHei", "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--sans);
  line-height: 1.5;
}
.top {
  position: sticky; top: 0; z-index: 20;
  background: rgba(15,20,25,.92);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line);
  padding: 12px 20px;
}
.top h1 { margin: 0 0 4px; font-size: 1.25rem; }
.top p { margin: 0; color: var(--muted); font-size: 13px; }
.nav {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-top: 10px; max-height: 72px; overflow: auto;
}
.nav a {
  font-size: 12px; padding: 3px 9px;
  background: var(--panel); border: 1px solid var(--line);
  border-radius: 999px; color: var(--ink); text-decoration: none;
}
.nav a:hover { border-color: #3d8bfd; color: #93c5fd; }
.wrap { max-width: 1600px; margin: 0 auto; padding: 16px 20px 48px; }
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
}
.card-hd {
  display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  padding: 12px 16px;
  border-bottom: 1px solid var(--line);
  background: rgba(0,0,0,.2);
}
.card-hd h2 { margin: 0; font-size: 1.1rem; letter-spacing: .04em; }
.fig { color: var(--muted); font-size: 13px; }
.grade { font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 6px; }
.grade.ok { background: #064e3b; color: var(--ok); }
.grade.warn { background: #78350f; color: var(--warn); }
.engine { font-size: 12px; color: var(--muted); font-family: var(--mono); }
.caption { margin: 0; padding: 8px 16px 0; color: var(--muted); font-size: 13px; }
.tri {
  display: grid;
  grid-template-columns: minmax(220px, 0.9fr) minmax(280px, 1fr) minmax(320px, 1.4fr);
  gap: 0;
  min-height: 280px;
}
@media (max-width: 1100px) {
  .tri { grid-template-columns: 1fr; }
}
.col { margin: 0; padding: 12px; border-right: 1px solid var(--line); min-width: 0; }
.col:last-child { border-right: 0; }
.col figcaption {
  font-size: 12px; font-weight: 700; color: #93c5fd;
  margin-bottom: 8px; text-transform: none;
}
.codes figcaption { margin-bottom: 10px; }
.img-wrap {
  background: #fff;
  border-radius: 8px;
  padding: 10px;
  display: flex; align-items: flex-start; justify-content: flex-start;
  min-height: 200px;
  max-height: 78vh;
  overflow: auto;
}
.img-wrap img, .img-wrap object { max-width: 100%; height: auto; }
/* 生成图不压缩：按 tbx 画布原尺寸显示，可滚动 */
.svg-inline { width: max-content; max-width: none; display: block; }
.svg-inline svg { display: block; max-width: none !important; height: auto; }
.code-pane {
  background: #121820;
  border: 1px solid var(--line);
  border-radius: 8px;
  margin-bottom: 10px;
  overflow: hidden;
}
.code-pane:last-child { margin-bottom: 0; }
.code-label {
  font-size: 11px; font-weight: 600;
  padding: 6px 10px;
  background: rgba(255,255,255,.04);
  border-bottom: 1px solid var(--line);
  color: #cbd5e1;
}
.code-label .meta { font-weight: 400; color: var(--muted); margin-left: 6px; }
pre {
  margin: 0; padding: 10px 12px;
  overflow: auto; max-height: 320px;
  font-family: var(--mono); font-size: 11.5px; line-height: 1.45;
  color: #d6deeb;
  white-space: pre;
}
.missing { color: var(--muted); font-size: 13px; padding: 20px; text-align: center; }
.empty .missing { padding: 8px; }
.logic-pipe { font-size: 12px; color: var(--muted); margin: 8px 0 0; padding: 0 12px; }
.logic-pipe code { font-family: var(--mono); font-size: 11px; color: var(--ink); }
</style>
</head>
<body>
<div class="top">
  <h1>Level-1 检阅 · 50 张三栏对照</h1>
  <p>① 课本原图 → ② 解析 IR + 输入脚本 → ③ 渲染结果 · 单文件自包含（图已内嵌）· 生成于 ${new Date().toISOString()}</p>
  <nav class="nav">${ids.map((id) => `<a href="#${id}">${id}</a>`).join("")}</nav>
</div>
<div class="wrap">
${sections.join("\n")}
</div>
</body>
</html>`;

const out = path.join(LEVEL1, "review_gallery.html");
fs.writeFileSync(out, html, "utf8");
console.log("wrote", out);
console.log("cards", ids.length);
