# 从原文、AI 输出到可复算结果

下面分为离线核对与重新运行 AI 两条路径。前者不需要模型账号；后者会调用读者自己的模型服务。

## 1. 离线核对：不安装依赖、不联网

在仓库根目录使用 Python 3.11 或更新版本：

```sh
python3 quick_check.py
```

预期返回 `status: passed`、`original_sessions_verified: 14`，并复算保存账本中的 25 条记录。它校验 14 份原始会话统计的哈希、真实耗时和 usage，重新汇总两组实验各自的配对结果，再调用随附原始核算器比较保存的计算输出。它不写回原始记录，也不重新调用 AI。

关键复算预期：

| 输入 | 设施能量 kWh | 历史因子下 lb |
|---|---:|---:|
| BERT 表内 79 h | 1503.0212782 | 1433.8822994028 |
| 正文条件 79.2 h | 1506.82639536 | 1437.51238117344 |

第二行取整兼容表中的 1507 / 1438。它支持一种上下文解释，不证明作者实际计算底稿，也不代表本地硬件测量或今天的碳排因子。

输入来自 [A1-with 原始账本](experiments/energy/runs/A1-with/out/ledger.json)，保存结果为 [calculations.json](experiments/energy/runs/A1-with/out/calculations.json)。所有 25 条记录包括名义值、条件舍入变体和缺项案例，不是 25 个独立测量或论文实验。

## 2. 亲自检查原文与解读

1. 打开 [ACL2019 原 PDF](experiments/energy/materials/acl-energy.pdf)，PDF 第 4 页（印刷页 3648）Table 3。确认 Power、Hours、能耗和 lb 的列归属，尤其整机配置和缺失的 TPU 项。
2. 对照 PDF 第 3 页正文的 79.2 小时说明，再看上面的两个复算结果。页级文字导出与原 PDF 一起保留在 `experiments/energy/materials/`。
3. 分别读 [A1 有 Skill](experiments/energy/runs/A1-with/out/report.md)与 [A1 无 Skill](experiments/energy/runs/A1-without/out/report.md)。两边都应按相同标准检查，不能把只有一边拥有 JSON 当成准确率优势。
4. 看 [A2 有 Skill](experiments/energy/runs/A2-with/out/report.md)和 [A2 无 Skill](experiments/energy/runs/A2-without/out/report.md)，确认首次观察到的省时没有在复测中保持。
5. 阅读 [事先验收标准](experiments/energy/cases/A/acceptance.md)、[固定任务](experiments/energy/cases/A/task.md)和 [作者侧 AI 核查记录](experiments/energy/assessment.json)。核查记录不是独立人类评审。

## 3. 单独调用原有核算器

```sh
python3 experiments/energy/skill/scripts/audit_energy.py \
  experiments/energy/runs/A1-with/out/ledger.json \
  --out /tmp/paper-reading-energy-recheck.json
```

预期 25 条账本记录，无 invalid 输入，部分缺项可以是 unknown/partial。退出 0 只表示未发现非法账本输入，不能代替原文转录、列归属或科学语义核验。

## 4. 在新目录重新运行 AI

原实践环境为 macOS Apple Silicon、Python 3.14.7、Poppler 26.08.0、Codex CLI 0.163.0-alpha.11.1。准确服务端快照和账单没有从导出取得。采集脚本依赖原来的 macOS Codex 路径；其他宿主先按自身环境适配，记录差异。不要把已有绝对路径当通用安装位置。

读者有可用 Codex 账号、PDF 工具并核对路径后，可在对应实验目录运行：

```sh
cd experiments/energy
python3 reproduce_tests.py --destination ./fresh-runs --jobs 2 --runs A1-with A1-without
```

目标目录须尚不存在；不覆盖保存的 `runs/`。该步骤会调用模型服务，耗时和账单属于新的运行。新结果应使用同一任务和标准记录；不能把本地旧结果复制成新实验。完整说明见各实验 README。

## 5. 如何解释检查结果

哈希相等证明所核查文件一致；算术相等证明代码对录入账本的复算一致；原文语义要结合上下文判断；相对收益要由同条件对照支持。四者分别成立，不能相互替代。
