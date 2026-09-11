/**
 * 生成 Level-1 50 张金标空卡（card.json + 链到 textbook_figures 图片）
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const GOLD = path.join(ROOT, "gold", "level1");

/** @type {{id:string,bucket:string,fig_id:string,caption:string,file:string,tier_guess:string,ir_schema:string}[]} */
const SELECTED = [
  // —— 基本/简单逻辑 10 ——
  { id: "L01", bucket: "basic_gates", fig_id: "2.5.2", caption: "举重裁判逻辑图 Y=A·(B+C)", file: "logic_dag/fig_2_5_2.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "L02", bucket: "basic_gates", fig_id: "2.5.4", caption: "例2.5.3的逻辑图", file: "logic_dag/fig_2_5_4.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "L03", bucket: "basic_gates", fig_id: "2.5.5", caption: "例2.5.4的逻辑图（异或展开）", file: "logic_dag/fig_2_5_5.jpg", tier_guess: "C", ir_schema: "logic_ir_v1" },
  { id: "L04", bucket: "basic_gates", fig_id: "2.8.2", caption: "根据式(2.8.2)的逻辑电路图", file: "logic_dag/fig_2_8_2.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "L05", bucket: "basic_gates", fig_id: "2.8.4", caption: "根据式(2.8.3)的逻辑电路图", file: "logic_dag/fig_2_8_4.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "L06", bucket: "basic_gates", fig_id: "2.9.2", caption: "按式(2.9.2)接成的逻辑电路", file: "logic_dag/fig_2_9_2.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "L07", bucket: "basic_gates", fig_id: "2.9.3", caption: "按式(2.9.3)接成的逻辑电路", file: "logic_dag/fig_2_9_3.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "L08", bucket: "basic_gates", fig_id: "2.9.4", caption: "按式(2.9.5)接成的逻辑电路", file: "logic_dag/fig_2_9_4.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "L09", bucket: "basic_gates", fig_id: "2.9.5", caption: "按式(2.9.6)接成的逻辑电路", file: "logic_dag/fig_2_9_5.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "L10", bucket: "basic_gates", fig_id: "4.1.1", caption: "组合逻辑电路实例", file: "logic_dag/fig_4_1_1.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },

  // —— 组合逻辑 10 ——
  { id: "C01", bucket: "combinational", fig_id: "4.3.3", caption: "例4.3.1逻辑图之一", file: "logic_dag/fig_4_3_3.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C02", bucket: "combinational", fig_id: "4.3.4", caption: "例4.3.1逻辑图之二（与非）", file: "logic_dag/fig_4_3_4.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C03", bucket: "combinational", fig_id: "4.3.6", caption: "例4.3.1逻辑图之三", file: "logic_dag/fig_4_3_6.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C04", bucket: "combinational", fig_id: "4.4.2", caption: "3位二进制编码器", file: "logic_dag/fig_4_4_2.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C05", bucket: "combinational", fig_id: "4.4.19", caption: "二选一数据选择器", file: "logic_dag/fig_4_4_19.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "C06", bucket: "combinational", fig_id: "4.4.21", caption: "半加器", file: "logic_dag/fig_4_4_21.jpg", tier_guess: "A", ir_schema: "logic_ir_v1" },
  { id: "C07", bucket: "combinational", fig_id: "4.7.4", caption: "1位全加器电路", file: "logic_dag/fig_4_7_4.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C08", bucket: "combinational", fig_id: "4.4.7", caption: "3线-8线译码器74HC138", file: "logic_dag/fig_4_4_7.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C09", bucket: "combinational", fig_id: "4.4.9", caption: "二-十进制译码器74HC42", file: "logic_dag/fig_4_4_9.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "C10", bucket: "combinational", fig_id: "4.4.20", caption: "双4选1数据选择器74HC153", file: "logic_dag/fig_4_4_20.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },

  // —— 触发器/时序结构 10 ——
  { id: "F01", bucket: "flipflop_seq", fig_id: "5.2.1", caption: "或非门组成的锁存器", file: "logic_dag/fig_5_2_1.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F02", bucket: "flipflop_seq", fig_id: "5.2.2", caption: "与非门组成的SR锁存器", file: "logic_dag/fig_5_2_2.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F03", bucket: "flipflop_seq", fig_id: "5.3.1", caption: "电平触发SR触发器", file: "logic_dag/fig_5_3_1.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F04", bucket: "flipflop_seq", fig_id: "5.3.4", caption: "电平触发D触发器", file: "logic_dag/fig_5_3_4.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F05", bucket: "flipflop_seq", fig_id: "5.3.7", caption: "两电平D组成边沿触发器", file: "logic_dag/fig_5_3_7.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F06", bucket: "flipflop_seq", fig_id: "6.2.1", caption: "例6.2.1时序逻辑电路", file: "logic_dag/fig_6_2_1.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F07", bucket: "flipflop_seq", fig_id: "6.2.3", caption: "例6.2.3时序逻辑电路", file: "logic_dag/fig_6_2_3.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F08", bucket: "flipflop_seq", fig_id: "6.3.1", caption: "D触发器移位寄存器", file: "logic_dag/fig_6_3_1.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F09", bucket: "flipflop_seq", fig_id: "6.3.8", caption: "同步二进制加法计数器", file: "logic_dag/fig_6_3_8_01faea9b.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },
  { id: "F10", bucket: "flipflop_seq", fig_id: "6.4.17", caption: "例6.4.3的逻辑图", file: "logic_dag/fig_6_4_17.jpg", tier_guess: "B", ir_schema: "logic_ir_v1" },

  // —— 状态图 10 ——
  { id: "S01", bucket: "state", fig_id: "6.2.2", caption: "图6.2.1电路的状态转换图", file: "state_machine/fig_6_2_2.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S02", bucket: "state", fig_id: "6.2.4", caption: "图6.2.3电路的状态转换图", file: "state_machine/fig_6_2_4.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S03", bucket: "state", fig_id: "6.2.11", caption: "图6.2.10电路的状态转换图", file: "state_machine/fig_6_2_11.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S04", bucket: "state", fig_id: "6.3.9", caption: "图6.3.8电路的状态转换图", file: "state_machine/fig_6_3_9.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S05", bucket: "state", fig_id: "6.4.2", caption: "例6.4.1的状态转换图", file: "state_machine/fig_6_4_2.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S06", bucket: "state", fig_id: "6.4.7", caption: "例6.4.2的状态转换图", file: "state_machine/fig_6_4_7.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S07", bucket: "state", fig_id: "6.4.8", caption: "化简后的例6.4.2状态转换图", file: "state_machine/fig_6_4_8.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S08", bucket: "state", fig_id: "6.4.14", caption: "例6.4.3的状态转换图", file: "state_machine/fig_6_4_14.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S09", bucket: "state", fig_id: "6.4.19", caption: "例6.4.4的状态转换图", file: "state_machine/fig_6_4_19.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },
  { id: "S10", bucket: "state", fig_id: "6.4.26", caption: "例6.4.5电路的状态转换图", file: "state_machine/fig_6_4_26.jpg", tier_guess: "C", ir_schema: "state_ir_v1" },

  // —— 波形 10 ——
  { id: "W01", bucket: "waveform", fig_id: "2.5.3", caption: "图2.5.1电路逻辑功能波形图", file: "timing_wave/fig_2_5_3.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W02", bucket: "waveform", fig_id: "2.5.6", caption: "例2.5.5的波形图", file: "timing_wave/fig_2_5_6.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W03", bucket: "waveform", fig_id: "5.2.3", caption: "例5.2.1电路和电压波形", file: "timing_wave/fig_5_2_3.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W04", bucket: "waveform", fig_id: "5.3.3", caption: "例5.3.1的电压波形图", file: "timing_wave/fig_5_3_3.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W05", bucket: "waveform", fig_id: "5.3.6", caption: "例5.3.2的电压波形", file: "timing_wave/fig_5_3_6.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W06", bucket: "waveform", fig_id: "5.3.9", caption: "例5.3.3的电压波形图", file: "timing_wave/fig_5_3_9.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W07", bucket: "waveform", fig_id: "5.3.11", caption: "例5.3.4的电压波形", file: "timing_wave/fig_5_3_11.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W08", bucket: "waveform", fig_id: "5.3.14", caption: "例5.3.5的电压波形图", file: "timing_wave/fig_5_3_14.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W09", bucket: "waveform", fig_id: "6.3.2", caption: "图6.3.1电路的电压波形", file: "timing_wave/fig_6_3_2.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
  { id: "W10", bucket: "waveform", fig_id: "6.3.7", caption: "例6.3.1电路的波形图", file: "timing_wave/fig_6_3_7.jpg", tier_guess: "C", ir_schema: "wave_ir_v1" },
];

function cardTemplate(item) {
  return {
    id: item.id,
    bucket: item.bucket,
    fig_id: item.fig_id,
    caption: item.caption,
    image: `../../textbook_figures/${item.file}`,
    image_exists: fs.existsSync(path.join(ROOT, "textbook_figures", item.file)),
    tier_guess: item.tier_guess,
    ir_schema: item.ir_schema,
    ir: null,
    dsl: null,
    render_engine: null,
    grade: null,
    fail_reasons: [],
    reviewer: null,
    reviewed_at: null,
    notes: "",
  };
}

function main() {
  fs.mkdirSync(GOLD, { recursive: true });
  const cardsDir = path.join(GOLD, "cards");
  fs.mkdirSync(cardsDir, { recursive: true });

  const rows = [];
  for (const item of SELECTED) {
    const dir = path.join(cardsDir, item.id);
    fs.mkdirSync(dir, { recursive: true });
    const card = cardTemplate(item);
    fs.writeFileSync(path.join(dir, "card.json"), JSON.stringify(card, null, 2), "utf8");
    // 空 IR 占位
    if (!fs.existsSync(path.join(dir, "ir.json"))) {
      fs.writeFileSync(
        path.join(dir, "ir.json"),
        JSON.stringify(
          {
            _todo: "人工或大模型填写；logic 见 ir/schema/logic_ir.schema.json",
            schema_version: item.ir_schema,
          },
          null,
          2
        ),
        "utf8"
      );
    }
    rows.push(card);
  }

  fs.writeFileSync(
    path.join(GOLD, "manifest.json"),
    JSON.stringify(
      {
        level: 1,
        target: 50,
        count: rows.length,
        generated_at: new Date().toISOString(),
        grade_enum: ["PARSE_OK", "RENDER_OK", "TOPOLOGY_OK", "TEXTBOOK_OK", null],
        fail_reason_enum: [
          "TOPOLOGY_ERROR",
          "WRONG_GATE",
          "MISSING_WIRE",
          "EXTRA_WIRE",
          "FANOUT_ERROR",
          "JUNCTION_MISSING",
          "CROSSING",
          "LABEL_POSITION",
          "SPACING",
          "SYMBOL_STYLE",
          "LAYOUT",
          "UNSUPPORTED",
        ],
        cards: rows.map((r) => ({
          id: r.id,
          bucket: r.bucket,
          fig_id: r.fig_id,
          tier_guess: r.tier_guess,
          image_exists: r.image_exists,
          grade: r.grade,
        })),
      },
      null,
      2
    ),
    "utf8"
  );

  const byBucket = {};
  for (const r of rows) {
    byBucket[r.bucket] = (byBucket[r.bucket] || 0) + 1;
  }

  let md = `# Level-1 金标清单（50 张空卡）

> 生成：\`node scripts/scaffold_level1.mjs\`  
> 验收标准见 \`ARCHITECTURE.md\`：仅 **TEXTBOOK_OK** 进训练集。  
> 每张卡目录：\`gold/level1/cards/<ID>/\` → \`card.json\` + \`ir.json\`

## 分布

| 子集 | 数量 |
|------|------|
${Object.entries(byBucket)
  .map(([k, n]) => `| ${k} | ${n} |`)
  .join("\n")}

## 标注步骤

1. 打开 \`cards/<ID>/\` 对应课本图（\`card.json\` → \`image\`）
2. 按图类填写 \`ir.json\`（logic 用 \`logic_ir_v1\`）
3. logic：\`node adapters/logic_ir_to_schematex.mjs cards/L01/ir.json\` → 对照台预览
4. 在 \`card.json\` 填写 \`grade\` / \`fail_reasons\` / \`tier_guess\` 修订

## 卡片表

| ID | 子集 | 图号 | tier_guess | 题注 | 图存在 |
|----|------|------|------------|------|--------|
`;

  for (const r of rows) {
    md += `| ${r.id} | ${r.bucket} | ${r.fig_id} | ${r.tier_guess} | ${r.caption} | ${r.image_exists ? "Y" : "N"} |\n`;
  }

  fs.writeFileSync(path.join(GOLD, "LEVEL1.md"), md, "utf8");
  console.log(JSON.stringify({ count: rows.length, byBucket, missing: rows.filter((r) => !r.image_exists).map((r) => r.id) }, null, 2));
}

main();
