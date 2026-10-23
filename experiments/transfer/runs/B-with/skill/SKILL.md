---
name: paper-transfer-audit
description: Read a quantitative methods paper against a specific research use case, locate its supporting evidence, distinguish facts from inference and missing information, and assess transfer conditions. Use for method applicability and source-checking, rather than general summaries or executing a reproduction.
metadata:
  version: "2.0.0"
---

# 论文方法适配与证据审计

把论文中的方法、实验条件、证据强度和用户的实际需求联系起来。交付可核查的阅读判断；机械核查通过不等于科学结论正确。

## 输入与范围

需要论文 PDF，以及用户拟解决的问题、自己的数据/平台条件。补充材料、图表原件和具体关注点按任务提供。目标缺失且会影响判断时先澄清；能完成的证据阅读可先进行。

只根据实际取得的材料作判断。执行论文分析、部署、训练、发消息或公开投稿不属于本 Skill 的阅读任务。

## 阅读和核查

1. **确认材料。** 列出已提供与未提供的正文、补充材料和版本。运行 `python3 <skill>/scripts/build_index.py paper.pdf --out index`。页码指 PDF 第几页，从1开始。已知为节选时加 `--scope excerpt`，已知完整页数时可加 `--expected-pages N`。索引只证明现有页，不能自行证明论文完整。
2. **围绕用户需求阅读。** 先从实际问题列关注项，再检查方法输入输出、数据划分、指标含义、比较对象、关键参数、负结果和作者的限制。阅读图注和相邻上下文；同一个数在不同实验中不能混用。需要时用可用 PDF 图像查看工具核对图表。不要把截图中估读的值写成精确测量。
3. **写证据记录。** 按 `references/claims-schema.md` 写 `claims.json`，同时覆盖用户所需的主要解释和适配判断。FACT 用原文直陈；INFERRED 写推理链，数值推断另列可复算式；UNKNOWN 表示在声明的材料和检索范围内尚未确定。引文从实际索引复制，可被多条结论共用，但每条须独立解释其成立条件。
4. **核查与修正。** 运行 `python3 <skill>/scripts/verify_claims.py --claims claims.json --index index --out verification.json`。失败时回到原文纠正引文、页号、分类或算式，保留重试。脚本仅检查定位、字面值、引用关系和算术；必须另审阅语义支持、适用对象、时间/空间范围、统计指标和因果措辞。数值出现在附近不代表支持该结论。
5. **形成迁移判断。** 逐项给出“可直接用 / 需改造 / 不可用 / 信息不足”，引用证据ID并解释用户条件与论文条件的关系。材料不足不能直接推成“不适用”，实验未验证也不能写“保证有效”。总体可用性须与各环节一致。给出为解决现有缺口而需要补读的具体来源或要确认的问题；尚未取得的材料只能作为查找建议。
6. **生成交付。** 运行 `python3 <skill>/scripts/render_report.py --claims claims.json --verification verification.json --index index --out report.md`。渲染器拒绝失败或与当前材料不匹配的旧核验。交付报告、claims.json、verification.json及索引；必要时附图表截图。报告须解释方法为何相关、关键结论依赖什么条件、用户下一步能据此作什么判断。不要把“脚本PASS”当语义正确率。

## UNKNOWN 的处理

为尚未确定的项写具体 `absence_probe` 检索词、`search_scope`（例如所供正文PDF，不含补充材料）及 `reasoning`。脚本实际执行检索，返回命中页和上下文。

关键词零命中不证明作者没有讨论；关键词命中也不保证回答了目标问题。阅读命中上下文并解释缺口，避免“搜不到某个词→整篇论文不存在这个事实”。部分材料中的缺口不得扩大成整个研究的缺口。

## 异常出口

- PDF无可读文本：索引返回 `insufficient_text` 和退出码2。若无已获授权且可核查的OCR路径，停止定量解读，交付材料状态、尚不能回答的问题和获取文本/OCR的建议。若已有OCR结果，可明确其来源与识别局限后另行审阅；本版脚本不自动OCR。
- 输入损坏、路径无效或抽取工具失败：保存错误，提供恢复方法，不生成成功审计报告。
- 缺页/缺补充材料：继续已提供范围的阅读，标明受影响结论，暂缓缺证据的判断。
- 预算结束：保留已完成输出与未核验清单；不得为了完成报告补写事实。

## 交付检查

- 关注项有对应证据或明确缺口，避免只核查“已经写出来的数”而漏掉任务主干。
- 图表与主张的比较对象、数据划分、指标和条件相符，保留反例及不利结果。
- 每项迁移建议可回到证据和用户实际条件；假设、外推和不确定性可辨识。
- 原件、原始输出、修正、工具成本和无法取得的信息如实留存。文本抽取与语义解释的限制分别说明。
