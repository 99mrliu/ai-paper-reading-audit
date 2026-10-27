# 能耗论文核查报告（paper-budget-audit）

## 来源定位

- 题名：**Energy and Policy Considerations for Modern Deep Learning Research**
- 作者：Emma Strubell, Ananya Ganesh, Andrew McCallum
- 会议/年份：The Thirty-Fourth AAAI Conference on Artificial Intelligence（**AAAI-20，2020 年**）
- 打印页：**13693–13696**（PDF 共 4 页）
- 关键表格：**Table 2**（打印页 **13695**，即 PDF 第 3 页）；方法段（PUE=1.58、0.954→0.477、公式(1)(2)）在打印页 **13694**（PDF 第 2 页）；Table 1（可再生比例）也在 13694；Table 3 在 13695。

## Table 2 相关原始行（打印页 13695）

| Model | Hardware | Power (W) | Hours | kWh·PUE | CO₂e (lb) | Cloud cost |
|---|---|---|---|---|---|---|
| BERTbase | V100x64 | 12,041.51 | 79 | 1507 | 719 | $3751–$12,571 |
| BERTbase | TPUv2x16 | — | 96 | — | — | $2074–$6912 |
| NAS | P100x8 | 1515.43 | 274,120 | 656,347 | 313,078 | $942,973–$3,201,722 |
| T2Tbig | P100x8 | 1515.43 | 84 | 201 | 96 | $289–$981 |

表注：“Power and carbon footprint are omitted for TPUs due to lack of public information on power draw.”

## 逐项核查

| 拟引用笔记的断言 | 本文实际内容 | 判定 |
|---|---|---|
| “BERTbase 用 64 张 V100” | Table 2 硬件列写 “V100x64” | **属实** |
| “运行 79 小时” | Table 2 Hours=79（方法说明该时长为“估算”，非电表实测墙钟） | **数值属实；“实测”定性不准确** |
| “实测得到 1507 kWh” | Table 2 “kWh·PUE=1507”；这是**估算值**（采样功率 × 估算时长 × PUE 1.58），且含 PUE（设施开销），不是独立电表实测 | **数值属实；性质与口径标注错误** |
| “和 1438 lb” | 本文 Table 2 BERTbase 的 CO₂e 为 **719 lb**；1438 = 1507 × 0.954（未减半的旧 EPA 因子），属于早先 ACL-2019 一文的换算结果，**不属本文** | **不属实（混入他文数字）** |
| “排放减半 → 硬件耗电也减半” | 本文只把**换算因子**减半（0.954→0.477，因 AWS 50% 可再生假设）；能耗 1507 kWh 未变。减半的是排放强度，不是电力 | **推断错误** |
| “0.477 是现在美国电网的普适实测强度” | 0.477 = 0.954（EPA 2018 美国均值 lb/kWh）÷ 2，用于“AWS 50% 可再生”假设，是**构造换算因子**，不是当前普适实测强度 | **不属实** |
| “NAS 与 T2Tbig 功率相同，证明直接复制了同一测量值” | 表值确实同为 1515.43 W；但论文**未声明**二者同源/复制。同值不能单独证明同源 | **过度推断，只能记为待核查** |
| “TPU 排放栏空着，说明排放为零” | 表注明确“因缺乏公开功率数据而省略”。空白=**未知/未报告**，不是零 | **不属实** |

## 名义复算（79 小时）

- 整机功率（CPU+DRAM+64×GPU 合计，非每卡功率）：12,041.51 W
- IT 能耗（乘 PUE 前）：12,041.51 W × 79 h = 951,279.29 Wh = **951.28 kWh**
- 乘 PUE 1.58：951.28 × 1.58 = **1,503.02 kWh·PUE**
- 印刷值：**1,507 kWh·PUE**
- 差：**−3.98 kWh（−0.26%）**，**不匹配**

## 复算不匹配后的时长问题

- 本文**没有**给出 V100x64 行 79 小时之外的另一个时长。96 小时是 **TPUv2x16 行**（不同硬件），不能当作 V100 行的实际时长。
- 条件性候选（均为**待核推定，非本文事实**）：
  - 若功率 12,041.51 W 与 PUE 1.58 精确，则印刷 1507 kWh 隐含时长 ≈ **79.21 h**；
  - 若 79 h 与 PUE 1.58 精确，则印刷 1507 kWh 隐含整机功率 ≈ **12,073.4 W**。
- 另一个带标签的对照：1507 × 0.954 = **1438 lb**（旧 EPA 因子，ACL-2019 一文口径，**不在本文**）；1507 × 0.477 = **719 lb**（本文口径，与表值一致）。

## 可用的引用说明

> 据 Strubell, Ganesh & McCallum《Energy and Policy Considerations for Modern Deep Learning Research》(AAAI-20, 2020, 打印页 13693–13696；Table 2 在打印页 13695)，BERTbase 在 V100x64（64 张 V100）配置下的数值为：整机功率 12,041.51 W、训练时长 79 小时、kWh·PUE = 1507 kWh、CO₂e = 719 lb。二者均为**估算**而非电表实测：功率为训练时采样（CPU+DRAM+64×GPU 合计），时长为据原论文墙钟时间的估算，再乘 PUE 1.58；排放按 **0.477 lb/kWh** 换算（= EPA 2018 美国均值 0.954 减半，用于“AWS 50% 可再生”的假设，并非当前美国电网的普适实测强度）。本文 BERTbase 的 CO₂e 是 **719 lb，不是 1438 lb**（1438=1507×0.954，属更早 ACL-2019 一文的口径）。“排放减半所以硬件耗电减半”不成立：本文只把换算因子减半，能耗 1507 kWh 未变。NAS 与 T2Tbig 功率同值 1515.43 W 仅为表值相同，论文未声明同源。TPU 行功率/能耗/排放空白是“因缺乏公开功率数据而省略”，属**未知而非零**。复算 12,041.51 W × 79 h × 1.58 = **1503.0 kWh·PUE**，与印刷 1507 相差 −3.98 kWh（−0.26%）；本文未给出 V100 行之外的第二个时长（96 小时为 TPUv2x16 行），候选 79.2 h / 12,073 W 均为待核推定。

## 计算产物

- `ledger.json`：录入账本（绑定来源与口径；含 BERT 复算行 + TPU 空白行）
- `calculations.json`：Skill 脚本 `audit_energy.py` 的输出（保留首次能量不匹配 `nominal_residual=-3.9787 kWh`、`conditional_rounding_overlap=false`；TPU 行 `status=unknown, reason="Missing power"`）
- `supplementary_checks.py` / `supplementary_checks.txt`：独立标明的因子推导、反向解算候选与 NAS/T2Tbig 同值观察
