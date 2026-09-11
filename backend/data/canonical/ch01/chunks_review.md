# 第01章 数制和码制 — Chunk 效果预览

> 自动生成，用于人工抽检。每个 chunk 以 `---` 分隔。

## 汇总

- 总 chunk 数：**68**
- 习题合并：**15/15**
- 教材图：**2**（含子图拆分）
- orphan 图：**0**
- 视觉描述：**3** 张

---

## Chunk 1/68：`ch01_sec_summary_theory_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_summary_theory_2 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary 内容提要 |
| section_id | ch01_sec_summary |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | — |
| next_chunk_id | ch01_sec_1_1_theory_6 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L2–4 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary 内容提要

本章首先介绍有关数制和码制的一些基本概念和术语,然后给出常用的数制和码制。此外,还将具体讲述不同数制之间的转换方法和二进制数算术运算的原理和方法。

---

## Chunk 2/68：`ch01_sec_1_1_theory_6`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_1_theory_6 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.1 概述 |
| section_id | ch01_sec_1_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_summary_theory_2 |
| next_chunk_id | ch01_sec_一_十进制_theory_20 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L6–16 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.1 概述

数字电路所处理的各种数字信号都是以数码形式给出的。不同的数码既可以用来表示不同数量的大小，又可以用来表示不同的事物或事物的不同状态。

用数码表示数量的大小时,仅仅使用一位数码往往不够用,因而经常需要用进位计数制的方法组成多位数码使用。多位数码中每一位的构成方法和从低位到高位的进位规则称为数制。在绪论中我们曾经提及,数字电路中使用最多的数制是二进制,其次是在二进制基础上构成的十六进制和十进制。有时也用到八进制。

当两个数码分别表示两个数量大小时,可以进行数量间的加、减、乘、除等运算。这一类运算称为算术运算。鉴于目前数字电路中的算术运算最终都是以二进制运算进行的,所以在这一章里我们还将比较详细地讨论在数字电路中是采用什么方式完成二进制算术运算的。

在用不同数码表示不同事物或事物的不同状态时,这些数码已经不再具有表示数量大小的含义了,它们只是不同事物的代号而已。我们将这些数码称之为代码。例如在举行长跑比赛时,为便于识别运动员,通常要给每一位运动员编一个号码。显然,这些号码仅仅表示不同的运动员而已,没有数量大小的含义。

为了便于记忆和查找，在编制代码时总要遵循一定的规则，这些规则就称为码制。每个人都可以根据自己的需要选定编码规则，编制出一组代码。但是考虑到信息交换的需要，还必须制定一些大家共同使用的通用代码。例如目前国际上通用的美国信息交换标准代码(ASCII码)就属于这一种。

---

## Chunk 3/68：`ch01_sec_一_十进制_theory_20`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_十进制_theory_20 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 一、十进制 |
| section_id | ch01_sec_一_十进制 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_1_1_theory_6 |
| next_chunk_id | ch01_sec_二_二进制_theory_46 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L20–44 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、十进制

十进制是日常生活和工作中最常使用的进位计数制。在十进制数中，每一位有0\~9十个数码，所以计数的基数是10。超过9的数必须用多位数表示，其中低位和相邻高位之间的关系是

“逢十进一”，故称为十进制。例如

$$
1 4 3. 7 5 = 1 \times 1 0 ^ {2} + 4 \times 1 0 ^ {1} + 3 \times 1 0 ^ {0} + 7 \times 1 0 ^ {- 1} + 5 \times 1 0 ^ {- 2}
$$

所以任意一个多位的十进制数 $D$ 均可展开为

$$
D = \sum k _ {i} \times 1 0 ^ {i}\tag{1.2.1}
$$

式中 $k_{i}$ 是第 i 位的系数, 它可以是 0\~9 这十个数码中的任何一个。若整数部分的位数是 n, 小数部分的位数为 m, 则 i 包含从 n-1 到 0 的所有正整数和从 -1 到 -m 的所有负整数, 整数部分的最高位为 n-1, 最低位为 0; 小数部分的最高位为 -1, 最低位为 -m。

若以 $N$ 取代式(1.2.1)中的10，即可得到多位任意进制（ $N$ 进制）数展开式的普遍形式

$$
D = \sum k _ {i} N ^ {i}\tag{1.2.2}
$$

式中 $i$ 的取值与式(1.2.1)的规定相同。 $N$ 称为计数的基数， $k_{i}$ 为第 $i$ 位的系数， $N^i$ 称为第 $i$ 位的权。

---

## Chunk 4/68：`ch01_sec_二_二进制_theory_46`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_二进制_theory_46 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、二进制 |
| section_id | ch01_sec_二_二进制 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_十进制_theory_20 |
| next_chunk_id | ch01_sec_三_八进制_theory_64 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L46–62 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、二进制

目前在数字电路中应用最广泛的是二进制。在二进制数中，每一位仅有0和1两个可能的数码，所以计数基数为2。低位和相邻高位间的进位关系是“逢二进一”，故称为二进制。

根据式 $(1.2.2)$ ，任何一个二进制数均可展开为

$$
D = \sum k _ {i} 2 ^ {i}\tag{1.2.3}
$$

并可用上式计算出它所表示的十进制数的大小。例如

$$
\begin{array}{r l} (1 0 1. 1 1) _ {2} & = 1 \times 2 ^ {2} + 0 \times 2 ^ {1} + 1 \times 2 ^ {0} + 1 \times 2 ^ {- 1} + 1 \times 2 ^ {- 2} \\ & = (5. 7 5) _ {1 0} \end{array}
$$

上式中分别使用下脚注2和10表示括号里的数是二进制数和十进制数。有时也用B(Binary)和D(Decimal)代替2和10这两个脚注。

---

## Chunk 5/68：`ch01_sec_三_八进制_theory_64`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_八进制_theory_64 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、八进制 |
| section_id | ch01_sec_三_八进制 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_二进制_theory_46 |
| next_chunk_id | ch01_sec_四_十六进制_theory_80_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L64–78 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、八进制

在某些场合有时也使用八进制。八进制数的每一位有0\~7八个不同的数码，计数的基数为8。低位和相邻的高位之间的进位关系是“逢八进一”。任意一个八进制数可以展开为

$$
D = \sum k _ {i} 8 ^ {i}\tag{1.2.4}
$$

并可利用上式计算出与之等效的十进制数值。例如

$$
\begin{array}{r l} (1 2. 4) _ {8} & = 1 \times 8 ^ {1} + 2 \times 8 ^ {0} + 4 \times 8 ^ {- 1} \\ & = (1 0. 5) _ {1 0} \end{array}
$$

有时也用 O(Octal) 代替下脚注 8, 表示八进制数。

---

## Chunk 6/68：`ch01_sec_四_十六进制_theory_80_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_四_十六进制_theory_80_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 四、十六进制 |
| section_id | ch01_sec_四_十六进制 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_八进制_theory_64 |
| next_chunk_id | ch01_sec_四_十六进制_theory_80_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L80–102 |

### 正文（检索用 text_content）

第01章 数制和码制 > 四、十六进制

十六进制数的每一位有十六个不同的数码,分别用 0\~9、A(10)、B(11)、C(12)、D(13)、E(14)、F(15)表示。因此,任意一个十六进制数均可展开为

$$
D = \sum k _ {i} 1 6 ^ {i}\tag{1.2.5}
$$

并可由此式计算出它所表示的十进制数值。例如

$$
\begin{array}{r l} (2 \mathrm{A}. 7 \mathrm{F}) _ {1 6} & = 2 \times 1 6 ^ {1} + 1 0 \times 1 6 ^ {0} + 7 \times 1 6 ^ {- 1} + 1 5 \times 1 6 ^ {- 2} \\ & = (4 2. 4 9 6 0 9 3 7) _ {1 0} \end{array}
$$

式中的下脚注 16 表示括号里的数是十六进制数,有时也用 H(Hexadecimal)代替这个脚注。

由于目前在微型计算机中普遍采用8位、16位和32位二进制并行运算，而8位、16位和32位的二进制数可以用2位、4位和8位的十六进制数表示，因而用十六进制符号书写程序十分简便。

表 1.2.1 是十进制数 0\~15 与等值二进制、八进制、十六进制数的对照表。

表 1.2.1 不同进制数的对照表

---

## Chunk 7/68：`ch01_sec_四_十六进制_theory_80_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_四_十六进制_theory_80_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 四、十六进制 |
| section_id | ch01_sec_四_十六进制 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_四_十六进制_theory_80_p00 |
| next_chunk_id | ch01_sec_review_review_105 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L80–102 |

### 正文（检索用 text_content）

第01章 数制和码制 > 四、十六进制

<table><tr><td>十进制( Decimal)</td><td>二进制( Binary)</td><td>八进制( Octal)</td><td>十六进制( Hexadecimal)</td></tr><tr><td>00</td><td>0000</td><td>00</td><td>0</td></tr><tr><td>01</td><td>0001</td><td>01</td><td>1</td></tr><tr><td>02</td><td>0010</td><td>02</td><td>2</td></tr><tr><td>03</td><td>0011</td><td>03</td><td>3</td></tr><tr><td>04</td><td>0100</td><td>04</td><td>4</td></tr><tr><td>05</td><td>0101</td><td>05</td><td>5</td></tr><tr><td>06</td><td>0110</td><td>06</td><td>6</td></tr><tr><td>07</td><td>0111</td><td>07</td><td>7</td></tr><tr><td>08</td><td>1000</td><td>10</td><td>8</td></tr><tr><td>09</td><td>1001</td><td>11</td><td>9</td></tr><tr><td>10</td><td>1010</td><td>12</td><td>A</td></tr><tr><td>11</td><td>1011</td><td>13</td><td>B</td></tr><tr><td>12</td><td>1100</td><td>14</td><td>C</td></tr><tr><td>13</td><td>1101</td><td>15</td><td>D</td></tr><tr><td>14</td><td>1110</td><td>16</td><td>E</td></tr><tr><td>15</td><td>1111</td><td>17</td><td>F</td></tr></table>

---

## Chunk 8/68：`ch01_sec_review_review_105`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_105 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_四_十六进制_theory_80_p01 |
| next_chunk_id | ch01_sec_review_review_107 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L105–106 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.2.1 写出 4 位二进制数、4 位八进制数和 4 位十六进制数的最大数。

---

## Chunk 9/68：`ch01_sec_review_review_107`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_107 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_105 |
| next_chunk_id | ch01_sec_一_二-十转换_theory_112 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L107–108 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.2.2 与4位二进制数、4位八进制数、4位十六进制数的最大值等值的十进制数各为多少？

---

## Chunk 10/68：`ch01_sec_一_二-十转换_theory_112`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_二-十转换_theory_112 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 一、二-十转换 |
| section_id | ch01_sec_一_二-十转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_107 |
| next_chunk_id | ch01_sec_二_十-二转换_theory_122_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L112–120 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、二-十转换

将二进制数转换为等值的十进制数称为二-十转换。转换时只要将二进制数按式(1.2.3)

展开,然后将所有各项的数值按十进制数相加,就可以得到等值的十进制数了。例如

$$
\begin{array}{r l} (1 0 1 1. 0 1) _ {2} & = 1 \times 2 ^ {3} + 0 \times 2 ^ {2} + 1 \times 2 ^ {1} + 1 \times 2 ^ {0} + 0 \times 2 ^ {- 1} + 1 \times 2 ^ {- 2} \\ & = (1 1. 2 5) _ {1 0} \end{array}
$$

---

## Chunk 11/68：`ch01_sec_二_十-二转换_theory_122_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_十-二转换_theory_122_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、十-二转换 |
| section_id | ch01_sec_二_十-二转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_二-十转换_theory_112 |
| next_chunk_id | ch01_sec_二_十-二转换_theory_122_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L122–184 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、十-二转换

所谓十-二转换,就是将十进制数转换为等值的二进制数。

首先讨论整数的转换。

假定十进制整数为 $(S)_{10}$ ，等值的二进制数为 $(k_{n}k_{n-1}\cdots k_{0})_{2}$ ，则依式(1.2.3)可知

$$
\begin{array}{r l} (S) _ {1 0} & = \left(k _ {n} 2 ^ {n} + k _ {n - 1} 2 ^ {n - 1} + \dots + k _ {1} 2 ^ {1} + k _ {0} 2 ^ {0}\right) _ {2} \\ & = 2 \left(k _ {n} 2 ^ {n - 1} + k _ {n - 1} 2 ^ {n - 2} + \dots + k _ {1}\right) _ {2} + k _ {0} \end{array}\tag{1.3.1}
$$

上式表明，若将 $(S)_{10}$ 除以2，则得到的商为 $k_{n}2^{n-1}+k_{n-1}2^{n-2}+\cdots+k_{1}$ ，而余数即 $k_{0}$ 。同理，可将式(1.3.1)除以2得到的商写成

$$
\left(k _ {n} 2 ^ {n - 1} + k _ {n - 1} 2 ^ {n - 2} + \dots + k _ {1}\right) _ {2} = 2 \left(k _ {n} 2 ^ {n - 2} + k _ {n - 1} 2 ^ {n - 3} + \dots + k _ {2}\right) _ {2} + k _ {1}\tag{1.3.2}
$$

由式(1.3.2)不难看出,若将 $(S)_{10}$ 除以2所得的商再次除以2,则所得余数即 $k_{1}$ 。

依此类推,反复将每次得到的商再除以2,就可求得二进制数的每一位了。

例如，将 $(173)_{10}$ 化为二进制数可如下进行

---

## Chunk 12/68：`ch01_sec_二_十-二转换_theory_122_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_十-二转换_theory_122_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、十-二转换 |
| section_id | ch01_sec_二_十-二转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_十-二转换_theory_122_p00 |
| next_chunk_id | ch01_sec_二_十-二转换_theory_122_p02 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L122–184 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、十-二转换

$$
\begin{array}{r l} & 2 \boxed {1 7 3} \quad \text {余数} = 1 = k _ {0} \\ & 2 \boxed {8 6} \quad \text {余数} = 0 = k _ {1} \\ & 2 \boxed {4 3} \quad \text {余数} = 1 = k _ {2} \\ & 2 \boxed {2 1} \quad \text {余数} = 1 = k _ {3} \\ & 2 \boxed {1 0} \quad \text {余数} = 0 = k _ {4} \\ & 2 \boxed {5} \quad \text {余数} = 1 = k _ {5} \\ & 2 \boxed {2} \quad \text {余数} = 0 = k _ {6} \\ & 2 \boxed {1} \quad \text {余数} = 1 = k _ {7} \\ & 0 \end{array}
$$

故 $(173)_{10} = (10101101)_2$

其次讨论小数的转换。

若 $(S)_{10}$ 是一个十进制的小数，对应的二进制小数为 $(0.k_{-1}k_{-2}\cdots k_{-m})_{2}$ ，则据式(1.2.3)可知

$$
(S) _ {1 0} = \left(k _ {- 1} 2 ^ {- 1} + k _ {- 2} 2 ^ {- 2} + \dots + k _ {- m} 2 ^ {- m}\right) _ {2}
$$

将上式两边同乘以2得到

$$
2 (S) _ {1 0} = k _ {- 1} + \left(k _ {- 2} 2 ^ {- 1} + k _ {- 3} 2 ^ {- 2} + \dots + k _ {- m} 2 ^ {- m + 1}\right) _ {2}\tag{1.3.3}
$$

式(1.3.3)说明,将小数 $(S)_{10}$ 乘以2所得乘积的整数部分即 $k_{-1}$ 。

同理,将乘积的小数部分再乘以2又可得到

$$
2 \left(k _ {- 2} 2 ^ {- 1} + k _ {- 3} 2 ^ {- 2} + \dots + k _ {- m} 2 ^ {- m + 1}\right) _ {2} = k _ {- 2} + \left(k _ {- 3} 2 ^ {- 1} + \dots + k _ {- m} 2 ^ {- m + 2}\right) _ {2}\tag{1.3.4}
$$

亦即乘积的整数部分就是 $k_{-2}$ 。

依此类推,将每次乘2后所得乘积的小数部分再乘以2,便可求出二进制小数的每一位了。

---

## Chunk 13/68：`ch01_sec_二_十-二转换_theory_122_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_十-二转换_theory_122_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、十-二转换 |
| section_id | ch01_sec_二_十-二转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_十-二转换_theory_122_p01 |
| next_chunk_id | ch01_sec_三_二-十六转换_theory_186 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L122–184 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、十-二转换

例如，将 $(0.8125)_{10}$ 化为二进制小数时可如下进行

$$
\begin{array}{r l} & 0. 8 1 2 5 \\ & \times \quad 2 \\ & \hline 1. 6 2 5 0 \dots \text {整数部分} = 1 = k _ {- 1} \\ & 0. 6 2 5 0 \\ & \times \quad 2 \\ & \hline 1. 2 5 0 0 \dots \text {整数部分} = 1 = k _ {- 2} \\ & 0. 2 5 0 0 \\ & \times \quad 2 \\ & \hline 0. 5 0 0 0 \dots \text {整数部分} = 0 = k _ {- 3} \\ & 0. 5 0 0 0 \\ & \times \quad 2 \\ & \hline 1. 0 0 0 0 \dots \text {整数部分} = 1 = k _ {- 4} \end{array}
$$

故 $(0.8125)_{10}=(0.1101)_{2}$

---

## Chunk 14/68：`ch01_sec_三_二-十六转换_theory_186`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_二-十六转换_theory_186 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、二-十六转换 |
| section_id | ch01_sec_三_二-十六转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_十-二转换_theory_122_p02 |
| next_chunk_id | ch01_sec_四_十六-二转换_theory_200 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L186–198 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、二-十六转换

将二进制数转换为等值的十六进制数称为二-十六转换。

由于 4 位二进制数恰好有 16 个状态,而把这 4 位二进制数看作一个整体时,它的进位输出又正好是逢十六进一,所以只要从低位到高位将整数部分每 4 位二进制数分为一组并代之以等值的十六进制数,同时从高位到低位将小数部分的每 4 位数分为一组并代之以等值的十六进制数,即可得到对应的十六进制数。

例如，将(01011110.10110010) $_{2}$ 化为十六进制数时可得

$$
\begin{array}{c c c c} \text {(0101} & 1 1 1 0. & 1 0 1 1 & \mathbf {0 0 1 0}) _ {2} \\ \downarrow & \downarrow & \downarrow & \downarrow \\ = (\quad 5 & \mathrm{E}. & \mathrm{B} & 2) _ {1 6} \end{array}
$$

若二进制数整数部分最高一组不足4位时，用0补足4位；小数部分最低一组不足4位时，也需用0补足4位。

---

## Chunk 15/68：`ch01_sec_四_十六-二转换_theory_200`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_四_十六-二转换_theory_200 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 四、十六-二转换 |
| section_id | ch01_sec_四_十六-二转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_二-十六转换_theory_186 |
| next_chunk_id | ch01_sec_五_八进制数与二进制数的转换_theory_210 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L200–208 |

### 正文（检索用 text_content）

第01章 数制和码制 > 四、十六-二转换

十六-二转换是指将十六进制数转换为等值的二进制数。转换时只需将十六进制数的每一位用等值的4位二进制数代替就行了。

例如，将 $(8FA.C6)_{16}$ 化为二进制数时得到

$$
\begin{array}{c c c c c} (8 & \mathrm{F} & \mathrm{A}. & \mathrm{C} & 6) _ {1 6} \\ \downarrow & \downarrow & \downarrow & \downarrow & \downarrow \\ = (\mathbf {1 0 0 0} & \mathbf {1 1 1 1} & \mathbf {1 0 1 0}. & \mathbf {1 1 0 0} & \mathbf {0 1 1 0}) _ {2} \end{array}
$$

---

## Chunk 16/68：`ch01_sec_五_八进制数与二进制数的转换_theory_210`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_五_八进制数与二进制数的转换_theory_210 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 五、八进制数与二进制数的转换 |
| section_id | ch01_sec_五_八进制数与二进制数的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_四_十六-二转换_theory_200 |
| next_chunk_id | ch01_sec_六_十六进制数与十进制数的转换_theory_230 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L210–228 |

### 正文（检索用 text_content）

第01章 数制和码制 > 五、八进制数与二进制数的转换

将二进制数转换为八进制数的二-八转换和将八进制数转换为二进制数的八-二转换，在方

法上与二-十六转换和十六-二转换的方法基本相同。

在将二进制数转换为八进制数时, 只要将二进制数的整数部分从低位到高位每 3 位分为一组并代之以等值的八进制数, 同时将小数部分从高位到低位每 3 位分为一组并代之以等值的八进制数就可以了。二进制数最高一组不足 3 位或小数部分最低一组不足 3 位时, 仍需以 0 补足 3 位。

例如,若将 $(011110.010111)_{2}$ 化为八进制数,则得到

$$
\begin{array}{c c c c} (0 1 1 & 1 1 0. & 0 1 0 & 1 1 1) _ {2} \\ \downarrow & \downarrow & \downarrow & \downarrow \\ (3 & 6. & 2 & 7) _ {8} \end{array}
$$

反之，若将八进制数转换为二进制数，则只要将八进制数的每一位代之以等值的3位二进制数即可。例如，将 $(52.43)_{8}$ 转换为二进制数时，得到

$$
\begin{array}{c c c c} (5 & 2. & 4 & 3) _ {8} \\ \downarrow & \downarrow & \downarrow & \downarrow \\ (1 0 1 & 0 1 0. & 1 0 0 & 0 1 1) _ {2} \end{array}
$$

---

## Chunk 17/68：`ch01_sec_六_十六进制数与十进制数的转换_theory_230`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_六_十六进制数与十进制数的转换_theory_230 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 六、十六进制数与十进制数的转换 |
| section_id | ch01_sec_六_十六进制数与十进制数的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_五_八进制数与二进制数的转换_theory_210 |
| next_chunk_id | ch01_sec_review_review_235 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L230–232 |

### 正文（检索用 text_content）

第01章 数制和码制 > 六、十六进制数与十进制数的转换

在将十六进制数转换为十进制数时,可根据式(1.2.5)将各位按权展开后相加求得。在将十进制数转换为十六进制数时,可以先转换为二进制数,然后再将得到的二进制数转换为等值的十六进制数。这两种转换方法上面已经讲过了。

---

## Chunk 18/68：`ch01_sec_review_review_235`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_235 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_六_十六进制数与十进制数的转换_theory_230 |
| next_chunk_id | ch01_sec_review_review_237 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L235–236 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.3.1 在十-二转换中,整数部分的转换方法和小数部分的转换方法有何不同?

---

## Chunk 19/68：`ch01_sec_review_review_237`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_237 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_235 |
| next_chunk_id | ch01_sec_review_review_239 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L237–238 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.3.2 怎样将八进制数转换为十六进制数和将十六进制数转换为八进制数？

---

## Chunk 20/68：`ch01_sec_review_review_239`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_239 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_237 |
| next_chunk_id | ch01_sec_1_4_1_theory_244 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L239–240 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.3.3 怎样才能将十进制数转换为八进制数？

---

## Chunk 21/68：`ch01_sec_1_4_1_theory_244`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_4_1_theory_244 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.4.1 二进制算术运算的特点 |
| section_id | ch01_sec_1_4_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_239 |
| next_chunk_id | ch01_sec_1_4_2_theory_258_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L244–256 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.4.1 二进制算术运算的特点

当两个二进制数码表示两个数量大小时,它们之间可以进行数值运算,这种运算称为算术运算。二进制算术运算和十进制算术运算的规则基本相同,唯一的区别在于二进制数是“逢二进一”而不是十进制数的“逢十进一”。

例如,两个二进制数 1001 和 0101 的算术运算有

$$
\begin{array}{c c} \text {加法运算} & \text {减法运算} \\ \frac {1 0 0 1}{+ 0 1 0 1} & \frac {1 0 0 1}{- 0 1 0 1} \\ \hline 1 1 1 0 & \frac {0 1 0 0}{0 1 0 0} \\ \text {乘法运算} & \text {除法运算} \\ \frac {1 0 0 1}{\times 0 1 0 1} & \frac {1 . 1 1 \cdots}{0 1 0 1} \\ \hline 1 0 0 1 & \frac {1 0 0 1}{0 1 0 1} \\ \frac {0 0 0 0}{1 0 0 1} & \frac {1 0 0 0}{0 1 0 1} \\ \frac {0 0 0 0}{0 1 0 1 1 0 1} & \frac {0 1 1 0}{0 1 0 1} \\ \hline \end{array}
$$

从上面的例子中可以看到二进制算术运算的两个特点,即二进制数的乘法运算可以通过若干次的“被乘数(或零)左移1位”和“被乘数(或零)与部分积相加”这两种操作完成;而二进制数的除法运算能通过若干次的“除数右移1位”和“从被除数或余数中减去除数”这两种操作完成。

如果我们再能设法将减法操作转化为某种形式的加法操作，那么加、减、乘、除运算就全部可以用“移位”和“相加”两种操作实现了。利用上述特点能使运算电路的结构大为简化。这也是数字电路中普遍采用二进制算术运算的重要原因之一。

---

## Chunk 22/68：`ch01_sec_1_4_2_theory_258_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_4_2_theory_258_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 |
| section_id | ch01_sec_1_4_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图1.4.1, 图1.4.2 |
| prev_chunk_id | ch01_sec_1_4_1_theory_244 |
| next_chunk_id | ch01_sec_1_4_2_theory_258_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L258–300 |

### 配图

**图1.4.1** — 说明补码运算原理的例子

![图1.4.1](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/2cb0c0ddf81e8b5bc470fd3a32324c36684a924efd467c8f23c1b109762a6408.jpg)

*视觉描述：* 十二点钟面示意补码运算：指针指10与5；逆时针10-5=5，顺时针10+7-12=5，旁注「舍弃进位」说明模12下减5等价加7。

**图1.4.2** — 4位二进制数补码运算的例子

![图1.4.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c0c573c7bd53e345165d2c6f56d8e9069fdf204e39bc16578affabae953f7729.jpg)

*视觉描述：* 4位二进制补码圆：0–15与0000–1111；示11-7=4及11+9-16=4，旁写1011+1001舍弃进位得0100。

### 正文（检索用 text_content）

第01章 数制和码制 > 1.4.2 反码、补码和补码运算

我们已经知道，在数字电路中是用逻辑电路输出的高、低电平表示二进制数的1和0的。那么数的正、负又如何表示呢？通常采用的方法是在二进制数的前面增加一位符号位。符号位为0表示这个数是正数，符号位为1表示这个数是负数。这种形式的数称为原码。

在做减法运算时,如果两个数是用原码表示的,则首先需要比较两数绝对值的大小,然后以绝对值大的一个作为被减数、绝对值小的一个作为减数,求出差值,并以绝对值大的一个数的符号作为差值的符号。不难看出,这个操作过程比较麻烦,而且需要使用数值比较电路和减法运算电路。如果能用两数的补码相加代替上述的减法运算,那么计算过程中就无需使用数值比较电路和减法运算电路了,从而使运算器的电路结构大为简化。

为了说明补码运算的原理,我们先来讨论一个生活中常见的事例。例如,你在5点钟的时候发现自己的手表停在10点上了,因而必须把表针拨回到5点。由图1.4.1可以看出,这时有两种拨法:第一种拨法是往回拨5格,10-5=5,拨回到了5点;另一种拨法是往前拨7格,10+7=17。由于表盘的最大数只有12,超过12以后的“进位”将自动消失,于是就只剩下减去12以后的余数了,即17-12=5,也将表针拨回到了5点。这个例子说明,10-5的减法运算可以用10+7的加法运算代替。因为5和7相加正好等于产生进位的模数12,所以我们称7为-5对模12的补数,也称为补码(Complement)。

图1.4.1 说明补码运算原理的例子

从这个例子中可以得出一个结论,就是在舍弃进位的条件下,减去某个数可以用加上它的补码来代替。这个结论同样适用于二进制数的运算。

图 1.4.2 给出了 4 位二进制数补码运算的一个例子。由图可见，1011-0111=0100 的减法运算，在舍弃进位的条件下，可以用 $1011+1001=0100$ 的加法运算代替。因为 4 位二进制数的进位基数是 16(10000)，所以 1001(9) 恰好是 -0111(-7) 对模 16 的补码。

图1.4.2 4位二进制数补码运算的例子

基于上述原理,对于有效数字(不包括符号位)为 n 位的二进制数 N,它的补码 $(N)_{\mathrm{COMP}}$ 表示方法为

$$
(N) _ {\mathrm{COMP}} = \left\{ \begin{array}{l l} N & (\text {当} N \text {为正数}) \\ 2 ^ {n} - N & (\text {当} N \text {为负数}) \end{array} \right.\tag{1.4.1}
$$

即正数(当符号位为0时)的补码与原码相同,负数(当符号位为1时)的补码等于 $2''-N$ 。符号位保持不变。

[图1.4.1] 说明补码运算原理的例子
[图1.4.1描述] 十二点钟面示意补码运算：指针指10与5；逆时针10-5=5，顺时针10+7-12=5，旁注「舍弃进位」说明模12下减5等价加7。
[图1.4.2] 4位二进制数补码运算的例子
[图1.4.2描述] 4位二进制补码圆：0–15与0000–1111；示11-7=4及11+9-16=4，旁写1011+1001舍弃进位得0100。

---

## Chunk 23/68：`ch01_sec_1_4_2_theory_258_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_4_2_theory_258_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 |
| section_id | ch01_sec_1_4_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_1_4_2_theory_258_p00 |
| next_chunk_id | ch01_eg1_4_1 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L258–300 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.4.2 反码、补码和补码运算

在一些国外的教材中,也将式(1.4.1)定义的补码称为“2的补码”(2's Complement)。

为了避免在求补码的过程中做减法运算,通常是先求出 N 的反码 $(N)_{\mathrm{INV}}$ ,然后在负数的反码上加 1 而得到补码。二进制 N 的反码 $(N)_{\mathrm{INV}}$ 是这样定义的

$$
(N) _ {\mathrm{INV}} = \left\{ \begin{array}{c l} N & (\text {当} N \text {为正数}) \\ (2 ^ {n} - 1) - N & (\text {当} N \text {为负数}) \end{array} \right.\tag{1.4.2}
$$

由上式可知，当 $N$ 为负数时， $N + (N)_{\mathrm{INV}} = 2^n - 1$ ，而 $2^n - 1$ 是 $n$ 位全为1的二进制数，所以只要将 $N$ 中每一位的1改为0、0改为1，就得到了 $(N)_{\mathrm{INV}}$ 。以后我们将会看到，将二进制数的每一位求反,在电路上是很容易实现的。国外的有些教材中又将式(1.4.2)定义的反码称为“1的补码”(1's Complement)。

由式(1.4.2)又可得到,当 N 为负数时, $(N)_{\mathrm{INV}}+1=2^{n}-N$ ,而由式(1.4.1)又知,当 N 为负数时, $(N)_{\mathrm{COMP}}=2^{n}-N$ ,由此得到

$$
(N) _ {\mathrm{COMP}} = (N) _ {\mathrm{INV}} + 1\tag{1.4.3}
$$

即二进制负数的补码等于它的反码加1。

---

## Chunk 24/68：`ch01_eg1_4_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_eg1_4_1 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 |
| section_id | ch01_sec_1_4_2 |
| exercise_id | — |
| example_id | 例1.4.1 |
| figure_ids | — |
| prev_chunk_id | ch01_sec_1_4_2_theory_258_p01 |
| next_chunk_id | ch01_eg1_4_2 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L301–314 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.4.2 反码、补码和补码运算

【例 1.4.1】写出带符号位二进制数 00011010(+26)、10011010(-26)、00101101(+45) 和 10101101(-45) 的反码和补码。

解：根据式（1.4.2）和式（1.4.3）得到

<table><tr><td>原码</td><td>反码</td><td>补码</td></tr><tr><td>00011010</td><td>00011010</td><td>00011010</td></tr><tr><td>10011010</td><td>11100101</td><td>11100110</td></tr><tr><td>00101101</td><td>00101101</td><td>00101101</td></tr><tr><td>10101101</td><td>11010010</td><td>11010011</td></tr></table>

表 1.4.1 是带符号位的 3 位二进制数原码、反码和补码的对照表。其中规定用 1000 作为 -8 的补码，而不用来表示 -0。

表 1.4.1 原码、反码、补码对照表

<table><tr><td rowspan="2">十进制数</td><td colspan="3">二进制数</td></tr><tr><td>原码(带符号数)</td><td>反码</td><td>补码</td></tr><tr><td>+7</td><td>0111</td><td>0111</td><td>0111</td></tr><tr><td>+6</td><td>0110</td><td>0110</td><td>0110</td></tr><tr><td>+5</td><td>0101</td><td>0101</td><td>0101</td></tr><tr><td>+4</td><td>0100</td><td>0100</td><td>0100</td></tr><tr><td>+3</td><td>0011</td><td>0011</td><td>0011</td></tr><tr><td>+2</td><td>0010</td><td>0010</td><td>0010</td></tr><tr><td>+1</td><td>0001</td><td>0001</td><td>0001</td></tr><tr><td>+0</td><td>0000</td><td>0000</td><td>0000</td></tr><tr><td>-1</td><td>1001</td><td>1110</td><td>1111</td></tr><tr><td>-2</td><td>1010</td><td>1101</td><td>1110</td></tr><tr><td>-3</td><td>1011</td><td>1100</td><td>1101</td></tr><tr><td>-4</td><td>1100</td><td>1011</td><td>1100</td></tr><tr><td>-5</td><td>1101</td><td>1010</td><td>1011</td></tr><tr><td>-6</td><td>1110</td><td>1001</td><td>1010</td></tr><tr><td>-7</td><td>1111</td><td>1000</td><td>1001</td></tr><tr><td>-8</td><td>1000</td><td>1111</td><td>1000</td></tr></table>

下面再来讨论两个用补码表示的二进制数相加时，和的符号位如何得到。为此，我们在例1.4.2中列举出了两数相加时的四种情况。

---

## Chunk 25/68：`ch01_eg1_4_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_eg1_4_2 |
| block_type | example |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 1.4.2 反码、补码和补码运算 |
| section_id | ch01_sec_1_4_2 |
| exercise_id | — |
| example_id | 例1.4.2 |
| figure_ids | 图1.4.2 |
| prev_chunk_id | ch01_eg1_4_1 |
| next_chunk_id | ch01_sec_review_review_335 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L315–332 |

### 配图

**图1.4.2** — 4位二进制数补码运算的例子

![图1.4.2](../../../../../课本/课本加习题册/markdown_云端解析/按章节拆分/images/c0c573c7bd53e345165d2c6f56d8e9069fdf204e39bc16578affabae953f7729.jpg)

*视觉描述：* 4位二进制补码圆：0–15与0000–1111；示11-7=4及11+9-16=4，旁写1011+1001舍弃进位得0100。

### 正文（检索用 text_content）

第01章 数制和码制 > 1.4.2 反码、补码和补码运算

【例 1.4.2】用二进制补码运算求出 $13+10$ 、 $13-10$ 、 $-13+10$ 和 $-13-10$ 。

解：由于 $13+10$ 和 -13-10 的绝对值为 23，所以必须用有效数字为 5 位的二进制数才能表示，再加上一位符号位，就得到 6 位的二进制补码。

由式(1.4.1)和式(1.4.3)可知，+13的二进制补码应为001101（最高位为符号位），-13的二进制补码为110011，+10的二进制补码为001010，-10的二进制补码为110110。计算结果分别为

$$
\begin{array}{c c c c c} + 1 3 & \mathbf {0} & \mathbf {0 1 1 0 1} & + 1 3 & \mathbf {0} & \mathbf {0 1 1 0 1} \\ + 1 0 & \mathbf {0} & \mathbf {0 1 0 1 0} & - 1 0 & \mathbf {1} & \mathbf {1 0 1 1 0} \\ \hline + 2 3 & \mathbf {0} & \mathbf {1 0 1 1 1} & + 3 & (\mathbf {1}) \mathbf {0} & \mathbf {0 0 0 1 1} \end{array}
$$

$$
\begin{array}{c c c} - 1 3 & 1 & 1 0 0 1 1 \\ + 1 0 & 0 & 0 1 0 1 0 \\ \hline - 3 & \frac {1}{1} & 1 1 1 0 1 \end{array} \quad \begin{array}{c c c} - 1 3 & 1 & 1 0 0 1 1 \\ - 1 0 & \frac {1}{1} & 1 0 1 1 0 \\ \hline - 2 3 & (1) \frac {1}{1} & 0 1 0 0 1 \end{array}
$$

从上面的例子中可以看出,若将两个加数的符号位和来自最高有效数字位的进位相加,得到的结果(舍弃产生的进位)就是和的符号。这个道理仍然可以用图 1.4.2 所示的图形加以说明。

需要强调指出,在两个同符号数相加时,它们的绝对值之和不可超过有效数字位所能表示的最大值,否则会得出错误的计算结果。

[图1.4.2] 4位二进制数补码运算的例子
[图1.4.2描述] 4位二进制补码圆：0–15与0000–1111；示11-7=4及11+9-16=4，旁写1011+1001舍弃进位得0100。

---

## Chunk 26/68：`ch01_sec_review_review_335`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_335 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_eg1_4_2 |
| next_chunk_id | ch01_sec_review_review_337 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L335–336 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.4.1 二进制正、负数的原码、反码和补码三者之间是什么关系？

---

## Chunk 27/68：`ch01_sec_review_review_337`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_337 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_335 |
| next_chunk_id | ch01_sec_review_review_339 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L337–338 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.4.2 为什么两个二进制数的补码相加时,和的符号位等于两数的符号位与来自最高有效数字位的进位相加的结果(舍弃产生的进位)?

---

## Chunk 28/68：`ch01_sec_review_review_339`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_339 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_337 |
| next_chunk_id | ch01_sec_一_十进制代码_theory_344_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L339–340 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.4.3 如何求二进制数补码对应的原码？

---

## Chunk 29/68：`ch01_sec_一_十进制代码_theory_344_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_十进制代码_theory_344_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 一、十进制代码 |
| section_id | ch01_sec_一_十进制代码 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_339 |
| next_chunk_id | ch01_sec_一_十进制代码_theory_344_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L344–366 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、十进制代码

为了用二进制代码表示十进制数的0\~9这十个状态，二进制代码至少应当有4位。4位二进制代码一共有十六个（0000\~1111），取其中哪十个以及如何与0\~9相对应，有许多种方案。表1.5.1中列出了常见的几种十进制代码，它们的编码规则各不相同。

表 1.5.1 几种常见的十进制代码

---

## Chunk 30/68：`ch01_sec_一_十进制代码_theory_344_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_十进制代码_theory_344_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 一、十进制代码 |
| section_id | ch01_sec_一_十进制代码 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_十进制代码_theory_344_p00 |
| next_chunk_id | ch01_sec_一_十进制代码_theory_344_p02 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L344–366 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、十进制代码

<table><tr><td>十进制数\编码种类</td><td>8421码(BCD代码)</td><td>余3码</td><td>2421码</td><td>5211码</td><td>余3循环码</td></tr><tr><td>0</td><td>0 0 0 0</td><td>0 0 1 1</td><td>0 0 0 0</td><td>0 0 0 0</td><td>0 0 1 0</td></tr><tr><td>1</td><td>0 0 0 1</td><td>0 1 0 0</td><td>0 0 0 1</td><td>0 0 0 1</td><td>0 1 1 0</td></tr><tr><td>2</td><td>0 0 1 0</td><td>0 1 0 1</td><td>0 0 1 0</td><td>0 1 0 0</td><td>0 1 1 1</td></tr><tr><td>3</td><td>0 0 1 1</td><td>0 1 1 0</td><td>0 0 1 1</td><td>0 1 0 1</td><td>0 1 0 1</td></tr><tr><td>4</td><td>0 1 0 0</td><td>0 1 1 1</td><td>0 1 0 0</td><td>0 1 1 1</td><td>0 1 0 0</td></tr><tr><td>5</td><td>0 1 0 1</td><td>1 0 0 0</td><td>1 0 1 1</td><td>1 0 0 0</td><td>1 1 0 0</td></tr><tr><td>6</td><td>0 1 1 0</td><td>1 0 0 1</td><td>1 1 0 0</td><td>1 0 0 1</td><td>1 1 0 1</td></tr><tr><td>7</td><td>0 1 1 1</td><td>1 0 1 0</td><td>1 1 0 1</td><td>1 1 0 0</td><td>1 1 1 1</td></tr><tr><td>8</td><td>1 0 0 0</td><td>1 0 1 1</td><td>1 1 1 0</td><td>1 1 0 1</td><td>1 1 1 0</td></tr><tr><td>9</td><td>1 0 0 1</td><td>1 1 0 0</td><td>1 1 1 1</td><td>1 1 1 1</td><td>1 0 1 0</td></tr><tr><td>权</td><td>8 4 2 1</td><td></td><td>2 4 2 1</td><td>5 2 1 1</td><td></td></tr></table>

---

## Chunk 31/68：`ch01_sec_一_十进制代码_theory_344_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_十进制代码_theory_344_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 一、十进制代码 |
| section_id | ch01_sec_一_十进制代码 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_十进制代码_theory_344_p01 |
| next_chunk_id | ch01_sec_二_格雷码_theory_368_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L344–366 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、十进制代码

8421 码又称 BCD(Binary Coded Decimal) 码, 是十进制代码中最常用的一种。在这种编码方式中, 每一位二值代码的 1 都代表一个固定数值, 将每一位的 1 代表的十进制数加起来, 得到的结果就是它所代表的十进制数码。由于代码中从左到右每一位的 1 分别表示 8、4、2、1, 所以将这种代码称为 8421 码。每一位的 1 代表的十进制数称为这一位的权。8421 码中每一位的权是固定不变的, 它属于恒权代码。

余 3 码的编码规则与 8421 码不同, 如果把每一个余 3 码看作 4 位二进制数, 则它的数值要比它所表示的十进制数码多 3, 故而将这种代码称为余 3 码。

如果将两个余3码相加,所得的和将比十进制数和所对应的二进制数多6。因此,在用余3码做十进制加法运算时,若两数之和为10,正好等于二进制数的16,于是便从高位自动产生进位信号。

此外，从表1.5.1中还可以看出，0和9、1和8、2和7、3和6、4和5的余3码互为反码，这对于求取对10的补码是很方便的。

余 3 码不是恒权代码。如果试图将每个代码视为二进制数，并使它等效的十进制数与所表示的代码相等，那么代码中每一位的 1 所代表的十进制数在各个代码中不能是固定的。

2421 码是一种恒权代码, 它的 0 和 9、1 和 8、2 和 7、3 和 6、4 和 5 也互为反码, 这个特点和余 3 码相仿。

5211码是另一种恒权代码。待学了第六章中计数器的分频作用后可以发现，如果按8421码接成十进制计数器，则连续输入计数脉冲时，4个触发器输出脉冲对于计数脉冲的分频比从低位到高位依次为 $5:2:1:1$ 。可见，5211码每一位的权正好与8421码十进制计数器4个触发器输出脉冲的分频比相对应。这种对应关系在构成某些数字系统时很有用。

余 3 循环码是一种变权码,每一位的 1 在不同代码中并不代表固定的数值。它的主要特点是相邻的两个代码之间仅有一位的状态不同。

---

## Chunk 32/68：`ch01_sec_二_格雷码_theory_368_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_格雷码_theory_368_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、格雷码 |
| section_id | ch01_sec_二_格雷码 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_十进制代码_theory_344_p02 |
| next_chunk_id | ch01_sec_二_格雷码_theory_368_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L368–378 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、格雷码

格雷码(Gray Code)又称循环码。从表1.5.2的4位格雷码编码表中可以看出格雷码的构成方法,这就是每一位的状态变化都按一定的顺序循环。如果从0000开始,最右边一位的状态按0110顺序循环变化,右边第二位的状态按00111100顺序循环变化,右边第三位按0000111111110000顺序循环变化。可见,自右向左,每一位状态循环中连续的0、1数目增加一倍。由于4位格雷码只有16个,所以最左边一位的状态只有半个循环,即0000000011111111。按照上述原则,我们就很容易得到更多位数的格雷码。

与普通的二进制代码相比,格雷码的最大优点就在于当它按照表1.5.2的编码顺序依次变化时,相邻两个代码之间只有一位发生变化。这样在代码转换的过程中就不会产生过渡“噪声”。而在普通二进制代码的转换过程中,则有时会产生过渡噪声。例如,第四行的二进制代码0011转换为第五行的0100过程中,如果最右边一位的变化比其他两位的变化慢,就会在一个极短的瞬间出现0101状态,这个状态将成为转换过程中出现的噪声。而在第四行的格雷码0010向第五行的0110转换过程中则不会出现过渡噪声。这种过渡噪声在有些情况下甚至会影响电路的正常工作,这时就必须采取措施加以避免。在第4.9节中我们还将进一步讨论这个问题。

表 1.5.2 4 位格雷码与二进制代码的比较

---

## Chunk 33/68：`ch01_sec_二_格雷码_theory_368_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_格雷码_theory_368_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 二、格雷码 |
| section_id | ch01_sec_二_格雷码 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_格雷码_theory_368_p00 |
| next_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p00 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L368–378 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、格雷码

<table><tr><td>编码顺序</td><td>二进制代码</td><td>格雷码</td></tr><tr><td>0</td><td>0000</td><td>0000</td></tr><tr><td>1</td><td>0001</td><td>0001</td></tr><tr><td>2</td><td>0010</td><td>0011</td></tr><tr><td>3</td><td>0011</td><td>0010</td></tr><tr><td>4</td><td>0100</td><td>0110</td></tr><tr><td>5</td><td>0101</td><td>0111</td></tr><tr><td>6</td><td>0110</td><td>0101</td></tr><tr><td>7</td><td>0111</td><td>0100</td></tr><tr><td>8</td><td>1000</td><td>1100</td></tr><tr><td>9</td><td>1001</td><td>1101</td></tr><tr><td>10</td><td>1010</td><td>1111</td></tr><tr><td>11</td><td>1011</td><td>1110</td></tr><tr><td>12</td><td>1100</td><td>1010</td></tr><tr><td>13</td><td>1101</td><td>1011</td></tr><tr><td>14</td><td>1110</td><td>1001</td></tr><tr><td>15</td><td>1111</td><td>1000</td></tr></table>

十进制代码中的余3循环码就是取4位格雷码中的十个代码组成的，它仍然具有格雷码的优点，即两个相邻代码之间仅有一位不同。

---

## Chunk 34/68：`ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p00 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、美国信息交换标准代码(ASCII) |
| section_id | ch01_sec_三_美国信息交换标准代码_ASCII |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_格雷码_theory_368_p01 |
| next_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p01 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L380–392 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、美国信息交换标准代码(ASCII)

美国信息交换标准代码(American Standard Code for Information Interchange,简称ASCII码)是由美国国家标准化协会(ANSI)制定的一种信息代码,广泛地用于计算机和通信领域中。ASCII码已经由国际标准化组织(ISO)认定为国际通用的标准代码。

ASCII 码是一组 7 位二进制代码 $(b_{7}b_{6}b_{5}b_{4}b_{3}b_{2}b_{1})$ ，共 128 个，其中包括表示 0\~9 的十个代码，表示大、小写英文字母的 52 个代码，32 个表示各种符号的代码以及 34 个控制码。表 1.5.3 是 ASCII 码的编码表，每个控制码在计算机操作中的含义列于表 1.5.4 中。

表 1.5.3 美国信息交换标准代码 (ASCII 码)

---

## Chunk 35/68：`ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p01 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、美国信息交换标准代码(ASCII) |
| section_id | ch01_sec_三_美国信息交换标准代码_ASCII |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p00 |
| next_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p02 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L380–392 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、美国信息交换标准代码(ASCII)

<table><tr><td rowspan="2"> $b_4b_3b_2b_1$ </td><td colspan="8"> $b_7b_6b_5$ </td></tr><tr><td>000</td><td>001</td><td>010</td><td>011</td><td>100</td><td>101</td><td>110</td><td>111</td></tr><tr><td>0000</td><td>NUL</td><td>DLE</td><td>SP</td><td>0</td><td>@</td><td>P</td><td>、</td><td>p</td></tr><tr><td>0001</td><td>SOH</td><td>DC1</td><td>!</td><td>1</td><td>A</td><td>Q</td><td>a</td><td>q</td></tr><tr><td>0010</td><td>STX</td><td>DC2</td><td>“</td><td>2</td><td>B</td><td>R</td><td>b</td><td>r</td></tr><tr><td>0011</td><td>ETX</td><td>DC3</td><td>#</td><td>3</td><td>C</td><td>S</td><td>c</td><td>s</td></tr><tr><td>0100</td><td>EOT</td><td>DC4</td><td>$</td><td>4</td><td>D</td><td>T</td><td>d</td><td>t</td></tr><tr><td>0101</td><td>ENQ</td><td>NAK</td><td>%</td><td>5</td><td>E</td><td>U</td><td>e</td><td>u</td></tr><tr><td>0110</td><td>ACK</td><td>SYN</td><td>&</td><td>6</td><td>F</td><td>V</td><td>f</td><td>v</td></tr><tr><td>0111</td><td>BEL</td><td>ETB</td><td>‘</td><td>7</td><td>G</td><td>W</td><td>g</td><td>w</td></tr><tr><td>1000</td><td>BS</td><td>CAN</td><td>(</td><td>8</td><td>H</td><td>X</td><td>h</td><td>x</td></tr><tr><td>1001</td><td>HT</td><td>EM</td><td>)</td><td>9

---

## Chunk 36/68：`ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p02 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、美国信息交换标准代码(ASCII) |
| section_id | ch01_sec_三_美国信息交换标准代码_ASCII |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p01 |
| next_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p03 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L380–392 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、美国信息交换标准代码(ASCII)

</td><td>I</td><td>Y</td><td>i</td><td>y</td></tr><tr><td>1010</td><td>LF</td><td>SUB</td><td>*</td><td>:</td><td>J</td><td>Z</td><td>j</td><td>z</td></tr><tr><td>1011</td><td>VT</td><td>ESC</td><td>+</td><td>;</td><td>K</td><td>[</td><td>k</td><td>{</td></tr><tr><td>1100</td><td>FF</td><td>FS</td><td>,</td><td><</td><td>L</td><td>\</td><td>l</td><td>|</td></tr><tr><td>1101</td><td>CR</td><td>GS</td><td>-</td><td>=</td><td>M</td><td>]</td><td>m</td><td>}</td></tr><tr><td>1110</td><td>SO</td><td>RS</td><td>.</td><td>></td><td>N</td><td>^</td><td>n</td><td>~</td></tr><tr><td>1111</td><td>SI</td><td>US</td><td>/</td><td>?</td><td>O</td><td>-</td><td>o</td><td>DEL</td></tr></table>

表 1.5.4 ASCII 码中控制码的含义

---

## Chunk 37/68：`ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p03 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、美国信息交换标准代码(ASCII) |
| section_id | ch01_sec_三_美国信息交换标准代码_ASCII |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p02 |
| next_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p04 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L380–392 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、美国信息交换标准代码(ASCII)

<table><tr><td>代码</td><td colspan="2">含义</td></tr><tr><td>NUL</td><td>Null</td><td>空白,无效</td></tr><tr><td>SOH</td><td>Start of heading</td><td>标题开始</td></tr><tr><td>STX</td><td>Start of text</td><td>正文开始</td></tr><tr><td>ETX</td><td>End of text</td><td>文本结束</td></tr><tr><td>EOT</td><td>End of transmission</td><td>传输结束</td></tr><tr><td>ENQ</td><td>Enquiry</td><td>询问</td></tr><tr><td>ACK</td><td>Acknowledge</td><td>承认</td></tr><tr><td>BEL</td><td>Bell</td><td>报警</td></tr><tr><td>BS</td><td>Backspace</td><td>退格</td></tr><tr><td>HT</td><td>Horizontal tab</td><td>横向制表</td></tr><tr><td>LF</td><td>Line feed</td><td>换行</td></tr><tr><td>VT</td><td>Vertical tab</td><td>垂直制表</td></tr><tr><td>FF</td><td>Form feed</td><td>换页</td></tr><tr><td>CR</td><td>Carriage return</td><td>回车</td></tr><tr><td>SO</td><td>Shift out</td><td>移出</td></tr><tr><td>SI</td><td>Shift in</td><td>移入</td></tr><tr><td>DLE</td><td>Date Link escape</td><td>数据通信换码</td></tr><tr><td>DC1</td><td>Device control 1</td><td>设备控制1</td></tr><tr><td>DC2</td><td>Device control 2</td><td>设备控制2</td></tr><tr><td>DC3</td><td>Device control 3</td><td>设备控制3</td></tr><tr><td>DC4</td><td>Device control 4</td><td>设备控制4</td></tr><tr><td>NAK</td>

---

## Chunk 38/68：`ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p04 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > 三、美国信息交换标准代码(ASCII) |
| section_id | ch01_sec_三_美国信息交换标准代码_ASCII |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p03 |
| next_chunk_id | ch01_sec_review_review_395 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L380–392 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、美国信息交换标准代码(ASCII)

<td>Negative acknowledge</td><td>否定</td></tr><tr><td>SYN</td><td>Synchronous idle</td><td>空转同步</td></tr><tr><td>ETB</td><td>End of transmission block</td><td>信息块传输结束</td></tr><tr><td>CAN</td><td>Cancel</td><td>作废</td></tr><tr><td>EM</td><td>End of medium</td><td>媒体用毕</td></tr><tr><td>SUB</td><td>Substitute</td><td>代替,置换</td></tr><tr><td>ESC</td><td>Escape</td><td>扩展</td></tr><tr><td>FS</td><td>File separator</td><td>文件分隔</td></tr><tr><td>GS</td><td>Group separator</td><td>组分隔</td></tr><tr><td>RS</td><td>Record separator</td><td>记录分隔</td></tr><tr><td>US</td><td>Unit separator</td><td>单元分隔</td></tr><tr><td>SP</td><td>Space</td><td>空格</td></tr><tr><td>DEL</td><td>Delete</td><td>删除</td></tr></table>

---

## Chunk 39/68：`ch01_sec_review_review_395`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_395 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_三_美国信息交换标准代码_ASCII_theory_380_p04 |
| next_chunk_id | ch01_sec_review_review_397 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L395–396 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.5.1 8421 码、2421 码、5211 码、余 3 码和余 3 循环码在编码规则上各有何特点？

---

## Chunk 40/68：`ch01_sec_review_review_397`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_397 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_395 |
| next_chunk_id | ch01_sec_review_review_399 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L397–398 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.5.2 你能写出3位和5位格雷码的顺序编码吗？

---

## Chunk 41/68：`ch01_sec_review_review_399`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_review_review_399 |
| block_type | review |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > review 复习思考题 |
| section_id | ch01_sec_review |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_397 |
| next_chunk_id | ch01_sec_summary_end_theory_402 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L399–400 |

### 正文（检索用 text_content）

第01章 数制和码制 > review 复习思考题

R1.5.3 你能用 ASCII 代码写出“Welcome!”吗?

---

## Chunk 42/68：`ch01_sec_summary_end_theory_402`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_summary_end_theory_402 |
| block_type | theory |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 |
| section_id | ch01_sec_summary_end |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_review_review_399 |
| next_chunk_id | ch01_ex1_1 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L402–410 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结

不同的数码既可以用来表示不同数量的大小,又可以用来表示不同的事物。

在用数码表示数量的大小时,采用的各种计数进位制规则称为数制。常用的数制有十进制、二进制、八进制和十六进制几种。各种进制所表示的数值可以按照本章介绍的方法互相转换。

由于数字电路的基本运算都采用二进制运算,所以这一章里还比较详细地介绍了二进制数的符号在数字电路中的表示方法,原码、反码和补码的概念,以及采用补码进行带符号数加法运算的原理。

在用数码表示不同的事物时,这些数码已没有数量大小的含义,所以将它们称为代码。本章中所列举的十进制代码、格雷码、ASCII码是几种常见的通用代码。此外,我们完全可以根据自己的需要,自行编制专用的代码。

---

## Chunk 43/68：`ch01_ex1_1`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_1 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.1 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_summary_end_theory_402 |
| next_chunk_id | ch01_ex1_2 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L413–414 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.1 题干】
[题 1.1] 为了将 600 份文件顺序编码, 如果采用二进制代码, 最少需要用几位? 如果改用八进制或十六进制代码, 则最少各需要用几位?

【题1.1 解答】
【题 1.1】为了将 600 份文件顺序编号, 如果采用二进制代码, 最少需要用几位? 如果改用八进制或十六进制代码, 则最少各需要用几位?

解：因为9位二进制代码共有 $2^{9}=512$ 个码，不够用；而10位二进制代码共有 $2^{10}=1024$ 个码，大于600，故采用二进制代码时最少需要十位。

若将 10 位二进制代码转换为八进制和十六进制代码,则各需要用 4 位和 3 位。因此,如果改用八进制代码,则需要用 4 位;如果改用十六进制代码,则 3 位就够了。

---

## Chunk 44/68：`ch01_ex1_2`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_2 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.2 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_1 |
| next_chunk_id | ch01_ex1_3 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L415–419 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.2 题干】
[题1.2] 将下列二进制整数转换为等值的十进制数。
(1) $(01101)_{2}$ ; (2) $(10100)_{2}$ ; (3) $(10010111)_{2}$ ; (4) $(1101101)_{2}$ 

（“二-十转换”）

【题1.2 解答】
【题 1.2】将下列二进制整数转换为等值的十进制数。

(1) $(01101)_{2}$ ;(2) $(10100)_{2}$ ;(3) $(10010111)_{2}$ ;(4) $(1101101)_{2}$ 。

解：

(1) $(01101)_{2}=0\times2^{4}+1\times2^{3}+1\times2^{2}+0\times2^{1}+1\times2^{0}=13$

(2) $(10100)_{2}=1\times2^{4}+0\times2^{3}+1\times2^{2}+0\times2^{1}+0\times2^{0}=20$

$$
\begin{array}{r l} (3) \quad (\mathbf {1 0 0 1 0 1 1 1}) _ {2} & = \mathbf {1} \times 2 ^ {7} + \mathbf {0} \times 2 ^ {6} + \mathbf {0} \times 2 ^ {5} + \mathbf {1} \times 2 ^ {4} + \mathbf {0} \times 2 ^ {3} + \mathbf {1} \times 2 ^ {2} + \mathbf {1} \times 2 ^ {1} + \mathbf {1} \times 2 ^ {0} \\ & = 1 5 1 \end{array}
$$

$$
\begin{array}{r l} (4) \quad (1 1 0 1 1 0 1) _ {2} & = 1 \times 2 ^ {6} + 1 \times 2 ^ {5} + 0 \times 2 ^ {4} + 1 \times 2 ^ {3} + 1 \times 2 ^ {2} + 0 \times 2 ^ {1} + 1 \times 2 ^ {0} \\ & = 1 0 9 \end{array}
$$

---

## Chunk 45/68：`ch01_ex1_3`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_3 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.3 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_2 |
| next_chunk_id | ch01_ex1_4 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L420–422 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.3 题干】
[题1.3] 将下列二进制小数转换为等值的十进制数。
(1) $(0.1001)_{2}$ ; (2) $(0.0111)_{2}$ ; (3) $(0.101101)_{2}$ ; (4) $(0.001111)_{2}$ 。

【题1.3 解答】
【题 1.3】将下列二进制小数转换为等值的十进制数。

(1) $(0.1001)_{2}$ ;(2) $(0.0111)_{2}$ ;(3) $(0.101101)_{2}$ ;(4) $(0.001111)_{2}$ 。

解：

(1) $(0.1001)_2 = 1 \times 2^{-1} + 0 \times 2^{-2} + 0 \times 2^{-3} + 1 \times 2^{-4} = 0.5625$

(2) $(0.0111)_2 = 0 \times 2^{-1} + 1 \times 2^{-2} + 1 \times 2^{-3} + 1 \times 2^{-4} = 0.4375$

$$
\begin{array}{r l} (3) \quad (\mathbf {0 . 1 0 1 1 0 1}) _ {2} & = \mathbf {1} \times 2 ^ {- 1} + \mathbf {0} \times 2 ^ {- 2} + \mathbf {1} \times 2 ^ {- 3} + \mathbf {1} \times 2 ^ {- 4} + \mathbf {0} \times 2 ^ {- 5} + \mathbf {1} \times 2 ^ {- 6} \\ & = 0. 7 0 3 1 2 5 \end{array}
$$

$$
\begin{array}{r l} (4) \quad (\mathbf {0 . 0 0 1 1 1 1}) _ {2} & = \mathbf {0} \times 2 ^ {- 1} + \mathbf {0} \times 2 ^ {- 2} + \mathbf {1} \times 2 ^ {- 3} + \mathbf {1} \times 2 ^ {- 4} + \mathbf {1} \times 2 ^ {- 5} + \mathbf {1} \times 2 ^ {- 6} \\ & = 0. 2 3 4 3 7 5 \end{array}
$$

---

## Chunk 46/68：`ch01_ex1_4`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_4 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.4 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_3 |
| next_chunk_id | ch01_ex1_5 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L423–425 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.4 题干】
[题1.4] 将下列二进制数转换为等值的十进制数。
(1) $(101.011)_{2}$ ; (2) $(110.101)_{2}$ ; (3) $(1111.1111)_{2}$ ; (4) $(1001.0101)_{2}$ 。

【题1.4 解答】
【题 1.4】将下列二进制数转换为等值的十进制数。

(1) $(101.011)_{2}$ ;(2) $(110.101)_{2}$ ;(3) $(1111.1111)_{2}$ ;(4) $(1001.0101)_{2}$ 。

解：

$$
\begin{array}{r l} (1) & (\mathbf {1 0 1 . 0 1 1}) _ {2} = \mathbf {1} \times 2 ^ {2} + \mathbf {0} \times 2 ^ {1} + \mathbf {1} \times 2 ^ {0} + \mathbf {0} \times 2 ^ {- 1} + \mathbf {1} \times 2 ^ {- 2} + \mathbf {1} \times 2 ^ {- 3} \\ & = 5. 3 7 5 \end{array}
$$

$$
\begin{array}{r l} (3) \quad (1 1 1 1. 1 1 1 1) _ {2} & = 1 \times 2 ^ {3} + 1 \times 2 ^ {2} + 1 \times 2 ^ {1} + 1 \times 2 ^ {0} + 1 \times 2 ^ {- 1} + 1 \times 2 ^ {- 2} + 1 \times 2 ^ {- 3} + 1 \times 2 ^ {- 4} \\ & = 1 5. 9 3 7 5 \end{array}
$$

$$
(4) (1 0 0 1. 0 1 0 1) _ {2} = 1 \times 2 ^ {3} + 0 \times 2 ^ {2} + 0 \times 2 ^ {1} + 1 \times 2 ^ {0} + 0 \times 2 ^ {- 1} + 1 \times 2 ^ {- 2} + 0 \times 2 ^ {- 3} + 1 \times 2 ^ {- 4}
$$

=9.3125

---

## Chunk 47/68：`ch01_ex1_5`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_5 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.5 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_4 |
| next_chunk_id | ch01_ex1_6 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L426–428 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.5 题干】
[题1.5] 将下列二进制数转换为等值的八进制数和十六进制数。
(1) $(1110.0111)_{2}$ ; (2) $(1001.1101)_{2}$ ; (3) $(0110.1001)_{2}$ ; (4) $(101100.110011)_{2}$ 。

【题1.5 解答】
【题 1.5】将下列二进制数转换为等值的八进制数和十六进制数。

(1) $(1110.0111)_{2}$ ;(2) $(1001.1101)_{2}$ ;(3) $(0110.1001)_{2}$ ;

(4) $(101100.110011)_{2}$

解：

(1) 将 $(1110.0111)_{2}$ 转换为八进制和十六进制数得到

(1110.0111) $_{2}$ ↓

( 001 110. 011 100 ) $_{2}$ ↓ ↓ ↓ ↓

( 1 6. 3 4 ) $_{8}$ (1110.0111) $_{2}$ ↓ ↓
( E. 7 ) $_{16}$

(2) 将 $(1001.1101)_{2}$ 转换为八进制和十六进制数得到

$$
\begin{array}{c c c c c} (1 0 0 1. 1 1 0 1) _ {2} & & & & \\ & \downarrow & & & \\ (\quad 0 0 1 \quad 0 0 1. \quad 1 1 0 \quad 1 0 0 \quad) _ {2} & & & & \\ & \downarrow & \downarrow & \downarrow & \downarrow \\ (\quad 1 \quad 1. \quad 6 \quad 4 \quad) _ {8} & & & & \end{array}
$$

(1001.1101) $_{2}$ ↓ ↓
(9. D ) $_{16}$

(3) 将 $(0110.1001)_2$ 转换为八进制和十六进制数得到 $\begin{array}{c}\text{(0110.1001)}_2 \\ \downarrow \\ \text{(110.1001)}_2 \\ \downarrow \\ \text{(6.9)}_{16} \\ \text{(6.44)}_8\end{array}$

(4) 将 $(101100.110011)_2$ 转换为八进制和十六进制数得到 $(101100.110011)_2$ $(101100.110011)_2$ ↓ ↓
( 101 100. 110 011 ) $_2$ ( 0010 1100. 1100 1100 ) $_2$ ↓ ↓ ↓ ↓ ↓ ↓ ↓
( 5 4. 6 3 ) $_8$ ( 2 C. C C ) $_{16}$

---

## Chunk 48/68：`ch01_ex1_6`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_6 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.6 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_5 |
| next_chunk_id | ch01_ex1_7 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L429–431 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.6 题干】
[题1.6] 将下列十六进制数转换为等值的二进制数。  
(1) $(8\mathrm{C})_{16}$ ; (2) $(3\mathrm{D.BE})_{16}$ ; (3) $(8\mathrm{F.FF})_{16}$ ; (4) $(10.00)_{16}$

【题1.6 解答】
【题 1.6】 将下列十六进制数转换为等值的二进制数。

(1) $(8\mathrm{C})_{16}$ ; (2) $(3\mathrm{D.BE})_{16}$ ; (3) $(8\mathrm{F.FF})_{16}$ ; (4) $(10.00)_{16}$

解：

(1) 将 $(8\mathrm{C})_{16}$ 中每一位十六进制数代之以等值的 4 位二进制数, 得到
\(\begin{array}{ccc}
( & 8 & C & )\_{16} \\
& \downarrow & \downarrow \\
( & 1000 & 1100 & )\_{2}
\end{array}\)

(2) 将 $(3D.BE)_{16}$ 中的每一位十六进制数代之以等值的 4 位二进制数, 得到
(3 D. B E ) $_{16}$ ↓ ↓ ↓ ↓
(0011 1101. 1011 1110 ) $_{2}$

(3) 将 $(8F.FF)_{16}$ 中的每一位十六进制数代之以等值的4位二进制数, 得到
(8 F. F F ) $_{16}$ ↓ ↓ ↓ ↓
(1000 1111. 1111 1111 ) $_{2}$

(4) 将 $(10.00)_{16}$ 中的每一位十六进制数代之以等值的 4 位二进制数, 得到
(100) $_{16}$ ↓↓↓↓

(0001 0000. 0000 0000 ) $_{2}$

---

## Chunk 49/68：`ch01_ex1_7`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_7 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.7 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_6 |
| next_chunk_id | ch01_ex1_8 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L432–434 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.7 题干】
[题1.7] 将下列十进制数转换为等值的二进制数和十六进制数。
(1) $(17)_{10}$ ; (2) $(127)_{10}$ ; (3) $(79)_{10}$ ; (4) $(255)_{10}$ 。

【题1.7 解答】
【题 1.7】将下列十进制数转换为等值的二进制数和十六进制数。

$$
(1) (1 7) _ {1 0}; (2) (1 2 7) _ {1 0}; (3) (7 9) _ {1 0}; (4) (2 5 5) _ {1 0} \circ
$$

解：

(1)

$$
\begin{array}{r l} & 2 \boxed {1 7} \dots \dots \text {余数} = \mathbf {1} = k _ {0} \\ & 2 \boxed {8} \dots \dots \text {余数} = \mathbf {0} = k _ {1} \\ & 2 \boxed {4} \dots \dots \text {余数} = \mathbf {0} = k _ {2} \\ & 2 \boxed {2} \dots \dots \text {余数} = \mathbf {0} = k _ {3} \\ & 2 \boxed {1} \dots \dots \text {余数} = \mathbf {1} = k _ {4} \\ & 0 \end{array}
$$

故得到(17) $_{10}$ =(10001) $_{2}$ 。

$$
\begin{array}{r l} \left(\mathbf {1 0 0 0 1}\right) _ {2} & = \left(\mathbf {0 0 0 1} \quad \mathbf {0 0 0 1}\right) _ {2} \\ & \downarrow \quad \downarrow \\ & = (\quad 1 \quad 1 \quad) _ {1 6} \end{array}
$$

(2)

$$
\begin{array}{r l} {2} & {\underline {{1 2 7}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {0}} \\ {2} & {\underline {{6 3}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {1}} \\ {2} & {\underline {{3 1}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {2}} \\ {2} & {\underline {{1 5}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {3}} \\ {2} & {\underline {{7}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {4}} \\ {2} & {\underline {{3}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {5}} \\ {2} & {\underline {{1}} \quad \dots \dots \text {余数} = \mathbf {1} = k _ {6}} \\ & {\underline {{0}}} \end{array}
$$

故得到 $(127)_{10}=(1111111)_{2}$ 。

$$
\begin{array}{r l} \left(\mathbf {1 1 1 1 1 1 1}\right) _ {2} & = \left(\mathbf {0 1 1 1} \quad \mathbf {1 1 1 1}\right) _ {2} \\ & \downarrow \quad \downarrow \\ & = (\quad 7 \quad \mathrm{F}) _ {1 6} \end{array}
$$

$$
\begin{array}{r l} & 2 \boxed {7 9} \dots \dots \text {余数} = \mathbf {1} = k _ {0} \\ & 2 \boxed {3 9} \dots \dots \text {余数} = \mathbf {1} = k _ {1} \\ & 2 \boxed {1 9} \dots \dots \text {余数} = \mathbf {1} = k _ {2} \\ & 2 \boxed {9} \dots \dots \text {余数} = \mathbf {1} = k _ {2} \\ & 2 \boxed {4} \dots \dots \text {余数} = \mathbf {0} = k _ {3} \\ & 2 \boxed {2} \dots \dots \text {余数} = \mathbf {0} = k _ {4} \\ & 2 \boxed {1} \dots \dots \text {余数} = \mathbf {1} = k _ {5} \\ & 0 \end{array}\tag{3}
$$

故得到 $(79)_{10}=(1001111)_{2}$ 。

(4)

$$
\begin{array}{r l} & (0 1 0 0 1 1 1 1) _ {2} \\ & \quad \downarrow \quad \downarrow \\ & = (\quad 4 \quad F \quad) _ {1 6} \\ 2 & \underline {{2 5 5}} \dots \dots \text {余数} = 1 = k _ {0} \\ 2 & \underline {{1 2 7}} \dots \dots \text {余数} = 1 = k _ {1} \\ 2 & \underline {{6 3}} \dots \dots \text {余数} = 1 = k _ {2} \\ 2 & \underline {{3 1}} \dots \dots \text {余数} = 1 = k _ {3} \\ 2 & \underline {{1 5}} \dots \dots \text {余数} = 1 = k _ {4} \\ 2 & \underline {{7}} \dots \dots \text {余数} = 1 = k _ {5} \\ 2 & \underline {{3}} \dots \dots \text {余数} = 1 = k _ {6} \\ 2 & \underline {{1}} \dots \dots \text {余数} = 1 = k _ {7} \\ & 0 \end{array}
$$

故得到 $(255)_{10}=(11111111)_{2}$ 。

$$
\begin{array}{c c} (1 1 1 1 & 1 1 1 1) _ {2} \\ \downarrow & \downarrow \\ = (\mathrm{F} & \mathrm{F}) _ {1 6} \end{array}
$$

---

## Chunk 50/68：`ch01_ex1_8`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_8 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.8 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_7 |
| next_chunk_id | ch01_ex1_9 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L435–436 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.8 题干】
[题1.8] 将下列十进制数转换为等值的二进制数和十六进制数。要求二进制数保留小数点以后8位有效数字。(1) $(0.519)_{10}$ ; (2) $(0.251)_{10}$ ; (3) $(0.0376)_{10}$ ; (4) $(0.5128)_{10}$ 。

【题1.8 解答】
【题 1.8】将下列十进制数转换为等值的二进制数和十六进制数。要求二进制数保留小数点以后 8 位有效数字。

(1) $(0.519)_{10}$ ; (2) $(0.251)_{10}$ ; (3) $(0.0376)_{10}$ ; (4) $(0.5128)_{10}$ .

解：

(1)

$$
\begin{array}{r l} & 0. 5 1 9 \\ & \times 2 \\ & \hline 1. 0 3 8 \dots\dots\text {整数部分} = 1 = k _ {- 1} \\ & 0. 0 3 8 \\ & \times 2 \\ & \hline 0. 0 7 6 \dots\dots\text {整数部分} = 0 = k _ {- 2} \\ & 0. 0 7 6 \\ & \times 2 \\ & \hline 0. 1 5 2 \dots\dots\text {整数部分} = 0 = k _ {- 3} \end{array}
$$

(2)

<table><tr><td>0.152× 2</td></tr><tr><td>0.304 ⋯整数部分=0=k-40.304× 2</td></tr><tr><td>0.608 ⋯整数部分=0=k-50.608× 2</td></tr><tr><td>1.216 ⋯整数部分=1=k-60.216× 2</td></tr><tr><td>0.432 ⋯整数部分=0=k-70.432× 2</td></tr></table>

故得 $(0.519)_{10}=(0.10000100)_{2}$ 。再转换为十六进制，得到 $(0.1000\ 0100)_{2}$ $=(\quad 0.8\quad 4)\ _{16}$

故得 $(0.251)_{10}=(0.01000000)_{2}$ 。

(3)

<table><tr><td>0.8128× 2</td></tr><tr><td>1.6256 ……整数部分=1=k-8故得(0.0376)10=(0.00001001)2。再转换为十六进制,得到(0.0000 1001)2↓ ↓ =( 0.0 9 )16</td></tr><tr><td>(4) 0.5128× 2</td></tr><tr><td>1.0256 ……整数部分=1=k-10.0256× 2</td></tr><tr><td>0.0512 ……整数部分=0=k-20.0512× 2</td></tr><tr><td>0.1024 ……整数部分=0=k-30.1024× 2</td></tr><tr><td>0.2048 ……整数部分=0=k-40.2048× 2</td></tr><tr><td>0.4096 ……整数部分=0=k-50.4096× 2</td></tr><tr><td>0.8192 ……整数部分=0=k-60.8192× 2</td></tr><tr><td>1.6384 ……整数部分=1=k-70.6384× 2</td></tr><tr><td>1.2768 ……整数部分=1=k-8</td></tr></table>

故得 $(0.5128)_{10}=(0.10000011)_{2}$ 。再转换为十六进制，得到 $(0.1000\ 0011)_{2}$ $\downarrow \quad \downarrow$ $=(\quad 0.8 \quad 3 \quad )_{16}$

---

## Chunk 51/68：`ch01_ex1_9`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_9 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.9 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_8 |
| next_chunk_id | ch01_ex1_10 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L437–440 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.9 题干】
[题 1.9] 将下列十进制数转换为等值的二进制数和十六进制数。要求二进制数保留小数点以后4位有效数字。

(1) $(25.7)_{10}$ ; (2) $(188.875)_{10}$ ; (3) $(107.39)_{10}$ ; (4) $(174.06)_{10}$

【题1.9 解答】
【题 1.9】将下列十进制数转换为等值的二进制数和十六进制数。要求二进制数保留小数点以后 4 位有效数字。

(1) $(25.7)_{10}$ ; (2) $(188.875)_{10}$ ; (3) $(107.39)_{10}$ ; (4) $(174.06)_{10}$ 。

解：

（1）将整数部分和小数部分分别转换

<table><tr><td>2</td><td>25</td><td>......余数=1=k0</td><td>0.7</td></tr><tr><td>2</td><td>12</td><td>......余数=0=k1</td><td>× 2</td></tr><tr><td>2</td><td>6</td><td>......余数=0=k2</td><td>1.4 ......整数部分=1=k-1</td></tr><tr><td>2</td><td>3</td><td>......余数=1=k3</td><td>0.4</td></tr><tr><td>2</td><td>1</td><td>......余数=1=k4</td><td>× 2</td></tr><tr><td></td><td>0</td><td></td><td>0.8 ......整数部分=0=k-2</td></tr><tr><td></td><td></td><td></td><td>0.8</td></tr><tr><td></td><td></td><td></td><td>× 2</td></tr><tr><td></td><td></td><td></td><td>1.6 ......整数部分=1=k-3</td></tr><tr><td></td><td></td><td></td><td>0.6</td></tr><tr><td></td><td></td><td></td><td>× 2</td></tr><tr><td></td><td></td><td></td><td>1.2 ......整数部分=1=k-4</td></tr></table>

故得到 $(25.7)_{10}=(11001.1011)_{2}$ 。再转换为十六进制，得到

$$
\begin{array}{r l} (1 1 0 0 1. 1 0 1 1) _ {2} & = (0 0 0 1 1 0 0 1. 1 0 1 1) _ {2} \\ & \downarrow \quad \downarrow \quad \downarrow \\ & = (1 9. B) _ {1 6} \end{array}
$$

(2) 将整数部分和小数部分分别转换

<table><tr><td>2</td><td>188</td><td>......余数 = 0 =  $k_{0}$ </td><td>0.875</td></tr><tr><td>2</td><td>94</td><td>......余数 = 0 =  $k_{1}$ </td><td>× 2</td></tr><tr><td>2</td><td>47</td><td>......余数 = 1 =  $k_{2}$ </td><td>1.750 ......整数部分 = 1 =  $k_{-1}$ </td></tr><tr><td>2</td><td>23</td><td>......余数 = 1 =  $k_{3}$ </td><td>0.750</td></tr><tr><td>2</td><td>11</td><td>......余数 = 1 =  $k_{4}$ </td><td>× 2</td></tr><tr><td>2</td><td>5</td><td>......余数 = 1 =  $k_{5}$ </td><td>1.500 ......整数部分 = 1 =  $k_{-2}$ </td></tr><tr><td>2</td><td>2</td><td>......余数 = 0 =  $k_{6}$ </td><td>0.500</td></tr><tr><td>2</td><td>1</td><td>......余数 = 1 =  $k_{7}$ </td><td>× 2</td></tr><tr><td></td><td>0</td><td></td><td>1.000 ......整数部分 = 1 =  $k_{-3}$ </td></tr><tr><td></td><td></td><td></td><td>0.000</td></tr><tr><td></td><td></td><td></td><td>× 2</td></tr><tr><td></td><td></td><td></td><td>0.000 ......整数部分 = 0 =  $k_{-4}$ </td></tr></table>

$(1011\ 1100.1110)_{2}$ 故得到 $(188.875)_{10}=(10111100.1110)_{2}$ 。再转换为十六进制,得到 $\downarrow \quad \downarrow \quad \downarrow$ $=(\text{ B } \quad \text{ C. } \quad \text{ E })_{16}$

<table><tr><td colspan="3">(3)将整数部分和小数部分分别转换</td></tr><tr><td>2</td><td>107</td><td> $\cdots\cdots$ 余数 = 1 =  $k_0$ </td></tr><tr><td>2</td><td>53</td><td> $\cdots\cdots$ 余数 = 1 =  $k_1$ </td></tr><tr><td>2</td><td>26</td><td> $\cdots\cdots$ 余数 = 0 =  $k_2$ </td></tr><tr><td>2</td><td>13</td><td> $\cdots\cdots$ 余数 = 1 =  $k_3$ </td></tr><tr><td>2</td><td>6</td><td> $\cdots\cdots$ 余数 = 0 =  $k_4$ </td></tr><tr><td>2</td><td>3</td><td> $\cdots\cdots$ 余数 = 1 =  $k_5$ </td></tr><tr><td>2</td><td>1</td><td> $\cdots\cdots$ 余数 = 1 =  $k_6$ </td></tr><tr><td></td><td>0</td><td></td></tr></table>

故得到 $(107.39)_{10}=(1101011.0110)_{2}$ 。再转换为十六进制，得到 $(0110\ 1011.0110)_{2}$ $=(\quad6\quad B.\quad6)\quad_{16}$

（4）将整数部分和小数部分分别转换

<table><tr><td>2</td><td>174</td><td>......余数 = 0 =  $k_{0}$ </td><td>0.06</td></tr><tr><td>2</td><td>87</td><td>......余数 = 1 =  $k_{1}$ </td><td>× 2</td></tr><tr><td>2</td><td>43</td><td>......余数 = 1 =  $k_{2}$ </td><td>0.12 ......整数部分 = 0 =  $k_{-1}$ </td></tr><tr><td>2</td><td>21</td><td>......余数 = 1 =  $k_{3}$ </td><td>0.12</td></tr><tr><td>2</td><td>10</td><td>......余数 = 0 =  $k_{4}$ </td><td>× 2</td></tr><tr><td>2</td><td>5</td><td>......余数 = 1 =  $k_{5}$ </td><td>0.24 ......整数部分 = 0 =  $k_{-2}$ </td></tr><tr><td>2</td><td>2</td><td>......余数 = 0 =  $k_{6}$ </td><td>0.24</td></tr><tr><td>2</td><td>1</td><td>......余数 = 1 =  $k_{7}$ </td><td>× 2</td></tr><tr><td></td><td>0</td><td></td><td>0.48 ......整数部分 = 0 =  $k_{-3}$ </td></tr><tr><td></td><td></td><td></td><td>0.48</td></tr><tr><td></td><td></td><td></td><td>× 2</td></tr><tr><td></td><td></td><td></td><td>0.96 ......整数部分 = 0 =  $k_{-4}$ </td></tr></table>

故得到 $(174.06)_{10}=(10101110.0000)_{2}$ 。转换为十六进制后得到

$$
\begin{array}{r l} & (1 0 1 0 1 1 1 0. 0 0 0 0) _ {2} \\ & \quad \downarrow \quad \downarrow \quad \downarrow \\ & = (\mathrm{A} \quad \mathrm{E}. \quad 0) _ {1 6} \end{array}
$$

---

## Chunk 52/68：`ch01_ex1_10`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_10 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.10 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_9 |
| next_chunk_id | ch01_ex1_11 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L441–444 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.10 题干】
[题 1.10] 写出下列二进制数的原码、反码和补码。

(1) $(+1011)_2$ (2) $(+00110)_2$ (3) $(-1101)_2$ (4) $(-00101)_2$

【题1.10 解答】
【题 1.10】 写出下列二进制数的原码、反码和补码。

(1) $(+1011)_2$ ; (2) $(+00110)_2$ ; (3) $(-1101)_2$ ; (4) $(-00101)_2$ 。

解：

（1）正数的反码、补码与原码相同，均为01011。

(2) 原码、反码、补码均为 000110。

（3）原码为11101，反码为10010，补码为10011。

（4）原码为100101，反码为111010，补码为111011。

---

## Chunk 53/68：`ch01_ex1_11`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_11 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.11 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_10 |
| next_chunk_id | ch01_ex1_12 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L445–447 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.11 题干】
[题1.11] 写出下列带符号位二进制数(最高位为符号位)的反码和补码。
(1) $(011011)_{2}$ ; (2) $(001010)_{2}$ ; (3) $(111011)_{2}$ ; (4) $(101010)_{2}$ 。

【题1.11 解答】
【题 1.11】写出下列带符号位二进制数(最高位为符号位)的反码和补码。

(1) $(011011)_{2}$ ;(2) $(001010)_{2}$ ;(3) $(111011)_{2}$ ;(4) $(101010)_{2}$ 。

解：

（1）符号位为0，该数为正数，故反码和补码与原码相同，均为011011。

（2）符号位为0，该数为正数，故反码和补码、原码相同，均为001010。

（3）符号位为1，该数为负数。反码为100100，补码为100101。

（4）符号位为1，该数为负数，反码为110101，补码为110110。

---

## Chunk 54/68：`ch01_ex1_12`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_12 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.12 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_11 |
| next_chunk_id | ch01_ex1_13 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L448–450 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.12 题干】
[题1.12] 用8位的二进制补码表示下列十进制数。  
(1) +17; (2) +28; (3) -13; (4) -47; (5) -89; (6) -121。

【题1.12 解答】
【题 1.12】用 8 位的二进制补码表示下列的十进制数。

(1) +17; (2) +28; (3) -13; (4) -47; (5) -89; (6) -121。

解：首先需要把每个十进制数的绝对值转换为7位的二进制数，然后加上1位符号位，就得到了8位的原码，再将原码化成补码形式。

(1) 求 +17 的补码

$$
\begin{array}{r l} & 2 \quad \underline {{1 7}} \dots \dots \text {余数} = \mathbf {1} = k _ {0} \\ & 2 \quad \underline {{8}} \dots \dots \text {余数} = \mathbf {0} = k _ {1} \\ & 2 \quad \underline {{4}} \dots \dots \text {余数} = \mathbf {0} = k _ {2} \\ & 2 \quad \underline {{2}} \dots \dots \text {余数} = \mathbf {0} = k _ {3} \\ & 2 \quad \underline {{1}} \dots \dots \text {余数} = \mathbf {1} = k _ {4} \\ & 0 \end{array}
$$

故得 $(17)_{10}=(10001)_{2}$ 。在高位加00将绝对值表示为7位二进制数，再在绝对值前面增加一位符号位0（正数），就得到原码00010001。它的补码与原码相同，也是00010001。

(2) 求+28 的补码

$$
\begin{array}{r l} {2} & {\underline {{\quad 2 8 \quad}}} \\ {2} & {\underline {{\quad 1 4 \quad}}} \\ {2} & {\underline {{\quad 7 \quad}}} \\ {2} & {\underline {{\quad 3 \quad}}} \\ {2} & {\underline {{\quad 1 \quad}}} \\ & {0} \end{array} \dots \dots \text {余数} = \mathbf {0} = k _ {0}
$$

故得 $(28)_{10}=(11100)_{2}=(0011100)_{2}$ 。在绝对值前面加上符号位0，得到原码00011100。补

码与原码相同,也是00011100。

(3) 求-13的补码

$$
\begin{array}{r l} {2} & {\underline {{1 3}} \dots \dots \text {余数} = 1 = k _ {0}} \\ {2} & {\underline {{6}} \dots \dots \text {余数} = 0 = k _ {1}} \\ {2} & {\underline {{3}} \dots \dots \text {余数} = 1 = k _ {2}} \\ {2} & {\underline {{1}} \dots \dots \text {余数} = 1 = k _ {3}} \\ & {\underline {{0}}} \end{array}
$$

故得 $(13)_{10}=(1101)_{2}=(0001101)_{2}$ 。在绝对值前面加上符号位1，得到原码10001101。从原码化成补码后得到11110011。

(4) 求 -47 的补码

$$
\begin{array}{r l} {2} & {\underline {{4 7}} \dots \dots \text {余数} = 1 = k _ {0}} \\ {2} & {\underline {{2 3}} \dots \dots \text {余数} = 1 = k _ {1}} \\ {2} & {\underline {{1 1}} \dots \dots \text {余数} = 1 = k _ {2}} \\ {2} & {\underline {{5}} \dots \dots \text {余数} = 1 = k _ {3}} \\ {2} & {\underline {{2}} \dots \dots \text {余数} = 0 = k _ {4}} \\ {2} & {\underline {{1}} \dots \dots \text {余数} = 1 = k _ {5}} \\ & {\quad 0} \end{array}
$$

故得 $(47)_{10}=(101111)_{2}=(0101111)_{2}$ 。在绝对值前面加上符号位1，得原码为10101111。将原码化成补码后得到11010001。

(5) 求 -89 的补码

$$
\begin{array}{r l} {2} & {\underline {{8 9}} \dots \dots \text {余数} = 1 = k _ {0}} \\ {2} & {\underline {{4 4}} \dots \dots \text {余数} = 0 = k _ {1}} \\ {2} & {\underline {{2 2}} \dots \dots \text {余数} = 0 = k _ {2}} \\ {2} & {\underline {{1 1}} \dots \dots \text {余数} = 1 = k _ {3}} \\ {2} & {\underline {{5}} \dots \dots \text {余数} = 1 = k _ {4}} \\ {2} & {\underline {{2}} \dots \dots \text {余数} = 0 = k _ {5}} \\ {2} & {\underline {{1}} \dots \dots \text {余数} = 1 = k _ {6}} \\ & {\quad 0} \end{array}
$$

故得 $(89)_{10}=(1011001)_{2}$ 。在绝对值前面加上符号位1，得到原码为11011001。将原码化为补码后得到10100111。

(6) 求-121的补码

$$
\begin{array}{r l} {2} & {\underline {{1 2 1}}} \\ {2} & {\underline {{6 0}}} \\ {2} & {\underline {{3 0}}} \\ {2} & {\underline {{1 5}}} \\ {2} & {\underline {{7}}} \\ {2} & {\underline {{3}}} \\ {2} & {\underline {{1}}} \\ & {0} \end{array} \dots \dots \text {余数} = \mathbf {1} = k _ {0}
$$

故得 $(121)_{10}=(1111001)_{2}$ 。在绝对值前加上符号位1，得到原码为11111001。将它化成补码后得10000111。

---

## Chunk 55/68：`ch01_ex1_13`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_13 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.13 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_12 |
| next_chunk_id | ch01_ex1_14 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L451–461 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.13 题干】
[题 1.13] 计算下列用补码表示的二进制数的代数和。如果和为负数,请求出负数的绝对值。

(1) 01001101+00100110;
(2) 00011101+01001100;

(3) 00110010+10000011; (4) 00011110+10011100;

(5) 11011101+01001011; (6) 10011101+01100110;

(7) 11100111+11011011; (8) 11111001+10001000。

【题1.13 解答】
【题 1.13】 计算下列用补码表示的二进制数的代数和。如果和为负数,试求出负数的绝对值。

(1) 01001101+00100110; (2) 00011101+01001100;

(3) 00110010+10000011; (4) 00011110+10011100;

(5) 11011101+01001011; (6) 10011101+01100110;

(7) 11100111+11011011; (8) 11111001+10001000。

解：

(1) 01001101

+ 00100110
  01110011

符号位等于0，和为正数。

(2) 00011101 + 01001100
01101001

符号位等于0，和为正数01101001。

(3) 00110010

+ 10000011
  10110101

符号位等于1，和为负数。将和的补码再求补，得原码11001011。故和的绝对值为1001011。

(4) 00011110

+ 10011100
  10111010

符号位等于1，和为负数。将和的补码再求补，得原码11000110。故和的绝对值为1000110。

(5) 11011101

+ 01001011
  00101000

符号位等于0，和为正数00101000。

(6) 10011101

+ 01100110
  00000011

符号位等于 0, 和为正数 00000011。

$$
\begin{array}{r l} & 1 1 1 0 0 1 1 1 \\ & + 1 1 0 1 1 0 1 1 \\ & \hline 1 1 0 0 0 0 1 0 \end{array} \tag {7}
$$

符号位等于1,和为负数。将和的补码再求补,得原码10111110。故和的绝对值为0111110。

$$
\begin{array}{r l} & \text {(8)} \quad \begin{array}{l} 1 1 1 1 1 0 0 1 \\ + 1 0 0 0 1 0 0 0 \\ \hline 1 0 0 0 0 0 0 1 \end{array} \end{array}
$$

符号位等于1，和为负数。将和的补码再求补，得原码11111111。故和的绝对值为1111111。

---

## Chunk 56/68：`ch01_ex1_14`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_14 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.14 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_13 |
| next_chunk_id | ch01_ex1_15 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L462–467 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.14 题干】
[题1.14] 用二进制补码运算计算下列各式。式中的4位二进制数是不带符号位的绝对值。如果和为负数，请求出负数的绝对值。（提示：所用补码的有效位数应足够表示代数和的最大绝对值。）  
(1) $1010 + 0011$ ； (2) $1101 + 1011$ ；  
(3) $1010 - 0011$ ； (4) $1101 - 1011$ ；  
(5) $0011 - 1010$ ； (6) $1011 - 1101$ ；  
(7) $-0011 - 1010$ ； (8) $-1101 - 1011$ 。

【题1.14 解答】
【题 1.14】用二进制补码运算计算下列各式。式中的 4 位二进制数是不带符号位的绝对值。如果和为负数，试求出负数的绝对值。（提示：所用补码的有效位数应足够表示代数和的最大绝大值。）

(1) 1010+0011; (2) 1101+1011; (3) 1010-0011; (4) 1101-1011;

(5) 0011-1010; (6) 1011-1101; (7) -0011-1010; (8) -1101-1011。

解：

（1）因为和的绝对值小于 $2^{4}$ ，故可采用5位的二进制补码（符号位加4位有效数字）表示两个加数。1010的补码为01010,0011的补码为00011。

$$
\begin{array}{r} 0 1 0 1 0 \\ + \quad 0 0 0 1 1 \\ \hline 0 1 1 0 1 \end{array}
$$

得到和的补码为 01101。符号位等于 0，和为正数。

（2）因为和的绝对值大于 $2^{4}$ 而小于 $2^{5}$ ，所以需要用6位的二进制补码（符号位加5位有效数字）表示两个加数。1101的补码为001101,1011的补码为001011。

$$
\begin{array}{c} \text {001101} \\ + \text {001011} \\ \hline \text {011000} \end{array}
$$

得到和的补码为 011000。符号位等于 0，和为正数。

（3）因为和的绝对值小于 $2^{4}$ ，故可用5位的二进制补码（符号位加4位有效数字）表示两个加数。1010的补码为01010，-0011的补码为11101。

$$
\begin{array}{c} 0 1 0 1 0 \\ + 1 1 1 0 1 \\ \hline 0 0 1 1 1 \end{array}
$$

得到和的补码为 00111。符号位等于 0，和为正数。

（4）因为和的绝对值小于 $2^{4}$ ，故可用五位二进制补码（符号位加4位有效数字）表示两个加数。1101的补码为01101，-1011的补码为10101。

$$
\begin{array}{c} 0 1 1 0 1 \\ + 1 0 1 0 1 \\ \hline 0 0 0 1 0 \end{array}
$$

得到和的补码为 00010。符号位等于 0，和为正数。

（5）因为和的绝对值小于 $2^{4}$ ，所以可用5位的二进制补码（符号位加4位有效数字）表示两个加数。0011的补码为00011，-1010的补码为10110。

$$
\begin{array}{c} \text {00011} \\ + \text {10110} \\ \hline \text {11001} \end{array}
$$

得到和的补码为 11001。符号位等于 1，表示和为负数。将和的补码再求补，得到原码 10111，和的绝对值等于 0111。

（6）因为和的绝对值小于 $2^{4}$ ，所以用5位的二进制补码（符号位加4位有效数字）表示两个加数。1011的补码为01011，-1101的补码为10011。

$$
\begin{array}{c} 0 1 0 1 1 \\ + 1 0 0 1 1 \\ \hline 1 1 1 1 0 \end{array}
$$

得到和的补码为 11110。符号位等于 1，和为负数。将和的补码再求补，得原码 10010。故知和的绝对值等于 0010。

（7）因为和的绝对值小于 $2^{4}$ ，所以用5位的二进制补码表示两个加数。-0011的补码为11101，-1010的补码为10110。

$$
\begin{array}{r} 1 1 1 0 1 \\ + \quad 1 0 1 1 0 \\ \hline 1 0 0 1 1 \end{array}
$$

得到和的补码为 10011。符号位等于 1，和为负数。将和的补码再求补，得原码 11101，故和的绝对值为 1101。

（8）因为和的绝对值大于 $2^{4}$ 而小于 $2^{5}$ ，所以需要用6位的二进制补码表示两个加数。-1101的补码写作110011，-1011的补码写作110101。

$$
\begin{array}{r} 1 1 0 0 1 1 \\ + \quad 1 1 0 1 0 1 \\ \hline 1 0 1 0 0 0 \end{array}
$$

得到和的补码为 101000。符号位等于 1，和为负数。将和的补码再求补，得原码 111000，和的绝对值为 11000。

---

## Chunk 57/68：`ch01_ex1_15`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_ex1_15 |
| block_type | exercise_merged |
| source_type | textbook |
| breadcrumb | 第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题 |
| section_id | ch01_sec_exercises |
| exercise_id | 题1.15 |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_14 |
| next_chunk_id | ch01_sec_1_1_theory_9 |
| source_file | 按章节拆分\03_第01章_数制和码制.md |
| line_range | L468–468 |

### 正文（检索用 text_content）

第01章 数制和码制 > summary_end 本章小结 > exercises 章末习题

【题1.15 题干】
[题1.15] 用二进制补码运算计算下列各式。（提示：所用补码的有效位数应足够表示代数和的最大绝对值。）(1) $3 + 15$ ；(2) $8 + 11$ ；(3) $12 - 7$ ；(4) $23 - 11$ ；(5) $9 - 12$ ；(6) $20 - 25$ ；(7) $-12 - 5$ ；(8) $-16 - 14$ 。

【题1.15 解答】
【题 1.15】用二进制补码运算计算下列各式。（提示：所用补码的有效位数应足够表示代数和的最大绝对值。）

$$
(1) 3 + 1 5; (2) 8 + 1 1; (3) 1 2 - 7; (4) 2 3 - 1 1; (5) 9 - 1 2; (6) 2 0 - 2 5;
$$

$$
(7) - 1 2 - 5; (8) - 1 6 - 1 4 _ {\circ}
$$

解：

（1）和的绝对值等于 18，需要用 5 位二进制数表示。加上符号位以后，补码应有 6 位。+3 的补码写作 000011，+15 的补码写作 001111。

$$
\begin{array}{c} 0 0 0 0 1 1 \\ + \quad 0 0 1 1 1 1 \\ \hline 0 1 0 0 1 0 \end{array}
$$

得到和的补码为 010010(+18)。

（2）和的绝对值等于19，需要用5位二进制数表示。加上符号位以后，补码应为6位。+8的补码写作001000,+11的补码写作001011。相加后得到

$$
\begin{array}{c} \text {001000} \\ + \text {001011} \\ \hline \text {010011} \end{array}
$$

和的补码为 010011(+19)。

（3）和的绝对值和加数的绝对值均小于16，可以用5位的二进制补码（符号位加4位有效数字)运算。+12的补码写作01100,-7的补码写作11001。将两数的补码相加

$$
\begin{array}{c} 0 1 1 0 0 \\ + 1 1 0 0 1 \\ \hline 0 0 1 0 1 \end{array}
$$

得到和的补码为 00101(+5)。

（4）用二进制数表示23需要5位代码，加上符号位以后，补码应有6位。+23的补码写作010111,-11的补码写作110101，相加后得到

$$
\begin{array}{c} 0 1 0 1 1 1 \\ + 1 1 0 1 0 1 \\ \hline 0 0 1 1 0 0 \end{array}
$$

和的补码为 001100(+12)。

(5) +9 的补码写作 01001, -12 的补码写作 10100。将两个补码相加

$$
\begin{array}{c} \text {01001} \\ + \text {10100} \\ \hline \text {11101} \end{array}
$$

得到和的补码为 11101, 和为负值。如再求补, 则得到和的原码 10011(-3)。

（6）用二进制数表示25需要5位，再加1位符号位，补码应有6位。+20的补码写作010100,-25的补码写作100111。将两个补码相加

---

## Chunk 58/68：`ch01_sec_1_1_theory_9`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_1_theory_9 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 1.1 本章重点内容 |
| section_id | ch01_sec_1_1 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_ex1_15 |
| next_chunk_id | ch01_sec_1_2_theory_17 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L9–15 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.1 本章重点内容

一、不同数制之间的转换

二、原码、反码、补码的定义和相互转换的方法

三、二进制数的补码运算

---

## Chunk 59/68：`ch01_sec_1_2_theory_17`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_2_theory_17 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 1.2 难点释疑 |
| section_id | ch01_sec_1_2 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_1_1_theory_9 |
| next_chunk_id | ch01_sec_二_为什么二进制算术运算要采用补码运算_theory_31 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L17–29 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.2 难点释疑

为什么在数字电路中要采用二进制补码进行两个数值的加、减运算？

一、首先，要回答为什么一定要采用二进制，而不是我们日常生活中熟悉的十进制。

由于一位二进制数只有1和0两个数值，可以用一个开关电路输出的高电平和低电平表示，所以用于表示1位二进制数值的单元电路结构非常简单，而且对电源电压的稳定度要求也比较低。因为只要能够正确区分出1和0两个不同状态，允许高、低电平在一定范围内波动，也就是说有一个允许的“噪声容限”。例如，在采用5V电源电压系列的CMOS电路中，以4.4V表示1，以0.5V表示0。若噪声容限为电源电压的30%，那么只要由于电源电压的波动、电路参数的变化以及外界的干扰导致输出电压的变化不超过1.5V，电路都能正常工作。

如果采用十进制, 就要求每个单元电路能够给出十个不同电压等级的输出信号, 以代表 0\~9 十个数值。不难想象, 组成这样一个单元电路是很困难的。至今尚未见有人设计出可以实际使用的十进制单元电路。而且, 即使有这样的单元电路, 在工作过程中无论对电源电压稳定度的要求, 还是对电路参数精度和稳定性的要求都是比较高的。例如, 同样也采用 5 V 的电源电压, 则需要将输出电压划分为 10 个等级, 用来表示 0\~9。这时每个电压等级之间相差将不到 0.5 V。如果由于电源电压波动、电路参数变化以及外界干扰使输出电平的变化接近 0.5 V, 则输出电压所表示的数值就可能发生错误。

鉴于以上原因,目前在几乎所有的数字电路(包括各种数字计算机)中,都采用二进制而不采用十进制。

虽然在有些数字电路的应用中有时也会提及“十进制”运算,其实只不过是用4位二进制数当中的十个状态表示十进制数的十个状态而已,本质上仍然是在用二进制数进行运算。

---

## Chunk 60/68：`ch01_sec_二_为什么二进制算术运算要采用补码运算_theory_31`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_为什么二进制算术运算要采用补码运算_theory_31 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 二、为什么二进制算术运算要采用补码运算？ |
| section_id | ch01_sec_二_为什么二进制算术运算要采用补码运算 |
| exercise_id | — |
| example_id | — |
| figure_ids | 图1 |
| prev_chunk_id | ch01_sec_1_2_theory_17 |
| next_chunk_id | ch01_sec_1_3_theory_48 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L31–46 |

### 配图

**图1** — -2-1 采用补码运算的加法运算电路

![图1](../../../../../课本/课本加习题册/markdown_云端解析/学习辅导按章节拆分/images/23024a6683b398b8c166a7051d8dd3d9179ab6b031bc25c2fe22b5171717ebce.jpg)

*视觉描述：* 补码加减法电路：四位全加器，n各比特与控制nF经异或入B端，nF接CI；nF=0做加法，nF=1对n取反加1实现减法，CO再与nF异或得SF。

### 正文（检索用 text_content）

第01章 数制和码制 > 二、为什么二进制算术运算要采用补码运算？

如果两个正数相加,则比较简单,用第四章中所讲的加法器电路就可以完成了。但如果是两个数相减(也就是两个不同符号的数相加)情况就不同了。首先必须比较两个数绝对值的大小,以确定哪一个作为被减数、哪一个作为减数。然后，让绝对值大的一个数减去绝对值小的一个数。这不仅需要用到比较电路和减法运算电路，而且运算过程也较复杂，影响运算速度。

我们在第二章中已经详细说明了,两个二进制数之间的减法运算可以用它们的补码相加实现。虽然这需要先求取两个数的补码,但产生补码的电路很简单,而且求取补码和两个数相加的操作可以合并为一步完成。

图1-2-1是一个采用补码运算的加法运算电路原理图。这个电路是在加法器的基础上附加了一组异或门 $\mathrm{G}_1\sim \mathrm{G}_5$ 而形成的。它既可以完成加法运算 $M + N$ ，又可以完成减法运算 $M - N$ 。

图1-2-1 采用补码运算的加法运算电路

当两个数正数 $M(m_{3}m_{2}m_{1}m_{0})$ 和 $N(n_{3}n_{2}n_{1}n_{0})$ 相加时，情况比较简单。因为在正常工作情况下，和数 $S(s_{3}s_{2}s_{1}s_{0})$ 不允许超出 1111，不会有进位输出，所以 CO=0。同时，N 为正数，它的符号位 $n_{F}=0$ 。因此，最后的进位输出信号 $S_{F}=0$ ，表示 S 为正数。

当 M 为正数、N 为负数时， $n_{F}=1$ ，经过 $G_{1}\sim G_{4}$ 反相后，得到 $n_{3}n_{2}n_{1}n_{0}$ 的反码，并加到加法器的输入端上。同时， $n_{F}$ 加到加法器的进位输入端，实现“加 1”运算。这样就实现了 M-N 的运算。在 M 的绝对值大于 N 的绝对值时，CO=1, $S_{F}=0$ ，表示和数为正；在 M 的绝对值小于 N 的绝对值时，CO=0, $S_{F}=1$ ，表示和数为负。

可见,用补码相加进行减法运算不仅运算电路结构简单,而且运算可以一步完成。

[图1] -2-1 采用补码运算的加法运算电路
[图1描述] 补码加减法电路：四位全加器，n各比特与控制nF经异或入B端，nF接CI；nF=0做加法，nF=1对n取反加1实现减法，CO再与nF异或得SF。

---

## Chunk 61/68：`ch01_sec_1_3_theory_48`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_1_3_theory_48 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 1.3 习题类型与解题方法 |
| section_id | ch01_sec_1_3 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_为什么二进制算术运算要采用补码运算_theory_31 |
| next_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p00 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L48–50 |

### 正文（检索用 text_content）

第01章 数制和码制 > 1.3 习题类型与解题方法

这一章的习题在内容上有三种主要类型:不同数制间的转换,原码、反码、补码间的转换,二进制数的补码运算。

---

## Chunk 62/68：`ch01_sec_一_不同数制间的转换_theory_52_p00`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p00 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 一、不同数制间的转换 |
| section_id | ch01_sec_一_不同数制间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_1_3_theory_48 |
| next_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p01 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L52–196 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、不同数制间的转换

1. 将任意进制数转换为等值的十进制数

解题方法和步骤：

利用公式

$$
D = \sum k _ {i} N ^ {i}\tag{1-3-1}
$$

即可将任何进制的数转换为等值的十进制数。上式中的 N 为以十进制数表示的计数进位的基数， $k_{i}$ 为第 i 位的系数，它可以是 0\~N 中的任何一个整数。若整数部分有 n 位，小数部分有 m 位，则 i 将包含从 n-1 到 0 的所有正整数和从 -1 到 -m 的所有负整数。

对于整数部分为 n 位、小数部分为 m 位的二进制数 $(N=2)$ ，则得到等值的十进制数为

$$
\begin{array}{r l} D & = \sum k _ {i} 2 ^ {i} \\ & = k _ {n - 1} 2 ^ {n - 1} + k _ {n - 2} 2 ^ {n - 2} + \dots + k _ {0} 2 ^ {0} + k _ {- 1} 2 ^ {- 1} + k _ {- 2} 2 ^ {- 2} + \dots + k _ {- m} 2 ^ {- m} \end{array}\tag{1-3-2}
$$

其中每一位的系数 $k_{i}$ 可能是1或0。

对于整数部分为 n 位、小数部分为 m 位的八进制数 (N=8)，则得到等值的十进制数为

$$
\begin{array}{r l} D & = \sum k _ {i} 8 ^ {i} \\ & = k _ {n - 1} 8 ^ {n - 1} + k _ {n - 2} 8 ^ {n - 2} + \dots + k _ {0} 8 ^ {0} + k _ {- 1} 8 ^ {- 1} + \dots + k _ {- m} 8 ^ {- m} \end{array}\tag{1-3-3}
$$

其中每一位的系数 $k_{i}$ 可能是 0\~7 当中的某个数值。

对于整数部分为 n 位、小数部分为 m 位的十六进制数 (N=16)，则得到等值的十进制数为

$$
\begin{array}{r l} D & = \sum k _ {i} 1 6 ^ {i} \\ & = k _ {n - 1} 1 6 ^ {n - 1} + k _ {n - 2} 1 6 ^ {n - 2} + \dots + k _ {0} 1 6 ^ {0} + k _ {- 1} 1 6 ^ {- 1} + \dots + k _ {- m} 1 6 ^ {- m} \end{array}\tag{1-3-4}
$$

式中每一位的系数 $k_{i}$ 的取值可能是 0\~15 当中的某一数值。

【例 1-3-1】将下面给出的二进制、八进制和十六进制数转换为等值的十进制数。

---

## Chunk 63/68：`ch01_sec_一_不同数制间的转换_theory_52_p01`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p01 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 一、不同数制间的转换 |
| section_id | ch01_sec_一_不同数制间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p00 |
| next_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p02 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L52–196 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、不同数制间的转换

(1) $(1101.011)_2$ ; (2) $(36.27)_8$ ; (3) $(4A.BD)_{16}$

解：

(1) 根据式 $(1-3-2)$ 得到

$$
\begin{array}{r l} (1 1 0 1. 0 1 1) _ {2} & = 1 \times 2 ^ {3} + 1 \times 2 ^ {2} + 0 \times 2 ^ {1} + 1 \times 2 ^ {0} + 0 \times 2 ^ {- 1} + 1 \times 2 ^ {- 2} + 1 \times 2 ^ {- 3} \\ & = 8 + 4 + 1 + 0. 2 5 + 0. 1 2 5 = (1 3. 3 7 5) _ {1 0} \end{array}
$$

(2) 根据式 $(1-3-3)$ 得到

$$
\begin{array}{r l} (3 6. 2 7) _ {8} & = 3 \times 8 ^ {1} + 6 \times 8 ^ {0} + 2 \times 8 ^ {- 1} + 7 \times 8 ^ {- 2} \\ & = 2 4 + 6 + 0. 2 5 + 0. 1 1 = (3 0. 3 6) _ {1 0} \end{array}
$$

(3) 根据式 $(1-3-4)$ 得到

$$
\begin{array}{r l} (4 \mathrm{A.BD}) _ {1 6} & = 4 \times 1 6 ^ {1} + 1 0 \times 1 6 ^ {0} + 1 1 \times 1 6 ^ {- 1} + 1 3 \times 1 6 ^ {- 2} \\ & = 6 4 + 1 0 + 0. 6 9 + 0. 0 5 = (7 4. 7 4) _ {1 0} \end{array}
$$

2. 将十进制数转换为等值的二进制数

解题方法和步骤：

若十进制数包含整数和小数,则整数部分和小数部分需按不同方法分别进行转换。

(1) 整数部分的转换

将十进制数除以 2, 所得余数即二进制数的 $k_{0}$ ;

将上面得到的商再除以2,所得余数即二进制数的 $k_{1}$ ;

将上面得到的商再除以2,所得余数即二进制数的 $k_{2}$ ;

依此类推,直到所得商等于0为止,就得到了等值的二进制数。

(2) 小数部分的转换

将十进制数的小数乘以2,所得乘积的整数部分即 $k_{-1}$ ;

将上面得到的乘积的小数部分再乘以2,所得乘积的整数部分即 $k_{-2}$ ;

将上面得到的乘积的小数部分再乘以2,所得乘积的整数部分即 $k_{-3}$ ;

依此类推,直到求出要求的位数为止,就得到了等值的二进制数。

---

## Chunk 64/68：`ch01_sec_一_不同数制间的转换_theory_52_p02`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p02 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 一、不同数制间的转换 |
| section_id | ch01_sec_一_不同数制间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p01 |
| next_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p03 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L52–196 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、不同数制间的转换

【例 1-3-2】将十进制数 $(273.69)_{10}$ 转换为等值的二进制数。小数部分要求保留4位有效数字。

解：首先进行整数部分的转换

$$
\begin{array}{r l} & {2 \boxed {2 7 3} \dots \dots \text {余数} = 1 = k _ {0}} \\ & {2 \boxed {1 3 6} \dots \dots \text {余数} = 0 = k _ {1}} \\ & {2 \boxed {6 8} \dots \dots \text {余数} = 0 = k _ {2}} \\ & {2 \boxed {3 4} \dots \dots \text {余数} = 0 = k _ {3}} \\ & {2 \boxed {1 7} \dots \dots \text {余数} = 1 = k _ {4}} \\ & {2 \boxed {8} \dots \dots \text {余数} = 0 = k _ {5}} \\ & {2 \boxed {4} \dots \dots \text {余数} = 0 = k _ {6}} \\ & {2 \boxed {2} \dots \dots \text {余数} = 0 = k _ {7}} \\ & {2 \boxed {1} \dots \dots \text {余数} = 1 = k _ {8}} \\ & {\qquad 0} \end{array}
$$

故整数部分等值的二进制数为 $(100010001)_{2}$ 。

其次进行小数部分的转换

$$
\begin{array}{r l} & 0. 6 9 \\ & \times \quad 2 \\ & \hline 1. 3 8 \dots\dots\text {整数部分} = \mathbf {1} = k _ {- 1} \\ & 0. 3 8 \\ & \times \quad 2 \\ & \hline 0. 7 6 \dots\dots\text {整数部分} = \mathbf {0} = k _ {- 2} \\ & 0. 7 6 \\ & \times \quad 2 \\ & \hline 1. 5 2 \dots\dots\text {整数部分} = \mathbf {1} = k _ {- 3} \\ & 0. 5 2 \\ & \times \quad 2 \\ & \hline 1. 0 4 \dots\dots\text {整数部分} = \mathbf {1} = k _ {- 4} \end{array}
$$

于是得到小数部分的转换结果为 $(0.1011)_{2}$ 。

---

## Chunk 65/68：`ch01_sec_一_不同数制间的转换_theory_52_p03`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p03 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 一、不同数制间的转换 |
| section_id | ch01_sec_一_不同数制间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p02 |
| next_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p04 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L52–196 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、不同数制间的转换

总的转换结果为 $(273.69)_{10}=(100010001.1011)_{2}$ 。

3. 二进制与八进制和十六进制间的互相转换

解题方法和步骤：

在将二进制数转换为八进制数时,首先将二进制数的整数部分从最低位向高位每3位划分为一组,同时将二进制数的小数部分从最高位向低位每3位划分为一组,然后将每一组代之以等值的八进制数,就得到了所求的转换结果。

在将二进制数转换为十六进制数时,首先将二进制数的整数部分从最低位向高位每4位划分为一组,同时将二进制数的小数部分从最高位向低位每4位划分为一组,然后将每一组代之以等值的十六进制数,就得到了所求的转换结果。

相反地，在将八进制数转换为二进制数时，只需将八进制数的每一位代之以等值的3位二进制数并按原来的顺序排列起来就行了。

同理,在将十六进制数转换为二进制数时,只需将十六进制数的每一位代之以等值的4位二进制数并按原来的顺序排列起来就行了。

【例1-3-3】试将二进制数（10111001011.0110111）转换为等值的八进制和十六进制数。

解：将给定的二进制数整数部分从右到左每3位分成一组、小数部分从左到右每3位分成一组，然后将每组用等值的八进制数代替，得到等值的八进制数为

$$
\begin{array}{c c c c c c c c} \text {(10)} & \text {111} & \text {001} & \text {011.} & \text {011} & \text {011} & \text {1}) _ {2} \\ \downarrow & \downarrow & \downarrow & \downarrow & \downarrow & \downarrow & \downarrow \\ \text {(2)} & 7 & 1 & 3. & 3 & 3 & 4) _ {8} \end{array}
$$

整数部分最左边一组的 10 应视为 010, 小数部分最右边的一组 1 应视为 100, 即不够 3 位时以 0 补足 3 位。

将二进制数的整数部分自右向左每4位分成一组,同时将小数部分自左向右每4位分成一组,然后将每组代之以等值的十六进制数,则得到

$$
\begin{array}{c c c c c} \text {(101} & 1 1 0 0 & 1 0 1 1. & 0 1 1 0 & 1 1 1) _ {2} \\ \downarrow & \downarrow & \downarrow & \downarrow & \downarrow \\ \text {(5} & \mathrm{C} & \mathrm{B}. & 6 & \mathrm{E}) _ {1 6} \end{array}
$$

---

## Chunk 66/68：`ch01_sec_一_不同数制间的转换_theory_52_p04`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p04 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 一、不同数制间的转换 |
| section_id | ch01_sec_一_不同数制间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p03 |
| next_chunk_id | ch01_sec_二_原码_反码_补码之间的转换_theory_198 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L52–196 |

### 正文（检索用 text_content）

第01章 数制和码制 > 一、不同数制间的转换

整数部分最左边一组的 101 应视为 0101, 小数部分最右边一组的 111 应视为 1110, 即不够 4 位时以 0 补足 4 位。

4. 将十进制数转换为等值的八进制和十六进制数

转换方法和步骤：

(1) 首先将十进制数转换为等值的二进制数。

(2) 再将得到的二进制数转换为等值的八进制和十六进制数。

---

## Chunk 67/68：`ch01_sec_二_原码_反码_补码之间的转换_theory_198`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_二_原码_反码_补码之间的转换_theory_198 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 二、原码、反码、补码之间的转换 |
| section_id | ch01_sec_二_原码_反码_补码之间的转换 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_一_不同数制间的转换_theory_52_p04 |
| next_chunk_id | ch01_sec_三_二进制数的补码运算_theory_222 |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L198–220 |

### 正文（检索用 text_content）

第01章 数制和码制 > 二、原码、反码、补码之间的转换

在数字电路中是用加在二进制数绝对值前面的符号位表示正、负数的。习惯上用符号位的0表示正数，用符号位的1表示负数。用这种表示方法得到的数码叫做原码。

同时还规定,正数的反码和补码与原码相同,所以正数不存在需要转换的问题。

1. 从负数的原码求反码和补码

解题方法和步骤：

（1）保持符号位的1不变，将数字部分的每一位求反（1改为0,0改为1），就得到了反码。

(2) 在反码的末位上加 1, 即得到补码。

2. 从负数的补码求原码

因为“补码的补码等于原码”，所以将补码再求补，得到的就是原码。

【例1-3-4】写出二进制数 $+1010$ 和-0101的原码、反码和补码。

解：+1010 的原码应写成 01010，反码和补码与原码相同，也是 01010。

-0101 的原码是 10101, 反码是 11010, 补码是 11011。

---

## Chunk 68/68：`ch01_sec_三_二进制数的补码运算_theory_222`

### 元数据

| 字段 | 值 |
|------|-----|
| chunk_id | ch01_sec_三_二进制数的补码运算_theory_222 |
| block_type | theory |
| source_type | guide_keypoints |
| breadcrumb | 第01章 数制和码制 > 三、二进制数的补码运算 |
| section_id | ch01_sec_三_二进制数的补码运算 |
| exercise_id | — |
| example_id | — |
| figure_ids | — |
| prev_chunk_id | ch01_sec_二_原码_反码_补码之间的转换_theory_198 |
| next_chunk_id | — |
| source_file | 学习辅导按章节拆分\02_第二部分_第01章_数制和码制_重点难点.md |
| line_range | L222–271 |

### 正文（检索用 text_content）

第01章 数制和码制 > 三、二进制数的补码运算

在数字计算机中,为了简化运算器的电路结构,是用补码相加完成两数相减(不同符号两个数的代数和)运算的。

解题方法和步骤：

(1) 将两个带符号的加数写成补码形式。

（2）将这两个补码按二进制加法相加，即得补码形式的和。

两数的符号位和来自数值部分的进位相加,所得结果就是和的符号位。

这里需要注意两点。第一，补码相加的和仍为补码，当符号位为1时，和为负数，这时的数值部分不是这个数的绝对值。第二，将两数写成补码时，数值部分所取的位数必须足以表示和的最大绝对值，否则计算结果将出现错误。

【例1-3-5】试用补码运算的方法计算下面各式

(1) 1101+0101; (2) 1110-0111; (3) 0111-1110; (4) -1011-1010。

解：

（1）因两数相加之和的绝对值为 10010，所以补码的数值部分至少应取 5 位。加上 1 位符号位，补码一共为 6 位。于是得到两数的补码相加结果

```txt
001101
+ 000101
010010
```

和的符号位仍为 0, 表示和为正数 $(+18)_{10}$ 。

（2）因两数符号不同，和的绝对值一定小于加数当中绝对值较大一个的绝对值，所以补码的数值部分不需要增加位数。由此可得两数的补码相加结果

```txt
01110
+ 11001
00111
```

和的符号位为0，表示和为正数 $(+7)_{10}$

（3）同上，因两数异号，所以补码的数值部分取4位即可。两数的补码相加结果为
00111

+ 10010
  11001

和的符号位为 1, 表示和为负数。

如果将和的补码再求补,则得到和的原码为 $10111(-7)_{10}$ 。

（4）因两数绝对值之和为5位二进制数10101，所以补码的数值部分至少需要用5位表示。加上一位符号位以后，补码一共为6位。由此可得到两数原码和补码为
