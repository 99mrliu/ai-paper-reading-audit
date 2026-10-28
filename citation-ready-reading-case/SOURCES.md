# 来源、版本、授权与本次贡献

主论文：Emma Strubell、Ananya Ganesh、Andrew McCallum，Energy and Policy Considerations for Deep Learning in NLP，ACL2019，pp.3645–3650，P19-1355。来源 https://aclanthology.org/P19-1355/ ，PDF https://aclanthology.org/P19-1355.pdf 。ACL该文为CC BY4.0，保留署名与出处。INPUT/paper.pdf是未改字节的完整6页原件，SHA256：184c42b148a3db99f4a59ed8336c403dc2229bf3100bbc934212116acd8c61d9。out/source-page-2.png、source-page-3.png、table3-page4.png是原PDF第2、3、4页渲染，保留上下文。

2026-10-27新增：玻尔科学空间同一文献两个新建可见会话的首答A/B，以及B内一次后续来源诊断。运行后查验安装版本0.10.12；可见标准模式一致，准确后端模型、采样参数、费用与缓存/记忆隔离未知。问题与流程由作者根据已知失败构造，非盲测。没有把A答案显式交给B，但不能宣称系统级无共享状态。任务中的外部电表201为假设，不是论文或本地实测。

matched/*-final-ax.txt及B-repair-answer-ax.txt是真实UI可见最终答复，保留错误与表格；后一份是完整最终区域选录，不是作者摘要，源快照范围与哈希见matched/provenance.json。三个Python脚本来自实际AI交付文件，原字节复制到包内；每个*author-replay.stdout为作者在本机重执行的结果，不能称模型原运行STDOUT。截图来自本次操作，只有公开论文和本任务，无私人对话侧栏、访问令牌或账户信息。

作者侧AI负责问题、流程、实际操作、原文核查、语义判定、两个独立核算脚本及本文；用户委托改进并发布。不是独立第三方审稿或新科学实验。author-review.json明确拒绝A的唯一性/PDU断言及B从拟合推来源的结论，也保留后续诊断仍过度归因的失败。不将代码执行成功、修订或通过检查说成全答案正确。

继承材料：out/、skill/、INPUT/task.md、prompt.txt、session.json等来自此前真实Codex会话，固定90分源commit cd0fe0fab5f6be053b58057c826003a62f3b9c6c的forward-reading-case。它不是本次新实验；完整报告、11条账本、unknown/partial和名义失败均保留。skill及作者核算为本项目贡献，不自动获得论文或玻尔商标权；与论文原文、玻尔原输出分开标明。

本次贡献是受限的同题首答实践、冻结检查、共同参数来源反例与可复做方法。未做随机化、重复采样、跨论文或盲评，不声称模型普遍更准/更快/更便宜，也不主张提出的流程已经普适。论文原始日志、作者底稿、逐行功率来源和外部电表条件仍缺。

本次另查AAAI2020同作者扩展文章（DOI10.1609/aaai.v34i09.7123），只提供与BERT因子/表值比较直接相关的合法短片段与小裁片，不假定全文再分发权，不随包分发完整2020PDF。官方来源、版本、原PDF哈希和位置见version-check/source-record.json，作者概述与原文短片段分开。新增玻尔追加问题仅收到该有限材料，不声称读过2020全文；它不加入原A/B首答比较。
