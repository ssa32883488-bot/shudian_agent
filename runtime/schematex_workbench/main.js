import { render } from "schematex";
import { isTbx, renderTbx } from "./renderers/tbx_logic.mjs";
import { waveIrToSvg } from "./adapters/wave_ir_to_svg.mjs";
import { stateIrToSvg } from "./adapters/state_ir_to_svg.mjs";

const dslEl = document.getElementById("dsl");
const preview = document.getElementById("preview");
const bookEl = document.getElementById("book");
const status = document.getElementById("status");
const meta = document.getElementById("meta");
const bookMeta = document.getElementById("book-meta");
const live = document.getElementById("live");
const showBook = document.getElementById("show-book");
const snippet = document.getElementById("snippet");
const cardPick = document.getElementById("card-pick");
const split = document.getElementById("split");
const bookPane = document.getElementById("book-pane");

const SNIPPETS = {
  tbx_l01: `tbx "L01 referee" w=420 h=200
in A 34 50
in B 34 109
in C 34 150
out Y 390 106
gate OR g1 130 95
gate AND g2 270 84
wire 42,109 144,109
wire 42,150 144,150 144,128 130,128
wire 188,117 270,117
wire 42,50 255,50 255,95 270,95
wire 326,106 380,106
`,
  logic: `logic "full_adder" style: ansi
input A, B, Cin
output Sum, Cout
s1 = XOR(A, B)
Sum = XOR(s1, Cin)
c1 = AND(A, B)
c2 = AND(s1, Cin)
Cout = OR(c1, c2)
`,
  timing: `timing "demo"
CLK: pppppppp
D:   00110011
Q:   00011100
`,
  state: `stateDiagram-v2
direction LR
[*] --> S00
S00 --> S01 : /0
S01 --> S10 : /0
S10 --> S11 : /1
S11 --> S00 : /1
`,
};

function setStatus(text, cls) {
  status.textContent = text;
  status.className = "status" + (cls ? ` ${cls}` : "");
}

function doRender() {
  const dsl = dslEl.value.trim();
  if (!dsl) {
    preview.innerHTML = '<p class="placeholder">在左侧粘贴 DSL / tbx</p>';
    meta.textContent = "";
    setStatus("空脚本");
    return;
  }
  try {
    let svg;
    let type;
    if (isTbx(dsl)) {
      svg = renderTbx(dsl);
      type = "tbx";
    } else {
      svg = render(dsl);
      type = (dsl.match(/^(\w[\w-]*)/m) || ["?", "?"])[1];
    }
    if (typeof svg !== "string" || !svg.includes("<svg")) {
      throw new Error("render 未返回合法 SVG");
    }
    preview.innerHTML = svg;
    meta.textContent = `type=${type} · ${svg.length} chars`;
    setStatus("渲染成功", "ok");
  } catch (e) {
    preview.innerHTML = `<p class="placeholder">渲染失败</p>`;
    meta.textContent = "";
    setStatus(String(e && e.message ? e.message : e), "err");
  }
}

function syncBookPane() {
  const on = showBook.checked;
  bookPane.style.display = on ? "" : "none";
  split.classList.toggle("three", on);
  split.classList.toggle("two", !on);
}

let timer = null;
function schedule() {
  if (!live.checked) return;
  clearTimeout(timer);
  timer = setTimeout(doRender, 220);
}

document.getElementById("btn-render").addEventListener("click", doRender);
document.getElementById("btn-clear").addEventListener("click", () => {
  dslEl.value = "";
  doRender();
});
dslEl.addEventListener("input", schedule);
showBook.addEventListener("change", syncBookPane);
snippet.addEventListener("change", () => {
  const key = snippet.value;
  if (key && SNIPPETS[key]) {
    dslEl.value = SNIPPETS[key];
    doRender();
  }
  snippet.value = "";
});

async function loadCard(id) {
  if (!id) return;
  const cardUrl = `/gold/level1/cards/${id}/card.json`;
  const card = await fetch(cardUrl).then((r) => r.json());
  bookMeta.textContent = `${id} · 图${card.fig_id}`;
  const imgPath = card.image.replace("../../textbook_figures/", "/textbook_figures/");
  bookEl.innerHTML = `<img src="${imgPath}" alt="${id}"/>`;

  // 优先 gold.tbx → from_ir.stx → wave ir.json
  const tryUrls = [
    `/gold/level1/cards/${id}/gold.tbx`,
    `/gold/level1/cards/${id}/from_ir.stx`,
  ];
  for (const u of tryUrls) {
    const res = await fetch(u);
    if (res.ok) {
      dslEl.value = await res.text();
      doRender();
      return;
    }
  }
  if (card.ir_schema === "wave_ir_v1" || card.render_engine?.includes("timing") || card.render_engine?.includes("wave")) {
    const irRes = await fetch(`/gold/level1/cards/${id}/ir.json`);
    if (irRes.ok) {
      const ir = await irRes.json();
      const svg = waveIrToSvg(ir);
      preview.innerHTML = svg;
      dslEl.value = JSON.stringify(ir, null, 2);
      meta.textContent = `type=wave_ir · ${svg.length} chars`;
      setStatus("波形 IR 渲染成功", "ok");
      return;
    }
  }
  if (card.ir_schema === "state_ir_v1" || card.bucket === "state") {
    const irRes = await fetch(`/gold/level1/cards/${id}/ir.json`);
    if (irRes.ok) {
      const ir = await irRes.json();
      const svg = stateIrToSvg(ir);
      preview.innerHTML = svg;
      dslEl.value = JSON.stringify(ir, null, 2);
      meta.textContent = `type=state_ir · ${svg.length} chars`;
      setStatus("状态 IR 渲染成功", "ok");
      return;
    }
  }
  setStatus(`${id} 无 gold.tbx / from_ir.stx / wave|state ir`, "err");
}

async function initCards() {
  try {
    const man = await fetch("/gold/level1/manifest.json").then((r) => r.json());
    for (const c of man.cards || []) {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = `${c.id} · ${c.fig_id}`;
      cardPick.appendChild(opt);
    }
  } catch {
    /* ignore */
  }
  cardPick.addEventListener("change", () => loadCard(cardPick.value));
}

const params = new URLSearchParams(location.search);
initCards().then(() => {
  const id = params.get("card") || "L01";
  cardPick.value = id;
  loadCard(id);
});
syncBookPane();
