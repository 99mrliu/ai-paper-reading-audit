# claims.json v2

顶层 `paper` 记录标题、来源、目标问题和 `limitations_of_this_audit`。
`claims` 至少一条，所有 claims/parameters 的ID非空且不重复。结构：

```json
{
  "paper": {"title": "实际标题", "doi": "实际DOI或空", "question": "用户的研究判断问题", "limitations_of_this_audit": ["实际材料限制"]},
  "claims": [
    {"id": "C1", "class": "FACT", "statement": "解释原文事实", "value": "0.86", "page": 2, "source": "Results", "quote": "从索引复制的连续原文", "conditions": "指标、数据划分、比较对象和适用条件"},
    {"id": "U1", "class": "UNKNOWN", "statement": "现有材料未能确定的问题", "value": null, "absence_probe": ["具体检索词", "相关词"], "search_scope": "所供正文PDF，不含补充材料", "reasoning": "已查范围和为什么尚不能作判断"}
  ],
  "parameters": [],
  "derivations": [],
  "coverage": [{"item": "用户要求的一个关注项", "status": "covered", "claim_ids": ["C1"]}],
  "transfer": [{"step": "与实际目标相关的环节", "verdict": "信息不足", "because": ["C1", "U1"], "needs": "为作判断还要确认什么"}],
  "verdict_overall": "信息不足",
  "gaps": [{"gap": "缺口", "impact": "对用户判断的影响", "close": "具体后续阅读或确认方向"}],
  "boundaries": ["本次判断的适用边界"]
}
```

上例仅说明结构，使用时替换为实际内容；不得把示例句当证据。

FACT 和 INFERRED 都需要 `page`、连续 `quote` 与解释。页号为输入PDF页号。规范化仅合并空白与Unicode兼容字符，不允许拼接不同句子充当连续引文。数值事实必须出现在引文本身；百分号与非百分号区分，17不匹配2017。数学等值不代表实验口径等价，需要阅读上下文。

INFERRED 需要 `reasoning`；若 value 非空，还须引用 `derivation_id`。对应 `derivations` 项有 `id`、`expr`、`expected`、`source_claims`、可选 `absolute_tolerance`（默认0.05，最大0.5）。source_claims 指向记录原始操作数的 FACT；表达式额外允许0、1、100作为常见算术常数。逻辑推断可令value为空并解释推理，不强制数字算式。

UNKNOWN 的检索只提供命中位置和供阅读的上下文，始终保留警告，不能由机械匹配证明语义不存在。

`coverage.status` 可用 covered/not_found/out_of_scope；covered须关联已有claim_ids。`transfer.because` 支持ID数组；每个ID必须存在且未机械失败。overall为“可直接用”时不能含需改造、不可用或信息不足环节。

运行 `verify_claims.py` 得到绑定 claims/index/pages 文件哈希的 verification.json。脚本有失败时退出1；render_report.py拒绝失败或过期核验。修改任何证据后重新核验。全部机械检查通过仍需审阅结论的语义、材料覆盖和迁移判断。
