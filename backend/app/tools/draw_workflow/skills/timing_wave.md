# Skill：时序波形图（timing_wave）

## 职责
生成 `wave_ir_v1` JSON，由 `wave_ir_to_svg` 渲染多信号高低电平时间轴。

## 规范
- schema_version=`wave_ir_v1`，diagram_type=`waveform`
- signals：1–10 条；每条 name + wave
- wave 字符：`0`/`1` 改电平，`.` 保持；长度建议 ≥4
- 在 schematex_workbench 金标 W01–W10 风格

## 输出格式
```json
{
  "schema_version": "wave_ir_v1",
  "diagram_type": "waveform",
  "title": "optional",
  "signals": [
    { "name": "A", "wave": "00001111" },
    { "name": "B", "wave": "00110011" },
    { "name": "Y", "wave": "00000111" }
  ]
}
```
