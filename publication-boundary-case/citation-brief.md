# 可引用短笺：作者核查后的结果

以下是本项目作者的整理，**不是AI原答**。引用时保留具体文章与表号，不将两篇拼成一项实测。

> Strubell、Ganesh与McCallum的AAAI2020文章《Energy and Policy Considerations for Modern Deep Learning Research》在Table2（PDF第3页，印刷13695）列出BERTbase/V100×64：Power=12041.51W，Hours=79，kWh·PUE=1507，CO₂e=719lb。这是论文的估计表，非我们重新测量的结果。方法（PDF2，13694）使用PUE1.58，并按AWS50%可再生能源及剩余能源比例近似美国的假设，将0.954减半为0.477lb/kWh；不能把它当作当前任意地点的普适实测强度。因子减半不足以证明实际硬件耗电减半。TPU行功率/电量/排放未报告，表注给出缺少公开功率信息的原因，不能填零。

| 判断性质 | 核查结果 | 本地证据 |
| --- | --- | --- |
| 论文表列事实 | 2020/Table2是719lb；2019/Table3是1438lb，两表电量均显示1507 | [2020表/表注](transfer/source/table2.png)、[2019表3页图](figures/table3-page4.png)PDF4 |
| 作者条件复算 | 按合计IT功率处理表列值：12041.51W÷1000×79h×1.58=1503.0212782kWh；再乘0.477为716.9411497014lb。与表列值不等，不能悄悄用候选替换原行 | [精确核算与假设](transfer/author-results.json)、[原始账本输出](transfer/actual-artifacts/calculations.json) |
| 作者条件舍入 | 1507×0.477=718.839，按整数half-up得719；1507×0.954=1437.678，得1438。兼容不证明原作者采用这个中间输入或舍入顺序 | [方法与因子](transfer/source/factor-assumptions.png)、[作者Fraction脚本](transfer/author_verify.py) |
| 有限范围的未发现 | 2020所附Models/BERT段及Table2没有提供另一个V100实际时长；四页文本提取也未检出79.2或3.3。不是其他版本/补充材料不存在这些信息的证明 | [Models段](transfer/source/bert-models.png)、[搜索范围记录](transfer/source/source-record.json) |
| 来源仍未知 | 方法有采样和合计功率公式，但未取得这行CPU/DRAM/GPU分项与原始日志；NAS与T2Tbig同值不足以确定复制、沿用或独立测量 | [训练流程](transfer/source/training-method.png)、[方法公式](transfer/source/method-pue-equation.png)、[2019未参与拟合行反例](matched/power-probe.json) |

若只收到2020论文，最多核实其关于2019因子的陈述，不能声称自己读了2019原表。本项目作者另查了完整2019原件，包内保留关键原文页图与转录，才可作上述跨文表值比较；玻尔新会话没有收到该原件，模型首答对2019表值的记忆不作为那次操作已核查的证据。

79.21只是在明示显示舍入模型下可行的时长之一。它不是2020原文新增事实；2019正文的79.2也不是2020测量证据。尚需原作者日志、未舍入输入与取整实现，才能进一步识别内部计算路径。
