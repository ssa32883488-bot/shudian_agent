# Level-1 金标清单（50 张空卡）

> 生成：`node scripts/scaffold_level1.mjs`  
> 验收标准见 `ARCHITECTURE.md`：仅 **TEXTBOOK_OK** 进训练集。  
> 每张卡目录：`gold/level1/cards/<ID>/` → `card.json` + `ir.json`

## 分布

| 子集 | 数量 |
|------|------|
| basic_gates | 10 |
| combinational | 10 |
| flipflop_seq | 10 |
| state | 10 |
| waveform | 10 |

## 标注步骤

1. 打开 `cards/<ID>/` 对应课本图（`card.json` → `image`）
2. 按图类填写 `ir.json`（logic 用 `logic_ir_v1`）
3. logic：`node adapters/logic_ir_to_schematex.mjs cards/L01/ir.json` → 对照台预览
4. 在 `card.json` 填写 `grade` / `fail_reasons` / `tier_guess` 修订

## 卡片表

| ID | 子集 | 图号 | tier_guess | 题注 | 图存在 |
|----|------|------|------------|------|--------|
| L01 | basic_gates | 2.5.2 | A | 举重裁判逻辑图 Y=A·(B+C) | Y |
| L02 | basic_gates | 2.5.4 | B | 例2.5.3的逻辑图 | Y |
| L03 | basic_gates | 2.5.5 | C | 例2.5.4的逻辑图（异或展开） | Y |
| L04 | basic_gates | 2.8.2 | A | 根据式(2.8.2)的逻辑电路图 | Y |
| L05 | basic_gates | 2.8.4 | A | 根据式(2.8.3)的逻辑电路图 | Y |
| L06 | basic_gates | 2.9.2 | A | 按式(2.9.2)接成的逻辑电路 | Y |
| L07 | basic_gates | 2.9.3 | A | 按式(2.9.3)接成的逻辑电路 | Y |
| L08 | basic_gates | 2.9.4 | B | 按式(2.9.5)接成的逻辑电路 | Y |
| L09 | basic_gates | 2.9.5 | B | 按式(2.9.6)接成的逻辑电路 | Y |
| L10 | basic_gates | 4.1.1 | A | 组合逻辑电路实例 | Y |
| C01 | combinational | 4.3.3 | B | 例4.3.1逻辑图之一 | Y |
| C02 | combinational | 4.3.4 | B | 例4.3.1逻辑图之二（与非） | Y |
| C03 | combinational | 4.3.6 | B | 例4.3.1逻辑图之三 | Y |
| C04 | combinational | 4.4.2 | B | 3位二进制编码器 | Y |
| C05 | combinational | 4.4.19 | A | 二选一数据选择器 | Y |
| C06 | combinational | 4.4.21 | A | 半加器 | Y |
| C07 | combinational | 4.7.4 | B | 1位全加器电路 | Y |
| C08 | combinational | 4.4.7 | B | 3线-8线译码器74HC138 | Y |
| C09 | combinational | 4.4.9 | B | 二-十进制译码器74HC42 | Y |
| C10 | combinational | 4.4.20 | B | 双4选1数据选择器74HC153 | Y |
| F01 | flipflop_seq | 5.2.1 | B | 或非门组成的锁存器 | Y |
| F02 | flipflop_seq | 5.2.2 | B | 与非门组成的SR锁存器 | Y |
| F03 | flipflop_seq | 5.3.1 | B | 电平触发SR触发器 | Y |
| F04 | flipflop_seq | 5.3.4 | B | 电平触发D触发器 | Y |
| F05 | flipflop_seq | 5.3.7 | B | 两电平D组成边沿触发器 | Y |
| F06 | flipflop_seq | 6.2.1 | B | 例6.2.1时序逻辑电路 | Y |
| F07 | flipflop_seq | 6.2.3 | B | 例6.2.3时序逻辑电路 | Y |
| F08 | flipflop_seq | 6.3.1 | B | D触发器移位寄存器 | Y |
| F09 | flipflop_seq | 6.3.8 | B | 同步二进制加法计数器 | Y |
| F10 | flipflop_seq | 6.4.17 | B | 例6.4.3的逻辑图 | Y |
| S01 | state | 6.2.2 | C | 图6.2.1电路的状态转换图 | Y |
| S02 | state | 6.2.4 | C | 图6.2.3电路的状态转换图 | Y |
| S03 | state | 6.2.11 | C | 图6.2.10电路的状态转换图 | Y |
| S04 | state | 6.3.9 | C | 图6.3.8电路的状态转换图 | Y |
| S05 | state | 6.4.2 | C | 例6.4.1的状态转换图 | Y |
| S06 | state | 6.4.7 | C | 例6.4.2的状态转换图 | Y |
| S07 | state | 6.4.8 | C | 化简后的例6.4.2状态转换图 | Y |
| S08 | state | 6.4.14 | C | 例6.4.3的状态转换图 | Y |
| S09 | state | 6.4.19 | C | 例6.4.4的状态转换图 | Y |
| S10 | state | 6.4.26 | C | 例6.4.5电路的状态转换图 | Y |
| W01 | waveform | 2.5.3 | C | 图2.5.1电路逻辑功能波形图 | Y |
| W02 | waveform | 2.5.6 | C | 例2.5.5的波形图 | Y |
| W03 | waveform | 5.2.3 | C | 例5.2.1电路和电压波形 | Y |
| W04 | waveform | 5.3.3 | C | 例5.3.1的电压波形图 | Y |
| W05 | waveform | 5.3.6 | C | 例5.3.2的电压波形 | Y |
| W06 | waveform | 5.3.9 | C | 例5.3.3的电压波形图 | Y |
| W07 | waveform | 5.3.11 | C | 例5.3.4的电压波形 | Y |
| W08 | waveform | 5.3.14 | C | 例5.3.5的电压波形图 | Y |
| W09 | waveform | 6.3.2 | C | 图6.3.1电路的电压波形 | Y |
| W10 | waveform | 6.3.7 | C | 例6.3.1电路的波形图 | Y |
