/**
 * Wave IR → 教材风时序波形 SVG
 */
const FONT = "Microsoft YaHei, PingFang SC, Noto Sans SC, Segoe UI, sans-serif";

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

export function waveIrToSvg(ir) {
  if (!ir || ir.diagram_type !== "waveform") throw new Error("diagram_type 必须为 waveform");
  if (ir.schema_version !== "wave_ir_v1") throw new Error("schema_version 必须为 wave_ir_v1");
  const signals = ir.signals || [];
  if (!signals.length || signals.length > 10) throw new Error("signals 需 1–10 条");

  const expanded = [];
  for (const sig of signals) {
    const name = String(sig.name || "?");
    const wave = String(sig.wave || "");
    const levels = [];
    let level = 0;
    for (const ch of wave) {
      if (ch === "1") level = 1;
      else if (ch === "0") level = 0;
      else if (".pPnN".includes(ch)) {
        /* hold */
      } else continue;
      levels.push(level);
    }
    if (levels.length < 2) throw new Error(`信号 ${name} wave 过短`);
    expanded.push([name, levels]);
  }

  const n = Math.max(...expanded.map(([, lv]) => lv.length));
  const step = 36;
  const rowH = 70;
  const ox = 70;
  const oy = 28;
  const plotW = n * step;
  const w = ox + plotW + 50;
  const h = oy + expanded.length * rowH + 30;

  const parts = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">`,
    `<rect width="100%" height="100%" fill="#ffffff"/>`,
  ];
  if (ir.title) {
    /* textbook waves often omit chart title; keep optional small title off by default */
  }

  for (let i = 0; i < expanded.length; i++) {
    const [name, levels0] = expanded[i];
    const levels = levels0.slice();
    while (levels.length < n) levels.push(levels[levels.length - 1]);
    const y0 = oy + i * rowH;
    const yHigh = y0 + 12;
    const yLow = y0 + 44;
    parts.push(
      `<line x1="${ox}" y1="${yLow + 8}" x2="${ox + plotW + 16}" y2="${yLow + 8}" stroke="#111" stroke-width="1.2"/>`
    );
    parts.push(
      `<line x1="${ox}" y1="${yLow + 8}" x2="${ox}" y2="${yHigh - 6}" stroke="#111" stroke-width="1.2"/>`
    );
    parts.push(
      `<text x="${ox - 12}" y="${(yHigh + yLow) / 2 + 4}" text-anchor="end" font-size="14" font-family="${FONT}">${esc(name)}</text>`
    );
    parts.push(
      `<text x="${ox + plotW + 20}" y="${yLow + 12}" font-size="12" font-family="${FONT}">t</text>`
    );
    parts.push(
      `<text x="${ox - 4}" y="${yLow + 12}" text-anchor="end" font-size="11" fill="#64748b">O</text>`
    );

    const path = [];
    for (let t = 0; t < levels.length; t++) {
      const x = ox + t * step;
      const y = levels[t] ? yHigh : yLow;
      if (!path.length) path.push(`M${x},${y}`);
      else path.push(`L${x},${y}`);
      path.push(`L${x + step},${y}`);
    }
    parts.push(`<path d="${path.join(" ")}" fill="none" stroke="#111" stroke-width="1.8"/>`);
    for (let t = 0; t <= n; t++) {
      const x = ox + t * step;
      parts.push(
        `<line x1="${x}" y1="${yHigh - 4}" x2="${x}" y2="${yLow + 8}" ` +
          `stroke="#94a3b8" stroke-width="1" stroke-dasharray="3 3"/>`
      );
    }
  }

  parts.push(`</svg>`);
  return parts.join("");
}
