# 复算与重新阅读

## 复算既有结果

Python3.11+标准库，在包根运行`python3 recheck.py`。它校验来源哈希，调用冻结核算器，并将输出与原calculations.json全部比较。预期25条记录：23条ok、1条partial、1条unknown，无invalid；BERT固定79小时的能量和排放舍入比较均失败。这些失败必须保留。原始ledger_sha256绑定原账本字节，不只比较表面数字。

独立调用原工具：`python3 skill/scripts/audit_energy.py evidence/ledger.json --out /tmp/energy-recheck.json`。退出0不等于所有数值比较通过，更不等于论文或测量语义已经验证。

## 重做同一个AI阅读

运行`python3 prepare_case.py --destination /tmp/fresh-energy-reading`，目标须不存在。只复制原始完整PDF、原任务、冻结Skill及实际提示，out为空。在新的、有本地文件/Python/PDF工具的AI会话中打开该目录，使用prompt.txt全文，保留自己的模型、环境、命令、失败与报告。不复制旧报告充当新输出。

原环境为macOS Apple Silicon、Python3.14.7、Poppler26.08.0、Codex CLI0.163.0-alpha.11.1；模型为当时CLI默认，准确快照和账单未从导出取得。本次未新增完整AI运行，不承诺跨模型逐字复现。新读者可用自己的工具可调用AI，按同样任务核查内容，不要求相同表述或账本数量。

检查原PDF第1页Table1的单位/预算，第2页方法公式和测量范围，第3页GPU情景79.2h，第4页Table3/4及脚注。用表内79h算不回整数能耗和排放，应保留失败再另列有原文依据的79.2h情景；不能把未知TPU功率当零，设施电量不能重复乘PUE。

原build_ledger.py最初构建20条，后由实际操作item_7增加固定小时变体到25条；不能仅重跑初始构建脚本就声称重建了最终账本。最终输入、输出及完整修正操作均在evidence/。

## 文本容量

`python3 check_text_budget.py`需要Poppler的pdftotext；逐个统计全部UTF-8文件，PDF取-layout与-raw两种提取结果的较大字节数，再加8KiB转换余量。PDF只有6页、约216KiB文件大小。该保守预算不是压缩ZIP大小。未把完整PDF和重复提取全文同时放入材料。
