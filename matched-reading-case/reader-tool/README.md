# 从玻尔交付文件到原文判定：可直接操作的复算入口

本工具由作者在真实A/B阅读和B后续失败之后编写，**不是玻尔生成的脚本**，也没有在模型对照输入中使用。它补上一个复做缺口：读者可修改明确的表格输入，直接检验“同一参数缩放”的条件模型，而不是手工修改硬编码脚本或相信模型的来源故事。只用Python标准库。

在材料包根目录执行：

```sh
python3 reader-tool/table_probe.py reader-tool/table-probe-input.json
```

用原PDF第4页Table3核查输入JSON里的五个字段：模型名、GPU型号、GPU数、功率W、显示步长。前两行是拟合输入，另两行是未参与拟合的检验输入。共享CPU/DRAM和每GPU功率是**待检验假设**，不是由原文确认的真实机制。P100/V100混合拟合会明确返回cross_hardware_fit=true，不能略过该前提。

如何验收本案例输出：

| 实际输出字段 | 预期与解释 |
| --- | --- |
| T2Tbase prediction_minus_display_W | 精确99.65W，不是零 |
| T2Tbase disjoint_envelopes | true：显示误差包络仍不相交 |
| T2Tbase minimum_envelope_gap_W | 精确99.64W：假设每个显示功率误差不超过0.005W，差异仍不能消除 |
| NAS disjoint_envelopes | false：与输入点同g、同功率，零残差没有新增判别力 |
| NAS input_coordinate_duplicates_fit_row | true，明确提示上面的非判别问题 |
| measurement_source_provenance | 始终not identified，不能由某行吻合或全表模型被否定推出来源 |

**为什么不用简单浮点容差？** 对待检验的P=a+g·b，预测是w0·P0+w1·P1，其中w1=(g−g0)/(g1−g0)，w0=1−w1。显示中心的预测半径为|w0|·q0/2+|w1|·q1/2，q为输入的显示步长。把预测包络与验证行[p−q/2,p+q/2]比较，只有严格分离才按这个包络拒绝模型。符号权重也覆盖线性外推。Fraction保留精确边界，Decimal只负责显示。

这里用的是**保守闭包络**，包含舍入边界，不是严格half-up解集，更不是统计置信区间。模型未被某行拒绝，只能说在所给包络中未排除；不能报告存在统一真实测量，更不能把硬件标签当可共享参数的证据。代码不自动提取PDF、不转换单位、不检查引用授权，也不能补真实功率来源。

再检查不可识别的边界：

```sh
python3 reader-tool/table_probe.py reader-tool/same-count-input.json
```

应输出status=invalid并以2退出。该文件是把第二拟合行的GPU数改成8的**合成输入校验例**，不是论文转录；相同g的两个点不能识别斜率。本工具不会随便设斜率为0或跳过失败继续宣布成功。完整实际输出分别保存在table-probe-output.json和same-count-output.json。

从玻尔复做时，先保存交付脚本和原回答，再下载到自己的路径；不要把本例本机session路径照搬到自己电脑。原AI脚本与作者后写工具分开：matched/A-verify_acl_energy.py、B-verify_acl_energy.py、B-acceptance.py是原实际产物，保留各自不当推断；本工具用于作者验收。更换其他表格时，显式修改输入与假设，并重新回原文核对。只验证了本案例和列出的输入边界，不声称跨论文普适。
