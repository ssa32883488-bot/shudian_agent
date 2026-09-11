# 教材器件 → Digital 出图库

由 `build_chip_library.py` 生成：`chip_pinmaps.json`（引脚几何）+ `components/*.dig`（考试外壳）。

脚间距 **40**；宽度 `Width*20+20`。

## 覆盖规模

| 来源 | 数量 | 说明 |
|------|------|------|
| Digital 官方 DIL | ~122 | 全部 `lib/DIL Chips`（74xx + EPROM 等） |
| 自定义考试外壳 | 28 | 555 / CMOS / DAC·ADC / 缺失 74 / GAL / 运放 / 2114 |
| 别名 | ~800 | `74LS*`/`74HC*`/`CC*`/`CD*`/`NE555`… |

`list_chips()` / `list_families()` 可查当前入库名。

## 族一览

| 族 | 代表 |
|----|------|
| **74xx** | 门、138/147/148/151/153/154、160–163、190/191/193/194、7485/74283/7442/7448、7490/7493… |
| **timer** | `NE555`（别名 555/LMC555）、`NE556` |
| **cmos** | `CC4069` `CC40106` `CC4007` `CC4027` `CC4024` `CC4510` `CC40192`；官方 `744017`↔4017 等 |
| **dac** | `AD7520`、`DAC0808`（兼 0806/0807/0830 别名） |
| **adc** | `ADC0820` |
| **analog** | `OPAMP`（DAC 外接运放） |
| **pld** | `GAL16V8` |
| **memory** | Digital EPROM + `2114` 外壳 |

金标考试脚名：`74163_exam`（`~R`/`D0`/`EP`…）。

## 教材脚名别名（自动映射）

`pin_library.PIN_ALIASES` + 通用回退。常见：

| 芯片 | 教材写法 | Digital 库脚 |
|------|----------|--------------|
| 74151 | `~G`/`Ḡ`/`STROBE` | `S` |
| 74151 | `~Y`/`Ȳ` | `W` |
| 74151 | `A0/A1/A2` | `A/B/C` |
| 74150 | `~G`；输出 `Y` | `S`；`W` |
| 74138 | `G1/~G2A/~G2B`；`Y0`… | `G/~GA/~GB`；`~Y0`… |
| 74157 | `~G` | `G` |

未知脚在校验/布局阶段**硬失败**，不再 warning 后继续出图。

## 脚名同义（节选）

- 计数：`~R`↔`~CLR`/`~SR`，`D0`↔`A`/`P0`，`EP`↔`ENP`/`CEP`，`Q0`↔`QA`
- 555：`TRIG`/`THRES`/`DISCH`/`CTRL`；教材 `vI1/vI2/vO` 可映射
- AD7520：`d9…d0`↔`DB1…DB10`，`Iout1`↔`OUT1`，`RF`↔`RFB`

见 `pin_library.PIN_ALIASES`。

## 自定义外壳说明

`components/` 下黑盒 DIL：**可出图布线**；多数**无完整模拟模型**，CLI `test` 向量可能失败——分析/计算题仍以 `logic_first`+网表为准，出图为考试原理图。

## Digital 官方 CMOS 怪异名

| 教材 | 库内 dig |
|------|----------|
| 4002 / CC4002 | `744002` |
| 4075 | `744075` |
| 4017 | `744017` |
| 40105 | `7440105` |

## 重建

```bash
cd shudian_agent/backend/app/tools/draw/digital_dig
py -3 build_chip_library.py
```

需能访问 `F:\code\digital-circuit-poc\digital\lib`。
