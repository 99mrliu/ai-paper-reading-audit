# 626155究竟属于什么？一次AI论文阅读的输入、回答与原文核查

本教程复用2026年10月23日已发生的真实阅读。本次按公开文本限额整理一个完整案例，保留原始6页PDF、实际输入、完整AI报告和25条核算记录。未新增独立模型实验；完整原生轨迹按平台协议另附，关键完整操作记录保留在本包。

## 要解决的阅读问题

我们给AI一道带有待审查错误引述的任务：“一个Transformer模型产生626155公斤碳排”。这不是我们已经相信的论文结论，而是刻意设置的引用审查问题。纠正单位仍不足以修好这句话：必须查明数字对应单次训练、调参还是整个架构搜索，以及它是测量还是估计。

主论文是Emma Strubell、Ananya Ganesh、Andrew McCallum的《Energy and Policy Considerations for Deep Learning in NLP》，ACL2019，印刷页3645–3650，ACL Anthology P19-1355六页版本。来源、许可及原件见[来源说明](SOURCES.md)与[原PDF](paper/acl-energy.pdf)。文中的8卡本地训练输入属于构造任务，未在真实机器上测量。

## 当时实际给了AI什么

这次阅读使用工具可调用的Codex CLI，只有本会话的论文PDF、任务和随附Skill，没有其他会话答案。准确服务端模型快照未在事件流中披露，不能用今天的模型标签追认。

实际任务全文如下，原件见[task.md](evidence/task.md)：

```text
请阅读 INPUT/paper.pdf（Strubell等，ACL2019），给准备引用这篇论文的机器学习研究者写一份可核查的中文阅读审计。
重点是方法节和Table 1、3、4，而非概括摘要。解释能耗和碳排估计怎样得到、哪些部分实际测量、哪些来自外推或假设。复算Table 3中所有有功率数据的行，逐项比较印刷能耗和排放值；对于名义复算与表值的差异，给出证据允许的判断，避免武断替作者认错或辩护。解释设备数、PUE、单位以及不同预算口径怎样影响解读。
我们将引用“一个Transformer模型产生626155公斤碳排”，并按论文方法估算一次本地训练：8张GPU的合计平均IT功率1.51543 kW，运行84小时；另有设施电表记录201 kWh。审查这句话与这两组数据应怎样使用、能确定什么、不能确定什么。不需要查询当前电网因子或重新训练。
报告说明对后续引用和测量的建议，保留原文PDF页码/短引文或表格位置、复算过程，以及事实、条件推导和缺失信息的区别。预算允许使用本地计算或图像工具，不要求特定报告格式。保存 out/report.md；若另有计算产物也保留。
```

实际会话指令如下，原件见[prompt.txt](evidence/prompt.txt)：

```text
You are executing one independent paper-reading task. You have no prior results from other sessions.
Read INPUT/task.md and the supplied INPUT materials. Only use files within this working directory, plus ordinary installed executables/libraries. Do not inspect parent directories, other sessions, credentials, global skills, or project history. No networking, publishing, submitting, or delegating. Do not alter INPUT files or the supplied skill. You may write temporary artifacts and your results within this directory.
Budget: at most 30 tool calls and 15 minutes. Work independently; do not ask the user questions. If material is insufficient, explain the limitation and stop or provide a bounded result. Save the requested Chinese report as out/report.md. Preserve failed checks and report any unresolved problems. Do not claim that literal evidence matching proves scientific meaning.
Use the supplied skill/SKILL.md and its referenced resources to carry out this task. Keep its verification and claims artifacts in out/ as well as the report.
```

Skill的作用是提示先确认口径，再建立数值账本并运行核算器；它没有预先填写这篇论文的答案。[当时冻结的Skill](skill/SKILL.md)与[核算器](skill/scripts/audit_energy.py)均保留。工具代码只检查录入数字和边界，不会自动证明引用含义。

## 实际执行顺序与每一步的作用

下列顺序依据原始完整事件流；其中涉及取证、核算与核查的[四次完整操作](evidence/selected-operations.jsonl)随包保留，完整原生流另附平台，不把选录称为完整轨迹。

1. AI列出INPUT和skill文件，读取任务、Skill说明、账本规范与核算代码。读代码是为了知道计算器接受的单位和口径，而不是把退出码0当作论文正确。
2. 实际执行`pdftotext -layout INPUT/paper.pdf out/paper.txt`并读取全文。全文仅六页，这次没有用检索片段代替方法上下文；短文中保留列布局更便于检查表头与跨行项目。
3. 实际执行`pdftoppm -f 4 -singlefile -scale-to 1800 -png INPUT/paper.pdf out/page4`，保留第4页图像。原报告自述查看该页；旧事件导出没有完整图像查看遥测，不能由“生成了PNG”独立证明每一次视觉查看。
4. AI编写`out/build_ledger.py`，把Table3的五行和条件性变体录入账本，调用`audit_energy.py`。首次为20条，随后增加固定小时的舍入变体，最终25条；这些是同一批数字的检查变体，不是25次物理实验。
5. AI输出中文报告、claims与verification，保留BERT直接复算失败及原始测量资料缺失。完整报告见[真实AI输出](evidence/report.md)。

为什么要同时看Table1、方法、模型段和Table3？Table1说明那个大数字的单位与预算，方法给PUE和因子，模型段给完整时长与等效情景，Table3把具体硬件、功率、时长和结果放在一起。任何一处单独抽取都不足以判定整句话。

![论文PDF第4页，包含Table3与Table4](paper/page4.png)

图出自上述ACL2019论文，CC BY4.0，作者与出处见来源说明。整页保留列标题、行分组、脚注和相邻文字，不把GPU行与缺失的TPU行拼接。

## AI实际回答，以及我们核查到了哪一步

下面逐字摘自真实AI报告，不是本次重写时生成的模拟答案：

> **引用判断：不能引用“一个 Transformer 模型产生 626155 公斤碳排”。** 所供论文 Table 1 的 626,155 属于“w/ neural arch. search”，Table 3 对应 NAS 的 GPU 情景，单位为 **lb CO₂e**，约 **284,019 kg（284 吨）**；它是完整架构搜索预算的估计，不是单个最终模型一次训练的实测排放。Table 1 的 Transformer big 单次训练另列 **192 lb，约 87.09 kg**。两处混淆分别涉及质量单位与预算范围。
>
> 可改为：“Strubell 等（2019，Table 1、3）在其功率外推、PUE=1.58 和美国平均排放因子假设下，估计该神经架构搜索的 GPU 等效情景排放约 626,155 lb CO₂e（约 284 吨）；同表 Transformer big 一次训练估计约 192 lb。”不可把 GPU 等效情景说成对原 TPU 搜索全过程的电表测量，也不可推广为所有 Transformer 的固定排放。

作者侧核查：PDF第1页Table1把626155列在含神经架构搜索的项目，单位是lb；第4页Table3的NAS GPU情景对应该数。换算`626155×0.45359237=284019.13043735 kg`。因此原句同时错在单位、预算归属和把估计说得过于确定。数值换成284吨仍不能省掉“完整搜索预算的GPU等效估计”。

方法节PDF第2页还说明短期采样、完整训练时长来自其他论文，采用PUE1.58和0.954 lb/kWh。它不能支持“逐一完整测量了表中所有训练的实际排放”。这里没有取得底层采样日志，不能复核跨硬件外推的准确性。

## 不只接受AI说法：逐行复算Table3

采用表中Power为合计IT功率的解释，设施能量为`P×t×1.58/1000`，排放为`E×0.954`。Power既是合计量就不能再乘设备数。这样能重现多数行的取整数值，是该解释的算术支持；它本身仍不证明原始测量覆盖全部IT设备。

| 行 | 功率W | 时长h | 复算/印刷kWh | 复算/印刷lb |
| --- | ---: | ---: | ---: | ---: |
| T2Tbase | 1415.78 | 12 | 26.8431888 / 27 | 25.6084021152 / 26 |
| T2Tbig | 1515.43 | 84 | 201.1278696 / 201 | 191.8759875984 / 192 |
| ELMo | 517.66 | 336 | 274.8153408 / 275 | 262.1738351232 / 262 |
| BERTbase | 12041.51 | 79 | 1503.0212782 / 1507 | 1433.8822994028 / 1438 |
| NAS | 1515.43 | 274120 | 656347.281128 / 656347 | 626155.306196112 / 626155 |

真正需要回读正文的是BERT：79小时算出1503.0212782 kWh和1433.8822994028 lb，无法仅靠最终整数取整得到1507与1438。PDF第3页BERT段又给出79.2小时；用它得到1506.82639536 kWh和1437.51238117344 lb，取整兼容表值。

原始工具输出的一段如下，可在上述事件流中检索，不是本稿新跑的模型结果：

```text
{"out": "out/calculations.json", "exit_code": 0, "records": 25}
T2Tbase lb 25.6084021152 delta lb -0.3915978848
T2Tbig lb 191.8759875984 delta lb -0.1240124016
ELMo lb 262.1738351232 delta lb 0.1738351232
BERTbase_GPU lb 1433.8822994028 delta lb -4.1177005972
NAS_GPU lb 626155.3061961120 delta lb 0.3061961120
BERT_79_2_sensitivity lb 1437.51238117344 delta lb -0.48761882656
T2Tbase_fixed_hours_rounding True True
T2Tbig_fixed_hours_rounding True True
ELMo_fixed_hours_rounding True True
BERTbase_GPU_fixed_hours_rounding False False
NAS_GPU_fixed_hours_rounding True True
```

作者判断：有原文支持“显示时长的精度可解释该差异”，但没有作者计算底稿，不能认定作者内部必定采用79.2，更不能由兼容性推断测量或跨硬件外推正确。保留79小时失败，再另列79.2敏感性检查，避免改输入后冒充原检查通过。

## 同一方法迁移到本地输入，哪里必须停止

合计IT功率1.51543 kW×84h＝127.29612 kWh；按论文PUE条件估计设施能量201.1278696 kWh。若另一个201 kWh已覆盖同次训练、同时间段和对应设施边界，就直接使用，不能再乘PUE，也不能与IT电量相加。

历史因子下，201×0.954＝191.754 lb；当地实际排放仍未知，因为任务没有提供地点、时间与适用排放因子。若IT功率实际只测了GPU，或设施电表还包含其他作业，边界必须先补齐。数字接近1.58不能单独验证真实PUE。这是方法的适用条件，不是再加几个小数位就能解决的缺口。

## 读者怎样重做同一阅读

先打开上述原PDF，同时保留任务和Skill。若使用有本地文件工具的AI助手，可建立新的空工作目录：把PDF放在`INPUT/paper.pdf`，任务全文保存为`INPUT/task.md`，复制冻结Skill目录，然后使用上面的原会话指令。只提供这些材料，保留新提示、输出和工具记录；不要把旧报告当输入。新的AI可能走不同步骤或给出不同措辞，这不是原输出逐字重放。

本包的`prepare_case.py`在新目录放入与原会话相同的PDF、实际任务、冻结Skill和原提示，不复制旧答案；具体环境与步骤见[复做说明](REPRODUCE.md)。原模型准确快照未知，新的模型会话可能给出不同措辞或结果。本次未执行新独立模型运行。

阅读完后，至少检查：626155的单位与预算；BERT79小时的失败及79.2小时上下文；TPU缺项不能当零；201kWh设施电量不能重复乘PUE。按照这些内容核查新回答，不要求复制账本格式。AI若说“原论文算错了”，却不读第3页，就尚未完成本案例最关键的核查。

如果只想复核旧结果，执行`python3 recheck.py`：它重跑原核算器，逐项比较全部25条结果与原件，并保留BERT名义比较失败、partial和unknown。它不调用模型，也不独立验证论文的底层测量。

## 这份实践究竟证明了什么

它展示了如何把一个容易传播的错误引用追到单位、预算、硬件情景与估计链，并怎样处理“表格算不回去”的情况。可复用之处是具体核查路径和停止条件。

本作品只分享一个完整阅读问题，不评价Skill相对无Skill的稳定收益，不声称提速。原论文、真实会话、原始计算器与输出来自既有项目；本次贡献是把原文条件、实际AI操作、完整数值失败和可复做步骤整理为独立教程。构造的本地功率/电表数据不是论文观测或生产测量。来源与许可见[SOURCES.md](SOURCES.md)。

## 新增验证：兼容解释为何不等于找到了原始计算

以上真实AI阅读及其25条结果全部冻结。本节是2026-10-26新增的作者侧确定性计算与工具测试，没有新增独立AI会话，不把代码测试视为论文实验或模型对照。

### 从显示值反推允许范围

只有“79.2可以算回去”还不足以确定原因。我们独立实现[inverse_check.py](inverse_check.py)，不调用原核算器。在固定功率12041.51W、PUE1.58、排放因子0.954lb/kWh，并假设表中整数各有±0.5显示舍入范围时，分别反解时长：

- 能量1507允许79.1828444–79.2354052小时；
- 排放1438允许79.1993179–79.2544130小时；
- 两个约束交集为79.1993179–79.2354052小时，包含正文79.2，排除表中79。

但固定79小时、反解PUE，两个约束交集又为1.58398636–1.58470810；例如1.5841也兼容。后者只是合成反事实，没有原文支持作者用过这个值。前者有PDF第3页正文支持，故是更有依据的解释。两组结果一起说明：显示值只能约束参数组合，不能唯一识别内部计算。必须把“兼容性”和“原文支持”分别回答。完整精度、假设和断言见[实际输出](evidence/inverse-check.json)。区间是保守封闭舍入边界，不是测量不确定度或置信区间。

### 可复用Skill的真实失效与修复

新增[Skill v1.1](skill-v1.1/SKILL.md)，保留[历史v1.0](skill/SKILL.md)不变。发现的实际问题是组件列表包含`null`时，旧核算器调用`.get`产生AttributeError，整个批次终止，包括后续本来有效的记录。新版本仅增加组件对象类型检查，将坏记录标记invalid，并继续核算其余记录；未把错误输入自动猜成零或删除。

同一套[22项测试](skill-v1.1/tests/test_boundaries.py)在两版分别执行：[旧版实际结果](evidence/boundary-v1.0.json)20/22，[新版实际结果](evidence/boundary-v1.1.json)22/22。两个旧版失败分别是异常返回和坏记录隔离，来自同一根因，不是两个独立缺陷。

测试期望来自手算的1kW×2h×1.5=3kWh、3×0.4=1.2kg及显式输入合同，覆盖W/kW、分钟/小时、g/kg等价、每设备求和、重复GPU数、设施PUE、缺失数据、非有限数、布尔值、负数、设备数量与分摊边界。分时例子另证：1kWh×0.2+3kWh×0.8=2.6kg，任取强度算术均值×4kWh只得2kg。它是合成反例，不能当成本论文观测。

这些结果支持输入健壮性修复，不支持“阅读准确率提升9.1个百分点”。同一测试集也是开发用例，未做盲测、未测模型行为泛化。计算器仍不检测跨行设备/时间重复归因，也不能验证转录和科学语义；新版Skill明确要求人工检查这两个出口。

执行以下步骤可重做新增计算，而无需联网或模型账号：

```sh
python3 inverse_check.py
python3 skill-v1.1/tests/test_boundaries.py
python3 skill-v1.1/tests/test_boundaries.py skill/scripts/audit_energy.py
```

最后一条预期退出1并列出两个失败，这是保留的旧版缺陷，不应通过修改预期使它变绿。历史25条复算仍使用`python3 recheck.py`，与新增测试分开。读者的新AI会话可自行选择v1.1；原历史会话实际使用的是v1.0，不能回填新工具。
