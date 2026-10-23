# 操作与人工语义复核记录

- 使用所供skill/SKILL.md、claims-schema.md及三个脚本；未修改INPUT或skill，未访问工作目录外文件、联网、委派或运行模型。
- build_index成功，6页均有可读文字。保留原始索引out/index/。
- 辅助读取失败：尝试cat out/index/pages.json，退出1，错误为No such file or directory。原因是实际输出文件为pages.jsonl；随后按正确路径读取成功。此失败不是证据核验失败。
- 使用pdftotext -layout与pdftoppm生成PDF第4页版面文本及PNG；目视核对表头、SVC、kNN、k-means各行与列。索引的flat文本不保留二维表格关系。
- verify_claims首轮：15条记录，13条正向定位，0失败，2个UNKNOWN警告。没有需要隐藏或丢弃的失败核验轮次。
- render_report成功，之后在报告前添加中文综合判断；未修改claims/index/verification。综合部分已对照对应证据与PDF相邻段落人工复核。
- 人工复核重点：秒数不等于预测质量；单基准非普适排名；近邻微小差异无显著性结论；40%为绑定开销非端到端加速；在线学习为未来工作；历史纯Python描述不外推今天；未由关键词检索断言科学语义不存在。
- 未解决：历史benchmark完整配置、当前版本行为、本课程实测性能。补查方案见报告和claims.json。
- 工具成本：9次functions.exec调用（含最终文件检查），其中1次调用读取本地图片；未使用外部服务或模型运行。无法从现有工具获得精确token/货币成本。
