# Schematex 对照台（独立工具）

与 `shudian_agent` **完全独立**。用途：左边贴 DSL，右边立刻出图；配合课本原图做「看图写脚本」验收。

## 架构定稿

见 [`ARCHITECTURE.md`](ARCHITECTURE.md)：目标分层、四级验收、`TEXTBOOK_OK`、IR、A/B/C。

## 已落地（本阶段）

| 产物 | 路径 |
|------|------|
| Logic IR Schema | `ir/schema/logic_ir.schema.json` |
| State / Wave IR Schema | `ir/schema/state_ir.schema.json` · `wave_ir.schema.json` |
| IR→Schematex 适配器 | `adapters/logic_ir_to_schematex.mjs` |
| Level-1 50 空卡 | `gold/level1/LEVEL1.md` |
| 看图出 IR 提示词 | `prompts/看图出IR.md` |

```bash
npm run scaffold-level1
node adapters/logic_ir_to_schematex.mjs ir/examples/fig_2_5_2.ir.json
```

## 启动

```bash
cd schematex_workbench
npm install
npm run dev
```

浏览器打开终端提示的本地地址（一般是 http://127.0.0.1:5173 ）。

## 课本图分类

```bash
npm run organize-figures
```

会生成：

- `textbook_figures/CATALOG.md` — **总清单（你要的「整理好到一个文件」）**
- `textbook_figures/manifest.json` — 机器可读
- `textbook_figures/<kind>/*.jpg` — 按类复制的原图

## 给大模型的提示词

见 [`prompts/看图出DSL.md`](prompts/看图出DSL.md)

## 目录

```text
schematex_workbench/
  index.html / main.js / style.css   # 对照台 UI
  prompts/看图出DSL.md
  textbook_figures/CATALOG.md
  scripts/organize_figures.mjs
```
