import fs from "fs";
import { parseTbx } from "../renderers/tbx_logic.mjs";

function fixTbx(text) {
  const lines = text.split(/\r?\n/);
  const out = [];
  for (const line of lines) {
    const m = line.match(/^(\s*wire\s+)(.+)$/);
    if (!m) {
      out.push(line);
      continue;
    }
    const pts = [];
    const re = /([\d.]+)\s*,\s*([\d.]+)/g;
    let mm;
    while ((mm = re.exec(m[2]))) pts.push([+mm[1], +mm[2]]);
    if (pts.length < 2) {
      out.push(line);
      continue;
    }
    const fixed = [pts[0]];
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = fixed[fixed.length - 1];
      const [x1, y1] = pts[i];
      if (x0 !== x1 && y0 !== y1) fixed.push([x1, y0]);
      fixed.push([x1, y1]);
    }
    const coll = [fixed[0]];
    for (let i = 1; i < fixed.length; i++) {
      const a = coll[coll.length - 1];
      const b = fixed[i];
      if (a[0] !== b[0] || a[1] !== b[1]) coll.push(b);
    }
    out.push(m[1] + coll.map((p) => `${p[0]},${p[1]}`).join(" "));
  }
  return out.join("\n");
}

const ids = process.argv.slice(2);
for (const id of ids) {
  const p = `gold/level1/cards/${id}/gold.tbx`;
  fs.writeFileSync(p, fixTbx(fs.readFileSync(p, "utf8")));
  const d = parseTbx(fs.readFileSync(p, "utf8"));
  let bad = 0;
  for (const w of d.wires)
    for (let i = 1; i < w.length; i++)
      if (w[i - 1][0] !== w[i][0] && w[i - 1][1] !== w[i][1]) bad++;
  console.log(id, bad ? `DIAG x${bad}` : "manhattan_ok");
}
