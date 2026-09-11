# 数电图绘制：目标分层与技术定稿

> 状态：定稿（2026-08-29）  
> 范围：Schematex / Tier-A/B/C / 课本金标 / Agent 路由  
> 原则：**不推翻现有路线**；把「像教材」拆成语义正确与版式还原两层。

---

## 0. 一句话

LLM 负责「看懂图、写语义」；引擎负责「渲染」；**不要让「逻辑 DSL + 自动布局」同时扛语义与像素级排版。**

核心资产不是 Schematex 本身，而是：

**数电 IR + 图类路由（能力矩阵）+ 课本金标 + 分级验收 + DSL/适配器提示词**

---

## 1. 目标拆层

| 层级 | 含义 | 谁负责 |
|------|------|--------|
| **语义正确** | 图类、门/状态/波形元素、端口、连接关系、逻辑式对 | LLM → IR →（可选）DSL |
| **版式还原** | 国标符号、左右流向、正交走线、结点、间距、标签 | 引擎能力 / SVG 后处理 / 专用 Renderer |

产品表述建议从「像素级复刻阎石某一页」改为：

> **符合数字电子技术教材视觉规范**（IEC 矩形门、左入右出、曼哈顿走线、扇出有结点、标签清楚、间距统一）。

---

## 2. 合格等级（取代「能渲染即成功」）

| 等级 | 含义 | 进训练集？ | 可对用户返回？ |
|------|------|------------|----------------|
| `PARSE_OK` | DSL/IR 能解析 | ❌ | ❌ |
| `RENDER_OK` | 能出 SVG | ❌ | ❌ |
| `TOPOLOGY_OK` | 门/端口/连线/逻辑关系正确 | ⚠️ 可作弱样本 | ⚠️ 仅草稿/内部 |
| `TEXTBOOK_OK` | 拓扑 + 符号 + 布局 + 走线达教材规范 | ✅ | ✅ **Agent 唯一成功标准** |

**Agent 对外成功 = 仅 `TEXTBOOK_OK`。**

失败必须记 `FAIL_REASON`（可多选），例如：

`TOPOLOGY_ERROR` / `WRONG_GATE` / `MISSING_WIRE` / `EXTRA_WIRE` / `FANOUT_ERROR` / `JUNCTION_MISSING` / `CROSSING` / `LABEL_POSITION` / `SPACING` / `SYMBOL_STYLE` / `LAYOUT` / `UNSUPPORTED`

用来区分：**模型错了**还是**引擎/后处理不够**。

---

## 3. 流水线（在现有「原图→模型→DSL→Schematex」上加层）

```text
用户问题 / 教材原图
        │
        ▼
  图类识别（路由）
        │
   ┌────┴────┬──────────────┐
   ▼         ▼              ▼
  A类       B类            C类
 Schematex  Schematex      专用 Renderer
   │        + SVG后处理      （IR→自研/模板）
   ▼         ▼              ▼
  DSL←IR    DSL←IR         IR
   │         │              │
   └────┬────┴──────┬───────┘
        ▼           ▼
       SVG        校验 Agent
        │           │
        └─────┬─────┘
              ▼
     TEXTBOOK_OK ? 返回 : 改 IR/DSL 或换引擎降级
```

要点：

- **LLM 不猜坐标**；只产出结构化语义（IR），再经 Adapter 生成 Schematex DSL 或其它后端。
- 暂不 fork Schematex；等 100～300 张金标后，若失败主因集中在 fan-out/layout/junction，再改引擎。

Schematex Logic 已知边界：依赖图 → DAG 布局 → Manhattan 布线；**显式 fan-out + junction dot 官方未完成** → 「逻辑对、走线乱」多半是引擎边界，不是提示词能根治。

---

## 4. 中间表示 IR（最值得加的一层）

示例（举重裁判 / 图2.5.2 语义）：

```yaml
diagram_type: logic
style: iec          # 国标矩形
inputs: [A, B, C]
gates:
  G1: { type: OR,  inputs: [B, C] }
  G2: { type: AND, inputs: [A, G1] }
outputs:
  Y: G2
```

路径：

- `IR → Schematex Adapter → DSL → Schematex`
- 将来：`IR → CircuitikZ / 自研 SVG Adapter`（不锁死引擎）

IR 是金标标注的主载体；DSL 是某一后端的投影。

---

## 5. A / B / C 制度化

| 类 | 定义 | 策略 |
|----|------|------|
| **A** | Schematex **语义+视觉**都能到 `TEXTBOOK_OK` | IR→DSL→Schematex 直出 |
| **B** | 语义能表达，**视觉达不到**教材规范（复杂扇出、全加器、多级组合等） | 标 `A_semantic=YES, A_visual=NO`；Schematex SVG + **后处理**（结点、疏距、标签）或日后换 Adapter |
| **C** | 不适合 Schematex 对照教材 | 专用渲染：卡诺 / 真值表 / 曲线 / 符号表 / 教材波形 / 圆形状态图等 |

注意：**「类型支持」≠「归入 A」**。必须实测达到 `TEXTBOOK_OK` 才进 A。

与现网工具对齐（已有）：

- C/B 已存在：`draw_kmap`、真值表、七段、VTC、符号表、`draw_xor_basic_gates`、`draw_state_ring`、`draw_timing_sft`
- A 试验场：`schematex_workbench` + 日后 IR Adapter

---

## 6. 能力矩阵（Agent 路由表 · 初稿，用金标实测填「还原率」）

| 图类 | 暂定档 | Schematex | 当前策略 |
|------|--------|-----------|----------|
| 基本门（少扇出） | A? | 可 | 金标验证后定档 |
| 简单组合（清晰 DAG） | A? | 可 | 同上 |
| 复杂扇出 / 全加器 | B | 语义可、走线差 | DSL + 后处理或 B 模板 |
| 触发器功能图 | A?/B | 视实测 | |
| 圆形状态转换图 | C | 视觉不符 | `StateDiagramIR` + ring renderer |
| 教材波形 | C/B | timing≠教材版式 | Waveform IR + 教材渲染器 |
| 卡诺 / 真值表 / 曲线 / 符号表 | C | 否 | 现有 Tier-B |

矩阵随金标更新；决策 Agent **查表路由**，不临场猜。

---

## 7. 课本分类图库（Level 1：50 张）

不要先堆 1000 张。先做：

| 子集 | 数量 |
|------|------|
| 基本门电路 | 10 |
| 组合逻辑 | 10 |
| 触发器/时序结构 | 10 |
| 状态图 | 10 |
| 波形 | 10 |

每张卡片字段：

`原图 → 图类 → 人工 IR →（可选 DSL）→ 引擎 SVG → 验收等级 → FAIL_REASON[] → 路由策略(A/B/C)`

目录锚点（已有粗分，需精修为 50 金标）：

- `schematex_workbench/textbook_figures/CATALOG.md`
- 对照台：`schematex_workbench/`（左 DSL 右预览）

---

## 8. 近期只投三件事（优先级）

1. **教材图 → IR 人工金标**（含等级与失败原因） → 已建空卡：`gold/level1/`  
2. **A/B/C 能力矩阵**（用金标实测填表，写入路由） → 卡片内 `tier_guess` 待修订  
3. **TEXTBOOK_OK 验收体系** → `card.json` 的 `grade` / `fail_reasons` 字段已预留  

工具：

- Schema：`ir/schema/*.schema.json`  
- Adapter：`adapters/logic_ir_to_schematex.mjs`  
- 提示词：`prompts/看图出IR.md`  

显式暂缓：

- 继续堆「让自动布局更漂亮」的超级 Prompt  
- fork Schematex  

先验证：**大模型看教材图 → 能否稳定产出正确 IR/语义**。

---

## 9. 与旧工作的关系

| 已有 | 去留 |
|------|------|
| Tier-A 子工作流 / `draw_diagram` | 保留方向；上收为「IR→Adapter→引擎」 |
| `schematex_workbench` | 保留，作 DSL/渲染人工台 |
| `CATALOG.md` 粗分图 | 作 Level-1 候选池，人工筛 50 |
| `RENDER_OK` 画廊话术 | 废弃作成功标准 |
| 看图出 DSL 提示词 | 演进为「看图出 IR」，再规则生成 DSL |

---

## 10. 决议摘要

1. 路线不推翻；目标分层：语义 / 版式。  
2. 对外成功只认 `TEXTBOOK_OK`。  
3. 引入 IR，避免锁死 Schematex。  
4. A/B/C 按「能否 TEXTBOOK_OK」定，不按「引擎是否声明支持」。  
5. 逻辑门产品默认 **国标 iec 矩形**。  
6. 近期资产：50 张金标 + 矩阵 + 验收；不先改引擎。
