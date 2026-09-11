# Skill：特性曲线（char_curve）

## 职责
生成 VTC 参数；由 `draw_with_workflow(diagram_kind=char_curve)` 经 Matplotlib runner 出图。

## 规范
- curve 仅：`ttl_vtc` | `cmos_vtc`
- 示意曲线，非实测数据
- 轴为伏特数字刻度

## 输出格式
```json
{
  "curve": "ttl_vtc",
  "title": "TTL 反相器 VTC"
}
```
