# 事后诊断修复说明（repair notes）

> 标注：本文件为**事后诊断**，不计入首答检查。首答与既有交付文件
> `audit_report.md`、`ledger.json`、`calculations.json`、`supplementary_checks.py`、
> `supplementary_checks.txt` **均未改动**。本诊断只读当前 AAAI-20 PDF、本次已生成文件与 Skill，
> 不联网、不读旧报告。

## 1. “=719”与“=1438”是精确等号还是显示取整

实际运行（新增 `repair_checks.py` → `repair_checks.json`）：

- 1507 × 0.477 = **718.839**（精确），不是 719；**719 是四舍五入到整数的显示值**。
  - 所以报告里“1507×0.477=719”是**显示取整**，精确式应为 1507×0.477=718.839≈719。
  - 这正是本文 Table 2（打印页 13695）CO₂e 列显示 719 的来源：本文自己对 718.839 取整。
- 1507 × 0.954 = **1437.678**（精确），不是 1438；**1438 是取整**。
  - 所以引用里“1438=1507×0.954”是**显示取整**，精确式为 1437.678≈1438。

**ACL-2019 表值核查情况（只读当前 AAAI-20）**

已直接从本文核实到的关于 ACL-2019 的**陈述**（非表值）：
- 方法段（打印页 13694）：ACL-2019“use this conversion [0.954] **without modification** to convert kilowatt-hours to carbon footprint”（即 ACL-2019 未减半地用了 0.954）。
- Table 1 表注（打印页 13694）：“Country percentages **taken from Strubell, Ganesh, and McCallum (2019)**”。
- Table 2 标题（打印页 13695）与 Table 3 标题（打印页 13695）均以“(Strubell, Ganesh, and McCallum 2019)”为来源。
- 摘要（打印页 13693）：ACL-2019“quantifying the approximate financial and environmental costs of training and tuning neural network models for NLP”。

**未核实**（本次未提供 ACL-2019 原文，本文也未复现其表格）：
- ACL-2019 的**任何具体表值**——包括其 BERTbase 的 kWh（是否为 1507？）与 CO₂e（是否为 1438？）——**都未被直接核查**。
- 因此首答中“1438 …属更早 ACL-2019 一文口径”应修正为：1438 只是**本文 1507 × 本文 0.954 的乘积取整**（1437.678→1438），它不是我从 ACL-2019 表里读到的值，也不能当作已核实的 ACL-2019 数字。

## 2. 无 quantum 时 `conditional_rounding_overlap=false` 到底排除了什么

脚本 `quantity()` 未给 `quantum` 时取 q=0，区间退化为单点 `[nominal, nominal]`。因此首答那次运行里：

- 计算能量区间 = `[1503.0212782, 1503.0212782]`（点）
- 报告能量区间 = `[1507, 1507]`（点）
- `conditional_rounding_overlap=false` 只表示：**在“所有输入零舍入”的点假设下，1503.02 ≠ 1507**。

它**不是**对显示舍入的检验，**不能**排除“Hours=79 等输入存在显示舍入”。要谈舍入必须显式提供 `quantum`（且本文未声明任何步长，只能做带标签的条件假设）。

验证（新增文件 `ledger_quantum_1h.json` → `calculations_quantum_1h.json`，`ledger_quantum_reported_kwh.json` → `calculations_quantum_reported_kwh.json`）：

- 给 `duration` 加 `quantum=1h`（条件假设“79 按 1h 步长显示舍入”，本文未声明）：计算区间变 `[1493.51, 1512.53]`，与 `[1507,1507]` 的 `overlap=True` → **时长显示舍入假设未被排除，且可兼容**。
- 只给 `reported_energy=1507` 加 `quantum=1kWh`（条件假设“1507 按 1kWh 步长显示舍入”）：报告区间变 `[1506.5,1507.5]`，仍 `overlap=False` → **仅把印刷 1507 当整数舍入无法解释 −3.98 kWh 的差距**；差距更可能来自输入侧（估算时长或未显示的功率小数）。

**carbon_check 残差单位**：脚本把 g/kg/lb 统一换算为 **kg**，故 `carbon_kg.nominal`、`carbon_check.reported.nominal`、`carbon_check.nominal_residual` 都是 **kg**。
- 残差 `-0.933878786417181682` 是 **kg**，折合 **−2.0588502986 lb**（新增计算）。不要把该字段读成 lb。

## 3. 三句表述的原文支持度（逐句、逐位置）

| 表述 | 判定 | 原文位置与性质 |
|---|---|---|
| “CPU+DRAM+64×GPU 合计的采样功率” | **部分支持** | ①“合计=CPU+DRAM+GPU 之和”：方法段打印页 **13694**——“the sum of GPU, CPU and DRAM draw”；公式 `pt=1.58(pc+pr+g·pg)/1000`，`g`=GPU 数，Table 2（13695）硬件“V100x64”即 g=64。②“采样”：仅本文**声称**——打印页 **13693**（Case study 1）——“sample power consumption during training using readily available command-line tools”。但本文未给出 pc/pr/pg 分项或采样日志，无法核实 12,041.51 W 是否确由采样得到。③12,041.51 W 是 Table 2（13695）的**表列显示值**；真实物理能耗=**未知**。 |
| “能耗 1507 未变” | **“1507”存在；“未变(相对旧文)”不支持** | “1507 kWh”= Table 2（13695）表列显示值，存在。但本文**未声明**该值是否与 ACL-2019 相同（摘要只说 incorporating updated estimates）。仅支持：“本文只把换算因子减半（0.954→0.477，13694），能耗列仍为 1507；因子减半不改变能耗列数值”。 |
| “仅有 79 小时” | **需限定到 V100 行，且为估算** | 仅对 Table 2（13695）BERTbase **V100x64** 行成立：该行 Hours=79，本文未给该行第二个时长。但 79 是**估算值**（打印页 13693：“We then estimate the time to train to convergence using wall-clock training times and hardware reported in the original papers”），非电表实测墙钟；且 BERTbase 另有 **TPUv2x16** 行 Hours=96（不同硬件）。故“仅有 79 小时”须写为“V100x64 行的估算时长为 79 h，本文未给该行第二时长；96 h 属 TPUv2x16 行”。 |

**性质区分（本文事实 / 我的推导 / 未知）**
- 表列显示值（本文事实）：12,041.51 W、79 h、1507 kWh、719 lb（Table 2，打印页 13695）；0.954、0.477、PUE 1.58（方法段，13694）。
- 公式条件复算（我的推导）：12,041.51×79×1.58=1503.02 kWh·PUE；1507×0.477=718.839→719；1507×0.954=1437.678→1438。
- 作者实际采样来源：本文**声称**采样（13693），但未附原始采样日志或分项功率 → **无法核实，未知**。
- 真实物理能耗：无电表/日志 → **未知**；79 h 是估算而非实测墙钟。

## 4. supplementary_checks.py 的注释与键名问题（仅指出，不改原文件）

- **第 19 行注释** `# --- Transcribed from Table 2 (printed page 13694) ---`：与同文件第 6–7 行题头及 `ledger.json` 的“Table 2 打印页 **13695**”冲突。Table 2 实为 13695；13694 是方法段所在页。应更正为 13695（本次按要求不改动原文件，仅记录）。
- **`candidate_C_old_factor_0p954_never_in_this_paper`**（及 label“from the earlier ACL-2019 paper, NOT this AAAI-20 paper”）混淆了两件事：
  - **0.954 在本文确实出现**（方法段，打印页 13694：EPA 美国均值，减半前的因子）；
  - **1438 lb 未在本文出现**（Table 2 及全文均无 1438），且**未被核实为 ACL-2019 表值**。
  - 正确表述应为：0.954 在本文存在；`0.954×1507=1437.678→1438` 只是条件乘积，既不在本文 Table 2，也未被本文证实为 ACL-2019 数值。键名“never_in_this_paper”把“因子存在”与“乘积不存在”绑在一起，属误标。

## 5. 最终可引用短段（修正后）

> 据 Strubell, Ganesh & McCallum《Energy and Policy Considerations for Modern Deep Learning Research》(AAAI-20, 2020, 打印页 13693–13696；Table 2 在打印页 13695)，BERTbase 的 V100x64 行：整机功率 12,041.51 W、Hours=79、kWh·PUE=1507、CO₂e=719 lb。功率按方法(打印页 13694)为 pc+pr+g·pg（CPU+DRAM+64×GPU 合计），系训练时采样功率的估算；时长 79 h 是据原论文墙钟时间的估算(打印页 13693)，非电表实测，本文未给 V100 行第二个时长（96 h 属 TPUv2x16 行，硬件不同）。能耗 1507 kWh 为估算值(含 PUE 1.58)，排放按 0.477 lb/kWh(=EPA 2018 均值 0.954 减半的构造因子)换算，故 1507×0.477=718.839，取整得表值 719 lb。本文只把换算因子减半(0.954→0.477)，未声明能耗 1507 是否与 ACL-2019 相同，故“排放减半故耗电减半”不成立。1438 lb 仅是 1507×0.954=1437.678 的取整结果，本文 Table 2 无此值，且本文未复现 ACL-2019 表值，不能把它当作已核实的 ACL-2019 数字。NAS 与 T2Tbig 功率同值 1515.43 W 仅为表值相同，论文未声明同源。TPU 行空白=“因缺乏公开功率数据而省略”=未知而非零。复算 12,041.51×79×1.58=1503.02 kWh·PUE，与印刷 1507 相差 −3.98 kWh(−0.26%)，本文未解释该差距。

## 新增文件清单

- `repair_checks.py` / `repair_checks.json`：精确乘积与 kg↔lb 换算。
- `ledger_quantum_1h.json` / `calculations_quantum_1h.json`：时长 quantum=1h 的条件候选（overlap=True）。
- `ledger_quantum_reported_kwh.json` / `calculations_quantum_reported_kwh.json`：报告值 quantum=1kWh 的条件候选（overlap=False）。
- `repair_notes.md`：本说明。
