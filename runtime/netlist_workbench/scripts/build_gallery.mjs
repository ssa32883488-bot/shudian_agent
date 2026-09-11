/**
 * 生成验收 HTML：课本图 | IR 摘要 | netlistsvg 自动布线 | 真值表仿真
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const LEVEL = path.join(ROOT, "gold", "level1");
const OLD_TBX = path.resolve(ROOT, "..", "schematex_workbench", "textbook_figures");

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function irSummary(ir) {
  const inputs = (ir.inputs || []).join(", ");
  const outs = Object.entries(ir.outputs || {})
    .map(([k, v]) => `${k}←${v}`)
    .join(", ");
  const cells = Object.entries(ir.gates || {})
    .map(([id, g]) => `${id} ${g.type}(${(g.inputs || []).join(",")})`)
    .join("\n");
  return `inputs: ${inputs}\noutputs: ${outs}\n\ngates:\n${cells}${ir.notes ? `\n\nnotes: ${ir.notes}` : ""}`;
}

function simTableHtml(samples) {
  if (!samples?.length) return "<p class='muted'>无仿真样本</p>";
  const keysIn = Object.keys(samples[0].inputs || {});
  const keysOut = Object.keys(samples[0].outputs || {});
  const head = [...keysIn, ...keysOut].map((k) => `<th>${esc(k)}</th>`).join("");
  const rows = samples
    .map((r) => {
      const cells = [
        ...keysIn.map((k) => `<td>${esc(r.inputs[k])}</td>`),
        ...keysOut.map((k) => `<td class="out">${esc(r.outputs[k])}</td>`),
      ].join("");
      return `<tr>${cells}</tr>`;
    })
    .join("\n");
  return `<table class="tt"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table>`;
}

function resolveTextbookSrc(image) {
  if (!image) return null;
  const cleaned = image.replace(/\\/g, "/");
  const candidates = [];
  // 常见：../../textbook_figures/logic_dag/foo.jpg → textbook_figures/...
  const m = cleaned.match(/(?:^|\/)(textbook_figures\/.+)$/);
  if (m) candidates.push(path.join(path.dirname(OLD_TBX), m[1]));
  // 仅 logic_dag/...
  if (cleaned.includes("logic_dag/")) {
    const rel = cleaned.slice(cleaned.indexOf("logic_dag/"));
    candidates.push(path.join(OLD_TBX, rel));
  }
  candidates.push(path.join(OLD_TBX, cleaned.replace(/^\/+/, "")));
  for (const abs of candidates) {
    if (fs.existsSync(abs)) {
      return path.relative(LEVEL, abs).split(path.sep).join("/");
    }
  }
  return null;
}

function main() {
  const batchPath = path.join(LEVEL, "BATCH_REPORT.json");
  if (!fs.existsSync(batchPath)) {
    console.error("缺少 BATCH_REPORT.json，请先 npm run run-batch");
    process.exit(1);
  }
  const reports = readJson(batchPath);

  const cardsHtml = reports
    .map((r) => {
      const cardDir = path.join(LEVEL, "cards", r.id);
      const ir = fs.existsSync(path.join(cardDir, "ir.json"))
        ? readJson(path.join(cardDir, "ir.json"))
        : null;
      const tbSrc = resolveTextbookSrc(r.image);
      const shot = fs.existsSync(path.join(LEVEL, "shots", `${r.id}.png`))
        ? `shots/${r.id}.png`
        : null;
      const svg = fs.existsSync(path.join(cardDir, "gen_netlist.svg"))
        ? `cards/${r.id}/gen_netlist.svg`
        : null;

      const badgeSim = r.sim_ok
        ? `<span class="badge ok">SIM_OK</span>`
        : `<span class="badge bad">SIM_${esc(r.sim_reason || "FAIL")}</span>`;
      const badgeRen = r.render_ok
        ? `<span class="badge ok">RENDER_OK</span>`
        : `<span class="badge bad">RENDER_FAIL</span>`;
      const badgeSelf = r.self_ok
        ? `<span class="badge ok">SELF_OK</span>`
        : `<span class="badge bad">SELF_FAIL</span>`;
      const selfLines = (r.self_checks || [])
        .map((c) => `${c.ok ? "✓" : "✗"} ${c.id}: ${c.detail}`)
        .join("\n");

      return `
<article class="card" id="${esc(r.id)}">
  <header>
    <h2>${esc(r.id)} · ${esc(r.fig_id || "")}</h2>
    <p class="cap">${esc(r.caption || "")}</p>
    <div class="badges">${badgeSim} ${badgeRen} ${badgeSelf}</div>
    ${
      r.multi_gates
        ? `<p class="meta">多输入单符号 ×${esc(r.multi_gates)}${r.fallback_splits ? ` · 降级拆分 ×${esc(r.fallback_splits)}` : ""}</p>`
        : ""
    }
  </header>
  <div class="grid">
    <section>
      <h3>课本原图</h3>
      ${
        tbSrc
          ? `<img src="${esc(tbSrc)}" alt="textbook ${esc(r.id)}" loading="lazy"/>`
          : `<p class="muted">无课本图 (${esc(r.image || "-")})</p>`
      }
    </section>
    <section>
      <h3>IR 摘要</h3>
      <pre class="ir">${esc(ir ? irSummary(ir) : r.fatal || "—")}</pre>
    </section>
    <section>
      <h3>netlistsvg 自动布线</h3>
      ${
        svg
          ? `<img class="net" src="${esc(svg)}" alt="netlist ${esc(r.id)}" loading="lazy"/>`
          : shot
            ? `<img class="net" src="${esc(shot)}" alt="netlist ${esc(r.id)}" loading="lazy"/>`
            : `<p class="muted">${esc(r.render_error || "未渲染")}</p>`
      }
    </section>
    <section>
      <h3>仿真（真值表抽样）</h3>
      <p class="meta">行数 ${esc(r.sim_rows)} · ${r.combinational ? "组合" : "非组合/跳过"}</p>
      ${simTableHtml(r.sim_samples)}
      <pre class="ir self">${esc(selfLines || "无自检")}</pre>
      ${r.notes ? `<p class="notes">${esc(r.notes)}</p>` : ""}
    </section>
  </div>
</article>`;
    })
    .join("\n");

  const okSim = reports.filter((r) => r.sim_ok).length;
  const okRen = reports.filter((r) => r.render_ok).length;
  const okSelf = reports.filter((r) => r.self_ok).length;

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>netlist_workbench v2 · Level-1 验收</title>
<style>
  :root {
    --bg: #f6f3ee;
    --ink: #1c1a16;
    --muted: #6b6560;
    --line: #d9d2c8;
    --ok: #1f6b3a;
    --bad: #9b2c2c;
    --panel: #fffdf9;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    color: var(--ink);
    background:
      radial-gradient(1200px 600px at 10% -10%, #e8f0e4 0%, transparent 55%),
      radial-gradient(900px 500px at 100% 0%, #efe6d8 0%, transparent 50%),
      var(--bg);
  }
  .top {
    position: sticky; top: 0; z-index: 5;
    backdrop-filter: blur(8px);
    background: rgba(246,243,238,.92);
    border-bottom: 1px solid var(--line);
    padding: 14px 22px;
  }
  .top h1 { margin: 0 0 4px; font-size: 1.25rem; font-weight: 650; }
  .top p { margin: 0; color: var(--muted); font-size: .92rem; }
  .nav { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
  .nav a {
    text-decoration: none; color: var(--ink);
    border: 1px solid var(--line); background: var(--panel);
    padding: 2px 8px; border-radius: 6px; font-size: .85rem;
  }
  main { max-width: 1400px; margin: 0 auto; padding: 18px 18px 64px; }
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    margin: 18px 0;
    overflow: hidden;
  }
  .card header { padding: 14px 16px 8px; border-bottom: 1px solid var(--line); }
  .card h2 { margin: 0; font-size: 1.1rem; }
  .cap { margin: 4px 0 8px; color: var(--muted); font-size: .9rem; }
  .badges { display: flex; gap: 8px; }
  .badge {
    font-size: .75rem; font-weight: 700; letter-spacing: .02em;
    padding: 2px 8px; border-radius: 999px; border: 1px solid;
  }
  .badge.ok { color: var(--ok); border-color: #b7d8c2; background: #eef8f1; }
  .badge.bad { color: var(--bad); border-color: #e5bcbc; background: #fdf0f0; }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }
  @media (max-width: 960px) { .grid { grid-template-columns: 1fr; } }
  .grid section {
    padding: 12px 14px 16px;
    border-top: 1px solid var(--line);
  }
  @media (min-width: 961px) {
    .grid section:nth-child(odd) { border-right: 1px solid var(--line); }
    .grid section:nth-child(-n+2) { border-top: none; }
  }
  h3 { margin: 0 0 8px; font-size: .85rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
  img { max-width: 100%; height: auto; display: block; background: #fff; border: 1px solid var(--line); }
  img.net { min-height: 120px; }
  pre.ir {
    margin: 0; max-height: 320px; overflow: auto;
    font-size: .78rem; line-height: 1.35;
    background: #f3efe8; padding: 10px; border-radius: 8px;
    white-space: pre-wrap; word-break: break-word;
  }
  table.tt { border-collapse: collapse; width: 100%; font-size: .82rem; }
  table.tt th, table.tt td { border: 1px solid var(--line); padding: 3px 6px; text-align: center; }
  table.tt th { background: #f0ebe3; }
  table.tt td.out { font-weight: 650; color: var(--ok); }
  .muted { color: var(--muted); font-size: .9rem; }
  .meta { margin: 0 0 8px; font-size: .85rem; color: var(--muted); }
  .notes { margin-top: 10px; font-size: .85rem; color: var(--muted); }
</style>
</head>
<body>
  <div class="top">
    <h1>netlist_workbench v2 · Level-1 组合逻辑验收</h1>
    <p>仿真正确优先 · 多输入单符号优先（失败再降级拆分）· 自检入库 · ${okSim}/${reports.length} 仿真 · ${okRen}/${reports.length} 渲染 · ${okSelf}/${reports.length} 自检</p>
    <div class="nav">
      ${reports.map((r) => `<a href="#${esc(r.id)}">${esc(r.id)}</a>`).join("")}
    </div>
  </div>
  <main>
    ${cardsHtml}
  </main>
</body>
</html>`;

  const out = path.join(LEVEL, "review_gallery.html");
  fs.writeFileSync(out, html);
  console.log("wrote", out);
}

main();
