/**
 * 状态图 TikZ 对照：课本 · 自研 SVG · TikZ(node-tikzjax)
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import sharp from "sharp";
import { stateIrToSvg, selfCheckStateSvg } from "../adapters/state_ir_to_svg.mjs";
import { stateIrToTikz } from "../adapters/state_ir_to_tikz.mjs";
import { tikzToSvg } from "../adapters/state_tikz_render.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CARDS = path.join(ROOT, "gold", "level1", "cards");
const OUT = path.join(ROOT, "gold", "level1", "state_opt");
const TB = path.join(ROOT, "textbook_figures");

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function resolveTextbookAbs(card) {
  if (!card?.image) return null;
  const cleaned = String(card.image).replace(/\\/g, "/");
  const m = cleaned.match(/(?:^|\/)(textbook_figures\/.+)$/);
  const candidates = [];
  if (m) candidates.push(path.join(ROOT, m[1]));
  if (cleaned.includes("state_machine/")) {
    candidates.push(path.join(TB, cleaned.slice(cleaned.indexOf("state_machine/"))));
  }
  for (const abs of candidates) if (fs.existsSync(abs)) return abs;
  return null;
}

function prepareSvg(svg) {
  if (/id="__bg__"/.test(svg)) return svg;
  if (!/<svg[^>]*>/.test(svg)) return svg;
  return svg.replace(
    /<svg([^>]*)>/,
    `<svg$1><rect id="__bg__" width="100%" height="100%" fill="#ffffff" stroke="none"/>`
  );
}

async function svgToPng(svg, pngPath) {
  await sharp(Buffer.from(prepareSvg(svg)), { density: 168 })
    .flatten({ background: "#ffffff" })
    .png()
    .toFile(pngPath);
}

async function main() {
  const tikzDir = path.join(OUT, "tikz");
  const shotsDir = path.join(OUT, "tikz_shots");
  fs.mkdirSync(tikzDir, { recursive: true });
  fs.mkdirSync(shotsDir, { recursive: true });

  const ids = fs.readdirSync(CARDS).filter((d) => /^S\d+$/.test(d)).sort();
  const rows = [];

  for (const id of ids) {
    const dir = path.join(CARDS, id);
    const ir = readJson(path.join(dir, "ir.json"));
    const card = readJson(path.join(dir, "card.json"));
    if (ir.diagram_type !== "state") continue;

    const svgNative = stateIrToSvg(ir);
    const check = selfCheckStateSvg(ir, svgNative);
    const nativePng = path.join(shotsDir, `${id}_native.png`);
    await svgToPng(svgNative, nativePng);

    let tikzOk = false;
    let tikzErr = "";
    let tikzPng = null;
    try {
      const tex = stateIrToTikz(ir);
      fs.writeFileSync(path.join(tikzDir, `${id}.tex`), tex, "utf8");
      const svgTikz = await tikzToSvg(tex);
      fs.writeFileSync(path.join(tikzDir, `${id}.svg`), svgTikz, "utf8");
      tikzPng = `tikz_shots/${id}.png`;
      await svgToPng(svgTikz, path.join(OUT, tikzPng));
      tikzOk = true;
      console.log(id, "TIKZ_OK", ir.layout || "auto");
    } catch (e) {
      tikzErr = e?.message || String(e);
      console.warn(id, "TIKZ_FAIL", tikzErr.split("\n")[0]);
    }

    const tbAbs = resolveTextbookAbs(card);
    const tbRel = tbAbs ? path.relative(OUT, tbAbs).split(path.sep).join("/") : null;

    rows.push({
      id,
      fig_id: card.fig_id,
      caption: card.caption,
      layout: ir.layout || "auto",
      has_positions: !!(ir.positions && Object.keys(ir.positions).length),
      self_ok: check.ok,
      tikz_ok: tikzOk,
      tikz_err: tikzErr,
      tbRel,
      nativeShot: `tikz_shots/${id}_native.png`,
      tikzShot: tikzPng,
      texRel: `tikz/${id}.tex`,
    });
  }

  const html = `<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<title>状态图：课本 · 自研 SVG · TikZ</title>
<style>
body{margin:0;font-family:Segoe UI,PingFang SC,Microsoft YaHei,sans-serif;background:#f3efe8;color:#1a1814}
header{position:sticky;top:0;z-index:2;padding:14px 18px;background:rgba(243,239,232,.96);border-bottom:1px solid #d9d2c8}
h1{margin:0;font-size:1.15rem}.sub{margin:4px 0 0;color:#666;font-size:.9rem}
.nav{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.nav a{font-size:.82rem;text-decoration:none;color:inherit;border:1px solid #d9d2c8;background:#fff;padding:2px 8px;border-radius:6px}
article{max-width:1200px;margin:16px auto;background:#fffdf9;border:1px solid #d9d2c8;border-radius:10px;overflow:hidden}
h2{margin:0;padding:10px 14px;font-size:1rem;border-bottom:1px solid #d9d2c8}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr}
section{padding:12px;border-right:1px solid #eee} section:last-child{border-right:none}
h3{margin:0 0 8px;font-size:.75rem;color:#666;letter-spacing:.05em;text-transform:uppercase}
img{max-width:100%;background:#fff;border:1px solid #eee}
.badge{font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid #b7d8c2;background:#eef8f1;color:#1f6b3a}
.warn{color:#9b2c2c;background:#fdf0f0;border-color:#e5bcbc}
.meta{font-size:.78rem;color:#888;margin-top:6px}
.err{font-size:.78rem;color:#9b2c2c;white-space:pre-wrap}
</style></head><body>
<header>
  <h1>状态图对照：课本 · 自研 SVG · TikZ (node-tikzjax)</h1>
  <p class="sub">TikZ 与自研 SVG 共用 computeStateLayout 坐标。渲染链：IR → .tex → WASM → SVG → PNG。</p>
  <div class="nav">${rows.map((r) => `<a href="#${esc(r.id)}">${esc(r.id)}</a>`).join("")}</div>
</header>
${rows
  .map(
    (r) => `<article id="${esc(r.id)}">
  <h2>${esc(r.id)} · 图${esc(r.fig_id)}
    <span class="badge ${r.tikz_ok ? "" : "warn"}">${r.tikz_ok ? "TIKZ_OK" : "TIKZ_FAIL"}</span>
    <span style="font-size:.85rem;color:#666;font-weight:400"> layout=${esc(r.layout)}${r.has_positions ? " · positions" : ""} · ${esc(r.caption || "")}</span>
  </h2>
  <div class="grid">
    <section><h3>课本原图</h3>${r.tbRel ? `<img src="${esc(r.tbRel)}" alt="tb"/>` : "<p>无</p>"}</section>
    <section><h3>自研 SVG</h3><img src="${esc(r.nativeShot)}" alt="native"/><p class="meta">${r.self_ok ? "STRUCT_OK" : "STRUCT_FAIL"}</p></section>
    <section><h3>TikZ</h3>${
      r.tikz_ok
        ? `<img src="${esc(r.tikzShot)}" alt="tikz"/><p class="meta"><a href="${esc(r.texRel)}">${esc(r.texRel)}</a></p>`
        : `<p class="err">${esc(r.tikz_err)}</p>`
    }</section>
  </div>
</article>`
  )
  .join("\n")}
</body></html>`;

  fs.writeFileSync(path.join(OUT, "review_tikz.html"), html);
  console.log("wrote", path.join(OUT, "review_tikz.html"));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
