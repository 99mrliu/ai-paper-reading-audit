from pathlib import Path
p=Path('out/report.md')
s=p.read_text()
intro='''# 课程平台适配判断（中文阅读报告）

建议有条件采用 scikit-learn 的接口与组合设计组织课程平台；总体为“需改造”，即补齐数据处理、评价与工程验收流程。论文的中等规模定位与本任务可装入内存的表格数据相符，但尚不能据此保证具体课程数据的运行效果。[C1、I1]

“所有算法都最快，而且适合超大规模在线训练”不能以本文为证据：表1有反例，正文承认大问题上的性能限制，online learning 被明确列为未来工作。[C8—C11、I2]

## 接口与教学流程

事实：estimator 用 `fit(X, y可选)` 学习；监督估计器可用 `predict`，transformer 用 `transform` 输出变换后的输入。接口靠约定而非强制继承（PDF p.3：“inheritance is not enforced”）。`score` 是越大越好的评价，可以是对数似然或负损失，不能一律解释为准确率。[C2、C3]

事实：交叉验证迭代器产生训练/测试索引对，文中举K-fold、留一及分层划分。GridSearchCV 在 `fit` 时搜索指定网格、用交叉验证最大化底层估计器的分数，可选多核；调优后继续以估计器方式提供相应方法。Pipeline 把多个变换与估计器组合，可共同调参（PDF p.4：“GridSearchCV therefore tune the parameters of all steps.”）。某些估计器还可用热启动、正则化路径加速交叉验证，例如LassoCV；不能假定所有算法都具备这种优化。[C3—C5；p.4邻文]

推断与建议：课程可以统一“预处理→模型”的接口，把组合对象交给选参和评估模块；需要学习数据统计量的预处理应在训练折内拟合，另留独立测试集或外层评估，不能把调参最优分数直接当作最终泛化表现。该防泄漏与评估建议是工程推断，不是本文已验证的课程流程。[I1]

## 表1与相邻段落的审读

以下均是PDF p.4表1的Madelon计时，单位为秒，越小表示这次实验运行时间越短。正文给出 **4400个样本、500个属性**，原文为“4400 instances and 500 attributes”。这是有限规模的单个基准，不是流式或超大规模实验。[C6—C8]

| 算法 | scikit-learn | 比较对象 | 可支持的判断 |
| --- | ---: | --- | --- |
| Support Vector Classification | 5.2秒 | mlpy 9.47秒；pybrain 17.5秒；pymvpa 11.52秒；mdp 40.48秒；shogun 5.63秒 | 本行列出的实现中用时最短 |
| k-Means（9簇） | 1.34秒 | mlpy 0.79秒；shogun 0.68秒 | 明确反例：并非所有算法最快 |
| k-Nearest Neighbors | 0.57秒 | pymvpa 0.56秒 | 也未占优；微小差异没有重复试验/方差证据支持稳定排名 |

表注短证据：“Time in seconds on the Madelon data set”。行列归属已人工对照保存的 `page4.png` 和 `page4-layout.txt`；普通平面文本把表格按列展开，字面核验本身无法证明算法与数值对应。表中的“-”指未实现，“⋆”指1小时内不收敛，不能当作零耗时或准确率结果。论文没有在所供正文中充分交代完整公平比较配置，故这些秒数不能保证今日性能或其他数据上的排名。[C7、C8、U2]

相邻说明把SVM优势归因于绑定避免复制及对libsvm的修改；“up to 40% less overhead”指相对原始libsvm Python绑定的开销减少，不能读成所有模型端到端快40%。Elastic Net 在中等规模上与Fortran glmnet为同一量级，超大问题受限于未用KKT条件定义活跃集；k-means当时纯Python实现，数组操作多遍扫描数据限制性能（PDF p.5：“numpy’s array operations take multiple passes over data”）。[C9、C10；SVM解释见p.4]

PDF p.5结论原文：“Future work includes online learning, to scale to large data sets.” 因而在线学习在该处属于未来方向，不能引用成已经完成的超大规模在线训练能力；也不把这一句扩大解释成当时任何单个组件都绝无增量能力。[C11]

## 时间边界与采用前补查

2011年文章支持历史上的统一接口、组合调参思路及限定条件下的计时事实。它不能确定今天的实现语言、默认参数、并行行为、增量学习支持或性能。没有当前文档和代码快照，这些保持未确定，不用历史实现描述替代当前事实。[U1]

采用前应锁定拟用版本，补读其官方API、用户指南、发布说明及必要源码，确认模型与预处理支持的数据类型、评价和交叉验证行为、在线/增量接口适用范围；再以课程代表性数据和硬件验收时间、峰值内存、预测质量及完整网格成本。历史比较若要复核，还须取得对应benchmark脚本及库版本、硬件、线程、超参数、停止条件、计时范围和重复次数。以上是后续所需材料，本次未取得、未联网、未运行模型。[U1、U2]

下附按所供skill生成的完整证据与迁移记录。机械核验为13条正向主张定位通过、2条UNKNOWN警告、0失败；**这不证明科学语义正确**。仍未解决的问题是当前版本状态和原始基准配置。一次辅助读取路径错误也保存在操作记录中。

---

'''
p.write_text(intro+s)
Path('out/audit-notes.md').write_text('''# 操作与人工语义复核记录

- 使用所供skill/SKILL.md、claims-schema.md及三个脚本；未修改INPUT或skill，未访问工作目录外文件、联网、委派或运行模型。
- build_index成功，6页均有可读文字。保留原始索引out/index/。
- 辅助读取失败：尝试cat out/index/pages.json，退出1，错误为No such file or directory。原因是实际输出文件为pages.jsonl；随后按正确路径读取成功。此失败不是证据核验失败。
- 使用pdftotext -layout与pdftoppm生成PDF第4页版面文本及PNG；目视核对表头、SVC、kNN、k-means各行与列。索引的flat文本不保留二维表格关系。
- verify_claims首轮：15条记录，13条正向定位，0失败，2个UNKNOWN警告。没有需要隐藏或丢弃的失败核验轮次。
- render_report成功，之后在报告前添加中文综合判断；未修改claims/index/verification。综合部分已对照对应证据与PDF相邻段落人工复核。
- 人工复核重点：秒数不等于预测质量；单基准非普适排名；近邻微小差异无显著性结论；40%为绑定开销非端到端加速；在线学习为未来工作；历史纯Python描述不外推今天；未由关键词检索断言科学语义不存在。
- 未解决：历史benchmark完整配置、当前版本行为、本课程实测性能。补查方案见报告和claims.json。
- 工具成本：11次functions.exec调用（含本次），其中1次调用读取本地图片；未使用外部服务或模型运行。无法从现有工具获得精确token/货币成本。
''')
