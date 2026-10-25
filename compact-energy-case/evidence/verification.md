# 验证记录

- 仅目录内材料和普通本地工具：pdftotext、pdftoppm、Python标准库；未联网或委派。INPUT和skill未修改。
- 阅读提供的skill/SKILL.md、references/ledger.md、scripts/audit_energy.py，采用其账本核算流程。
- PDF文本成功提取，6页；视觉核对PDF第4页Table3/4。原件SHA256及版本范围见source_manifest.json。
- 执行：`python3 skill/scripts/audit_energy.py out/ledger.json --out out/calculations.json`。最终退出码0，25条记录，无invalid；存在预期的partial（本地实际排放因子缺失）和unknown（TPU功率缺失）。脚本成功不代表所有表值比较通过。
- nominal记录保留全部原印刷输入。五行的精确点值与印刷整数均有非零残差，因此点区间比较为false；这是预期的精确相等检查失败，不应一律作为论文出错。
- 显式条件舍入：功率0.01W、报告能量1kWh/碳排1lb、时长固定。T2Tbase、T2Tbig、ELMo、NAS两项兼容；BERT两项不兼容（失败保留为BERTbase_GPU_fixed_hours_rounding）。
- 额外允许时长按1h舍入时五行两项兼容；固定PUE及强度。此为条件显示区间，不是测量误差或置信区间。
- 正文BERT79.2h另存BERT_79_2_sensitivity，不覆盖Table3原79h；结果按整数舍入得到1507kWh/1438lb。该敏感性结果自身与印刷整数仍非精确相等。
- 印刷能量到碳排独立检验五行均条件兼容，不能据此推断作者实际取整顺序。
- 原始采样、跨硬件规则、NAS步数精度、R&D平均52h与表内50.10h差异等未解决，报告中明示；无首次无效输入需要更正，所有失败数值检查保留在最终账本输出。
- 主张记录见claims.json。脚本输出的ledger_sha256仅绑定账本；它不自动绑定PDF证据或证明语义。
