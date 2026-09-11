/**
 * TikZ 源码 → SVG（node-tikzjax WASM，无需本地 TeX）
 */
import tikzjax from "node-tikzjax";

const tex2svg = typeof tikzjax === "function" ? tikzjax : tikzjax.default;

const TIKZ_OPTS = {
  showConsole: false,
  tikzLibraries: "automata,positioning,arrows.meta,calc",
};

export async function tikzToSvg(source) {
  if (typeof tex2svg !== "function") {
    throw new Error("node-tikzjax default export missing");
  }
  return tex2svg(source, TIKZ_OPTS);
}

export async function stateIrToTikzSvg(ir, { writeTex } = {}) {
  const { stateIrToTikz } = await import("./state_ir_to_tikz.mjs");
  const tex = stateIrToTikz(ir);
  if (writeTex) writeTex(tex);
  const svg = await tikzToSvg(tex);
  return { tex, svg };
}
