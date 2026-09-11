/**
 * 冻结状态图 S01–S10 验收快照：重生 SVG/TikZ、写入 acceptance.json、更新 card 元数据
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { stateIrToSvg, selfCheckStateSvg, computeStateLayout } from "../adapters/state_ir_to_svg.mjs";
import { stateIrToTikz } from "../adapters/state_ir_to_tikz.mjs";
import { tikzToSvg } from "../adapters/state_tikz_render.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CARDS = path.join(ROOT, "gold", "level1", "cards");
const OUT = path.join(ROOT, "gold", "level1", "state_opt");
const ACCEPTED_AT = "2026-09-02T12:00:00+08:00";

const CARD_NOTES = {
  S01: "positions 金标；阎石 6.2.2 两排跑道",
  S02: "square 布局；双向眼形双弧（8 线）",
  S03: "positions 金标；16 态类矩形+分支",
  S04: "square/ring 自动；Moore 型状态图",
  S05: "racetrack 启发式",
  S06: "square 布局；S0↔S1 双弧",
  S07: "triangle 布局；三态化简",
  S08: "triangle 布局；多入边错开",
  S09: "racetrack/ring；循环计数",
  S10: "positions 金标；虚线/叉号/文字图例 Q1Q2Q3",
};

function readJson(p) {
  let t = fs.readFileSync(p, "utf8");
  if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
  return JSON.parse(t);
}

function writeJson(p, obj) {
  fs.writeFileSync(p, `${JSON.stringify(obj, null, 2)}\n`, "utf8");
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const ids = fs.readdirSync(CARDS).filter((d) => /^S\d+$/.test(d)).sort();
  const entries = [];

  for (const id of ids) {
    const dir = path.join(CARDS, id);
    const ir = readJson(path.join(dir, "ir.json"));
    const card = readJson(path.join(dir, "card.json"));
    if (ir.diagram_type !== "state") continue;

    const layout = computeStateLayout(ir);
    const svg = stateIrToSvg(ir);
    const check = selfCheckStateSvg(ir, svg);
    fs.writeFileSync(path.join(dir, "gen.svg"), svg, "utf8");
    fs.writeFileSync(path.join(dir, "gen_tbx.svg"), svg, "utf8");
    writeJson(path.join(dir, "state_self_check.json"), check);

    let tikzOk = false;
    try {
      const tex = stateIrToTikz(ir);
      fs.writeFileSync(path.join(dir, "gen.tikz.tex"), tex, "utf8");
      const svgTikz = await tikzToSvg(tex);
      fs.writeFileSync(path.join(dir, "gen_tikz.svg"), svgTikz, "utf8");
      tikzOk = true;
    } catch (e) {
      console.warn(id, "tikz", e.message?.split("\n")[0]);
    }

    const hasPos = !!(ir.positions && Object.keys(ir.positions).length >= (ir.states?.length || 0));
    writeJson(path.join(dir, "card.json"), {
      ...card,
      render_engine: "state_ir_v1_svg+tikz",
      grade: "TEXTBOOK_OK",
      fail_reasons: [],
      reviewer: "user_accepted",
      reviewed_at: ACCEPTED_AT,
      notes: CARD_NOTES[id] || `layout=${layout.mode}`,
    });

    entries.push({
      id,
      fig_id: card.fig_id,
      caption: card.caption,
      layout_mode: layout.mode,
      has_positions: hasPos,
      ir_layout: ir.layout || "auto",
      states: ir.states?.length,
      transitions: ir.transitions?.length,
      struct_ok: check.ok,
      tikz_ok: tikzOk,
      outputs: {
        svg: `../cards/${id}/gen.svg`,
        tikz_tex: `../cards/${id}/gen.tikz.tex`,
        tikz_svg: tikzOk ? `../cards/${id}/gen_tikz.svg` : null,
      },
    });
    console.log(id, "FROZEN", layout.mode, check.ok ? "STRUCT_OK" : "FAIL", tikzOk ? "TIKZ_OK" : "");
  }

  const acceptance = {
    schema_version: "state_acceptance_v1",
    accepted_at: ACCEPTED_AT,
    reviewer: "user",
    textbook: "阎石《数字电子技术基础》状态转换图 S01–S10",
    pipeline: {
      ir: "state_ir_v1",
      layout: ["free(positions)", "square", "triangle", "racetrack", "ring"],
      renderers: ["adapters/state_ir_to_svg.mjs", "adapters/state_ir_to_tikz.mjs + node-tikzjax"],
      edge_routing: "lib/state_edge_route.mjs（双向眼形双弧 / 虚线 / 叉号）",
      rejected: ["Graphviz 自动布局作为主路径"],
    },
    galleries: {
      textbook: "review_textbook.html",
      tikz: "review_tikz.html",
      index: "index.html",
    },
    rebuild: {
      all: "npm run rebuild-state-accepted",
      textbook: "npm run rebuild-state-textbook",
      tikz: "npm run rebuild-state-tikz",
      freeze: "npm run freeze-state-acceptance",
    },
    cards: entries,
  };

  writeJson(path.join(OUT, "acceptance.json"), acceptance);
  console.log("wrote", path.join(OUT, "acceptance.json"));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
