/**
 * 课本 vs 自研(positions/racetrack) 对照 —— 不再主推 Graphviz
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import sharp from "sharp";
import { stateIrToSvg, selfCheckStateSvg } from "../adapters/state_ir_to_svg.mjs";

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
  return svg.replace(
    /<svg([^>]*)>/,
    `<svg$1><rect id="__bg__" width="100%" height="100%" fill="#ffffff" stroke="none"/>`
  );
}

async function main() {
  fs.mkdirSync(path.join(OUT, "shots"), { recursive: true });
  const ids = fs.readdirSync(CARDS).filter((d) => /^S\d+$/.test(d)).sort();
  const rows = [];

  for (const id of ids) {
    const dir = path.join(CARDS, id);
    const ir = readJson(path.join(dir, "ir.json"));
    const card = readJson(path.join(dir, "card.json"));
    if (ir.diagram_type !== "state") continue;

    const svg = stateIrToSvg(ir);
    const check = selfCheckStateSvg(ir, svg);
    fs.writeFileSync(path.join(dir, "gen.svg"), svg);
    fs.writeFileSync(path.join(dir, "gen_tbx.svg"), svg);

    const png = path.join(OUT, "shots", `${id}.png`);
    await sharp(Buffer.from(prepareSvg(svg)), { density: 168 })
      .flatten({ background: "#ffffff" })
      .png()
      .toFile(png);

    const tbAbs = resolveTextbookAbs(card);
    const tbRel = tbAbs ? path.relative(OUT, tbAbs).split(path.sep).join("/") : null;
    if (!tbRel) console.warn("missing tb", id);

    rows.push({
      id,
      fig_id: card.fig_id,
      caption: card.caption,
      layout: ir.layout || "auto",
      has_positions: !!(ir.positions && Object.keys(ir.positions).length),
      self_ok: check.ok,
      tbRel,
      shot: `shots/${id}.png`,
    });
    console.log(id, check.ok ? "OK" : "FAIL", ir.layout, ir.positions ? "positions" : "");
  }

  const html = `<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<title>状态图：课本 vs 自研（金标坐标/跑道）</title>
<style>
body{margin:0;font-family:Segoe UI,PingFang SC,Microsoft YaHei,sans-serif;background:#f3efe8;color:#1a1814}
header{position:sticky;top:0;z-index:2;padding:14px 18px;background:rgba(243,239,232,.96);border-bottom:1px solid #d9d2c8}
h1{margin:0;font-size:1.15rem}.sub{margin:4px 0 0;color:#666;font-size:.9rem}
.nav{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.nav a{font-size:.82rem;text-decoration:none;color:inherit;border:1px solid #d9d2c8;background:#fff;padding:2px 8px;border-radius:6px}
article{max-width:1100px;margin:16px auto;background:#fffdf9;border:1px solid #d9d2c8;border-radius:10px;overflow:hidden}
h2{margin:0;padding:10px 14px;font-size:1rem;border-bottom:1px solid #d9d2c8}
.grid{display:grid;grid-template-columns:1fr 1fr}
section{padding:12px} section:first-child{border-right:1px solid #eee}
h3{margin:0 0 8px;font-size:.75rem;color:#666;letter-spacing:.05em;text-transform:uppercase}
img{max-width:100%;background:#fff;border:1px solid #eee}
.badge{font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid #b7d8c2;background:#eef8f1;color:#1f6b3a}
.warn{color:#9b2c2c;background:#fdf0f0;border-color:#e5bcbc}
</style></head><body>
<header>
  <h1>状态图对照：课本 · 自研渲染（弃用 Graphviz 主路径）</h1>
  <p class="sub">S01 已写入课本 positions 金标。其余仍用跑道/环启发式。Graphviz 无法复现阎石两排布局。</p>
  <div class="nav">${rows.map((r) => `<a href="#${esc(r.id)}">${esc(r.id)}</a>`).join("")}</div>
</header>
${rows
  .map(
    (r) => `<article id="${esc(r.id)}">
  <h2>${esc(r.id)} · 图${esc(r.fig_id)}
    <span class="badge ${r.self_ok ? "" : "warn"}">${r.self_ok ? "STRUCT_OK" : "FAIL"}</span>
    <span style="font-size:.85rem;color:#666;font-weight:400"> layout=${esc(r.layout)}${r.has_positions ? " · positions金标" : ""} · ${esc(r.caption || "")}</span>
  </h2>
  <div class="grid">
    <section><h3>课本原图</h3>${r.tbRel ? `<img src="${esc(r.tbRel)}" alt="tb"/>` : "<p>无</p>"}</section>
    <section><h3>自研渲染</h3><img src="${esc(r.shot)}" alt="gen"/></section>
  </div>
</article>`
  )
  .join("\n")}
</body></html>`;

  fs.writeFileSync(path.join(OUT, "review_textbook.html"), html);
  console.log("wrote", path.join(OUT, "review_textbook.html"));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
