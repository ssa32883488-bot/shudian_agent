/**
 * State IR → 阎石教材风状态转换图
 *
 * 结论：Graphviz/circo/neato/dot 无法复现课本「上下两排跑道」。
 * 本渲染器以 positions 金标 / racetrack / square / triangle 为主；双向边分离弧线。
 */
import {
  buildEdgeMeta,
  createEdgeCounters,
  routeEdge,
  loopMidAt,
  markOffset,
} from "../lib/state_edge_route.mjs";

const FONT = "Times New Roman, Songti SC, SimSun, serif";
const STROKE = "#333333";

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function hypot(x, y) {
  return Math.hypot(x, y) || 1;
}

function onCircle(cx, cy, tx, ty, r, inset = 0) {
  const dx = tx - cx;
  const dy = ty - cy;
  const d = hypot(dx, dy);
  const rr = r + inset;
  return [cx + (dx / d) * rr, cy + (dy / d) * rr];
}

function buildAdj(transitions) {
  const adj = new Map();
  for (const t of transitions) {
    if (!adj.has(t.from)) adj.set(t.from, []);
    adj.get(t.from).push(t.to);
  }
  return adj;
}

function longestCycle(states, transitions) {
  const adj = buildAdj(transitions);
  const set = new Set(states);
  let best = [];

  function dfs(start, cur, path, visited) {
    for (const nxt of adj.get(cur) || []) {
      if (!set.has(nxt)) continue;
      if (nxt === start && path.length >= 2) {
        if (path.length > best.length) best = path.slice();
        continue;
      }
      if (visited.has(nxt) || path.length >= states.length) continue;
      visited.add(nxt);
      path.push(nxt);
      dfs(start, nxt, path, visited);
      path.pop();
      visited.delete(nxt);
    }
  }

  for (const s of states) {
    const visited = new Set([s]);
    dfs(s, s, [s], visited);
  }
  return best;
}

function inferLegend(ir) {
  if (ir.legend && (ir.legend.state_label || ir.legend.edge_label)) {
    return {
      state_label: ir.legend.state_label || "",
      edge_label: ir.legend.edge_label || "",
      style: ir.legend.style || "circle",
      position: ir.legend.position || null,
    };
  }
  const sample = (ir.states || [])[0] || "";
  const bits = /^\d+$/.test(sample) ? sample.length : 0;
  let state_label = "";
  if (bits === 2) state_label = "Q1Q0";
  else if (bits === 3) state_label = "Q3Q2Q1";
  else if (bits === 4) state_label = "Q3Q2Q1Q0";
  else if (bits === 1) state_label = "Q";
  const labs = (ir.transitions || []).map((t) => t.label || "");
  const edge_label = labs.some((l) => /^\d+\//.test(l)) ? "X/Y" : "/Y";
  return { state_label, edge_label, style: "circle", position: null };
}

function rotateCycleMin(cycle) {
  if (!cycle.length) return cycle;
  if (!cycle.every((s) => /^\d+$/.test(s))) return cycle.slice();
  let bestI = 0;
  for (let i = 1; i < cycle.length; i++) if (cycle[i] < cycle[bestI]) bestI = i;
  return cycle.slice(bestI).concat(cycle.slice(0, bestI));
}

/**
 * 阎石 6.2.2 式：上排左→右主序列前半，下排左→右 = 旁支 + 主序列后半倒序
 * 例：上 000 001 010 011；下 111 110 101 100
 */
function layoutRacetrack(cycle, outliers, opts = {}) {
  const k = cycle.length;
  const nTop = Math.ceil(k / 2);
  const top = cycle.slice(0, nTop);
  const bottomCore = cycle.slice(nTop).reverse();
  const bottom = [...outliers, ...bottomCore];

  const cols = Math.max(top.length, bottom.length);
  const rNode = opts.rNode ?? (cols >= 5 ? 26 : 30);
  const gapX = opts.gapX ?? 110;
  const yTop = opts.yTop ?? 70;
  const yBot = opts.yBot ?? 210;
  const x0 = opts.x0 ?? 70;
  const coords = new Map();

  // 上排左对齐、下排左对齐（旁支在左），使 000 与 111 同列
  for (let i = 0; i < top.length; i++) coords.set(top[i], [x0 + i * gapX, yTop]);
  for (let i = 0; i < bottom.length; i++) coords.set(bottom[i], [x0 + i * gapX, yBot]);

  const w = x0 + (cols - 1) * gapX + 160;
  const h = yBot + 70;
  return { coords, rNode, w, h, yTop, yBot };
}

function layoutRing(states) {
  const n = states.length;
  const rNode = n > 8 ? 24 : 28;
  const R = Math.min(150, 50 + n * 12);
  const cx = 60 + R;
  const cy = 40 + R;
  const coords = new Map();
  for (let i = 0; i < n; i++) {
    const ang = -Math.PI / 2 + (i * 2 * Math.PI) / n;
    coords.set(states[i], [cx + R * Math.cos(ang), cy + R * Math.sin(ang)]);
  }
  return { coords, rNode, w: cx + R + 140, h: cy + R + 60 };
}

function layoutFree(states, positions) {
  const coords = new Map();
  let maxX = 0;
  let maxY = 0;
  for (const s of states) {
    const p = positions[s];
    if (!p || p.length < 2) throw new Error(`free layout 缺 positions[${s}]`);
    const x = +p[0];
    const y = +p[1];
    coords.set(s, [x, y]);
    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
  }
  const rNode = states.some((s) => s.length >= 4) ? 26 : states.length >= 7 ? 27 : 30;
  return { coords, rNode, w: maxX + 120, h: maxY + 70 };
}

/** 四角方阵：TL TR BR BL（阎石 4 状态图） */
function layoutSquare(states, order) {
  const gapX = 110;
  const gapY = 140;
  const x0 = 70;
  const yTop = 70;
  const corners = order || states;
  const coords = new Map();
  coords.set(corners[0], [x0, yTop]);
  coords.set(corners[1], [x0 + gapX, yTop]);
  coords.set(corners[2], [x0 + gapX, yTop + gapY]);
  coords.set(corners[3], [x0, yTop + gapY]);
  return { coords, rNode: 30, w: x0 + gapX + 160, h: yTop + gapY + 80, yTop, yBot: yTop + gapY };
}

/** 三状态三角：S0 左上 S1 右上 S2 下中 */
function layoutTriangle(states) {
  const order =
    states.every((s) => /^S\d+$/.test(s)) ? ["S0", "S1", "S2"].filter((s) => states.includes(s)) : states;
  const coords = new Map();
  coords.set(order[0], [70, 70]);
  coords.set(order[1], [220, 70]);
  coords.set(order[2], [145, 210]);
  return { coords, rNode: 28, w: 360, h: 280, yTop: 70, yBot: 210 };
}

function inferSquareOrder(states) {
  if (states.length !== 4) return states;
  if (states.includes("S0") && states.includes("S3")) return ["S0", "S1", "S2", "S3"];
  if (states.every((s) => /^\d{2}$/.test(s))) return ["00", "01", "10", "11"];
  return states;
}

function pickAutoLayout(ir, states, cycle) {
  if (ir.positions && Object.keys(ir.positions).length >= states.length) return "free";
  if (states.length === 3 && states.every((s) => /^S\d+$/.test(s))) return "triangle";
  if (states.length === 4) {
    if (states.every((s) => /^S[0-3]$/.test(s) || /^\d{2}$/.test(s))) return "square";
  }
  if (cycle.length >= Math.max(3, states.length - 2) && states.length >= 4) return "racetrack";
  return "ring";
}

function pairKey(a, b) {
  return a < b ? `${a}||${b}` : `${b}||${a}`;
}

/** 按 route 绘制边（双向分离弧线 / 平行边错开） */
function edgeGeometryRouted(from, to, coords, rNode, route) {
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  const gap = 1.5;

  if (from === to) {
    const R = rNode * 1.05;
    if (route.loopDir === "loop below") {
      const sx = x1;
      const sy = y1 + rNode;
      const path = `M ${sx},${sy} C ${sx + R * 1.7},${sy + R * 1.6} ${sx - R * 1.7},${sy + R * 1.6} ${sx},${sy}`;
      return { path, labelAt: [x1, y1 + rNode + R * 1.4], midAt: [x1, y1 + rNode + R * 0.9] };
    }
    if (route.loopDir === "loop right") {
      const sx = x1 + rNode;
      const sy = y1;
      const path = `M ${sx},${sy} C ${sx + R * 1.6},${sy - R * 1.7} ${sx + R * 1.6},${sy + R * 1.7} ${sx},${sy}`;
      return { path, labelAt: [x1 + rNode + R * 1.2, y1], midAt: [x1 + rNode + R * 0.85, y1] };
    }
    if (route.loopDir === "loop left") {
      const sx = x1 - rNode;
      const sy = y1;
      const path = `M ${sx},${sy} C ${sx - R * 1.6},${sy - R * 1.7} ${sx - R * 1.6},${sy + R * 1.7} ${sx},${sy}`;
      return { path, labelAt: [x1 - rNode - R * 1.2, y1], midAt: [x1 - rNode - R * 0.85, y1] };
    }
    const sx = x1;
    const sy = y1 - rNode;
    const path = `M ${sx},${sy} C ${sx + R * 1.7},${sy - R * 1.9} ${sx - R * 1.7},${sy - R * 1.9} ${sx},${sy}`;
    return { path, labelAt: [x1, y1 - rNode - R * 1.55], midAt: [x1, y1 - rNode - R * 0.95] };
  }

  const dx = x2 - x1;
  const dy = y2 - y1;
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const len = hypot(dx, dy);
  const nx = (-dy / len) * (route.bend || 0);
  const ny = (dx / len) * (route.bend || 0);

  if (route.kind === "line") {
    const a = onCircle(x1, y1, x2, y2, rNode, gap);
    const b = onCircle(x2, y2, x1, y1, rNode, gap);
    const path = `M ${a[0]},${a[1]} L ${b[0]},${b[1]}`;
    const lift = Math.abs(dy) < 12 ? -11 : -10;
    return { path, labelAt: [mx, my + lift], midAt: [mx, my] };
  }

  if (route.kind === "quad") {
    const { cpx, cpy } = route;
    const p1 = onCircle(x1, y1, cpx, cpy, rNode, gap);
    const p2 = onCircle(x2, y2, cpx, cpy, rNode, gap);
    const lx = cpx + (cpx - mx) * 0.12;
    const ly = cpy + (cpy - my) * 0.12 - 6;
    return {
      path: `M ${p1[0]},${p1[1]} Q ${cpx},${cpy} ${p2[0]},${p2[1]}`,
      labelAt: [lx, ly],
      midAt: [cpx, cpy],
    };
  }

  const bx = mx + nx;
  const by = my + ny;
  const p1 = onCircle(x1, y1, bx, by, rNode, gap);
  const p2 = onCircle(x2, y2, bx, by, rNode, gap);
  const labelAt = [bx + nx * 0.15, by + ny * 0.15 - 8];
  return { path: `M ${p1[0]},${p1[1]} Q ${bx},${by} ${p2[0]},${p2[1]}`, labelAt, midAt: [bx, by] };
}

/** 共享布局：供 SVG / TikZ 等后端复用 */
export function computeStateLayout(ir) {
  if (!ir || ir.diagram_type !== "state") throw new Error("diagram_type 必须为 state");
  if (ir.schema_version !== "state_ir_v1") throw new Error("schema_version 必须为 state_ir_v1");
  const states = ir.states || [];
  const transitions = ir.transitions || [];
  if (states.length < 2) throw new Error("states 至少 2 个");

  const cycle = rotateCycleMin(longestCycle(states, transitions));
  const cycleSet = new Set(cycle);
  const outliers = states.filter((s) => !cycleSet.has(s));

  let mode = ir.layout || "auto";
  if (mode === "auto") mode = pickAutoLayout(ir, states, cycle);

  let laid;
  if (mode === "free" || (ir.positions && Object.keys(ir.positions).length >= states.length)) {
    laid = layoutFree(states, ir.positions);
    mode = "free";
  } else if (mode === "square" && states.length === 4) {
    laid = layoutSquare(states, inferSquareOrder(states));
  } else if (mode === "triangle" && states.length === 3) {
    laid = layoutTriangle(states);
  } else if (mode === "racetrack" && cycle.length >= 3) {
    laid = layoutRacetrack(cycle, outliers);
  } else {
    laid = layoutRing(states);
    mode = "ring";
  }

  return {
    states,
    transitions,
    mode,
    laid,
    legend: inferLegend(ir),
    coords: laid.coords,
    rNode: laid.rNode,
    w: laid.w,
    h: laid.h,
  };
}

export function stateIrToSvg(ir) {
  const { states, transitions, mode, laid, legend, coords, rNode } = computeStateLayout(ir);
  let w = laid.w;
  let h = laid.h;

  // 图例占位加宽（圆图例才占右侧）
  if (legend.style !== "text" && (legend.state_label || legend.edge_label)) {
    w = Math.max(w, [...coords.values()].reduce((m, p) => Math.max(m, p[0]), 0) + 150);
  }

  const edgeMeta = buildEdgeMeta(transitions);
  const counters = createEdgeCounters();

  function forbiddenMark(from, to, coords, g, route) {
    let mid = g.midAt;
    if (route.kind === "loop") mid = loopMidAt(from, coords, rNode, route.loopDir);
    const [mx, my] = markOffset(from, to, coords, mid);
    const s = 7;
    return [
      `<rect x="${mx - s - 2}" y="${my - s - 2}" width="${(s + 2) * 2}" height="${(s + 2) * 2}" fill="#fff" stroke="none"/>`,
      `<line x1="${mx - s}" y1="${my - s}" x2="${mx + s}" y2="${my + s}" stroke="${STROKE}" stroke-width="1.5"/>`,
      `<line x1="${mx - s}" y1="${my + s}" x2="${mx + s}" y2="${my - s}" stroke="${STROKE}" stroke-width="1.5"/>`,
    ];
  }

  const parts = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" data-layout="${mode}">`,
    `<rect width="100%" height="100%" fill="#ffffff"/>`,
    `<defs><marker id="arrow" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">`,
    `<path d="M 0 1.2 L 9 5 L 0 8.8 z" fill="${STROKE}"/></marker></defs>`,
  ];

  if (ir.show_title) {
    parts.push(
      `<text x="${w / 2}" y="22" text-anchor="middle" font-size="13" font-weight="700" font-family="${FONT}">${esc(ir.title || "")}</text>`
    );
  }

  const edgeMarks = [];

  transitions.forEach((t) => {
    if (!coords.has(t.from) || !coords.has(t.to)) return;
    const route = routeEdge(t.from, t.to, coords, edgeMeta, counters);
    const g = edgeGeometryRouted(t.from, t.to, coords, rNode, route);
    const dashed = t.style === "dashed";
    const dash = dashed ? ` stroke-dasharray="5 3"` : "";
    parts.push(
      `<path d="${g.path}" fill="none" stroke="${STROKE}" stroke-width="1.35"${dash} marker-end="url(#arrow)"/>`
    );
    if (t.forbidden) edgeMarks.push(forbiddenMark(t.from, t.to, coords, g, route));
    if (t.label) {
      parts.push(
        `<text x="${g.labelAt[0]}" y="${g.labelAt[1]}" text-anchor="middle" font-size="13" font-family="${FONT}" fill="#222">${esc(t.label)}</text>`
      );
    }
  });

  for (const s of states) {
    const [x, y] = coords.get(s);
    parts.push(
      `<circle cx="${x}" cy="${y}" r="${rNode}" fill="#fff" stroke="${STROKE}" stroke-width="1.5"/>`
    );
    const fs = s.length >= 4 ? 12 : 14;
    parts.push(
      `<text x="${x}" y="${y + 5}" text-anchor="middle" font-size="${fs}" font-weight="600" font-family="${FONT}" fill="#111">${esc(s)}</text>`
    );
  }

  for (const mk of edgeMarks) parts.push(...mk);

  // 图例：圆（阎石多数图）或纯文字（如 6.4.26 的 Q1Q2Q3）
  if (legend.state_label || legend.edge_label) {
    if (legend.style === "text") {
      const [lx, ly] = legend.position || [40, 36];
      const text = legend.edge_label
        ? `${legend.state_label} ${legend.edge_label}`
        : `(${legend.state_label})`;
      parts.push(
        `<text x="${lx}" y="${ly}" font-size="13" font-family="${FONT}" fill="#111">${esc(text)}</text>`
      );
    } else {
      let maxX = 0;
      let midY = h / 2;
      for (const [, p] of coords) {
        maxX = Math.max(maxX, p[0]);
        midY = laid.yTop && laid.yBot ? (laid.yTop + laid.yBot) / 2 : midY;
      }
      const lx = maxX + 100;
      const ly = midY;
      const lr = 36;
      parts.push(
        `<circle cx="${lx}" cy="${ly}" r="${lr}" fill="#fff" stroke="${STROKE}" stroke-width="1.5"/>`
      );
      if (legend.state_label) {
        parts.push(
          `<text x="${lx}" y="${ly - 2}" text-anchor="middle" font-size="12" font-family="${FONT}">${esc(legend.state_label)}</text>`
        );
      }
      if (legend.edge_label) {
        parts.push(
          `<text x="${lx}" y="${ly + 16}" text-anchor="middle" font-size="13" font-family="${FONT}">${esc(legend.edge_label)}</text>`
        );
      }
    }
  }

  parts.push(`</svg>`);
  return parts.join("");
}

export function selfCheckStateSvg(ir, svg) {
  const states = ir.states || [];
  const transitions = ir.transitions || [];
  const checks = [
    {
      id: "HAS_CIRCLES",
      ok: (svg.match(/<circle /g) || []).length >= states.length,
      detail: `states=${states.length}`,
    },
    {
      id: "HAS_EDGES",
      ok: (svg.match(/<path d=/g) || []).length >= transitions.length,
      detail: `edges=${transitions.length}`,
    },
    {
      id: "LABELS",
      ok: transitions.every((t) => !t.label || svg.includes(esc(t.label))),
      detail: "labels",
    },
    { id: "NO_NAN", ok: !/NaN|undefined/.test(svg), detail: "coords" },
  ];
  const ok = checks.every((c) => c.ok);
  return { ok, grade: ok ? "STATE_SELF_OK" : "STATE_SELF_FAIL", checks };
}
