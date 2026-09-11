/**
 * Level-1 全量 50 卡：IR → 渲染 → card.json → gallery
 */
import fs from "fs";
import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";
import { logicIrToSchematex } from "../adapters/logic_ir_to_schematex.mjs";
import { stateIrToSvg } from "../adapters/state_ir_to_svg.mjs";
import { waveIrToSvg } from "../adapters/wave_ir_to_svg.mjs";
import { IRS } from "./level1_all_irs.mjs";

const require = createRequire(import.meta.url);
const { render } = require("schematex");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CARDS = path.join(ROOT, "gold", "level1", "cards");

const SIMPLE_A = new Set(["L01", "L07", "L08", "L09", "C05", "C06"]);
const XOR_C = new Set(["L03"]);
const PLA_B = new Set(["L04", "L05", "C04"]);
const CHIP_C = new Set(["C08", "C09"]);
const HEAVY_B = new Set(["L02", "L06", "L10", "C01", "C02", "C03", "C07", "C10"]);

function gradeLogic(id, renderOk, ir) {
  if (!renderOk) {
    return { grade: "PARSE_OK", fail_reasons: ["LAYOUT"], tier_guess: ir._tier || "B", notes: "渲染失败" };
  }
  if (SIMPLE_A.has(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["JUNCTION_MISSING", "CROSSING", "SYMBOL_STYLE"],
      tier_guess: "A",
      notes: "拓扑可对；未达 TEXTBOOK_OK",
    };
  }
  if (XOR_C.has(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["FANOUT_ERROR", "LAYOUT", "SYMBOL_STYLE"],
      tier_guess: "C",
      notes: "异或展开建议 C",
    };
  }
  if (PLA_B.has(id) || CHIP_C.has(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["LAYOUT", "FANOUT_ERROR", "JUNCTION_MISSING", "SPACING"],
      tier_guess: CHIP_C.has(id) ? "C" : "B",
      notes: "总线/芯片图版式难",
    };
  }
  if (id.startsWith("F")) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["LAYOUT", "FANOUT_ERROR", "JUNCTION_MISSING", "SYMBOL_STYLE"],
      tier_guess: ir._tier || "B",
      notes: "时序/锁存；Schematex 布局≠课本",
    };
  }
  if (HEAVY_B.has(id) || id.startsWith("C") || id.startsWith("L")) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["FANOUT_ERROR", "JUNCTION_MISSING", "CROSSING", "LAYOUT", "SYMBOL_STYLE"],
      tier_guess: ir._tier || "B",
      notes: "拓扑大致正确",
    };
  }
  return { grade: "RENDER_OK", fail_reasons: ["LAYOUT"], tier_guess: "B", notes: "" };
}

function gradeState(renderOk) {
  if (!renderOk) return { grade: "PARSE_OK", fail_reasons: ["LAYOUT"], tier_guess: "C", notes: "渲染失败" };
  return {
    grade: "TOPOLOGY_OK",
    fail_reasons: ["LAYOUT", "LABEL_POSITION", "SPACING"],
    tier_guess: "C",
    notes: "专用 ring；非 Schematex UML；版式仍非 TEXTBOOK_OK",
  };
}

function gradeWave(renderOk, id) {
  if (!renderOk) return { grade: "PARSE_OK", fail_reasons: ["LAYOUT"], tier_guess: "C", notes: "渲染失败" };
  const approx = id === "W03";
  return {
    grade: approx ? "RENDER_OK" : "TOPOLOGY_OK",
    fail_reasons: approx ? ["UNSUPPORTED", "LAYOUT"] : ["LAYOUT", "SPACING", "LABEL_POSITION"],
    tier_guess: "C",
    notes: approx ? "原图无波形，IR 示意" : "教材风 timing；非 TEXTBOOK_OK",
  };
}

function runOne(id) {
  const irRaw = IRS[id];
  if (!irRaw) return { id, skipped: true };

  const dir = path.join(CARDS, id);
  fs.mkdirSync(dir, { recursive: true });

  const { _placeholder, _tier, ...ir } = irRaw;
  fs.writeFileSync(path.join(dir, "ir.json"), JSON.stringify(ir, null, 2), "utf8");

  let dsl = "";
  let renderOk = false;
  let err = null;
  let engine = null;
  let g;

  try {
    if (ir.diagram_type === "logic") {
      engine = "schematex";
      dsl = logicIrToSchematex(ir);
      fs.writeFileSync(path.join(dir, "from_ir.stx"), dsl, "utf8");
      const svg = render(dsl);
      if (typeof svg === "string" && svg.includes("<svg")) {
        fs.writeFileSync(path.join(dir, "gen.svg"), svg, "utf8");
        renderOk = true;
      } else err = "not svg";
      g = gradeLogic(id, renderOk, irRaw);
    } else if (ir.diagram_type === "state") {
      engine = "svg_state_ring";
      const svg = stateIrToSvg(ir);
      fs.writeFileSync(path.join(dir, "gen.svg"), svg, "utf8");
      dsl = null;
      renderOk = true;
      g = gradeState(true);
    } else if (ir.diagram_type === "waveform") {
      engine = "svg_timing_textbook";
      const svg = waveIrToSvg(ir);
      fs.writeFileSync(path.join(dir, "gen.svg"), svg, "utf8");
      dsl = null;
      renderOk = true;
      g = gradeWave(true, id);
    } else {
      err = `unknown type ${ir.diagram_type}`;
      g = { grade: null, fail_reasons: ["UNSUPPORTED"], tier_guess: "C", notes: err };
    }
  } catch (e) {
    err = String(e.message || e);
    if (ir.diagram_type === "logic") g = gradeLogic(id, false, irRaw);
    else if (ir.diagram_type === "state") g = gradeState(false);
    else g = gradeWave(false, id);
  }

  const cardPath = path.join(dir, "card.json");
  const card = JSON.parse(fs.readFileSync(cardPath, "utf8"));
  Object.assign(card, {
    ir: "ir.json",
    dsl: dsl ? "from_ir.stx" : null,
    render_engine: engine,
    grade: g.grade,
    fail_reasons: g.fail_reasons,
    tier_guess: g.tier_guess,
    reviewer: "batch_full_v1",
    reviewed_at: new Date().toISOString(),
    notes: [ir.notes, g.notes, err ? `error:${err}` : ""].filter(Boolean).join(" | "),
  });
  fs.writeFileSync(cardPath, JSON.stringify(card, null, 2), "utf8");

  return { id, type: ir.diagram_type, renderOk, grade: g.grade, tier_guess: g.tier_guess, err };
}

function main() {
  const ids = Object.keys(IRS);
  const results = ids.map(runOne);
  const summary = {
    ran_at: new Date().toISOString(),
    total: results.length,
    render_ok: results.filter((r) => r.renderOk).length,
    textbook_ok: results.filter((r) => r.grade === "TEXTBOOK_OK").length,
    results,
    by_grade: {},
    by_type: {},
  };
  for (const r of results) {
    const k = r.grade || "null";
    summary.by_grade[k] = (summary.by_grade[k] || 0) + 1;
    const t = r.type || "?";
    if (!summary.by_type[t]) summary.by_type[t] = { n: 0, ok: 0 };
    summary.by_type[t].n++;
    if (r.renderOk) summary.by_type[t].ok++;
  }
  fs.writeFileSync(
    path.join(ROOT, "gold", "level1", "RUN_REPORT.json"),
    JSON.stringify(summary, null, 2),
    "utf8"
  );

  const blocks = results
    .filter((r) => !r.skipped)
    .map((r) => {
      const card = JSON.parse(fs.readFileSync(path.join(CARDS, r.id, "card.json"), "utf8"));
      const imgRel = card.image.replace("../../textbook_figures/", "");
      const img = path.join(ROOT, "textbook_figures", imgRel);
      const relRef = path.relative(path.join(ROOT, "gold", "level1"), img).replace(/\\/g, "/");
      const gen = fs.existsSync(path.join(CARDS, r.id, "gen.svg")) ? `cards/${r.id}/gen.svg` : "";
      const eng = card.render_engine || "";
      return `<section class="card" id="${r.id}">
  <h2>${r.id} · 图${card.fig_id} · <span class="g">${r.grade}</span> · tier=${r.tier_guess} · ${eng}</h2>
  <p>${card.caption || ""} · ${card.notes || ""}</p>
  <div class="cols">
    <figure><figcaption>课本</figcaption><img src="${relRef}" onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'err',textContent:'missing'}))"/></figure>
    <figure><figcaption>生成</figcaption>${
      gen ? `<img src="${gen}"/>` : `<div class="err">${r.err || "no svg"}</div>`
    }</figure>
  </div>
</section>`;
    });

  const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>
<title>Level-1 Full Batch (50)</title>
<style>
body{font-family:Microsoft YaHei,sans-serif;background:#f1f5f9;margin:0;padding:20px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px;margin:14px auto;max-width:1100px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px}
img{max-width:100%;background:#fff}
.g{color:#b45309}.err{color:#dc2626;padding:20px}
.banner{max-width:1100px;margin:0 auto 12px;padding:10px 14px;background:#fff7ed;border:1px solid #fdba74;border-radius:8px}
.nav{max-width:1100px;margin:0 auto 12px;display:flex;flex-wrap:wrap;gap:6px}
.nav a{font-size:12px;padding:2px 8px;background:#e2e8f0;border-radius:4px;text-decoration:none;color:#334155}
</style></head><body>
<h1>Level-1 全量 ${summary.total} 张</h1>
<div class="banner">render_ok=${summary.render_ok}/${summary.total} · TEXTBOOK_OK=${summary.textbook_ok} ·
grades=${JSON.stringify(summary.by_grade)} · types=${JSON.stringify(summary.by_type)}</div>
<nav class="nav">${results.map((r) => `<a href="#${r.id}">${r.id}</a>`).join("")}</nav>
${blocks.join("\n")}
</body></html>`;
  fs.writeFileSync(path.join(ROOT, "gold", "level1", "run_gallery.html"), html, "utf8");
  console.log(JSON.stringify({ ...summary, results: undefined }, null, 2));
  const fails = results.filter((r) => !r.renderOk);
  if (fails.length) {
    console.log("FAILS:");
    for (const f of fails) console.log(f.id, f.err);
  }
  console.log("gallery → gold/level1/run_gallery.html");
}

main();
