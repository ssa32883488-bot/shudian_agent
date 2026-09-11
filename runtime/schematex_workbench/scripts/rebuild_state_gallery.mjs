/**
 * 只重建状态图金卡 + 课本对照验收页
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

function prepareSvg(svg) {
  if (/id="__bg__"/.test(svg)) return svg;
  return svg.replace(
    /<svg([^>]*)>/,
    `<svg$1><rect id="__bg__" width="100%" height="100%" fill="#ffffff" stroke="none"/>`
  );
}

function resolveTextbookAbs(card, cardDir) {
  if (!card?.image) return null;
  const cleaned = String(card.image).replace(/\\/g, "/");
  const candidates = [];
  const m = cleaned.match(/(?:^|\/)(textbook_figures\/.+)$/);
  if (m) candidates.push(path.join(ROOT, m[1]));
  if (cleaned.includes("state_machine/")) {
    candidates.push(
      path.join(TB, cleaned.slice(cleaned.indexOf("state_machine/")))
    );
  }
  candidates.push(path.resolve(cardDir, cleaned));
  candidates.push(path.join(TB, path.basename(cleaned)));
  for (const abs of candidates) {
    if (fs.existsSync(abs)) return abs;
  }
  return null;
}

async function main() {
  fs.mkdirSync(path.join(OUT, "shots"), { recursive: true });
  const ids = fs
    .readdirSync(CARDS)
    .filter((d) => /^S\d+$/.test(d))
    .sort();

  const rows = [];
  for (const id of ids) {
    const dir = path.join(CARDS, id);
    const ir = readJson(path.join(dir, "ir.json"));
    const card = readJson(path.join(dir, "card.json"));
    if (ir.diagram_type !== "state") continue;

    // 默认走 auto（S01 已显式 racetrack）
    if (!ir.layout) ir.layout = "auto";

    const svg = stateIrToSvg(ir);
    const check = selfCheckStateSvg(ir, svg);
    fs.writeFileSync(path.join(dir, "gen.svg"), svg);
    fs.writeFileSync(path.join(dir, "gen_tbx.svg"), svg);
    fs.writeFileSync(path.join(dir, "state_self_check.json"), JSON.stringify(check, null, 2));

    const png = path.join(OUT, "shots", `${id}.png`);
    await sharp(Buffer.from(prepareSvg(svg)), { density: 160 })
      .flatten({ background: "#ffffff" })
      .png()
      .toFile(png);

    let tbRel = null;
    const tbAbs = resolveTextbookAbs(card, dir);
    if (tbAbs) tbRel = path.relative(OUT, tbAbs).split(path.sep).join("/");
    if (!tbRel) console.warn("missing textbook image:", id, card.image);

    rows.push({
      id,
      fig_id: card.fig_id,
      caption: card.caption,
      layout: ir.layout || "auto",
      self_ok: check.ok,
      checks: check.checks,
      tbRel,
      shot: `shots/${id}.png`,
      svgRel: path.relative(OUT, path.join(dir, "gen.svg")).split(path.sep).join("/"),
    });

    console.log(
      id,
      check.ok ? "STATE_SELF_OK" : "STATE_SELF_FAIL",
      `layout=${ir.layout || "auto"}`,
      check.checks.map((c) => `${c.ok ? "OK" : "FAIL"}:${c.id}`).join(" ")
    );
  }

  const okN = rows.filter((r) => r.self_ok).length;
  const html = `<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<title>状态图优化验收</title>
<style>
body{margin:0;font-family:"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f3efe8;color:#1c1916}
header{position:sticky;top:0;background:rgba(243,239,232,.95);padding:14px 18px;border-bottom:1px solid #d9d2c8}
h1{margin:0;font-size:1.15rem} p{margin:4px 0 0;color:#6b6560;font-size:.9rem}
.nav{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.nav a{text-decoration:none;color:inherit;border:1px solid #d9d2c8;background:#fffdf9;padding:2px 8px;border-radius:6px;font-size:.82rem}
article{max-width:1100px;margin:16px auto;background:#fffdf9;border:1px solid #d9d2c8;border-radius:10px;overflow:hidden}
article h2{margin:0;padding:12px 14px;font-size:1rem;border-bottom:1px solid #d9d2c8}
.badge{font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid}
.ok{color:#1f6b3a;background:#eef8f1;border-color:#b7d8c2}
.bad{color:#9b2c2c;background:#fdf0f0;border-color:#e5bcbc}
.grid{display:grid;grid-template-columns:1fr 1fr}
section{padding:12px;border-top:1px solid #d9d2c8}
@media(min-width:900px){section:first-child{border-right:1px solid #d9d2c8;border-top:0} section:nth-child(2){border-top:0}}
h3{margin:0 0 8px;font-size:.78rem;letter-spacing:.06em;color:#6b6560;text-transform:uppercase}
img{max-width:100%;background:#fff;border:1px solid #e7e0d6}
.meta{font-size:.85rem;color:#6b6560}
</style></head><body>
<header>
  <h1>状态图专用优化验收 · 课本 vs 新渲染</h1>
  <p>跑道布局 / 圆周截断箭头 / 图例 / 自检 · ${okN}/${rows.length} SELF_OK</p>
  <div class="nav">${rows.map((r) => `<a href="#${esc(r.id)}">${esc(r.id)}</a>`).join("")}</div>
</header>
${rows
  .map(
    (r) => `<article id="${esc(r.id)}">
  <h2>${esc(r.id)} · 图${esc(r.fig_id)} <span class="badge ${r.self_ok ? "ok" : "bad"}">${r.self_ok ? "SELF_OK" : "SELF_FAIL"}</span>
  <span class="meta"> layout=${esc(r.layout)} · ${esc(r.caption || "")}</span></h2>
  <div class="grid">
    <section><h3>课本原图</h3>${r.tbRel ? `<img src="${esc(r.tbRel)}" alt="tb"/>` : `<p class="meta">无课本图</p>`}</section>
    <section><h3>优化后渲染</h3><img src="${esc(r.shot)}" alt="gen"/></section>
  </div>
</article>`
  )
  .join("\n")}
</body></html>`;

  fs.writeFileSync(path.join(OUT, "review_gallery.html"), html);
  fs.writeFileSync(path.join(OUT, "BATCH_REPORT.json"), JSON.stringify(rows, null, 2));
  console.log("wrote", path.join(OUT, "review_gallery.html"));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
