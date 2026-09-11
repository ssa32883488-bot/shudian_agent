# Skill：真值表（truth_table）

## 职责
生成真值表参数 JSON；由 `draw_with_workflow(diagram_kind=truth_table)` 经 runner 出图。

## 规范
- inputs / outputs：列名字符串数组
- rows：每行是 inputs+outputs 拼接的 0/1 列表
- 行数通常为 2^len(inputs)

## 输出格式
```json
{
  "inputs": ["A", "B"],
  "outputs": ["Y"],
  "rows": [[0,0,0],[0,1,1],[1,0,1],[1,1,0]],
  "title": "异或真值表"
}
```
