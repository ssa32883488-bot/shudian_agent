/**
 * 批量跑 Level-1 logic 卡：写 IR → DSL → Schematex SVG → 更新 card.json
 */
import fs from "fs";
import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";
import { logicIrToSchematex } from "../adapters/logic_ir_to_schematex.mjs";

const require = createRequire(import.meta.url);
const { render } = require("schematex");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const CARDS = path.join(ROOT, "gold", "level1", "cards");

/** 人工/识图得到的 IR；三输入拆成两级 */
const IRS = {
  L01: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "referee",
    inputs: ["A", "B", "C"],
    gates: {
      G1: { type: "OR", inputs: ["B", "C"] },
      G2: { type: "AND", inputs: ["A", "G1"] },
    },
    outputs: { Y: "G2" },
    notes: "Y=A*(B+C)",
  },
  L02: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "ex_2_5_3",
    inputs: ["A", "B", "C"],
    gates: {
      nB: { type: "NOT", inputs: ["B"] },
      t_bc: { type: "AND", inputs: ["nB", "C"] },
      t_sum: { type: "OR", inputs: ["A", "t_bc"] },
      t_nand: { type: "NOT", inputs: ["t_sum"] },
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      t_ab: { type: "AND", inputs: ["nA", "B"] },
      t_abc: { type: "AND", inputs: ["t_ab", "nC"] },
      t_or: { type: "OR", inputs: ["t_nand", "t_abc"] },
      Y: { type: "OR", inputs: ["t_or", "C"] },
    },
    outputs: { Y: "Y" },
    notes: "Y=(A+B'C)'+A'BC'+C",
  },
  L03: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "xor_nor",
    inputs: ["A", "B"],
    gates: {
      G1: { type: "NOR", inputs: ["A", "B"] },
      nA: { type: "NOT", inputs: ["A"] },
      nB: { type: "NOT", inputs: ["B"] },
      G2: { type: "NOR", inputs: ["nA", "nB"] },
      Y: { type: "NOR", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
    notes: "异或 NOR 展开；教材版式建议 C/B",
  },
  L04: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "pla_y123_a",
    inputs: ["A", "B", "C", "D"],
    gates: {
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      nD: { type: "NOT", inputs: ["D"] },
      nB: { type: "NOT", inputs: ["B"] },
      a1: { type: "AND", inputs: ["A", "C"] },
      t_acd: { type: "AND", inputs: ["nA", "nC"] },
      a2: { type: "AND", inputs: ["t_acd", "D"] },
      y1a: { type: "OR", inputs: ["B", "a1"] },
      Y1: { type: "OR", inputs: ["y1a", "a2"] },
      a3: { type: "AND", inputs: ["nA", "D"] },
      a4: { type: "AND", inputs: ["B", "nD"] },
      Y2: { type: "OR", inputs: ["a3", "a4"] },
      a5: { type: "AND", inputs: ["nA", "C"] },
      t_abc: { type: "AND", inputs: ["A", "nB"] },
      a6: { type: "AND", inputs: ["t_abc", "nC"] },
      Y3: { type: "OR", inputs: ["a5", "a6"] },
    },
    outputs: { Y1: "Y1", Y2: "Y2", Y3: "Y3" },
    notes: "PLA 总线型；版式难 TEXTBOOK_OK",
  },
  L05: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "pla_y123_b",
    inputs: ["A", "B", "C", "D"],
    gates: {
      nA: { type: "NOT", inputs: ["A"] },
      nB: { type: "NOT", inputs: ["B"] },
      nC: { type: "NOT", inputs: ["C"] },
      nD: { type: "NOT", inputs: ["D"] },
      g1a: { type: "AND", inputs: ["nA", "nC"] },
      G1: { type: "AND", inputs: ["g1a", "D"] },
      G2: { type: "AND", inputs: ["B", "nD"] },
      g3a: { type: "AND", inputs: ["A", "nB"] },
      G3: { type: "AND", inputs: ["g3a", "C"] },
      g4a: { type: "AND", inputs: ["nA", "C"] },
      G4: { type: "AND", inputs: ["g4a", "D"] },
      Y1: { type: "OR", inputs: ["B", "G1"] },
      y2a: { type: "OR", inputs: ["G1", "G2"] },
      Y2: { type: "OR", inputs: ["y2a", "G4"] },
      y3a: { type: "OR", inputs: ["G2", "G3"] },
      Y3: { type: "OR", inputs: ["y3a", "G4"] },
    },
    outputs: { Y1: "Y1", Y2: "Y2", Y3: "Y3" },
    notes: "PLA 共享乘积项",
  },
  L06: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "nand_net_2_9_2",
    inputs: ["A", "B", "C"],
    gates: {
      nB: { type: "NOT", inputs: ["B"] },
      nA: { type: "NOT", inputs: ["A"] },
      nC: { type: "NOT", inputs: ["C"] },
      G1: { type: "NAND", inputs: ["A", "nB"] },
      G2: { type: "NAND", inputs: ["nA", "B"] },
      G3: { type: "NOT", inputs: ["G1"] },
      G4: { type: "NOT", inputs: ["G2"] },
      G5: { type: "NAND", inputs: ["G3", "nC"] },
      G6: { type: "NAND", inputs: ["nC", "G4"] },
      Y: { type: "NAND", inputs: ["G5", "G6"] },
    },
    outputs: { Y: "Y" },
    notes: "全 NAND 网；G3/G4 课本为双输入短接 NAND≈NOT",
  },
  L07: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "xor_and_2_9_3",
    inputs: ["A", "B", "Cn"],
    gates: {
      t1: { type: "XOR", inputs: ["A", "B"] },
      Y: { type: "AND", inputs: ["t1", "Cn"] },
    },
    outputs: { Y: "Y" },
    notes: "Cn 表示 C'；Y=(A⊕B)·C'",
  },
  L08: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "nand_aoi_2_9_4",
    inputs: ["A", "C", "B", "Cn"],
    gates: {
      G1: { type: "NAND", inputs: ["A", "C"] },
      G2: { type: "NAND", inputs: ["B", "Cn"] },
      Y: { type: "NAND", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
    notes: "Cn=C'；Y=((A·C)'·(B·C')')'=AC+BC'",
  },
  L09: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "nor_aoi_2_9_5",
    inputs: ["B", "C", "A", "Cn"],
    gates: {
      G1: { type: "NOR", inputs: ["B", "C"] },
      G2: { type: "NOR", inputs: ["A", "Cn"] },
      Y: { type: "NOR", inputs: ["G1", "G2"] },
    },
    outputs: { Y: "Y" },
    notes: "Cn=C'；Y=((B+C)'+(A+C')')'=(B+C)(A+C')",
  },
  L10: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "full_adder_4_1_1",
    inputs: ["A", "B", "CI"],
    gates: {
      s1: { type: "XOR", inputs: ["A", "B"] },
      S: { type: "XOR", inputs: ["s1", "CI"] },
      c1: { type: "AND", inputs: ["A", "B"] },
      c2: { type: "AND", inputs: ["s1", "CI"] },
      nor1: { type: "NOR", inputs: ["c1", "c2"] },
      CO: { type: "NOT", inputs: ["nor1"] },
    },
    outputs: { S: "S", CO: "CO" },
    notes: "课本用 NOR+NOT 实现进位或",
  },
  C05: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "mux2_1",
    inputs: ["A", "SEL", "B"],
    gates: {
      G1: { type: "AND", inputs: ["A", "SEL"] },
      G2: { type: "NOT", inputs: ["SEL"] },
      G3: { type: "AND", inputs: ["G2", "B"] },
      Y: { type: "OR", inputs: ["G1", "G3"] },
    },
    outputs: { Y: "Y" },
    notes: "Y=A·SEL+B·SEL'",
  },
  C06: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "half_adder",
    inputs: ["A", "B"],
    gates: {
      S: { type: "XOR", inputs: ["A", "B"] },
      CO: { type: "AND", inputs: ["A", "B"] },
    },
    outputs: { S: "S", CO: "CO" },
  },
  C07: {
    schema_version: "logic_ir_v1",
    diagram_type: "logic",
    style: "iec",
    title: "full_adder",
    inputs: ["CI", "A", "B"],
    gates: {
      XOR1: { type: "XOR", inputs: ["A", "B"] },
      Sum: { type: "XOR", inputs: ["CI", "XOR1"] },
      AND1: { type: "AND", inputs: ["A", "B"] },
      AND2: { type: "AND", inputs: ["B", "CI"] },
      AND3: { type: "AND", inputs: ["A", "CI"] },
      t1: { type: "OR", inputs: ["AND1", "AND2"] },
      Cout: { type: "OR", inputs: ["t1", "AND3"] },
    },
    outputs: { Sum: "Sum", Cout: "Cout" },
    notes: "三与一或全加；扇出多",
  },
};

function gradeFor(id, renderOk, placeholder) {
  if (placeholder) {
    return {
      grade: renderOk ? "RENDER_OK" : null,
      fail_reasons: ["UNSUPPORTED"],
      tier_guess: "B",
      notes: "IR 占位未精标",
    };
  }
  // 经验：简单少扇出 → TOPOLOGY_OK；PLA/复杂扇出 → TOPOLOGY_OK + LAYOUT/FANOUT
  const simple = ["L01", "L07", "L08", "L09", "C05", "C06"];
  const xorExpand = ["L03"];
  const pla = ["L04", "L05"];
  const heavy = ["L02", "L06", "L10", "C07"];

  if (!renderOk) {
    return { grade: "PARSE_OK", fail_reasons: ["LAYOUT"], tier_guess: "B", notes: "渲染失败" };
  }
  if (simple.includes(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["JUNCTION_MISSING", "CROSSING", "SYMBOL_STYLE"],
      tier_guess: ["L01", "L07", "L08", "L09", "C05", "C06"].includes(id) ? "A" : "B",
      notes: "拓扑可对；Schematex 走线/结点未达 TEXTBOOK_OK；符号为 iec 非课本 ansi",
    };
  }
  if (xorExpand.includes(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["FANOUT_ERROR", "JUNCTION_MISSING", "LAYOUT", "SYMBOL_STYLE"],
      tier_guess: "C",
      notes: "语义可；教材异或展开建议专用/后处理",
    };
  }
  if (pla.includes(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["LAYOUT", "FANOUT_ERROR", "JUNCTION_MISSING", "SPACING"],
      tier_guess: "B",
      notes: "PLA 总线版式 Schematex 达不到 TEXTBOOK_OK",
    };
  }
  if (heavy.includes(id)) {
    return {
      grade: "TOPOLOGY_OK",
      fail_reasons: ["FANOUT_ERROR", "JUNCTION_MISSING", "CROSSING", "LAYOUT", "SYMBOL_STYLE"],
      tier_guess: "B",
      notes: "拓扑大致正确；复杂扇出 → B",
    };
  }
  return {
    grade: "RENDER_OK",
    fail_reasons: ["LAYOUT"],
    tier_guess: "B",
    notes: "",
  };
}

function runOne(id) {
  const ir = IRS[id];
  if (!ir) return { id, skipped: true };

  const dir = path.join(CARDS, id);
  fs.mkdirSync(dir, { recursive: true });

  const { _placeholder, ...irClean } = ir;
  fs.writeFileSync(path.join(dir, "ir.json"), JSON.stringify(irClean, null, 2), "utf8");

  let dsl = "";
  let renderOk = false;
  let err = null;
  try {
    dsl = logicIrToSchematex(irClean);
    fs.writeFileSync(path.join(dir, "from_ir.stx"), dsl, "utf8");
    const svg = render(dsl);
    if (typeof svg === "string" && svg.includes("<svg")) {
      fs.writeFileSync(path.join(dir, "gen.svg"), svg, "utf8");
      renderOk = true;
    } else {
      err = "not svg";
    }
  } catch (e) {
    err = String(e.message || e);
  }

  const g = gradeFor(id, renderOk, !!_placeholder);
  const cardPath = path.join(dir, "card.json");
  const card = JSON.parse(fs.readFileSync(cardPath, "utf8"));
  Object.assign(card, {
    ir: `ir.json`,
    dsl: renderOk || dsl ? "from_ir.stx" : null,
    render_engine: "schematex",
    grade: g.grade,
    fail_reasons: g.fail_reasons,
    tier_guess: g.tier_guess,
    reviewer: "batch_run_v1",
    reviewed_at: new Date().toISOString(),
    notes: [ir.notes, g.notes, err ? `error:${err}` : ""].filter(Boolean).join(" | "),
  });
  fs.writeFileSync(cardPath, JSON.stringify(card, null, 2), "utf8");

  return { id, renderOk, grade: g.grade, tier_guess: g.tier_guess, err };
}

function main() {
  const ids = Object.keys(IRS);
  const results = ids.map(runOne);
  const summary = {
    ran_at: new Date().toISOString(),
    results,
    by_grade: {},
  };
  for (const r of results) {
    const k = r.grade || "null";
    summary.by_grade[k] = (summary.by_grade[k] || 0) + 1;
  }
  fs.writeFileSync(
    path.join(ROOT, "gold", "level1", "RUN_REPORT.json"),
    JSON.stringify(summary, null, 2),
    "utf8"
  );

  // HTML 画廊
  const blocks = results
    .filter((r) => !r.skipped)
    .map((r) => {
      const card = JSON.parse(fs.readFileSync(path.join(CARDS, r.id, "card.json"), "utf8"));
      const img = path.join(ROOT, "textbook_figures", card.image.replace("../../textbook_figures/", ""));
      const relRef = path.relative(path.join(ROOT, "gold", "level1"), img).replace(/\\/g, "/");
      const gen = fs.existsSync(path.join(CARDS, r.id, "gen.svg"))
        ? `cards/${r.id}/gen.svg`
        : "";
      return `<section class="card">
  <h2>${r.id} · 图${card.fig_id} · <span class="g">${r.grade}</span> · tier=${r.tier_guess}</h2>
  <p>${card.caption || ""} · ${card.notes || ""}</p>
  <div class="cols">
    <figure><figcaption>课本</figcaption><img src="${relRef}"/></figure>
    <figure><figcaption>IR→Schematex(iec)</figcaption>${
      gen ? `<img src="${gen}"/>` : `<div class="err">${r.err || "no svg"}</div>`
    }</figure>
  </div>
</section>`;
    });

  const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>
<title>Level-1 Batch Run</title>
<style>
body{font-family:Microsoft YaHei,sans-serif;background:#f1f5f9;margin:0;padding:20px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:14px;margin:14px auto;max-width:1100px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px}
img{max-width:100%;background:#fff}
.g{color:#b45309}.err{color:#dc2626;padding:20px}
.banner{max-width:1100px;margin:0 auto 12px;padding:10px 14px;background:#fff7ed;border:1px solid #fdba74;border-radius:8px}
</style></head><body>
<h1>Level-1 批量跑通</h1>
<div class="banner">无 TEXTBOOK_OK：Schematex 自动布局+缺结点；本轮最高 TOPOLOGY_OK。成功标准按 ARCHITECTURE.md。</div>
${blocks.join("\n")}
</body></html>`;
  fs.writeFileSync(path.join(ROOT, "gold", "level1", "run_gallery.html"), html, "utf8");
  console.log(JSON.stringify(summary, null, 2));
  console.log("gallery → gold/level1/run_gallery.html");
}

main();
