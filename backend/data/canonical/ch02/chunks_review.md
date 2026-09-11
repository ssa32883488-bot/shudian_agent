# 第02章 逻辑代数基础 — Chunk 效果预览

> 自动生成，用于人工抽检。每个 chunk 以 `---` 分隔。

## 汇总

- 总 chunk 数：**161**
- 习题合并：**27/27**
- 教材图：**58**（含子图拆分）
- orphan 图：**0**
- 视觉描述：**77** 张

---

## Chunk 1/161：`ch02_sec_summary_theory_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_summary_theory_4 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > summary 内容提要 |
| section_id | ch02_sec_summary |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | — |
| next_chunk_id | ch02_sec_2_1_theory_8 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L4–6 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > summary 内容提要

本章介绍用于分析数字电路逻辑功能的数学方法——逻辑代数。首先将介绍逻辑代数的基本公式、常用公式和几个重要的定理，然后讲授逻辑函数的各种描述方法以及这些描述方法之间的互相转换。最后，介绍逻辑函数的化简方法。

---

## Chunk 2/161：`ch02_sec_2_1_theory_8`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_1_theory_8 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.1 概述 |
| section_id | ch02_sec_2_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_summary_theory_4 |
| next_chunk_id | ch02_sec_2_2_theory_18_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L8–16 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.1 概述

在上一章中我们已经讲过,不同的数码不仅可以表示数量的不同大小,而且还能用来表示不同的事物。在数字逻辑电路中,用1位二进制数码的0和1表示一个事物的两种不同逻辑状态。例如,可以用1和0分别表示一件事情的是和非、真和伪、有和无、好和坏,或者表示电路的通和断、电灯的亮和暗、门的开和关等等。这种只有两种对立逻辑状态的逻辑关系称为二值逻辑。

所谓“逻辑”，在这里是指事物间的因果关系。当两个二进制数码表示不同的逻辑状态时，它们之间可以按照指定的某种因果关系进行推理运算。我们将这种运算称为逻辑运算。

1849年英国数学家乔治·布尔(George Boole)首先提出了进行逻辑运算的数学方法——布尔代数。后来，由于布尔代数被广泛应用于解决开关电路和数字逻辑电路的分析与设计中，所以也将布尔代数称为开关代数或逻辑代数。本章所讲的逻辑代数就是布尔代数在二值逻辑电路中的应用。下面我们将会看到，虽然有些逻辑代数的运算公式在形式上和普通代数的运算公式雷同，但是两者所包含的物理意义有本质的不同。逻辑代数中也用字母表示变量，这种变量称为逻辑变量。逻辑运算表示的是逻辑变量以及常量之间逻辑状态的推理运算，而不是数量之间的运算。

虽然在二值逻辑中,每个变量的取值只有0和1两种可能,只能表示两种不同的逻辑状态,但是我们可以用多变量的不同状态组合表示事物的多种逻辑状态,处理任何复杂的逻辑问题。

---

## Chunk 3/161：`ch02_sec_2_2_theory_18_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_18_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.2.1(a), 图2.2.1(b), 图2.2.1(c) |
| prev_chunk_id | ch02_sec_2_1_theory_8 |
| next_chunk_id | ch02_sec_2_2_theory_18_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L18–130 |

### 配图

**图2.2.1(a)** — 用于说明与、或、非定义的电路 子图(a)

![图2.2.1(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/a2fc5020ce3ae729813c2f357a2f050521c5e5965b37c6d9a36879e6b0bdfebc.jpg)

*视觉描述：* 串联开关A、B与灯泡Y的与逻辑示意电路：两开关均闭合灯才亮，对应Y=A·B。

**图2.2.1(b)** — 用于说明与、或、非定义的电路 子图(b)

![图2.2.1(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/7df8cfc2a74d38854f365d223fa41ca6bfb25214f480a2421f8062fa55d89f20.jpg)

*视觉描述：* 开关A、B并联控制灯泡Y的或逻辑电路：任一开关闭合即可点亮，对应Y=A+B。

**图2.2.1(c)** — 用于说明与、或、非定义的电路 子图(c)

![图2.2.1(c)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/05a329851db8052fe7993e2a055853ddd0b8d277a4f027b2d3b9e6879d7b0dae.jpg)

*视觉描述：* 开关A与灯泡Y并联的非逻辑电路：A断开时灯亮，A闭合时短路灯灭，对应Y=A'。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算

逻辑代数的基本运算有与（AND）、或（OR）、非（NOT）三种。为便于理解它们的含义，先来

看一个简单的例子。

图 2.2.1 中给出了三个指示灯的控制电路。在图(a)电路中，只有当两个开关同时闭合时，指示灯才会亮；在图(b)电路中，只要有任何一个开关闭合，指示灯就亮；而在图(c)电路中，开关断开时灯亮，开关闭合时灯反而不亮。

图 2.2.1 用于说明与、或、非定义的电路

如果把开关闭合作为条件(或导致事物结果的原因), 把灯亮作为结果, 那么图 2.2.1 中的三个电路代表了三种不同的因果关系:

图(a)的例子表明,只有决定事物结果的全部条件同时具备时,结果才发生。这种因果关系称为逻辑与,或称逻辑相乘。

图(b)的例子表明,在决定事物结果的诸条件中只要有任何一个满足,结果就会发生。这种因果关系称为逻辑或,也称逻辑相加。

图(c)的例子表明,只要条件具备了,结果便不会发生;而条件不具备时,结果一定发生。这种因果关系称为逻辑非,也称逻辑求反。

若以 A、B 表示开关的状态，并以 1 表示开关闭合，以 0 表示开关断开；以 Y 表示指示灯的状态，并以 1 表示灯亮，以 0 表示不亮，则可以列出以 0、1 表示的与、或、非逻辑关系的图表，如表 2.2.1、表 2.2.2 和表 2.2.3 所示。这种图表称为逻辑真值表（truth table），简称真值表。

表 2.2.1 与逻辑

<table><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></table>

表 2.2.2 或逻辑

<table><tr><td colspan="3">运算的真值表</td></tr><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></table>

表 2.2.3 非逻辑

<table><tr><td>A</td><td>Y</td></tr><tr><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td></tr></table>

[图2.2.1(a)] 用于说明与、或、非定义的电路 子图(a)
[图2.2.1(a)描述] 串联开关A、B与灯泡Y的与逻辑示意电路：两开关均闭合灯才亮，对应Y=A·B。
[图2.2.1(b)] 用于说明与、或、非定义的电路 子图(b)
[图2.2.1(b)描述] 开关A、B并联控制灯泡Y的或逻辑电路：任一开关闭合即可点亮，对应Y=A+B。
[图2.2.1(c)] 用于说明与、或、非定义的电路 子图(c)
[图2.2.1(c)描述] 开关A与灯泡Y并联的非逻辑电路：A断开时灯亮，A闭合时短路灯灭，对应Y=A'。

---

## Chunk 4/161：`ch02_sec_2_2_theory_18_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_18_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.2.2, 图2.2.3 |
| prev_chunk_id | ch02_sec_2_2_theory_18_p00 |
| next_chunk_id | ch02_sec_2_2_theory_18_p02 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L18–130 |

### 配图

**图2.2.2** — 与、或、非的图形符号

![图2.2.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/a0766d8ed3c61208fb79fb90fbd4b443871bcf528b0de6fe3e916e3949747cea.jpg)

*视觉描述：* 与、或、非门的特定外形符号(a)与矩形轮廓符号(b)对照，输入A/B、输出Y。

**图2.2.3** — 复合逻辑的图形符号和运算符号

![图2.2.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/5e5b89f29b232b6e256d2704380e871f6fa5a189de742bed1fe205f4b84e896d.jpg)

*视觉描述：* 与非、或非、异或、同或及与或非复合逻辑的标准图形符号与布尔式。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算

在逻辑代数中，将与、或、非看作是逻辑变量 A、B 间的三种最基本的逻辑运算，并以“·”表示与运算，以“+”表示或运算，以变量右上角的“'”表示非运算。因此，A 和 B 进行与逻辑运算时可写成

$$
Y = A \cdot B\tag{2.2.1}
$$

A 和 B 进行或逻辑运算时可写成

$$
Y = A + B\tag{2.2.2}
$$

对 $A$ 进行非逻辑运算时可写成

$$
Y = A ^ {\prime}\tag{2.2.3}
$$

同时,将实现与逻辑运算的单元电路称为与门,将实现或逻辑运算的单元电路称为或门,将实现非逻辑运算的单元电路称为非门(也称为反相器)。

逻辑非的运算符号尚无统一的标准。除了本书中采用“'”表示非运算以外，目前在国内、外的某些电子技术教材和EDA软件中，也采用 $\overline{A}$ 、 $\sim A$ 、 $\neg A$ 表示A的非运算。用“'”作为非运算符号比起在变量上加横线作为非运算符号更便于计算机输入，尤其在逻辑运算式中存在多重非运算时，这种优越性就更加明显。因此，在教材和EDA软件中使用“'”作为非运算符号的越来越多了。

与、或、非逻辑运算还可以用图形符号表示。图2.2.2中给出了被IEEE（电气与电子工程师协会）和IEC（国际电工协会）认定的两套与、或、非的图形符号，其中一套是目前在国外教材和EDA软件中普遍使用的特定外形符号，如图2.2.2(a)所示。另一套是矩形轮廓的符号，如图2.2.2(b)所示。本书中采用特定外形符号。

图 2.2.2 与、或、非的图形符号  
(a) 特定外形符号 (b) 矩形轮廓符号

实际的逻辑问题往往比与、或、非复杂得多，不过它们都可以用与、或、非的组合来实现。最常见的复合逻辑运算有与非（NAND）、或非（NOR）、与或非（AND-NOR）、异或（EXCLUSIVE OR）、同或（EXCLUSIVE NOR）等。表2.2.4\~表2.2.8给出了这些复合逻辑运算的真值表。图2.2.3是它们的图形逻辑符号和运算符号。这些图形符号同样也有特定外形符号和矩形轮廓符号两种。

表 2.2.4 与非逻辑的真值表

<table><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td></tr></table>

表 2.2.5 或非逻辑的真值表

[图2.2.2] 与、或、非的图形符号
[图2.2.2描述] 与、或、非门的特定外形符号(a)与矩形轮廓符号(b)对照，输入A/B、输出Y。
[图2.2.3] 复合逻辑的图形符号和运算符号
[图2.2.3描述] 与非、或非、异或、同或及与或非复合逻辑的标准图形符号与布尔式。

---

## Chunk 5/161：`ch02_sec_2_2_theory_18_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_18_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_18_p01 |
| next_chunk_id | ch02_sec_2_2_theory_18_p03 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L18–130 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算

<table><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td></tr></table>

表 2.2.6 与或非逻辑的真值表

---

## Chunk 6/161：`ch02_sec_2_2_theory_18_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_18_p03 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_18_p02 |
| next_chunk_id | ch02_sec_2_2_theory_18_p04 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L18–130 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

表 2.2.7 异或逻辑的真值表

---

## Chunk 7/161：`ch02_sec_2_2_theory_18_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_18_p04 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.2.3 |
| prev_chunk_id | ch02_sec_2_2_theory_18_p03 |
| next_chunk_id | ch02_sec_review_review_133 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L18–130 |

### 配图

**图2.2.3** — 复合逻辑的图形符号和运算符号

![图2.2.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/5e5b89f29b232b6e256d2704380e871f6fa5a189de742bed1fe205f4b84e896d.jpg)

*视觉描述：* 与非、或非、异或、同或及与或非复合逻辑的标准图形符号与布尔式。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.2 逻辑代数中的三种基本运算

<table><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td></tr></table>

表 2.2.8 同或逻辑的真值表

<table><tr><td>A</td><td>B</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></table>

图 2.2.3 复合逻辑的图形符号和运算符号

由表 2.2.4 可见, 将 A、B 先进行与运算, 然后将结果求反, 最后得到的即为 A、B 的与非运算结果。因此, 可以把与非运算看作是与运算和非运算的组合。图 2.2.3 中图形符号上的小圆圈表示非运算。

在与或非逻辑中，A、B之间以及C、D之间都是与的关系，只要A、B或C、D任何一组同时为1，输出Y就是0。只有当每一组输入都不全是1时，输出Y才是1。

异或是这样一种逻辑关系: 当 A、B 不同时, 输出 Y 为 1; 而当 A、B 相同时, 输出 Y 为 0。异或也可以用与、或、非的组合表示。

$$
A \textcircled {+} B = A \cdot B ^ {\prime} + A ^ {\prime} \cdot B\tag{2.2.4}
$$

同或和异或相反，当 $A, B$ 相同时， $Y$ 等于1， $A, B$ 不同时， $Y$ 等于0。同或也可以写成与、或、非的组合形式

$$
A \odot B = A \cdot B + A ^ {\prime} \cdot B ^ {\prime}\tag{2.2.5}
$$

而且，由表2.2.7和表2.2.8可见，异或和同或互为反运算，即

$$
A \oplus B = (A \odot B) ^ {\prime}; A \odot B = (A \oplus B) ^ {\prime}\tag{2.2.6}
$$

为简化书写,允许将 $A \cdot B$ 简写成 AB,略去逻辑相乘的运算符号“·”。

[图2.2.3] 复合逻辑的图形符号和运算符号
[图2.2.3描述] 与非、或非、异或、同或及与或非复合逻辑的标准图形符号与布尔式。

---

## Chunk 8/161：`ch02_sec_review_review_133`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_133 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_18_p04 |
| next_chunk_id | ch02_sec_review_review_135 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L133–134 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.2.1 你能各举出一个现实生活中存在的与、或、非逻辑关系的事例吗？

---

## Chunk 9/161：`ch02_sec_review_review_135`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_135 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_133 |
| next_chunk_id | ch02_sec_2_3_1_theory_140_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L135–136 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.2.2 两个变量的异或运算和同或运算之间是什么关系？

---

## Chunk 10/161：`ch02_sec_2_3_1_theory_140_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_3_1_theory_140_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.3.1 基本公式 |
| section_id | ch02_sec_2_3_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_135 |
| next_chunk_id | ch02_sec_2_3_1_theory_140_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L140–162 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.3.1 基本公式

表 2.3.1 给出了逻辑代数的基本公式。这些公式也称为布尔恒等式。

表 2.3.1 逻辑代数的基本公式

<table><tr><td>序号</td><td>公式</td><td>序号</td><td>公式</td></tr><tr><td>1</td><td> $\mathbf{0} \cdot A = 0$ </td><td>10</td><td> $\mathbf{1}' = \mathbf{0};\mathbf{0}' = \mathbf{1}$ </td></tr><tr><td>2</td><td> $\mathbf{1} \cdot A = A$ </td><td>11</td><td> $\mathbf{1} + A = \mathbf{1}$ </td></tr><tr><td>3</td><td> $A \cdot A = A$ </td><td>12</td><td> $\mathbf{0} + A = A$ </td></tr><tr><td>4</td><td> $A \cdot A' = \mathbf{0}$ </td><td>13</td><td> $A + A = A$ </td></tr><tr><td>5</td><td> $A \cdot B = B \cdot A$ </td><td>14</td><td> $A + A' = \mathbf{1}$ </td></tr><tr><td>6</td><td> $A \cdot (B \cdot C) = (A \cdot B) \cdot C$ </td><td>15</td><td> $A + B = B + A$ </td></tr><tr><td>7</td><td> $A \cdot (B + C) = A \cdot B + A \cdot C$ </td><td>16</td><td> $A + (B + C) = (A + B) + C$ </td></tr><tr><td>8</td><td> $(A \cdot B)' = A' + B'$ </td><td>17</td><td> $A + B \cdot C = (A + B) \cdot (A + C)$ </td></tr><tr><td>9</td><td> $(A')' = A$ </td><td>18</td><td> $(A + B)' = A' \cdot B'$ </td></tr></table>

式(1)、(2)、(11)和(12)给出了变量与常量间的运算规则。

式(3)和(13)是同一变量的运算规律,也称为重叠律。

式(4)和(14)表示变量与它的反变量之间的运算规律,也称为互补律。

---

## Chunk 11/161：`ch02_sec_2_3_1_theory_140_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_3_1_theory_140_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.3.1 基本公式 |
| section_id | ch02_sec_2_3_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_3_1_theory_140_p00 |
| next_chunk_id | ch02_eg2_3_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L140–162 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.3.1 基本公式

式(5)和(15)为交换律,式(6)和(16)为结合律,式(7)和(17)为分配律。

式(8)和(18)是著名的德·摩根(De.Morgan)定理,亦称反演律。在逻辑函数的化简和变换中经常要用到这一对公式。

式(9)表明,一个变量经过两次求反运算之后还原为其本身,所以该式又称为还原律。

式(10)是对0和1求反运算的规则,它说明0和1互为求反的结果。

这些公式的正确性可以用列真值表的方法加以验证。如果等式成立，那么将任何一组变量的取值代入公式两边所得的结果应该相等。因此，等式两边所对应的真值表也必然相同。

---

## Chunk 12/161：`ch02_eg2_3_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_3_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.3.1 基本公式 |
| section_id | ch02_sec_2_3_1 |
| exercise_id | — |
| example_id | 例2.3.1 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_3_1_theory_140_p01 |
| next_chunk_id | ch02_sec_2_3_2_theory_178_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L163–176 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.3.1 基本公式

【例 2.3.1】用真值表证明表 2.3.1 中式(17)的正确性。

解：已知表2.3.1中的式(17)为

$$
A + B \cdot C = (A + B) \cdot (A + C)
$$

将 A、B、C 所有可能的取值组合逐一代入上式的两边，算出相应的结果，即得到表 2.3.2 所示的真值表。可见，等式两边对应的真值表相同，故等式成立。

表 2.3.2 式 (17) 的真值表

<table><tr><td>A</td><td>B</td><td>C</td><td> $B \cdot C$ </td><td> $A + B \cdot C$ </td><td> $A + B$ </td><td> $A + C$ </td><td> $(A + B) \cdot (A + C)$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

---

## Chunk 13/161：`ch02_sec_2_3_2_theory_178_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_3_2_theory_178_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.3.2 若干常用公式 |
| section_id | ch02_sec_2_3_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_3_1 |
| next_chunk_id | ch02_sec_2_3_2_theory_178_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L178–238 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.3.2 若干常用公式

表 2.3.3 中列出了几个常用公式。这些公式是利用基本公式导出的。直接运用这些导出公式可以给化简逻辑函数的工作带来很大方便。

表 2.3.3 若干常用公式

<table><tr><td>序号</td><td>公式</td></tr><tr><td>21</td><td> $A+A \cdot B=A$ </td></tr><tr><td>22</td><td> $A+A' \cdot B=A+B$ </td></tr><tr><td>23</td><td> $A \cdot B+A \cdot B'=A$ </td></tr><tr><td>24</td><td> $A \cdot (A+B)=A$ </td></tr><tr><td>25</td><td> $A \cdot B+A' \cdot C+B \cdot C=A \cdot B+A' \cdot C$  $A \cdot B+A' \cdot C+BCD=A \cdot B+A' \cdot C$ </td></tr><tr><td>26</td><td> $A \cdot (A \cdot B)'=A \cdot B';A' \cdot (AB)'=A'$ </td></tr></table>

现将表 2.3.3 中的各式证明如下。

1. 式(21) $A+A \cdot B=A$

证明： $A + A\cdot B = A\cdot (1 + B) = A\cdot 1 = A$

上式说明，在两个乘积项相加时，若其中一项以另一项为因子，则该项是多余的，可以删去。

2. 式(22) $A+A'\cdot B=A+B$

证明： $A + A^{\prime}\cdot B = (A + A^{\prime})\cdot (A + B) = 1\cdot (A + B) = A + B$

这一结果表明,两个乘积项相加时,如果一项取反后是另一项的因子,则此因子是多余的,可以消去。

3. 式(23) $A \cdot B + A \cdot B' = A$

证明： $A\cdot B + A\cdot B^{\prime} = A(B + B^{\prime}) = A\cdot 1 = A$

这个公式的含义是,当两个乘积项相加时,若它们分别包含 B 和 $B'$ 两个因子而其他因子相同,则两项定能合并,且可将 B 和 $B'$ 两个因子消去。

4. 式(24) $A \cdot (A + B) = A$

证明： $A\cdot (A + B) = A\cdot A + A\cdot B = A + A\cdot B$

该式说明,变量 A 和包含 A 的和相乘时,其结果等于 A,即可以将和消掉。

---

## Chunk 14/161：`ch02_sec_2_3_2_theory_178_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_3_2_theory_178_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.3.2 若干常用公式 |
| section_id | ch02_sec_2_3_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_3_2_theory_178_p00 |
| next_chunk_id | ch02_sec_review_review_241 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L178–238 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.3.2 若干常用公式

5. 式(25) $A \cdot B + A' \cdot C + B \cdot C = A \cdot B + A' \cdot C$

$$
\begin{array}{r l} \therefore A \cdot B + A ^ {\prime} \cdot C + B \cdot C & = A \cdot B + A ^ {\prime} \cdot C + B \cdot C (A + A ^ {\prime}) \\ & = A \cdot B + A ^ {\prime} \cdot C + A \cdot B \cdot C + A ^ {\prime} \cdot B \cdot C \\ & = A \cdot B \cdot (1 + C) + A ^ {\prime} \cdot C \cdot (1 + B) \\ & = A \cdot B + A ^ {\prime} \cdot C \end{array}
$$

这个公式说明,若两个乘积项中分别包含 A 和 $A'$ 两个因子,而这两个乘积项的其余因子组成第三个乘积项时,则第三个乘积项是多余的,可以消去。

从上式不难进一步导出

$$
A \cdot B + A ^ {\prime} \cdot C + B \cdot C \cdot D = A \cdot B + A ^ {\prime} \cdot C
$$

6. 式(26) $A \cdot (A \cdot B)' = A \cdot B'; A' \cdot (A \cdot B)' = A'$

证明： $A \cdot (A \cdot B)' = A \cdot (A' + B') = A \cdot A' + A \cdot B' = A \cdot B'$

上式说明, 当 A 和一个乘积项的非相乘, 且 A 为乘积项的因子时, 则 A 这个因子可以消去。

$$
\begin{array}{r l} A ^ {\prime} \cdot (A \cdot B) ^ {\prime} & = A ^ {\prime} \cdot (A ^ {\prime} + B ^ {\prime}) = A ^ {\prime} \cdot A ^ {\prime} + A ^ {\prime} \cdot B ^ {\prime} = A ^ {\prime} \cdot (1 + B ^ {\prime}) \\ & = A ^ {\prime} \end{array}
$$

此式表明，当 $A'$ 和一个乘积项的非相乘，且 A 为乘积项的因子时，其结果就等于 $A'$ 。

从以上的证明可以看到,这些常用公式都是从基本公式导出的结果。当然,还可以推导出更多的常用公式。

---

## Chunk 15/161：`ch02_sec_review_review_241`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_241 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_3_2_theory_178_p01 |
| next_chunk_id | ch02_sec_2_4_1_theory_246 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L241–242 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.3.1 在逻辑代数的基本公式当中哪些公式的运算规则和普通代数的运算规则是相同的？哪些是不同的、需要特别记住的？

---

## Chunk 16/161：`ch02_sec_2_4_1_theory_246`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_4_1_theory_246 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.1 代入定理 |
| section_id | ch02_sec_2_4_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_241 |
| next_chunk_id | ch02_eg2_4_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L246–252 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.1 代入定理

在任何一个包含变量 A 的逻辑等式中, 若以另外一个逻辑式代入式中所有 A 的位置, 则等式仍然成立。这就是所谓的代入定理。

因为变量 A 仅有 0 和 1 两种可能的状态, 所以无论将 A=0 还是 A=1 代入逻辑等式, 等式都一定成立。而任何一个逻辑式的取值也不外 0 和 1 两种, 所以用它取代式中的 A 时, 等式自然也成立。因此, 可以将代入定理看作无需证明的公理。

利用代入定理很容易把表 2.3.1 中的基本公式和表 2.3.3 中的常用公式推广为多变量的形式。

---

## Chunk 17/161：`ch02_eg2_4_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_4_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.1 代入定理 |
| section_id | ch02_sec_2_4_1 |
| exercise_id | — |
| example_id | 例2.4.1 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_4_1_theory_246 |
| next_chunk_id | ch02_sec_2_4_2_theory_276 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L253–274 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.1 代入定理

【例 2.4.1】用代入定理证明德·摩根定理也适用于多变量的情况。

解：已知二变量的德·摩根定理为

$$
(A + B) ^ {\prime} = A ^ {\prime} \cdot B ^ {\prime} \quad \text {及} \quad (A \cdot B) ^ {\prime} = A ^ {\prime} + B ^ {\prime}
$$

今以 $(B+C)$ 代入左边等式中B的位置,同时以 $(B\cdot C)$ 代入右边等式中B的位置,于是得到

$$
(A + (B + C)) ^ {\prime} = A ^ {\prime} \cdot (B + C) ^ {\prime} = A ^ {\prime} \cdot B ^ {\prime} \cdot C ^ {\prime}
$$

$$
(A \cdot (B \cdot C)) ^ {\prime} = A ^ {\prime} + (B \cdot C) ^ {\prime} = A ^ {\prime} + B ^ {\prime} + C ^ {\prime}
$$

对一个乘积项或逻辑式求反时,应在乘积项或逻辑式外边加括号,然后对括号内的整个内容求反。

此外，在对复杂的逻辑式进行运算时，仍需遵守与普通代数一样的运算优先顺序，即先算括号里的内容，其次算乘法，最后算加法。

---

## Chunk 18/161：`ch02_sec_2_4_2_theory_276`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_4_2_theory_276 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.2 反演定理 |
| section_id | ch02_sec_2_4_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_4_1 |
| next_chunk_id | ch02_eg2_4_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L276–288 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.2 反演定理

对于任意一个逻辑式 Y，若将其中所有的“·”换成“+”，“+”换成“·”，0 换成 1,1 换成 0，原变量换成反变量，反变量换成原变量，则得到的结果就是 $Y'$ 。这个规律称为反演定理。

反演定理为求取已知逻辑式的反逻辑式提供了方便。

在使用反演定理时,还需注意遵守以下两个规则:

① 仍需遵守“先括号、然后乘、最后加”的运算优先次序。

② 不属于单个变量上的反号应保留不变。

回顾一下 2.3.1 节中讲过的德·摩根定理便可发现,它只不过是反演定理的一个特例而已。正是由于这个原因,才将它称为反演律。

---

## Chunk 19/161：`ch02_eg2_4_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_4_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.2 反演定理 |
| section_id | ch02_sec_2_4_2 |
| exercise_id | — |
| example_id | 例2.4.2 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_4_2_theory_276 |
| next_chunk_id | ch02_eg2_4_3 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L289–298 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.2 反演定理

【例 2.4.2】已知 $Y=A(B+C)+CD$ ，求 $Y'$ 。

解：根据反演定理可写出

$$
\begin{array}{r l} Y ^ {\prime} & = (A ^ {\prime} + B ^ {\prime} C ^ {\prime}) (C ^ {\prime} + D ^ {\prime}) \\ & = A ^ {\prime} C ^ {\prime} + B ^ {\prime} C ^ {\prime} + A ^ {\prime} D ^ {\prime} + B ^ {\prime} C ^ {\prime} D ^ {\prime} \\ & = A ^ {\prime} C ^ {\prime} + B ^ {\prime} C ^ {\prime} + A ^ {\prime} D ^ {\prime} \end{array}
$$

如果利用基本公式和常用公式进行运算,也能得到同样的结果,但是要麻烦得多。

---

## Chunk 20/161：`ch02_eg2_4_3`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_4_3 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.2 反演定理 |
| section_id | ch02_sec_2_4_2 |
| exercise_id | — |
| example_id | 例2.4.3 |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_4_2 |
| next_chunk_id | ch02_sec_2_4_3_theory_308 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L299–306 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.2 反演定理

【例 2.4.3】 若 $Y=(AB'+C)'+D)'+C$ ，求 $Y'$ 。

解：依据反演定理可直接写出

$$
\begin{array}{r l} Y ^ {\prime} & = \left(\left(A ^ {\prime} + B\right) C ^ {\prime}\right) ^ {\prime} D ^ {\prime}) ^ {\prime} C ^ {\prime} \\ & = \left(\left(A ^ {\prime} C ^ {\prime} + B C ^ {\prime}\right) + D\right) C ^ {\prime} \\ & = A ^ {\prime} C ^ {\prime} + B C ^ {\prime} + C ^ {\prime} D \end{array}
$$

---

## Chunk 21/161：`ch02_sec_2_4_3_theory_308`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_4_3_theory_308 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.3 对偶定理 |
| section_id | ch02_sec_2_4_3 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_4_3 |
| next_chunk_id | ch02_eg2_4_4 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L308–322 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.3 对偶定理

若两逻辑式相等,则它们的对偶式也相等,这就是对偶定理。

所谓对偶式是这样定义的:对于任何一个逻辑式 Y, 若将其中的“·”换成“+”, “+”换成“·”, 0 换成 1, 1 换成 0, 则得到一个新的逻辑式 $Y^{D}$ , 这个 $Y^{D}$ 就称为 Y 的对偶式, 或者说 Y 和 $Y^{D}$ 互为对偶式。

例如，若 $Y = A(B + C)$ ，则 $Y^{\mathrm{D}} = A + BC$

$$
\text { 若 } Y = (A B + C D) ^ {\prime}, \quad \text { 则 } Y ^ {\mathrm{D}} = ((A + B) (C + D)) ^ {\prime}
$$

若 $Y = AB + (C + D)'$ ， 则 $Y^{\mathrm{D}} = (A + B)(CD)'$

为了证明两个逻辑式相等,也可以通过证明它们的对偶式相等来完成,因为有些情况下证明它们的对偶式相等更加容易。

---

## Chunk 22/161：`ch02_eg2_4_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_4_4 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.4.3 对偶定理 |
| section_id | ch02_sec_2_4_3 |
| exercise_id | — |
| example_id | 例2.4.4 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_4_3_theory_308 |
| next_chunk_id | ch02_sec_review_review_341 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L323–338 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.4.3 对偶定理

【例 2.4.4】试证明表 2.3.1 中的式(17)，即

$$
A + B C = (A + B) (A + C)
$$

解：首先写出等式两边的对偶式，得到

$$
A \left(B + C\right) \quad {\text {和}} \quad A B + A C
$$

根据乘法分配律可知,这两个对偶式是相等的,亦即 $A(B+C)=AB+AC$ 。由对偶定理即可确定原来的两式也一定相等,于是式(17)得到证明。

如果仔细分析一下表2.3.1就能够发现，其中的公式(1)和(11)、(2)和(12)、(3)和(13)、(4)和(14)、(5)和(15)、(6)和(16)、(7)和(17)、(8)和(18)皆互为对偶式。因此，只要能证明公式(1)\~(8)成立，则公式(11)\~(18)已无需另做证明。

---

## Chunk 23/161：`ch02_sec_review_review_341`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_341 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_4_4 |
| next_chunk_id | ch02_sec_review_review_343 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L341–342 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.4.1 代入定理中对代入逻辑式的形式和复杂程度有无限制？

---

## Chunk 24/161：`ch02_sec_review_review_343`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_343 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_341 |
| next_chunk_id | ch02_sec_2_5_1_theory_348 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L343–344 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.4.2 利用反演定理对给定逻辑式求反时,应如何处理变换的优先顺序和式中所有的非运算符号?

---

## Chunk 25/161：`ch02_sec_2_5_1_theory_348`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_5_1_theory_348 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.5.1 逻辑函数 |
| section_id | ch02_sec_2_5_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.1 |
| prev_chunk_id | ch02_sec_review_review_343 |
| next_chunk_id | ch02_sec_2_5_2_theory_371 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L348–369 |

### 配图

**图2.5.1** — 举重裁判电路

![图2.5.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2ec7bafe6c78b632a91cacc044bc7c776e53d53755772ec0b6244e6f06a8f4c1.jpg)

*视觉描述：* 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.5.1 逻辑函数

从上面讲过的各种逻辑关系中可以看到,如果以逻辑变量作为输入,以运算结果作为输出,那么当输入变量的取值确定之后,输出的取值便随之而定。因此,输出与输入之间乃是一种函数关系。这种函数关系称为逻辑函数(logic function),写作

$$
Y = F (A, B, C, \dots)
$$

由于变量和输出(函数)的取值只有0和1两种状态,所以我们所讨论的都是二值逻辑函数。

任何一件具体的因果关系都可以用一个逻辑函数来描述。例如，图2.5.1所示是一个举重裁判电路，可以用一个逻辑函数描述它的逻辑功能。

比赛规则规定,在一名主裁判和两名副裁判中,必须有两人以上(而且必须包括主裁判)认定运动员的动作合格,试举才算成功。比赛时主裁判掌握着开关A,两名副裁判分别掌握着开关B和C。当运动员举起杠铃时,裁判认为动作合格了就合上开关,否则不合。显然,指示灯Y的状态(亮与暗)是开关A、B、C状态(合上与断开)的函数。

图 2.5.1 举重裁判电路

若以 1 表示开关闭合, 0 表示开关断开; 以 1 表示灯亮, 以 0 表示灯暗, 则指示灯 Y 是开关 A、B、C 的二值逻辑函数, 即

$$
Y = F (A, B, C)
$$

[图2.5.1] 举重裁判电路
[图2.5.1描述] 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

---

## Chunk 26/161：`ch02_sec_2_5_2_theory_371`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_5_2_theory_371 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.5.2 逻辑函数的描述方法 |
| section_id | ch02_sec_2_5_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_5_1_theory_348 |
| next_chunk_id | ch02_sec_一_逻辑真值表_theory_375 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L371–373 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.5.2 逻辑函数的描述方法

常用的逻辑函数描述方法有逻辑真值表、逻辑函数式（简称逻辑式或函数式）、逻辑图、波形图、卡诺图和硬件描述语言等。这一节只介绍前面四种方法，用卡诺图和硬件描述语言描述逻辑函数的方法将在后面做专门介绍。

---

## Chunk 27/161：`ch02_sec_一_逻辑真值表_theory_375`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑真值表_theory_375 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑真值表 |
| section_id | ch02_sec_一_逻辑真值表 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.1 |
| prev_chunk_id | ch02_sec_2_5_2_theory_371 |
| next_chunk_id | ch02_sec_二_逻辑函数式_theory_385 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L375–383 |

### 配图

**图2.5.1** — 举重裁判电路

![图2.5.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2ec7bafe6c78b632a91cacc044bc7c776e53d53755772ec0b6244e6f06a8f4c1.jpg)

*视觉描述：* 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑真值表

将输入变量所有的取值下对应的输出值找出来,列成表格,即可得到真值表。

仍以图 2.5.1 所示的举重裁判电路为例, 根据电路的工作原理不难看出, 只有 A=1, 同时 B、C 至少有一个为 1 时 Y 才等于 1, 于是可列出图 2.5.1 所示电路的真值表, 见表 2.5.1。

表 2.5.1 图 2.5.1 所示电路的真值表

<table><tr><td colspan="3">输入</td><td>输出</td></tr><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

[图2.5.1] 举重裁判电路
[图2.5.1描述] 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

---

## Chunk 28/161：`ch02_sec_二_逻辑函数式_theory_385`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数式_theory_385 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、逻辑函数式 |
| section_id | ch02_sec_二_逻辑函数式 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.1 |
| prev_chunk_id | ch02_sec_一_逻辑真值表_theory_375 |
| next_chunk_id | ch02_sec_三_逻辑图_theory_395 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L385–393 |

### 配图

**图2.5.1** — 举重裁判电路

![图2.5.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2ec7bafe6c78b632a91cacc044bc7c776e53d53755772ec0b6244e6f06a8f4c1.jpg)

*视觉描述：* 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、逻辑函数式

将输出与输入之间的逻辑关系写成与、或、非等运算的组合式，即逻辑代数式，就得到了所需的逻辑函数式。

在图2.5.1所示的电路中，根据对电路功能的要求和与、或的逻辑定义，“ $B$ 和 $C$ 中至少有一个合上”可以表示为 $(B + C)$ ，“同时还要求合上 $A$ ”，则应写作 $A\cdot (B + C)$ 。因此得到输出的逻辑函数式为

$$
Y = A (B + C)\tag{2.5.1}
$$

[图2.5.1] 举重裁判电路
[图2.5.1描述] 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

---

## Chunk 29/161：`ch02_sec_三_逻辑图_theory_395`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_三_逻辑图_theory_395 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 三、逻辑图 |
| section_id | ch02_sec_三_逻辑图 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.1, 图2.5.2 |
| prev_chunk_id | ch02_sec_二_逻辑函数式_theory_385 |
| next_chunk_id | ch02_sec_四_波形图_theory_404 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L395–402 |

### 配图

**图2.5.1** — 举重裁判电路

![图2.5.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2ec7bafe6c78b632a91cacc044bc7c776e53d53755772ec0b6244e6f06a8f4c1.jpg)

*视觉描述：* 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

**图2.5.2** — 描述图2.5.1电路逻辑功能的逻辑图

![图2.5.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/d4d5230cfe3f79486c5866159d4179f604ae8cd3472bc8b1b6a79051e343c025.jpg)

*视觉描述：* 图2.5.1的逻图：B、C经或门，再与A经与门得输出Y=A·(B+C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 三、逻辑图

将逻辑函数式中各变量之间的与、或、非等逻辑关系用图形符号表示出来, 就可以画出描述函数关系的逻辑图(logic diagram)。

为了画出描述图 2.5.1 电路功能的逻辑图, 只要用逻辑运算的图形符号代替式(2.5.1)中的代数运算符号便可得到图 2.5.2 所示的逻辑图。

图2.5.2 描述图2.5.1电路逻辑功能的逻辑图

[图2.5.1] 举重裁判电路
[图2.5.1描述] 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。
[图2.5.2] 描述图2.5.1电路逻辑功能的逻辑图
[图2.5.2描述] 图2.5.1的逻图：B、C经或门，再与A经与门得输出Y=A·(B+C)。

---

## Chunk 30/161：`ch02_sec_四_波形图_theory_404`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_四_波形图_theory_404 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 四、波形图 |
| section_id | ch02_sec_四_波形图 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.3 |
| prev_chunk_id | ch02_sec_三_逻辑图_theory_395 |
| next_chunk_id | ch02_sec_五_各种描述方法间的相互转换_theory_410 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L404–408 |

### 配图

**图2.5.3** — 描述图 2.5.1 电路逻辑功能的波形图

![图2.5.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/fd57c10b280833b08e86ffaa71cb78cfb6ed2d50823ba991984972ab8caa5a5d.jpg)

*视觉描述：* A、B、C及输出Y的时序波形，Y在A=1且(B或C为1)时为高，验证与或逻辑。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 四、波形图

如果将逻辑函数输入变量每一种可能出现的取值与对应的输出值按时间顺序依次排列起来,就得到了描述该逻辑函数的波形图。这种波形图(waveform)也称为时序图(timing diagram)。在逻辑分析仪和一些计算机仿真工具中,经常以这种波形图的形式给出分析结果。此外,也可以通过实验观察这些波形图,以检验实际逻辑电路的功能是否正确。

如果用波形图来描述式(2.5.1)的逻辑函数,则只需将表2.5.1给出的输入变量与对应的输出变量取值依时间顺序排列起来,就可以得到所要的波形图了(如图2.5.3所示)。

[图2.5.3] 描述图 2.5.1 电路逻辑功能的波形图
[图2.5.3描述] A、B、C及输出Y的时序波形，Y在A=1且(B或C为1)时为高，验证与或逻辑。

---

## Chunk 31/161：`ch02_sec_五_各种描述方法间的相互转换_theory_410`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_五_各种描述方法间的相互转换_theory_410 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.5.3, 图2.5.1 |
| prev_chunk_id | ch02_sec_四_波形图_theory_404 |
| next_chunk_id | ch02_eg2_5_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L410–421 |

### 配图

**图2.5.3** — 描述图 2.5.1 电路逻辑功能的波形图

![图2.5.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/fd57c10b280833b08e86ffaa71cb78cfb6ed2d50823ba991984972ab8caa5a5d.jpg)

*视觉描述：* A、B、C及输出Y的时序波形，Y在A=1且(B或C为1)时为高，验证与或逻辑。

**图2.5.1** — 举重裁判电路

![图2.5.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2ec7bafe6c78b632a91cacc044bc7c776e53d53755772ec0b6244e6f06a8f4c1.jpg)

*视觉描述：* 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

从上面的讨论中可以看到,这几种描述方式各具有不同的特点。因此,在实际应用中,需要选择一种最合适的方式来描述所讨论的逻辑函数。当讨论的逻辑函数不是用我们所希望的描述方式给出时,就必须将给出的描述方式转换成我们所需要的描述方式。

图 2.5.3 描述图 2.5.1 电路逻辑功能的波形图

既然同一个逻辑函数可以用多种不同的方法描述,那么这几种方法之间必能相互转换。

1. 真值表与逻辑函数式的相互转换

首先讨论从真值表得到逻辑函数式的方法。为了便于理解转换的原理，先来讨论下面一个具体的例子。

[图2.5.3] 描述图 2.5.1 电路逻辑功能的波形图
[图2.5.3描述] A、B、C及输出Y的时序波形，Y在A=1且(B或C为1)时为高，验证与或逻辑。
[图2.5.1] 举重裁判电路
[图2.5.1描述] 举重裁判电路：B、C并联后与A串联再驱动指示灯Y，体现Y=A·(B+C)。

---

## Chunk 32/161：`ch02_eg2_5_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | 例2.5.1 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_五_各种描述方法间的相互转换_theory_410 |
| next_chunk_id | ch02_eg2_5_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L422–449 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

【例 2.5.1】已知一个奇偶判别函数的真值表如表 2.5.2 所示, 试写出它的逻辑函数式。

表 2.5.2 例 2.5.1 的函数真值表

<table><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td> $1 \cdots\cdots\rightarrow A^{\prime}B^{\prime}C^{\prime}=1$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td> $1 \cdots\cdots\rightarrow A^{\prime}BC=1$ </td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td> $1 \cdots\cdots\rightarrow AB^{\prime}C=1$ </td></tr><tr><td>1</td><td>1</td><td>0</td><td> $1 \cdots\cdots\rightarrow ABC^{\prime}=1$ </td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

解：由真值表可见，只有当 A、B、C 三个输入变量中两个同时为 1 或三个同为 0 时，Y 才为 1。因此，在输入变量取值为以下四种情况时，Y 将等于 1：

$$
\begin{array}{l} {A = 0, B = 0, C = 0} \\ {A = 0, B = 1, C = 1} \\ {A = 1, B = 0, C = 1} \\ {A = 1, B = 1, C = 0} \end{array}
$$

而当 $A = 0, B = 0, C = 0$ 时，必然使乘积项 $A'B'C' = 1$ ；当 $A = 0, B = 1, C = 1$ 时，必然使乘积项 $A'BC = 1$ ；当 $A = 1, B = 0, C = 1$ 时，必然使乘积项 $AB'C = 1$ ；当 $A = 1, B = 1, C = 0$ 时，必然使 $ABC' = 1$ ，因此 $Y$ 的逻辑函数应当等于这四个乘积项之和，即

$$
Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C + A B ^ {\prime} C + A B C ^ {\prime}
$$

通过例 2.5.1 可以总结出由真值表写出逻辑函数式的一般方法, 这就是:

① 找出真值表中使逻辑函数 Y=1 的那些输入变量取值的组合。

② 每组输入变量取值的组合对应一个乘积项,其中取值为 1 的写入原变量,取值为 0 的写入反变量。

③ 将这些乘积项相加, 即得 Y 的逻辑函数式。

由逻辑式列出真值表就更简单了。这时只需将输入变量取值的所有组合状态逐一代入逻辑式求出函数值，列成表，即可得到真值表。

---

## Chunk 33/161：`ch02_eg2_5_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | 例2.5.2 |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_5_1 |
| next_chunk_id | ch02_eg2_5_3 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L450–463 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

【例 2.5.2】已知逻辑函数 $Y=A+B'C+A'BC'$ ，求它对应的真值表。

解：将 A、B、C 的各种取值逐一代入 Y 式中计算，将计算结果列表，即得表 2.5.3 所示的真值表。初学时为避免差错，可先将 $B^{\prime}C$ 、 $A^{\prime}BC^{\prime}$ 两项算出，然后将 A、 $B^{\prime}C$ 和 $A^{\prime}BC^{\prime}$ 相加求出 Y 的值。

表 2.5.3 例 2.5.2 的真值表

<table><tr><td>A</td><td>B</td><td>C</td><td> $B^{\prime}C$ </td><td> $A^{\prime}BC^{\prime}$ </td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr></table>

2. 逻辑函数式与逻辑图的相互转换

从给定的逻辑函数式转换为相应的逻辑图时, 只要用逻辑图形符号代替逻辑函数式中的逻辑运算符号并按运算优先顺序将它们连接起来, 就可以得到所求的逻辑图了。

而在从给定的逻辑图转换为对应的逻辑函数式时,只要从逻辑图的输入端到输出端逐级写出每个图形符号的输出逻辑式,就可以在输出端得到所求的逻辑函数式了。

---

## Chunk 34/161：`ch02_eg2_5_3`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_3 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | 例2.5.3 |
| figure_ids | 图2.5.4 |
| prev_chunk_id | ch02_eg2_5_2 |
| next_chunk_id | ch02_eg2_5_4 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L464–470 |

### 配图

**图2.5.4** — 例2.5.3的逻辑图

![图2.5.4](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/3cdc828a80cc61497d1814b88230dbdf1e1159e4b4a67f5a1bb636152b7388e6.jpg)

*视觉描述：* 例2.5.3逻辑图：输入A/B/C经非门得反变量；三输入与门得A'BC，二输入与门得B'C，再经或非门得(A+B'C)'，最后三输入或门合成Y=A'BC+(A+B'C)'+C'。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

【例 2.5.3】已知逻辑函数为 $Y=(A+B'C)'+A'BC'+C$ ，画出其对应的逻辑图。

解：将式中所有的与、或、非运算符号用图形符号代替，并依据运算优先顺序将这些图形符号连接起来，就得到了图2.5.4所示的逻辑图。

图2.5.4 例2.5.3的逻辑图

[图2.5.4] 例2.5.3的逻辑图
[图2.5.4描述] 例2.5.3逻辑图：输入A/B/C经非门得反变量；三输入与门得A'BC，二输入与门得B'C，再经或非门得(A+B'C)'，最后三输入或门合成Y=A'BC+(A+B'C)'+C'。

---

## Chunk 35/161：`ch02_eg2_5_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_4 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | 例2.5.4 |
| figure_ids | 图2.5.5 |
| prev_chunk_id | ch02_eg2_5_3 |
| next_chunk_id | ch02_eg2_5_5 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L471–489 |

### 配图

**图2.5.5** — 例2.5.4的逻辑图

![图2.5.5](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/525fd3b018cf075c0793242544068331b971208bedff58e1483d392b61c43cfd.jpg)

*视觉描述：* 例2.5.4逻辑图：用非门与或非门实现异或，中间标(A+B)'与(A'+B')'，输出Y=((A+B)'+(A'+B')')'，等价于A⊕B。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

【例 2.5.4】已知函数的逻辑图如图 2.5.5 所示, 试求它的逻辑函数式。

图2.5.5 例2.5.4的逻辑图

解：从输入端 A、B 开始逐个写出每个图形符号输出端的逻辑式，得到 $Y = ((A + B)' + (A' + B')')'$ 。将该式变换后得到

$$
\begin{array}{r l} Y & = \left(\left(A + B\right) ^ {\prime} + \left(A ^ {\prime} + B ^ {\prime}\right) ^ {\prime}\right) ^ {\prime} = \left(A + B\right) \left(A ^ {\prime} + B ^ {\prime}\right) \\ & = A B ^ {\prime} + A ^ {\prime} B = A \oplus B \end{array}
$$

可见，输出 Y 和 A、B 间是异或逻辑关系。

## 3. 波形图与真值表的相互转换

在从已知的逻辑函数波形图求对应的真值表时,首先需要从波形图上找出每个时间段里输入变量与函数输出的取值,然后将这些输入、输出取值对应列表,就得到了所求的真值表。

在将真值表转换为波形图时,只需将真值表中所有的输入变量与对应的输出变量取值依次排列画成以时间为横轴的波形,就得到了所求的波形图,如我们前面已经做过的那样。

[图2.5.5] 例2.5.4的逻辑图
[图2.5.5描述] 例2.5.4逻辑图：用非门与或非门实现异或，中间标(A+B)'与(A'+B')'，输出Y=((A+B)'+(A'+B')')'，等价于A⊕B。

---

## Chunk 36/161：`ch02_eg2_5_5`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_5 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、各种描述方法间的相互转换 |
| section_id | ch02_sec_五_各种描述方法间的相互转换 |
| exercise_id | — |
| example_id | 例2.5.5 |
| figure_ids | 图2.5.6 |
| prev_chunk_id | ch02_eg2_5_4 |
| next_chunk_id | ch02_sec_2_5_3_theory_502 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L490–500 |

### 配图

**图2.5.6** — 例2.5.5的波形图

![图2.5.6](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c8a2784c5667a0e4103c500d9c97c9912dcd6b3ad61fe299c460e4ac64221aae.jpg)

*视觉描述：* 例2.5.5时序波形图：输入A、B、C与输出Y随时间t1~t16变化，A为最低频方波、C为最高频脉冲，用于由波形列真值表并推导逻辑表达式。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、各种描述方法间的相互转换

【例 2.5.5】已知逻辑函数 Y 的波形图如图 2.5.6 所示, 试求该逻辑函数的真值表。

图2.5.6 例2.5.5的波形图

解：从 Y 的波形图上可以看出，在 $0 \sim t_{8}$ 时间区间里输入变量 A、B、C 所有可能的取值组合均已出现了，而且 $t_{8} \sim t_{16}$ 区间的波形只不过是 $0 \sim t_{8}$ 区间波形的重复。因此，只要将 $0 \sim t_{8}$ 区间每个时间段里 A、B、C 与 Y 的取值对应列表，即可得表 2.5.4 所示的真值表。

表 2.5.4 例 2.5.5 的真值表

<table><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

[图2.5.6] 例2.5.5的波形图
[图2.5.6描述] 例2.5.5时序波形图：输入A、B、C与输出Y随时间t1~t16变化，A为最低频方波、C为最高频脉冲，用于由波形列真值表并推导逻辑表达式。

---

## Chunk 37/161：`ch02_sec_2_5_3_theory_502`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_5_3_theory_502 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.5.3 逻辑函数的两种标准形式 |
| section_id | ch02_sec_2_5_3 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_5_5 |
| next_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L502–504 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.5.3 逻辑函数的两种标准形式

在讲述逻辑函数的标准形式之前,先介绍一下最小项和最大项的概念,然后再介绍逻辑函数的“最小项之和”及“最大项之积”这两种标准形式。

---

## Chunk 38/161：`ch02_sec_一_最小项和最大项_theory_506_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_最小项和最大项_theory_506_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、最小项和最大项 |
| section_id | ch02_sec_一_最小项和最大项 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_5_3_theory_502 |
| next_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L506–536 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、最小项和最大项

## 1. 最小项

在 n 变量逻辑函数中, 若 m 为包含 n 个因子的乘积项, 而且这 n 个变量均以原变量或反变量的形式在 m 中出现一次, 则称 m 为该组变量的最小项。

例如，A、B、C 三个变量的最小项有 $A^{\prime}B^{\prime}C^{\prime}$ 、 $A^{\prime}B^{\prime}C$ 、 $A^{\prime}BC^{\prime}$ 、 $A^{\prime}BC$ 、 $AB^{\prime}C^{\prime}$ 、 $AB^{\prime}C$ 、 $ABC^{\prime}$ 、ABC 共 8 个（即 $2^{3}$ 个）。n 变量的最小项应有 $2^{n}$ 个。

输入变量的每一组取值都使一个对应的最小项的值等于1。例如，在三变量A、B、C的最小项中，当 $A=1$ 、B=0、C=1时， $AB'C=1$ 。如果把 $AB'C$ 的取值101看作一个二进制数，那么它所表示的十进制数就是5。为了今后使用的方便，将 $AB'C$ 这个最小项记作 $m_{5}$ 。按照这一约定，就得到了三变量最小项的编号表，如表2.5.5所示。

表 2.5.5 三变量最小项的编号表

---

## Chunk 39/161：`ch02_sec_一_最小项和最大项_theory_506_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_最小项和最大项_theory_506_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、最小项和最大项 |
| section_id | ch02_sec_一_最小项和最大项 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p00 |
| next_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p02 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L506–536 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、最小项和最大项

<table><tr><td rowspan="2">最小项</td><td colspan="3">使最小项为1的变量取值</td><td rowspan="2">对应的十进制数</td><td rowspan="2">编号</td></tr><tr><td>A</td><td>B</td><td>C</td></tr><tr><td> $A'$   $B'$   $C'$ </td><td>0</td><td>0</td><td>0</td><td>0</td><td> $m_0$ </td></tr><tr><td> $A'$   $B'$   $C$ </td><td>0</td><td>0</td><td>1</td><td>1</td><td> $m_1$ </td></tr><tr><td> $A'$   $B$   $C'$ </td><td>0</td><td>1</td><td>0</td><td>2</td><td> $m_2$ </td></tr><tr><td> $A'$   $B$   $C$ </td><td>0</td><td>1</td><td>1</td><td>3</td><td> $m_3$ </td></tr><tr><td> $A$   $B'$   $C'$ </td><td>1</td><td>0</td><td>0</td><td>4</td><td> $m_4$ </td></tr><tr><td> $A$   $B'$   $C$ </td><td>1</td><td>0</td><td>1</td><td>5</td><td> $m_5$ </td></tr><tr><td> $A$   $B$   $C'$ </td><td>1</td><td>1</td><td>0</td><td>6</td><td> $m_6$ </td></tr><tr><td> $A$   $B$   $C$ </td><td>1</td><td>1</td><td>1</td><td>7</td><td> $m_7$ </td></tr></table>

根据同样的道理,我们将 A、B、C、D 这 4 个变量的 16 个最小项记作 $m_{0} \sim m_{15}$ 。

从最小项的定义出发可以证明它具有如下的重要性质：

① 在输入变量的任何取值下必有一个最小项，而且仅有一个最小项的值为 1。

② 全体最小项之和为 1。

③ 任意两个最小项的乘积为 0。

④ 具有相邻性的两个最小项之和可以合并成一项并消去一对因子。

---

## Chunk 40/161：`ch02_sec_一_最小项和最大项_theory_506_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_最小项和最大项_theory_506_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、最小项和最大项 |
| section_id | ch02_sec_一_最小项和最大项 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p01 |
| next_chunk_id | ch02_sec_2_最大项_theory_538_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L506–536 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、最小项和最大项

若两个最小项只有一个因子不同,则称这两个最小项具有相邻性。例如, $A^{\prime}BC^{\prime}$ 和 $ABC^{\prime}$ 两个最小项仅第一个因子不同,所以它们具有相邻性。这两个最小项相加时定能合并成一项并将一对不同的因子消去

$$
A ^ {\prime} B C ^ {\prime} + A B C ^ {\prime} = (A ^ {\prime} + A) B C ^ {\prime} = B C ^ {\prime}
$$

---

## Chunk 41/161：`ch02_sec_2_最大项_theory_538_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_最大项_theory_538_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2. 最大项 |
| section_id | ch02_sec_2_最大项 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_最小项和最大项_theory_506_p02 |
| next_chunk_id | ch02_sec_2_最大项_theory_538_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L538–566 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2. 最大项

在 n 变量逻辑函数中, 若 M 为 n 个变量之和, 而且这 n 个变量均以原变量或反变量的形式在 M 中出现一次, 则称 M 为该组变量的最大项。

例如，三变量 A、B、C 的最大项有 $(A'+B'+C')$ 、 $(A'+B'+C)$ 、 $(A'+B+C')$ 、 $(A'+B+C)$ 、 $(A+B'+C')$ 、 $(A+B'+C)$ 、 $(A+B+C')$ 、 $(A+B+C)$ 共 8 个（即 $2^{3}$ 个）。对于 n 个变量则有 $2^{n}$ 个最大项。可见，n 变量的最大项数目和最小项数目是相等的。

输入变量的每一组取值都使一个对应的最大项的值为0。例如，在三变量A、B、C的最大项中，当 $A=1$ 、 $B=0$ 、C=1时， $(A'+B+C')=0$ 。若将使最大项为0的ABC取值视为一个二进制数，并以其对应的十进制数给最大项编号，则 $(A'+B+C')$ 可记作 $M_{5}$ 。由此得到的三变量最大项编号表，如表2.5.6所示。

表 2.5.6 三变量最大项的编号表

---

## Chunk 42/161：`ch02_sec_2_最大项_theory_538_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_最大项_theory_538_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2. 最大项 |
| section_id | ch02_sec_2_最大项 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_最大项_theory_538_p00 |
| next_chunk_id | ch02_sec_二_逻辑函数的最小项之和形式_theory_568 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L538–566 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2. 最大项

<table><tr><td rowspan="2">最大项</td><td colspan="3">使最大项为0的变量取值</td><td rowspan="2">对应的十进制数</td><td rowspan="2">编号</td></tr><tr><td>A</td><td>B</td><td>C</td></tr><tr><td> $A + B + C$ </td><td>0</td><td>0</td><td>0</td><td>0</td><td> $M_0$ </td></tr><tr><td> $A + B + C'$ </td><td>0</td><td>0</td><td>1</td><td>1</td><td> $M_1$ </td></tr><tr><td> $A + B' + C$ </td><td>0</td><td>1</td><td>0</td><td>2</td><td> $M_2$ </td></tr><tr><td> $A + B' + C'$ </td><td>0</td><td>1</td><td>1</td><td>3</td><td> $M_3$ </td></tr><tr><td> $A' + B + C$ </td><td>1</td><td>0</td><td>0</td><td>4</td><td> $M_4$ </td></tr><tr><td> $A' + B + C'$ </td><td>1</td><td>0</td><td>1</td><td>5</td><td> $M_5$ </td></tr><tr><td> $A' + B' + C$ </td><td>1</td><td>1</td><td>0</td><td>6</td><td> $M_6$ </td></tr><tr><td> $A' + B' + C'$ </td><td>1</td><td>1</td><td>1</td><td>7</td><td> $M_7$ </td></tr></table>

根据最大项的定义同样也可以得到它的主要性质,这就是:

① 在输入变量的任何取值下必有一个最大项,而且只有一个最大项的值为 0。

② 全体最大项之积为 0。

③ 任意两个最大项之和为1。

④ 只有一个变量不同的两个最大项的乘积等于各相同变量之和。

如果将表 2.5.5 和表 2.5.6 加以对比则可发现, 最大项和最小项之间存在如下关系

$$
M _ {i} = m _ {i} ^ {\prime}\tag{2.5.2}
$$

例如， $m_0 = A'B'C'$ ，则 $m_0' = (A'B'C')' = A + B + C = M_0$

---

## Chunk 43/161：`ch02_sec_二_逻辑函数的最小项之和形式_theory_568`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数的最小项之和形式_theory_568 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、逻辑函数的最小项之和形式 |
| section_id | ch02_sec_二_逻辑函数的最小项之和形式 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_最大项_theory_538_p01 |
| next_chunk_id | ch02_eg2_5_6 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L568–588 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、逻辑函数的最小项之和形式

首先将给定的逻辑函数式化为若干乘积项之和的形式，亦称“积之和”（sum of products, 简称 SOP）形式。然后，再利用基本公式 $A + A' = 1$ 将每个乘积项中缺少的因子补全，这样就可以将与或的形式化为最小项之和的标准形式。这种标准形式在逻辑函数的化简以及计算机辅助分析和设计中得到了广泛的应用。

例如，给定逻辑函数为

$$
Y = A B C ^ {\prime} + B C
$$

则可化为

$$
Y = A B C ^ {\prime} + \left(A + A ^ {\prime}\right) B C = A B C ^ {\prime} + A B C + A ^ {\prime} B C = m _ {3} + m _ {6} + m _ {7}
$$

或写作

$$
Y (A, B, C) = \sum m (3, 6, 7)
$$

---

## Chunk 44/161：`ch02_eg2_5_6`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_6 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、逻辑函数的最小项之和形式 |
| section_id | ch02_sec_二_逻辑函数的最小项之和形式 |
| exercise_id | — |
| example_id | 例2.5.6 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_逻辑函数的最小项之和形式_theory_568 |
| next_chunk_id | ch02_sec_三_逻辑函数的最大项之积形式_theory_602 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L589–600 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、逻辑函数的最小项之和形式

【例 2.5.6】将逻辑函数 $Y=AB'C'D+A'CD+AC$ 展开为最小项之和的形式。

$$
\begin{array}{r l} \text { 解: } & Y = A B ^ {\prime} C ^ {\prime} D + A ^ {\prime} (B + B ^ {\prime}) C D + A (B + B ^ {\prime}) C \\ & = A B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C D + A ^ {\prime} B ^ {\prime} C D + A B C (D + D ^ {\prime}) + A B ^ {\prime} C (D + D ^ {\prime}) \\ & = A B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C D + A ^ {\prime} B ^ {\prime} C D + A B C D + A B C D ^ {\prime} + A B ^ {\prime} C D + A B ^ {\prime} C D ^ {\prime} \end{array}
$$

或写作

$$
Y (A, B, C, D) = \sum m (3, 7, 9, 1 0, 1 1, 1 4, 1 5)
$$

---

## Chunk 45/161：`ch02_sec_三_逻辑函数的最大项之积形式_theory_602`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_三_逻辑函数的最大项之积形式_theory_602 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 三、逻辑函数的最大项之积形式 |
| section_id | ch02_sec_三_逻辑函数的最大项之积形式 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_5_6 |
| next_chunk_id | ch02_eg2_5_7 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L602–604 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 三、逻辑函数的最大项之积形式

利用逻辑代数的基本公式和定理,首先我们一定能把任何一个逻辑函数式化成若干多项式相乘的或与形式(也称“和之积”形式)。然后再利用基本公式 $AA' = 0$ 将每个多项式中缺少的变量补齐,就可以将函数式的或与形式化成最大项之积的形式了。

---

## Chunk 46/161：`ch02_eg2_5_7`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_5_7 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 三、逻辑函数的最大项之积形式 |
| section_id | ch02_sec_三_逻辑函数的最大项之积形式 |
| exercise_id | — |
| example_id | 例2.5.7 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_三_逻辑函数的最大项之积形式_theory_602 |
| next_chunk_id | ch02_sec_review_review_627 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L605–624 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 三、逻辑函数的最大项之积形式

【例 2.5.7】将逻辑函数 $Y = A'B + AC$ 化为最大项之积的形式。

解：首先可以利用基本公式 $A + BC = (A + B)(A + C)$ 将 $Y$ 化成或与形式

$$
\begin{array}{r l} Y & = A ^ {\prime} B + A C \\ & = (A ^ {\prime} B + A) (A ^ {\prime} B + C) \\ & = (A + B) (A ^ {\prime} + C) (B + C) \end{array}
$$

然后在第一个括号内加入一项 $CC'$ ，在第二个括号内加入 $BB'$ ，在第三个括号内加入 $AA'$ ，于是得到

$$
\begin{array}{r l} Y & = (A + B + C C ^ {\prime}) (A ^ {\prime} + B B ^ {\prime} + C) (A A ^ {\prime} + B + C) \\ & = (A + B + C) (A + B + C ^ {\prime}) (A ^ {\prime} + B + C) (A ^ {\prime} + B ^ {\prime} + C) \end{array}
$$

或写作

$$
Y (A, B, C, D) = \prod M (0, 1, 4, 6)
$$

---

## Chunk 47/161：`ch02_sec_review_review_627`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_627 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_5_7 |
| next_chunk_id | ch02_sec_review_review_629 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L627–628 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.5.1 逻辑函数的描述方法有哪几种？你能把由任何一种描述方法给出的逻辑函数转换为由其他任何一种描述方法表示的逻辑函数吗？

---

## Chunk 48/161：`ch02_sec_review_review_629`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_629 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_627 |
| next_chunk_id | ch02_sec_2_6_1_theory_634 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L629–630 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.5.2 在逻辑函数的真值表和波形图中,任意改变各组输入和输出取值的排列顺序对函数有无影响?

---

## Chunk 49/161：`ch02_sec_2_6_1_theory_634`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_1_theory_634 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.6.1 公式化简法 |
| section_id | ch02_sec_2_6_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_629 |
| next_chunk_id | ch02_sec_一_并项法_theory_658 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L634–656 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.6.1 公式化简法

在进行逻辑运算时常常会看到，同一个逻辑函数可以写成不同的逻辑式，而这些逻辑式的繁简程度又相差甚远。逻辑式越是简单，它所表示的逻辑关系越明显，同时也有利于用最少的电子器件实现这个逻辑函数。因此，经常需要通过化简的手段找出逻辑函数的最简形式。

例如,有两个逻辑函数

$$
Y = A B C + B ^ {\prime} C + A C D\tag{2.6.1}
$$

$$
Y = A C + B ^ {\prime} C\tag{2.6.2}
$$

将它们的真值表分别列出后即可见到，它们是同一个逻辑函数。显然，下式比上式简单得多。

在与或逻辑函数式中,若其中包含的乘积项已经最少,而且每个乘积项里的因子也不能再减少时,则称此逻辑函数式为最简形式。对与或逻辑式最简形式的定义对其他形式的逻辑式同样也适用,即函数式中相加的乘积项不能再减少,而且每项中相乘的因子不能再减少时,则函数式为最简形式。

化简逻辑函数的目的就是要消去多余的乘积项和每个乘积项中多余的因子，以得到逻辑函数式的最简形式。常用的化简方法有公式化简法、卡诺图化简法以及适用于编制计算机辅助分析程序的Q-M法等。

公式化简法的原理就是反复使用逻辑代数的基本公式和常用公式消去函数式中多余的乘积项和多余的因子，以求得函数式的最简形式。

公式化简法没有固定的步骤。现将经常使用的方法归纳如下。

---

## Chunk 50/161：`ch02_sec_一_并项法_theory_658`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_并项法_theory_658 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、并项法 |
| section_id | ch02_sec_一_并项法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_1_theory_634 |
| next_chunk_id | ch02_eg2_6_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L658–660 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、并项法

利用表 2.3.3 中的公式 $AB + AB' = A$ 可以将两项合并为一项，并消去 B 和 $B'$ 这一对因子。而且，根据代入定理可知，A 和 B 均可以是任何复杂的逻辑式。

---

## Chunk 51/161：`ch02_eg2_6_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、并项法 |
| section_id | ch02_sec_一_并项法 |
| exercise_id | — |
| example_id | 例2.6.1 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_并项法_theory_658 |
| next_chunk_id | ch02_sec_二_吸收法_theory_674 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L661–672 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、并项法

【例2.6.1】试用并项法化简下列逻辑函数

$$
\begin{array}{l} Y _ {1} = A (B ^ {\prime} C D) ^ {\prime} + A B ^ {\prime} C D \\ Y _ {2} = A B ^ {\prime} + A C D + A ^ {\prime} B ^ {\prime} + A ^ {\prime} C D \end{array}
$$

解：

$$
\begin{array}{r l} & Y _ {3} = A ^ {\prime} B C ^ {\prime} + A C ^ {\prime} + B ^ {\prime} C ^ {\prime} \\ & Y _ {4} = B C ^ {\prime} D + B C D ^ {\prime} + B C ^ {\prime} D ^ {\prime} + B C D \\ & Y _ {1} = A ((B ^ {\prime} C D) ^ {\prime} + B ^ {\prime} C D) = A \\ & Y _ {2} = A (B ^ {\prime} + C D) + A ^ {\prime} (B ^ {\prime} + C D) = B ^ {\prime} + C D \\ & Y _ {3} = A ^ {\prime} B C ^ {\prime} + (A + B ^ {\prime}) C ^ {\prime} = (A ^ {\prime} B) C ^ {\prime} + (A ^ {\prime} B) ^ {\prime} C ^ {\prime} = C ^ {\prime} \\ & Y _ {4} = B (C ^ {\prime} D + C D ^ {\prime}) + B (C ^ {\prime} D ^ {\prime} + C D) \\ & \quad = B (C \oplus D) + B (C \oplus D) ^ {\prime} = B \end{array}
$$

---

## Chunk 52/161：`ch02_sec_二_吸收法_theory_674`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_吸收法_theory_674 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、吸收法 |
| section_id | ch02_sec_二_吸收法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_1 |
| next_chunk_id | ch02_eg2_6_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L674–676 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、吸收法

利用表 2.3.3 中的公式 $A+AB=A$ 可将 AB 项消去。A 和 B 同样也可以是任何一个复杂的逻辑式。

---

## Chunk 53/161：`ch02_eg2_6_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、吸收法 |
| section_id | ch02_sec_二_吸收法 |
| exercise_id | — |
| example_id | 例2.6.2 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_吸收法_theory_674 |
| next_chunk_id | ch02_sec_三_消项法_theory_686 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L677–684 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、吸收法

【例 2.6.2】试用吸收法化简下列逻辑函数

解：

$$
\begin{array}{r l} & Y _ {1} = ((A ^ {\prime} B) ^ {\prime} + C) A B D + A D \\ & Y _ {2} = A B + A B C ^ {\prime} + A B D + A B (C ^ {\prime} + D ^ {\prime}) \\ & Y _ {3} = A + (A ^ {\prime} (B C) ^ {\prime}) ^ {\prime} (A ^ {\prime} + (B ^ {\prime} C ^ {\prime} + D) ^ {\prime}) + B C \\ & Y _ {1} = ((A ^ {\prime} B) ^ {\prime} + C) B \cdot A D + A D = A D \\ & Y _ {2} = A B + A B (C ^ {\prime} + D + (C ^ {\prime} + D ^ {\prime})) = A B \\ & Y _ {3} = (A + B C) + (A + B C) (A ^ {\prime} + (B ^ {\prime} C ^ {\prime} + D) ^ {\prime}) = A + B C \end{array}
$$

---

## Chunk 54/161：`ch02_sec_三_消项法_theory_686`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_三_消项法_theory_686 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 三、消项法 |
| section_id | ch02_sec_三_消项法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_2 |
| next_chunk_id | ch02_eg2_6_3 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L686–688 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 三、消项法

利用表 2.3.3 中的公式 $AB + A'C + BC = AB + A'C$ 及 $AB + A'C + BCD = AB + A'C$ 将 BC 或 BCD 项消去。其中 A、B、C、D 均可以是任何复杂的逻辑式。

---

## Chunk 55/161：`ch02_eg2_6_3`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_3 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 三、消项法 |
| section_id | ch02_sec_三_消项法 |
| exercise_id | — |
| example_id | 例2.6.3 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_三_消项法_theory_686 |
| next_chunk_id | ch02_sec_四_消因子法_theory_698 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L689–696 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 三、消项法

【例 2.6.3】用消项法化简下列逻辑函数

解：

$$
\begin{array}{r l} & Y _ {1} = A C + A B ^ {\prime} + (B + C) ^ {\prime} \\ & Y _ {2} = A B ^ {\prime} C D ^ {\prime} + (A B ^ {\prime}) ^ {\prime} E + A ^ {\prime} C D ^ {\prime} E \\ & Y _ {3} = A ^ {\prime} B ^ {\prime} C + A B C + A ^ {\prime} B D ^ {\prime} + A B ^ {\prime} D ^ {\prime} + A ^ {\prime} B C D ^ {\prime} + B C D ^ {\prime} E ^ {\prime} \\ & \quad Y _ {1} = A C + A B ^ {\prime} + B ^ {\prime} C ^ {\prime} = A C + B ^ {\prime} C ^ {\prime} \\ & \quad Y _ {2} = (A B ^ {\prime}) C D ^ {\prime} + (A B ^ {\prime}) ^ {\prime} E + (C D ^ {\prime}) (E) A ^ {\prime} \\ & \quad \quad = A B ^ {\prime} C D ^ {\prime} + (A B ^ {\prime}) ^ {\prime} E \\ & \quad Y _ {3} = (A ^ {\prime} B ^ {\prime} + A B) C + (A ^ {\prime} B + A B ^ {\prime}) D ^ {\prime} + B C D ^ {\prime} (A ^ {\prime} + E ^ {\prime}) \\ & \quad \quad = (A \oplus B) ^ {\prime} C + (A \oplus B) D ^ {\prime} + C D ^ {\prime} (B (A ^ {\prime} + E ^ {\prime})) \\ & \quad \quad = (A \oplus B) ^ {\prime} C + (A \oplus B) D ^ {\prime} \end{array}
$$

---

## Chunk 56/161：`ch02_sec_四_消因子法_theory_698`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_四_消因子法_theory_698 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 四、消因子法 |
| section_id | ch02_sec_四_消因子法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_3 |
| next_chunk_id | ch02_eg2_6_4 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L698–700 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 四、消因子法

利用表 2.3.3 中的公式 $A + A'B = A + B$ 可将 $A'B$ 中的 $A'$ 消去。A、B 均可以是任何复杂的逻辑式。

---

## Chunk 57/161：`ch02_eg2_6_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_4 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 四、消因子法 |
| section_id | ch02_sec_四_消因子法 |
| exercise_id | — |
| example_id | 例2.6.4 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_四_消因子法_theory_698 |
| next_chunk_id | ch02_sec_五_配项法_theory_714 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L701–712 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 四、消因子法

【例 2.6.4】试利用消因子法化简下列逻辑函数

$$
\begin{array}{l} Y _ {1} = B ^ {\prime} + A B C \\ Y _ {2} = A B ^ {\prime} + B + A ^ {\prime} B \end{array}
$$

解：

$$
\begin{array}{r l} & Y _ {3} = A C + A ^ {\prime} D + C ^ {\prime} D \\ & Y _ {1} = B ^ {\prime} + A B C = B ^ {\prime} + A C \\ & Y _ {2} = A B ^ {\prime} + B + A ^ {\prime} B = A + B + A ^ {\prime} B = A + B \\ & Y _ {3} = A C + A ^ {\prime} D + C ^ {\prime} D = A C + (A ^ {\prime} + C ^ {\prime}) D = A C + (A C) ^ {\prime} D \\ & \quad = A C + D \end{array}
$$

---

## Chunk 58/161：`ch02_sec_五_配项法_theory_714`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_五_配项法_theory_714 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、配项法 |
| section_id | ch02_sec_五_配项法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_4 |
| next_chunk_id | ch02_eg2_6_5 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L714–716 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、配项法

① 根据基本公式中的 $A+A=A$ 可以在逻辑函数式中重复写入某一项,有时能获得更加简单的化简结果。

---

## Chunk 59/161：`ch02_eg2_6_5`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_5 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、配项法 |
| section_id | ch02_sec_五_配项法 |
| exercise_id | — |
| example_id | 例2.6.5 |
| figure_ids | — |
| prev_chunk_id | ch02_sec_五_配项法_theory_714 |
| next_chunk_id | ch02_eg2_6_6 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L717–726 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、配项法

【例 2.6.5】试化简逻辑函数 $Y = A'BC' + A'BC + ABC$ 。

解：若在式中重复写入 $A^{\prime}BC$ ，则可得到

$$
\begin{array}{r l} Y & = (A ^ {\prime} B C ^ {\prime} + A ^ {\prime} B C) + (A ^ {\prime} B C + A B C) \\ & = A ^ {\prime} B (C + C ^ {\prime}) + B C (A + A ^ {\prime}) \\ & = A ^ {\prime} B + B C \end{array}
$$

② 根据基本公式中的 $A+A'=1$ 可以在函数式中的某一项上乘以 $(A+A')$ ，然后拆成两项分别与其他项合并，有时能得到更加简单的化简结果。

---

## Chunk 60/161：`ch02_eg2_6_6`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_6 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、配项法 |
| section_id | ch02_sec_五_配项法 |
| exercise_id | — |
| example_id | 例2.6.6 |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_5 |
| next_chunk_id | ch02_eg2_6_7 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L727–736 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、配项法

【例 2.6.6】试化简逻辑函数 $Y=AB'+A'B+BC'+B'C$ 。

解：利用配项法可将 Y 写成

$$
\begin{array}{r l} Y & = A B ^ {\prime} + A ^ {\prime} B (C + C ^ {\prime}) + B C ^ {\prime} + (A + A ^ {\prime}) B ^ {\prime} C \\ & = A B ^ {\prime} + A ^ {\prime} B C + A ^ {\prime} B C ^ {\prime} + B C ^ {\prime} + A B ^ {\prime} C + A ^ {\prime} B ^ {\prime} C \\ & = (A B ^ {\prime} + A B ^ {\prime} C) + (B C ^ {\prime} + A ^ {\prime} B C ^ {\prime}) + (A ^ {\prime} B C + A ^ {\prime} B ^ {\prime} C) \\ & = A B ^ {\prime} + B C ^ {\prime} + A ^ {\prime} C \end{array}
$$

在化简复杂的逻辑函数时,往往需要灵活、交替地综合运用上述方法,才能得到最后的化简结果。

---

## Chunk 61/161：`ch02_eg2_6_7`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_7 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 五、配项法 |
| section_id | ch02_sec_五_配项法 |
| exercise_id | — |
| example_id | 例2.6.7 |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_6 |
| next_chunk_id | ch02_sec_2_6_2_theory_744 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L737–742 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 五、配项法

【例 2.6.7】化简逻辑函数

$$
\begin{array}{r l} & Y = A C + B ^ {\prime} C + B D ^ {\prime} + C D ^ {\prime} + A (B + C ^ {\prime}) + A ^ {\prime} B C D ^ {\prime} + A B ^ {\prime} D E \\ \text {解:} & Y = A C + B ^ {\prime} C + B D ^ {\prime} + \underbrace {C D ^ {\prime}} _ {} + A (B + C ^ {\prime}) + \underbrace {A ^ {\prime} B C D ^ {\prime}} _ {} + A B ^ {\prime} D E \\ & \Biggl \downarrow (\text {根据} A + A B = A, \text {消去} A ^ {\prime} B C D ^ {\prime}) \\ & = A C + \underbrace {B ^ {\prime} C} _ {} + B D ^ {\prime} + C D ^ {\prime} + A (\underbrace {B ^ {\prime} C} _ {}) ^ {\prime} + A B ^ {\prime} D E \\ & \Biggl \downarrow (\text {根据} A + A ^ {\prime} B = A + B, \text {消去} A (\underbrace {B ^ {\prime} C} _ {}) ^ {\prime} \text {中的} (B ^ {\prime} C) ^ {\prime} \text {因子}) \\ & = \underbrace {A C + B ^ {\prime} C + B D ^ {\prime} + C D ^ {\prime}} _ {} + \underbrace {A + A B ^ {\prime} D E} _ {} \\ & \Biggl \downarrow (\text {根据} A + A B = A, \text {消去} A C \text {和} A B ^ {\prime} D E) \\ & = A + \underbrace {B ^ {\prime} C} _ {} + \underbrace {B D ^ {\prime}} _ {} + \underbrace {C D ^ {\prime}} _ {} \\ & \Biggl \downarrow (\text {根据} A B + A ^ {\prime} C + B C = A B + A ^ {\prime} C, \text {消去} C D ^ {\prime}) \\ & = A + B ^ {\prime} C + B D ^ {\prime} \end{array}
$$

---

## Chunk 62/161：`ch02_sec_2_6_2_theory_744`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_2_theory_744 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.6.2 卡诺图化简法 |
| section_id | ch02_sec_2_6_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_7 |
| next_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L744–750 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.6.2 卡诺图化简法

从前面公式化简法的例题中可以看出,用公式运算的方法化简不同的逻辑函数时,没有固定的方法和步骤,存在很大的灵活性。用这种方法化简复杂的逻辑函数时,必须具备熟练掌握和灵活运用逻辑代数的公式和定理的能力,方能得到满意的化简结果。因此,我们希望能找到一种对任何逻辑函数都适用的,而且具有固定操作步骤和方法的化简方法。

于是我们想到,既然任何逻辑函数都可以展开为最小项之和的形式,那么采用合并最小项的方法化简逻辑函数,就应当是适用于任何逻辑函数的、通用的化简方法。

下面介绍的卡诺图化简法就是一种基于合并最小项的化简方法。

---

## Chunk 63/161：`ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法 |
| section_id | ch02_sec_一_逻辑函数的卡诺图表示法 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.6.1 |
| prev_chunk_id | ch02_sec_2_6_2_theory_744 |
| next_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L752–784 |

### 配图

**图2.6.1** — 二到五变量最小项的卡诺图

![图2.6.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/8ddfd8c067b03e7249c306e627cdf8f8afee6c225d3ccb2578e586a5a8762bb4.jpg)

*视觉描述：* 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法

将 n 变量的全部最小项各用一个小方块表示，并使具有逻辑相邻性的最小项在几何位置上也相邻地排列起来，所得到的图形称为 n 变量最小项的卡诺图。因为这种表示方法是由美国工程师卡诺（M.Karnaugh）首先提出的，所以将这种图形称为卡诺图（Karnaugh Map）。

图 2.6.1 中画出了二到五变量最小项的卡诺图。图形两侧标注的 0 和 1 表示使对应小方格内的最小项为 1 的变量取值。同时，这些 0 和 1 组成的二进制数所对应的十进制数大小也就是对应的最小项的编号。

(a)

<table><tr><td>A\BC</td><td>00</td><td>01</td><td>11</td><td>10</td></tr><tr><td>0</td><td> $m_0$ </td><td> $m_1$ </td><td> $m_3$ </td><td> $m_2$ </td></tr><tr><td>1</td><td> $m_4$ </td><td> $m_5$ </td><td> $m_7$ </td><td> $m_6$ </td></tr></table>

(b)

<table><tr><td>AB\CD</td><td>00</td><td>01</td><td>11</td><td>10</td></tr><tr><td>00</td><td> $m_0$ </td><td> $m_1$ </td><td> $m_3$ </td><td> $m_2$ </td></tr><tr><td>01</td><td> $m_4$ </td><td> $m_5$ </td><td> $m_7$ </td><td> $m_6$ </td></tr><tr><td>11</td><td> $m_{12}$ </td><td> $m_{13}$ </td><td> $m_{15}$ </td><td> $m_{14}$ </td></tr><tr><td>10</td><td> $m_8$ </td><td> $m_9$ </td><td> $m_{11}$ </td><td> $m_{10}$ </td></tr></table>

(c)

[图2.6.1] 二到五变量最小项的卡诺图
[图2.6.1描述] 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

---

## Chunk 64/161：`ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法 |
| section_id | ch02_sec_一_逻辑函数的卡诺图表示法 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.6.1 |
| prev_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p00 |
| next_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p02 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L752–784 |

### 配图

**图2.6.1** — 二到五变量最小项的卡诺图

![图2.6.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/8ddfd8c067b03e7249c306e627cdf8f8afee6c225d3ccb2578e586a5a8762bb4.jpg)

*视觉描述：* 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法

<table><tr><td>AB\CDE</td><td>000</td><td>001</td><td>011</td><td>010</td><td>110</td><td>111</td><td>101</td><td>100</td></tr><tr><td>00</td><td> $m_0$ </td><td> $m_1$ </td><td> $m_3$ </td><td> $m_2$ </td><td> $m_6$ </td><td> $m_7$ </td><td> $m_5$ </td><td> $m_4$ </td></tr><tr><td>01</td><td> $m_8$ </td><td> $m_9$ </td><td> $m_{11}$ </td><td> $m_{10}$ </td><td> $m_{14}$ </td><td> $m_{15}$ </td><td> $m_{13}$ </td><td> $m_{12}$ </td></tr><tr><td>11</td><td> $m_{24}$ </td><td> $m_{25}$ </td><td> $m_{27}$ </td><td> $m_{26}$ </td><td> $m_{30}$ </td><td> $m_{31}$ </td><td> $m_{29}$ </td><td> $m_{28}$ </td></tr><tr><td>10</td><td> $m_{16}$ </td><td> $m_{17}$ </td><td> $m_{19}$ </td><td> $m_{18}$ </td><td> $m_{22}$ </td><td> $m_{23}$ </td><td> $m_{21}$ </td><td> $m_{20}$ </td></tr></table>

(d)  
图 2.6.1 二到五变量最小项的卡诺图  
(a) 两变量 $(A, B)$ 最小项的卡诺图 (b) 三变量 $(A, B, C)$ 最小项的卡诺图  
(c) 四变量 $(A, B, C, D)$ 最小项的卡诺图 (d) 五变量 $(A, B, C, D, E)$ 最小项的卡诺图

为了保证图中几何位置相邻的最小项在逻辑上也具有相邻性,这些数码不能按自然二进制数从小到大地顺序排列,而必须按图中的方式排列,以确保相邻的两个最小项仅有一个变量是不

同的。

从图 2.6.1 所示的卡诺图上还可以看到,处在任何一行或一列两端的最小项也仅有一个变量不同,所以它们也具有逻辑相邻性。因此,从几何位置上应当将卡诺图看成是上下、左右闭合的图形。

[图2.6.1] 二到五变量最小项的卡诺图
[图2.6.1描述] 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

---

## Chunk 65/161：`ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法 |
| section_id | ch02_sec_一_逻辑函数的卡诺图表示法 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.6.1 |
| prev_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p01 |
| next_chunk_id | ch02_eg2_6_8 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L752–784 |

### 配图

**图2.6.1** — 二到五变量最小项的卡诺图

![图2.6.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/8ddfd8c067b03e7249c306e627cdf8f8afee6c225d3ccb2578e586a5a8762bb4.jpg)

*视觉描述：* 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法

在变量数大于、等于五以后，仅仅用几何图形在两维空间的相邻性来表示逻辑相邻性已经不够了。例如，在图2.6.1(d)所示的五变量最小项的卡诺图中，除了几何位置相邻的最小项具有逻辑相邻性以外，以图中双竖线为轴左右对称位置上的两个最小项也具有逻辑相邻性。

既然任何一个逻辑函数都能表示为若干最小项之和的形式,那么自然也就可以设法用卡诺图来表示任意一个逻辑函数。具体的方法是:首先将逻辑函数化为最小项之和的形式,然后在卡诺图上与这些最小项对应的位置上填入1,在其余的位置上填入0,就得到了表示该逻辑函数的卡诺图。也就是说,任何一个逻辑函数都等于它的卡诺图中填入1的那些最小项之和。

[图2.6.1] 二到五变量最小项的卡诺图
[图2.6.1描述] 二至五变量最小项卡诺图标准结构：依次给出2×2、2×4、4×4及4×8格图的变量排列与m0起的最小项编号，行列均按格雷码编码排列。

---

## Chunk 66/161：`ch02_eg2_6_8`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_8 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法 |
| section_id | ch02_sec_一_逻辑函数的卡诺图表示法 |
| exercise_id | — |
| example_id | 例2.6.8 |
| figure_ids | 图2.6.2 |
| prev_chunk_id | ch02_sec_一_逻辑函数的卡诺图表示法_theory_752_p02 |
| next_chunk_id | ch02_eg2_6_9 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L785–804 |

### 配图

**图2.6.2** — 例2.6.8的卡诺图

![图2.6.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/49392bea931a9555853228bb5e9c028040fbb0d35b3b3ddbc4cf790207834442.jpg)

*视觉描述：* 例2.6.8四变量AB-CD卡诺图：m1、m4、m6、m15及AB=10行共五处为1，其余格为0，供按相邻规则圈组合并化简逻辑函数。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法

【例 2.6.8】用卡诺图表示逻辑函数

$$
Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B D ^ {\prime} + A C D + A B ^ {\prime}
$$

解：首先将 $Y$ 化为最小项之和的形式

$$
\begin{array}{r l} Y & = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B (C + C ^ {\prime}) D ^ {\prime} + A (B + B ^ {\prime}) C D + A B ^ {\prime} (C + C ^ {\prime}) (D + D ^ {\prime}) \\ & = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C D ^ {\prime} + A ^ {\prime} B C ^ {\prime} D ^ {\prime} + A B C D + A B ^ {\prime} C D + A B ^ {\prime} C D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D \\ & \quad + A B ^ {\prime} C ^ {\prime} D ^ {\prime} \\ & = m _ {1} + m _ {4} + m _ {6} + m _ {8} + m _ {9} + m _ {1 0} + m _ {1 1} + m _ {1 5} \end{array}
$$

画出四变量最小项的卡诺图，在对应于函数式中各最小项的位置上填入1，其余位置上填入0，就得到如图2.6.2所示的函数 $Y$ 的卡诺图。

图2.6.2 例2.6.8的卡诺图

图2.6.3 例2.6.9的卡诺图

[图2.6.2] 例2.6.8的卡诺图
[图2.6.2描述] 例2.6.8四变量AB-CD卡诺图：m1、m4、m6、m15及AB=10行共五处为1，其余格为0，供按相邻规则圈组合并化简逻辑函数。

---

## Chunk 67/161：`ch02_eg2_6_9`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_9 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法 |
| section_id | ch02_sec_一_逻辑函数的卡诺图表示法 |
| exercise_id | — |
| example_id | 例2.6.9 |
| figure_ids | 图2.6.3 |
| prev_chunk_id | ch02_eg2_6_8 |
| next_chunk_id | ch02_sec_二_用卡诺图化简逻辑函数_theory_814 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L805–812 |

### 配图

**图2.6.3** — 例2.6.9的卡诺图

![图2.6.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/6f470e357c56ab91019e14c663be2b46b7f149e2a17e488943c6bf14e8f35d85.jpg)

*视觉描述：* 例2.6.9三变量A-BC卡诺图：1呈棋盘格分布于m1、m2、m4、m7，相邻1均不可合并，对应三变量异或函数Y=A⊕B⊕C。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 一、逻辑函数的卡诺图表示法

【例 2.6.9】已知逻辑函数 Y 的卡诺图如图 2.6.3 所示，试写出该函数的逻辑式。

解：因为函数 Y 等于卡诺图中填入 1 的那些最小项之和，所以有

$$
Y = A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A B C + A ^ {\prime} B C ^ {\prime}
$$

[图2.6.3] 例2.6.9的卡诺图
[图2.6.3描述] 例2.6.9三变量A-BC卡诺图：1呈棋盘格分布于m1、m2、m4、m7，相邻1均不可合并，对应三变量异或函数Y=A⊕B⊕C。

---

## Chunk 68/161：`ch02_sec_二_用卡诺图化简逻辑函数_theory_814`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_用卡诺图化简逻辑函数_theory_814 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 二、用卡诺图化简逻辑函数 |
| section_id | ch02_sec_二_用卡诺图化简逻辑函数 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.6.4(a), 图2.6.4(b), 图2.6.4(c), 图2.6.4(d), 图2.6.4(e) |
| prev_chunk_id | ch02_eg2_6_9 |
| next_chunk_id | ch02_sec_2_theory_865 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L814–863 |

### 配图

**图2.6.4(a)** — 最小项相邻的几种情况 子图(a)

![图2.6.4(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/163a56243e6b1b37f37794ac699ef9e706ffb0a95b709c50de4b595bebb8e2d0.jpg)

*视觉描述：* 三变量卡诺图最小项相邻示例(a)：A=0行BC=01/11水平圈、BC=11列垂直圈及BC=00/10跨边绕回圈，演示多种相邻合并规则。

**图2.6.4(b)** — 最小项相邻的几种情况 子图(b)

![图2.6.4(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/9b28aa32453e1c522e786c4fef2aa37b86e698e1cfda9599adfe7133132c29c1.jpg)

*视觉描述：* 四变量卡诺图最小项相邻示例(b)：八个1经BCD八格圈、A'BC四格圈及跨列ABD'四格圈等多组合并，展示格雷码下各类邻接方式。

**图2.6.4(c)** — 最小项相邻的几种情况 子图(c)

![图2.6.4(c)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c29eaca1b52ef29a43b7963807ce967e15ce82ddbe855ec4316536a02cdf86e2.jpg)

*视觉描述：* 三变量卡诺图最小项相邻示例(c)：八格全为1，中间BC=01/11两列圈为B，首尾BC=00/10绕回圈为B'，说明B+B'=1恒真函数化简。

**图2.6.4(d)** — 最小项相邻的几种情况 子图(d)

![图2.6.4(d)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/9264b5cf377533f50c5ac360b6f821d2c141223d207fbe9963ec5719a9f7725c.jpg)

*视觉描述：* 四变量卡诺图最小项相邻示例(d)：标注B=1且D=1的2×2方块合并为BD，另有CD=11四格圈及跨左右边界八格圈，演示多级圈组化简。

**图2.6.4(e)** — 最小项相邻的几种情况 子图(e)

![图2.6.4(e)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/ae426005887ee4857088f14aa5fb1c21a692f35256fadb5425e568a0a6d8b00c.jpg)

*视觉描述：* 四变量卡诺图最小项相邻示例(e)：前两行(A=0)八格圈为A'，首尾两列(CD=00/10)绕回八格圈为D'，合并得最简与或式F=A'+D'。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 二、用卡诺图化简逻辑函数

利用卡诺图化简逻辑函数的方法称为卡诺图化简法或图形化简法。化简时依据的基本原理就是具有相邻性的最小项可以合并，并消去不同的因子。由于在卡诺图上几何位置相邻与逻辑上的相邻性是一致的，因而从卡诺图上能直观地找出那些具有相邻性的最小项并将其合并化简。

## 1. 合并最小项的原则

若两个最小项相邻，则可合并为一项并消去一对因子。合并后的结果中只剩下公共因子。

在图 2.6.4(a) 和 (b) 中画出了两个最小项相邻的几种可能情况。例如，图 (a) 中 $A^{\prime}BC(m_{3})$ 和 $ABC(m_{7})$ 相邻，故可合并为

$$
A ^ {\prime} B C + A B C = (A ^ {\prime} + A) B C = B C
$$

合并后将 A 和 $A'$ 一对因子消掉了，只剩下公共因子 B 和 C。

(a)

(b)

(c)

(d)

(e)  
图 2.6.4 最小项相邻的几种情况  
(a)、(b) 两个最小项相邻 (c)、(d) 四个最小项相邻 (e) 八个最小项相邻

若四个最小项相邻并排列成一个矩形组,则可合并为一项并消去两对因子。合并后的结果中只包含公共因子。

例如，在图2.6.4(d)中， $A^{\prime}BC^{\prime}D(m_{5})$ 、 $A^{\prime}BCD(m_{7})$ 、 $ABC^{\prime}D(m_{13})$ 和 $ABCD(m_{15})$ 相邻，故可合并。合并后得到

$$
\begin{array}{r l} & A ^ {\prime} B C ^ {\prime} D + A ^ {\prime} B C D + A B C ^ {\prime} D + A B C D \\ & = A ^ {\prime} B D (C + C ^ {\prime}) + A B D (C + C ^ {\prime}) \\ & = B D (A + A ^ {\prime}) = B D \end{array}
$$

可见，合并后消去了 $A, A'$ 和 $C, C'$ 两对因子，只剩下四个最小项的公共因子 $B$ 和 $D$ 。

若八个最小项相邻并且排列成一个矩形组,则可合并为一项并消去三对因子。合并后的结果中只包含公共因子。

例如，在图 2.6.4(e) 中，上边两行的八个最小项是相邻的，可将它们合并为一项 $A'$ 。其他的

因子都被消去了。

至此,可以归纳出合并最小项的一般规则,这就是:如果有 $2^{n}$ 个最小项相邻 $(n=1,2,\cdots)$ 并排列成一个矩形组,则它们可以合并为一项,并消去n对因子。合并后的结果中仅包含这些最小项的公共因子。

[图2.6.4(a)] 最小项相邻的几种情况 子图(a)
[图2.6.4(a)描述] 三变量卡诺图最小项相邻示例(a)：A=0行BC=01/11水平圈、BC=11列垂直圈及BC=00/10跨边绕回圈，演示多种相邻合并规则。
[图2.6.4(b)] 最小项相邻的几种情况 子图(b)
[图2.6.4(b)描述] 四变量卡诺图最小项相邻示例(b)：八个1经BCD八格圈、A'BC四格圈及跨列ABD'四格圈等多组合并，展示格雷码下各类邻接方式。
[图2.6.4(c)] 最小项相邻的几种情况 子图(c)
[图2.6.4(c)描述] 三变量卡诺图最小项相邻示例(c)：八格全为1，中间BC=01/11两列圈为B，首尾BC=00/10绕回圈为B'，说明B+B'=1恒真函数化简。
[图2.6.4(d)] 最小项相邻的几种情况 子图(d)
[图2.6.4(d)描述] 四变量卡诺图最小项相邻示例(d)：标注B=1且D=1的2×2方块合并为BD，另有CD=11四格圈及跨左右边界八格圈，演示多级圈组化简。
[图2.6.4(e)] 最小项相邻的几种情况 子图(e)
[图2.6.4(e)描述] 四变量卡诺图最小项相邻示例(e)：前两行(A=0)八格圈为A'，首尾两列(CD=00/10)绕回八格圈为D'，合并得最简与或式F=A'+D'。

---

## Chunk 69/161：`ch02_sec_2_theory_865`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_865 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2 卡诺图化简法的步骤 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_用卡诺图化简逻辑函数_theory_814 |
| next_chunk_id | ch02_eg2_6_10 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L865–881 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2 卡诺图化简法的步骤

用卡诺图化简逻辑函数时可按如下步骤进行：

(1) 将函数化为最小项之和的形式。

(2) 画出表示该逻辑函数的卡诺图。

(3) 找出可以合并的最小项。

（4）选取化简后的乘积项。选取的原则是：

① 这些乘积项应包含函数式中所有的最小项（应覆盖卡诺图中所有的 1）。

② 所用的乘积项数目最少。也就是可合并的最小项组成的矩形组数目最少。

③ 每个乘积项包含的因子最少。也就是每个可合并的最小项矩形组中应包含尽量多的最小项。

---

## Chunk 70/161：`ch02_eg2_6_10`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_10 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2 卡诺图化简法的步骤 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | 例2.6.10 |
| figure_ids | 图2.6.5(a), 图2.6.5(b) |
| prev_chunk_id | ch02_sec_2_theory_865 |
| next_chunk_id | ch02_eg2_6_11 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L882–914 |

### 配图

**图2.6.5(a)** — 例 2.6.10 的卡诺图 子图(a)

![图2.6.5(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/8ba11bab586972c14b92fde604cd36db985aa5f812a7bccb05e70c1b2e2f5d90.jpg)

*视觉描述：* 例2.6.10卡诺图(a)：三变量A-BC图，三对相邻1分别圈为A'C、AB'、BC'，按最小项合并规则化简得Y=A'C+AB'+BC'。

**图2.6.5(b)** — 例 2.6.10 的卡诺图 子图(b)

![图2.6.5(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/24a7738d47731e68c614774dc760ef9024f48146df5545cc730eeb693727d358.jpg)

*视觉描述：* 例2.6.10卡诺图(b)：同一函数的另一组圈——BC=01列(B'C)、A=0行BC=11/10(A'B)及A=1行绕回(AC')，得Y=B'C+A'B+AC'。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2 卡诺图化简法的步骤

【例 2.6.10】用卡诺图化简法将下式化简为最简与或函数式

$$
Y = A C ^ {\prime} + A ^ {\prime} C + B C ^ {\prime} + B ^ {\prime} C
$$

解：首先画出表示函数 Y 的卡诺图，如图 2.6.5 所示。

(a)

(b)  
图 2.6.5 例 2.6.10 的卡诺图

事实上在填写 $Y$ 的卡诺图时，并不一定要将 $Y$ 化为最小项之和的形式。例如，式中的 $AC'$ 一项包含了所有含有 $AC'$ 因子的最小项，而不管另一个因子是 $B$ 还是 $B'$ 。从另外一个角度讲，也可以理解为 $AC'$ 是 $ABC'$ 和 $AB'C'$ 两个最小项相加合并的结果。因此，在填写 $Y$ 的卡诺图时，可以直接在卡诺图上所有对应 $A = 1, C = 0$ 的空格里填入 1。按照这种方法，就可以省去将 $Y$ 化为最小项之和这一步骤了。

其次,需要找出可以合并的最小项。将可能合并的最小项用线圈出。由图2.6.5(a)和(b)可见,有两种可取的合并最小项的方案。如果按图2.6.5(a)的方案合并最小项,则得到

$$
Y = A B ^ {\prime} + A ^ {\prime} C + B C ^ {\prime}
$$

而按图2.6.5(b)的方案合并最小项得到

$$
Y = A C ^ {\prime} + B ^ {\prime} C + A ^ {\prime} B
$$

两个化简结果都符合最简与或式的标准。

此例说明,有时一个逻辑函数的化简结果不是唯一的。

[图2.6.5(a)] 例 2.6.10 的卡诺图 子图(a)
[图2.6.5(a)描述] 例2.6.10卡诺图(a)：三变量A-BC图，三对相邻1分别圈为A'C、AB'、BC'，按最小项合并规则化简得Y=A'C+AB'+BC'。
[图2.6.5(b)] 例 2.6.10 的卡诺图 子图(b)
[图2.6.5(b)描述] 例2.6.10卡诺图(b)：同一函数的另一组圈——BC=01列(B'C)、A=0行BC=11/10(A'B)及A=1行绕回(AC')，得Y=B'C+A'B+AC'。

---

## Chunk 71/161：`ch02_eg2_6_11`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_6_11 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2 卡诺图化简法的步骤 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | 例2.6.11 |
| figure_ids | 图2.6.6 |
| prev_chunk_id | ch02_eg2_6_10 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L915–949 |

### 配图

**图2.6.6** — 例2.6.11的卡诺图

![图2.6.6](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/d149710b475adec671f90ab152d31a55539f1f442578fb2d47f61ea27103d8d9.jpg)

*视觉描述：* 例2.6.11四变量卡诺图：CD=00与10两列绕回八格圈(D')，AB=11与10两行八格圈(A)，其余格为0，最简与或式Y=A+D'。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2 卡诺图化简法的步骤

【例 2.6.11】用卡诺图化简法将下式化为最简与或逻辑式

$$
Y = A B C + A B D + A C ^ {\prime} D + C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C + A ^ {\prime} C D ^ {\prime}
$$

解：首先画出 Y 的卡诺图，如图 2.6.6 所示。然后将可能合并的最小项圈出，并按照前面

所述的原则选择化简后与或式中的乘积项。由图可见，应将图中下边两行的8个最小项合并，同时将左、右两列最小项合并，于是得到

$$
Y = A + D ^ {\prime}
$$

从图2.6.6中可以看到， $A$ 和 $D^{\prime}$ 中重复包含了 $m_{8}, m_{10}, m_{12}$ 和 $m_{14}$ 这4个最小项。但据 $A + A = A$ 可知，在合并最小项的过程中允许重复使用函数式中的最小项，以利于得到更简单的化简结果。

图2.6.6 例2.6.11的卡诺图

另外,还要补充说明一个问题。在以上的两个例子中,我们

都是通过合并卡诺图中的1来求得化简结果的。但有时也可以通过合并卡诺图中的0先求出 $Y'$ 的化简结果，然后再将 $Y'$ 求反而得到Y。

这种方法所依据的原理我们已在2.5.4节中做过说明。因为全部最小项之和为1，所以若将全部最小项之和分成两部分，一部分（卡诺图中填入1的那些最小项）之和记作 $Y$ ，则根据 $Y + Y' = 1$ 可知，其余一部分（卡诺图中填入0的那些最小项）之和必为 $Y'$ 。

在多变量逻辑函数的卡诺图中, 当 0 的数目远小于 1 的数目时, 采用合并 0 的方法有时会比合并 1 来得简单。例如, 在图 2.6.6 所示的卡诺图中, 如果将 0 合并, 则可立即写出

$$
Y ^ {\prime} = A ^ {\prime} D, \quad Y = ((Y ^ {\prime})) ^ {\prime} = (A ^ {\prime} D) ^ {\prime} = A + D ^ {\prime}
$$

与合并1得到的化简结果一致。

此外，在需要将函数化为最简的与或非式时，采用合并0的方式最为适宜，因为得到的结果正是与或非形式。如果要求得到 $Y'$ 的化简结果，则采用合并0的方式就更简便了。

[图2.6.6] 例2.6.11的卡诺图
[图2.6.6描述] 例2.6.11四变量卡诺图：CD=00与10两列绕回八格圈(D')，AB=11与10两行八格圈(A)，其余格为0，最简与或式Y=A+D'。

---

## Chunk 72/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_6_11 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

从上一小节的内容中不难看出，虽然卡诺图化简法具有直观、简单的优点，但它同时又存在着很大的局限性。首先，在函数的输入逻辑变量较多时（例如大于5以后），便失掉了直观的优点。其次，在许多情况下要凭设计者的经验确定应如何合并最小项才能得到最简单的化简结果，因而不便于借助计算机完成化简工作。

公式化简法的使用虽然不受输入变量数目的影响,但由于化简的过程没有固定的、通用的步骤可循,所以同样不适用于计算机辅助化简。

由奎恩(W.V.Quine)和麦克拉斯基(E.J.McCluskey)提出的用列表方式进行化简的方法则有一定的规则和步骤可循，较好地克服了公式化简法和卡诺图化简法在这方面的局限性，因而适用于编制计算机辅助化简程序。通常将这种化简方法称为奎恩-麦克拉斯基法，简称Q-M法。

Q-M 法的基本原理仍然是通过合并相邻最小项并消去多余因子而求得逻辑函数的最简与

或式。下面再结合一个具体的例子简要地介绍一下 Q-M 法的基本原理和化简的步骤。

假定需要化简的五变量逻辑函数为

$$
\begin{array}{r l} Y (A, B, C, D, E) & = A B ^ {\prime} C D E ^ {\prime} + A ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B D E ^ {\prime} \\ & \quad + B C D E + A B C ^ {\prime} (D \oplus E) ^ {\prime} \end{array}\tag{2.6.3}
$$

则使用Q-M法的化简步骤如下：

（1）将函数化为最小项之和形式，列出最小项编码表。

将式 $(2.6.3)$ 化为最小项之和形式后得到

---

## Chunk 73/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p00 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p02 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

$$
\begin{array}{r l} Y (A, B, C, D, E) & = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} D E ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} D E + A ^ {\prime} B C ^ {\prime} D ^ {\prime} E ^ {\prime} \\ & \quad + A ^ {\prime} B C ^ {\prime} D E ^ {\prime} + A ^ {\prime} B C D E ^ {\prime} + A ^ {\prime} B C D E + A B ^ {\prime} C D E ^ {\prime} + A B C ^ {\prime} D ^ {\prime} E ^ {\prime} + A B C ^ {\prime} D E + A B C D E \\ & = \sum m (0, 2, 3, 8, 1 0, 1 4, 1 5, 2 2, 2 4, 2 7, 3 1) \end{array} \tag {2.6}\tag{2.6.4}
$$

用 1 表示最小项中的原变量, 用 0 表示最小项中的反变量, 就得到了表 2.6.1 所示的最小项编码表。

表 2.6.1 式 (2.6.4) 最小项的编码表

<table><tr><td>最小项编号</td><td>0</td><td>2</td><td>3</td><td>8</td><td>10</td><td>14</td></tr><tr><td>代码</td><td>00000</td><td>00010</td><td>00011</td><td>01000</td><td>01010</td><td>01110</td></tr><tr><td>最小项编号</td><td>15</td><td>22</td><td>24</td><td>27</td><td>31</td><td></td></tr><tr><td>代码</td><td>01111</td><td>10110</td><td>11000</td><td>11011</td><td>11111</td><td></td></tr></table>

(2) 按包含 1 的个数将最小项分组, 如表 2.6.2 中最左边一列所示。

表 2.6.2 列表合并最小项

---

## Chunk 74/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p01 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p03 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

<table><tr><td colspan="7">合并前的最小项 $(\sum m_i)$ </td><td colspan="6">第一次合并结果(含n-1个变量的乘积项)</td><td colspan="6">第二次合并结果(含n-2个变量的乘积项)</td><td></td><td></td></tr><tr><td>编号</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td></td><td>编号</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>编号</td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td></td><td></td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>√</td><td>0,2</td><td>0</td><td>0</td><td>0</td><td>—</td><td>0</td><td>√</td><td rowspan="2">0,2 $\left. \begin{array}{c} 0 \\ 8,10 \end{array} \right\}$ </td><td rowspan="2">0</td><td rowspan="2">—</td><td rowspan="2">0</td><td rowspan="2">—</td><td rowspan="2">0</td><td> $P_8$ </td></tr><tr><td>2</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>√</td><td>0,8</td><td>0</td><td>—</td><td>0</td><td>0</td><td>0</td><td>√</td><td></td></tr><tr><td>8</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>√</td><td>2,3</td><td>0</td><td>0</td><td>0</td><td>1</td><td>—</td><td> $P_2$ </td><td rowspan="9">0,8 $\left. \begin{array}{c} 0 \\ 2,10 \end{array} \right\}$ </td><td rowspan="9">0</td><td rowspan="9">—</td><td rowspan="9">0</td><td

---

## Chunk 75/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p03 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p02 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p04 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

rowspan="9">—</td><td rowspan="9">0</td><td> $P_8$ </td></tr><tr><td>3</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>√</td><td>2,10</td><td>0</td><td>—</td><td>0</td><td>1</td><td>0</td><td>√</td><td></td></tr><tr><td>10</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>√</td><td>8,10</td><td>0</td><td>1</td><td>0</td><td>—</td><td>0</td><td>√</td><td></td></tr><tr><td>24</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>√</td><td>8,24</td><td>—</td><td>1</td><td>0</td><td>0</td><td>0</td><td> $P_3$ </td><td></td></tr><tr><td>14</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>√</td><td>10,14</td><td>0</td><td>1</td><td>—</td><td>1</td><td>0</td><td> $P_4$ </td><td></td></tr><tr><td>22</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td> $P_1$ </td><td>14,15</td><td>0</td><td>1</td><td>1</td><td>1</td><td>—</td><td> $P_5$ </td><td></td></tr><tr><td>15</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>√</td><td>15,31</td><td>—</td><td>1</td><td>1</td><td>1</td><td>1</td><td> $P_6$ </td><td></td></tr><tr><td>27</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>√</td><td>27,31</td><td>1</td><td>1</td><td>—</td><td>1</td><td>1<

---

## Chunk 76/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p04 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p03 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p05 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

/td><td> $P_7$ </td><td></td></tr><tr><td>31</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>√</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

---

## Chunk 77/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p05`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p05 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p04 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p06 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

(3) 合并相邻的最小项。

将表 2.6.2 中最左边一列里每一组的每一个最小项与相邻组里所有的最小项逐一比较，若仅有一个因子不同，则定可合并，并消去不同的因子。消去的因子用“—”号表示，将合并后的结果列于表 2.6.2 的第二列中。同时，在第一列中可以合并的最小项右边标以“√”号。

按照同样的方法再将第二列中的乘积项合并，合并后的结果写在第三列中。

如此进行下去，直到不能再合并为止。

(4) 选择最少的乘积项。

只要将表 2.6.2 中合并过程中没有用过的那些乘积项相加, 自然就包含了函数 Y 的全部最小项, 故得

$$
Y (A, B, C, D, E) = P _ {1} + P _ {2} + P _ {3} + P _ {4} + P _ {5} + P _ {6} + P _ {7} + P _ {8}\tag{2.6.5}
$$

然而，上式并不一定是最简的与或表达式。为了进一步将式(2.6.5)化简，将 $P_{1}\sim P_{8}$ 各包含的最小项列成表2.6.3。因为表中带圆圈的最小项仅包含在一个乘积项中，所以化简结果中一定包含它们所在的这些乘积项，即 $P_{1},P_{2},P_{3},P_{7}$ 和 $P_{8}$ 。而且，选取了这五项之和以后，已包含了除 $m_{14}$ 和 $m_{15}$ 以外所有Y的最小项。

表 2.6.3 用列表法选择最少的乘积项

---

## Chunk 78/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p06`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p06 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p05 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p07 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

<table><tr><td> $\begin{array}{c}m_{i}\\P_{j}\end{array}$ </td><td>0</td><td>2</td><td>3</td><td>8</td><td>10</td><td>14</td><td>15</td><td>22</td><td>24</td><td>27</td><td>31</td></tr><tr><td> $P_{1}$ </td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1</td><td></td><td></td><td></td></tr><tr><td> $P_{2}$ </td><td></td><td>1</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td> $P_{3}$ </td><td></td><td></td><td></td><td>1</td><td></td><td></td><td></td><td></td><td>1</td><td></td><td></td></tr><tr><td> $P_{4}$ </td><td></td><td></td><td></td><td></td><td>1</td><td>1</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td> $P_{5}$ </td><td></td><td></td><td></td><td></td><td></td><td>1</td><td>1</td><td></td><td></td><td></td><td></td></tr><tr><td> $P_{6}$ </td><td></td><td></td><td></td><td></td><td></td><td></td><td>1</td><td></td><td></td><td></td><td>1</td></tr><tr><td> $P_{7}$ </td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1</td><td>1</td></tr><tr><td> $P_{8}$ </td><td>1</td><td>1</td><td></td><td>1</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td>

</td></tr></table>

---

## Chunk 79/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p07`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p07 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p06 |
| next_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p08 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

剩下的问题就是要确定化简结果中是否应包含 $P_{4}, P_{5}$ 和 $P_{6}$ 了。为此，可将表2.6.3中有关 $P_{4}, P_{5}, P_{6}$ 的部分简化成表2.6.4的形式。

表 2.6.4 表 2.6.3 的 ${P}_{4}\text{、}{P}_{5}\text{、}{P}_{6}$ 部分

<table><tr><td> ${P}_{j}$  ${m}_{i}$ </td><td>14</td><td>15</td></tr><tr><td> ${P}_{4}$ </td><td>1</td><td></td></tr><tr><td> ${P}_{5}$ </td><td>1</td><td>1</td></tr><tr><td> ${P}_{6}$ </td><td></td><td>1</td></tr></table>

由表 2.6.4 中可以看到, $P_{4}$ 行所有的 1 和 $P_{6}$ 行所有的 1 皆与 $P_{5}$ 中的 1 重叠,亦即 $P_{5}$ 中的最小项包含了 $P_{4}$ 和 $P_{6}$ 的所有最小项，故可将 $P_{4}$ 和 $P_{6}$ 两行删掉。因此，可将式(2.6.5)中的 $P_{4}$ 和 $P_{6}$ 两项去掉，从而得到最后的化简结果

```txt
复习思考题R2.6.1 卡诺图化简法所依据的基本原理是什么？R2.6.2 卡诺图两侧变量取值的标注次序应遵守什么规则？R2.6.3 Q-M法所依据的基本原理是什么？R2.6.4 公式化简法、卡诺图化简法、Q-M化简法各有何优缺点？
```

$$
\begin{array}{r l} Y (A, B, C, D, E) & = P _ {1} + P _ {2} + P _ {3} + P _ {5} + P _ {7} + P _ {8} \\ & = A B ^ {\prime} C D E ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + B C ^ {\prime} D ^ {\prime} E ^ {\prime} \\ & \quad + A ^ {\prime} B C D + A B D E + A ^ {\prime} C ^ {\prime} E ^ {\prime} \end{array}\tag{2.6.6}
$$

---

## Chunk 80/161：`ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p08`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p08 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法) |
| section_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p07 |
| next_chunk_id | ch02_sec_2_7_1_theory_1033_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L951–1029 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > * 2.6.3 奎恩-麦克拉斯基化简法 (Q-M 法)

从上面的例子中可以看到,虽然 Q-M 法的化简过程看起来比较繁琐,但由于它有确定的流程,适用于任何复杂逻辑函数的化简,这就为编制计算机辅助化简程序提供了方便。因此,几乎很少有人用手工方法使用 Q-M 法去化简复杂的逻辑函数,而是使用基于 Q-M 法的基本原理去编制各种计算机软件,然后在计算机上完成逻辑函数的化简工作。

---

## Chunk 81/161：`ch02_sec_2_7_1_theory_1033_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_7_1_theory_1033_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项 |
| section_id | ch02_sec_2_7_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.7.1 |
| prev_chunk_id | ch02_sec_2_6_3_奎恩-麦克拉斯基化简法_Q-M_法_theory_951_p08 |
| next_chunk_id | ch02_sec_2_7_1_theory_1033_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1033–1094 |

### 配图

**图2.7.1** — 用于说明具有约束的逻辑函数的实例

![图2.7.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/dcc4c98d0af4563278a7620270501d5f8d9ee899ab30b95ff1d446fdf6c12d93.jpg)

*视觉描述：* 具有约束的逻辑函数实例：水箱侧壁安装水位传感器A、B、C检测液位，控制两侧进水泵MS与ML启停，用于约束条件下组合逻辑电路设计。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项

在处理具体的逻辑问题时,有时会遇到两种特殊情况。其中一种情况是输入变量的取值不是任意的。对输入变量取值的限制称为约束。我们把具有这种特点的逻辑函数称为具有约束的逻辑函数,同时把这一组输入变量称为具有约束的一组逻辑变量。

下面让我们来讨论一下图2.7.1给出的一个实例。图中的水箱由大、小两台水泵 $\mathrm{M_L}$ 和 $\mathrm{M_S}$ 供水。水箱中设置了3个水位检测元件 $A,B,C$ 。水位低于检测元件时，检测元件给出低电平；水位高于检测元件时，检测元件给出高电平。

图2.7.1 用于说明具有约束的逻辑函数的实例

现以 $Y_{\mathrm{L}}$ 和 $Y_{\mathrm{S}}$ 分别表示 $\mathbf{M}_{\mathrm{L}}$ 和 $\mathbf{M}_{\mathrm{S}}$ 的启动控制信号，取值为1时水泵启动，取值为0时水泵停止。根据要求，当水位超过 $C$ 点时（ABC的取值为111）水泵停止工作， $Y_{\mathrm{S}} = 0, Y_{\mathrm{L}} = 0$ ；水位低于 $C$ 点而高于 $B$ 点时（ABC的取值为110），小水泵 $\mathbf{M}_{\mathrm{S}}$ 单独工作， $Y_{\mathrm{S}} = 1$ ；水位低于 $B$ 点而高于 $A$ 点时（ABC的取值为100），大水泵 $\mathbf{M}_{\mathrm{L}}$ 单独工作， $Y_{\mathrm{L}} = 1$ ；水位低于 $A$ 点时（ABC的取值为000）， $\mathbf{M}_{\mathrm{S}}$ 和 $\mathbf{M}_{\mathrm{L}}$ 同时工作， $Y_{\mathrm{S}} = 1, Y_{\mathrm{L}} = 1$ 。因此， $\mathbf{M}_{\mathrm{S}}$ 和 $\mathbf{M}_{\mathrm{L}}$ 的启动控制信号 $Y_{\mathrm{S}}$ 和 $Y_{\mathrm{L}}$ 是 $A, B, C$ 这三个逻辑变量的逻辑函数，并可写成

$$
Y _ {\mathrm{L}} = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A B ^ {\prime} C ^ {\prime} = B ^ {\prime} C ^ {\prime}\tag{2.7.1}
$$

$$
Y _ {\mathrm{s}} = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A B C ^ {\prime}\tag{2.7.2}
$$

[图2.7.1] 用于说明具有约束的逻辑函数的实例
[图2.7.1描述] 具有约束的逻辑函数实例：水箱侧壁安装水位传感器A、B、C检测液位，控制两侧进水泵MS与ML启停，用于约束条件下组合逻辑电路设计。

---

## Chunk 82/161：`ch02_sec_2_7_1_theory_1033_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_7_1_theory_1033_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项 |
| section_id | ch02_sec_2_7_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_7_1_theory_1033_p00 |
| next_chunk_id | ch02_sec_2_7_1_theory_1033_p02 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1033–1094 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项

由于不可能出现水位高于 C 点而低于 B 点和 A 点的情况，也不可能出现水位高于 B 点而低于 A 点的情况，所以 ABC 的取值不可能出现 001、010、011、101 这四种情况。由此可见，A、B、C 是一组具有约束的逻辑变量， $Y_{s}$ 和 $Y_{L}$ 是两个具有约束的逻辑函数。

通常用约束条件来描述约束的具体内容。显然，用上面的这样一段文字叙述约束条件是很不方便的，最好能用简单、明了的逻辑语言表述约束条件。

由于每一组输入变量的取值都使一个、而且仅有一个最小项的值为 1，所以当限制某些输入变量的取值不能出现时，可以用它们对应的最小项恒等于 0 来表示。这样，上面例子中的约束条件可以表示为

$$
\left\{ \begin{array}{l} A ^ {\prime} B ^ {\prime} C = 0 \\ A ^ {\prime} B C ^ {\prime} = 0 \\ A ^ {\prime} B C = 0 \\ A B ^ {\prime} C = 0 \end{array} \right.
$$

或写成

$$
A ^ {\prime} B ^ {\prime} C + A _ {2} ^ {\prime} B C ^ {\prime} + A ^ {\prime} B C + A B ^ {\prime} C = 0
$$

同时，将这些恒等于0的最小项称为函数 $Y_{s}$ 和 $Y_{L}$ 的约束项。

在存在约束项的情况下,由于约束项的值始终等于0,所以既可以将约束项写进逻辑函数式中,也可以将约束项从函数式中删掉,而不影响函数值。

有时还会遇到另外一种情况,就是在输入变量的某些取值下函数值是1还是0皆可,并不影响电路的功能。在这些变量取值下,其值等于1的那些最小项称为任意项。

为了进一步说明任意项的物理概念,让我们来看一个电动机控制的例子。现以三个逻辑变量 A、B、C 分别表示一台电动机的正转、反转和停止的命令,A=1 表示正转,B=1 表示反转,C=1 表示停止。表示正转、反转和停止工作状态的逻辑函数可写成

$$
Y _ {1} = A B ^ {\prime} C ^ {\prime} \quad (\text {正转})\tag{2.7.3}
$$

$$
Y _ {2} = A ^ {\prime} B C ^ {\prime} \quad (\text { 反   转 })\tag{2.7.4}
$$

$$
Y _ {3} = A ^ {\prime} B ^ {\prime} C \qquad (\text { 停   止 })\tag{2.7.5}
$$

---

## Chunk 83/161：`ch02_sec_2_7_1_theory_1033_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_7_1_theory_1033_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项 |
| section_id | ch02_sec_2_7_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_7_1_theory_1033_p01 |
| next_chunk_id | ch02_sec_2_7_2_theory_1096 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1033–1094 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.7.1 约束项、任意项和逻辑函数式中的无关项

因为任何时候电动机只能执行其中的一种命令，所以 A、B、C 当中出现两个以上为 1 时，电动机将无法工作。为此，将实际的电路设计成当 A、B、C 三个控制变量出现两个以上同时为 1 或者全部为 0 时电路能自动切断供电电源，那么这时 $Y_{1}$ 、 $Y_{2}$ 和 $Y_{3}$ 等于 1 还是等于 0 已无关紧要，电动机肯定会受到保护而停止运行。例如，当出现 A = B = C = 1 时，对应的最小项 $ABC(m_{7}) = 1$ 。如果把最小项 ABC 写入 $Y_{1}$ 式中，则当 A = B = C = 1 时 $Y_{1} = 1$ ；如果没有把 ABC 这一项写入 $Y_{1}$ 式中，则当 A=B=C=1 时 $Y_{1}=0$ 。因为这时 $Y_{1}=1$ 还是 $Y_{1}=0$ 都是允许的，所以既可以把 ABC 这个最小项写入 $Y_{1}$ 式中，也可以不写入。因此，我们把 ABC 称为逻辑函数 $Y_{1}$ 的任意项。同理，在这个例子中 $A'B'C'$ 、 $A'BC$ 、 $AB'C$ 、 $ABC'$ 也是 $Y_{1}$ 、 $Y_{2}$ 和 $Y_{3}$ 的任意项。这种存在任意项的逻辑函数也叫做不完全定义的逻辑函数。

因为使约束项的取值等于1的输入变量取值是不允许出现的，所以约束项的值始终为0。而任意项则不同，在函数的运行过程中，有可能出现使任意项取值为1的输入变量取值。

我们将约束项和任意项统称为逻辑函数式中的无关项。这里所说的“无关”是指是否把这些最小项写入逻辑函数式无关紧要，可以写入也可以删除。

上一节中曾经讲到，在用卡诺图表示逻辑函数时，首先将函数化为最小项之和的形式，然后在卡诺图中这些最小项对应的位置上填入1，其他位置上填入0。既然可以认为无关项包含于函数式中，也可以认为不包含在函数式中，那么在卡诺图中对应的位置上就可以填入1，也可以填入0。为此，在卡诺图中用×(或∅)表示无关项。在化简逻辑函数时既可以认为它是1，也可以认为它是0。

---

## Chunk 84/161：`ch02_sec_2_7_2_theory_1096`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_7_2_theory_1096 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.7.2 无关项在化简逻辑函数中的应用 |
| section_id | ch02_sec_2_7_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_7_1_theory_1033_p02 |
| next_chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1096–1102 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.7.2 无关项在化简逻辑函数中的应用

化简具有无关项的逻辑函数时,如果能合理利用这些无关项,一般都可得到更加简单的化简结果。

为达到此目的,加入的无关项应与函数式中尽可能多的最小项(包括原有的最小项和已写入的无关项)具有逻辑相邻性。

合并最小项时,究竟把卡诺图中的×作为1(即认为函数式中包含了这个最小项)还是作为0(即认为函数式中不包含这个最小项)对待,应以得到的相邻最小项矩形组合最大、而且矩形组合数目最少为原则。

---

## Chunk 85/161：`ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数 |
| section_id | ch02_sec_例2_7_1_化简具有约束的逻辑函数 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_7_2_theory_1096 |
| next_chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1104–1134 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数

$$
Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C D + A B ^ {\prime} C ^ {\prime} D ^ {\prime}
$$

给定约束条件为

$$
A ^ {\prime} B ^ {\prime} C D + A ^ {\prime} B C ^ {\prime} D + A B C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D + A B C D + A B C D ^ {\prime} + A B ^ {\prime} C D ^ {\prime} = 0
$$

在用最小项之和形式表示上述具有约束的逻辑函数时,也可写成如下形式

$$
Y (A, B, C, D) = \sum m (1, 7, 8) + d (3, 5, 9, 1 0, 1 2, 1 4, 1 5)
$$

式中以 d 表示无关项，d 后面括号内的数字是无关项的最小项编号。

解：如果不利用约束项，则 Y 已无可化简。但适当地加进一些约束项以后，可以得到

$$
\begin{array}{r l} Y & = (A ^ {\prime} B ^ {\prime} C ^ {\prime} D + \underbrace {A ^ {\prime} B ^ {\prime} C D} _ {\text {约束项}}) + (A ^ {\prime} B C D + \underbrace {A ^ {\prime} B C ^ {\prime} D} _ {\text {约束项}}) \\ & \quad + (A B ^ {\prime} C ^ {\prime} D ^ {\prime} + \underbrace {A B C ^ {\prime} D ^ {\prime}} _ {\text {约束项}}) + (\underbrace {A B C D ^ {\prime}} _ {\text {约束项}} + \underbrace {A B ^ {\prime} C D ^ {\prime}} _ {\text {约束项}}) \\ & = (A ^ {\prime} B ^ {\prime} D + A ^ {\prime} B D) + (A C ^ {\prime} D ^ {\prime} + A C D ^ {\prime}) \\ & = A ^ {\prime} D + A D ^ {\prime} \end{array}
$$

可见,利用了约束项以后,使逻辑函数得以进一步化简。但是,在确定该写入哪些约束项时尚不够直观。

---

## Chunk 86/161：`ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数 |
| section_id | ch02_sec_例2_7_1_化简具有约束的逻辑函数 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.7.2 |
| prev_chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p00 |
| next_chunk_id | ch02_eg2_7_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1104–1134 |

### 配图

**图2.7.2** — 例2.7.1的卡诺图

![图2.7.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c6cc6f3d8044ea0967a3a321a6db15f81d019133ecbaff1026f7e5eab8aa2387.jpg)

*视觉描述：* 例2.7.1带无关项卡诺图：四变量AB-CD格内填0、1及X，中间2×2圈(A'D)与左右绕回2×2圈(AD')，演示利用X扩大圈组化简。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数

如果改用卡诺图化简法,则只要将表示 Y 的卡诺图画出,就能从图上直观地判断对这些约束项应如何取舍。

图 2.7.2 是例 2.7.1 的逻辑函数的卡诺图。从图中不难看出，为了得到最大的相邻最小项的矩形组合，应取约束项 $m_{3}$ 、 $m_{5}$ 为 1，与 $m_{1}$ 、 $m_{7}$ 组成一个矩形组。同时取约束项 $m_{10}$ 、 $m_{12}$ 、 $m_{14}$ 为 1，与 $m_{8}$ 组成一个矩形组。将两组相邻的最小项合并后得到的化简结果与上面推演的结果相同。卡诺图中没有被圈进去的约束项 ( $m_{9}$ 和 $m_{15}$ ) 是当作 0 对待的。

[图2.7.2] 例2.7.1的卡诺图
[图2.7.2描述] 例2.7.1带无关项卡诺图：四变量AB-CD格内填0、1及X，中间2×2圈(A'D)与左右绕回2×2圈(AD')，演示利用X扩大圈组化简。

---

## Chunk 87/161：`ch02_eg2_7_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_7_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数 |
| section_id | ch02_sec_例2_7_1_化简具有约束的逻辑函数 |
| exercise_id | — |
| example_id | 例2.7.2 |
| figure_ids | 图2.7.3 |
| prev_chunk_id | ch02_sec_eg2_7_1_化简具有约束的逻辑函数_theory_1104_p01 |
| next_chunk_id | ch02_sec_review_review_1157 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1135–1154 |

### 配图

**图2.7.3** — 例2.7.2的卡诺图

![图2.7.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/dae496fc62e48f30638c208330efaa4c753d79d231ac697c66804d5a041f4f0d.jpg)

*视觉描述：* 例2.7.2带无关项卡诺图：CD=10整列四格(含X)圈为C D'，CD=00列AB=01/11/10三格圈，展示约束项参与合并的最简化简方法。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 【例2.7.1】化简具有约束的逻辑函数

【例2.7.2】试化简具有无关项的逻辑函数

$$
Y (A, B, C, D) = \sum m (2, 4, 6, 8) + d (1 0, 1 1, 1 2, 1 3, 1 4, 1 5)
$$

解：画出函数 Y 的卡诺图，如图 2.7.3 所示。

由图可见，若认为其中的无关项 $m_{10}, m_{12}, m_{14}$ 为1，而无关项 $m_{11}, m_{13}, m_{15}$ 为0，则可将 $m_4, m_6, m_{12}$ 和 $m_{14}$ 合并为 $BD'$ ，将 $m_8, m_{10}, m_{12}$ 和 $m_{14}$ 合并为 $AD'$ ，将 $m_2, m_6, m_{10}$ 和 $m_{14}$ 合并为 $CD'$ ，于是得到

$$
Y = B D ^ {\prime} + A D ^ {\prime} + C D ^ {\prime}
$$

图2.7.2 例2.7.1的卡诺图

图2.7.3 例2.7.2的卡诺图

[图2.7.3] 例2.7.2的卡诺图
[图2.7.3描述] 例2.7.2带无关项卡诺图：CD=10整列四格(含X)圈为C D'，CD=00列AB=01/11/10三格圈，展示约束项参与合并的最简化简方法。

---

## Chunk 88/161：`ch02_sec_review_review_1157`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1157 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_7_2 |
| next_chunk_id | ch02_sec_review_review_1159 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1157–1158 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.7.1 什么是逻辑函数的约束项、任意项和逻辑函数式的无关项？

---

## Chunk 89/161：`ch02_sec_review_review_1159`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1159 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_1157 |
| next_chunk_id | ch02_sec_review_review_1161 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1159–1160 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.7.2 将一个约束项写入逻辑函数式或不写入逻辑函数式,对函数的输出是否有影响?将一个任意项写入逻辑函数式或不写入逻辑函数式,对函数的输出有无影响?

---

## Chunk 90/161：`ch02_sec_review_review_1161`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1161 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_1159 |
| next_chunk_id | ch02_sec_2_8_theory_1164_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1161–1162 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.7.3 怎样利用无关项才能得到更简单的逻辑函数化简结果?

---

## Chunk 91/161：`ch02_sec_2_8_theory_1164_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_8_theory_1164_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.8 多输出逻辑函数的化简 |
| section_id | ch02_sec_2_8 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.8.1(a), 图2.8.1(b), 图2.8.1(c), 图2.8.2, 图2.8.3 |
| prev_chunk_id | ch02_sec_review_review_1161 |
| next_chunk_id | ch02_sec_2_8_theory_1164_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1164–1204 |

### 配图

**图2.8.1(a)** — 用于化简式(2.8.1)逻辑函数的卡诺图 子图(a)

![图2.8.1(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/7e852eafc891342d001485d3a46aee44e4581459d22b5ccca326cfa7ef6a976b.jpg)

*视觉描述：* 四变量AB-CD卡诺图化简Y1函数：中间两行八格1合并为B项，右下四角1合并为AC项，左上CD=01两格1合并为A'C'D项，得Y1=B+AC+A'C'D。

**图2.8.1(b)** — 用于化简式(2.8.1)逻辑函数的卡诺图 子图(b)

![图2.8.1(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/29b1c6218663df389c9c7ad2234b701e0913b32f120d946b6c392c67ae6777be.jpg)

*视觉描述：* 四变量卡诺图化简Y2：左上2×2圈合并得A'D项，中间行左右边界2×2圈跨越合并得BD'项，化简结果为Y2=A'D+BD'。

**图2.8.1(c)** — 用于化简式(2.8.1)逻辑函数的卡诺图 子图(c)

![图2.8.1(c)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/d1486bf0122c53aa4c1bf6d2969d54b4c95f62f12c43a45110f3cac8d36ee899.jpg)

*视觉描述：* 四变量卡诺图化简Y3：竖向圈合并AB=00、01且CD=11的两格1得A'CD项，横向圈合并AB=10且CD=11、10的两格1得AB'C项。

**图2.8.2** — 根据式(2.8.2)得到的逻辑电路图

![图2.8.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/e54e2cf054e3623fd8ff8b78d002ba7fa35860d68b9c2c792781939bbb2b004e.jpg)

*视觉描述：* 与-或结构组合逻辑电路：六与门、三或门实现Y1=B+AC+A'C'D、Y2=A'D+BD'、Y3=A'CD+AB'C三输出，对应式(2.8.2)。

**图2.8.3** — 利用公共项化简式(2.8.1)逻辑函数的卡诺图

![图2.8.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/f5dd1dc9c1a4b43a6d7478216c8f6b683b27a6f40a354144407c9560e0bd7067.jpg)

*视觉描述：* Y1、Y2、Y3三张四变量卡诺图并列，利用公共乘积项A'C'D、BD'、AB'C合并化简，体现多输出函数共享项的化简方法。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.8 多输出逻辑函数的化简

在化简多输出逻辑函数的过程中,我们发现,如果不是孤立地分别对每一个输出函数进行化简,而是从整体上综合考虑进行化简,有时会获得更加简单的化简结果,使得所用门电路的数目和所有门电路总的输入端数目均为最少。例如有下面的一组多输出逻辑函数需要化简

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = \sum (1, 4, 5, 6, 7, 1 0, 1 1, 1 2, 1 3, 1 4, 1 5) \\ Y _ {2} (A, B, C, D) = \sum (1, 3, 4, 5, 6, 7, 1 2, 1 4,) \\ Y _ {3} (A, B, C, D) = \sum (3, 7, 1 0, 1 1,) \end{array}\tag{2.8.1}
$$

如果用卡诺图分别化简每一个函数，并按图2.8.1所示合并最小项，就可得到如下的化简结果

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = B + A C + A ^ {\prime} C ^ {\prime} D \\ Y _ {2} (A, B, C, D) = A ^ {\prime} D + B D ^ {\prime} \\ Y _ {3} (A, B, C, D) = A ^ {\prime} C D + A B ^ {\prime} C \end{array}\tag{2.8.2}
$$

根据式 $(2.8.2)$ 画出的逻辑图如图2.8.2所示。

图 2.8.1 用于化简式(2.8.1)逻辑函数的卡诺图  
图 2.8.2 根据式(2.8.2)得到的逻辑电路图

如果我们改用图2.8.3所示的方式合并最小项，即找出 $Y_{1}, Y_{2}, Y_{3}$ 之间存在的共用项并加以利用，就可以得到如式(2.8.3)所示的另一种化简结果，即

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = B + A B ^ {\prime} C + A ^ {\prime} C ^ {\prime} D \\ Y _ {2} (A, B, C, D) = \underbrace {A ^ {\prime} C ^ {\prime} D + A ^ {\prime} C D + B D ^ {\prime}} \\ Y _ {3} (A, B, C, D) = \underbrace {A ^ {\prime} C D + A B ^ {\prime} C} \end{array}\tag{2.8.3}
$$

图 2.8.3 利用公共项化简式(2.8.1)逻辑函数的卡诺图

[图2.8.1(a)] 用于化简式(2.8.1)逻辑函数的卡诺图 子图(a)
[图2.8.1(a)描述] 四变量AB-CD卡诺图化简Y1函数：中间两行八格1合并为B项，右下四角1合并为AC项，左上CD=01两格1合并为A'C'D项，得Y1=B+AC+A'C'D。
[图2.8.1(b)] 用于化简式(2.8.1)逻辑函数的卡诺图 子图(b)
[图2.8.1(b)描述] 四变量卡诺图化简Y2：左上2×2圈合并得A'D项，中间行左右边界2×2圈跨越合并得BD'项，化简结果为Y2=A'D+BD'。
[图2.8.1(c)] 用于化简式(2.8.1)逻辑函数的卡诺图 子图(c)
[图2.8.1(c)描述] 四变量卡诺图化简Y3：竖向圈合并AB=00、01且CD=11的两格1得A'CD项，横向圈合并AB=10且CD=11、10的两格1得AB'C项。
[图2.8.2] 根据式(2.8.2)得到的逻辑电路图
[图2.8.2描述] 与-或结构组合逻辑电路：六与门、三或门实现Y1=B+AC+A'C'D、Y2=A'D+BD'、Y3=A'CD+AB'C三输出，对应式(2.8.2)。
[图2.8.3] 利用公共项化简式(2.8.1)逻辑函数的卡诺图
[图2.8.3描述] Y1、Y2、Y3三张四变量卡诺图并列，利用公共乘积项A'C'D、BD'、AB'C合并化简，体现多输出函数共享项的化简方法。

---

## Chunk 92/161：`ch02_sec_2_8_theory_1164_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_8_theory_1164_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.8 多输出逻辑函数的化简 |
| section_id | ch02_sec_2_8 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.8.2, 图2.8.4 |
| prev_chunk_id | ch02_sec_2_8_theory_1164_p00 |
| next_chunk_id | ch02_sec_2_9_theory_1206_p00 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1164–1204 |

### 配图

**图2.8.2** — 根据式(2.8.2)得到的逻辑电路图

![图2.8.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/e54e2cf054e3623fd8ff8b78d002ba7fa35860d68b9c2c792781939bbb2b004e.jpg)

*视觉描述：* 与-或结构组合逻辑电路：六与门、三或门实现Y1=B+AC+A'C'D、Y2=A'D+BD'、Y3=A'CD+AB'C三输出，对应式(2.8.2)。

**图2.8.4** — 根据式(2.8.3)得到的逻辑电路图

![图2.8.4](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/d596482eec7fa2076f8496d14682916f8c4735ce7a38f0dd6c3b577eebb1fbdf.jpg)

*视觉描述：* 与-或两级PLA结构电路：四与门产生A'C'D、BD'、AB'C、A'CD乘积项，三或门输出Y1=B+A'C'D+BD'、Y2=A'C'D+BD'+AB'C、Y3=AB'C+A'CD。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.8 多输出逻辑函数的化简

由于 $Y_{1}$ 和 $Y_{3}$ 中都含有 $AB^{\prime}C$ 这一项，所以我们将 $AB^{\prime}C$ 称作 $Y_{1}$ 和 $Y_{3}$ 共有的共用项。同理， $A^{\prime}C^{\prime}D$ 是 $Y_{1}$ 和 $Y_{2}$ 共有的共用项， $A^{\prime}CD$ 是 $Y_{2}$ 和 $Y_{3}$ 共有的公共项。虽然现在 $Y_{1}, Y_{2}, Y_{3}$ 每个函数本身不是最简与或形式了，但是在用逻辑图实现式(2.8.3)的多输出逻辑函数时，由于每个共用项可以同时供两个输出函数使用，从而减少了所需门电路的数目，于是就得到了图2.8.4中的电路。和图2.8.2的电路相比，图2.8.4电路不仅少用了2个门，而且电路中总的连线数目也减少了。

图 2.8.4 根据式(2.8.3)得到的逻辑电路图

以上的例子说明,在化简多输出逻辑函数时,通过寻找并合理地利用共用项,有时可以得到更简单的化简结果。然而在实际应用中我们发现,并不是任何情况下,利用共用项都能够得到更简单的化简结果。对于两级与或形式的多输出逻辑函数,可以利用Q-M化简法进行化简,找出可以利用的共用项,并利用这些共用项得到更简单的化简结果。 $^{①}$

[图2.8.2] 根据式(2.8.2)得到的逻辑电路图
[图2.8.2描述] 与-或结构组合逻辑电路：六与门、三或门实现Y1=B+AC+A'C'D、Y2=A'D+BD'、Y3=A'CD+AB'C三输出，对应式(2.8.2)。
[图2.8.4] 根据式(2.8.3)得到的逻辑电路图
[图2.8.4描述] 与-或两级PLA结构电路：四与门产生A'C'D、BD'、AB'C、A'CD乘积项，三或门输出Y1=B+A'C'D+BD'、Y2=A'C'D+BD'+AB'C、Y3=AB'C+A'CD。

---

## Chunk 93/161：`ch02_sec_2_9_theory_1206_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_9_theory_1206_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换 |
| section_id | ch02_sec_2_9 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.9.1 |
| prev_chunk_id | ch02_sec_2_8_theory_1164_p01 |
| next_chunk_id | ch02_sec_2_9_theory_1206_p01 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1206–1245 |

### 配图

**图2.9.1** — 按照式(2.9.1)

![图2.9.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/86ec6a754e726277fdf7d9abca7541063579cbedf999f7a647fb1d44efd5d3e1.jpg)

*视觉描述：* 两三输入与门共接C'后送或门：上路与A、B'相与得AB'C'，下路与A'、B相与得A'BC'，输出Y=AB'C'+A'BC'，对应式(2.9.1)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换

在前面所讲的逻辑函数化简方法中,都是以最简与或式作为化简目标的。然而在用电路实现这些逻辑函数时,这种最简与或式有时并不是理想的形式。这是因为在电路实现的过程中,往往可供选择的电子器件种类有限,所以必须把逻辑函数的形式变换为与所用器件相适应的形式。

在使用标准化的数字集成电路组成所需要的逻辑电路时，不仅受到所提供的门电路类型的限制，而且由于很难找到具有4个以上输入端的与门和或门，因而当与或逻辑函数式的输入变量数和乘积项数很大时，就无法用一个两级的与或电路实现这个逻辑函数。在PLD当中，虽然某些PAL型PLD可以满足生成多输入变量、多乘积项的与或逻辑函数的需要，但是在用来实现输入变量数和乘积项数较少的与或逻辑函数时，器件内部的资源将得不到充分利用。因此，在FPGA型PLD的结构中，所提供的门电路都是输入端不多、逻辑功能种类有限的几种。可见，在使用PLD实现逻辑函数的过程中，同样会遇到逻辑函数形式变换的问题。所幸这种变换工作现在已经完全可以由PLD的编程软件来完成了。

例如我们需要用门电路实现式 $(2.9.1)$ 的逻辑函数。

$$
Y = A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C ^ {\prime}\tag{2.9.1}
$$

如果有 3 输入端的与门和 2 输入端的或门可以选用，则可以很方便地与上式对应地接成图 2.9.1 的两级与或逻辑电路。

但如果限定只能使用2输入端的与非门，这时就需要将式(2.9.1)变换为全部由两变量与非运算组成的形式。为此，可利用摩根定理将式(2.9.1)进行两次求反运算，变换成与非-与非形式，得到

图 2.9.1 按照式(2.9.1)
接成的逻辑电路

$$
\begin{array}{r l} Y & = A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C ^ {\prime} \\ & = ((A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & = ((A B ^ {\prime} C ^ {\prime}) ^ {\prime} (A ^ {\prime} B C ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & = (((A B ^ {\prime}) ^ {\prime}) ^ {\prime} C ^ {\prime}) ^ {\prime} (((A ^ {\prime} B) ^ {\prime}) ^ {\prime} C ^ {\prime}) ^ {\prime}) ^ {\prime} \end{array}\tag{2.9.2}
$$

[图2.9.1] 按照式(2.9.1)
[图2.9.1描述] 两三输入与门共接C'后送或门：上路与A、B'相与得AB'C'，下路与A'、B相与得A'BC'，输出Y=AB'C'+A'BC'，对应式(2.9.1)。

---

## Chunk 94/161：`ch02_sec_2_9_theory_1206_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_9_theory_1206_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换 |
| section_id | ch02_sec_2_9 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2.9.2, 图2.9.3 |
| prev_chunk_id | ch02_sec_2_9_theory_1206_p00 |
| next_chunk_id | ch02_eg2_9_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1206–1245 |

### 配图

**图2.9.2** — 按照式(2.9.2)接成的逻辑电路

![图2.9.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/98ac086640bc097e188197bf19bec290a3109d7d0924c1766b85a5348a377966.jpg)

*视觉描述：* 七与非门实现组合逻辑：G3、G4并接作非门，经多级与非运算得Y=(AB'+A'B)C'，即用与非门实现A、B异或后再与C'相与的运算。

**图2.9.3** — 按照式(2.9.3)接成的逻辑电路

![图2.9.3](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/1779bafb463c7a45bcda00ab89411f6b22468d4deaa058005214ac0f33601173.jpg)

*视觉描述：* 异或门与与门级联：输入A、B经异或门后与C'相与，输出Y=(A⊕B)C'，展示用基本逻辑门组合实现特定布尔函数的典型接法。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换

按照上式就得到了全部由2输入端与非门组成的逻辑电路，如图2.9.2所示。其中 $G_{3}$ 和 $G_{4}$ 两个与非门被接成了反相器使用。

如果有异或门和与门可以使用,则应当将式(2.9.1)变换成下面的形式

$$
\begin{array}{r l} Y & = A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C ^ {\prime} \\ & = (A B ^ {\prime} + A ^ {\prime} B) C ^ {\prime} \\ & = (A \oplus B) C ^ {\prime} \end{array}\tag{2.9.3}
$$

根据上式就得到了图 2.9.3 的逻辑电路。

图 2.9.2 按照式(2.9.2)接成的逻辑电路

图 2.9.3 按照式(2.9.3)接成的逻辑电路

[图2.9.2] 按照式(2.9.2)接成的逻辑电路
[图2.9.2描述] 七与非门实现组合逻辑：G3、G4并接作非门，经多级与非运算得Y=(AB'+A'B)C'，即用与非门实现A、B异或后再与C'相与的运算。
[图2.9.3] 按照式(2.9.3)接成的逻辑电路
[图2.9.3描述] 异或门与与门级联：输入A、B经异或门后与C'相与，输出Y=(A⊕B)C'，展示用基本逻辑门组合实现特定布尔函数的典型接法。

---

## Chunk 95/161：`ch02_eg2_9_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_9_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换 |
| section_id | ch02_sec_2_9 |
| exercise_id | — |
| example_id | 例2.9.1 |
| figure_ids | 图2.9.4 |
| prev_chunk_id | ch02_sec_2_9_theory_1206_p01 |
| next_chunk_id | ch02_eg2_9_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1246–1262 |

### 配图

**图2.9.4** — 按照式(2.9.5)接成的逻辑电路

![图2.9.4](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/e2a59c6d0b8c98e1518180d79b87d4ef83ce1275f28b579d13291039918b6dff.jpg)

*视觉描述：* 三与非门实现与-或逻辑：左上与门输入A、C，左下与门输入B、C'，末级与非得Y=AC+BC'，为与非门实现或-与变换的示例。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换

【例 2.9.1】试用 2 输入端与非门产生如下的逻辑函数

$$
Y = A C + B C ^ {\prime}\tag{2.9.4}
$$

解：为了全部用2输入端与非门实现这个电路，就必须将式(2.9.4)变换成全部由两变量与非运算组成的形式。为此，利用摩根定理将式(2.9.4)变换为

$$
\begin{array}{r l} Y & = A C + B C ^ {\prime} \\ & = \left(\left(A C + B C ^ {\prime}\right) ^ {\prime}\right) ^ {\prime} \\ & = \left(\left(A C\right) ^ {\prime} \left(B C ^ {\prime}\right) ^ {\prime}\right) ^ {\prime} \end{array}\tag{2.9.5}
$$

根据上式就得到了图 2.9.4 的电路。

图 2.9.4 按照式(2.9.5)接成的逻辑电路

[图2.9.4] 按照式(2.9.5)接成的逻辑电路
[图2.9.4描述] 三与非门实现与-或逻辑：左上与门输入A、C，左下与门输入B、C'，末级与非得Y=AC+BC'，为与非门实现或-与变换的示例。

---

## Chunk 96/161：`ch02_eg2_9_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_eg2_9_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换 |
| section_id | ch02_sec_2_9 |
| exercise_id | — |
| example_id | 例2.9.2 |
| figure_ids | 图2.9.5 |
| prev_chunk_id | ch02_eg2_9_1 |
| next_chunk_id | ch02_sec_review_review_1278 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1263–1275 |

### 配图

**图2.9.5** — 按照式(2.9.6)接成的逻辑电路

![图2.9.5](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/6d1accf15e3cd4b9d968e850354164e37c199c7759532a9d10f29dd46c693c94.jpg)

*视觉描述：* 三或非门两级结构：左上或非输入B、C得(B+C)'，左下或非输入A、C'得(A+C')'，末级或非输出Y=(A+C')(B+C)。 | 按式(2.9.6)用或非门实现的组合逻辑电路，结构与图2.9.5(a)互补，展示同一布尔函数采用不同通用逻辑门进行级联实现的方法。

**图2.9.5** — 按照式(2.9.6)接成的逻辑电路

![图2.9.5](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/91e89cbdfa903587bd5630dbe35c7d26af6902c839852a1548cc20afe6506c54.jpg)

*视觉描述：* 三或非门两级结构：左上或非输入B、C得(B+C)'，左下或非输入A、C'得(A+C')'，末级或非输出Y=(A+C')(B+C)。 | 按式(2.9.6)用或非门实现的组合逻辑电路，结构与图2.9.5(a)互补，展示同一布尔函数采用不同通用逻辑门进行级联实现的方法。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 2.9 逻辑函数形式的变换

【例 2.9.2】试用 2 输入端或非门产生式(2.9.4)给出的逻辑函数。

解：为了全部用2输入端或非门实现这个电路，则需要将式(2.9.4)变换成全部由两变量或非运算组成的形式。为此，用摩根定理将式(2.9.4)变换为

$$
\begin{array}{r l} Y & = A C + B C ^ {\prime} \\ & = ((A C) ^ {\prime} (B C ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & = ((A ^ {\prime} + C ^ {\prime}) (B ^ {\prime} + C)) ^ {\prime} \\ & = (B ^ {\prime} C ^ {\prime} + A ^ {\prime} C) ^ {\prime} \\ & = ((B + C) ^ {\prime} + (A + C ^ {\prime}) ^ {\prime}) ^ {\prime} \end{array}\tag{2.9.6}
$$

按照式 $(2.9.6)$ 接成的逻辑电路如图2.9.5所示。

图 2.9.5 按照式(2.9.6)接成的逻辑电路

[图2.9.5] 按照式(2.9.6)接成的逻辑电路
[图2.9.5描述] 三或非门两级结构：左上或非输入B、C得(B+C)'，左下或非输入A、C'得(A+C')'，末级或非输出Y=(A+C')(B+C)。 | 按式(2.9.6)用或非门实现的组合逻辑电路，结构与图2.9.5(a)互补，展示同一布尔函数采用不同通用逻辑门进行级联实现的方法。

---

## Chunk 97/161：`ch02_sec_review_review_1278`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1278 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_eg2_9_2 |
| next_chunk_id | ch02_sec_review_review_1280 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1278–1279 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.9.1 用什么方法可以把逻辑函数的与或形式变换为与非-与非形式？

---

## Chunk 98/161：`ch02_sec_review_review_1280`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1280 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_1278 |
| next_chunk_id | ch02_sec_review_review_1282 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1280–1281 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.9.2 用什么方法可以把逻辑函数的与或形式变换为与或非形式？

---

## Chunk 99/161：`ch02_sec_review_review_1282`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_review_review_1282 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > review 复习思考题 |
| section_id | ch02_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_1280 |
| next_chunk_id | ch02_sec_summary_end_theory_1287 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1282–1285 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > review 复习思考题

R2.9.3 用什么方法可以把逻辑函数的与或形式变换为或非-或非形式？

---

## Chunk 100/161：`ch02_sec_summary_end_theory_1287`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_summary_end_theory_1287 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > summary_end 本章小结 |
| section_id | ch02_sec_summary_end |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_review_review_1282 |
| next_chunk_id | ch02_ex2_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1287–1307 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > summary_end 本章小结

这一章所讲的内容主要是逻辑代数的公式和定理、逻辑函数的描述方法、逻辑函数的化简和

变换这三部分。

为了进行逻辑运算,必须熟练掌握表2.3.1中的基本公式。至于表2.3.3中的常用公式,完全可以由基本公式导出。尽管如此,掌握尽可能多的常用公式仍然是十分有益的,因为直接引用这些公式可以大大提高运算效率。

在逻辑函数的描述方法中,共介绍了五种描述方法,即真值表、逻辑函数式、逻辑图、波形图和卡诺图。这几种方法之间可以任意地互相转换。根据具体的使用情况,可以选择最适当的一种方法描述所研究的逻辑函数。

在逻辑函数化简方法当中,一共介绍了三种方法——公式化简法、卡诺图化简法和 Q-M 法。公式化简法的优点是它的使用不受任何条件的限制。但由于这种方法没有固定的步骤可循,所以在化简复杂的逻辑函数时,不仅需要熟练地运用各种公式和定理,而且需要有一定的运算技巧和经验。

卡诺图化简法是一种通过合并最小项进行化简的方法。它的优点是简单、直观，而且有一定的化简步骤可循。初学者容易掌握这种方法，而且化简过程中也易于避免出差错。然而在逻辑变量超过5个以上时，将失去简单、直观的优点，因而也就没有多大的实用价值了。

Q-M 法的基本原理仍然是通过合并最小项的方法来化简逻辑函数。但由于 Q-M 法有一定的化简步骤，所以适合于机器运算。这种方法已经被用于编制分析和设计数字电路的计算机程序。

在具体设计数字电路的过程中,通常可供使用的器件类型是有限的,这就需要利用逻辑函数的公式和定理,将函数式化成与所用器件逻辑类型相适应的形式,而不一定是最简的与或形式。变换后的逻辑函数式可能既不是由单一的与非运算组成的,也不是由单一的或非运算组成的,而且可能是多级函数式。因此,究竟将函数式化成什么形式最有利,要根据选用哪些类型的电子器件而定。此外,在化简一组多输出逻辑函数时,不应仅以孤立地求出每个函数输出的最简形式为目标,而应通过找出并合理利用共用项,以求得总体最简的化简结果。

鉴于现代的数字电路规模日益庞大,产品更新的周期越来越短,因而使用已有的电路模块组成所需要的逻辑电路已经成为设计人员经常使用的方法。这种方法不仅可以提高设计速度,而且有利于降低设计成本。在后面的章节里还将看到,采用模块电路进行设计时,同样需要将逻辑函数式变换成与所用模块电路相适应的形式。

目前用于数字集成电路设计和 PLD 开发的 EDA 软件中, 一般都具备逻辑函数化简和变换的功能。在使用这些 EDA 软件进行设计时, 逻辑函数的化简和变换工作都是由计算机完成的。

---

## Chunk 101/161：`ch02_ex2_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_1 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.1 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_summary_end_theory_1287 |
| next_chunk_id | ch02_ex2_2 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1310–1319 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.1 题干】
[题 2.1] 试用列真值表的方法证明下列异或运算公式。

(1) $A \oplus 0 = A$ (2) $A \oplus 1 = A'$

(3) $A \oplus A = 0$ (4) $A \oplus A' = 1$

(5) $(A\oplus B)\oplus C = A\oplus (B\oplus C)$ (6) $A(B\oplus C) = AB\oplus AC$

(7) $A \oplus B' = (A \oplus B)' = A \oplus B \oplus 1$

【题2.1 解答】
【题 2.1】试用列真值表的方法证明下列异或运算公式。

(1) $A \oplus 0 = A$

(2) $A \oplus 1 = A'$

(3) $A \oplus A = 0$

(4) $A \oplus A' = 1$

(5) $(A \oplus B) \oplus C = A \oplus (B \oplus C)$

(6) $A(B \oplus C) = AB \oplus AC$

(7) $A \oplus B' = (A \oplus B)' = A \oplus B \oplus 1$

解：将输入变量所有的取值逐一代入公式两边计算，然后将计算结果列成真值表。如果两边的真值表相同，则等式成立。

(1) 证明 $A \oplus 0 = A$

<table><tr><td>A</td><td>0</td><td>A $\oplus$ 0</td></tr><tr><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td></tr></table>

(2) 证明 $A \oplus 1 = A'$

<table><tr><td>A</td><td>1</td><td>A $\oplus$ 1</td></tr><tr><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td></tr></table>

<table><tr><td>A</td><td>A</td><td>A⊕A</td></tr><tr><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td></tr></table>

(4) 证明 $A \oplus A' = 1$

<table><tr><td>A</td><td>A&#x27;</td><td>A⊕A&#x27;</td></tr><tr><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td></tr></table>

---

## Chunk 102/161：`ch02_ex2_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_2 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.2 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_1 |
| next_chunk_id | ch02_ex2_3 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1320–1329 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.2 题干】
[题2.2] 证明下列逻辑恒等式(方法不限)

(1) $AB' + B + A'B = A + B$

(2) $(A + C') (B + D)(B + D') = AB + BC'$

(3) $\left((A + B + C')'C'D\right)' + (B + C')\left(AB'D + B'C'\right) = 1$

(4) $A^{\prime}B^{\prime}C^{\prime} + A(B + C) + BC = (AB^{\prime}C^{\prime} + A^{\prime}B^{\prime}C + A^{\prime}BC^{\prime})'$

【题2.2 解答】
【题 2.2】 证明下列逻辑恒等式(方法不限)

(1) $AB' + B + A'B = A + B$

(2) $(A + C') (B + D)(B + D') = AB + BC'$

(3) $\left((A + B + C')'C'D\right)' + (B + C')(AB'D + B'C') = 1$

(4) $A'B'C' + A(B + C) + BC = (AB'C' + A'B'C + A'BC')'$

解：在前面的解题方法中我们介绍了四种证明逻辑恒等式的方法，即列真值表的方法、用公式和定理推演的方法、画卡诺图的方法进行化简的方法。

在实际应用中,除非逻辑式很简单、而且逻辑变量数很少的情况下,一般不宜用列真值表的方法。对多变量、复杂的逻辑等式,通常采用公式推演或公式推演与画卡诺图相结合的方法去证明。如果有条件使用 Multisim 等 EDA 软件进行证明,则更加简单、便捷。

下面采用公式推演的方法来进行证明。

(1) 用公式推演将等式左边化简, 得到

$$
A B ^ {\prime} + B + A ^ {\prime} B = A + A ^ {\prime} B = A + B
$$

所得结果与等式右边相同,故等式成立。

(2) 用公式推演将等式左边化简为

$$
\begin{array}{r l} (A + C ^ {\prime}) (B + D) (B + D ^ {\prime}) & = (A + C ^ {\prime}) (B + B D ^ {\prime} + B D + D D ^ {\prime}) \\ & = (A + C ^ {\prime}) B \end{array}
$$

$$
= A B + B C ^ {\prime}
$$

所得结果与等式右边相同,故等式成立。

（3）用公式推演将等式左边化为

$$
\begin{array}{r l} & \left(\left(A + B + C ^ {\prime}\right) ^ {\prime} C ^ {\prime} D\right) ^ {\prime} + \left(B + C ^ {\prime}\right) \left(A B ^ {\prime} D + B ^ {\prime} C ^ {\prime}\right) \\ & = A + B + C ^ {\prime} + \left(C ^ {\prime} D\right) ^ {\prime} + \left(B + C ^ {\prime}\right) \left(A B ^ {\prime} D + B ^ {\prime} C ^ {\prime}\right) \\ & = A + B + C ^ {\prime} + C + D ^ {\prime} + \left(B + C ^ {\prime}\right) \left(A B ^ {\prime} D + B ^ {\prime} C ^ {\prime}\right) \\ & = \left(C ^ {\prime} + C\right) + A + B + D ^ {\prime} + \left(B + C ^ {\prime}\right) \left(A B ^ {\prime} D + B ^ {\prime} C ^ {\prime}\right) \\ & = 1 + A + B + D ^ {\prime} + \left(B + C ^ {\prime}\right) \left(A B ^ {\prime} D + B ^ {\prime} C ^ {\prime}\right) = 1 \end{array}
$$

故等式成立。

（4）用公式推演将等式左边写成

$$
A ^ {\prime} B ^ {\prime} C ^ {\prime} + A (B + C) + B C = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A B + A C + B C
$$

将等式右边变换为与或式,得到

$$
\begin{array}{r l} (A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B C ^ {\prime}) ^ {\prime} & = (A B ^ {\prime} C ^ {\prime}) ^ {\prime} (A ^ {\prime} B ^ {\prime} C) ^ {\prime} (A ^ {\prime} B C ^ {\prime}) ^ {\prime} \\ & = (A ^ {\prime} + B + C) (A + B + C ^ {\prime}) (A + B ^ {\prime} + C) \\ & = (A ^ {\prime} C ^ {\prime} + B + A C) (A + B ^ {\prime} + C) \\ & = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A B + B C + A C \end{array}
$$

可见，等式成立。

在用公式推导证明逻辑等式时并不要求必须将等式两边化成最简的与或形式, 只要能把等式两边变换为相同的逻辑式就行了。本题的(1)、(2)、(3)小题中, 因为等式右边已经是最简与或式了, 所以将左边的式子化成与右边的式子相同的过程也就是化简过程了。

---

## Chunk 103/161：`ch02_ex2_3`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_3 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.3 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_2 |
| next_chunk_id | ch02_ex2_4 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1330–1339 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.3 题干】
[题2.3] 已知逻辑函数 $Y_{1}$ 和 $Y_{2}$ 的真值表如表P2.3(a)、(b)所示，试写出 $Y_{1}$ 和 $Y_{2}$ 的逻辑函数式。

表 P2.3(a)

<table><tr><td>A</td><td>B</td><td>C</td><td> ${Y}_{1}$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

表 P2.3(b)

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td> ${Y}_{2}$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

【题2.3 解答】
【题 2.3】已知逻辑函数 $Y_{1}$ 和 $Y_{2}$ 的真值表如表 P2.3(a)、(b) 所示，试写出 $Y_{1}$ 和 $Y_{2}$ 的逻辑函数式。

表 P2.3(a)  
表 P2.3(b)

<table><tr><td>A</td><td>B</td><td>C</td><td> $Y_1$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td> $1 \rightarrow A'B'C'$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td> $1 \rightarrow A'B'C$ </td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td> $1 \rightarrow AB'C'$ </td></tr><tr><td>1</td><td>0</td><td>1</td><td> $1 \rightarrow AB'C$ </td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td> $1 \rightarrow ABC$ </td></tr></table>

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td> ${Y}_{2}$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td> $1 \rightarrow {A}^{\prime }{B}^{\prime }{C}^{\prime }{D}$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td> $1 \rightarrow {A}^{\prime }{B}^{\prime }{CD}^{\prime }$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td> $1 \rightarrow {A}^{\prime }{BC}^{\prime }{D}^{\prime }$ </td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td> $1 \rightarrow {A}^{\prime }{BCD}$ </td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td> $1 \rightarrow {AB}^{\prime }{C}^{\prime }{D}^{\prime }$ </td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td> $1 \rightarrow {AB}^{\prime }{CD}$ </td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td> $1 \rightarrow {ABC}^{\prime }{D}$ </td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td> $1 \rightarrow {ABCD}^{\prime }$ </td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

解：找出 $Y_{1}$ （或 $Y_{2}$ ）为 1 时的输入变量取值组合，写出在这些变量取值下其值为 1 的最小项（如表中所示），将这些最小项相加，得到

$$
Y _ {1} = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A B ^ {\prime} C ^ {\prime} + A B ^ {\prime} C + A B C
$$

$$
Y _ {2} = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A ^ {\prime} B C ^ {\prime} D ^ {\prime} + A ^ {\prime} B C D + A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C D + A B C ^ {\prime} D + A B C D ^ {\prime}
$$

---

## Chunk 104/161：`ch02_ex2_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_4 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.4 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_3 |
| next_chunk_id | ch02_ex2_5 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1340–1344 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.4 题干】
[题 2.4] 已知逻辑函数的真值表如表 P2.4(a)、(b) 所示, 试写出对应的逻辑函数式。  
表 P2.4(a)

<table><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

【题2.4 解答】
【题 2.4】已知逻辑函数的真值表如表 P2.4(a)、(b) 所示, 试写出对应的逻辑函数式。

解：参见上题的说明。

$$
Y = A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B C ^ {\prime} + A B ^ {\prime} C ^ {\prime}
$$

$$
Z = M ^ {\prime} N ^ {\prime} P Q + M ^ {\prime} N P Q ^ {\prime} + M ^ {\prime} N P Q + M N ^ {\prime} P Q + M N P ^ {\prime} Q ^ {\prime} + M N P ^ {\prime} Q + M N P Q ^ {\prime} + M N P Q
$$

表 P2.4(a)

<table><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

表 P2.4(b)

<table><tr><td>M</td><td>N</td><td>P</td><td>Q</td><td>Z</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

---

## Chunk 105/161：`ch02_ex2_5`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_5 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.5 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_4 |
| next_chunk_id | ch02_ex2_6 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1345–1354 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.5 题干】
[题 2.5] 列出下列逻辑函数的真值表。

(1) $Y_{1}=A^{\prime}B+BC+ACD^{\prime}$

(2) $Y_{2}=A^{\prime}B^{\prime}CD^{\prime}+(B\oplus C)^{\prime}D+AD$

表 P2.4(b)

<table><tr><td>M</td><td>N</td><td>P</td><td>Q</td><td>Z</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

【题2.5 解答】
【题 2.5】列出下列逻辑函数的真值表。

(1) $Y_{1}=A^{\prime}B+BC+ACD^{\prime}$

(2) $Y_{2}=A^{\prime}B^{\prime}CD^{\prime}+(B\oplus C)^{\prime}D+AD$

解：

(1) $Y_{1}$ 的真值表如表 A2.5(a)。

(2) 如果采用全部列表的方法, 为直观起见, 可以将 $Y_{2}$ 式展开为

$$
Y _ {2} = A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A D + B ^ {\prime} C ^ {\prime} D + B C D
$$

然后列出如表 A2.5(b) 的真值表。

表 A2.5(a) $Y_{1}$ 的真值表

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td> $A^{\prime}B$ </td><td>BC</td><td> $ACD^{\prime}$ </td><td> $Y_1$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td></tr></table>

表 A2.5(b) $Y_{2}$ 的真值表

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td> $A^{\prime}B^{\prime}CD^{\prime}$ </td><td>AD</td><td> $B^{\prime}C^{\prime}D$ </td><td>BCD</td><td> $Y_{2}$ </td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td></tr></table>

也可以将 ABCD 的十六种取值逐一代入 $Y_{1}$ 和 $Y_{2}$ 的式中计算，求出对应的输出值，然后列出只包含 ABCD 与 $Y_{1}$ 和 $Y_{2}$ 对应取值的真值表。

---

## Chunk 106/161：`ch02_ex2_6`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_6 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.6 |
| example_id | — |
| figure_ids | 图P2.6(a), 图P2.6(b) |
| prev_chunk_id | ch02_ex2_5 |
| next_chunk_id | ch02_ex2_7 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1355–1364 |

### 配图

**图P2.6(a)** — 图P2.6 子图(a)

![图P2.6(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/0e9fe75769d743d99f92bb454659685f7f9530a445b623467b6641ec29c36d33.jpg)

*视觉描述：* 两非门与三与非门构成异或电路：A、B经反相后分别送入两个二输入与非门，末级与非输出Y1=A⊕B，为异或逻辑的标准与非门实现。

**图P2.6(b)** — 图P2.6 子图(b)

![图P2.6(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/ad5950e3aa20545d2186a35893ecf04664844cb8227fd54d12490a16f3d2f80a.jpg)

*视觉描述：* 含异或、非、与非、或非的组合电路：A⊕B与(B·C')'经末级或非得Y2=((A⊕B)+(B·C'))'，输入为A、B、C。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.6 题干】
[题 2.6] 写出图 P2.6(a)、(b) 所示电路的输出逻辑函数式。

(a)  
(b)  

(b)  
图P2.6

【题2.6 解答】
【题 2.6】写出图 P2.6(a)、(b) 所示电路的输出逻辑函数式。

(a)

(b)  
图P2.6

解：从输入端向输出端逐级写出每个门的输出逻辑式，如图中所示，可得到

$$
\begin{array}{r l} Y _ {1} & = \left(\left(A B ^ {\prime}\right) ^ {\prime} \left(A ^ {\prime} B\right) ^ {\prime}\right) ^ {\prime} = A B ^ {\prime} + A ^ {\prime} B = A \oplus B \\ Y _ {2} & = \left(\left(A \oplus B\right) + \left(B C ^ {\prime}\right) ^ {\prime}\right) ^ {\prime} = A B C ^ {\prime} \end{array}
$$

因题目未要求化简,所以写出哪一步的式子都可以。

[图P2.6(a)] 图P2.6 子图(a)
[图P2.6(a)描述] 两非门与三与非门构成异或电路：A、B经反相后分别送入两个二输入与非门，末级与非输出Y1=A⊕B，为异或逻辑的标准与非门实现。
[图P2.6(b)] 图P2.6 子图(b)
[图P2.6(b)描述] 含异或、非、与非、或非的组合电路：A⊕B与(B·C')'经末级或非得Y2=((A⊕B)+(B·C'))'，输入为A、B、C。

---

## Chunk 107/161：`ch02_ex2_7`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_7 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.7 |
| example_id | — |
| figure_ids | 图P2.7(a), 图P2.7(b) |
| prev_chunk_id | ch02_ex2_6 |
| next_chunk_id | ch02_ex2_8 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1365–1372 |

### 配图

**图P2.7(a)** — 图P2.7 子图(a)

![图P2.7(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/88a9692b334b7f26abde84d780cf2b8707b6413ad040d094654517b63516eac4.jpg)

*视觉描述：* 四输入组合电路：A、B经或非后与C进上方与非，C经非后与D进下方与非，两路与异或门得输出Y1，含或非、非、与非、异或门。

**图P2.7(b)** — 图P2.7 子图(b)

![图P2.7(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/7d66c572670b51c50b582f1c5ef3e4fa00442ab30681117092a29d44e7affd4f.jpg)

*视觉描述：* 五输入多级组合电路：B经非门后与A进二输入与非、与C、D进三输入与非，两路与E分别相与后送或非门得输出Y2。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.7 题干】
[题 2.7] 写出图 P2.7(a)、(b) 所示电路的输出逻辑函数式。

(a)

图P2.7

【题2.7 解答】
【题 2.7】 写出图 P2.7(a)、(b) 所示电路的输出逻辑函数式。

(a)

图 P2.7

解：从输入向输出逐级写出每个门的输出逻辑式，如图中所示，得到

$$
\begin{array}{r l} Y _ {1} & = ((A + B) ^ {\prime} C) ^ {\prime} \oplus (C ^ {\prime} D) ^ {\prime} \\ & = (A ^ {\prime} B ^ {\prime} C) ^ {\prime} \oplus (C ^ {\prime} D) ^ {\prime} \\ & = A ^ {\prime} B ^ {\prime} C (C + D ^ {\prime}) + (A + B + C ^ {\prime}) C ^ {\prime} D \\ & = A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A C ^ {\prime} D + B C ^ {\prime} D + C ^ {\prime} D \\ & = A ^ {\prime} B ^ {\prime} C + C ^ {\prime} D \\ Y _ {2} & = ((A B ^ {\prime}) ^ {\prime} E + (B ^ {\prime} C D) ^ {\prime} E) ^ {\prime} \\ & = ((A B ^ {\prime}) ^ {\prime} E) ^ {\prime} ((B ^ {\prime} C D) ^ {\prime} E) ^ {\prime} \\ & = (A B ^ {\prime} + E ^ {\prime}) (B ^ {\prime} C D + E ^ {\prime}) \\ & = A B ^ {\prime} C D + E ^ {\prime} \end{array}
$$

因为题目没有要求化简,所以写出逻辑式的哪一步都是可以的。

[图P2.7(a)] 图P2.7 子图(a)
[图P2.7(a)描述] 四输入组合电路：A、B经或非后与C进上方与非，C经非后与D进下方与非，两路与异或门得输出Y1，含或非、非、与非、异或门。
[图P2.7(b)] 图P2.7 子图(b)
[图P2.7(b)描述] 五输入多级组合电路：B经非门后与A进二输入与非、与C、D进三输入与非，两路与E分别相与后送或非门得输出Y2。

---

## Chunk 108/161：`ch02_ex2_8`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_8 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.8 |
| example_id | — |
| figure_ids | 图P2.8 |
| prev_chunk_id | ch02_ex2_7 |
| next_chunk_id | ch02_ex2_9 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1373–1377 |

### 配图

**图P2.8** — 图P2.8

![图P2.8](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c3222e8d4333dec5dfb73708fa572a9cffa5472fc9c3e383ca445f01ab18632b.jpg)

*视觉描述：* A、B、C及Y的时序波形图：A频率最高，B为其一半，C再减半；Y在A=1且B、C异或时为高，对应Y=A·(B⊕C)。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.8 题干】
[题2.8] 已知逻辑函数 $Y$ 的波形图如图P2.8所示，试求 $Y$ 的真值表和逻辑函数式。

图P2.8

【题2.8 解答】
【题 2.8】已知逻辑函数 Y 的波形图如图 P2.8 所示, 试求 Y 的真值表和逻辑函数式。

图P2.8

解：根据波形图列出 Y 与 A、B、C 关系的真值表，如表 A2.8。从真值表写出逻辑式为

$$
Y = A B C ^ {\prime} + A B ^ {\prime} C + A ^ {\prime} B C
$$

表 A2.8

<table><tr><td>C</td><td>B</td><td>A</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

[图P2.8] 图P2.8
[图P2.8描述] A、B、C及Y的时序波形图：A频率最高，B为其一半，C再减半；Y在A=1且B、C异或时为高，对应Y=A·(B⊕C)。

---

## Chunk 109/161：`ch02_ex2_9`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_9 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.9 |
| example_id | — |
| figure_ids | 图P2.9 |
| prev_chunk_id | ch02_ex2_8 |
| next_chunk_id | ch02_ex2_10 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1378–1379 |

### 配图

**图P2.9** — 图 P2.9

![图P2.9](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/f15c574af5b395c46655c3e1eab9c460e170cc6611e2c38334cb9ed26add375f.jpg)

*视觉描述：* 四输入A0~A3与输出Y的时序波形：A0为最低位计数频率最高，按二进制递增排列，虚线对齐各时刻逻辑电平以分析组合逻辑功能。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.9 题干】
[题2.9] 给定逻辑函数 $Y$ 的波形图如图P2.9所示，试写出该逻辑函数的真值表和逻辑函数式。

【题2.9 解答】
【题 2.9】给定逻辑函数 Y 的波形图如图 P2.9 所示, 试写出该逻辑函数的真值表和逻辑函数式。

图P2.9

解：由给定的波形图中每个时间段里 Y 与 $A_{0}$ 、 $A_{1}$ 、 $A_{2}$ 、 $A_{3}$ 对应的取值可列出函数的真值表，如表 A2.9。从真值表写出相应的逻辑式，得到

$$
\begin{array}{r l} Y & = A _ {3} ^ {\prime} A _ {2} ^ {\prime} A _ {1} ^ {\prime} A _ {0} + A _ {3} ^ {\prime} A _ {2} ^ {\prime} A _ {1} A _ {0} ^ {\prime} + A _ {3} ^ {\prime} A _ {2} A _ {1} ^ {\prime} A _ {0} ^ {\prime} + A _ {3} ^ {\prime} A _ {2} A _ {1} A _ {0} + A _ {3} A _ {2} ^ {\prime} A _ {1} ^ {\prime} A _ {0} ^ {\prime} \\ & \quad + A _ {3} A _ {2} ^ {\prime} A _ {1} A _ {0} + A _ {3} A _ {2} A _ {1} ^ {\prime} A _ {0} + A _ {3} A _ {2} A _ {1} A _ {0} ^ {\prime} \end{array}
$$

表 A2.9

<table><tr><td> $A_3$ </td><td> $A_2$ </td><td> $A_1$ </td><td> $A_0$ </td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

[图P2.9] 图 P2.9
[图P2.9描述] 四输入A0~A3与输出Y的时序波形：A0为最低位计数频率最高，按二进制递增排列，虚线对齐各时刻逻辑电平以分析组合逻辑功能。

---

## Chunk 110/161：`ch02_ex2_10`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_10 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.10 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_9 |
| next_chunk_id | ch02_ex2_11 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1380–1387 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.10 题干】
[题 2.10] 将下列各函数式化为最小项之和的形式。

(1) $Y = A^{\prime}BC + AC + B^{\prime}C$ (2) $Y = AB^{\prime}C^{\prime}D + BCD + A^{\prime}D$

(3) $Y = A + B + CD$ (4) $Y = AB + ((BC)'(C' + D'))'$

(5) $Y = LM' + MN' + NL'$ (6) $Y = ((A \odot B)(C \odot D))'$

【题2.10 解答】
【题 2.10】将下列各函数式化为最小项之和的形式。

(1) $Y = A'BC + AC + B'C$

(2) $Y = AB'C'D + BCD + A'D$

(3) $Y = A + B + CD$

(4) $Y = AB + ((BC)'(C' + D'))'$

(5) $Y = LM' + MN' + NL'$

(6) $Y = ((A \odot B)(C \odot D))'$

解：

(1) $Y = A'BC + AC(B + B') + B'C(A + A')$ $= A'BC + AB'C + ABC + A'B'C$

(2) $Y = AB'C'D + (A + A')BCD + A'D(B + B')(C + C')$ $= AB'C'D + A'BCD + ABCD + A'B'C'D + A'B'CD + A'BC'D$

(3) $Y = A(B + B') + B(A + A') + CD(A + A')(B + B')$ $= AB(C + C')(D + D') + A'B(C + C')(D + D') + AB'(C + C')(D + D') + CD(A + A')(B + B')$ $= A'B'CD + A'BC'D' + A'BC'D + A'BCD' + A'BCD + AB'C'D' + AB'C'D + AB'CD' + AB'CD + ABC'D' + ABC'D + ABCD' + ABCD$ $= \sum m(3,4,5,6,7,8,9,10,11,12,13,14,15)$

(4) $Y = AB + BC + CD$ $= ABC'D' + ABC'D + ABCD' + ABCD + A'BCD' + A'BCD + A'B'CD + AB'CD$

(5) $Y = LM'N' + LM'N + L'MN' + LMN' + L'M'N + L'MN$

(6) $Y = (A \odot B)' + (C \odot D)' = (A \oplus B) + (C \oplus D)$ $= A'B + AB' + C'D + CD'$ $= A'BC'D' + A'BC'D + A'BCD' + A'BCD + AB'C'D' + AB'C'D + AB'CD' + AB'CD + A'B'CD' + ABCD' + A'B'C'D + ABC'D$ $= \sum m(1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)$

---

## Chunk 111/161：`ch02_ex2_11`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_11 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.11 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_10 |
| next_chunk_id | ch02_ex2_12 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1388–1404 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.11 题干】
[题2.11] 将下列各式化为最大项之积的形式。

(1) $Y = (A + B)(A' + B' + C')$

(2) $Y = AB' + C$

图 P2.9

(3) $Y = A^{\prime}BC^{\prime} + B^{\prime}C + AB^{\prime}C$

(4) $Y = BCD' + C + A'D$

(5) $Y(A,B,C)=\sum m(1,2,4,6,7)$

(6) $Y(A,B,C,D)=\sum m(0,1,2,4,5,6,8,10,11,12,14,15)$

【题2.11 解答】
【题 2.11】 将下列各式化为最大项之积的形式。

(1) $Y = (A + B)(A' + B' + C')$

(2) $Y = AB' + C$

(3) $Y = A^{\prime}BC^{\prime} + B^{\prime}C + AB^{\prime}C$

(4) $Y = BCD' + C + A'D$

(5) $Y(A,B,C)=\sum m(1,2,4,6,7)$

(6) $Y(A,B,C,D)=\sum m(0,1,2,4,5,6,8,10,11,12,14,15)$

解：

(1) $Y = (A + B + CC') (A' + B' + C')$ $= (A + B + C)(A + B + C')(A' + B' + C')$

(2) $Y = (A + C)(B' + C)$

$$
\begin{array}{r l} & = (A + B B ^ {\prime} + C) (A A ^ {\prime} + B ^ {\prime} + C) \\ & = (A + B ^ {\prime} + C) (A + B + C) (A ^ {\prime} + B ^ {\prime} + C) \end{array}
$$

(3) 首先将 Y 展开为最小项之和形式, 得到

$$
Y (A, B, C) = m _ {1} + m _ {2} + m _ {5}
$$

根据 $Y+Y'=1$ 以及全部最小项之和为 1 可知

$$
\begin{array}{r l} & Y ^ {\prime} = m _ {0} + m _ {3} + m _ {4} + m _ {6} + m _ {7} \\ & Y = (Y ^ {\prime}) ^ {\prime} = (m _ {0} + m _ {3} + m _ {4} + m _ {6} + m _ {7}) ^ {\prime} \\ & = m _ {0} ^ {\prime} m _ {3} ^ {\prime} m _ {4} ^ {\prime} m _ {6} ^ {\prime} m _ {7} ^ {\prime} \end{array}
$$

又知 $m_i' = M_i$ ，故得

$$
\begin{array}{r l} Y & = M _ {0} M _ {3} M _ {4} M _ {6} M _ {7} \\ & = (A + B + C) (A + B ^ {\prime} + C ^ {\prime}) (A ^ {\prime} + B + C) (A ^ {\prime} + B ^ {\prime} + C) (A ^ {\prime} + B ^ {\prime} + C ^ {\prime}) \\ (4) Y & = B C D ^ {\prime} + C + A ^ {\prime} D \\ & = C + A ^ {\prime} D \\ & = (A ^ {\prime} + C) (C + D) \\ & = (A ^ {\prime} + B B ^ {\prime} + C) (A A ^ {\prime} + C + D) \\ & = (A ^ {\prime} + B ^ {\prime} + C + D D ^ {\prime}) (A ^ {\prime} + B + C + D D ^ {\prime}) \\ & \quad (A ^ {\prime} + B B ^ {\prime} + C + D) (A + B B ^ {\prime} + C + D) \\ & = (A ^ {\prime} + B ^ {\prime} + C + D ^ {\prime}) (A ^ {\prime} + B ^ {\prime} + C + D) \\ & \quad (A ^ {\prime} + B + C + D ^ {\prime}) (A ^ {\prime} + B + C + D) \\ & \quad (A + B ^ {\prime} + C + D) (A + B + C + D) \end{array}
$$

(5) 因为已知 $Y(A, B, C) = m_{1} + m_{2} + m_{4} + m_{6} + m_{7}$ ，所以

$$
\begin{array}{r l} & Y ^ {\prime} (A, B, C) = m _ {0} + m _ {3} + m _ {5} \\ & Y (A, B, C) = (Y ^ {\prime}) ^ {\prime} = (m _ {0} + m _ {3} + m _ {5}) ^ {\prime} = m _ {0} ^ {\prime} \cdot m _ {3} ^ {\prime} \cdot m _ {5} ^ {\prime} \\ & \quad = M _ {0} \cdot M _ {3} \cdot M _ {5} \\ & \quad = (A + B + C) (A + B ^ {\prime} + C ^ {\prime}) (A ^ {\prime} + B + C ^ {\prime}) \end{array}
$$

(6) 因为已知

$$
\begin{array}{r l} Y (A, B, C, D) & = m _ {0} + m _ {1} + m _ {2} + m _ {4} + m _ {5} + m _ {6} + m _ {8} + m _ {1 0} + \\ & \quad m _ {1 1} + m _ {1 2} + m _ {1 4} + m _ {1 5} \end{array}
$$

所以可知

$$
\begin{array}{r l} Y ^ {\prime} (A, B, C, D) & = m _ {3} + m _ {7} + m _ {9} + m _ {1 3} \\ Y (A, B, C, D) & = (Y ^ {\prime}) ^ {\prime} = (m _ {3} + m _ {7} + m _ {9} + m _ {1 3}) ^ {\prime} \\ & = m _ {3} ^ {\prime} \cdot m _ {7} ^ {\prime} \cdot m _ {9} ^ {\prime} \cdot m _ {1 3} ^ {\prime} \\ & = M _ {3} \cdot M _ {7} \cdot M _ {9} \cdot M _ {1 3} \\ & = (A + B + C ^ {\prime} + D ^ {\prime}) (A + B ^ {\prime} + C ^ {\prime} + D ^ {\prime}) \\ & (A ^ {\prime} + B + C + D ^ {\prime}) (A ^ {\prime} + B ^ {\prime} + C + D ^ {\prime}) \end{array}
$$

---

## Chunk 112/161：`ch02_ex2_12`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_12 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.12 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_11 |
| next_chunk_id | ch02_ex2_13 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1405–1407 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.12 题干】
[题 2.12] 利用逻辑代数的基本公式和常用公式化简下列各式。
(1) $ACD'+D'$ (2) $AB'(A+B)$ (3) $AB'+AC+BC$ (4) $AB(A+B'C)$ (5) $E'F'+E'F+EF'+EF$ (6) $ABD+AB'CD'+AC'DE+A$ (7) $A'BC+(A+B')C$ (8) $AC+BC'+A'B$

【题2.12 解答】
【题 2.12】 利用逻辑代数的基本公式和常用公式化简下列各式。

(1) $ACD'+D'$

(2) $AB'(A+B)$

(3) $AB' + AC + BC$

(4) $AB(A + B'C)$

(5) $E^{\prime}F^{\prime} + E^{\prime}F + EF^{\prime} + EF$

(6) $ABD + AB'CD' + AC'DE + A$

(7) $A^{\prime}BC+(A+B^{\prime})C$

(8) $AC + BC' + A'B$

解：

(1) $ACD' + D' = D'$

(2) $AB^{\prime}(A + B) = AB^{\prime}$

(3) $AB' + AC + BC = AB' + BC$

(4) $AB(A + B'C) = AB$

(5) $E^{\prime}F^{\prime} + E^{\prime}F + EF^{\prime} + EF = E^{\prime}(F^{\prime} + F) + E(F^{\prime} + F) = E^{\prime} + E = 1$

(6) $ABD + AB'CD' + AC'DE + A = A$

(7) $A^{\prime}BC + (A + B^{\prime})C = (A^{\prime}B)C + (A^{\prime}B)^{\prime}C = C$

(8) $AC + BC' + A'B = AC + B(A' + C') = AC + (AC)'B = AC + B$

---

## Chunk 113/161：`ch02_ex2_13`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_13 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.13 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_12 |
| next_chunk_id | ch02_ex2_14 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1408–1429 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.13 题干】
[题 2.13] 用逻辑代数的基本公式和常用公式将下列逻辑函数化为最简与或形式。

(1) $Y = AB' + B + A'B$

(2) $Y = AB'C + A' + B + C'$

(3) $Y = (A'BC)' + (AB')'$

(4) $Y = AB'CD + ABD + AC'D$

(5) $Y = AB'(A'CD + (AD + B'C')') (A' + B)$

(6) $Y = AC(C'D + A'B) + BC((B' + AD)' + CE)'$

(7) $Y = AC' + ABC + ACD' + CD$

(8) $Y = A + (B + C')' (A + B' + C) (A + B + C)$

(9) $Y = BC' + ABC'E + B'(A'D' + AD)' + B(AD' + A'D)$

(10) $Y = AC + AC'D + AB'E'F + B(D \oplus E) + BC'DE' + BC'D'E + ABE'F$

【题2.13 解答】
【题 2.13】用逻辑代数的基本公式和常用公式将下列逻辑函数化为最简与或形式。

(1) $Y = AB' + B + A'B$

(2) $Y = AB'C + A' + B + C'$

(3) $Y = (A'BC)' + (AB')'$

(4) $Y = AB'CD + ABD + AC'D$

(5) $Y = AB'(A'CD + (AD + B'C')') (A' + B)$

(6) $Y = AC(C'D + A'B) + BC((B' + AD)' + CE)'$

(7) $Y = AC' + ABC + ACD' + CD$

(8) $Y = A + (B + C')' (A + B' + C) (A + B + C)$

(9) $Y = BC' + ABC'E + B'(A'D' + AD)' + B(AD' + A'D)$

(10) $Y = AC + AC'D + AB'E'F + B(D \oplus E) + BC'DE' + BC'D'E + ABE'F$

解：

(1) $Y = AB' + B + A'B = AB' + B = A + B$

(2) $Y = AB'C + A' + B + C' = AB'C + (AB'C)' = 1$

(3) $Y = (A'BC)' + (AB')' = A + B' + C' + A' + B$ $= (A + A') + (B + B') + C' = 1$

(4) $Y = AB'CD + ABD + AC'D = AD(B'C + B + C') = AD(C + C') = AD$

(5) $Y = AB'(A'CD + (AD + B'C')') (A' + B)$ $= (AB')(AB')'(A'CD + (AD + B'C')') = 0$

(6) $Y = AC(C'D + A'B) + BC((B' + AD)' + CE)'$ $= BC(B' + AD)(CE)' = ABCD(C'E') = ABCDE'$

(7) $Y = AC' + ABC + ACD' + CD = A(C' + BC) + C(AD' + D)$ $= A(C' + B) + C(A + D)$


$$
\begin{array}{r l} & = A C ^ {\prime} + A B + A C + C D = A (C + C ^ {\prime}) + A B + C D \\ & = A + C D \end{array}
$$

$$
\begin{array}{r l} (8) Y & = A + (B + C ^ {\prime}) ^ {\prime} (A + B ^ {\prime} + C) (A + B + C) = A + B ^ {\prime} C (A + C) \\ & = A + A B ^ {\prime} C + B ^ {\prime} C = A + B ^ {\prime} C \end{array}
$$

$$
\begin{array}{r l} Y & = B C ^ {\prime} + A B C ^ {\prime} E + B ^ {\prime} (A ^ {\prime} D ^ {\prime} + A D) ^ {\prime} + B (A D ^ {\prime} + A ^ {\prime} D) \\ & = B C ^ {\prime} + B ^ {\prime} (A D ^ {\prime} + A ^ {\prime} D) + B (A D ^ {\prime} + A ^ {\prime} D) \\ & = B C ^ {\prime} + (B ^ {\prime} + B) (A D ^ {\prime} + A ^ {\prime} D) = B C ^ {\prime} + A D ^ {\prime} + A ^ {\prime} D \end{array} \tag {9}
$$

$$
\begin{array}{r l} (1 0) Y & = A C + A C ^ {\prime} D + A B ^ {\prime} E ^ {\prime} F + B (D \oplus E) + B C ^ {\prime} D E ^ {\prime} + B C ^ {\prime} D ^ {\prime} E + A B E ^ {\prime} F \\ & = A C + A C D + A C ^ {\prime} D + A B ^ {\prime} E ^ {\prime} F + B (D \oplus E) + B C ^ {\prime} (D \oplus E) + A B E ^ {\prime} F \\ & = A C + A D + A E ^ {\prime} F (B ^ {\prime} + B) + B (D \oplus E) \\ & = A C + A D + A E ^ {\prime} F + B (D \oplus E) \end{array}
$$

---

## Chunk 114/161：`ch02_ex2_14`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_14 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.14 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_13 |
| next_chunk_id | ch02_ex2_15 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1430–1431 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.14 题干】
[题 2.14] 写出图 P2.14 中各卡诺图所表示的逻辑函数式。

【题2.14 解答】
【题 2.14】 写出图 P2.14 中各卡诺图所表示的逻辑函数式。

(a)


(b)  
(c)  
(d)  
图 P2.14

解：

$$
(a) Y = A ^ {\prime} B C + A B ^ {\prime} C ^ {\prime} + A B ^ {\prime} C + A B C ^ {\prime}
$$

$$
(b) Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A ^ {\prime} B C ^ {\prime} D + A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C D ^ {\prime} + A B C D
$$

$$
(c) Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A ^ {\prime} B C ^ {\prime} D + A ^ {\prime} B C D + A B ^ {\prime} C D ^ {\prime} + A B C ^ {\prime} D ^ {\prime} + A B C D
$$

$$
(\mathrm{d}) Y = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} + A ^ {\prime} B ^ {\prime} C D ^ {\prime} E + A ^ {\prime} B ^ {\prime} C D E + A ^ {\prime} B C ^ {\prime} D ^ {\prime} E + A ^ {\prime} B C ^ {\prime} D E +
$$

$$
A ^ {\prime} B C D ^ {\prime} E ^ {\prime} + A B ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} + A B ^ {\prime} C ^ {\prime} D E ^ {\prime} + A B ^ {\prime} C ^ {\prime} D E + A B C D ^ {\prime} E + A B C D E
$$

---

## Chunk 115/161：`ch02_ex2_15`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_15 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.15 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_14 |
| next_chunk_id | ch02_ex2_16 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1432–1441 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.15 题干】
[题 2.15] 用卡诺图化简法化简以下逻辑函数。

(1) $Y_{1}=C+ABC$

(2) $Y_{2}=AB'C+BC+A'BC'D$

(3) $Y_{3}(A,B,C) = \sum m(1,2,3,7)$

(4) $Y_{4}(A,B,C,D)=\sum m(0,1,2,3,4,6,8,9,10,11,14)$

【题2.15 解答】
【题 2.15】用卡诺图化简法化简以下逻辑函数。

(1) $Y_{1}=C+ABC$

(2) $Y_{2}=AB'C+BC+A'BC'D$

(3) $Y_{3}(A,B,C) = \sum m(1,2,3,7)$

(4) $Y_{4}(A,B,C,D) = \sum m(0,1,2,3,4,6,8,9,10,11,14)$

解：

(1) 画出 $Y_{1}$ 的卡诺图, 如图 A2.15(a)。将图中的 1 合并, 得到

$$
Y _ {1} = C
$$

(a)

(b)

(c)

(d)  
图A2.15

(2) 画出 $Y_{2}$ 的卡诺图, 如图 A2.15(b)。按图中合并最小项方法得到

$$
Y _ {2} = A ^ {\prime} B D + A C + B C
$$

(3) 画出 $Y_{3}$ 的卡诺图, 如图 A2.15(c)。合并最小项后得到

$$
Y _ {3} = A ^ {\prime} B + A ^ {\prime} C + B C
$$

(4) 画出 $Y_{4}$ 的卡诺图, 如图 A2.15(d)。合并最小项后得到

$$
Y _ {4} = A ^ {\prime} D ^ {\prime} + C D ^ {\prime} + B ^ {\prime}
$$

---

## Chunk 116/161：`ch02_ex2_16`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_16 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.16 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_15 |
| next_chunk_id | ch02_ex2_17 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1442–1473 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.16 题干】
[题 2.16] 用卡诺图化简法将下列函数化为最简与或形式。

(1) $Y = ABC + ABD + C'D' + AB'C + A'CD' + AC'D$

(a)

(b)


<table><tr><td>AB\CDE</td><td>000</td><td>001</td><td>011</td><td>010</td><td>110</td><td>111</td><td>101</td><td>100</td></tr><tr><td>00</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>01</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td></tr><tr><td>11</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>10</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

(c)  
(d)  
图P2.14

(2) $Y = AB' + A'C + BC + C'D$

(3) $Y = A'B' + BC' + A' + B' + ABC$

(4) $Y = A'B' + AC + B'C$

(5) $Y = AB'C' + A'B' + A'D + C + BD$

(6) $Y(A,B,C)=\sum m(0,1,2,5,6,7)$

(7) $Y(A,B,C,D)=\sum m(0,1,2,5,8,9,10,12,14)$

(8) $Y(A,B,C)=\sum m(1,4,7)$

【题2.16 解答】
【题 2.16】用卡诺图化简法将下列函数化为最简与或形式。

(1) $Y = ABC + ABD + C'D' + AB'C + A'CD' + AC'D$

(2) $Y = AB' + A'C + BC + C'D$

(3) $Y = A'B' + BC' + A' + B' + ABC$

(4) $Y = A'B' + AC + B'C$

(5) $Y = AB'C' + A'B' + A'D + C + BD$

(6) $Y(A,B,C)=\sum m(0,1,2,5,6,7)$

(7) $Y(A,B,C,D)=\sum m(0,1,2,5,8,9,10,12,14)$

(8) $Y(A,B,C)=\sum m(1,4,7)$

解：

(1) 画出函数的卡诺图, 如图 A2.16(a)。合并最小项后得到

$$
Y = A + D ^ {\prime}
$$

(a)


(c)

(b)  

(e)

(d)  

(g)

(f)  
(h)  
图A2.16

(2) 画出函数的卡诺图, 如图 A2.16(b)。合并最小项后得到

$$
Y = A B ^ {\prime} + C + D
$$

（3）画出函数的卡诺图，如图 A2.16(c)。合并最小项后得到

$$
Y = 1
$$

（4）画出函数的卡诺图，如图 A2.16(d)。合并最小项后得到

$$
Y = A ^ {\prime} B ^ {\prime} + A C
$$

(5) 画出函数的卡诺图, 如图 A2.16(e)。合并最小项后得到

$$
Y = B ^ {\prime} + C + D
$$

(6) 画出函数的卡诺图, 如图 A2.16(f)。合并最小项后得到

$$
Y = A ^ {\prime} B ^ {\prime} + A C + B C ^ {\prime}
$$

(7) 画出函数的卡诺图, 如图 A2.16(g)。合并最小项后得到

$$
Y = A D ^ {\prime} + B ^ {\prime} C ^ {\prime} + B ^ {\prime} D ^ {\prime} + A ^ {\prime} C ^ {\prime} D
$$

(8) 画出函数的卡诺图, 如图 A2.16(h)。由于最小项已不能合并, 故仍为

$$
Y = A ^ {\prime} B ^ {\prime} C + A B ^ {\prime} C ^ {\prime} + A B C = \sum m (1, 4, 7)
$$

---

## Chunk 117/161：`ch02_ex2_17`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_17 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.17 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_16 |
| next_chunk_id | ch02_ex2_18 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1474–1485 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.17 题干】
[题 2.17] 化简下列逻辑函数(方法不限)。

(1) $Y = AB' + A'C + C'D' + D$

(2) $Y = A'(CD' + C'D) + BC'D + AC'D + A'CD'$

(3) $Y = \left( \left( A' + B' \right) D \right)' + \left( A'B' + BD \right) C' + A'C'BD + D'$

(4) $Y = AB'D + A'B'C'D + B'CD + (AB'C)'(B + D)$

(5) $Y = (AB'C'D + AC'DE + B'DE' + AC'D'E)'$

【题2.17 解答】
【题 2.17】化简下列逻辑函数(方法不限)。

(1) $Y = AB' + A'C + C'D' + D$

(2) $Y = A'(CD' + C'D) + BC'D + AC'D + A'CD'$

(3) $Y = ((A' + B')D)' + (A'B' + BD)C' + A'BC'D + D'$

(4) $Y = AB'D + A'B'C'D + B'CD + (AB'+C)'(B+D)$

(5) $Y = (AB'C'D + AC'DE + B'DE' + AC'D'E)'$

解：

$$
\begin{array}{r l} Y & = A B ^ {\prime} + A ^ {\prime} C + C ^ {\prime} D ^ {\prime} + D = A B ^ {\prime} + A ^ {\prime} C + C ^ {\prime} + D = A B ^ {\prime} + A ^ {\prime} + C ^ {\prime} + D \\ & = A ^ {\prime} + B ^ {\prime} + C ^ {\prime} + D \end{array} \tag {1}
$$

$$
\begin{array}{r l} (2) Y & = A ^ {\prime} (C D ^ {\prime} + C ^ {\prime} D) + B C ^ {\prime} D + A C ^ {\prime} D + A ^ {\prime} C D ^ {\prime} \\ & = A ^ {\prime} C D ^ {\prime} + A ^ {\prime} C ^ {\prime} D + B C ^ {\prime} D + A C ^ {\prime} D + A ^ {\prime} C D ^ {\prime} \\ & = C ^ {\prime} D (A ^ {\prime} + A) + B C ^ {\prime} D + A ^ {\prime} C D ^ {\prime} = C ^ {\prime} D + B (C ^ {\prime} D) + A ^ {\prime} C D ^ {\prime} \\ & = C ^ {\prime} D + A ^ {\prime} C D ^ {\prime} \end{array}
$$

$$
\begin{array}{r l} (3) Y & = ((A ^ {\prime} + B ^ {\prime}) D) ^ {\prime} + (A ^ {\prime} B ^ {\prime} + B D) C ^ {\prime} + A ^ {\prime} B C ^ {\prime} D + D ^ {\prime} \\ & = ((A B) ^ {\prime} D) ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} + B C ^ {\prime} D + A ^ {\prime} B C ^ {\prime} D + D ^ {\prime} \\ & = A B + D ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} + B C ^ {\prime} + A ^ {\prime} B C ^ {\prime} = A B + A ^ {\prime} C ^ {\prime} (B + B ^ {\prime}) + B C ^ {\prime} + D ^ {\prime} \\ & = A B + A ^ {\prime} C ^ {\prime} + B C ^ {\prime} + D ^ {\prime} \\ & = A B + A ^ {\prime} C ^ {\prime} + D ^ {\prime} \end{array}
$$

（4）首先将函数展开为与或形式并化简

$$
\begin{array}{r l} Y & = A B ^ {\prime} D + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + B ^ {\prime} C D + (A B ^ {\prime} + C) ^ {\prime} (B + D) \\ & = A B ^ {\prime} D + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + B ^ {\prime} C D + (A ^ {\prime} + B) C ^ {\prime} (B + D) \\ & = A B ^ {\prime} D + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + B ^ {\prime} C D + B C ^ {\prime} + A ^ {\prime} C ^ {\prime} D \\ & = A B ^ {\prime} D + B ^ {\prime} C D + B C ^ {\prime} + A ^ {\prime} C ^ {\prime} D \end{array}
$$

根据上式画出相应的卡诺图,如图 A2.17(a)。利用卡诺图进一步化简后得到

$$
Y = B C ^ {\prime} + B ^ {\prime} D
$$

(a)

图A2.17  
(b)

（5）画出函数的卡诺图。填写这个卡诺图时，只要在括号内各个最小项对应位置上填入0，在其余位置上填入1就行了。将括号内的逻辑式化为最小项之和形式得到

$$
\begin{array}{r l} Y (A, B, C, D, E) & = (A B ^ {\prime} C ^ {\prime} D + A C ^ {\prime} D E + B ^ {\prime} D E ^ {\prime} + A C ^ {\prime} D ^ {\prime} E) ^ {\prime} \\ & = (m _ {2} + m _ {6} + m _ {1 7} + m _ {1 8} + m _ {1 9} + m _ {2 2} + m _ {2 5} + m _ {2 7}) ^ {\prime} \end{array}
$$

将上式括号内最小项在卡诺图中的位置上填入0，而在卡诺图中其余最小项位置上填入1，就得到了图A2.17(b)的卡诺图。合并最小项后得出

$$
Y = A ^ {\prime} E + C E + B E ^ {\prime} + D ^ {\prime} E ^ {\prime}
$$

合并最小项时需注意,图中以双线为轴左右对称的最小项也是相邻的。

---

## Chunk 118/161：`ch02_ex2_18`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_18 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.18 |
| example_id | — |
| figure_ids | 图P2.18(a), 图P2.18(b), 图P2.18(c), 图P2.18(d) |
| prev_chunk_id | ch02_ex2_17 |
| next_chunk_id | ch02_ex2_19 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1486–1487 |

### 配图

**图P2.18(a)** — 图 P2.18 子图(a)

![图P2.18(a)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/f80d7847b637f2395ab27f1312ea230dd9414021882dad3700ff6af2ca77964c.jpg)

*视觉描述：* 两非门与三与非门电路：B、C经非门，A与B'、C进三输入与非，B与C'进二输入与非，末级与非输出Y=AB'C+BC'。

**图P2.18(b)** — 图 P2.18 子图(b)

![图P2.18(b)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/f3ee67c4cb4461ba8c0b34e0ce76f65225c80ffd684067cf44d6828e9bdbbdd5.jpg)

*视觉描述：* 三非门、三二输入或非门与一三输入或非门：A、B、C经循环或非产生中间项，末级三输入或非得Y=((A·C')+(A'·B)+(B'·C))'。

**图P2.18(c)** — 图 P2.18 子图(c)

![图P2.18(c)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/fa8ba3ccbc89fe626083571c5c3eccbff12f6cd71281d451f0ea82620db349cb.jpg)

*视觉描述：* 四输入双输出与非-与非电路：A~D经反相器后由五个中间与非门产生乘积项，两输出与非门分别得Y1、Y2，属典型与非门化简结构。

**图P2.18(d)** — 图 P2.18 子图(d)

![图P2.18(d)](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/6eb778dd1d02f09787ce4ceb8de0ed3d4d250f61f80ddcc3d0ba4880d09d5ad5.jpg)

*视觉描述：* 全加器逻辑电路：两异或门级联得和位Y2=A⊕B⊕C；A·B与(A⊕B)·C经与门、或非、非门得进位Y1=AB+(A⊕B)C。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.18 题干】
[题 2.18] 写出图 P2.18 中各逻辑图的逻辑函数式, 并化简为最简与或式。

【题2.18 解答】
【题 2.18】 写出图 P2.18 中各逻辑图的逻辑函数式, 并化简为最简与或式。

(a)

(b)

(c)

图P2.18  
(d)

解：

$$
\begin{array}{r l} & \text {(a)} Y = ((A B ^ {\prime} C) ^ {\prime} (B C ^ {\prime}) ^ {\prime}) ^ {\prime} = A B ^ {\prime} C + B C ^ {\prime} \\ & \text {(b)} Y = ((A ^ {\prime} + C) ^ {\prime} + (A + B ^ {\prime}) ^ {\prime} + (B + C ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & \qquad = (A ^ {\prime} + C) (A + B ^ {\prime}) (B + C ^ {\prime}) = A B C + A ^ {\prime} B ^ {\prime} C ^ {\prime} \\ & \text {(c)} Y _ {1} = ((A B ^ {\prime}) ^ {\prime} (A C D ^ {\prime}) ^ {\prime}) ^ {\prime} = A B ^ {\prime} + A C D ^ {\prime} \\ & \qquad Y _ {2} = ((A B ^ {\prime}) ^ {\prime} (A C ^ {\prime} D ^ {\prime}) ^ {\prime} (A ^ {\prime} C ^ {\prime} D) ^ {\prime} (A C D) ^ {\prime}) ^ {\prime} \\ & \qquad = A B ^ {\prime} + A C ^ {\prime} D ^ {\prime} + A ^ {\prime} C ^ {\prime} D + A C D \\ & \text {(d)} Y _ {1} = (((A B) + C (A \oplus B)) ^ {\prime}) ^ {\prime} = A B + C (A ^ {\prime} B + A B ^ {\prime}) = A B + A C + B C \\ & \qquad Y _ {2} = (A \oplus B) \oplus C = (A \oplus B) C ^ {\prime} + (A \oplus B) ^ {\prime} C \\ & \qquad = A B ^ {\prime} C ^ {\prime} + A ^ {\prime} B C ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A B C \end{array}
$$

[图P2.18(a)] 图 P2.18 子图(a)
[图P2.18(a)描述] 两非门与三与非门电路：B、C经非门，A与B'、C进三输入与非，B与C'进二输入与非，末级与非输出Y=AB'C+BC'。
[图P2.18(b)] 图 P2.18 子图(b)
[图P2.18(b)描述] 三非门、三二输入或非门与一三输入或非门：A、B、C经循环或非产生中间项，末级三输入或非得Y=((A·C')+(A'·B)+(B'·C))'。
[图P2.18(c)] 图 P2.18 子图(c)
[图P2.18(c)描述] 四输入双输出与非-与非电路：A~D经反相器后由五个中间与非门产生乘积项，两输出与非门分别得Y1、Y2，属典型与非门化简结构。
[图P2.18(d)] 图 P2.18 子图(d)
[图P2.18(d)描述] 全加器逻辑电路：两异或门级联得和位Y2=A⊕B⊕C；A·B与(A⊕B)·C经与门、或非、非门得进位Y1=AB+(A⊕B)C。

---

## Chunk 119/161：`ch02_ex2_19`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_19 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.19 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_18 |
| next_chunk_id | ch02_ex2_20 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1488–1489 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.19 题干】
[题 2.19] 对于互相排斥的一组变量 A、B、C、D、E、(即任何情况下，A、B、C、D、E 不可能有两个或两个以上同时为 1)，试证明 $AB^{\prime}C^{\prime}D^{\prime}E^{\prime}=A, A^{\prime}BC^{\prime}D^{\prime}E^{\prime}=B, A^{\prime}B^{\prime}CD^{\prime}E^{\prime}=C, A^{\prime}B^{\prime}C^{\prime}DE^{\prime}=D, A^{\prime}B^{\prime}C^{\prime}D^{\prime}E=E$ 。

【题2.19 解答】
【题 2.19】对于互相排斥的一组变量 A、B、C、D、E（即任何情况下 A、B、C、D、E 不可能有两个或两个以上同时为 1），试证明 $AB'C'D'E'=A, A'BC'D'E'=B, A'B'CD'E'=C, A'B'C'D'E=D, A'B'C'D'E=E$ 。

解：首先证明 $AB'C'D'E'=A$ 。

根据题意,任何时候不可能出现两个以上的变量同时等于1,所以凡是包含两个以上原变量因子的最小项均为约束项,取值始终为0。而且,任何包含两个以上原变量的乘积项也始为0。由此可知

$$
\begin{array}{r l} A B ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} & = A B ^ {\prime} C ^ {\prime} D ^ {\prime} E ^ {\prime} + A B ^ {\prime} C ^ {\prime} D ^ {\prime} E = A B ^ {\prime} C ^ {\prime} D ^ {\prime} (E ^ {\prime} + E) \\ & = A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D = A B ^ {\prime} C ^ {\prime} (D ^ {\prime} + D) \\ & = A B ^ {\prime} C ^ {\prime} + A B ^ {\prime} C = A B ^ {\prime} (C ^ {\prime} + C) \\ & = A B ^ {\prime} + A B = A (B ^ {\prime} + B) \\ & = A \end{array}
$$

同理可以证明 $A^{\prime}BC^{\prime}D^{\prime}E^{\prime}=B$ , $A^{\prime}B^{\prime}CD^{\prime}E^{\prime}=C$ , $A^{\prime}B^{\prime}C^{\prime}DE^{\prime}=D$ , $A^{\prime}B^{\prime}C^{\prime}D^{\prime}E=E$ 。

---

## Chunk 120/161：`ch02_ex2_20`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_20 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.20 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_19 |
| next_chunk_id | ch02_ex2_21 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1490–1518 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.20 题干】
[题 2.20] 将下列具有约束项的逻辑函数化为最简与或形式。

(1) $Y_{1} = AB'C' + ABC + A'B'C + A'BC'$

给定约束条件为 $A'B'C'+A'BC=0$

(2) $Y_{2}=(A+C+D)^{\prime}+A^{\prime}B^{\prime}CD^{\prime}+AB^{\prime}C^{\prime}D$ ，给定约束条件为 $AB^{\prime}CD^{\prime}+AB^{\prime}CD+ABC^{\prime}D^{\prime}+ABC^{\prime}D+ABCD^{\prime}+ABCD=0$ 。

(3) $Y_{3}=CD'(A\oplus B)+A'BC'+A'C'D$ ，给定约束条件为 $AB+CD=0$ 。

(4) $Y_{4}=(AB'+B)CD'+((A+B)(B'+C))'$ ，给定约束条件为

(a)

(b)


(c)  
(d)  
图 P2.18

$$
A B C + A B D + A C D + B C D = 0
$$

【题2.20 解答】
【题 2.20】 将下列具有约束项的逻辑函数化为最简与或形式。

(1) $Y_{1} = AB'C' + ABC + A'B'C + A'BC'$

给定约束条件为 $A^{\prime}B^{\prime}C^{\prime}+A^{\prime}BC=0$ 。

(2) $Y_{2}=(A+C+D)'+A'B'CD'+AB'C'D$ ，给定约束条件为 $AB'CD'+AB'CD+ABC'D'+ABC'D+ABCD'+ABCD=0$ 。

(3) $Y_{3}=CD'(A\oplus B)+A'BC'+A'C'D$ ，给定约束条件为 $AB+CD=0$ 。

(4) $Y_{4}=(AB'+B)CD'+((A+B)(B'+C))'$ ，给定约束条件为 $ABC+ABD+ACD+BCD=0$ 。

解：先将函数式化为最小项之和形式，然后画出每个函数的卡诺图，利用卡诺图化简。

(1) $Y_{1}(A,B,C) = \sum m(1,2,4,7) + d(0,3)$

画出 $Y_{1}$ 的卡诺图, 如图 A2.20(a)。化简后得到

$$
Y _ {1} = A ^ {\prime} + B ^ {\prime} C ^ {\prime} + B C
$$

(2) $Y_{2}(A,B,C,D) = \sum m(0,2,4,9) + d(10,11,12,13,14,15)$

画出 $Y_{2}$ 的卡诺图, 如图 A2.20(b)。化简后得到

$$
Y _ {2} = A ^ {\prime} B ^ {\prime} D ^ {\prime} + A ^ {\prime} C ^ {\prime} D ^ {\prime} + A D
$$

(3) $Y_{3}(A,B,C,D) = \sum m(1,4,5,6,10) + d(3,7,11,12,13,14,15)$

(b)  
(a)


(c)

(d)  
图A2.20

画出 $Y_{3}$ 的卡诺图, 如图 A2.20(c)。化简后得到

$$
Y _ {3} = B + A ^ {\prime} D + A C
$$

(4) $Y_{4}(A,B,C,D) = \sum m(0,1,2,3,4,5,6,10,12) + d(7,11,13,14,15)$

画出 $Y_{4}$ 的卡诺图, 如图 A2.20(d)。化简后得到

$$
Y _ {4} = A ^ {\prime} + B + C
$$

---

## Chunk 121/161：`ch02_ex2_21`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_21 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.21 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_20 |
| next_chunk_id | ch02_ex2_22 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1519–1528 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.21 题干】
[题 2.21] 将下列具有无关项的逻辑函数化为最简的与或逻辑式。

(1) $Y_{1}(A,B,C)=\sum m(0,1,2,4)+d(5,6)$

(2) $Y_{2}(A,B,C)=\sum m(1,2,4,7)+d(3,6)$

(3) $Y_{3}(A,B,C,D) = \sum m(3,5,6,7,10) + d(0,1,2,4,8)$

(4) $Y_{4}(A,B,C,D)=\sum m(2,3,7,8,11,14)+d(0,5,10,15)$

【题2.21 解答】
【题 2.21】将下列具有无关项的逻辑函数化为最简的与或逻辑式。

(1) $Y_{1}(A,B,C) = \sum m(0,1,2,4) + d(5,6)$

(2) $Y_{2}(A,B,C) = \sum m(1,2,4,7) + d(3,6)$

(3) $Y_{3}(A,B,C,D) = \sum m(3,5,6,7,10) + d(0,1,2,4,8)$

(4) $Y_{4}(A,B,C,D) = \sum m(2,3,7,8,11,14) + d(0,5,10,15)$

解：画出 $Y_{1}, Y_{2}, Y_{3}, Y_{4}$ 的卡诺图分别为图A2.21(a)、(b)、(c)、(d)。化简后得到

$$
\begin{array}{r l} & Y _ {1} = B ^ {\prime} + C ^ {\prime} \\ & Y _ {2} = B + A ^ {\prime} C + A C ^ {\prime} \\ & Y _ {3} = A ^ {\prime} + B ^ {\prime} D ^ {\prime} \\ & Y _ {4} = A C + C D + B ^ {\prime} D ^ {\prime} \end{array}
$$

---

## Chunk 122/161：`ch02_ex2_22`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_22 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.22 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_21 |
| next_chunk_id | ch02_ex2_23 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1529–1530 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.22 题干】
[题 2.22] 试证明两个逻辑函数间的与、或、异或运算可以通过将它们的卡诺图中对应的最小项做与、或、异或运算来实现，如图 P2.22 所示。

【题2.22 解答】
【题 2.22】试证明两个逻辑函数间的与、或、异或运算可以通过将它们的卡诺图中对应的最小项作与、或、异或运算来实现，如图 P2.22 所示。

(a)


(c)

(b)  
(d)  
图 A2.21

解：设两个逻辑函数分别为 $Y_{1} = \sum m_{i1}, Y_{2} = \sum m_{i2}$ 。

(1) 证明 $Y_{1} \cdot Y_{2} = \sum m_{i1} \cdot m_{i2}$

因为任何两个不同的最小项之积均为0，而两个相同的最小项之积仍等于这个最小项，所以 $Y_{1}$ 和 $Y_{2}$ 的乘积中仅为它们的共同的最小项之和，即

$$
Y _ {1} \cdot Y _ {2} = \sum m _ {i 1} \cdot \sum m _ {i 2} = \sum m _ {i 1} \cdot m _ {i 2}
$$

因此，可以通过将 $Y_{1}$ 、 $Y_{2}$ 卡诺图上对应的最小项相乘，得到 $Y_{1} \cdot Y_{2}$ 卡诺图上对应的最小项。

(2) 证明 $Y_{1} + Y_{2} = \sum m_{i1} + \sum m_{i2}$

因为 $Y_{1}+Y_{2}$ 等于 $Y_{1}$ 和 $Y_{2}$ 的所有最小项之和，所以将 $Y_{1}$ 和 $Y_{2}$ 卡诺图中对应的最小项相加，就得到 $Y_{1}+Y_{2}$ 卡诺图中对应的最小项了。

(3) 证明 $Y_{1} \oplus Y_{2} = \sum m_{i1} \oplus m_{i2}$

已知 $Y_{1} \oplus Y_{2} = (Y_{1} \odot Y_{2})' = (Y_{1}Y_{2} + Y_{1}'Y_{2}')'$

根据上面已证明的与运算方法知， $Y_{1}Y_{2}$ 等于两个卡诺图中同为1的最小项之和， $Y_{1}^{\prime}Y_{2}^{\prime}$ 等于 $Y_{1},Y_{2}$ 卡诺图中同为0的最小项之和。因此， $Y_{1}\odot Y_{2}$ 等于 $Y_{1},Y_{2}$ 卡诺图中同为1和同为0的最小项之和。

由于 $Y_{1} \oplus Y_{2} = (Y_{1} \odot Y_{2})'$ ，所以 $Y_{1} \oplus Y_{2}$ 应等于 $Y_{1}, Y_{2}$ 卡诺图中取值不同的那些最小项之和。因此，可以通过 $Y_{1}, Y_{2}$ 卡诺图中对应最小项的异或运算求出 $Y_{1} \oplus Y_{2}$ 卡诺图中对应的最小项。

---

## Chunk 123/161：`ch02_ex2_23`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_23 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.23 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_22 |
| next_chunk_id | ch02_ex2_24 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1531–1546 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.23 题干】
[题 2.23] 利用卡诺图之间的运算(参见上题)将下列逻辑函数化为最简与或式。

(1) $Y = (AB + A'C + B'D)(AB'C'D + A'CD + BCD + B'C)$

$$
Y = (A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B C ^ {\prime} + A C) (A B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C + C D)
$$

$$
Y = (A ^ {\prime} D ^ {\prime} + C ^ {\prime} D + C D ^ {\prime}) \oplus (A C ^ {\prime} D ^ {\prime} + A B C + A ^ {\prime} D + C D)
$$

$$
Y = (A ^ {\prime} C ^ {\prime} D ^ {\prime} + B ^ {\prime} D ^ {\prime} + B D) \oplus (A ^ {\prime} B D ^ {\prime} + B ^ {\prime} D + B C D ^ {\prime}) \tag {4}
$$

【题2.23 解答】
【题 2.23】利用卡诺图之间的运算(参见上题)将下列逻辑函数化为最简与或式。

(1) $Y = (AB + A'C + B'D)(AB'C'D + A'CD + BCD + B'C)$

$$
Y = \left(A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B C ^ {\prime} + A C\right) \left(A B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C + C D\right) \tag {2}
$$

$$
Y = (A ^ {\prime} D ^ {\prime} + C ^ {\prime} D + C D ^ {\prime}) \oplus (A C ^ {\prime} D ^ {\prime} + A B C + A ^ {\prime} D + C D) \tag {3}
$$

图P2.22

(4) $Y = (A'C'D' + B'D' + BD) \oplus (A'BD' + B'D + BCD')$

解：

（1）令 $Y_{1}=AB+A'C+B'D, Y_{2}=AB'C'D+A'CD+BCD+B'C$ 则 $Y=Y_{1} \cdot Y_{2}=AB'D + A'B'C + CD$ [见图 A2.23(a)]

(2) 令 $Y_{1} = A'B'C + A'BC' + AC, Y_{2} = AB'C'D + A'BC + CD$ 则 $Y_{1} \cdot Y_{2} = ACD + B'CD[$ 见图A2.23(b)]

（3）令 $Y_{1}=A'D'+C'D+CD', Y_{2}=AC'D'+ABC+A'D+CD$ 则 $Y_{1}\oplus Y_{2}=AB'+A'C+AD+C'D'$ [见图 A2.23(c)]

(此题化简结果不是唯一的。)






图A2.23

(4) 令 $Y_{1}=A^{\prime}C^{\prime}D^{\prime}+B^{\prime}D^{\prime}+BD$ , $Y_{2}=A^{\prime}BD^{\prime}+B^{\prime}D+BCD^{\prime}$ ,

则 $Y_{1} \oplus Y_{2} = (BC'D')' = B' + C + D[$ 见图A2.23(d)]

---

## Chunk 124/161：`ch02_ex2_24`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_24 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.24 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_23 |
| next_chunk_id | ch02_ex2_25 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1547–1556 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.24 题干】
[题 2.24] 化简下列一组多输出逻辑函数。要求尽可能利用共用项，将这一组逻辑函数从总体上化为最简，并将化简结果与 $Y_{1}, Y_{2}$ 各自独立化简的结果进行比较。

$$
Y _ {1} (A, B, C, D) = \sum m (0, 1, 8, 9, 1 0, 1 2, 1 3, 1 4)
$$

$$
Y _ {2} (A, B, C, D) = \sum m (0, 1, 2, 3, 6, 7, 1 0, 1 4)
$$

【题2.24 解答】
【题 2.24】化简下列一组多输出逻辑函数。要求尽可能利用共用项，将这一组逻辑函数从总体上化为最简，并将化简结果与 $Y_{1}$ 、 $Y_{2}$ 各自独立化简的结果进行比较。

$$
Y _ {1} (A, B, C, D) = \sum m (0, 1, 8, 9, 1 0, 1 2, 1 3, 1 4)
$$

$$
Y _ {2} (A, B, C, D) = \sum m (0, 1, 2, 3, 6, 7, 1 0, 1 4)
$$

解：

（1）若将 $Y_{1}$ 、 $Y_{2}$ 分别进行化简，则可以画出图 A2.24(a) 的卡诺图，合并最小项后得到


(a)


(b)

(c)

(d)  
图A2.24

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = A C ^ {\prime} + B ^ {\prime} C ^ {\prime} + A D ^ {\prime} \\ Y _ {2} (A, B, C, D) = A ^ {\prime} B ^ {\prime} + C D ^ {\prime} + A ^ {\prime} C \end{array}
$$

根据上式得到的逻辑图如图 A2.24(c) 所示。实现这一组逻辑函数需要用 8 个门和 18 个输入端。

（2）若利用共用项将 $Y_{1}, Y_{2}$ 整体化简，则可以按图A2.24(b)所示合并最小项，得到

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = A C ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} + A C D ^ {\prime} \\ Y _ {2} (A, B, C, D) = A ^ {\prime} C + A ^ {\prime} B ^ {\prime} C ^ {\prime} + A C D ^ {\prime} \end{array}
$$

根据上式得到的逻辑图如图 A2.24(d) 所示。实现这一组逻辑函数只需要 6 个门和 16 个输入端。

---

## Chunk 125/161：`ch02_ex2_25`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_25 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.25 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_24 |
| next_chunk_id | ch02_ex2_26 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1557–1587 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.25 题干】
[题 2.25] 化简下列一组多输出逻辑函数。要求尽可能利用共用项，将这一组逻辑函数从总体上化为最简，并将化简结果与 $Y_{1}$ 、 $Y_{2}$ 和 $Y_{3}$ 各自独立化简的结果进行比较。

$$
Y _ {1} (A, B, C, D) = \sum m (0, 8, 9, 1 0, 1 1, 1 4, 1 5)
$$

$$
Y _ {2} (A, B, C, D) = \sum m (0, 2, 3, 6, 7, 1 0, 1 1, 1 2, 1 3, 1 5)
$$








图P2.22


$Y_{3}(A,B,C,D) = \sum m(0,1,3,5,7,10,11,12,13,14,15)$

【题2.25 解答】
【题 2.25】化简下列一组多输出逻辑函数。要求尽可能利用共用项，将这一组逻辑函数从总体上化为最简，并将化简结果与 $Y_{1}$ 、 $Y_{2}$ 和 $Y_{3}$ 各自独立化简的结果进行比较。

$$
\begin{array}{r l} & Y _ {1} (A, B, C, D) = \sum m (0, 8, 9, 1 0, 1 1, 1 4, 1 5) \\ & Y _ {2} (A, B, C, D) = \sum m (0, 2, 3, 6, 7, 1 0, 1 1, 1 2, 1 3, 1 5) \\ & Y _ {3} (A, B, C, D) = \sum m (0, 1, 3, 5, 7, 1 0, 1 1, 1 2, 1 3, 1 4, 1 5) \end{array}
$$

解：

（1）若将 $Y_{1}$ 、 $Y_{2}$ 、 $Y_{3}$ 分别进行化简，则可以画出图 A2.25(a) 的卡诺图，合并最小项后得到

$$
\begin{array}{r l} & Y _ {1} (A, B, C, D) = A B ^ {\prime} + B ^ {\prime} C ^ {\prime} D ^ {\prime} + A C \\ & Y _ {2} (A, B, C, D) = A ^ {\prime} B ^ {\prime} D ^ {\prime} + A B C ^ {\prime} + C D + B ^ {\prime} C + A ^ {\prime} C \\ & Y _ {3} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A ^ {\prime} D + A B + A C \end{array}
$$

根据上式得到的逻辑图如图 A2.25(c) 所示。实现这一组逻辑函数需要 15 个门和 40 个输入端。

(2) 若利用共用项将 $Y_{1}$ 、 $Y_{2}$ 整体化简，则可以按图 A2.25(b) 所示合并最小项，得到

$$
\begin{array}{r l} & Y _ {1} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} + A C \\ & Y _ {2} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B C ^ {\prime} + C D + B ^ {\prime} C + A ^ {\prime} C \\ & Y _ {3} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A ^ {\prime} D + A B C ^ {\prime} + A C \end{array}
$$

根据上式得到的逻辑图如图 A2.25(d) 所示。实现这一组逻辑函数只需要 11 个门和 31 个输入端。

---

## Chunk 126/161：`ch02_ex2_26`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_26 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.26 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_25 |
| next_chunk_id | ch02_ex2_27 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1588–1593 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.26 题干】
[题 2.26] 将下列逻辑函数式化为与非-与非形式，并画出全部由与非逻辑单元组成的逻辑电路图。

(1) $Y = AB + BC + AC$ (2) $Y = (A' + B)(A + B')C + (BC)'$

(3) $Y = (ABC' + AB'C + A'BC)'$ (4) $Y = A(BC)' + ((AB')' + A'B' + BC)'$

【题2.26 解答】
【题 2.26】将下列逻辑函数式化为与非-与非形式,并画出全部由与非逻辑单元组成的逻辑电路图。

(1) $Y = AB + BC + AC$

(2) $Y = (A' + B)(A + B')C + (BC)'$

(3) $Y = (ABC' + AB'C + A'BC)'$

(4) $Y = A(BC)' + ((AB')' + A'B' + BC)'$

解：

$$
Y = \left(\left(A B + B C + A C\right) ^ {\prime}\right) ^ {\prime} = \left(\left(A B\right) ^ {\prime} \cdot (B C) ^ {\prime} \cdot (A C) ^ {\prime}\right) ^ {\prime} \tag {1}
$$

$$
\begin{array}{r l} (2) Y & = (A ^ {\prime} + B) (A + B ^ {\prime}) C + (B C) ^ {\prime} \\ & = (A B + A ^ {\prime} B ^ {\prime}) C + B ^ {\prime} + C ^ {\prime} \\ & = A + B ^ {\prime} + C ^ {\prime} = (A ^ {\prime} B C) ^ {\prime} \end{array}
$$

(a)

(b)



(c)

图A2.25  
(d)

$$
\begin{array}{r l} (3) Y & = (A B C ^ {\prime} + A B ^ {\prime} C + A ^ {\prime} B C) ^ {\prime} \\ & = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A ^ {\prime} B C ^ {\prime} + A B ^ {\prime} C ^ {\prime} + A B C \\ & = A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime} + B ^ {\prime} C ^ {\prime} + A B C \\ & = ((A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime} + B ^ {\prime} C ^ {\prime} + A B C) ^ {\prime}) ^ {\prime} \\ & = ((A ^ {\prime} B ^ {\prime}) ^ {\prime} \cdot (A ^ {\prime} C ^ {\prime}) ^ {\prime} \cdot (B ^ {\prime} C ^ {\prime}) ^ {\prime} \cdot (A B C) ^ {\prime}) ^ {\prime} \end{array}
$$

$$
\begin{array}{r l} (4) Y & = A (B C) ^ {\prime} + ((A B ^ {\prime}) ^ {\prime} + A ^ {\prime} B ^ {\prime} + B C) ^ {\prime} \\ & = A (B C) ^ {\prime} + A B ^ {\prime} \cdot (A ^ {\prime} B ^ {\prime}) ^ {\prime} \cdot (B C) ^ {\prime} \\ & = A (B C) ^ {\prime} = ((A \cdot (B C) ^ {\prime}) ^ {\prime}) ^ {\prime} \end{array}
$$

(1)、(2)、(3)、(4)各式对应的电路图如图 A2.26(a)、(b)、(c)、(d)。

(a)

(b)

(c)

(d)  
图 A2.26

---

## Chunk 127/161：`ch02_ex2_27`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_ex2_27 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第02章 逻辑代数基础 > exercises 章末习题 |
| section_id | ch02_sec_exercises |
| exercise_id | 题2.27 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_26 |
| next_chunk_id | ch02_root_theory_1 |
| source_file | 按章节拆分\04_第02章_逻辑代数基础.md |
| line_range | L1594–1602 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > exercises 章末习题

【题2.27 题干】
[题 2.27] 将下列逻辑函数化为或非-或非形式，并画出全部用或非逻辑单元组成的逻辑电路图。

(1) $Y = AB'C + BC'$

(2) $Y = (A + C)(A' + B + C') (A' + B' + C)$

(3) $Y = (ABC' + B'C)'D' + A'B'D$

(4) $Y = ((CD')'(BC)'(ABC)'D')'$

【题2.27 解答】
【题 2.27】将下列逻辑函数化为或非-或非形式,并画出全部用或非逻辑单元组成的逻辑电路图。

(1) $Y = AB'C + BC'$

(2) $Y = (A + C)(A' + B + C') (A' + B' + C)$

(3) $Y = (ABC' + B'C)'D' + A'B'D$

(4) $Y = ((CD')'(BC)'(ABC)'D')'$

解：

$$
\begin{array}{r l} Y & = A B ^ {\prime} C + B C ^ {\prime} \\ & = ((A B ^ {\prime} C) ^ {\prime} \cdot (B C ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & = ((A ^ {\prime} + B + C ^ {\prime}) (B ^ {\prime} + C)) ^ {\prime} \\ & = (A ^ {\prime} B ^ {\prime} + A ^ {\prime} C + B C + B ^ {\prime} C ^ {\prime}) ^ {\prime} \\ & = (A ^ {\prime} B ^ {\prime} + B C + B ^ {\prime} C ^ {\prime}) ^ {\prime} \end{array} \tag {1}
$$

---

## Chunk 128/161：`ch02_root_theory_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_root_theory_1 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 |
| section_id | ch02_root |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_ex2_27 |
| next_chunk_id | ch02_sec_2_1_theory_15 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L1–9 |

### 正文（检索用 text_content）

第02章 逻辑代数基础

将上面的两个补码相加后得到
110101
+ 110110
101011

和的符号位为1，表示和为负。

如果将和的补码再求补码,就得到和的原码为 $110101(-21)_{10}$ 。

---

## Chunk 129/161：`ch02_sec_2_1_theory_15`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_1_theory_15 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.1 本章重点内容 |
| section_id | ch02_sec_2_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_root_theory_1 |
| next_chunk_id | ch02_sec_2_2_theory_27_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L15–25 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.1 本章重点内容

一、逻辑代数的基本公式、常用公式和定理。

二、逻辑函数的描述方法(真值表、逻辑式、逻辑图、波形图、卡诺图)及相互转换的方法。

三、最小项的定义及其性质，逻辑函数的最小项之和表示法。

四、逻辑函数的化简方法（公式化简法和卡诺图化简法）。

五、无关项在化简逻辑函数中的应用。

---

## Chunk 130/161：`ch02_sec_2_2_theory_27_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_1_theory_15 |
| next_chunk_id | ch02_sec_2_2_theory_27_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

什么是约束项、任意项和无关项？

首先需要强调说明的是约束项和任意项是两个不同的概念。然而，在有些教材和书籍中没有将这两个概念明确地加以区分。

我们在分析一个逻辑函数时经常会遇到这样一类情况,就是输入逻辑变量的某些取值始终不会出现。因此,在这些取值下等于1的那些最小项,也将始终为0。这些取值始终为0的最小项,就叫做该函数的约束项。

在《数字电子技术基础(第六版)》第2.7节中,我们是通过图2-2-1的实例来说明约束项的概念的。该例要求设计一个逻辑电路,用水箱中水位高度的检测信号A、B、C控制两个水泵 $M_{L}$ 和 $M_{S}$ 的启、停工作状态(见图2-2-1)。如果用 $Y_{L}$ 和 $Y_{S}$ 分别表示两个水泵的工作状态,则 $Y_{L}$ 和 $Y_{S}$ 为A、B、C三个变量的逻辑函数。假定水位高于A、B、C中的任何一个检测点时给出的检测信号为1,水位低于任何一个检测点时给出的检测信号为0,则水箱工作过程中ABC的取值只可能出现100、110、111和000这四种状态,而不可能出现001、011、101和010这四种状态,因为水位永远不会高于B或C而同时又低于A。因此,与ABC的取值001、011、101和010对应的四个最小项 $A'B'C$ 、 $A'BC$ 、 $AB'C$ 和 $A'BC'$ 将永远是0,这四个最小项就是 $Y_{L}$ 和 $Y_{S}$ 的约束项。

既然在逻辑函数的工作过程中约束项的值永远是0，那么我们就可以在 $Y_{L}$ 和 $Y_{S}$ 的逻辑函数式中加上这些约束项，也可以不加上这些约束项，而不影响 $Y_{L}$ 和 $Y_{S}$ 的取值。也就是说 $Y_{L}$ 和 $Y_{S}$ 的取值与是否加上了约束项没有关系，因此约束项又是逻辑函数式中的无关项。

在分析和设计逻辑电路时,还可能遇到另外一种情况,就是在输入变量的某些取值下,无论逻辑函数值等于1还是0,对电路的逻辑功能都没有影响。在这些变量取值下等于1的那些最小项,就叫做这个逻辑函数的任意项。

图2-2-1 用于说明约束项概念的实例

例如,设计一个拒绝伪码的七段显示译码器,其真值表如表2-2-1。所谓拒绝伪码,系指在输入为1010\~1111时输出无任何字形显示,即 $a\sim g$ 输出全都等于0。

表 2-2-1 七段显示译码器的真值表

---

## Chunk 131/161：`ch02_sec_2_2_theory_27_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p00 |
| next_chunk_id | ch02_sec_2_2_theory_27_p02 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

<table><tr><td colspan="5">输入</td><td colspan="7">输出</td></tr><tr><td>数字</td><td>D</td><td>C</td><td>B</td><td>A</td><td>a</td><td>b</td><td>c</td><td>d</td><td>e</td><td>f</td><td>g</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>3</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>4</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>5</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>6</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>7</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><

---

## Chunk 132/161：`ch02_sec_2_2_theory_27_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p01 |
| next_chunk_id | ch02_sec_2_2_theory_27_p03 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

td>0</td><td>0</td></tr><tr><td>8</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>9</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>10</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>11</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>12</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>13</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>14</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>15</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

---

## Chunk 133/161：`ch02_sec_2_2_theory_27_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p03 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p02 |
| next_chunk_id | ch02_sec_2_2_theory_27_p04 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

由表2-2-1可以看出，这个译码器是一个有4个输入变量和7个输出函数的组合逻辑电路。如果我们采用图2-2-2的电路结构，在 $a\sim g$ 的输出端增加一级缓冲器，同时还在缓冲器的输入增加一个控制信号 $Y = (DC + DB)^{\prime}$ ，那么当 $DCBA = 1010\sim 1111$ 时，不论 $a\sim g$ 是1还是0， $a_{0}\sim g_{0}$ 肯定等于0，所以 $a_0\sim g_0$ 仍然符合表2-2-1的要求。

图2-2-2 拒绝伪码的七段显示译码器

这就是说，当 DCBA 取值为 1010～1111 时， $a \sim g$ 每个函数输出的取值是 1 是 0 都可以，不影响最后的输出 $a_{0} \sim g_{0}$ 。因此，在 DCBA 取值为 1010～1111 时，其值为 1 的六个最小项 $DC^{\prime}BA^{\prime}$ 、 $DC^{\prime}BA$ 、 $DCB^{\prime}A^{\prime}$ 、 $DCB^{\prime}A$ 、 $DCBA^{\prime}$ 和 DCBA 是函数 $a \sim g$ 的任意项。在化简 $a \sim g$ 的逻辑函数式时，既可以在式中写入这些任意项，也可以不写进这些任意项，所以任意项也是逻辑函数式中的无关项。这样我们就可以把表 2-2-1 改写为表 2-2-2 的形式了。表中的 × 仍然表示无关项。

虽然任意项和约束项都是逻辑函数式中的无关项,但二者是有区别的。因为约束项的取值永远是0,所以在逻辑函数式中无论写入约束项还是去掉约束项,都不会改变函数的输出值。而任意项则不同,当我们在逻辑函数式中写入某个任意项之后,则输入变量的取值使这个任意项的值为1时,函数的输出值也为1;如果从逻辑函数式中将这个任意项拿掉,则输入变量取值使这个任意项的值为1时,函数的输出值等于0。

表 2-2-2 修改后的表 2-2-1

---

## Chunk 134/161：`ch02_sec_2_2_theory_27_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p04 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p03 |
| next_chunk_id | ch02_sec_2_2_theory_27_p05 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

<table><tr><td colspan="5">输入</td><td colspan="7">输出</td></tr><tr><td>数字</td><td>D</td><td>C</td><td>B</td><td>A</td><td>a</td><td>b</td><td>c</td><td>d</td><td>e</td><td>f</td><td>g</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>3</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>4</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>5</td><td>0</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>6</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>7</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><

---

## Chunk 135/161：`ch02_sec_2_2_theory_27_p05`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p05 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p04 |
| next_chunk_id | ch02_sec_2_2_theory_27_p06 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

td>0</td><td>0</td></tr><tr><td>8</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>9</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr><tr><td>10</td><td>1</td><td>0</td><td>1</td><td>0</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>11</td><td>1</td><td>0</td><td>1</td><td>1</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>12</td><td>1</td><td>1</td><td>0</td><td>0</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>13</td><td>1</td><td>1</td><td>0</td><td>1</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>14</td><td>1</td><td>1</td><td>1</td><td>0</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>15</td><td>1</td><td>1</td><td>1</td><td>1</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr></table>

---

## Chunk 136/161：`ch02_sec_2_2_theory_27_p06`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p06 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p05 |
| next_chunk_id | ch02_sec_2_2_theory_27_p07 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

在化简逻辑函数的过程中,合理地使用这些无关项通常都可以得到更简单的化简结果。图 2-2-3(a) 是根据没有无关项的表 2-2-1 画出的卡诺图。利用这一组卡诺图得到的化简结果为

$$
\left\{ \begin{array}{l} a = D ^ {\prime} C ^ {\prime} A ^ {\prime} + D ^ {\prime} C A + D ^ {\prime} B A + D C ^ {\prime} B ^ {\prime} \\ b = D ^ {\prime} B ^ {\prime} A ^ {\prime} + D ^ {\prime} B A + D ^ {\prime} C ^ {\prime} + C ^ {\prime} B ^ {\prime} \\ c = D ^ {\prime} C + D ^ {\prime} A + C ^ {\prime} B ^ {\prime} \\ d = D ^ {\prime} C B ^ {\prime} A + C ^ {\prime} B ^ {\prime} A ^ {\prime} + D ^ {\prime} C ^ {\prime} B + D ^ {\prime} B A ^ {\prime} \\ e = D ^ {\prime} C ^ {\prime} A ^ {\prime} + D ^ {\prime} B A ^ {\prime} + C ^ {\prime} B ^ {\prime} A ^ {\prime} \\ f = D ^ {\prime} C B ^ {\prime} + D ^ {\prime} C A ^ {\prime} + D C ^ {\prime} B ^ {\prime} + C ^ {\prime} B ^ {\prime} A ^ {\prime} \\ g = D ^ {\prime} C B ^ {\prime} + D C ^ {\prime} B ^ {\prime} + D ^ {\prime} C ^ {\prime} B + D ^ {\prime} B A ^ {\prime} \end{array} \right.\tag{2-2-1}
$$

如果考虑了无关项的存在,则根据表2-2-2画出的卡诺图如图2-2-3(b)所示。利用这一组卡诺图化简得到的结果为

---

## Chunk 137/161：`ch02_sec_2_2_theory_27_p07`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_2_theory_27_p07 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑 |
| section_id | ch02_sec_2_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p06 |
| next_chunk_id | ch02_sec_2_3_theory_84 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L27–82 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.2 难点释疑

$$
\left\{ \begin{array}{l} a = D + C ^ {\prime} A ^ {\prime} + C A + B A \\ b = C ^ {\prime} + B A + B ^ {\prime} A ^ {\prime} \\ c = C + A + B ^ {\prime} \\ d = C B ^ {\prime} A + C ^ {\prime} A ^ {\prime} + C ^ {\prime} B + B A ^ {\prime} \\ e = C ^ {\prime} A ^ {\prime} + B A ^ {\prime} \\ f = D + C A ^ {\prime} + C B ^ {\prime} + B ^ {\prime} A ^ {\prime} \\ g = D + C B ^ {\prime} + C ^ {\prime} B + C A ^ {\prime} \end{array} \right.\tag{2-2-2}
$$

很显然,式(2-2-2)比式(2-2-1)简单得多。按照式(2-2-2)接成的逻辑电路也比按照式(2-2-1)接成的逻辑电路简单。

(a)

(b)  
图2-2-3

---

## Chunk 138/161：`ch02_sec_2_3_theory_84`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_3_theory_84 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2.3 习题类型与解题方法 |
| section_id | ch02_sec_2_3 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_2_theory_27_p07 |
| next_chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L84–86 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2.3 习题类型与解题方法

这一章的习题从内容上可以分为四种类型:逻辑等式的证明、逻辑函数不同描述方法之间的转换、逻辑函数形式的变换和逻辑函数的化简。下面分别总结、归纳一下这几种类型习题的解题方法并给出相应的例解。

---

## Chunk 139/161：`ch02_sec_一_逻辑等式的证明_theory_88_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 一、逻辑等式的证明 |
| section_id | ch02_sec_一_逻辑等式的证明 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_3_theory_84 |
| next_chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L88–137 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 一、逻辑等式的证明

解题方法和步骤：

方法一,分别列出等式两边逻辑式的真值表,若真值表完全相同,则等式成立。

方法二,若能利用逻辑代数的公式和定理将等式两边化为完全相同的形式,则等式成立。

方法三,分别画出等式两边逻辑式的卡诺图,若卡诺图相同,则等式成立。

【例2-3-1】试用列真值表的方法证明下面的等式

$$
A \oplus B ^ {\prime} = A ^ {\prime} \oplus B
$$

解：分别列出 $A \oplus B'$ 和 $A' \oplus B$ 的真值表，如表2-3-1。可见， $A \oplus B'$ 与 $A' \oplus B$ 的真值表完全相同，故等式成立。

表 2-3-1 例 2-3-1 的真值表

<table><tr><td>A</td><td>B</td><td> $A'$ </td><td> $B'$ </td><td> $A \oplus B'$ </td><td> $A' \oplus B$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr></table>

【例2-3-2】试用公式变换的方法证明下面的等式

$$
(A \oplus B) + A = (A \oplus B) + B
$$

解：左式 $(A\oplus B)+A=AB'+A'B+A$ $=A'B+A$ （根据 $A+AB=A$ ） $=A+B$ （根据 $A+A'B=A+B$ ）

右式

$$
\begin{array}{r l r} {( A \oplus B) + B = A B ^ {\prime} + A ^ {\prime} B + B} \\ & {= A B ^ {\prime} + B} & {\quad (\text {根据} A + A B = A)} \\ & {= A + B} & {\quad (\text {根据} A + A ^ {\prime} B = A + B)} \end{array}
$$

故等式成立。

【例2-3-3】试用卡诺图证明下面的等式

---

## Chunk 140/161：`ch02_sec_一_逻辑等式的证明_theory_88_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 一、逻辑等式的证明 |
| section_id | ch02_sec_一_逻辑等式的证明 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p00 |
| next_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L88–137 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 一、逻辑等式的证明

$$
A B ^ {\prime} + A ^ {\prime} C + B C ^ {\prime} = A C ^ {\prime} + B ^ {\prime} C + A ^ {\prime} B
$$

解：画出等式两边对应的卡诺图，均得到图2-3-1的结果，故等式成立。

从以上的三个例子还可以看出，列真值表的方法一般适合于证明变量数较少（例如不多于四个）、逻辑式也比较简单的等式。变量数较多、函数式又比较复杂的情况下，一般适于使用公式变换的方法去证明。画卡诺图证明的方法通常用在变量数较少（不多于四个），而且逻辑式是与或形式的情况。

图2-3-1 例2-3-3的卡诺图

---

## Chunk 141/161：`ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换 |
| section_id | ch02_sec_二_逻辑函数不同描述方法之间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_一_逻辑等式的证明_theory_88_p01 |
| next_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L139–163 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换

用于描述逻辑函数的方法有逻辑真值表(简称真值表)、逻辑函数式(简称逻辑式)、逻辑图、卡诺图、波形图和硬件描述语言(简称HDL)等几种。由于每一种描述方法各有其特点和应用场合,所以经常要求将用某一种描述方法给定的逻辑函数改用另外的描述方法来描述。尽管目前已经有计算机软件能自动完成这些转换,但为了理解和掌握这些转换方法的基本原理,通过手工的方法去解这一类题目仍然是必不可少的。

## 1. 真值表 $\Rightarrow$ 逻辑式

解题方法和步骤：

（1）首先从真值表中找出所有使函数值等于1的那些输入变量取值组合。

（2）每一组使输出为 1 的输入变量取值下，必然有一个最小项的值等于 1。取值为 1 的变量在这个最小项中写为原变量，取值为 0 的变量在这个最小项中写为反变量。

（3）将所有的这些最小项相加，就得到了所求的逻辑函数式。

【例2-3-4】给出逻辑函数的真值表如表2-3-2，试写出这个逻辑函数的逻辑式。

表 2-3-2 例 2-3-4 的逻辑真值表

---

## Chunk 142/161：`ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换 |
| section_id | ch02_sec_二_逻辑函数不同描述方法之间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p00 |
| next_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p02 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L139–163 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td> $1 \rightarrow {A}^{\prime }{B}^{\prime }{CD}^{\prime } = 1$ </td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td> $1 \rightarrow {A}^{\prime }{B}^{\prime }{CD} = 1$ </td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td> $1 \rightarrow {A}^{\prime }{BC}^{\prime }{D}^{\prime } = 1$ </td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td> $1 \rightarrow {A}^{\prime }{BC}{D}^{\prime } = 1$ </td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td> $1 \rightarrow {AB}^{\prime }{CD}^{\prime } = 1$ </td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td> $1 \rightarrow {AB}^{\prime }{CD} = 1$ </td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><

---

## Chunk 143/161：`ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换 |
| section_id | ch02_sec_二_逻辑函数不同描述方法之间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p01 |
| next_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p03 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L139–163 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换

/tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td></tr></table>

---

## Chunk 144/161：`ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p03 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换 |
| section_id | ch02_sec_二_逻辑函数不同描述方法之间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p02 |
| next_chunk_id | ch02_sec_解ex方法和步骤_theory_167 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L139–163 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 二、逻辑函数不同描述方法之间的转换

解：由真值表可见，当输入变量 ABCD 的取值为 0010、0011、0100、0110、1010 和 1011 之中的任何一种时，Y 都等于 1。这六种输入变量取值的每一种都使一个对应的最小项等于 1，所以输出 Y 就等于这些最小项之和。例如，当 ABCD 取值为 0010 时，最小项 $A'B'CD'=1$ ，所以 Y 的函数式中应包含这一项。而当 ABCD 取值为 0011 时，最小项 $A'B'CD=1$ ，所以 Y 的函数式中也应包含这一项。依此类推，于是得到

$$
Y = A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A ^ {\prime} B ^ {\prime} C D + A ^ {\prime} B C ^ {\prime} D ^ {\prime} + A ^ {\prime} B C D ^ {\prime} + A B ^ {\prime} C D ^ {\prime} + A B ^ {\prime} C D
$$

---

## Chunk 145/161：`ch02_sec_解ex方法和步骤_theory_167`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_解ex方法和步骤_theory_167 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 解题方法和步骤： |
| section_id | ch02_sec_解题方法和步骤 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_二_逻辑函数不同描述方法之间的转换_theory_139_p03 |
| next_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L167–171 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 解题方法和步骤：

（1）如果没有附加限制条件,则只要用逻辑图形符号取代逻辑函数式中的逻辑运算符号,将这些图形符号按输入到输出的顺序连起来,就得到所求的逻辑图了。

（2）如果对使用的逻辑图形符号有限制，则往往还需要将函数式变换为适于使用限定图形符号的形式,然后再用图形符号代替逻辑运算符号。例如,规定全部使用与非图形符号画出逻辑图,那么就必须先将函数式化为全部由与非运算组成的形式。这个问题我们在后面还会讲到。

---

## Chunk 146/161：`ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为 |
| section_id | ch02_sec_例2-3-5_给定逻辑函数式为 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图2 |
| prev_chunk_id | ch02_sec_解ex方法和步骤_theory_167 |
| next_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L173–288 |

### 配图

**图2** — 图2

![图2](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/442d0f24118324e689e5b79c25fced736598033ed35adcab21b4a3894382d9b4.jpg)

*视觉描述：* 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

**图2** — 图2

![图2](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/67ece744a7cd0161b1a01190044e9038bad590a401f44d1f489f017898ccc715.jpg)

*视觉描述：* 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

**图2** — 图2

![图2](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/0370a451385370b4f096f3422693002bd555c13471df32d4ac5bb74385520b82.jpg)

*视觉描述：* 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

**图2** — 图2

![图2](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/5334d4bfff031a83dd1b837297846c5a4d14b10b2f976cb80717b22313cbb728.jpg)

*视觉描述：* 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

**图2** — 图2

![图2](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/7ee226252f2c6c969fe092e581caedd95764939823c9c166610e9076d415bdaa.jpg)

*视觉描述：* 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为

$$
Y = A ^ {\prime} B D ^ {\prime} + A ^ {\prime} C D ^ {\prime} + B ^ {\prime} C
$$

试画出对应的逻辑图。

解：由于本题对逻辑图中可以使用的图形符号种类没有限制，所以直接用与、或、非逻辑图形符号取代式中的逻辑运算符号就行了，于是得到如图2-3-2所示的逻辑图。

## 3. 逻辑式 $\Rightarrow$ 卡诺图

解题方法和步骤：

(1) 将逻辑函数式展开为最小项之和的形式。

（2）画出最小项的卡诺图，在函数式中包含的最小项对应的位置上填入1，其余位置上填入0，就得到了表示该逻辑函数的卡诺图。如果函数式中包含无关项，则在相应位置上填入“×”，表示填入0或1均可。

图2-3-2 例2-3-5的逻辑图

【例2-3-6】 给定逻辑函数式为

$$
Y = A ^ {\prime} B C ^ {\prime} D + B ^ {\prime} C ^ {\prime} D ^ {\prime} + A ^ {\prime} C
$$

试画出表示该逻辑函数的卡诺图。

解：首先将 Y 化为最小项之和形式。式中第一项是最小项，第二、三项不是最小项。第二项缺少 A 或 $A'$ 因子，第三项缺少 B 或 $B'$ 和 D 或 $D'$ 因子。利用公式 $A + A' = 1$ ，将所缺的因子补齐，于是得到

$$
\begin{array}{r l} Y & = A ^ {\prime} B C ^ {\prime} D + B ^ {\prime} C ^ {\prime} D ^ {\prime} (A + A ^ {\prime}) + A ^ {\prime} C (B + B ^ {\prime}) (D + D ^ {\prime}) \\ & = A ^ {\prime} B C ^ {\prime} D + A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A ^ {\prime} B ^ {\prime} C D ^ {\prime} + A ^ {\prime} B ^ {\prime} C D + A ^ {\prime} B C D ^ {\prime} + A ^ {\prime} B C D \\ & = m _ {0} + m _ {2} + m _ {3} + m _ {5} + m _ {6} + m _ {7} + m _ {8} \end{array}
$$

[图2] 图2
[图2描述] 四变量AB-CD卡诺图带最小项下标，1位于m0,2,4,6,8,9,12,13,14,15。 | 函数Y1的四变量卡诺图：圈A'B'C'（顶行两格）、整行A'B、以及虚线圈A'B'C（底行右侧）。 | 函数Y2的四变量卡诺图：实线圈A'B'C'与A'C'四格块，虚线圈A'B'C，对应公共项化简示例。 | 函数Y3的四变量卡诺图：圈A'C'四格、A'B'C'、A'C'D'与A'CD'等项。 | 多输出与或阵列：五个与门产生A'B、AB'C、A'B'C'、AC'、A'D'，经三或门得Y1/Y2/Y3并共享公共积项。

---

## Chunk 147/161：`ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为 |
| section_id | ch02_sec_例2-3-5_给定逻辑函数式为 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p00 |
| next_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p02 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L173–288 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为

画出四变量的卡诺图，在其中 $m_{0}$ 、 $m_{2}$ 、 $m_{3}$ 、 $m_{5}$ 、 $m_{6}$ 、 $m_{7}$ 和 $m_{8}$ 的位置填入 1，其余位置填入 0，即得到如图 2-3-3 所示的卡诺图。

在解这类题目的过程中,完全可以跳过将函数展开为最小项之和的这一步,根据给出的逻辑式直接填写卡诺图中的1和0。例如 $B^{\prime}C^{\prime}D^{\prime}$ 一项包含了所有含 $B^{\prime}$ 、 $C^{\prime}$ 、 $D^{\prime}$ 因子的最小项,而 $A^{\prime}C$

则包含了所有含有 $A'$ 和 C 两个因子的最小项, 这样就可以直接填写出函数的卡诺图了。

【例2-3-7】已知逻辑函数式为

$$
Y = A B + A ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime}
$$

试画出表示 Y 的卡诺图。

解：因为 AB 这一项包含了所有含 AB 的最小项，所以可以直接在四变量卡诺图上标为 A=1、B=1 的最小项 $(m_{12}, m_{13}, m_{14}, m_{15})$ 位置上填入 1。同理， $A'D'$ 一项包含了所有含有 $A'D'$ 的最小项，所以在对应 A=0、D=0 的最小项 $(m_{0}, m_{2}, m_{4}, m_{6})$ 位置上填入 1。 $AB'C'$ 包含了所有含 $AB'C'$ 的最小项，所以在对应 A=1、B=0、C=0 的最小项$(m_{8}, m_{9})$ 位置上填入 1。这样就直接得到了如图2-3-4所示的卡诺图，而不必事先将 Y 化成最小项之和的表达式。

图2-3-3 例2-3-6的卡诺图

## 4. 波形图 $\Rightarrow$ 真值表

解题方法和步骤：

（1）在周期性重复的波形图中，将每个时间段内输入变量和输出的取值对应列表，即可得到函数的真值表。

（2）若波形图中有些输入变量状态组合始终没有出现，则这些输入变量组合下等于1的最小项为函数的约束项。

【例 2-3-8】由逻辑分析仪给出了某逻辑电路输入与输出的波形图如图2-3-5所示,试列出描述该电路逻辑功能的真值表。

图2-3-4 例2-3-7的卡诺图  
图2-3-5 例2-3-8的函数波形图

---

## Chunk 148/161：`ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为 |
| section_id | ch02_sec_例2-3-5_给定逻辑函数式为 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p01 |
| next_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p03 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L173–288 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为

解：由波形图上可以看出，从 ABC 的 001 状态至 111 状态为一个循环周期（也可以从任何一个其他状态算起，七个输入状态为一个循环周期），将 ABC 的七个不同的状态组合与 Y 的对应状态列表，即得表 2-3-3 的真值表。由于波形图中始终没有出现 ABC = 000 的状态，所以最小项 $A'B'C'$ 始终等于 0，是一个约束项，在真值表中以“×”表示。Y 的函数式中可以包含 $A'B'C'$ 这个最小项，也可以不包含这一项。

表 2-3-3 例 2-3-8 的逻辑真值表

<table><tr><td>A</td><td>B</td><td>C</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>0</td><td>0</td><td>0</td><td> $\times$ </td></tr></table>

## 5. 逻辑式 $\Rightarrow$ 真值表

解题方法和步骤：

将所有的输入变量取值组合逐一代入逻辑式,算出输出的函数值,然后将输入与输出的取值对应列成表格,得到的就是真值表。

【例2-3-9】已知逻辑函数式为

$$
Y = A B C + A B D + A C D + B C D
$$

试列出此函数的真值表。

解：将 ABCD 四个变量全部 16 种取值的组合 (0000\~1111) 逐个代入 Y 的函数式中，求出对应的 Y 值，然后列表，就得到了由表 2-3-4 所示的真值表。由真值表可以看出，这是一个代码判断函数。当输入代码中含有 3 个或 3 个以上的 1 时，Y=1；否则 Y=0。

表 2-3-4 例 2-3-9 的真值表

---

## Chunk 149/161：`ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p03 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为 |
| section_id | ch02_sec_例2-3-5_给定逻辑函数式为 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p02 |
| next_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p04 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L173–288 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为

<table><tr><td>A</td><td>B</td><td>C</td><td>D</td><td>Y</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr><tr><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>

6. 逻辑图 $\Rightarrow$ 逻辑式

解题方法和步骤：

通常采用的方法是从电路的输入端到输出端逐级写出逻辑图形符号所表示的逻辑运算式，从而得到所求的逻辑式。

【例2-3-10】写出图2-3-6所示电路输出 $Y$ 的逻辑函数式。

解：从输入端开始，逐级写出图形符号代表的逻辑运算式，如图2-3-6中所示，最后得到

---

## Chunk 150/161：`ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p04 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为 |
| section_id | ch02_sec_例2-3-5_给定逻辑函数式为 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p03 |
| next_chunk_id | ch02_sec_三_逻辑函数式的变换_theory_290 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L173–288 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 【例2-3-5】给定逻辑函数式为

$$
Y = A B + \left(A ^ {\prime} (B + C)\right) ^ {\prime} + B (B + C)
$$

图2-3-6 例2-3-10的逻辑图

## 7. 其他的互相转换

利用上面几种基本的转换方法,可以实现任何两种表示方法之间的转换。例如我们要找出给定逻辑图的真值表,就可以先写出等效的逻辑式,再从逻辑式列出真值表。又比如我们需写出给定波形图所代表的逻辑式,这时可以先列出与波形图对应的真值表,然后从真值表写出逻辑式。

---

## Chunk 151/161：`ch02_sec_三_逻辑函数式的变换_theory_290`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_三_逻辑函数式的变换_theory_290 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 三、逻辑函数式的变换 |
| section_id | ch02_sec_三_逻辑函数式的变换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_eg2-3-5_给定逻辑函数式为_theory_173_p04 |
| next_chunk_id | ch02_sec_2_theory_314_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L290–312 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 三、逻辑函数式的变换

在设计逻辑电路的过程中,往往首先得到的是逻辑函数的与或形式(也称为积之和形式)。如果规定全部使用与非门组成这个逻辑电路,这时就必须把与或形式的逻辑函数式变换成全部由与非运算组合成的形式(也称为与非-与非形式)。又如,在使用 ROM 实现一个组合逻辑函数时,则要求将逻辑函数式化为最小项之和的形式,等等。

## 1. 与或形式 $\Rightarrow$ 与非-与非形式

解题方法和步骤：

利用摩根定理将整个与或式两次求反,即可将与或形式化为与非-与非形式。

【例2-3-11】将下面的逻辑函数化为与非-与非形式

$$
Y = A B ^ {\prime} + A ^ {\prime} B D + C D ^ {\prime}
$$

解：应用摩根定理将上式两次求反，得到

$$
\begin{array}{r l} Y & = (Y ^ {\prime}) ^ {\prime} = ((A B ^ {\prime} + A ^ {\prime} B D + C D ^ {\prime}) ^ {\prime}) ^ {\prime} \\ & = ((A B ^ {\prime}) ^ {\prime} (A ^ {\prime} B D) ^ {\prime} (C D ^ {\prime}) ^ {\prime}) ^ {\prime} \end{array}
$$

这样就把函数式化成了全部由与非运算组成的形式。

---

## Chunk 152/161：`ch02_sec_2_theory_314_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_314_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_三_逻辑函数式的变换_theory_290 |
| next_chunk_id | ch02_sec_2_theory_314_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L314–491 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式

解题方法和步骤：

根据逻辑代数的基本公式和代入定理可知,任何一个逻辑函数都遵守公式 $Y + Y' = 1$ 。又知所有最小项之和恒等于 1，所以若将不包含在 Y 式中的所有最小项相加，得到的就是 $Y'$ 。将这些最小项之和再求反，也得到 Y。因此，将不包含在函数式中的那些最小项相加，然后求反，得到的就是函数式的与或非形式。

如果画出函数的卡诺图,则只需将图中填入0的那些最小项相加,再求反,就可得到与或非形式的逻辑函数式了。

【例2-3-12】将下面的逻辑函数式化为与或非形式

$$
Y = A ^ {\prime} C ^ {\prime} D ^ {\prime} + A ^ {\prime} B D + A B ^ {\prime} + B ^ {\prime} C D ^ {\prime}
$$

解：首先画出 Y 的卡诺图，如图 2-3-7 所示。

图2-3-7 例2-3-12的卡诺图

将卡诺图中的 0 合并, 然后求反, 得到

$$
Y = \left(A ^ {\prime} B ^ {\prime} D + A B + B C D ^ {\prime}\right) ^ {\prime}
$$

## 3. 与或式 $\Rightarrow$ 或与式

解题方法和步骤：

方法一,首先用上面所讲的方法将与或形式的逻辑函数转换成与或非形式。然后,利用摩根定理就可以将与或非形式的逻辑式转换成或与形式的逻辑式了。

方法二, 反复运用公式 $A + BC = (A + B)(A + C)$ 进行运算, 也可以将与或形式的逻辑函数式变换为或与形式的逻辑函数式。

【例2-3-13】将下面给出的逻辑函数转换为或与形式的逻辑式

$$
Y = A C + A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime}
$$

解：采用第一种方法时，需首先画出 Y 的卡诺图，如图 2-3-8 所示。

将图中的 0 合并, 然后求反, 得到

$$
Y = \left(A ^ {\prime} B C + A C ^ {\prime}\right) ^ {\prime}
$$

再利用摩根定理将上式展开

$$
\begin{array}{r l} Y & = (A ^ {\prime} B C) ^ {\prime} \cdot (A C ^ {\prime}) ^ {\prime} \\ & = (A + B ^ {\prime} + C ^ {\prime}) (A ^ {\prime} + C) \end{array}
$$

也可以采用第二种方法,直接进行公式运算

---

## Chunk 153/161：`ch02_sec_2_theory_314_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_314_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_theory_314_p00 |
| next_chunk_id | ch02_sec_2_theory_314_p02 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L314–491 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式

$$
\begin{array}{r l} Y & = A C + A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime} \\ & = (A + A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime}) (C + A ^ {\prime} B ^ {\prime} + A ^ {\prime} C ^ {\prime}) \\ & = (A + B ^ {\prime} + C ^ {\prime}) (C + A ^ {\prime} B ^ {\prime} + A ^ {\prime}) \\ & = (A + B ^ {\prime} + C ^ {\prime}) (A ^ {\prime} + C) \end{array}
$$

图2-3-8 例2-3-13的卡诺图

也得到同样的变换结果。

这里需要提醒一点,用第二种公式推演方法得到的或与式有时不是最简的,还能进一步化简;而用第一种方法,在合并卡诺图上的0时已经进行了合并化简,所以得到的或与表达式应当是最简的了。

## 4. 与或式 $\Rightarrow$ 或非-或非式

解题方法和步骤：

（1）首先按前述方法将与或式转换为与或非形式。

（2）用摩根定理将与或非式中的每个乘积项化为或非的形式，即可得到或非-或非形式的函数式了。

【例2-3-14】将下面的逻辑函数式化为或非-或非形式

$$
Y = A ^ {\prime} D ^ {\prime} + A ^ {\prime} B ^ {\prime} C + A C ^ {\prime} D + C D ^ {\prime}
$$

解：画出 Y 的卡诺图，如图 2-3-9 所示。

将图中的0合并后得到

$$
\begin{array}{r l} Y & = (A C ^ {\prime} D ^ {\prime} + A ^ {\prime} C ^ {\prime} D + A C D + B C D) ^ {\prime} \\ & = ((A ^ {\prime} + C + D) ^ {\prime} + (A + C + D ^ {\prime}) ^ {\prime} + \\ & (A ^ {\prime} + C ^ {\prime} + D ^ {\prime}) ^ {\prime} + (B ^ {\prime} + C ^ {\prime} + D ^ {\prime}) ^ {\prime}) ^ {\prime} \end{array}
$$

5. 将逻辑函数式化为最小项之和的形式

解题方法和步骤：

（1）首先利用逻辑代数的公式和定理将函数式化成与或形式。

---

## Chunk 154/161：`ch02_sec_2_theory_314_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_314_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_theory_314_p01 |
| next_chunk_id | ch02_sec_2_theory_314_p03 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L314–491 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式

图2-3-9 例2-3-14的卡诺图

（2）利用公式 $A+A'=1$ 将每个乘积项中缺少的因子补齐。例如某个乘积项中缺少因子 B，则应在该项上乘以 $(B+B')$ ，然后拆成两项，每项中便分别增加了 B 或 $B'$ 因子。

【例2-3-15】试将下面的逻辑函数式化为最小项之和的形式

$$
Y = \left(\left(A B ^ {\prime}\right) ^ {\prime} + C\right) ^ {\prime} + A D
$$

解：首先将上式化为与或形式

$$
Y = (A B ^ {\prime}) C ^ {\prime} + A D = A B ^ {\prime} C ^ {\prime} + A D
$$

然后在第一项上乘以 $(D+D')$ ，在第二项上乘以 $(B+B')$ ，得到

$$
\begin{array}{r l} Y & = A B ^ {\prime} C ^ {\prime} (D + D ^ {\prime}) + A D (B + B ^ {\prime}) \\ & = A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D + A B D + A B ^ {\prime} D \end{array}
$$

再将上式的最后两项上各乘以 $(C+C')$ ，最后得到

$$
\begin{array}{r l} Y & = A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D + A B ^ {\prime} D (C + C ^ {\prime}) + A B D (C + C ^ {\prime}) \\ & = A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D + A B ^ {\prime} C D + A B C D + A B C ^ {\prime} D \\ & = m _ {8} + m _ {9} + m _ {1 1} + m _ {1 3} + m _ {1 5} \end{array}
$$

6. 将逻辑函数式化为最大项之积的形式

解题方法和步骤：

（1）若给出的函数式已经是或与形式，则可以利用公式 $AA' = 0$ 将每个括号内缺少的因子补齐。例如 $(A + C')$ 中缺少 B 或 $B'$ ，这时就可以在括号里加上 $BB'$ ，然后再利用公式 $A + BC = (A + B)(A + C)$ 将它拆开，就得到了两个最大项的乘积

---

## Chunk 155/161：`ch02_sec_2_theory_314_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_314_p03 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_theory_314_p02 |
| next_chunk_id | ch02_sec_2_theory_314_p04 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L314–491 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式

$$
(A + C ^ {\prime} + B B ^ {\prime}) = (A + B ^ {\prime} + C ^ {\prime}) (A + B + C ^ {\prime})
$$

（2）若给出的函数式是与或形式，则应当先利用上面介绍的方法将它变换为或与形式，然后再按(1)中所说的方法去做。

【例2-3-16】将下面的逻辑函数式化为最大项之积的形式

$$
Y = (B + C ^ {\prime}) (A + B ^ {\prime} + C)
$$

解：在左边的一个括号内加入 $AA'$ ，然后利用公式 $A + BC = (A + B)(A + C)$ 将它拆开成两个最大项，得到

$$
\begin{array}{r l} Y & = (B + C ^ {\prime} + A A ^ {\prime}) (A + B ^ {\prime} + C) \\ & = (A ^ {\prime} + B + C ^ {\prime}) (A + B + C ^ {\prime}) (A + B ^ {\prime} + C) \\ & = M _ {1} M _ {2} M _ {5} \end{array}
$$

【例2-3-17】将下面的逻辑函数式化为最大项之积的形式

$$
Y = A ^ {\prime} B D + A B ^ {\prime} C ^ {\prime} + A ^ {\prime} C + A D ^ {\prime} + B C + B ^ {\prime} D ^ {\prime}
$$

解：首先将上式化成最小项之和的形式

$$
Y (A, B, C, D) = \sum m (0, 2, 3, 5, 6, 7, 8, 9, 1 0, 1 2, 1 4, 1 5)
$$

而 $Y'$ 应当等于不包含在上式中的那些最小项之和, 即

$$
Y ^ {\prime} (A, B, C, D) = \sum m (1, 4, 1 1, 1 3)
$$

因此

$$
\begin{array}{r l} Y (A, B, C, D) & = \left(Y ^ {\prime}\right) ^ {\prime} = \left(m _ {1} + m _ {4} + m _ {1 1} + m _ {1 3}\right) ^ {\prime} \\ & = m _ {1} ^ {\prime} m _ {4} ^ {\prime} m _ {1 1} ^ {\prime} m _ {1 3} ^ {\prime} \end{array}
$$

根据 $m_i' = M_i$ ，于是得到

---

## Chunk 156/161：`ch02_sec_2_theory_314_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_2_theory_314_p04 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式 |
| section_id | ch02_sec_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_theory_314_p03 |
| next_chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L314–491 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 2 与或形式 $\Rightarrow$ 与或非形式

$$
\begin{array}{r l} Y (A, B, C, D) & = M _ {1} M _ {4} M _ {1 1} M _ {1 3} \\ & = (A + B + C + D ^ {\prime}) (A + B ^ {\prime} + C + D) \\ & (A ^ {\prime} + B + C ^ {\prime} + D ^ {\prime}) (A ^ {\prime} + B ^ {\prime} + C + D ^ {\prime}) \end{array}
$$

---

## Chunk 157/161：`ch02_sec_四_逻辑函数的化简_theory_493_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 四、逻辑函数的化简 |
| section_id | ch02_sec_四_逻辑函数的化简 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_2_theory_314_p04 |
| next_chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L493–519 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 四、逻辑函数的化简

## 1. 公式化简法

解题方法和步骤：

公式化简法就是运用逻辑代数的公式和定理进行逻辑运算,以消去逻辑函数式中多余的乘积项和每项中多余的因子。

如果是有无关项的逻辑函数,则应充分利用无关项的特点(可以写入逻辑式也可以从逻辑式中删除),使化简的结果更加简单。

【例2-3-18】用公式化简法化简下面的逻辑函数

$$
Y = \left(\left(A ^ {\prime} + B ^ {\prime}\right) D\right) ^ {\prime} + \left(A ^ {\prime} B ^ {\prime} + B D\right) C ^ {\prime} + A ^ {\prime} B C ^ {\prime} D + D ^ {\prime}
$$

---

## Chunk 158/161：`ch02_sec_四_逻辑函数的化简_theory_493_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > 四、逻辑函数的化简 |
| section_id | ch02_sec_四_逻辑函数的化简 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p00 |
| next_chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p00 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L493–519 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > 四、逻辑函数的化简

$$
\begin{array}{r l} \text {解:} Y = ((A B) ^ {\prime} D) ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} + B C ^ {\prime} D + A ^ {\prime} B C ^ {\prime} D + D ^ {\prime} \dots (\text {根据} A ^ {\prime} + B ^ {\prime} = (A B) ^ {\prime}, \\ & (A + B) C = A C + B C) \\ & = A B + D ^ {\prime} + A ^ {\prime} B ^ {\prime} C ^ {\prime} + B C ^ {\prime} + A ^ {\prime} B C ^ {\prime} \dots \dots (\text {根据} (A B) ^ {\prime} = A ^ {\prime} + B ^ {\prime}, \\ & A + A ^ {\prime} B = A + B) \\ & = A B + D ^ {\prime} + A ^ {\prime} C ^ {\prime} + B C ^ {\prime} \dots \dots (\text {根据} A + A ^ {\prime} = 1) \\ & = A B + D ^ {\prime} + A ^ {\prime} C ^ {\prime} + (A + A ^ {\prime}) B C ^ {\prime} \dots \dots (\text {根据} A + A ^ {\prime} = 1) \\ & = A B + D ^ {\prime} + A ^ {\prime} C ^ {\prime} + A B C ^ {\prime} + A ^ {\prime} B C ^ {\prime} \dots \dots (\text {根据} (A + B) C = A C + B C) \\ & = A B + D ^ {\prime} + A ^ {\prime} C ^ {\prime} \dots \dots (\text {根据} A + A B = A) \end{array}
$$

2. 卡诺图化简法

解题方法和步骤：

(1) 画出表示逻辑函数的卡诺图。

(2) 找出可以合并的最小项, 把它们圈起来。

---

## Chunk 159/161：`ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是 |
| section_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_四_逻辑函数的化简_theory_493_p01 |
| next_chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p01 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L521–593 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是

第一,这些乘积项必须包含函数式中所有的最小项,即包含卡诺图中全部的1;

第二,所用的乘积项数目最少,即用最少的可合并的圈将卡诺图中的1圈进去;

第三,每个乘积项的因子最少,即每个圈应尽可能地圈大。

为了使每个可以合并的圈尽量大,可以在不同的圈里重复圈入某一项。因为 $A+A=A$ , 所以重复写入某个最小项不影响逻辑函数值。

如果是有无关项的函数,则既可以将它圈入可合并的最小项当中,也可以不圈入。是否应当圈入可合并的最小项当中,要看能否得到最大的合并圈。

【例2-3-19】试用卡诺图化简如下的逻辑函数

$$
\begin{array}{r l} & Y = A ^ {\prime} B C ^ {\prime} + A ^ {\prime} C ^ {\prime} D + A B ^ {\prime} C + B C D ^ {\prime} \\ & \quad A ^ {\prime} B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B ^ {\prime} C ^ {\prime} D ^ {\prime} + A B C D = 0 (\text {   约束条件   }) \end{array}
$$

解：将 $Y$ 展开为最小项之和形式得到

$$
\begin{array}{r l} Y & = A ^ {\prime} B C ^ {\prime} D ^ {\prime} + A ^ {\prime} B C ^ {\prime} D + A ^ {\prime} B ^ {\prime} C ^ {\prime} D + A ^ {\prime} B C D ^ {\prime} + A B ^ {\prime} C D ^ {\prime} + A B ^ {\prime} C D + A B C D ^ {\prime} \\ & = m _ {1} + m _ {4} + m _ {5} + m _ {6} + m _ {1 0} + m _ {1 1} + m _ {1 4} \\ & \quad m _ {0} + m _ {8} + m _ {1 5} = \mathbf {0} (\text {约束条件}) \end{array}
$$

在四变量最小项卡诺图中，在 Y 所含最小项的位置上填入 1，约束项位置上填入“×”，其余位置上填入 0，就得到了 Y 的卡诺图，如图 2-3-10 所示。

图2-3-10 例2-3-19的卡诺图

---

## Chunk 160/161：`ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是 |
| section_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p00 |
| next_chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p02 |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L521–593 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是

利用约束项 $m_{0}$ 可将 $m_{0}$ 、 $m_{1}$ 、 $m_{4}$ 和 $m_{5}$ 合并为 $A^{\prime}C^{\prime}$ ，利用约束项 $m_{15}$ 可将 $m_{10}$ 、 $m_{11}$ 、 $m_{14}$ 和 $m_{15}$ 合并为 AC。化简后的结果为

$$
Y = A ^ {\prime} C ^ {\prime} + A C + B C D ^ {\prime}
$$

如将上式展开为最小之和形式时，式中将包含有 $m_0$ 和 $m_{15}$ 两个约束项，而不包含 $m_8$ 。

## 3. 多输出逻辑函数的化简

在化简一组具有多输出的逻辑函数时,应当充分利用这些逻辑函数式中含有的“共用项”,以求得总体上最简的化简结果。

从这一组函数的卡诺图上寻找共用项的方法虽然简单、直观，但局限性很大，尤其是在输入变量较多的情况下。为了解决多变量、多输出逻辑函数的化简问题，可以将Q-M化简法用于多输出逻辑函数的化简，并在此基础上编制出适于计算机化简的程序。读者如有兴趣，可参阅《数字电子技术基础(第六版)》参考文献[3]的第四章。

【例 2-3-20】化简下列一组多输出逻辑函数。要求充分利用共用项,以求整体化简结果最简

$$
\begin{array}{l} {Y _ {1} (A, B, C, D) = \sum \mathrm{m} (0, 1, 4, 5, 6, 7, 1 0, 1 1)} \\ {Y _ {2} (A, B, C, D) = \sum \mathrm{m} (0, 1, 8, 9, 1 0, 1 1, 1 2, 1 3)} \\ {Y _ {3} (A, B, C, D) = \sum \mathrm{m} (0, 1, 2, 4, 6, 8, 9, 1 2, 1 3)} \end{array}
$$

解：首先画出 $Y_{1}, Y_{2}, Y_{3}$ 的卡诺图，如图2-3-11(a)所示。由图可见， $(m_{0}, m_{1})$ 是 $Y_{1}, Y_{2}$ 和 $Y_{3}$ 的共用项； $(m_{10}, m_{11})$ 是 $Y_{1}, Y_{2}$ 的共用项； $(m_{8}, m_{9}, m_{12}, m_{13})$ 是 $Y_{2}, Y_{3}$ 的共用项。利用这3个共用项化简的结果为

---

## Chunk 161/161：`ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是 |
| section_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch02_sec_3_选择化简后保留的乘积项_选取的原则是_theory_521_p01 |
| next_chunk_id | — |
| source_file | 学习辅导按章节拆分\03_第二部分_第02章_逻辑代数基础_重点难点.md |
| line_range | L521–593 |

### 正文（检索用 text_content）

第02章 逻辑代数基础 > 逻辑代数基础 > （3）选择化简后保留的乘积项。选取的原则是

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A ^ {\prime} B + A B ^ {\prime} C \\ Y _ {2} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A C ^ {\prime} + A B ^ {\prime} C \\ Y _ {3} (A, B, C, D) = A ^ {\prime} B ^ {\prime} C ^ {\prime} + A C ^ {\prime} + A ^ {\prime} D ^ {\prime} \end{array}
$$

实现上述一组逻辑函数需要用8个门电路和21个输入端，如图2-3-11(b)所示。

如果分别将 $Y_{1}$ 、 $Y_{2}$ 和 $Y_{3}$ 单独进行化简，则可以按图 2-3-11(c) 所示合并最小项，得到

$$
\begin{array}{l} Y _ {1} (A, B, C, D) = A ^ {\prime} C ^ {\prime} + A ^ {\prime} B + A B ^ {\prime} C \\ Y _ {2} (A, B, C, D) = B ^ {\prime} C ^ {\prime} + A C ^ {\prime} + A B ^ {\prime} \\ Y _ {3} (A, B, C, D) = A ^ {\prime} D ^ {\prime} + A C ^ {\prime} + B ^ {\prime} C ^ {\prime} \end{array}
$$

按这一组逻辑函数式接成的逻辑图将如图 2-3-11(d) 所示。这时需要使用 12 个门电路和 28 个输入端。

(a)  
(b)
