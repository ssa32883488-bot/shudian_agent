/**
 * 从 schematex_workbench 迁移 logic 卡 → 仿真 + netlistsvg 出图 + 自检
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
import sharp from "sharp";
import { logicIrToYosysJson } from "../lib/ir_to_yosys_json.mjs";
import { classifyIr, sampleTruth } from "../lib/sim_logic_ir.mjs";
import { selfCheck, summarizeChecks } from "../lib/self_check.mjs";

const require = createRequire(import.meta.url);
const netlistsvg = require("netlistsvg");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OLD = path.resolve(ROOT, "..", "schematex_workbench", "gold", "level1");
const OUT = path.join(ROOT, "gold", "level1");
const SKIN = path.join(ROOT, "skins", "textbook.svg");

/** 同函数对偶卡：自检 PEER_EQ */
const PEERS = {
  C01: { peer: "C02", label: "C02" },
  C02: { peer: "C01", label: "C01" },
};

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function renderYosys(yosysJson) {
  const skin = fs.readFileSync(SKIN, "utf8");
  return new Promise((resolve, reject) => {
    netlistsvg.render(skin, yosysJson, (err, svg) => {
      if (err) reject(err);
      else resolve(svg);
    });
  });
}

function prepareSvgForRaster(svg) {
  if (/<rect[^>]*id="__bg__"/.test(svg)) return svg;
  return svg.replace(
    /<svg([^>]*)>/,
    `<svg$1><rect id="__bg__" width="100%" height="100%" fill="#ffffff" stroke="none"/>`
  );
}

async function svgToPng(svg, pngPath) {
  const prepared = prepareSvgForRaster(svg);
  await sharp(Buffer.from(prepared), { density: 192 })
    .flatten({ background: "#ffffff" })
    .png()
    .toFile(pngPath);
}

const INCLUDE = new Set([
  "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10",
  "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10",
  "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10",
]);

const irCache = new Map();

async function processCard(id) {
  const srcDir = path.join(OLD, "cards", id);
  const irPath = path.join(srcDir, "ir.json");
  const cardPath = path.join(srcDir, "card.json");
  if (!fs.existsSync(irPath) || !fs.existsSync(cardPath)) return null;

  const ir = readJson(irPath);
  const card = readJson(cardPath);
  if (ir.diagram_type && ir.diagram_type !== "logic") return null;
  irCache.set(id, ir);

  const dst = path.join(OUT, "cards", id);
  const stxCardDir = path.join(OLD, "cards", id);
  fs.mkdirSync(dst, { recursive: true });
  fs.writeFileSync(path.join(dst, "ir.json"), JSON.stringify(ir, null, 2));

  const figRel = card.image || null;
  const cls = classifyIr(ir);
  const sim = sampleTruth(ir, 8);

  let yosysBundle = null;
  let svg = null;
  let renderErr = null;
  try {
    yosysBundle = logicIrToYosysJson(ir, id);
    fs.writeFileSync(path.join(dst, "yosys.json"), JSON.stringify(yosysBundle.json, null, 2));
    fs.writeFileSync(path.join(dst, "yosys_meta.json"), JSON.stringify(yosysBundle.meta, null, 2));
    svg = await renderYosys(yosysBundle.json);
    fs.writeFileSync(path.join(dst, "gen_netlist.svg"), svg);
    fs.writeFileSync(path.join(stxCardDir, "gen.svg"), svg);
    fs.writeFileSync(path.join(stxCardDir, "gen_netlist.svg"), svg);
    const pngPath = path.join(OUT, "shots", `${id}.png`);
    fs.mkdirSync(path.dirname(pngPath), { recursive: true });
    await svgToPng(svg, pngPath);
  } catch (e) {
    renderErr = e.message || String(e);
  }

  fs.writeFileSync(
    path.join(dst, "card.json"),
    JSON.stringify(
      {
        ...card,
        render_engine: "netlistsvg",
        engine: "netlist_workbench_v2",
        grade: renderErr ? card.grade : "TEXTBOOK_OK",
        notes: "logic_ir_v1 → 仿真 → yosys JSON → netlistsvg 自动布线（主路径）",
      },
      null,
      2
    )
  );

  const stxCardPath = path.join(stxCardDir, "card.json");
  if (fs.existsSync(stxCardPath)) {
    const stxCard = readJson(stxCardPath);
    fs.writeFileSync(
      stxCardPath,
      JSON.stringify(
        {
          ...stxCard,
          render_engine: "netlistsvg",
          dsl: null,
          notes: svg
            ? "主路径 netlistsvg；gold.tbx 已弃用"
            : `netlistsvg 跳过: ${renderErr || "unknown"}`,
          reviewed_at: new Date().toISOString(),
        },
        null,
        2
      )
    );
  }

  const peerCfg = PEERS[id];
  let peerIr = null;
  if (peerCfg) {
    const peerPath = path.join(OLD, "cards", peerCfg.peer, "ir.json");
    if (fs.existsSync(peerPath)) peerIr = readJson(peerPath);
  }

  const self = selfCheck(ir, {
    svg: svg || undefined,
    yosysMeta: yosysBundle?.meta,
    peerIr: peerIr || undefined,
    peerLabel: peerCfg?.label,
  });
  fs.writeFileSync(path.join(dst, "self_check.json"), JSON.stringify(self, null, 2));

  const report = {
    id,
    fig_id: card.fig_id,
    caption: card.caption,
    image: figRel,
    combinational: cls.combinational,
    sim_ok: !!sim.ok,
    sim_reason: sim.reason,
    sim_rows: sim.total ?? sim.rows?.length ?? 0,
    sim_samples: sim.samples || [],
    render_ok: !renderErr && !!svg,
    render_error: renderErr,
    self_ok: self.ok,
    self_grade: self.grade,
    self_checks: self.checks,
    multi_gates: yosysBundle?.meta?.multiGates ?? 0,
    fallback_splits: yosysBundle?.meta?.fallbackSplits?.length ?? 0,
    notes: ir.notes || "",
  };
  fs.writeFileSync(path.join(dst, "report.json"), JSON.stringify(report, null, 2));
  return report;
}

async function main() {
  fs.mkdirSync(path.join(OUT, "cards"), { recursive: true });
  fs.mkdirSync(path.join(OUT, "shots"), { recursive: true });
  const reports = [];
  for (const id of [...INCLUDE].sort()) {
    try {
      const r = await processCard(id);
      if (r) {
        reports.push(r);
        console.log(
          r.id,
          r.sim_ok ? "SIM_OK" : `SIM_${r.sim_reason}`,
          r.render_ok ? "RENDER_OK" : `RENDER_FAIL:${r.render_error}`,
          r.self_ok ? "SELF_OK" : "SELF_FAIL",
          `multi=${r.multi_gates}`,
          r.fallback_splits ? `fallback=${r.fallback_splits}` : "",
          summarizeChecks({ checks: r.self_checks })
        );
      }
    } catch (e) {
      console.log(id, "FAIL", e.message);
      reports.push({ id, fatal: e.message });
    }
  }
  fs.writeFileSync(path.join(OUT, "BATCH_REPORT.json"), JSON.stringify(reports, null, 2));
  const nSelf = reports.filter((r) => r.self_ok).length;
  console.log("done", reports.length, `SELF_OK ${nSelf}/${reports.length}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
