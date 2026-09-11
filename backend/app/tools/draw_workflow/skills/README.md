# Skill：数电教材绘图工作流（Agent 用）

> 权威定稿：`shudian_agent/docs/定稿-绘图子系统.md`  
> **唯一入口**：`draw_with_workflow`（8 种 kind，无其它绘图工具）

## 调用卡（复制即用）

```text
draw_with_workflow(
  brief="题意：画什么 + 芯片/表达式/约束",
  diagram_kind="",     # 能确定就填；不确定留空由路由推断
  slots_json="",       # 可选结构化槽位
  script="",           # 可选完整 IR JSON
  max_retries=3        # 结构校验修正上限 1..3
)
```

正文占位（勿编造 URL）：

```text
<<<DRAW kind="msi_design" desc="简短中文说明">>>
```

## 选 kind（仅此 8 种）

| 场景 | kind |
|------|------|
| 门级逻辑 / 表达式实现（含异或） | `logic_dag` |
| 时序波形 | `timing_wave` |
| 状态转换图 | `state_machine` |
| 真值表 | `truth_table` |
| 卡诺图 ≤4 变量 | `kmap` |
| 七段数码管 | `seven_seg` |
| TTL/CMOS VTC | `char_curve` |
| **芯片搭电路、置零/加载、555、DAC、模N…** | **`msi_design`** |

**禁止**：框图 / 泛原理图（已搁置）。  
**禁止**：直调其它绘图工具名；一律走本工作流。

## 流程与上限

1. 路由 kind → 读对应 `skills/<kind>.md`  
2. 生成 IR/参数 JSON → **结构校验** → 引擎出 **SVG**  
3. 失败则带 feedback 重试；**单次工具最多 3 次**（`max_retries`）  
4. 会话累计绘图次数另受 `AGENT_MAX_DRAW_CALLS`（默认 3）熔断  

## msi_design 要点

- 方法论：项目 `.cursor/skills/msi-design-circuit/SKILL.md`  
- 本 Skill：`msi_design.md`  
- 器件库：`draw/digital_dig/LIBRARY.md`  
- 必须：`logic_first` + `components` + `connections`  
- 硬规范：线不穿符号；同步清零检 N−1；进位显式门  
- 环境：`runtime/` workbench + Node；MSI 需 Java 17 + `DIGITAL_JAR`（部署前跑 `python -m scripts.check_draw_runtime`）
