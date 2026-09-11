/**
 * 从阎石教材 Markdown 抽图，按 Schematex 可对种类粗分，复制图片并写清单。
 * 独立于 shudian_agent。
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const MD_ROOT = path.resolve(
  ROOT,
  "..",
  "课本",
  "课本加习题册",
  "markdown_云端解析",
  "按章节拆分"
);
const IMG_DIR = path.join(MD_ROOT, "images");
const OUT = path.join(ROOT, "textbook_figures");

const FIG_CAP = /图\s*(\d+\.\d+\.\d+)\s*([^\n]*)/;
const IMG = /!\[[^\]]*\]\((?:images\/)?([0-9a-f]{64}\.(?:jpg|png|jpeg|webp))\)/gi;

const RULES = [
  ["reject", /图形符号|符号对照|特定外形|矩形轮廓|卡诺图|真值表|伏安特性|传输特性|特性曲线|VTC|七段/, "不进 Schematex 对照"],
  ["timing_wave", /波形图|电压波形|时序波形/, "timing"],
  ["state_machine", /状态转换图(?!.*SM)|状态图/, "state"],
  ["block_struct", /结构框图|电路的框图|方框图|结构图/, "blockdiagram"],
  ["circuit_netlist", /二极管与门|二极管或门|开关电路|等效电路/, "circuit"],
  ["logic_dag", /逻辑图|逻辑电路|全加器|半加器|编码器|译码器|选择器|数据选择|锁存器|触发器(?!.*波形)/, "logic"],
];

function classify(line) {
  for (const [kind, pat, note] of RULES) {
    if (pat.test(line)) return { kind, note };
  }
  return { kind: "unknown", note: "未分类" };
}

function parseChapter(filePath) {
  const text = fs.readFileSync(filePath, "utf8");
  const lines = text.split(/\r?\n/);
  const items = [];
  let pending = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const m of line.matchAll(IMG)) pending.push(m[1]);
    const m = line.match(FIG_CAP);
    if (!m) continue;
    const figId = m[1];
    const caption = (m[2] || "").trim() || line.trim().slice(0, 80);
    const images = pending.slice(-6);
    pending = [];
    const { kind, note } = classify(line);
    items.push({
      fig_id: figId,
      caption,
      caption_line: line.trim().slice(0, 200),
      chapter_file: path.basename(filePath),
      images,
      kind,
      note,
      line_no: i + 1,
    });
  }
  return items;
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function main() {
  if (!fs.existsSync(MD_ROOT)) {
    console.error("找不到教材目录:", MD_ROOT);
    process.exit(1);
  }
  const chapters = fs
    .readdirSync(MD_ROOT)
    .filter((n) => n.endsWith(".md"))
    .map((n) => path.join(MD_ROOT, n));

  let all = [];
  for (const ch of chapters) all = all.concat(parseChapter(ch));

  const kinds = [
    "logic_dag",
    "timing_wave",
    "state_machine",
    "circuit_netlist",
    "block_struct",
  ];

  const byKind = Object.fromEntries(kinds.map((k) => [k, []]));
  const rejected = [];
  const unknown = [];

  for (const it of all) {
    if (it.kind === "reject") rejected.push(it);
    else if (kinds.includes(it.kind)) byKind[it.kind].push(it);
    else unknown.push(it);
  }

  // 每类复制「有图片」的条目；文件名 fig_X_Y_Z__hash.jpg
  const manifest = { generated_at: new Date().toISOString(), kinds: {} };

  let md = `# 课本图分类清单（Schematex 对照用）

> 来源：阎石《数字电子技术基础》Markdown 拆章  
> 生成：\`npm run organize-figures\`  
> **说明**：粗分候选，供大模型看图写 DSL；符号表/卡诺/真值表/曲线已剔除。

`;

  for (const kind of kinds) {
    const rows = byKind[kind];
    const dir = path.join(OUT, kind);
    ensureDir(dir);
    const copied = [];

    for (const it of rows) {
      const img = (it.images || []).find((n) => fs.existsSync(path.join(IMG_DIR, n)));
      if (!img) continue;
      const ext = path.extname(img);
      const safeFig = it.fig_id.replace(/\./g, "_");
      const outName = `fig_${safeFig}${ext}`;
      // 同图号多图时加短哈希避免覆盖
      let finalName = outName;
      const destTry = path.join(dir, finalName);
      if (fs.existsSync(destTry)) {
        finalName = `fig_${safeFig}_${img.slice(0, 8)}${ext}`;
      }
      fs.copyFileSync(path.join(IMG_DIR, img), path.join(dir, finalName));
      copied.push({
        ...it,
        local_file: `${kind}/${finalName}`,
        source_hash: img,
      });
    }

    manifest.kinds[kind] = {
      count: copied.length,
      schematex_header: RULES.find((r) => r[0] === kind)?.[2] || kind,
      items: copied.map((c) => ({
        fig_id: c.fig_id,
        caption: c.caption,
        chapter: c.chapter_file,
        file: c.local_file,
        source_hash: c.source_hash,
      })),
    };

    md += `\n## ${kind}（${copied.length} 张）\n\n`;
    md += `| 图号 | 题注 | 文件 |\n|------|------|------|\n`;
    for (const c of copied) {
      md += `| ${c.fig_id} | ${c.caption.replace(/\|/g, "/")} | \`${c.local_file}\` |\n`;
    }
  }

  md += `\n## 已剔除 reject（${rejected.length}）\n\n符号表/卡诺/真值表/曲线等，不建议喂给 Schematex。\n`;
  md += `\n## 未分类 unknown（${unknown.length}）\n\n需人工再标。详见 \`manifest.json\`。\n`;

  fs.writeFileSync(path.join(OUT, "CATALOG.md"), md, "utf8");
  fs.writeFileSync(
    path.join(OUT, "manifest.json"),
    JSON.stringify(
      {
        ...manifest,
        reject_count: rejected.length,
        unknown_count: unknown.length,
        unknown_sample: unknown.slice(0, 30).map((u) => ({
          fig_id: u.fig_id,
          caption: u.caption,
          chapter: u.chapter_file,
        })),
      },
      null,
      2
    ),
    "utf8"
  );

  console.log(
    JSON.stringify(
      {
        out: OUT,
        counts: Object.fromEntries(
          kinds.map((k) => [k, manifest.kinds[k].count])
        ),
        reject: rejected.length,
        unknown: unknown.length,
      },
      null,
      2
    )
  );
}

main();
