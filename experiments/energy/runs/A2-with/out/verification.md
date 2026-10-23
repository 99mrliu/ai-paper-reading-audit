# 核查记录

- 遵守范围：只读工作目录内 INPUT 和随附 skill；无网络、无委派；未改变 INPUT 或 skill。未检查项目历史及其他会话文件。
- 来源：完整提取6页 PDF；核对 p2 方法公式和 p4 Table 3/4 渲染图。PDF 页码与印刷页之差为3644。源文件哈希保存于 source-sha256.txt。
- 运行：`python3 skill/scripts/audit_energy.py out/ledger.json --out out/calculations.json`；首次运行退出码0，20条记录，无 invalid。日志在 audit-run.log。没有失败后覆盖重跑。
- 保留的名义检查失败：五行精确点值均与整数印刷值存在非零残差；其中base/big/ELMo/NAS的两项可按最终整数舍入重现，BERT 79h 两项不能。calculation 的 nominal 精确重叠为 false 不等同于判错。
- BERT 独立候选：正文79.2h计算结果为1506.82639536kWh、1437.51238117344lb，两项整数舍入吻合；不宣称取得原始计算表。
- 条件舍入检查：两套假设均明确写在报告与ledger中；各行能量、排放分别重叠，不表示物理真实性或统计不确定度。
- 保留 unknown：TPU代表行缺功率 status=unknown；本地设施能量可算，但缺当地因子 status=partial、carbon_status=unknown。其他TPU行的缺项已在报告逐类说明，不以已知GPU值填补。
- 保留未决来源差异：ELMo及其他模型的测量/表列硬件转换不充分；DRAM采样细节不足；Table 4的9998天与239942小时相差10h，52小时均值与50.10小时名义均值不同。未自行修正原文。
- claims.json 为精简主张记录；源文短引文与数字匹配仅支持转录核对，不能证明外推合理、完整排放核算或科学语义。
