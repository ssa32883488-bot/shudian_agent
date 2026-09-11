# 课本图分类清单（Schematex 对照用）

> 来源：阎石《数字电子技术基础》Markdown 拆章  
> 生成：`npm run organize-figures`  
> **说明**：粗分候选，供大模型看图写 DSL；符号表/卡诺/真值表/曲线已剔除。


## logic_dag（82 张）

| 图号 | 题注 | 文件 |
|------|------|------|
| 2.5.2 | 描述图2.5.1电路逻辑功能的逻辑图 | `logic_dag/fig_2_5_2.jpg` |
| 2.5.4 | 例2.5.3的逻辑图 | `logic_dag/fig_2_5_4.jpg` |
| 2.5.5 | 例2.5.4的逻辑图 | `logic_dag/fig_2_5_5.jpg` |
| 2.8.2 | 根据式(2.8.2)得到的逻辑电路图 | `logic_dag/fig_2_8_2.jpg` |
| 2.8.4 | 根据式(2.8.3)得到的逻辑电路图 | `logic_dag/fig_2_8_4.jpg` |
| 2.9.2 | 按照式(2.9.2)接成的逻辑电路 | `logic_dag/fig_2_9_2.jpg` |
| 2.9.3 | 按照式(2.9.3)接成的逻辑电路 | `logic_dag/fig_2_9_3.jpg` |
| 2.9.4 | 按照式(2.9.5)接成的逻辑电路 | `logic_dag/fig_2_9_4.jpg` |
| 2.9.5 | 按照式(2.9.6)接成的逻辑电路 | `logic_dag/fig_2_9_5.jpg` |
| 3.4.34 | OC 门输出并联的接法及逻辑图 | `logic_dag/fig_3_4_34.jpg` |
| 4.1.1 | 组合逻辑电路实例 | `logic_dag/fig_4_1_1.jpg` |
| 4.3.1 | 组合逻辑电路的基本设计过程 | `logic_dag/fig_4_3_1.jpg` |
| 4.3.3 | 例4.3.1的逻辑图之一 | `logic_dag/fig_4_3_3.jpg` |
| 4.3.4 | 例4.3.1的逻辑图之二 | `logic_dag/fig_4_3_4.jpg` |
| 4.3.6 | 例4.3.1的逻辑图之三 | `logic_dag/fig_4_3_6.jpg` |
| 4.4.2 | 3 位二进制编码器 | `logic_dag/fig_4_4_2.jpg` |
| 4.4.3 | 8 线-3 线优先编码器 74HC148 | `logic_dag/fig_4_4_3.jpg` |
| 4.4.4 | 二-十进制优先编码器 74HC147 | `logic_dag/fig_4_4_4.jpg` |
| 4.4.7 | 用与非门组成的 3 线-8 线译码器 74HC138 | `logic_dag/fig_4_4_7.jpg` |
| 4.4.9 | 二-十进制译码器 74HC42 | `logic_dag/fig_4_4_9.jpg` |
| 4.4.19 | 二选一数据选择器 | `logic_dag/fig_4_4_19.jpg` |
| 4.4.20 | 双 4 选 1 数据选择器 74HC153 | `logic_dag/fig_4_4_20.jpg` |
| 4.4.21 | 半加器 | `logic_dag/fig_4_4_21.jpg` |
| 4.4.23 | 双全加器 74LS183 | `logic_dag/fig_4_4_23.jpg` |
| 4.5.1 | 用两片 74HC148 接成的 16 线-4 线优先编码器 | `logic_dag/fig_4_5_1.jpg` |
| 4.5.2 | 用两片 74HCI38 接成的 4 线 -16 线译码器 | `logic_dag/fig_4_5_2.jpg` |
| 4.5.4 | 所示, 则数据选择器的输出就是式 (4.5.4) 所要求的逻辑函数 Z。 | `logic_dag/fig_4_5_4.jpg` |
| 4.7.1 | 所示的 2 选 1 数据选择器为例, 若用 Verilog HDL 对它作行为描述, 则可写成下面的程序模块。 | `logic_dag/fig_4_7_1.jpg` |
| 4.7.2 | 2选1数据选择器的电路原理图 | `logic_dag/fig_4_7_2.jpg` |
| 4.7.4 | 例 4.7.1 中的 1 位全加器电路 | `logic_dag/fig_4_7_4.jpg` |
| 4.9.2 | 2 线-4 线译码器中的竞争-冒险现象 | `logic_dag/fig_4_9_2.jpg` |
| 4.4.3 | 。允许附加必要的门电路。 | `logic_dag/fig_4_4_3_e598df57.jpg` |
| 4.4.7 | ）和门电路产生如下多输出逻辑函数的逻辑图。 | `logic_dag/fig_4_4_7_8a9277ca.jpg` |
| 4.5.5 | ) 产生逻辑函数 | `logic_dag/fig_4_5_5.jpg` |
| 5.2.1 | 用或非门组成的锁存器 | `logic_dag/fig_5_2_1.jpg` |
| 5.2.2 | 用与非门组成的 SR 锁存器 | `logic_dag/fig_5_2_2.jpg` |
| 5.3.1 | 电平触发 SR 触发器（门控 SR 锁存器） | `logic_dag/fig_5_3_1.jpg` |
| 5.3.2 | 带异步置位、复位端的电平触发 SR 触发器 | `logic_dag/fig_5_3_2.jpg` |
| 5.3.4 | 电平触发 D 触发器 (D 型锁存器) | `logic_dag/fig_5_3_4.jpg` |
| 5.3.5 | 利用 CMOS 传输门组成的电平触发 D 触发器（透明 D 型锁存器） | `logic_dag/fig_5_3_5.jpg` |
| 5.3.7 | 用两个电平触发 D 触发器组成的边沿触发器 | `logic_dag/fig_5_3_7.jpg` |
| 5.3.8 | 带有异步置位、复位端的 CMOS 边沿触发 D 触发器 | `logic_dag/fig_5_3_8.jpg` |
| 5.3.10 | 脉冲触发的 SR 触发器 | `logic_dag/fig_5_3_10.jpg` |
| 5.3.12 | 正脉冲触发的 JK 触发器 | `logic_dag/fig_5_3_12.jpg` |
| 5.3.13 | 具有多输入端的主从JK触发器（a）电路结构 （b）逻辑符号 | `logic_dag/fig_5_3_13.jpg` |
| 5.3.16 | $T$ 触发器的图形逻辑符号 | `logic_dag/fig_5_3_16.jpg` |
| 5.3.17 | 将 JK 触发器用作 SR、T 触发器 | `logic_dag/fig_5_3_17.jpg` |
| 5.3.18 | 用两个电平触发 D 触发器构成的边沿触发 JK 触发器 (CC4027) | `logic_dag/fig_5_3_18.jpg` |
| 5.3.19 | 边沿触发 D 触发器动态特性的分析 | `logic_dag/fig_5_3_19.jpg` |
| 5.4.1 | 74LS75的逻辑图 | `logic_dag/fig_5_4_1.jpg` |
| 5.4.2 | 74HC175 的逻辑图 | `logic_dag/fig_5_4_2.jpg` |
| 4.4.7 | ) 组成 4096×4 位的 RAM。 | `logic_dag/fig_4_4_7_adf690ee.jpg` |
| 6.2.1 | 例6.2.1的时序逻辑电路 | `logic_dag/fig_6_2_1.jpg` |
| 6.2.3 | 例6.2.3的时序逻辑电路 | `logic_dag/fig_6_2_3.jpg` |
| 6.2.10 | 例 6.2.4 的异步时序逻辑电路 | `logic_dag/fig_6_2_10.jpg` |
| 6.3.1 | 用 D 触发器构成的移位寄存器 | `logic_dag/fig_6_3_1.jpg` |
| 6.3.3 | 用 JK 触发器构成的移位寄存器 | `logic_dag/fig_6_3_3.jpg` |
| 6.3.4 | 双向移位寄存器 74HC194A 的逻辑图 | `logic_dag/fig_6_3_4.jpg` |
| 6.3.8 | 所示电路就是按式(6.3.1)接成的 4 位二进制同步加法计数器。由图可见, 各触发器的驱动方程为 | `logic_dag/fig_6_3_8.jpg` |
| 6.3.8 | 用 $T$ 触发器构成的同步二进制加法计数器 | `logic_dag/fig_6_3_8_01faea9b.jpg` |
| 6.3.11 | 4 位同步二进制计数器 74161 的逻辑图 | `logic_dag/fig_6_3_11.jpg` |
| 6.3.13 | 用 T 触发器接成的同步二进制减法计数器 | `logic_dag/fig_6_3_13.jpg` |
| 6.3.14 | 单时钟同步十六进制加/减计数器 74LS191 的逻辑图 | `logic_dag/fig_6_3_14.jpg` |
| 6.3.16 | 双时钟同步十六进制加/减计数器 74LS193 的逻辑图 | `logic_dag/fig_6_3_16.jpg` |
| 6.3.19 | 同步十进制加法计数器 74160 的逻辑图 | `logic_dag/fig_6_3_19.jpg` |
| 6.3.50 | 用计数器和译码器构成的顺序脉冲发生器 | `logic_dag/fig_6_3_50.jpg` |
| 6.3.52 | 用扭环形计数器和译码器构成的顺序脉冲发生器 | `logic_dag/fig_6_3_52.jpg` |
| 6.3.53 | 用计数器和数据选择器组成的序列信号发生器 | `logic_dag/fig_6_3_53.jpg` |
| 6.3.54 | 中的反馈逻辑电路就是按式(6.3.16)接成的。 | `logic_dag/fig_6_3_54.jpg` |
| 6.4.1 | 同步时序逻辑电路的设计过程 | `logic_dag/fig_6_4_1.jpg` |
| 6.4.5 | 所示。 | `logic_dag/fig_6_4_5.jpg` |
| 6.4.11 | 用 JK 触发器设计的例 6.4.2 电路 | `logic_dag/fig_6_4_11.jpg` |
| 6.4.13 | 用 $D$ 触发器设计的例6.4.2电路 | `logic_dag/fig_6_4_13.jpg` |
| 6.4.17 | 例6.4.3的逻辑图 | `logic_dag/fig_6_4_17.jpg` |
| 6.4.23 | 例6.4.4的逻辑图 | `logic_dag/fig_6_4_23.jpg` |
| 6.4.29 | 例6.4.5的逻辑图 | `logic_dag/fig_6_4_29.jpg` |
| 6.4.35 | 异步十进制减法计数器的逻辑图 | `logic_dag/fig_6_4_35.jpg` |
| 6.3.19 | 和表 6.3.4。 | `logic_dag/fig_6_3_19_5ee6c5c8.jpg` |
| 6.3.22 | ，它的功能表与表6.3.5相同。可以附加必要的门电路。 | `logic_dag/fig_6_3_22.jpg` |
| 7.2.1 | 的施密特触发电路中可以看出， $\mathrm{T}_{2}$ 饱和导通时输出端 $v_{0}$ 的低电平近似地等于 $V_{\mathrm{CC}}R_{\mathrm{E}} / (R_{2} + R_{\mathrm{E}})$ ，不是接近于0的逻辑低电平。因此，在将图7.2.1的施密特触发电路用于逻辑电路时，还需要在电路的输出端附加电平变换电路，将输出的低电平变换为标准的逻辑低电平。 | `logic_dag/fig_7_2_1.jpg` |
| 7.3.9 | 集成单稳态电路 74121 简化的逻辑图 | `logic_dag/fig_7_3_9.jpg` |
| 8.6.10 | 双积分型 A/D 转换器的控制逻辑电路 | `logic_dag/fig_8_6_10.jpg` |

## timing_wave（23 张）

| 图号 | 题注 | 文件 |
|------|------|------|
| 2.5.3 | 描述图 2.5.1 电路逻辑功能的波形图 | `timing_wave/fig_2_5_3.jpg` |
| 2.5.6 | 例2.5.5的波形图 | `timing_wave/fig_2_5_6.jpg` |
| 3.4.21 | TTL 反相器的动态电压波形 | `timing_wave/fig_3_4_21.jpg` |
| 5.2.3 | 例 5.2.1 的电路和电压波形 | `timing_wave/fig_5_2_3.jpg` |
| 5.3.3 | 例5.3.1的电压波形图 | `timing_wave/fig_5_3_3.jpg` |
| 5.3.6 | 例 5.3.2 的电压波形 | `timing_wave/fig_5_3_6.jpg` |
| 5.3.9 | 例5.3.3的电压波形图 | `timing_wave/fig_5_3_9.jpg` |
| 5.3.11 | 例 5.3.4 的电压波形 | `timing_wave/fig_5_3_11.jpg` |
| 5.3.14 | 例5.3.5的电压波形图 | `timing_wave/fig_5_3_14.jpg` |
| 5.3.15 | 例 5.3.6 的电压波形图 | `timing_wave/fig_5_3_15.jpg` |
| 6.3.2 | 图6.3.1电路的电压波形 | `timing_wave/fig_6_3_2.jpg` |
| 6.3.7 | 例6.3.1电路的波形图 | `timing_wave/fig_6_3_7.jpg` |
| 7.3.2 | 图 7.3.1 电路的电压波形图 | `timing_wave/fig_7_3_2.jpg` |
| 7.3.6 | 图 7.3.5 电路的电压波形图 | `timing_wave/fig_7_3_6.jpg` |
| 7.3.10 | 集成单稳态电路 74121 的工作波形图 | `timing_wave/fig_7_3_10.jpg` |
| 7.4.6 | 所示的非对称型多谐振荡电路。但需注意的是，在输入电压低于 $V_{\mathrm{TH}}$ 时反相器的输入电流不能忽略不计，所以电容充、放电时的等效电路略显复杂一些，而且输出电压波形的占空比不等于 $50\%$ 。 | `timing_wave/fig_7_4_6.jpg` |
| 7.4.9 | 图 7.4.6 电路的工作波形图 | `timing_wave/fig_7_4_9.jpg` |
| 7.4.11 | 图 7.4.10 电路的工作波形图 | `timing_wave/fig_7_4_11.jpg` |
| 7.5.5 | 图7.5.4电路的电压波形图 | `timing_wave/fig_7_5_5.jpg` |
| 7.5.7 | 图 7.5.6 电路的电压波形图 | `timing_wave/fig_7_5_7.jpg` |
| 8.6.9 | 双积分型 A/D 转换器的电压波形图 | `timing_wave/fig_8_6_9.jpg` |
| 8.6.13 | 图 8.6.12 电路中各点的电压波形 | `timing_wave/fig_8_6_13.jpg` |
| 8.2.5 | 。同步十进制计数器74HC160的功能表同表6.3.4。表P8.8给出了RAM的16个地址单元中所存的数据。高6位地址 $A_{9}\sim A_{4}$ 始终为0，在表中没有列出。RAM的输出数据只用了低4位，作为AD7520的输入。因RAM的高4位数据没有使用，故表中也未列出。 | `timing_wave/fig_8_2_5.jpg` |

## state_machine（26 张）

| 图号 | 题注 | 文件 |
|------|------|------|
| 6.2.2 | 图6.2.1电路的状态转换图 | `state_machine/fig_6_2_2.jpg` |
| 6.2.4 | 图 6.2.3 电路的状态转换图 | `state_machine/fig_6_2_4.jpg` |
| 6.2.11 | 图6.2.10电路的状态转换图 | `state_machine/fig_6_2_11.jpg` |
| 6.3.9 | 图 6.3.8 电路的状态转换图 | `state_machine/fig_6_3_9.jpg` |
| 6.3.18 | 图 6.3.17 电路的状态转换图 | `state_machine/fig_6_3_18.jpg` |
| 6.3.21 | 图6.3.20电路的状态转换图 | `state_machine/fig_6_3_21.jpg` |
| 6.3.32 | 图 6.3.31 电路的状态转换图 | `state_machine/fig_6_3_32.jpg` |
| 6.3.35 | 图6.3.34电路的状态转换图 | `state_machine/fig_6_3_35.jpg` |
| 6.3.41 | 图6.3.40电路的状态转换图 | `state_machine/fig_6_3_41.jpg` |
| 6.3.43 | 图6.3.44电路的状态转换图 | `state_machine/fig_6_3_43.jpg` |
| 6.3.46 | 图 6.3.45 电路的状态转换图 | `state_machine/fig_6_3_46.jpg` |
| 6.3.48 | 图6.3.47电路的状态转换图 | `state_machine/fig_6_3_48.jpg` |
| 6.4.2 | 例6.4.1的状态转换图 | `state_machine/fig_6_4_2.jpg` |
| 6.4.6 | 图6.4.5电路的状态转换图 | `state_machine/fig_6_4_6.jpg` |
| 6.4.7 | 例6.4.2的状态转换图 | `state_machine/fig_6_4_7.jpg` |
| 6.4.8 | 化简后的例6.4.2的状态转换图 | `state_machine/fig_6_4_8.jpg` |
| 6.4.12 | 图6.4.11电路的状态转换图 | `state_machine/fig_6_4_12.jpg` |
| 6.4.14 | 例6.4.3的状态转换图 | `state_machine/fig_6_4_14.jpg` |
| 6.4.18 | 图 6.4.17 电路的状态转换图 | `state_machine/fig_6_4_18.jpg` |
| 6.4.19 | 例6.4.4的状态转换图 | `state_machine/fig_6_4_19.jpg` |
| 6.4.24 | 图6.4.23电路的状态转换图 | `state_machine/fig_6_4_24.jpg` |
| 6.4.26 | 例6.4.5电路的状态转换图 | `state_machine/fig_6_4_26.jpg` |
| 6.4.30 | 例 6.4.6 电路的状态转换图 | `state_machine/fig_6_4_30.jpg` |
| 6.4.36 | 图 6.4.35 电路的状态转换图 | `state_machine/fig_6_4_36.jpg` |
| 6.6.2 | 图 6.6.1 电路的状态转换图 | `state_machine/fig_6_6_2.jpg` |
| 6.3.29 | 。 | `state_machine/fig_6_3_29.jpg` |

## circuit_netlist（21 张）

| 图号 | 题注 | 文件 |
|------|------|------|
| 3.1.1 | 用来获得高、低电平的基本开关电路 | `circuit_netlist/fig_3_1_1.jpg` |
| 3.2.1 | 二极管开关电路 | `circuit_netlist/fig_3_2_1.jpg` |
| 3.2.5 | 二极管与门 | `circuit_netlist/fig_3_2_5.jpg` |
| 3.2.6 | 二极管或门 | `circuit_netlist/fig_3_2_6.jpg` |
| 3.1.1 | (a) 中的开关 S, 便得到了图 3.3.4 所示的 MOS 管开关电路。 | `circuit_netlist/fig_3_1_1_fd2cd266.jpg` |
| 3.3.4 | MOS 管的基本开关电路 | `circuit_netlist/fig_3_3_4.jpg` |
| 3.3.5 | MOS 管的开关等效电路 | `circuit_netlist/fig_3_3_5.jpg` |
| 3.3.8 | 用 P 沟道增强型 MOS 管接成的开关电路 | `circuit_netlist/fig_3_3_8.jpg` |
| 3.4.3 | 双极型三极管的基本开关电路 | `circuit_netlist/fig_3_4_3.jpg` |
| 3.4.5 | 双极型三极管的开关等效电路 | `circuit_netlist/fig_3_4_5.jpg` |
| 3.4.6 | 双极型三极管反相器的等效电路 | `circuit_netlist/fig_3_4_6.jpg` |
| 3.4.13 | TTL 反相器高电平输出等效电路 | `circuit_netlist/fig_3_4_13.jpg` |
| 4.4.6 | 用二极管与门阵列组成的 3 线-8 线译码器 | `circuit_netlist/fig_4_4_6.jpg` |
| 7.3.3 | 图 7.3.1 电路中电容 C 充电的等效电路 | `circuit_netlist/fig_7_3_3.jpg` |
| 7.4.3 | 计算 TTL 反相器静态工作点的等效电路 | `circuit_netlist/fig_7_4_3.jpg` |
| 7.4.4 | 图 7.4.1 电路中电容的充、放电等效电路 | `circuit_netlist/fig_7_4_4.jpg` |
| 7.4.8 | 图 7.4.6 电路中电容的充、放电等效电路 | `circuit_netlist/fig_7_4_8.jpg` |
| 7.4.14 | 图 7.4.12(b) 电路中电容 C 的充、放电等效电路 | `circuit_netlist/fig_7_4_14.jpg` |
| 7.4.6 | 所示非对称式多谐振荡电路中的 $G_{1}$ 和 $G_{2}$ 改用 TTL 反相器，并将 $R_{p}$ 短路，试画出电容 C 充、放电时的等效电路，并求出计算电路振荡频率的公式。 | `circuit_netlist/fig_7_4_6.jpg` |
| 8.2.4 | 计算倒 T 形电阻网络支路电流的等效电路 | `circuit_netlist/fig_8_2_4.jpg` |
| 8.2.6 | AD7520 中的 CMOS 模拟开关电路 | `circuit_netlist/fig_8_2_6.jpg` |

## block_struct（15 张）

| 图号 | 题注 | 文件 |
|------|------|------|
| 4.1.2 | 组合逻辑电路的框图 | `block_struct/fig_4_1_2.jpg` |
| 5.5.1 | SRAM 的结构框图 | `block_struct/fig_5_5_1.jpg` |
| 5.5.2 | 1024×4 位 SRAM 的结构框图 | `block_struct/fig_5_5_2.jpg` |
| 5.5.5 | $1\mathrm{M}\times 1$ 位DRAM的结构框图 | `block_struct/fig_5_5_5.jpg` |
| 5.5.6 | ROM的电路结构框图 | `block_struct/fig_5_5_6.jpg` |
| 5.5.7 | 二极管 ROM 的电路结构图 | `block_struct/fig_5_5_7.jpg` |
| 6.1.2 | 时序逻辑电路的结构框图 | `block_struct/fig_6_1_2.jpg` |
| 7.5.1 | 555 定时器的电路结构图 | `block_struct/fig_7_5_1.jpg` |
| 8.2.10 | DAC0808 的电路结构框图 | `block_struct/fig_8_2_10.jpg` |
| 8.6.6 | 逐次逼近型 A/D 转换器的电路结构框图 | `block_struct/fig_8_6_6.jpg` |
| 8.6.8 | 双积分型 A/D 转换器的结构框图 | `block_struct/fig_8_6_8.jpg` |
| 8.6.15 | V-F 变换型 A/D 转换器的电路结构框图 | `block_struct/fig_8_6_15.jpg` |
| 8.6.16 | 积分器型电荷平衡式 V-F 变换器的电路结构框图 | `block_struct/fig_8_6_16.jpg` |
| 8.6.17 | AD650 的电路结构框图 | `block_struct/fig_8_6_17.jpg` |
| 8.6.18 | LM331 的电路结构框图 | `block_struct/fig_8_6_18.jpg` |

## 已剔除 reject（146）

符号表/卡诺/真值表/曲线等，不建议喂给 Schematex。

## 未分类 unknown（628）

需人工再标。详见 `manifest.json`。
