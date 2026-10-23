# 论文能耗、单位与预算审计 Skill 1.0.0

用于阅读能耗/碳排定量论文、复算其表格、审查用户引用与计量迁移。无需网络、嵌入数据库、额外LLM、训练服务或付费解析API。目录中的真实运行是评分证据；脚本不代替科学语义判断。

## 环境与入口

原环境macOS Apple Silicon，Python3.14.7、Poppler26.08.0（pdftotext/pdftoppm）、Codex CLI0.163.0-alpha.11.1及其本地图像查看能力。Skill计算代码只依赖Python标准库；阅读PDF还需宿主现有PDF工具，例如Poppler，可用其他工具但须记录差异。单独调用计算脚本不需要Codex账号；重新跑AI对照需要已认证且可用的模型服务，费用无法从本轮导出取得。

向Agent提供论文PDF和具体阅读问题，并让它使用 `skill/SKILL.md`。按其中引用的 `skill/references/ledger.md` 转录账本，再运行：

```sh
python3 skill/scripts/audit_energy.py ledger.json --out calculations.json
```

量纲或边界错误退出2；缺数据可返回unknown/partial，不能仅以退出0宣告完整科学验证。来源、单位、设备合计/PUE边界须由读者确认；不自动OCR或下载缺失材料。

## 案例与完整记录

- A：ACL2019原论文6页；同一任务对照两组独立会话，核验五行能耗表、训练/NAS/R&D口径、用户引用与本地测量边界。
- B：JMLR2020原论文43页；共享机器分资源归因和分时碳强度，使用明确标注的合成用户测量，不冒充论文实验数据。
- C：原创合成不完整测量PDF，缺单位、设施边界与排放因子，检验合理降级，两次独立复测。

原PDF、逐页文字、来源页与共享说明在materials/；任务和事先标准在cases/，冻结哈希在cases/preregistration.json；逐次原始事件、stderr、任务prompt、session统计和输出在runs/。开发的两次工程失败与修正在development/披露，18项工程不变量不算18次阅读成功。

每个阅读会话独立目录、ephemeral/ignore-user-config、同一CLI默认模型选择，30次调用/900秒共同预算，不共享中间答案；实际预算执行按原始日志核查。with额外获得冻结Skill与资源；without保留相同普通工具，允许编写自己的计算代码、抽取和看图。两种条件都无网络、外发或其他模型调用。采集器的with提示还要求保留其核验/主张产物，属于with成本，不用这类额外产物本身证明增益。

准确服务端模型快照未在JSONL公开，无法确认严格锁定；宿主工具版本已记录。duration包含模型服务、启动、重试及共享机器负载，不是隔离性能基准。token为原生usage，cached是input子集；费用未知，不从token编造金额。

用户给出目标与“上传前确认”的约束。作者侧AI选题、写Skill/代码、准备任务标准、启动独立CLI会话并阅卷；没有真人科学纠正、第三方复现或人工补做核心阅读。独立CLI是行为复跑，不是独立第三方评审。

## 新目录复跑

在作品根目录，指定尚不存在的目标路径：

```sh
python3 reproduce_tests.py --destination ./fresh-runs --jobs 2
```

可用 `--runs A1-with A1-without` 只跑一组；不改写原runs/。必须记录新环境、模型设置和依赖差异；本轮结果不承诺跨服务/机器一致。工程检查运行：

```sh
python3 development/test_invariants.py
```

report.md按同一事先标准报告原始差异、实际开销与局限；assessment.json给出作者侧AI核查索引，manifest/review.json为本题工具验证的提交索引。本作品未承诺官方分数或奖金，不包含令牌，不执行上传。
