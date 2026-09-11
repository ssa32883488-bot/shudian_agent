# Skill：卡诺图（kmap）

## 职责
生成卡诺图参数 JSON；由 `draw_with_workflow(diagram_kind=kmap)` 经 runner 出图。

## 规范
- var_count 仅 2/3/4（不支持 5/6）
- minterms：取 1 的最小项编号
- dont_cares：可选任意项
- auto_group 默认 true

## 输出格式
```json
{
  "minterms": [0, 2, 5, 7, 8, 10, 13, 15],
  "var_count": 4,
  "dont_cares": [],
  "auto_group": true,
  "title": "F=Σm(...)"
}
```
