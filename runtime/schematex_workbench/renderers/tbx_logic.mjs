/**
 * Textbook (tbx) logic renderer — ANSI 符号 + 显式坐标/曼哈顿走线 + 结点
 * DSL 不以 Schematex 自动布局为准，专供课本复原。
 *
 * 语法见 parseTbx() 注释。
 */

const STROKE = "#333333";
const FONT = "Times New Roman, Songti SC, SimSun, serif";

/** ANSI 门几何（相对门原点左上角） */
const GEOM = {
  AND: { w: 56, h: 44, ins: [11, 33], out: [56, 22] },
  OR: { w: 58, h: 44, ins: [14, 33], out: [58, 22] },
  OR3: { w: 62, h: 56, ins: [10, 28, 46], out: [62, 28] },
  OR4: { w: 66, h: 70, ins: [10, 26, 44, 60], out: [66, 35] },
  AND3: { w: 58, h: 56, ins: [10, 28, 46], out: [58, 28] },
  AND4: { w: 60, h: 70, ins: [10, 26, 44, 60], out: [60, 35] },
  NAND3: { w: 64, h: 56, ins: [10, 28, 46], out: [64, 28], bubble: true },
  NAND4: { w: 66, h: 70, ins: [10, 26, 44, 60], out: [66, 35], bubble: true },
  NOR3: { w: 66, h: 56, ins: [10, 28, 46], out: [66, 28], bubble: true },
  NAND: { w: 62, h: 44, ins: [11, 33], out: [62, 22], bubble: true },
  NOR: { w: 64, h: 44, ins: [14, 33], out: [64, 22], bubble: true },
  XOR: { w: 62, h: 44, ins: [18, 33], out: [62, 22] },
  XNOR: { w: 66, h: 44, ins: [18, 33], out: [66, 22], bubble: true },
  NOT: { w: 44, h: 36, ins: [18], out: [44, 18], bubble: true },
  BUF: { w: 40, h: 36, ins: [18], out: [40, 18] },
  /** 触发器方框：上 D、下 CLK，右出 Q */
  DFF: { w: 56, h: 72, ins: [18, 54], out: [56, 36], box: true, label: "D" },
  LATCH_D: { w: 56, h: 72, ins: [18, 54], out: [56, 36], box: true, label: "D" },
  JKFF: { w: 64, h: 80, ins: [16, 40, 64], out: [64, 40], box: true, label: "JK" },
  TFF: { w: 56, h: 72, ins: [18, 54], out: [56, 36], box: true, label: "T" },
  /** MSI 方框：教材级逻辑符号 */
  DECODER138: {
    w: 170,
    h: 310,
    msi: true,
    title: "74HC138",
    left: ["A0", "A1", "A2", "S1", "/S2", "/S3"],
    right: ["/Y0", "/Y1", "/Y2", "/Y3", "/Y4", "/Y5", "/Y6", "/Y7"],
    ins: [28, 68, 108, 168, 208, 248],
    out: [170, 155],
  },
  DECODER42: {
    w: 170,
    h: 340,
    msi: true,
    title: "74HC42",
    left: ["A0", "A1", "A2", "A3"],
    right: ["/Y0", "/Y1", "/Y2", "/Y3", "/Y4", "/Y5", "/Y6", "/Y7", "/Y8", "/Y9"],
    ins: [50, 110, 170, 230],
    out: [170, 170],
  },
  MUX153: {
    w: 200,
    h: 280,
    msi: true,
    title: "74HC153",
    left: ["1G", "1C0", "1C1", "1C2", "1C3", "A", "B", "2C0", "2C1", "2C2", "2C3", "2G"],
    right: ["1Y", "2Y"],
    ins: [18, 40, 62, 84, 106, 128, 150, 172, 194, 216, 238, 260],
    out: [200, 80],
  },
};

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** 画 ANSI 门身（相对 0,0） */
function gateBody(type, g) {
  const w = g.w;
  const h = g.h;
  const mid = h / 2;
  const parts = [];
  if (type === "AND" || type === "NAND" || type === "AND3" || type === "AND4" || type === "NAND3" || type === "NAND4") {
    // 有气泡时门身止于气泡左侧，出线点 = 气泡右缘（避免线与圈脱节/叠穿）
    const bw = g.bubble ? g.out[0] - 8 : w;
    const br = Math.min(mid, bw / 2);
    parts.push(
      `<path d="M 0,0 L ${bw - br},0 A ${br},${br} 0 0 1 ${bw - br},${h} L 0,${h} Z" fill="#fff" stroke="${STROKE}" stroke-width="1.6"/>`
    );
  } else if (type === "OR" || type === "NOR" || type === "XOR" || type === "XNOR" || type === "OR3" || type === "OR4" || type === "NOR3") {
    const bw = g.bubble ? g.out[0] - 8 : w;
    const back = type === "XOR" || type === "XNOR";
    if (back) {
      parts.push(
        `<path d="M -6,0 Q 6,${mid} -6,${h}" fill="none" stroke="${STROKE}" stroke-width="1.6"/>`
      );
    }
    parts.push(
      `<path d="M 0,0 Q 14,${mid} 0,${h} Q 28,${h} ${bw},${mid} Q 28,0 0,0 Z" fill="#fff" stroke="${STROKE}" stroke-width="1.6"/>`
    );
  } else if (type === "NOT" || type === "BUF") {
    parts.push(
      `<path d="M 0,0 L ${w - (type === "NOT" ? 8 : 0)},${mid} L 0,${h} Z" fill="#fff" stroke="${STROKE}" stroke-width="1.6"/>`
    );
  } else if (g.msi) {
    parts.push(
      `<rect x="0" y="0" width="${w}" height="${h}" fill="#fff" stroke="${STROKE}" stroke-width="1.8"/>`
    );
    parts.push(
      `<text x="${w / 2}" y="18" text-anchor="middle" font-size="13" font-weight="700" font-family="${FONT}">${esc(g.title || type)}</text>`
    );
    const left = g.left || [];
    const right = g.right || [];
    const lPad = 28;
    const rPad = 28;
    const lSpan = h - lPad - 12;
    const rSpan = h - rPad - 12;
    left.forEach((lab, i) => {
      const y = lPad + (left.length === 1 ? lSpan / 2 : (i * lSpan) / (left.length - 1));
      parts.push(`<line x1="0" y1="${y}" x2="-8" y2="${y}" stroke="${STROKE}" stroke-width="1.4"/>`);
      parts.push(
        `<text x="10" y="${y + 4}" font-size="11" font-family="${FONT}">${esc(lab)}</text>`
      );
    });
    right.forEach((lab, i) => {
      const y = rPad + (right.length === 1 ? rSpan / 2 : (i * rSpan) / (right.length - 1));
      const activeLow = lab.startsWith("/") || lab.startsWith("n");
      if (activeLow) {
        parts.push(
          `<circle cx="${w}" cy="${y}" r="3.5" fill="#fff" stroke="${STROKE}" stroke-width="1.3"/>`
        );
        parts.push(`<line x1="${w + 3.5}" y1="${y}" x2="${w + 10}" y2="${y}" stroke="${STROKE}" stroke-width="1.4"/>`);
      } else {
        parts.push(`<line x1="${w}" y1="${y}" x2="${w + 8}" y2="${y}" stroke="${STROKE}" stroke-width="1.4"/>`);
      }
      parts.push(
        `<text x="${w - 10}" y="${y + 4}" text-anchor="end" font-size="11" font-family="${FONT}">${esc(lab.replace(/^\//, ""))}</text>`
      );
    });
  } else if (g.box) {
    parts.push(
      `<rect x="0" y="0" width="${w}" height="${h}" fill="#fff" stroke="${STROKE}" stroke-width="1.6"/>`
    );
    const lab = g.label || type;
    parts.push(
      `<text x="${w / 2}" y="${mid - 6}" text-anchor="middle" font-size="15" font-family="${FONT}">${esc(lab)}</text>`
    );
    if (type === "JKFF") {
      parts.push(`<text x="6" y="20" font-size="11" font-family="${FONT}">J</text>`);
      parts.push(`<text x="6" y="${mid + 4}" font-size="11" font-family="${FONT}">C</text>`);
      parts.push(`<text x="6" y="${h - 8}" font-size="11" font-family="${FONT}">K</text>`);
      parts.push(`<text x="${w - 6}" y="${mid + 4}" text-anchor="end" font-size="11" font-family="${FONT}">Q</text>`);
    } else {
      parts.push(`<text x="8" y="22" text-anchor="start" font-size="11" font-family="${FONT}">D</text>`);
      parts.push(`<text x="8" y="${h - 10}" text-anchor="start" font-size="11" font-family="${FONT}">C</text>`);
      parts.push(`<text x="${w - 8}" y="${mid + 4}" text-anchor="end" font-size="11" font-family="${FONT}">Q</text>`);
    }
  } else {
    parts.push(
      `<rect x="0" y="0" width="${w}" height="${h}" fill="#fff" stroke="${STROKE}" stroke-width="1.6"/>`
    );
    parts.push(
      `<text x="${w / 2}" y="${mid + 4}" text-anchor="middle" font-size="11" font-family="${FONT}">${esc(type)}</text>`
    );
  }
  if (g.bubble) {
    const bx = type === "NOT" ? w - 4 : g.out[0] - 4;
    const by = g.out[1];
    parts.push(
      `<circle cx="${bx}" cy="${by}" r="4" fill="#fff" stroke="${STROKE}" stroke-width="1.5"/>`
    );
  }
  return parts.join("");
}

/**
 * 解析 tbx DSL
 *
 * tbx "title" w=W h=H
 * in NAME x y
 * out NAME x y
 * gate TYPE ID x y          # 左上角；可选 pins=n 多输入均分
 * wire x1,y1 x2,y2 ...      # 折线折点
 * junction x y
 * # comment
 */
export function parseTbx(text) {
  const lines = String(text).replace(/\r\n/g, "\n").split("\n");
  const doc = {
    title: "",
    w: 480,
    h: 240,
    inputs: [],
    outputs: [],
    gates: [],
    wires: [],
    junctions: [],
  };
  for (const raw of lines) {
    const line = raw.replace(/#.*$/, "").trim();
    if (!line) continue;
    if (line.startsWith("tbx")) {
      const tm = line.match(/tbx\s+"([^"]*)"/);
      if (tm) doc.title = tm[1];
      const wm = line.match(/w\s*=\s*(\d+)/);
      const hm = line.match(/h\s*=\s*(\d+)/);
      if (wm) doc.w = +wm[1];
      if (hm) doc.h = +hm[1];
      continue;
    }
    const mIn = line.match(/^in\s+(\S+)\s+([\d.]+)\s+([\d.]+)$/);
    if (mIn) {
      doc.inputs.push({ name: mIn[1], x: +mIn[2], y: +mIn[3] });
      continue;
    }
    const mOut = line.match(/^out\s+(\S+)\s+([\d.]+)\s+([\d.]+)$/);
    if (mOut) {
      doc.outputs.push({ name: mOut[1], x: +mOut[2], y: +mOut[3] });
      continue;
    }
    const mG = line.match(/^gate\s+(\w+)\s+(\S+)\s+([\d.]+)\s+([\d.]+)(?:\s+pins=(\d+))?(?:\s+(flip))?(?:\s+showid)?$/i);
    if (mG) {
      doc.gates.push({
        type: mG[1].toUpperCase(),
        id: mG[2],
        x: +mG[3],
        y: +mG[4],
        pins: mG[5] ? +mG[5] : null,
        flip: !!mG[6],
        showId: /showid/i.test(line),
      });
      continue;
    }
    const mW = line.match(/^wire\s+(.+)$/);
    if (mW) {
      const pts = [];
      const re = /([\d.]+)\s*,\s*([\d.]+)/g;
      let mm;
      while ((mm = re.exec(mW[1]))) pts.push([+mm[1], +mm[2]]);
      if (pts.length >= 2) doc.wires.push(pts);
      continue;
    }
    const mJ = line.match(/^junction\s+([\d.]+)\s+([\d.]+)$/);
    if (mJ) {
      doc.junctions.push({ x: +mJ[1], y: +mJ[2] });
      continue;
    }
    const mL = line.match(/^label\s+(.+?)\s+([\d.]+)\s+([\d.]+)$/);
    if (mL) {
      doc.labels = doc.labels || [];
      doc.labels.push({ text: mL[1], x: +mL[2], y: +mL[3] });
      continue;
    }
    throw new Error(`tbx 无法解析: ${line}`);
  }
  return doc;
}

/** 两点线强制曼哈顿（先横后竖） */
function orthoWire(pts) {
  if (pts.length !== 2) return pts;
  const [a, b] = pts;
  if (a[0] === b[0] || a[1] === b[1]) return pts;
  return [a, [b[0], a[1]], b];
}

export function renderTbx(textOrDoc) {
  const doc = typeof textOrDoc === "string" ? parseTbx(textOrDoc) : textOrDoc;
  const parts = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${doc.w}" height="${doc.h}" viewBox="0 0 ${doc.w} ${doc.h}">`,
    `<rect width="100%" height="100%" fill="#ffffff"/>`,
  ];

  // wires first（两点自动正交）
  for (let pts of doc.wires) {
    if (pts.length === 2) pts = orthoWire(pts);
    const d = pts.map((p, i) => `${i ? "L" : "M"}${p[0]},${p[1]}`).join(" ");
    parts.push(`<path d="${d}" fill="none" stroke="${STROKE}" stroke-width="1.5"/>`);
  }

  for (const j of doc.junctions) {
    parts.push(`<circle cx="${j.x}" cy="${j.y}" r="3.2" fill="${STROKE}"/>`);
  }

  for (const g of doc.gates) {
    const base = GEOM[g.type] || { w: 50, h: 40, ins: [12, 28], out: [50, 20] };
    if (g.flip) {
      parts.push(
        `<g transform="translate(${g.x + base.w},${g.y}) scale(-1,1)">${gateBody(g.type, base)}</g>`
      );
    } else {
      parts.push(`<g transform="translate(${g.x},${g.y})">${gateBody(g.type, base)}</g>`);
    }
    if (g.showId) {
      parts.push(
        `<text x="${g.x + base.w / 2}" y="${g.y - 6}" text-anchor="middle" font-size="10" fill="#64748b" font-family="${FONT}">${esc(g.id)}</text>`
      );
    }
  }

  for (const lb of doc.labels || []) {
    parts.push(
      `<text x="${lb.x}" y="${lb.y}" font-size="12" font-style="italic" font-family="${FONT}" fill="${STROKE}">${esc(lb.text)}</text>`
    );
  }

  for (const p of doc.inputs) {
    parts.push(
      `<text x="${p.x}" y="${p.y + 5}" text-anchor="end" font-size="18" font-style="italic" font-family="${FONT}" fill="${STROKE}">${esc(p.name)}</text>`
    );
  }
  for (const p of doc.outputs) {
    parts.push(
      `<text x="${p.x}" y="${p.y + 5}" text-anchor="start" font-size="18" font-style="italic" font-family="${FONT}" fill="${STROKE}">${esc(p.name)}</text>`
    );
  }

  parts.push(`</svg>`);
  return parts.join("");
}

export function isTbx(text) {
  return /^\s*tbx\b/m.test(text);
}
