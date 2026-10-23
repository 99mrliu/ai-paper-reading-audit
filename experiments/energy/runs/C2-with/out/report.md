# 合成不完整测量节选审查

现有记录不能支持该训练完整能耗与碳排的确定估计。可以确认的是材料报告了训练时长和一个电表能量读数；不能确认电表边界、归属与覆盖完整性，也不能把无单位的“180”直接作为功率计算。碳排仍为 unknown，缺失项不是零。

## 实际可读范围与证据

本次仅审阅 `INPUT/task.md`、`INPUT/paper.pdf` 和本目录提供的技能及其引用资源，未联网。PDF 为1页、PDF 1.7，无可识别的作者、日期或版本编号；原件哈希见 [source_manifest.json](source_manifest.json)。已成功提取全文，并查看 [第1页渲染图](page-1.png)，文字与页面可见内容一致。没有表格、图注、详细方法段或补充材料可供继续核对。

材料明确自称 “an artificial boundary-test fixture, not a published paper”（PDF第1页）。因此下表均为**合成节选陈述**，不是对真实实验测量有效性的认证。

| PDF第1页原文短引文 | 可确定的记录事实 | 不能据此确定 |
|---|---|---|
| “A training run lasted 4 hours.” | 报告训练历时4小时 | 电表是否覆盖同一完整4小时 |
| “Average draw was recorded as 180, but its unit was lost.” | 平均用量/功率记录的数值为180，单位丢失 | W或kW、总功率或单设备功率、设备数量及分摊 |
| “A separate meter recorded 0.72 kWh.” | 另一个电表记录能量0.72 kWh | 是否为训练专属、是否读数差值、是否含其他负载 |
| “It is unknown whether the meter covers IT equipment or the whole facility.” | IT/设施边界未定 | 是否需要PUE，以及完整训练能耗 |
| “The PUE and electricity carbon intensity are not available.” | 两项因子均未提供 | 设施能耗换算及电力运行碳排 |
| “No supplementary material is supplied.” | 本次没有补充材料 | 仪表、采样、校准、地点时段及误差信息 |

## 核算结果及条件推导

使用随附脚本运行 [ledger.json](ledger.json)，原始结果保存在 [calculations.json](calculations.json)。以下条件分支是同一未知情形的替代解释，不能相加。

| 账本记录 | 脚本结果 | 解读 |
|---|---|---|
| recorded_draw_missing_unit | unknown：Missing unit for power | 无单位的180不能换算成kWh；功率范围也仍未知 |
| recorded_meter_unknown_boundary | unknown：Missing measurement_scope: it or facility | 0.72 kWh仍是已知的记录数值；脚本无法把它认定为确定边界的能耗 |
| conditional_meter_facility | 能耗0.72 kWh；碳排unknown，状态partial | 仅假设该表覆盖本训练全部设施能耗时成立，不再乘PUE |
| conditional_meter_it | unknown：Missing numerical value | 假设0.72 kWh是训练完整IT能耗后，仍缺PUE；这里unknown不否认条件下的IT读数，而是无法计算设施总能耗 |
| conditional_180W_facility | 能耗0.720 kWh；残差0.000；碳排unknown | 假设180 W为同一4小时的设施总平均功率，算术上与电表数值相等 |

具体条件公式如下，均非本训练的新增实测结果：

- 若电表确实覆盖本训练完整4小时、同一对象，则该电表边界下的平均功率为 `0.72 kWh / 4 h = 0.18 kW = 180 W`。这不能证明丢失的单位就是W，也不能证明两项记录具有相同物理范围。
- 若180的单位为W且为总平均功率，则 `E = 180 × 4 / 1000 = 0.72 kWh`；若单位为kW，则得到720 kWh。后者只说明单位选择会改变数量级，不能据此认定原记录有错。若为单设备功率，还需设备数和分摊边界。
- 若0.72 kWh是完整且可归属的IT能耗，`E设施 = 0.72 × PUE kWh`；若已是完整设施能耗，`E设施 = 0.72 kWh`。这里不为PUE赋值。
- 若强度 `I` 的单位为kg CO₂e/kWh，且适用于相同地区、时段与电力核算口径，`C = E设施 × I`；分时情况应为 `C = Σ(E设施,i × I_i)`。缺失的强度不能设成零，也不能凭空套用平均值。

没有提供取整步长，本账本未填 `quantum`。输出中的重叠标志true及退化区间仅是给定数值下的算术行为，不证明显示精度、测量误差或科学意义。没有证据可确认数值矛盾，也没有足够证据确认测量相互验证。字面匹配、转录核对、算术相等都不证明物理对象和归因模型正确。

## 继续核算所需最少补充材料

1. **先澄清0.72 kWh的测量元数据**：电表位置及覆盖设备，是IT还是设施；计量开始/结束时间，是否覆盖完整训练；是累计值还是前后差值；是否存在其他任务、共享负载及采用何种分摊。若这些信息能证明它是训练完整设施能耗，则估计该边界能耗不必恢复180或补PUE。
2. **若电表只覆盖IT**：补充与该训练时段和设施边界相符的PUE及其来源；若漏计CPU、DRAM等，应补足遗漏部分，不能把它们当零。共享设备需避免重复归因。
3. **计算电力运行碳排**：提供用电地点、训练具体日期/时段、匹配的排放强度及来源、单位、时间粒度、生产/消费等核算口径。若要求硬件制造等全生命周期碳排，还须另补相应数据，现有材料不涵盖这些部分。
4. **若采用180作为替代或交叉核验路径**：恢复单位、设备/整机范围、设备数（仅在每设备功率时）、平均方法与采样区间。若还要报告误差或置信程度，需仪表精度、校准和原始采样记录；当前不能给出可信的不确定度区间。

现有材料只支持“报告有4小时与0.72 kWh读数”的有限陈述及上述条件公式；不支持把0.72 kWh直接标为本训练完整设施实测能耗，也不支持任何确定的碳排数值。

## 核验及未解决项

PDF信息读取、文本提取与单页渲染均成功；运行核算脚本退出码为0，意味着账本结构可接受，允许unknown，并不表示证据完整。五行结果为3个unknown、2个partial，无invalid。未出现需要修正重跑的计算失败，首次账本与首次输出均保留；未解决的缺失检查及原因没有删除。

文本提取原始stdout/stderr、脚本stdout/stderr及核验记录均保存在out目录。渲染时出现`fitz`接口弃用警告，已留存在 [verification.json](verification.json)；不影响本次渲染成功。主张与证据分类见 [claims.json](claims.json)。脚本绑定的是账本哈希，不能自动验证PDF语义；本报告的边界判断来自对第1页原文及图像的人工审阅。
