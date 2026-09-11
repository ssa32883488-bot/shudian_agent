/** 状态图边路由：双向 = 两条独立二次弧（眼形），来去绝不合并 */

export function pairKey(a, b) {
  return a < b ? `${a}||${b}` : `${b}||${a}`;
}

export function buildEdgeMeta(transitions) {
  const undirected = new Map();
  const directed = new Map();
  for (const t of transitions) {
    if (t.from === t.to) continue;
    const k = pairKey(t.from, t.to);
    undirected.set(k, (undirected.get(k) || 0) + 1);
    const dk = `${t.from}>${t.to}`;
    directed.set(dk, (directed.get(dk) || 0) + 1);
  }
  return { undirected, directed };
}

function hypot(x, y) {
  return Math.hypot(x, y) || 1;
}

function layoutCenter(coords) {
  let cx = 0;
  let cy = 0;
  for (const [, p] of coords) {
    cx += p[0];
    cy += p[1];
  }
  return [cx / coords.size, cy / coords.size];
}

function canonicalPair(from, to, coords) {
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  if (Math.abs(x1 - x2) > 8) return x1 < x2 ? [from, to] : [to, from];
  return y1 < y2 ? [from, to] : [to, from];
}

/** 边中点指向布局外侧的单位法向（方阵四边 / 三角均适用） */
function outwardNormal(from, to, coords) {
  const [cx, cy] = layoutCenter(coords);
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const nx = mx - cx;
  const ny = my - cy;
  const n = hypot(nx, ny);
  if (n < 1e-6) return [0, -1];
  return [nx / n, ny / n];
}

function labelFromNormal(nx, ny) {
  if (Math.abs(nx) > Math.abs(ny)) return nx >= 0 ? "right" : "left";
  return ny >= 0 ? "below" : "above";
}

/** 节点在布局中的象限角色，用于自环方向 */
export function nodeCorner(state, coords) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const [, p] of coords) {
    minX = Math.min(minX, p[0]);
    maxX = Math.max(maxX, p[0]);
    minY = Math.min(minY, p[1]);
    maxY = Math.max(maxY, p[1]);
  }
  const [x, y] = coords.get(state);
  const left = x <= minX + 8;
  const right = x >= maxX - 8;
  const top = y <= minY + 8;
  const bottom = y >= maxY - 8;
  if (top && left) return "tl";
  if (top && right) return "tr";
  if (bottom && right) return "br";
  if (bottom && left) return "bl";
  if (top) return "t";
  if (bottom) return "b";
  if (left) return "l";
  if (right) return "r";
  return "c";
}

function routeQuad(from, to, coords, offset, flip = false) {
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  let [nx, ny] = outwardNormal(from, to, coords);
  if (flip) {
    nx = -nx;
    ny = -ny;
  }
  const cpx = mx + nx * offset;
  const cpy = my + ny * offset;
  return { kind: "quad", cpx, cpy, labelPos: labelFromNormal(nx, ny) };
}

/**
 * 双向边：canonical A→B 走外弧，B→A 走内弧 —— 两条独立二次曲线
 * @returns {{ kind: 'loop'|'quad'|'line', cpx?: number, cpy?: number, labelPos: string, loopDir?: string }}
 */
export function routeEdge(from, to, coords, meta, counters) {
  if (from === to) {
    const corner = nodeCorner(from, coords);
    let loopDir = "loop above";
    let labelPos = "above";
    if (corner === "tr") {
      loopDir = "loop right";
      labelPos = "right";
    } else if (corner === "tl" || corner === "l") {
      loopDir = "loop left";
      labelPos = "left";
    } else if (corner === "bl" || corner === "br") {
      loopDir = "loop below";
      labelPos = "below";
    }
    return { kind: "loop", labelPos, loopDir };
  }

  const k = pairKey(from, to);
  const dk = `${from}>${to}`;
  const isBidirectional = (meta.undirected.get(k) || 0) >= 2;
  const parallel = meta.directed.get(dk) || 1;
  const parIdx = counters.parallel.get(dk) || 0;
  counters.parallel.set(dk, parIdx + 1);

  if (isBidirectional) {
    const [a, b] = canonicalPair(from, to, coords);
    const isForward = from === a;
    // 外弧 32pt / 内弧 32pt，控制点在中点两侧 → 眼形双轨
    return routeQuad(from, to, coords, 32, !isForward);
  }

  if (parallel > 1) {
    const extra = parIdx * 14;
    return routeQuad(from, to, coords, 36 + extra, parIdx % 2 === 1);
  }

  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  const sameRow = Math.abs(y2 - y1) < 20;
  const sameCol = Math.abs(x2 - x1) < 20;

  // 单向边优先直线（课本 6.4.26 式对角/正交）
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  let labelPos = "above";
  if (sameRow) labelPos = "above";
  else if (sameCol) labelPos = "right";
  else if (x2 > x1 && y2 > y1) labelPos = "above right";
  else if (x2 > x1) labelPos = "below right";
  else labelPos = "above left";
  return { kind: "line", labelPos, cpx: mx, cpy: my };
}

/** 自环叉号 / 标注应落在环外，而非圆心 */
export function loopMidAt(state, coords, rNode, loopDir) {
  const [x, y] = coords.get(state);
  const R = rNode * 1.85;
  if (loopDir === "loop right") return [x + R, y];
  if (loopDir === "loop left") return [x - R, y];
  if (loopDir === "loop below") return [x, y + R];
  return [x, y - R];
}

export function markOffset(from, to, coords, midAt) {
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  let [mx, my] = midAt;
  if (from === to) return midAt;
  if (Math.abs(y2 - y1) < 20) return [mx, my - 11];
  if (Math.abs(x2 - x1) < 20) return [mx + 11, my];
  return midAt;
}

export function createEdgeCounters() {
  return { bidir: new Map(), parallel: new Map() };
}
