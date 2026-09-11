/**
 * State IR → TikZ (automata) 源码
 */
import { computeStateLayout } from "./state_ir_to_svg.mjs";
import {
  buildEdgeMeta,
  createEdgeCounters,
  routeEdge,
  loopMidAt,
  markOffset,
} from "../lib/state_edge_route.mjs";

function escTex(s) {
  return String(s)
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/([&%$#_{}])/g, "\\$1")
    .replace(/~/g, "\\textasciitilde{}")
    .replace(/\^/g, "\\textasciicircum{}");
}

function nodeId(state) {
  return `s${state.replace(/[^A-Za-z0-9]/g, "_")}`;
}

function tikzLabelPos(pos) {
  if (pos.includes(",")) return pos;
  return pos;
}

function resolveMid(from, to, coords, route, rNode) {
  if (route.kind === "quad") return [route.cpx, route.cpy];
  if (route.kind === "loop") return loopMidAt(from, coords, rNode, route.loopDir);
  const [x1, y1] = coords.get(from);
  const [x2, y2] = coords.get(to);
  return [(x1 + x2) / 2, (y1 + y2) / 2];
}

export function stateIrToTikz(ir) {
  const { states, transitions, coords, rNode, legend, h, laid } = computeStateLayout(ir);
  const edgeMeta = buildEdgeMeta(transitions);
  const counters = createEdgeCounters();
  const markLines = [];
  const edgeLines = [];

  const lines = [];
  lines.push("% state_ir_v1 → TikZ (generated)");
  lines.push("\\begin{document}");
  lines.push("\\begin{tikzpicture}[");
  lines.push("  x=1pt, y=-1pt,");
  lines.push("  >=Stealth,");
  lines.push("  every node/.style={font=\\rmfamily},");
  lines.push(
    `  state/.style={circle, draw=black!75, line width=0.95pt, minimum size=${(rNode * 2).toFixed(1)}pt, inner sep=0pt, font=\\bfseries},`
  );
  lines.push("  every edge/.style={draw=black!75, line width=0.95pt},");
  lines.push("  edge label/.style={font=\\rmfamily, fill=white, inner sep=1pt}");
  lines.push("]");

  for (const s of states) {
    const [x, y] = coords.get(s);
    const fs = s.length >= 4 ? "\\small" : "";
    lines.push(`  \\node[state] (${nodeId(s)}) at (${x}, ${y}) {${fs}${escTex(s)}};`);
  }

  for (const t of transitions) {
    if (!coords.has(t.from) || !coords.has(t.to)) continue;
    const route = routeEdge(t.from, t.to, coords, edgeMeta, counters);
    const label = t.label ? ` node[edge label, ${tikzLabelPos(route.labelPos)}] {${escTex(t.label)}}` : "";
    const dashed = t.style === "dashed";
    const dash = dashed ? "dashed, " : "";

    if (route.kind === "loop") {
      edgeLines.push(
        `  \\draw[${dash}->] (${nodeId(t.from)}) edge[${route.loopDir}, min distance=${(rNode * 2.15).toFixed(0)}pt]${label} (${nodeId(t.to)});`
      );
    } else if (route.kind === "line") {
      edgeLines.push(`  \\draw[${dash}->] (${nodeId(t.from)}) --${label} (${nodeId(t.to)});`);
    } else if (route.kind === "quad") {
      edgeLines.push(
        `  \\draw[${dash}->] (${nodeId(t.from)}) .. controls (${route.cpx.toFixed(1)}, ${route.cpy.toFixed(1)}) ..${label} (${nodeId(t.to)});`
      );
    }

    if (t.forbidden) {
      const mid = resolveMid(t.from, t.to, coords, route, rNode);
      const [mx, my] = markOffset(t.from, t.to, coords, mid);
      markLines.push(`  \\fill[white] (${(mx - 9).toFixed(1)}, ${(my - 9).toFixed(1)}) rectangle (${(mx + 9).toFixed(1)}, ${(my + 9).toFixed(1)});`);
      markLines.push(`  \\draw[line width=0.95pt] (${(mx - 6).toFixed(1)}, ${(my - 6).toFixed(1)}) -- (${(mx + 6).toFixed(1)}, ${(my + 6).toFixed(1)});`);
      markLines.push(`  \\draw[line width=0.95pt] (${(mx - 6).toFixed(1)}, ${(my + 6).toFixed(1)}) -- (${(mx + 6).toFixed(1)}, ${(my - 6).toFixed(1)});`);
    }
  }

  lines.push(...edgeLines);
  lines.push(...markLines);

  if (legend.state_label || legend.edge_label) {
    if (legend.style === "text") {
      const [lx, ly] = legend.position || [40, 36];
      const text = legend.edge_label
        ? `${legend.state_label} ${legend.edge_label}`
        : `(${legend.state_label})`;
      lines.push(`  \\node[font=\\rmfamily] at (${lx}, ${ly}) {${escTex(text)}};`);
    } else {
      let maxX = 0;
      let midY = h / 2;
      for (const [, p] of coords) {
        maxX = Math.max(maxX, p[0]);
        if (laid.yTop != null && laid.yBot != null) midY = (laid.yTop + laid.yBot) / 2;
      }
      const lx = maxX + 100;
      const ly = midY;
      const lr = 36;
      lines.push(`  \\node[circle, draw=black!75, line width=0.95pt, minimum size=${lr * 2}pt, inner sep=0pt] (legend) at (${lx}, ${ly}) {};`);
      if (legend.state_label) {
        lines.push(`  \\node at (${lx}, ${ly - 4}) {\\small ${escTex(legend.state_label)}};`);
      }
      if (legend.edge_label) {
        lines.push(`  \\node at (${lx}, ${ly + 14}) {${escTex(legend.edge_label)}};`);
      }
    }
  }

  lines.push("\\end{tikzpicture}");
  lines.push("\\end{document}");
  return lines.join("\n");
}
