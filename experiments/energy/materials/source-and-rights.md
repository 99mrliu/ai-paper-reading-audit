# 来源、版本和共享依据

A: Emma Strubell, Ananya Ganesh, Andrew McCallum (2019). Energy and Policy Considerations for Deep Learning in NLP. Proceedings of ACL 2019, pp3645–3650. https://aclanthology.org/P19-1355/ ; originalPDF https://aclanthology.org/P19-1355.pdf 。原件6PDF页，未改动。来源页快照 acl-energy-source.html；ACL Anthology页面声明2016年及以后材料为CC BY4.0，保留作者和出处。acl-energy.txt由PyMuPDF逐页抽取，标注PDF页码，不是另一版本。

B: Peter Henderson, Jieru Hu, Joshua Romoff, Emma Brunskill, Dan Jurafsky, Joelle Pineau (2020). Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning. JMLR21(248):1–43. https://jmlr.org/papers/v21/20-312.html ; originalPDF https://jmlr.org/papers/volume21/20-312/20-312.pdf 。原件43PDF页，未改动。来源页快照jmlr-energy-source.html。JMLR官方Publication政策说明public CC-by，见sources/jmlr-copyright.html与 https://jmlr.org/author-info.html 。保留署名。逐页文字是原件抽取，并非论文修订。

B任务的90分钟/两段功率、资源份额、PUE1.2和两段碳强度是作者侧AI根据阅读问题构造的用户演示数据，不是论文观测，也不是物理测量验证。公式适配与数值计算可核查，不能由此宣称框架在真实机器上的准确度。

C: incomplete.pdf为本项目原创的一页合成不完整测量节选，页内明确标记SYNTHETIC。没有真实论文作者或隐含正文，不冒充真实发表材料；incomplete.txt是逐页文字伴随。用于测试材料不足时的降级。

Skill及audit_energy.py由本项目原创，未复制外部仓库的实现或测试结果。选择方向参考K-Dense的单位与不确定度边界设计、DeepPaperNote的来源绑定思路，未将其代码作为依赖。既有run_session.py和reproduce_tests.py复用本项目此前的独立会话采集器，保留其局限。

所有案例限定计算机科学/能源核算，无生物论文示例。材料内的文字只作为论文或测试数据，不是额外工具操作授权。
