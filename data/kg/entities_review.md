# 知识图谱实体抽取审阅稿

本文件仅含**实体**，尚未构建 TESTS / 前置关系。请重点看：Concept 是否过碎/过空，Problem 种类是否齐全。

## 汇总

- Chapter: **8**
- Problem: **425** （{'example': 82, 'review': 116, 'chapter_exercise': 227}）
- Concept 候选: **295** （置信度 {'low': 179, 'high': 109, 'medium': 7}）
- 小练(drill): **0**（辅导材料中未检出独立「小练」块；若书中有，需另补解析）

## Chapter

- `ch01` 第01章 数制和码制
- `ch02` 第02章 逻辑代数基础
- `ch03` 第03章 门电路
- `ch04` 第04章 组合逻辑电路
- `ch05` 第05章 半导体存储电路
- `ch06` 第06章 时序逻辑电路
- `ch07` 第07章 脉冲波形的产生和整形电路
- `ch08` 第08章 数模和模数转换

## Problem 抽样（每章每种最多 5 条）

### 第01章

- **example** ×2
  - `例1.4.1`: 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 【例 1.4.1】写出带符号位二进制数 00011010(+26)、10011010(-26)、00101101(+45) 和 101011
  - `例1.4.2`: 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 【例 1.4.2】用二进制补码运算求出 $13+10$ 、 $13-10$ 、 $-13+10$ 和 $-13-10$ 。 解：由于 $13
- **review** ×11
  - `R1.2.1`: 第01章 数制和码制 > review 复习思考题 R1.2.1 写出 4 位二进制数、4 位八进制数和 4 位十六进制数的最大数。
  - `R1.2.2`: 第01章 数制和码制 > review 复习思考题 R1.2.2 与4位二进制数、4位八进制数、4位十六进制数的最大值等值的十进制数各为多少？
  - `R1.3.1`: 第01章 数制和码制 > review 复习思考题 R1.3.1 在十-二转换中,整数部分的转换方法和小数部分的转换方法有何不同?
  - `R1.3.2`: 第01章 数制和码制 > review 复习思考题 R1.3.2 怎样将八进制数转换为十六进制数和将十六进制数转换为八进制数？
  - `R1.3.3`: 第01章 数制和码制 > review 复习思考题 R1.3.3 怎样才能将十进制数转换为八进制数？
- **chapter_exercise** ×15
  - `题1.1`: [题 1.1] 为了将 600 份文件顺序编码, 如果采用二进制代码, 最少需要用几位? 如果改用八进制或十六进制代码, 则最少各需要用几位?
  - `题1.10`: [题 1.10] 写出下列二进制数的原码、反码和补码。  (1) $(+1011)_2$ (2) $(+00110)_2$ (3) $(-1101)_2$ (4) $(-00101)_2$
  - `题1.11`: [题1.11] 写出下列带符号位二进制数(最高位为符号位)的反码和补码。 (1) $(011011)_{2}$ ; (2) $(001010)_{2}$ ; (3) $(111011)_{2}$ ; 
  - `题1.12`: [题1.12] 用8位的二进制补码表示下列十进制数。   (1) +17; (2) +28; (3) -13; (4) -47; (5) -89; (6) -121。
  - `题1.13`: [题 1.13] 计算下列用补码表示的二进制数的代数和。如果和为负数,请求出负数的绝对值。  (1) 01001101+00100110; (2) 00011101+01001100;  (3) 00

### 第02章

- **example** ×26
  - `例2.3.1`: 第02章 逻辑代数基础 > 2.3.1 基本公式 【例 2.3.1】用真值表证明表 2.3.1 中式(17)的正确性。 解：已知表2.3.1中的式(17)为 $$ A + B \cdot C = (A
  - `例2.4.1`: 第02章 逻辑代数基础 > 2.4.1 代入定理 【例 2.4.1】用代入定理证明德·摩根定理也适用于多变量的情况。 解：已知二变量的德·摩根定理为 $$ (A + B) ^ {\prime} = A
  - `例2.4.2`: 第02章 逻辑代数基础 > 2.4.2 反演定理 【例 2.4.2】已知 $Y=A(B+C)+CD$ ，求 $Y'$ 。 解：根据反演定理可写出 $$ \begin{array}{r l} Y ^ {
  - `例2.4.3`: 第02章 逻辑代数基础 > 2.4.2 反演定理 【例 2.4.3】 若 $Y=(AB'+C)'+D)'+C$ ，求 $Y'$ 。 解：依据反演定理可直接写出 $$ \begin{array}{r l
  - `例2.4.4`: 第02章 逻辑代数基础 > 2.4.3 对偶定理 【例 2.4.4】试证明表 2.3.1 中的式(17)，即 $$ A + B C = (A + B) (A + C) $$ 解：首先写出等式两边的对偶
- **review** ×13
  - `R2.2.1`: 第02章 逻辑代数基础 > review 复习思考题 R2.2.1 你能各举出一个现实生活中存在的与、或、非逻辑关系的事例吗？
  - `R2.2.2`: 第02章 逻辑代数基础 > review 复习思考题 R2.2.2 两个变量的异或运算和同或运算之间是什么关系？
  - `R2.3.1`: 第02章 逻辑代数基础 > review 复习思考题 R2.3.1 在逻辑代数的基本公式当中哪些公式的运算规则和普通代数的运算规则是相同的？哪些是不同的、需要特别记住的？
  - `R2.4.1`: 第02章 逻辑代数基础 > review 复习思考题 R2.4.1 代入定理中对代入逻辑式的形式和复杂程度有无限制？
  - `R2.4.2`: 第02章 逻辑代数基础 > review 复习思考题 R2.4.2 利用反演定理对给定逻辑式求反时,应如何处理变换的优先顺序和式中所有的非运算符号?
- **chapter_exercise** ×27
  - `题2.1`: [题 2.1] 试用列真值表的方法证明下列异或运算公式。  (1) $A \oplus 0 = A$ (2) $A \oplus 1 = A'$  (3) $A \oplus A = 0$ (4) $
  - `题2.10`: [题 2.10] 将下列各函数式化为最小项之和的形式。  (1) $Y = A^{\prime}BC + AC + B^{\prime}C$ (2) $Y = AB^{\prime}C^{\prime
  - `题2.11`: [题2.11] 将下列各式化为最大项之积的形式。  (1) $Y = (A + B)(A' + B' + C')$  (2) $Y = AB' + C$  ![](images/f15c574af5b
  - `题2.12`: [题 2.12] 利用逻辑代数的基本公式和常用公式化简下列各式。 (1) $ACD'+D'$ (2) $AB'(A+B)$ (3) $AB'+AC+BC$ (4) $AB(A+B'C)$ (5) $E
  - `题2.13`: [题 2.13] 用逻辑代数的基本公式和常用公式将下列逻辑函数化为最简与或形式。  (1) $Y = AB' + B + A'B$  (2) $Y = AB'C + A' + B + C'$  (3)

### 第03章

- **example** ×7
  - `例3.3.1`: 第03章 门电路 > review 复习思考题 > 三、动态功耗 【例 3.3.1】计算 CMOS 反相器的总功耗 $P_{TOT}$ 。已知电源电压 $V_{DD} = 5 \, V$ ，静态电源电
  - `例3.3.2`: 第03章 门电路 > review 复习思考题 > 二、漏极开路输出门电路（OD门） 【例 3.3.2】在图 3.3.35 所示的电路中，已知 $G_{1}$ 、 $G_{2}$ 、 $G_{3}$ 
  - `例3.4.1`: 第03章 门电路 > review 复习思考题 > 五、双极型三极管反相器的动态开关特性 【例 3.4.1】在图 3.4.8 所示的反相器电路中，已知 $V_{cc}=5\ V, R_{1}=4\ k
  - `例3.4.2`: 第03章 门电路 > review 复习思考题 > 二、输出特性 【例 3.4.2】在图 3.4.17 所示的电路中，试计算门 $G_{1}$ 最多可以驱动多少个同样的反相器电路。这些反相器的输入特性
  - `例3.4.3`: 第03章 门电路 > review 复习思考题 > 三、输入端负载特性 【例 3.4.3】在图 3.4.20 所示的电路中，为保证门 $G_{1}$ 输出的高、低电平能正确地传送到门【例 3.4.3】
- **review** ×24
  - `R3.2.1`: 第03章 门电路 > review 复习思考题 R3.2.1 为什么在图3.2.3中给出了三种不同形式的二极管等效电路？它们各适用于什么场合？ [图3.2.3(a)] 二极管伏安特性的几种近似方法 子
  - `R3.3.1`: 第03章 门电路 > review 复习思考题 R3.3.1 在什么条件下才可以将图 3.3.4 中的 MOS 管近似地看作一个理想开关？ [图3.3.4] MOS 管的基本开关电路 [图3.3.4描
  - `R3.3.10`: 第03章 门电路 > review 复习思考题 R3.3.10 能否将两个互补输出结构的普通 CMOS 门电路输出端并联,接成线与结构?
  - `R3.3.11`: 第03章 门电路 > review 复习思考题 R3.3.11 三态输出的缓冲器有哪些用途？
  - `R3.3.12`: 第03章 门电路 > review 复习思考题 R3.3.12 为防止 CMOS 电路中发生静电击穿, 应当注意哪些问题?
- **chapter_exercise** ×27
  - `题3.1`: [题 3.1] 在图 3.2.5 所示的正逻辑与门和图 3.2.6 所示的正逻辑或门电路中, 若改用负逻辑, 试列出它们的逻辑真值表, 并说明 Y 和 A、B 之间是什么逻辑关系。
  - `题3.10`: [题3.10] 图P3.10中的 $G_{1} \sim G_{4}$ 是OD输出结构的与非门74HC03，它们接成线与结构。试写出线与输出 $Y$ 与输入 $A_{1}, A_{2}, B_{1},
  - `题3.11`: [题 3.11] 指出图 P3.11 中各门电路的输出是什么状态（高电平、低电平或高阻态）。已知这些门电路都是 74 系列 TTL 电路。  ![](images/da6f612e4860620215
  - `题3.12`: [题 3.12] 说明图 P3.12 中各门电路的输出是高电平还是低电平。已知它们都是 74HC 系列的 CMOS 电路。  ![](images/b8a66f110071e9752e4e984003
  - `题3.13`: [题3.13] 试说明在下列情况下，用万用表测量图P3.13中的 $v_{12}$ 端得到的电压各为多少：  (1) $v_{11}$ 悬空；  (2) $v_{11}$ 接低电平(0.2 V);  

### 第04章

- **example** ×11
  - `例4.2.1`: 第04章 组合逻辑电路 > 4.2 组合逻辑电路的分析方法 【例 4.2.1】试分析图 4.2.1 所示电路的逻辑功能, 指出该电路的用途。 解：根据给出的逻辑图可写出 $Y_{2}, Y_{1}, 
  - `例4.3.1`: 第04章 组合逻辑电路 > 七、工艺设计 【例 4.3.1】 使用逻辑门电路设计一个监视交通信号灯工作状态的逻辑电路。每一组信号灯均由红、黄、绿三盏灯组成，如图 4.3.2 所示。正常工作情况下，任何
  - `例4.5.1`: 第04章 组合逻辑电路 > 4.5 层次化和模块化的设计方法 【例 4.5.1】试用 4.4 节中介绍的 8 线 -3 线优先编码器 74HC148 接成 16 线 -4 线优先编码器，将 $A_{0
  - `例4.5.2`: 第04章 组合逻辑电路 > 4.5 层次化和模块化的设计方法 【例 4.5.2】试用 3 线-8 线译码器 74HC138 组成 4 线-16 线译码器，将输入的 4 位二进制代码 $D_{3}D_{
  - `例4.5.3`: 第04章 组合逻辑电路 > 4.5 层次化和模块化的设计方法 【例 4.5.3】试用两片 74HC85 组成一个 8 位数值比较器。 解：根据多位数比较的规则，在高位相等时取决于低位的比较结果。因此只
- **review** ×13
  - `R4.3.1`: 第04章 组合逻辑电路 > review 复习思考题 R4.3.1 什么是“逻辑抽象”？它包含哪些内容？
  - `R4.3.2`: 第04章 组合逻辑电路 > review 复习思考题 R4.3.2 对于同一个实际的逻辑问题,两个同学经过逻辑抽象得到的逻辑函数不完全相同,这是为什么?
  - `R4.4.1`: 第04章 组合逻辑电路 > review 复习思考题 R4.4.1 在需要使用普通编码器的场合能否用优先编码器取代普通编码器？在需要使用优先编码器的场合能否用普通编码器取代优先编码器？
  - `R4.4.2`: 第04章 组合逻辑电路 > review 复习思考题 R4.4.2 用二-十进制译码器(如图 4.4.9 所示的结构形式)附加门电路能否得到任何形式的四变量逻辑函数？为什么？ [图4.4.9(a)] 
  - `R4.4.3`: 第04章 组合逻辑电路 > review 复习思考题 R4.4.3 用4线-16线译码器（输入为 $A_{3}, A_{2}, A_{1}, A_{0}$ ，输出为 $Y_{0}^{\prime} \
- **chapter_exercise** ×36
  - `题4.1`: [题 4.1] 分析图 P4.1 电路的逻辑功能, 写出输出的逻辑函数式, 列出真值表, 说明电路逻辑功能的特点。  ![](images/4ad6d532432392be3aa646846573be
  - `题4.10`: [题4.10] 写出图P4.10中 $Z_{1}, Z_{2}, Z_{3}$ 的逻辑函数式，并化简为最简的与或表达式。译码器74HC42的逻辑图见图4.4.9。
  - `题4.11`: [题 4.11] 画出用两片 4 线-16 线译码器 74LS154 组成 5 线-32 线译码器的接线图。图 P4.11 是 74LS154 的逻辑框图，图中的 $S_{A}^{\prime}$ 、
  - `题4.12`: [题 4.12] 试画出用 3 线 -8 线译码器 74HC138（见图 4.4.7）和门电路产生如下多输出逻辑函数的逻辑图。  $$ \left\{ \begin{array}{l} Y _ {1}
  - `题4.13`: [题 4.13] 画出用 4 线-16 线译码器 74LS154(参见题 4.11) 和门电路产生如下多输出逻辑函数的逻辑图。  $$ \left\{ \begin{array}{l} Y _ {1}

### 第05章

- **example** ×9
  - `例5.2.1`: 第05章 半导体存储电路 > 第五章半导体存储电路 > 5.2 SR 锁存器 【例 5.2.1】在图 5.2.3(a) 所示的 SR 锁存器电路中，已知 $S_{D}^{\prime}$ 和 $R_{
  - `例5.3.1`: 第05章 半导体存储电路 > 第五章半导体存储电路 > 二、电平触发方式的动作特点 【例 5.3.1】已知电平触发 SR 触发器的输入信号波形如图 5.3.3 所示，试画出 Q、 $Q'$ 端的电压波
  - `例5.3.2`: 第05章 半导体存储电路 > 第五章半导体存储电路 > 二、电平触发方式的动作特点 【例 5.3.2】若图 5.3.5 所示电平触发 D 触发器的 CLK 和输入端 D 的电压波形如图 5.3.6 中
  - `例5.3.3`: 第05章 半导体存储电路 > 第五章半导体存储电路 > 一、电路结构和工作原理 【例 5.3.3】在图 5.3.7 所示的边沿触发器电路中, 若 D 端和 CLK 的电压波形如图 5.3.9 所示,试
  - `例5.3.4`: 第05章 半导体存储电路 > 第五章半导体存储电路 > 一、电路结构和工作原理 【例 5.3.4】在图 5.3.10(a) 的正脉冲触发 SR 触发器中, 若 CLK、S 和 R 的电压波形如图 5.
- **review** ×19
  - `R5.2.1`: 第05章 半导体存储电路 > 第五章半导体存储电路 > review 复习思考题 R5.2.1 为什么 $SR$ 锁存器的输入信号需要遵守 $SR = 0$ 的约束条件？
  - `R5.3.1`: 第05章 半导体存储电路 > 第五章半导体存储电路 > review 复习思考题 R5.3.1 为什么电平触发 $SR$ 触发器也应当遵守 $SR = 0$ 的约束条件？在什么情况下会发生触发器的次态
  - `R5.3.2`: 第05章 半导体存储电路 > 第五章半导体存储电路 > review 复习思考题 R5.3.2 边沿触发的动作特点和电平触发的动作特点有何不同？
  - `R5.3.3`: 第05章 半导体存储电路 > 第五章半导体存储电路 > review 复习思考题 R5.3.3 脉冲触发方式有哪些动作特点？它和电平触发方式、边沿触发方式有何不同？
  - `R5.3.4`: 第05章 半导体存储电路 > 第五章半导体存储电路 > review 复习思考题 R5.3.4 脉冲触发 JK 触发器和脉冲触发 SR 触发器在逻辑功能上有什么区别？用 JK 触发器代替 SR 触发器
- **chapter_exercise** ×40
  - `题5.1`: [题 5.1] 画出图 P5.1 由与非门组成的 SR 锁存器输出端 Q、 $Q'$ 的电压波形，输入端 $S_{D}^{\prime}$ 、 $R_{D}^{\prime}$ 的电压波形如图中所示。
  - `题5.10`: [题 5.10] 若脉冲触发 SR 触发器各输入端的电压波形如图 P5.10 中所给出，试画出 Q、 $Q'$ 端对应的电压波形。设触发器的初始状态为 Q=0。  ![](images/fae64ab
  - `题5.11`: [题 5.11] 在脉冲触发 SR 触发器电路中, 若 S、R、CLK 端的电压波形如图 P5.11 中所示, 试画出 Q、Q' 端对应的电压波形。假定触发器的初始状态为 Q = 0。  ![](im
  - `题5.12`: [题 5.12] 在脉冲触发 JK 触发器中, 已知 J、K、CLK 端的电压波形如图 P5.12 中所示, 试画出 Q、Q' 端对应的电压波形。设触发器的初始状态为 Q = 0。  ![](imag
  - `题5.13`: [题 5.13] 已知脉冲触发 JK 触发器输入端 J、K 和 CLK 的电压波形如图 P5.13 中所示，试画出 Q、 $Q'$ 端对应的电压波形。设触发器的初始状态为 Q=0。  ![](imag

### 第06章

- **example** ×18
  - `例6.2.1`: 第06章 时序逻辑电路 > 6.2.1 同步时序逻辑电路的分析方法 【例 6.2.1】试分析图 6.2.1 所示时序逻辑电路的逻辑功能, 写出它的驱动方程、状态方程和输出方程。 $FF_{1}$ 、 
  - `例6.2.2`: 第06章 时序逻辑电路 > 一、状态转换表 【例 6.2.2】试列出图 6.2.1 所示电路的状态转换表。 解：由图6.2.1可见，这个电路没有输入逻辑变量。（需要注意的是，不要把CLK当作输入逻辑变
  - `例6.2.3`: 第06章 时序逻辑电路 > 二、状态转换图 【例 6.2.3】分析图 6.2.3 所示时序逻辑电路的逻辑功能, 写出电路的驱动方程、状态方程和输出方程, 画出电路的状态转换图。 解：首先从给定的电路图
  - `例6.2.4`: 第06章 时序逻辑电路 > *6.2.3 异步时序逻辑电路的分析方法 【例 6.2.4】已知异步时序电路的逻辑图如图 6.2.10 所示,试分析它的逻辑功能,画出电路的状态转换图和时序图。触发器和门电
  - `例6.3.1`: 第06章 时序逻辑电路 > 6.3.1 移位寄存器 【例 6.3.1】试分析图 6.3.6 所示电路的逻辑功能，并指出在图 6.3.7 所示的时钟信号及 $S_{1}, S_{0}$ 状态作用下， $
- **review** ×12
  - `R6.1.1`: 第06章 时序逻辑电路 > review 复习思考题 R6.1.1 组合逻辑电路和时序逻辑电路在逻辑功能与电路结构上有何区别？
  - `R6.1.2`: 第06章 时序逻辑电路 > review 复习思考题 R6.1.2 同步时序电路和异步时序电路有何不同？
  - `R6.2.1`: 第06章 时序逻辑电路 > review 复习思考题 R6.2.1 时序电路逻辑功能的描述方式有哪几种？你能将其中任何一种描述方式转换为其他各种描述方式吗？
  - `R6.3.1`: 第06章 时序逻辑电路 > review 复习思考题 R6.3.1 用电平触发的触发器、脉冲触发的触发器是否也能组成图 6.3.1 形式的移位寄存器？ [图6.3.1] 用 D 触发器构成的移位寄存器
  - `R6.3.2`: 第06章 时序逻辑电路 > review 复习思考题 R6.3.2 在图 6.3.6 所示的加法运算电路中,为了保证得出正确的运算结果,对 M 和 N 的数值应作何限制? [图6.3.6] 例6.3.
- **chapter_exercise** ×35
  - `题6.1`: [题 6.1] 分析图 P6.1 时序电路的逻辑功能, 写出电路的驱动方程、状态方程和输出方程, 画出电路的状态转换图和时序图。  ![](images/7c86340b1de2ccacf03df68
  - `题6.10`: [题 6.10] 在图 P6.10 电路中, 若两个移位寄存器中的原始数据分别为 $A_{3}A_{2}A_{1}A_{0}=1001$ , $B_{3}B_{2}B_{1}B_{0}=0011$ ,
  - `题6.11`: [题 6.11] 分析图 P6.11 的计数器电路,说明这是多少进制的计数器。十进制计数器 74160 的功能表与表 6.3.4 相同。
  - `题6.12`: [题 6.12] 分析图 P6.12 的计数器电路, 画出电路的状态转换图, 说明这是多少进制的计数器。十六进制计数器 74LS161 的功能表如表 6.3.4 所示。  ![](images/2e0
  - `题6.13`: [题6.13] 试分析图P6.13的计数器在 $M = 1$ 和 $M = 0$ 时各为几进制。74160的功能表与表6.3.4相同。

### 第07章

- **example** ×5
  - `例7.2.1`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > 7.2.2 用门电路组成的施密特触发电路 【例 7.2.1】在图 7.2.5(a) 电路中, 如果要求 $V_{T+}=7.
  - `例7.4.1`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > 7.4.1 对称式多谐振荡电路 【例 7.4.1】在图 7.4.1 所示的对称式多谐振荡电路中，已知 $R_{F1}=R_{
  - `例7.4.2`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > 7.4.2 非对称式多谐振荡电路 【例 7.4.2】 在图 7.4.6 所示的非对称式多谐 振荡电路中，已知 $G_{1}$
  - `例7.4.3`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > 7.4.4 用施密特触发电路构成的多谐振荡电路 【例 7.4.3】已知图 7.4.15 电路中的施密特触发电路为 CMOS 
  - `例7.5.1`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > 7.5.4 用 555 定时器接成的多谐振荡电路 【例 7.5.1】试用 NE555 定时器设计一个多谐振荡电路, 要求振荡
- **review** ×13
  - `R7.2.1`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > review 复习思考题 R7.2.1 能否用施密特触发电路存储 1 位二值代码？为什么？
  - `R7.2.2`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > review 复习思考题 R7.2.2 在图 7.2.5 所示的施密特触发电路中,为什么要求 $R_{1}<R_{2}$ ?
  - `R7.2.3`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > review 复习思考题 R7.2.3 反相输出的施密特触发电路的电压传输特性和普通反相器的电压传输特性有什么不同？
  - `R7.3.1`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > review 复习思考题 R7.3.1 单稳态电路输出脉冲的宽度(即暂稳态持续时间)由哪些因素决定?与触发脉冲的宽度和幅度有
  - `R7.3.2`: 第07章 脉冲波形的产生和整形电路 > 第七章脉冲波形的产生和整形电路 > review 复习思考题 R7.3.2 比较一下图 7.3.1 的微分型单稳态电路和图 7.3.5 的积分型单稳态电路, 它
- **chapter_exercise** ×27
  - `题7.1`: [题 7.1] 若反相输出的施密特触发电路输入信号波形如图 P7.1 所示，试画出输出信号的波形。施密特触发电路的转换电平 $V_{T+}$ 、 $V_{T-}$ 已在输入信号波形图上标出。  ![]
  - `题7.10`: [题7.10] 在图P7.9所示的微分型单稳态电路中，若 $\mathrm{G}_1$ 和 $\mathrm{G}_2$ 为74系列TTL门电路，它们的 $V_{\mathrm{OH}} = 3.2\
  - `题7.11`: [题7.11] 图P7.11是用两个集成单稳态电路74121所组成的脉冲变换电路，外接电阻和外接电容的参数如图中所示。试计算在输入触发信号 $v_{1}$ 作用下 $v_{01}, v_{02}$ 输
  - `题7.12`: [题7.12] 在图7.4.1所示的对称式多谐振荡电路中，若 $R_{\mathrm{F1}} = R_{\mathrm{F2}} = 1\mathrm{k}\Omega ,C_1 = C_2 = 0
  - `题7.13`: [题7.13] 图P7.13是用CMOS反相器组成的对称式多谐振荡电路，若 $R_{\mathrm{F1}} = R_{\mathrm{F2}} = 10\mathrm{k}\Omega ,C_1 =

### 第08章

- **example** ×4
  - `例8.3.1`: 第08章 数模和模数转换 > 数-模和模-数转换 > 8.3.1 D/A转换器的转换精度 【例 8.3.1】在图 8.2.5 所示的倒 T 形电阻网络 D/A 转换器中，外接参考电压 $V_{REF}
  - `例8.6.1`: 第08章 数模和模数转换 > review 复习思考题 > 8.6.6 V-F 变换型 A/D 转换器 【例 8.6.1】在图 8.6.17 所示用 AD650 接成的 V-F 变换器电路中，给定 $
  - `例8.6.2`: 第08章 数模和模数转换 > review 复习思考题 > 8.6.6 V-F 变换型 A/D 转换器 【例 8.6.2】在图 8.6.18 所示的电路中，已知 $R_{T}=10\ k\Omega,
  - `例8.6.3`: 第08章 数模和模数转换 > review 复习思考题 > 8.6.6 V-F 变换型 A/D 转换器 【例 8.6.3】在图 8.6.15 所示的 V-F 变换型 A/D 转换器电路中，若计数器和寄
- **review** ×11
  - `R8.2.1`: 第08章 数模和模数转换 > review 复习思考题 R8.2.1 D/A 转换器的电路结构有哪些类型？它们各有何优、缺点？
  - `R8.2.2`: 第08章 数模和模数转换 > review 复习思考题 R8.2.2 在图 8.2.3 所示的倒 T 形电阻网络 D/A 转换器中, 用哪些方法可以调节输出电压 $v_{0}$ 的最大幅度? [图8.
  - `R8.2.3`: 第08章 数模和模数转换 > review 复习思考题 R8.2.3 如果将图 8.2.3 电路改成具有双极性输出的 D/A 转换器, 电路应如何连接? [图8.2.3] 倒 T 形电阻网络 D/A 
  - `R8.3.1`: 第08章 数模和模数转换 > review 复习思考题 R8.3.1 D/A转换器的转换精度是怎样表述的？
  - `R8.3.2`: 第08章 数模和模数转换 > review 复习思考题 R8.3.2 若 D/A 转换器输入数字量的有效位数为 12 位, 参考电压 $V_{REF}$ 为 12 V, 理论上输出电压的误差最大值是多
- **chapter_exercise** ×20
  - `题8.1`: [题 8.1] 在图 8.2.1 所示的权电阻网络 D/A 转换器中, 若取 $V_{REF} = 5 \, V$ , 试求当输入数字量为 $d_{3}d_{2}d_{1}d_{0} = 0101$ 
  - `题8.10`: [题 8.10] 设计一个波形发生器电路,要求产生图 P8.10 所给定的电压波形。  ![](images/5ca37edfe4c37854ad1ac90f58a4cc28c52176ed9d4d0
  - `题8.11`: [题8.11] 图P8.11所示电路是用D/A转换器AD7520和运算放大器构成的增益可编程放大器，它的电压放大倍数 $A_{v} = \frac{v_{0}}{v_{1}}$ 由输入的数字量 $D(
  - `题8.12`: [题8.12] 图P8.12电路是用D/A转换器AD7520和运算放大器组成的增益可编程放大器，它的电压放大倍数 $A_{\mathrm{v}} = \frac{v_0}{v_1}$ 由输入的数字量 
  - `题8.13`: [题8.13] 在图P8.13所示的D/A转换器中，已知输入为8位二进制数码，接在AD7520的高8位输入端上， $V_{\mathrm{REF}} = 10\mathrm{V}$ 。为保证 $V_{

## Concept 候选（按章，high/medium 优先）

### 第01章

- [high] **二进制算术运算的特点**  `concept_ch01_二进制算术运算的特点`  section=1.4.1  sources=section_title
- [high] **反码、补码和补码运算**  `concept_ch01_反码_补码和补码运算`  section=1.4.2  sources=section_title
- [low] **不同数制间的转换**  `concept_ch01_不同数制间的转换`  section=—  sources=guide_enum_title
- [low] **二-十六转换**  `concept_ch01_二_十六转换`  section=—  sources=guide_enum_title
- [low] **二-十转换**  `concept_ch01_二_十转换`  section=—  sources=guide_enum_title
- [low] **二进制**  `concept_ch01_二进制`  section=—  sources=guide_enum_title
- [low] **二进制数的补码运算**  `concept_ch01_二进制数的补码运算`  section=—  sources=guide_enum_title
- [low] **八进制**  `concept_ch01_八进制`  section=—  sources=guide_enum_title
- [low] **八进制数与二进制数的转换**  `concept_ch01_八进制数与二进制数的转换`  section=—  sources=guide_enum_title
- [low] **十-二转换**  `concept_ch01_十_二转换`  section=—  sources=guide_enum_title
- [low] **十六-二转换**  `concept_ch01_十六_二转换`  section=—  sources=guide_enum_title
- [low] **十六进制**  `concept_ch01_十六进制`  section=—  sources=guide_enum_title
- [low] **十六进制数与十进制数的转换**  `concept_ch01_十六进制数与十进制数的转换`  section=—  sources=guide_enum_title
- [low] **十进制**  `concept_ch01_十进制`  section=—  sources=guide_enum_title
- [low] **十进制代码**  `concept_ch01_十进制代码`  section=—  sources=guide_enum_title
- [low] **原码、反码、补码之间的转换**  `concept_ch01_原码_反码_补码之间的转换`  section=—  sources=guide_enum_title
- [low] **格雷码**  `concept_ch01_格雷码`  section=—  sources=guide_enum_title
- [low] **美国信息交换标准代码(ASCII)**  `concept_ch01_美国信息交换标准代码_ASCII_`  section=—  sources=guide_enum_title

### 第02章

- [high] **代入定理**  `concept_ch02_代入定理`  section=2.4.1  sources=section_title
- [high] **公式化简法**  `concept_ch02_公式化简法`  section=2.6.1  sources=section_title
- [high] **卡诺图化简法**  `concept_ch02_卡诺图化简法`  section=2.6.2  sources=section_title
- [high] **反演定理**  `concept_ch02_反演定理`  section=2.4.2  sources=section_title
- [high] **基本公式**  `concept_ch02_基本公式`  section=2.3.1  sources=section_title
- [high] **多输出逻辑函数的化简**  `concept_ch02_多输出逻辑函数的化简`  section=2.8  sources=section_title
- [high] **奎恩-麦克拉斯基化简法 (Q-M 法)**  `concept_ch02_奎恩_麦克拉斯基化简法_Q_M_法_`  section=2.6.3  sources=section_title
- [high] **对偶定理**  `concept_ch02_对偶定理`  section=2.4.3  sources=section_title
- [high] **无关项在化简逻辑函数中的应用**  `concept_ch02_无关项在化简逻辑函数中的应用`  section=2.7.2  sources=section_title
- [high] **约束项、任意项和逻辑函数式中的无关项**  `concept_ch02_约束项_任意项和逻辑函数式中的无关项`  section=2.7.1  sources=section_title
- [high] **若干常用公式**  `concept_ch02_若干常用公式`  section=2.3.2  sources=section_title
- [high] **逻辑代数中的三种基本运算**  `concept_ch02_逻辑代数中的三种基本运算`  section=2.2  sources=section_title
- [high] **逻辑函数**  `concept_ch02_逻辑函数`  section=2.5.1  sources=section_title
- [high] **逻辑函数形式的变换**  `concept_ch02_逻辑函数形式的变换`  section=2.9  sources=section_title
- [high] **逻辑函数的两种标准形式**  `concept_ch02_逻辑函数的两种标准形式`  section=2.5.3  sources=section_title
- [high] **逻辑函数的描述方法**  `concept_ch02_逻辑函数的描述方法`  section=2.5.2  sources=section_title
- [medium] **与或形式 $\Rightarrow$ 与或非形式**  `concept_ch02_与或形式_Rightarrow_与或非形式`  section=2  sources=section_title
- [medium] **卡诺图化简法的步骤**  `concept_ch02_卡诺图化简法的步骤`  section=2  sources=section_title
- [low] *** 2. 最大项**  `concept_ch02__2_最大项`  section=—  sources=breadcrumb_tail
- [low] *** 三、逻辑函数的最大项之积形式**  `concept_ch02__三_逻辑函数的最大项之积形式`  section=—  sources=breadcrumb_tail
- [low] **【例2-3-5】给定逻辑函数式为**  `concept_ch02__例2_3_5_给定逻辑函数式为`  section=—  sources=breadcrumb_tail
- [low] **【例2.7.1】化简具有约束的逻辑函数**  `concept_ch02__例2_7_1_化简具有约束的逻辑函数`  section=—  sources=breadcrumb_tail
- [low] **各种描述方法间的相互转换**  `concept_ch02_各种描述方法间的相互转换`  section=—  sources=guide_enum_title
- [low] **吸收法**  `concept_ch02_吸收法`  section=—  sources=guide_enum_title
- [low] **并项法**  `concept_ch02_并项法`  section=—  sources=guide_enum_title
- [low] **最小项和最大项**  `concept_ch02_最小项和最大项`  section=—  sources=guide_enum_title
- [low] **波形图**  `concept_ch02_波形图`  section=—  sources=guide_enum_title
- [low] **消因子法**  `concept_ch02_消因子法`  section=—  sources=guide_enum_title
- [low] **消项法**  `concept_ch02_消项法`  section=—  sources=guide_enum_title
- [low] **用卡诺图化简逻辑函数**  `concept_ch02_用卡诺图化简逻辑函数`  section=—  sources=guide_enum_title
- [low] **逻辑函数不同描述方法之间的转换**  `concept_ch02_逻辑函数不同描述方法之间的转换`  section=—  sources=guide_enum_title
- [low] **逻辑函数式**  `concept_ch02_逻辑函数式`  section=—  sources=guide_enum_title
- [low] **逻辑函数式的变换**  `concept_ch02_逻辑函数式的变换`  section=—  sources=guide_enum_title
- [low] **逻辑函数的化简**  `concept_ch02_逻辑函数的化简`  section=—  sources=guide_enum_title
- [low] **逻辑函数的卡诺图表示法**  `concept_ch02_逻辑函数的卡诺图表示法`  section=—  sources=guide_enum_title
- [low] **逻辑函数的最小项之和形式**  `concept_ch02_逻辑函数的最小项之和形式`  section=—  sources=guide_enum_title
- [low] **逻辑图**  `concept_ch02_逻辑图`  section=—  sources=guide_enum_title
- [low] **逻辑真值表**  `concept_ch02_逻辑真值表`  section=—  sources=guide_enum_title
- [low] **逻辑等式的证明**  `concept_ch02_逻辑等式的证明`  section=—  sources=guide_enum_title
- [low] **配项法**  `concept_ch02_配项法`  section=—  sources=guide_enum_title
- [low] **（3）选择化简后保留的乘积项。选取的原则是**  `concept_ch02__3_选择化简后保留的乘积项_选取的原则是`  section=—  sources=breadcrumb_tail

### 第03章

- [high] **Bi-CMOS 电路**  `concept_ch03_Bi_CMOS_电路`  section=3.6  sources=section_title
- [high] **Bi-CMOS 电路的基本结构和工作原理**  `concept_ch03_Bi_CMOS_电路的基本结构和工作原理`  section=3.6.1  sources=section_title
- [high] **Bi-CMOS 集成电路的各种系列**  `concept_ch03_Bi_CMOS_集成电路的各种系列`  section=3.6.2  sources=section_title
- [high] **CMOS 反相器的电路结构和工作原理**  `concept_ch03_CMOS_反相器的电路结构和工作原理`  section=3.3.2  sources=section_title
- [high] **CMOS 反相器的静态输入特性和输出特性**  `concept_ch03_CMOS_反相器的静态输入特性和输出特性`  section=3.3.3  sources=section_title
- [high] **CMOS 电路和 TTL 电路的接口**  `concept_ch03_CMOS_电路和_TTL_电路的接口`  section=3.7.1  sources=section_title
- [high] **CMOS反相器的动态特性**  `concept_ch03_CMOS反相器的动态特性`  section=3.3.4  sources=section_title
- [high] **CMOS数字集成电路的各种系列**  `concept_ch03_CMOS数字集成电路的各种系列`  section=3.3.7  sources=section_title
- [high] **ECL 电路的基本结构和工作原理**  `concept_ch03_ECL_电路的基本结构和工作原理`  section=3.5.1  sources=section_title
- [high] **ECL 集成电路**  `concept_ch03_ECL_集成电路`  section=3.5  sources=section_title
- [high] **ECL 集成电路的各种系列**  `concept_ch03_ECL_集成电路的各种系列`  section=3.5.2  sources=section_title
- [high] **MOS 管的开关特性**  `concept_ch03_MOS_管的开关特性`  section=3.3.1  sources=section_title
- [high] **TTL数字集成电路的各种系列**  `concept_ch03_TTL数字集成电路的各种系列`  section=3.4.6  sources=section_title
- [high] **不同类型数字集成电路间的接口**  `concept_ch03_不同类型数字集成电路间的接口`  section=3.7  sources=section_title
- [high] **不同逻辑电平电路间的接口**  `concept_ch03_不同逻辑电平电路间的接口`  section=3.7.2  sources=section_title
- [high] **二极管与门**  `concept_ch03_二极管与门`  section=3.2.2  sources=section_title
- [high] **二极管或门**  `concept_ch03_二极管或门`  section=3.2.3  sources=section_title
- [high] **半导体二极管的开关特性**  `concept_ch03_半导体二极管的开关特性`  section=3.2.1  sources=section_title
- [high] **双极型三极管的开关特性**  `concept_ch03_双极型三极管的开关特性`  section=3.4.1  sources=section_title
- [medium] **/14000 系列**  `concept_ch03__14000_系列`  section=4000  sources=section_title
- [medium] **ALVT 系列**  `concept_ch03_ALVT_系列`  section=74  sources=section_title
- [medium] **三极管接口电路的电路参数计算**  `concept_ch03_三极管接口电路的电路参数计算`  section=3  sources=section_title
- [medium] **与或非门**  `concept_ch03_与或非门`  section=3  sources=section_title
- [low] *** 三、CMOS 电路锁定效应的防护**  `concept_ch03__三_CMOS_电路锁定效应的防护`  section=—  sources=breadcrumb_tail
- [low] **CMOS 反相器的电路结构**  `concept_ch03_CMOS_反相器的电路结构`  section=—  sources=guide_enum_title
- [low] **CMOS传输门**  `concept_ch03_CMOS传输门`  section=—  sources=guide_enum_title
- [low] **CMOS门电路**  `concept_ch03_CMOS门电路`  section=—  sources=guide_enum_title
- [low] **MECL 10K 系列**  `concept_ch03_MECL_10K_系列`  section=—  sources=breadcrumb_tail
- [low] **MECL 10KH 及 MECL 100K 系列**  `concept_ch03_MECL_10KH_及_MECL_100K_系列`  section=—  sources=breadcrumb_tail
- [low] **MECLⅢ系列**  `concept_ch03_MECLⅢ系列`  section=—  sources=breadcrumb_tail
- [low] **MOS 管的开关等效电路**  `concept_ch03_MOS_管的开关等效电路`  section=—  sources=guide_enum_title
- [low] **MOS 管的结构和工作原理**  `concept_ch03_MOS_管的结构和工作原理`  section=—  sources=guide_enum_title
- [low] **MOS 管的输入特性和输出特性**  `concept_ch03_MOS_管的输入特性和输出特性`  section=—  sources=guide_enum_title
- [low] **MOS管的四种类型**  `concept_ch03_MOS管的四种类型`  section=—  sources=guide_enum_title
- [low] **MOS管的基本开关电路**  `concept_ch03_MOS管的基本开关电路`  section=—  sources=guide_enum_title
- [low] **OC 门和 OD 门外接上拉电阻阻值的计算**  `concept_ch03_OC_门和_OD_门外接上拉电阻阻值的计算`  section=—  sources=guide_enum_title
- [low] **TTL门电路**  `concept_ch03_TTL门电路`  section=—  sources=guide_enum_title
- [low] **三态输出的 CMOS 门电路**  `concept_ch03_三态输出的_CMOS_门电路`  section=—  sources=guide_enum_title
- [low] **三态输出门电路(TS门)**  `concept_ch03_三态输出门电路_TS门_`  section=—  sources=guide_enum_title
- [low] **三极管反相器的开关等效电路**  `concept_ch03_三极管反相器的开关等效电路`  section=—  sources=guide_enum_title
- [low] **交流噪声容限**  `concept_ch03_交流噪声容限`  section=—  sources=guide_enum_title
- [low] **传输延迟时间**  `concept_ch03_传输延迟时间`  section=—  sources=guide_enum_title
- [low] **其他逻辑功能的门电路**  `concept_ch03_其他逻辑功能的门电路`  section=—  sources=guide_enum_title
- [low] **动态功耗**  `concept_ch03_动态功耗`  section=—  sources=guide_enum_title
- [low] **半导体二极管和三极管的开关特性**  `concept_ch03_半导体二极管和三极管的开关特性`  section=—  sources=guide_enum_title
- [low] **双极型三极管反相器的动态开关特性**  `concept_ch03_双极型三极管反相器的动态开关特性`  section=—  sources=guide_enum_title
- [low] **双极型三极管工作状态的计算**  `concept_ch03_双极型三极管工作状态的计算`  section=—  sources=guide_enum_title
- [low] **双极型三极管的基本开关电路——三极管反相器**  `concept_ch03_双极型三极管的基本开关电路_三极管反相器`  section=—  sources=guide_enum_title
- [low] **双极型三极管的结构**  `concept_ch03_双极型三极管的结构`  section=—  sources=guide_enum_title
- [low] **双极型三极管的输入特性和输出特性**  `concept_ch03_双极型三极管的输入特性和输出特性`  section=—  sources=guide_enum_title
- [low] **各种逻辑功能的 CMOS 门电路**  `concept_ch03_各种逻辑功能的_CMOS_门电路`  section=—  sources=guide_enum_title
- [low] **扇出**  `concept_ch03_扇出`  section=—  sources=guide_enum_title
- [low] **漏极开路输出门电路（OD门）**  `concept_ch03_漏极开路输出门电路_OD门_`  section=—  sources=guide_enum_title
- [low] **用 CMOS 电路驱动 TTL 电路**  `concept_ch03_用_CMOS_电路驱动_TTL_电路`  section=—  sources=guide_enum_title
- [low] **用TTL电路驱动CMOS电路**  `concept_ch03_用TTL电路驱动CMOS电路`  section=—  sources=guide_enum_title
- [low] **电压传输特性**  `concept_ch03_电压传输特性`  section=—  sources=guide_enum_title
- [low] **电压传输特性和电流传输特性**  `concept_ch03_电压传输特性和电流传输特性`  section=—  sources=guide_enum_title
- [low] **电源的动态尖峰电流**  `concept_ch03_电源的动态尖峰电流`  section=—  sources=guide_enum_title
- [low] **电路结构**  `concept_ch03_电路结构`  section=—  sources=guide_enum_title
- [low] **输入特性**  `concept_ch03_输入特性`  section=—  sources=guide_enum_title
- [low] **输入特性和输出特性的应用**  `concept_ch03_输入特性和输出特性的应用`  section=—  sources=guide_enum_title
- [low] **输入电路的过流保护**  `concept_ch03_输入电路的过流保护`  section=—  sources=guide_enum_title
- [low] **输入电路的静电防护**  `concept_ch03_输入电路的静电防护`  section=—  sources=guide_enum_title
- [low] **输入端噪声容限**  `concept_ch03_输入端噪声容限`  section=—  sources=guide_enum_title
- [low] **输入端负载特性**  `concept_ch03_输入端负载特性`  section=—  sources=guide_enum_title
- [low] **输出特性**  `concept_ch03_输出特性`  section=—  sources=guide_enum_title
- [low] **集成门电路逻辑功能的分析**  `concept_ch03_集成门电路逻辑功能的分析`  section=—  sources=guide_enum_title
- [low] **集电极开路输出的门电路(OC门)**  `concept_ch03_集电极开路输出的门电路_OC门_`  section=—  sources=guide_enum_title

### 第04章

- [high] **加法器**  `concept_ch04_加法器`  section=4.4.4  sources=section_title
- [high] **可编程逻辑器件**  `concept_ch04_可编程逻辑器件`  section=4.6  sources=section_title
- [high] **层次化和模块化的设计方法**  `concept_ch04_层次化和模块化的设计方法`  section=4.5  sources=section_title
- [high] **数值比较器**  `concept_ch04_数值比较器`  section=4.4.5  sources=section_title
- [high] **数据选择器**  `concept_ch04_数据选择器`  section=4.4.3  sources=section_title
- [high] **检查竞争-冒险现象的方法**  `concept_ch04_检查竞争_冒险现象的方法`  section=4.9.2  sources=section_title
- [high] **用可编程通用模块设计组合逻辑电路**  `concept_ch04_用可编程通用模块设计组合逻辑电路`  section=4.8  sources=section_title
- [high] **硬件描述语言**  `concept_ch04_硬件描述语言`  section=4.7  sources=section_title
- [high] **竞争-冒险现象及其成因**  `concept_ch04_竞争_冒险现象及其成因`  section=4.9.1  sources=section_title
- [high] **组合逻辑电路的分析方法**  `concept_ch04_组合逻辑电路的分析方法`  section=4.2  sources=section_title
- [high] **组合逻辑电路的基本设计方法**  `concept_ch04_组合逻辑电路的基本设计方法`  section=4.3  sources=section_title
- [high] **编码器**  `concept_ch04_编码器`  section=4.4.1  sources=section_title
- [high] **若干常用的组合逻辑电路模块**  `concept_ch04_若干常用的组合逻辑电路模块`  section=4.4  sources=section_title
- [high] **译码器**  `concept_ch04_译码器`  section=4.4.2  sources=section_title
- [medium] **数值比较器的应用**  `concept_ch04_数值比较器的应用`  section=4  sources=section_title
- [low] **1位加法器**  `concept_ch04_1位加法器`  section=—  sources=guide_enum_title
- [low] **1位数值比较器**  `concept_ch04_1位数值比较器`  section=—  sources=guide_enum_title
- [low] **二-十进制译码器**  `concept_ch04_二_十进制译码器`  section=—  sources=guide_enum_title
- [low] **二进制译码器**  `concept_ch04_二进制译码器`  section=—  sources=guide_enum_title
- [low] **优先编码器**  `concept_ch04_优先编码器`  section=—  sources=guide_enum_title
- [low] **修改逻辑设计**  `concept_ch04_修改逻辑设计`  section=—  sources=guide_enum_title
- [low] **写出逻辑函数式**  `concept_ch04_写出逻辑函数式`  section=—  sources=guide_enum_title
- [low] **分析用中规模集成常用组合逻辑电路组成的组合逻辑电路**  `concept_ch04_分析用中规模集成常用组合逻辑电路组成的组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **分析用小规模集成门电路组成的组合逻辑电路**  `concept_ch04_分析用小规模集成门电路组成的组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **基本程序结构**  `concept_ch04_基本程序结构`  section=—  sources=guide_enum_title
- [low] **多位加法器**  `concept_ch04_多位加法器`  section=—  sources=guide_enum_title
- [low] **多位数值比较器**  `concept_ch04_多位数值比较器`  section=—  sources=guide_enum_title
- [low] **将逻辑函数化简或转换成适当的描述形式**  `concept_ch04_将逻辑函数化简或转换成适当的描述形式`  section=—  sources=guide_enum_title
- [low] **工艺设计**  `concept_ch04_工艺设计`  section=—  sources=guide_enum_title
- [low] **引入选通脉冲**  `concept_ch04_引入选通脉冲`  section=—  sources=guide_enum_title
- [low] **接入滤波电容**  `concept_ch04_接入滤波电容`  section=—  sources=guide_enum_title
- [low] **描述组合逻辑电路的实例**  `concept_ch04_描述组合逻辑电路的实例`  section=—  sources=guide_enum_title
- [low] **显示译码器**  `concept_ch04_显示译码器`  section=—  sources=guide_enum_title
- [low] **普通编码器**  `concept_ch04_普通编码器`  section=—  sources=guide_enum_title
- [low] **根据 Verilog HDL 语言的描述画出相应的逻辑电路图**  `concept_ch04_根据_Verilog_HDL_语言的描述画出相应的逻辑电路图`  section=—  sources=guide_enum_title
- [low] **模块的两种描述方式**  `concept_ch04_模块的两种描述方式`  section=—  sources=guide_enum_title
- [low] **用 Verilog HDL 语言描述一个逻辑电路模块**  `concept_ch04_用_Verilog_HDL_语言描述一个逻辑电路模块`  section=—  sources=guide_enum_title
- [low] **用加法器设计组合逻辑电路**  `concept_ch04_用加法器设计组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **用小规集成门电路设计组合逻辑电路**  `concept_ch04_用小规集成门电路设计组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **用数据选择器设计组合逻辑电路**  `concept_ch04_用数据选择器设计组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **用译码器设计组合逻辑电路**  `concept_ch04_用译码器设计组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **组合逻辑电路的特点**  `concept_ch04_组合逻辑电路的特点`  section=—  sources=guide_enum_title
- [low] **设计验证**  `concept_ch04_设计验证`  section=—  sources=guide_enum_title
- [low] **进行逻辑抽象**  `concept_ch04_进行逻辑抽象`  section=—  sources=guide_enum_title
- [low] **选定器件类型**  `concept_ch04_选定器件类型`  section=—  sources=guide_enum_title
- [low] **逻辑功能的描述**  `concept_ch04_逻辑功能的描述`  section=—  sources=guide_enum_title
- [low] **（4）画出用门电路组成的逻辑电路图**  `concept_ch04__4_画出用门电路组成的逻辑电路图`  section=—  sources=breadcrumb_tail

### 第05章

- [high] **SR 锁存器**  `concept_ch05_SR_锁存器`  section=5.2  sources=section_title
- [high] **只读存储器(ROM)**  `concept_ch05_只读存储器_ROM_`  section=5.5.3  sources=section_title
- [high] **存储器**  `concept_ch05_存储器`  section=5.5  sources=section_title
- [high] **存储器容量的扩展**  `concept_ch05_存储器容量的扩展`  section=5.5.4  sources=section_title
- [high] **寄存器**  `concept_ch05_寄存器`  section=5.4  sources=section_title
- [high] **用存储器实现组合逻辑函数**  `concept_ch05_用存储器实现组合逻辑函数`  section=5.5.5  sources=section_title
- [high] **触发器**  `concept_ch05_触发器`  section=5.3  sources=section_title
- [high] **触发器按逻辑功能的分类**  `concept_ch05_触发器按逻辑功能的分类`  section=5.3.4  sources=section_title
- [high] **触发器的动态特性**  `concept_ch05_触发器的动态特性`  section=5.3.5  sources=section_title
- [low] **$D$ 触发器**  `concept_ch05__D_触发器`  section=—  sources=guide_enum_title
- [low] **$T$ 触发器**  `concept_ch05__T_触发器`  section=—  sources=guide_enum_title
- [low] **DRAM 的动态存储单元**  `concept_ch05_DRAM_的动态存储单元`  section=—  sources=guide_enum_title
- [low] **DRAM的总体结构**  `concept_ch05_DRAM的总体结构`  section=—  sources=guide_enum_title
- [low] **JK 触发器**  `concept_ch05_JK_触发器`  section=—  sources=guide_enum_title
- [low] **ROM的分类**  `concept_ch05_ROM的分类`  section=—  sources=guide_enum_title
- [low] **ROM的结构和工作原理**  `concept_ch05_ROM的结构和工作原理`  section=—  sources=guide_enum_title
- [low] **SR 触发器**  `concept_ch05_SR_触发器`  section=—  sources=guide_enum_title
- [low] **SRAM的结构和工作原理**  `concept_ch05_SRAM的结构和工作原理`  section=—  sources=guide_enum_title
- [low] **SRAM的静态存储单元**  `concept_ch05_SRAM的静态存储单元`  section=—  sources=guide_enum_title
- [low] **② 边沿触发方式的动作特点**  `concept_ch05_②_边沿触发方式的动作特点`  section=—  sources=breadcrumb_tail
- [low] **③ 脉冲触发方式的动作特点**  `concept_ch05_③_脉冲触发方式的动作特点`  section=—  sources=breadcrumb_tail
- [low] **传输延迟时间(Propagation delay time) $t_{pd}$**  `concept_ch05_传输延迟时间_Propagation_delay_time_t__pd_`  section=—  sources=guide_enum_title
- [low] **位扩展方式**  `concept_ch05_位扩展方式`  section=—  sources=guide_enum_title
- [low] **保持时间（Hold time） $t_{h}$**  `concept_ch05_保持时间_Hold_time_t__h_`  section=—  sources=guide_enum_title
- [low] **字扩展方式**  `concept_ch05_字扩展方式`  section=—  sources=guide_enum_title
- [low] **存储器扩展容量的方法**  `concept_ch05_存储器扩展容量的方法`  section=—  sources=guide_enum_title
- [low] **建立时间（Setup time） $t_{su}$**  `concept_ch05_建立时间_Setup_time_t__su_`  section=—  sources=guide_enum_title
- [low] **用存储器设计组合逻辑电路**  `concept_ch05_用存储器设计组合逻辑电路`  section=—  sources=guide_enum_title
- [low] **电平触发方式的动作特点**  `concept_ch05_电平触发方式的动作特点`  section=—  sources=guide_enum_title
- [low] **电路结构和工作原理**  `concept_ch05_电路结构和工作原理`  section=—  sources=guide_enum_title
- [low] **给定触发器输入信号的波形，求对应的输出波形**  `concept_ch05_给定触发器输入信号的波形_求对应的输出波形`  section=—  sources=guide_enum_title
- [low] **脉冲触发方式的动作特点**  `concept_ch05_脉冲触发方式的动作特点`  section=—  sources=guide_enum_title
- [low] **触发器的应用**  `concept_ch05_触发器的应用`  section=—  sources=guide_enum_title
- [low] **触发器的种类繁多，怎样才能系统地掌握它们的分类方法和各自的特点？**  `concept_ch05_触发器的种类繁多_怎样才能系统地掌握它们的分类方法和各自的特点_`  section=—  sources=guide_enum_title
- [low] **边沿触发方式的动作特点**  `concept_ch05_边沿触发方式的动作特点`  section=—  sources=guide_enum_title

### 第06章

- [high] **可以实现时序逻辑电路的可编程逻辑器件**  `concept_ch06_可以实现时序逻辑电路的可编程逻辑器件`  section=6.5.1  sources=section_title
- [high] **同步时序逻辑电路的分析方法**  `concept_ch06_同步时序逻辑电路的分析方法`  section=6.2.1  sources=section_title
- [high] **同步时序逻辑电路的设计方法**  `concept_ch06_同步时序逻辑电路的设计方法`  section=6.4.1  sources=section_title
- [high] **复杂时序逻辑电路的设计**  `concept_ch06_复杂时序逻辑电路的设计`  section=6.4.4  sources=section_title
- [high] **序列信号发生器**  `concept_ch06_序列信号发生器`  section=6.3.4  sources=section_title
- [high] **异步时序逻辑电路的分析方法**  `concept_ch06_异步时序逻辑电路的分析方法`  section=6.2.3  sources=section_title
- [high] **异步时序逻辑电路的设计方法**  `concept_ch06_异步时序逻辑电路的设计方法`  section=6.4.3  sources=section_title
- [high] **时序逻辑电路中的竞争-冒险现象**  `concept_ch06_时序逻辑电路中的竞争_冒险现象`  section=6.6  sources=section_title
- [high] **时序逻辑电路的状态转换表、状态转换图、状态机流程图和时序图**  `concept_ch06_时序逻辑电路的状态转换表_状态转换图_状态机流程图和时序图`  section=6.2.2  sources=section_title
- [high] **时序逻辑电路的自启动设计**  `concept_ch06_时序逻辑电路的自启动设计`  section=6.4.2  sources=section_title
- [high] **用硬件描述语言 Verilog HDL 描述时序逻辑电路**  `concept_ch06_用硬件描述语言_Verilog_HDL_描述时序逻辑电路`  section=6.5.2  sources=section_title
- [high] **移位寄存器**  `concept_ch06_移位寄存器`  section=6.3.1  sources=section_title
- [high] **计数器**  `concept_ch06_计数器`  section=6.3.2  sources=section_title
- [high] **顺序脉冲发生器**  `concept_ch06_顺序脉冲发生器`  section=6.3.3  sources=section_title
- [low] **① 置零法**  `concept_ch06_①_置零法`  section=—  sources=breadcrumb_tail
- [low] **② 置数法**  `concept_ch06_②_置数法`  section=—  sources=breadcrumb_tail
- [low] **任意进制计数器的构成方法**  `concept_ch06_任意进制计数器的构成方法`  section=—  sources=guide_enum_title
- [low] **分析由中规模集成时序逻辑电路组成的时序电路**  `concept_ch06_分析由中规模集成时序逻辑电路组成的时序电路`  section=—  sources=guide_enum_title
- [low] **分析由触发器和门电路组成的时序逻辑电路**  `concept_ch06_分析由触发器和门电路组成的时序逻辑电路`  section=—  sources=guide_enum_title
- [low] **同步计数器**  `concept_ch06_同步计数器`  section=—  sources=guide_enum_title
- [low] **对时序逻辑电路的描述**  `concept_ch06_对时序逻辑电路的描述`  section=—  sources=guide_enum_title
- [low] **对触发器的描述**  `concept_ch06_对触发器的描述`  section=—  sources=guide_enum_title
- [low] **异步计数器**  `concept_ch06_异步计数器`  section=—  sources=guide_enum_title
- [low] **时序图**  `concept_ch06_时序图`  section=—  sources=guide_enum_title
- [low] **检查设计的电路能否自启动**  `concept_ch06_检查设计的电路能否自启动`  section=—  sources=guide_enum_title
- [low] **状态分配**  `concept_ch06_状态分配`  section=—  sources=guide_enum_title
- [low] **状态化简**  `concept_ch06_状态化简`  section=—  sources=guide_enum_title
- [low] **状态机流程图（SM 图）**  `concept_ch06_状态机流程图_SM_图_`  section=—  sources=guide_enum_title
- [low] **状态转换图**  `concept_ch06_状态转换图`  section=—  sources=guide_enum_title
- [low] **状态转换表**  `concept_ch06_状态转换表`  section=—  sources=guide_enum_title
- [low] **用 Verilog HDL 语言描述时序逻辑电路**  `concept_ch06_用_Verilog_HDL_语言描述时序逻辑电路`  section=—  sources=guide_enum_title
- [low] **用中规模集成的计数器设计任意进制计数器**  `concept_ch06_用中规模集成的计数器设计任意进制计数器`  section=—  sources=guide_enum_title
- [low] **用触发器和门电路设计时序逻辑电路**  `concept_ch06_用触发器和门电路设计时序逻辑电路`  section=—  sources=guide_enum_title
- [low] **移位寄存器型计数器**  `concept_ch06_移位寄存器型计数器`  section=—  sources=guide_enum_title
- [low] **选定触发器的类型，求出电路的状态方程、驱动方程和输出方程**  `concept_ch06_选定触发器的类型_求出电路的状态方程_驱动方程和输出方程`  section=—  sources=guide_enum_title
- [low] **逻辑抽象，得出电路的状态转换图或状态转换表**  `concept_ch06_逻辑抽象_得出电路的状态转换图或状态转换表`  section=—  sources=guide_enum_title

### 第07章

- [high] **555定时器的电路结构与功能**  `concept_ch07_555定时器的电路结构与功能`  section=7.5.1  sources=section_title
- [high] **单稳态电路**  `concept_ch07_单稳态电路`  section=7.3  sources=section_title
- [high] **多谐振荡电路**  `concept_ch07_多谐振荡电路`  section=7.4  sources=section_title
- [high] **定时器的输入电路**  `concept_ch07_定时器的输入电路`  section=3.555  sources=section_title
- [high] **对称式多谐振荡电路**  `concept_ch07_对称式多谐振荡电路`  section=7.4.1  sources=section_title
- [high] **施密特触发电路**  `concept_ch07_施密特触发电路`  section=7.2  sources=section_title
- [high] **施密特触发电路的结构和工作原理**  `concept_ch07_施密特触发电路的结构和工作原理`  section=7.2.1  sources=section_title
- [high] **环形振荡电路**  `concept_ch07_环形振荡电路`  section=7.4.3  sources=section_title
- [high] **用 555 定时器接成的单稳态电路**  `concept_ch07_用_555_定时器接成的单稳态电路`  section=7.5.3  sources=section_title
- [high] **用 555 定时器接成的多谐振荡电路**  `concept_ch07_用_555_定时器接成的多谐振荡电路`  section=7.5.4  sources=section_title
- [high] **用 555 定时器接成的施密特触发电路**  `concept_ch07_用_555_定时器接成的施密特触发电路`  section=7.5.2  sources=section_title
- [high] **用施密特触发电路构成的多谐振荡电路**  `concept_ch07_用施密特触发电路构成的多谐振荡电路`  section=7.4.4  sources=section_title
- [high] **用门电路组成的单稳态电路**  `concept_ch07_用门电路组成的单稳态电路`  section=7.3.1  sources=section_title
- [high] **用门电路组成的施密特触发电路**  `concept_ch07_用门电路组成的施密特触发电路`  section=7.2.2  sources=section_title
- [high] **石英晶体多谐振荡电路**  `concept_ch07_石英晶体多谐振荡电路`  section=7.4.5  sources=section_title
- [high] **集成单稳态电路**  `concept_ch07_集成单稳态电路`  section=7.3.2  sources=section_title
- [high] **非对称式多谐振荡电路**  `concept_ch07_非对称式多谐振荡电路`  section=7.4.2  sources=section_title
- [low] **555 定时器应用电路的分析计算**  `concept_ch07_555_定时器应用电路的分析计算`  section=—  sources=guide_enum_title
- [low] **多谐振荡电路的分析计算**  `concept_ch07_多谐振荡电路的分析计算`  section=—  sources=guide_enum_title
- [low] **微分型单稳态电路**  `concept_ch07_微分型单稳态电路`  section=—  sources=guide_enum_title
- [low] **施密特触发电路阈值电压的计算**  `concept_ch07_施密特触发电路阈值电压的计算`  section=—  sources=guide_enum_title
- [low] **用于波形变换**  `concept_ch07_用于波形变换`  section=—  sources=guide_enum_title
- [low] **用于脉冲整形**  `concept_ch07_用于脉冲整形`  section=—  sources=guide_enum_title
- [low] **用于脉冲鉴幅**  `concept_ch07_用于脉冲鉴幅`  section=—  sources=guide_enum_title
- [low] **积分型单稳态电路**  `concept_ch07_积分型单稳态电路`  section=—  sources=guide_enum_title

### 第08章

- [high] **$\Sigma -\Delta$ 型A/D转换器**  `concept_ch08__Sigma_Delta_型A_D转换器`  section=8.6.5  sources=section_title
- [high] **A/D 转换器的转换速度**  `concept_ch08_A_D_转换器的转换速度`  section=8.7.2  sources=section_title
- [high] **A/D 转换的基本原理**  `concept_ch08_A_D_转换的基本原理`  section=8.4  sources=section_title
- [high] **A/D转换器的转换精度**  `concept_ch08_A_D转换器的转换精度`  section=8.7.1  sources=section_title
- [high] **D/A转换器的转换精度**  `concept_ch08_D_A转换器的转换精度`  section=8.3.1  sources=section_title
- [high] **D/A转换器的转换速度**  `concept_ch08_D_A转换器的转换速度`  section=8.3.2  sources=section_title
- [high] **V-F 变换型 A/D 转换器**  `concept_ch08_V_F_变换型_A_D_转换器`  section=8.6.6  sources=section_title
- [high] **倒 T 形电阻网络 D/A 转换器**  `concept_ch08_倒_T_形电阻网络_D_A_转换器`  section=8.2.2  sources=section_title
- [high] **具有双极性输出的 D/A 转换器**  `concept_ch08_具有双极性输出的_D_A_转换器`  section=8.2.6  sources=section_title
- [high] **双积分型 A/D 转换器**  `concept_ch08_双积分型_A_D_转换器`  section=8.6.4  sources=section_title
- [high] **取样-保持电路**  `concept_ch08_取样_保持电路`  section=8.5  sources=section_title
- [high] **并联比较型 A/D 转换器**  `concept_ch08_并联比较型_A_D_转换器`  section=8.6.1  sources=section_title
- [high] **开关树型 D/A 转换器**  `concept_ch08_开关树型_D_A_转换器`  section=8.2.4  sources=section_title
- [high] **权电容网络 D/A 转换器**  `concept_ch08_权电容网络_D_A_转换器`  section=8.2.5  sources=section_title
- [high] **权电流型 D/A 转换器**  `concept_ch08_权电流型_D_A_转换器`  section=8.2.3  sources=section_title
- [high] **权电阻网络 D/A 转换器**  `concept_ch08_权电阻网络_D_A_转换器`  section=8.2.1  sources=section_title
- [high] **流水线型 A/D 转换器**  `concept_ch08_流水线型_A_D_转换器`  section=8.6.2  sources=section_title
- [high] **逐次逼近型A/D转换器**  `concept_ch08_逐次逼近型A_D转换器`  section=8.6.3  sources=section_title
- [low] **D/A 转换器的应用**  `concept_ch08_D_A_转换器的应用`  section=—  sources=guide_enum_title
- [low] **D/A 转换器输出电压的定量计算**  `concept_ch08_D_A_转换器输出电压的定量计算`  section=—  sources=guide_enum_title
- [low] **倒 T 形电阻网络 D/A 转换器参考电压稳定度的计算**  `concept_ch08_倒_T_形电阻网络_D_A_转换器参考电压稳定度的计算`  section=—  sources=guide_enum_title
- [low] **取样定理**  `concept_ch08_取样定理`  section=—  sources=guide_enum_title
- [low] **求和放大器的基本原理**  `concept_ch08_求和放大器的基本原理`  section=—  sources=guide_enum_title
- [low] **量化和编码**  `concept_ch08_量化和编码`  section=—  sources=guide_enum_title
- [low] **量化电平参考电压稳定度的计算**  `concept_ch08_量化电平参考电压稳定度的计算`  section=—  sources=guide_enum_title
