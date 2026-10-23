# AI 读论文的四层核验

从 BERT 能耗表到 14 次独立会话：把原文定位、算术检查、语义判断和实际收益分别验证。

两个论文阅读Skill、四组公平对照、14次真实独立会话。方法迁移审计平均慢42.5%，能耗审计平均慢12.1%，没有发现稳定的实质阅读质量收益。研究的价值是揭示“增加核验能力”与“减少读者投入”之间的差别，并给出可以复算的真实例子。

这是一份有原始证据和离线复算入口的技术实践分享。四组公平对照用于检验收益，结果与限制逐项保留。

## 先运行一个不需要模型账号的核查

```sh
python3 quick_check.py
```

只依赖 Python 标准库，核对 14 份原始会话统计、四组配对结果，并重算保存账本中的 25 条记录。预期输出 `status: passed`，BERT 的 79 h / 79.2 h 分别对应 1503.0212782 / 1506.82639536 kWh。详细路径和预期结果见 [复算教程](REPRODUCE.md)。这是既有结果的离线核查，不会调用 AI 或覆盖原始记录。

## 阅读顺序

1. [技术文章](ARTICLE.md)：阅读问题、证据核对、BERT表格时长差异、代码取舍、公平性与负面结果。
2. [离线复算教程](REPRODUCE.md)与[结果复算](verification/results.json)：由14份原始session.json汇总，附文件哈希；运行`python3 verify_results.py`可重算。
3. [方法迁移完整报告](experiments/transfer/report.md)与[能耗完整报告](experiments/energy/report.md)：细化任务和逐项作者侧AI核查。
4. 两套[方法迁移使用/复跑说明](experiments/transfer/README.md)、[能耗使用/复跑说明](experiments/energy/README.md)。

## 直接核查关键发现

| 关注点 | 原文/材料 | 实际AI输出 |
| --- | --- | --- |
| Random Search迁移到6参数、36次预算 | [原PDF](experiments/transfer/materials/random_search.pdf)，[任务](experiments/transfer/cases/A/task.md)，[事先标准](experiments/transfer/cases/A/acceptance.md) | [A1有Skill](experiments/transfer/runs/A1-with/out/report.md)、[A1无Skill](experiments/transfer/runs/A1-without/out/report.md)、[A2有Skill](experiments/transfer/runs/A2-with/out/report.md)、[A2无Skill](experiments/transfer/runs/A2-without/out/report.md) |
| 能耗表BERT79与正文79.2小时、NAS lbs引用、PUE边界 | [原PDF](experiments/energy/materials/acl-energy.pdf)，[任务](experiments/energy/cases/A/task.md)，[事先标准](experiments/energy/cases/A/acceptance.md) | [A1有Skill](experiments/energy/runs/A1-with/out/report.md)、[A1无Skill](experiments/energy/runs/A1-without/out/report.md)、[A2有Skill](experiments/energy/runs/A2-with/out/report.md)、[A2无Skill](experiments/energy/runs/A2-without/out/report.md) |
| 两套Skill与可执行代码 | [方法迁移Skill](experiments/transfer/skill/SKILL.md)、[能耗Skill](experiments/energy/skill/SKILL.md) | 每个runs目录保留prompt.txt、events.jsonl、stderr.log、session.json和真实产物 |
| 复用和异常测试 | 各实验cases/B、cases/C与材料目录 | 各实验runs/B-with、C1-with、C2-with中的原始报告 |
| 原文来源与许可 | [JMLR两论文](experiments/transfer/materials/source-and-rights.md)、[ACL/JMLR能耗论文](experiments/energy/materials/source-and-rights.md) | PDF未改，提取文字及页面图片为辅助；C材料明确合成 |

为了保留完整运行现场，两套原始提交材料中的输入、Skill副本和中间产物没有去重。文章不要求联网才能阅读；重跑模型会话需要读者自己的Codex认证与可用模型服务。

## 原文、AI输出和贡献

论文署名与结论归原作者，来源/共享说明见上表。Skill、代码、任务设计、运行采集、文章整理与核查由作者侧AI完成，用户提出方向与约束；没有虚构人类纠错或用户访谈。独立CLI会话是行为复测，不能叫独立第三方科学评审。工程检查通过也不等于论文结论正确。

准确服务端模型快照和账单不可得，明确记为未知。CLI原生JSONL不导出所有内部事件，特别是本轮没有单列image-view事件；可见调用计数不代表全部工具操作，不能据此独立证明视觉接收过程或总调用上限。详见[导出边界说明](verification/native-export-limit.md)。耗时包含服务和共享主机负载，样本只支持这几次观察。某些原始日志保留当时绝对路径，迁移时按本仓库相对入口复跑；不要把日志中的路径当成可在新机器访问的文件。

两套实验中manifest/review索引属于原Skill赛道提交结构；嵌套包自查不替代本GitHub作品的来源审查、公开版本一致性或评分。

来源与本次贡献见 [SOURCES.md](SOURCES.md)。主要阅读、核查与图表证据已随仓库保存，评审无需联网补齐材料。
