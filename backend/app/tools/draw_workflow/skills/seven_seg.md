# Skill：七段数码管（seven_seg）

## 职责
生成点亮参数（白底共阴教材风）；由 `draw_with_workflow(diagram_kind=seven_seg)` 经 runner 出图。

## 规范
- digit：整数 0–9
- 只画点亮示意，不画外形引脚图

## 输出格式
```json
{
  "digit": 5,
  "title": "共阴七段数码管"
}
```
