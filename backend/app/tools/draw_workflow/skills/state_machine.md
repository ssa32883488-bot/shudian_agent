# Skill：状态转换图（state_machine）

## 职责
生成 `state_ir_v1` JSON，由 `state_ir_to_svg` 渲染圆形状态与转移标注。

## 规范
- schema_version=`state_ir_v1`，diagram_type=`state`
- states：字符串数组；transitions：{from,to,label?}
- layout：无坐标时用 `"auto"` / `"racetrack"`；有金标坐标用 `"free"` + positions
- 状态数建议 ≤12

## 输出格式
```json
{
  "schema_version": "state_ir_v1",
  "diagram_type": "state",
  "layout": "racetrack",
  "title": "mod4",
  "states": ["S0", "S1", "S2", "S3"],
  "transitions": [
    { "from": "S0", "to": "S1", "label": "/0" },
    { "from": "S1", "to": "S2", "label": "/0" },
    { "from": "S2", "to": "S3", "label": "/0" },
    { "from": "S3", "to": "S0", "label": "/1" }
  ]
}
```
