# 金标实例 + 通用方法论索引

- **通用方法论（一切 MSI 设计电路）**  
  - Cursor skill：`.cursor/skills/msi-design-circuit/SKILL.md`  
  - 工作流 skill：`draw_workflow/skills/msi_design.md`  
  - 图类：`msi_design`

- **本文件**：74163 置零法模 7 金标 **实例**（v8），用来锚定布线规范与验收，不是唯一题型。

详见方法论 skill 第三、五节；实例细则如下。

---

# 金标实例：74163 置零法模 7（detect state 6）· v8

> 用户 2026-09-09 认可。

## 逻辑

| 项 | 约定 |
|----|------|
| 序列 | `0→1→2→3→4→5→6→0` |
| 检测态 | **6** = `110`（同步清零 = N−1） |
| 清零 | `~R = NAND(Q2,Q1,~Q0)` |
| 进位 | `CO = AND(Q2,Q1,~Q0)`（显式与门） |
| Q0 | 经 Not；Q3 只探针；不用芯片 C |

## 布线硬规则（升格为方法论通用条款）

1. 禁止线穿芯片/门符号  
2. 实线为主；Tunnel 仅长回授且落在端点  
3. 门从输入侧进线；绕行槽在门外侧  
4. 正交走线；改完静检 + 截图  

## 验收

`validate_logic_first` → 布局静检 → `CLI test` MOD7 passed
