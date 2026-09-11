# Skill：逻辑符号图（logic_dag）

## 职责
根据需求生成 `logic_ir_v1` JSON，由 netlistsvg 自动布线出教材风格门级图。
金标对照：全加器 C07（课本原图 | netlistsvg）。

## 规范
- 只用标准门：AND/OR/NOT/NAND/NOR/XOR/XNOR/BUF；触发器可用 DFF（JKFF/LATCH 暂不可）
- 门名唯一；inputs 为输入端口列表；outputs 映射输出名→门/网名
- 扇出用显式中间网，勿写未声明信号
- diagram_type 固定 `"logic"`；schema_version 固定 `"logic_ir_v1"`
- style 建议 `"iec"`（国标矩形）或省略

## 禁止
- 不要输出 Schematex DSL
- 不要画框图/原理图
- 不要使用未支持的门类型

## 输出格式（只输出 JSON）
```json
{
  "schema_version": "logic_ir_v1",
  "diagram_type": "logic",
  "style": "iec",
  "title": "short_title",
  "inputs": ["A", "B"],
  "gates": {
    "n1": { "type": "NAND", "inputs": ["A", "B"] }
  },
  "outputs": { "F": "n1" }
}
```

## 样例：全加器
需求：1 位全加器 Sum=(A⊕B)⊕CI，Cout=AB+B·CI+A·CI
```json
{
  "schema_version": "logic_ir_v1",
  "diagram_type": "logic",
  "style": "iec",
  "title": "full_adder",
  "inputs": ["CI", "A", "B"],
  "gates": {
    "XOR1": { "type": "XOR", "inputs": ["A", "B"] },
    "Sum": { "type": "XOR", "inputs": ["CI", "XOR1"] },
    "AND1": { "type": "AND", "inputs": ["A", "B"] },
    "AND2": { "type": "AND", "inputs": ["B", "CI"] },
    "AND3": { "type": "AND", "inputs": ["A", "CI"] },
    "t1": { "type": "OR", "inputs": ["AND1", "AND2"] },
    "Cout": { "type": "OR", "inputs": ["t1", "AND3"] }
  },
  "outputs": { "Sum": "Sum", "Cout": "Cout" }
}
```
