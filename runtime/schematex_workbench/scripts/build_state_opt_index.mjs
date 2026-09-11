/**
 * 状态图验收入口页
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, "..", "gold", "level1", "state_opt");
const acceptancePath = path.join(OUT, "acceptance.json");

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const acc = fs.existsSync(acceptancePath) ? readJson(acceptancePath) : null;
const cards = acc?.cards || [];

const html = `<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"/>
<title>状态图验收 · S01–S10</title>
<style>
body{margin:0;font-family:Segoe UI,PingFang SC,Microsoft YaHei,sans-serif;background:#f3efe8;color:#1a1814;padding:24px}
h1{margin:0 0 8px;font-size:1.3rem}
.sub{color:#666;margin:0 0 16px;font-size:.92rem}
.panel{background:#fffdf9;border:1px solid #d9d2c8;border-radius:10px;padding:16px;margin-bottom:16px}
.links{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}
.links a{padding:8px 14px;background:#fff;border:1px solid #d9d2c8;border-radius:8px;text-decoration:none;color:inherit}
.links a.primary{background:#1f6b3a;color:#fff;border-color:#1f6b3a}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left}
.badge{font-size:.72rem;padding:2px 8px;border-radius:999px;background:#eef8f1;color:#1f6b3a;border:1px solid #b7d8c2}
code{font-size:.82rem;background:#f5f2ec;padding:2px 6px;border-radius:4px}
</style></head><body>
<h1>状态转换图 · 验收冻结（S01–S10）</h1>
<p class="sub">${acc ? `验收时间 ${esc(acc.accepted_at)} · ${esc(acc.textbook)}` : "尚未运行 freeze-state-acceptance"}</p>
<div class="panel">
  <strong>对照页</strong>
  <div class="links">
    <a class="primary" href="review_textbook.html">课本 vs 自研 SVG</a>
    <a href="review_tikz.html">课本 vs SVG vs TikZ</a>
  </div>
  <strong>重建命令</strong>
  <p><code>npm run rebuild-state-accepted</code> · <code>npm run freeze-state-acceptance</code></p>
</div>
<div class="panel">
<table>
  <thead><tr><th>卡</th><th>图号</th><th>布局</th><th>positions</th><th>说明</th></tr></thead>
  <tbody>
${cards
  .map(
    (c) => `<tr>
  <td><span class="badge">${esc(c.id)}</span></td>
  <td>${esc(c.fig_id)}</td>
  <td>${esc(c.layout_mode)}</td>
  <td>${c.has_positions ? "✓" : "—"}</td>
  <td>${esc(c.caption)}</td>
</tr>`
  )
  .join("\n")}
  </tbody>
</table>
</div>
</body></html>`;

fs.writeFileSync(path.join(OUT, "index.html"), html);
console.log("wrote", path.join(OUT, "index.html"));
