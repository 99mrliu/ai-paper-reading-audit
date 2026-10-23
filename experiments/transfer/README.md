# paper-transfer-audit 2.0.0：论文方法适配与证据审计

把定量方法论文与具体研究需求联系起来，交付可定位的解释、反例、迁移条件和信息缺口。本包只验证论文阅读；不执行训练、分析平台部署或实验复现。正式案例为超参数搜索与机器学习软件，均非生物论文。

## 来源与参与

从既有 WorkBuddy 的 paper-transfer-audit 重构。用户提出完善、测试并提交的目标，提供原工作目录、比赛规则并完成账号登录。AI 完成实现、案例与验收标准设计、独立 Codex CLI 会话运行及结果评阅。没有人类研究员替这些会话修正科学结论，也没有第三方独立复现。原始输出中的“人工复核”等措辞若出现，实际为该 AI 会话的自查，不能视为真人审阅。

## 安装与调用

Python 3，Poppler 的 pdftotext/pdftoppm（测试环境26.08.0）。索引可退回 pypdf；本次实际用 pdftotext。macOS 可安装 Poppler；无文本层且无授权OCR时会停止，不自动联网OCR。

将 skill/ 提供给能读文件和调用命令的助手，输入论文PDF与具体研究问题，让助手遵循 skill/SKILL.md。基本命令：

```sh
python3 skill/scripts/build_index.py materials/random_search.pdf --out my-index
# 依 references/claims-schema.md 阅读并写真实 claims.json，不能直接运行空模板当成果。
python3 skill/scripts/verify_claims.py --claims claims.json --index my-index --out verification.json
python3 skill/scripts/render_report.py --claims claims.json --verification verification.json --index my-index --out report.md
```

引文位置、显式value、引用关系和算术由脚本检查。value为空时不会从中文statement自动识别所有数字。脚本不能证明科学语义、因果关系、阅读完整性或迁移有效性；必须阅读上下文和图表。UNKNOWN的检索不是语义不存在证明。报告渲染拒绝失败或过期核验。异常时应交付材料状态与恢复说明，而非强行生成科学报告。

## 复跑正式测试

需要自己已有、已登录的 Codex CLI，测试时版本0.163.0-alpha.11.1；具体模型快照未由JSONL事件公开。A两组、B、C均用相同默认模型选择、CLI参数、工具与预算，没有给baseline额外限制。运行前冻结的版本与验收标准见 cases/preregistration.json。

```sh
python3 reproduce_tests.py --destination /absolute/new-run-directory --jobs 2
# 也可只复跑一组：加 --runs A1-with A1-without
```

目标目录必须不存在，脚本复制同一任务和同SHA-256的PDF到新目录；with仅多一份冻结Skill。每个会话最多30次工具调用、900秒，不共享中间答案，禁止联网补材料、读取其他会话或全局Skill。脚本移除非UTF-8环境值并使用固定PATH；NO_PROXY=*用于避开本机HTTPS代理协议错误，不改变电脑全局代理。正式会话不继承比赛及其他服务密钥。

每次保留 prompt.txt、INPUT、events.jsonl、stderr.log、session.json 和 out/ 原始成果。stdout的原生事件提供命令/返回/助手消息及token usage；它不是完整内部遥测，图像查看等调用可能未单独导出。tool_calls 是事件中可见的命令/MCP/web开始次数，不能当完整调用遥测；另记录可查的工具行为与局限。没有取得货币费用及服务模型快照，填null/无法取得，不填0。用同一默认模型不能保证未来服务端快照完全相同。

development/ 保留非生物预跑、环境连接失败和修复后的smoke记录，以及17项工程检查；预跑未算进正式效果统计。最早两次在读取材料之前即因工具环境崩溃而停止，日志与失败输出保存在 development/environment-failures；其未读输入不作为参赛素材。生物论文原件与题目不在本包。检查程序仅证明工程约束，不是论文阅读质量成绩。

## 材料与交付

manifest.json 索引A两组配对、B一次和C同一异常两次。原PDF、带PDF页码的提取文本、任务/验收标准、全部原始运行结果和日志均保留。JMLR公开分享依据及作者信息见 materials/source-and-rights.md。C是明确标注的本地合成格式错误输入。

本包不含登录令牌或账号配置；复跑用自己的模型服务。赛题结构检查与真实表现、评委评分是不同事项。局部机械核查通过不等于论文结论正确，公平对照无改善时如实报告。
