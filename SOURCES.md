# 来源、授权与本次贡献

| 材料 | 来源 | 包内位置及共享说明 |
|---|---|---|
| Random Search for Hyper-Parameter Optimization（Bergstra & Bengio, 2012） | https://jmlr.org/papers/v13/bergstra12a.html | `experiments/transfer/materials/random_search.pdf`；JMLR 公开 CC-by 政策，保留作者与出处 |
| Scikit-learn: Machine Learning in Python（Pedregosa 等，2011） | https://jmlr.org/papers/v12/pedregosa11a.html | `experiments/transfer/materials/`；同目录来源说明与原件 |
| Energy and Policy Considerations for Deep Learning in NLP（Strubell 等，2019） | https://aclanthology.org/P19-1355/ | `experiments/energy/materials/acl-energy.pdf`；CC BY 4.0，保留作者与出处 |
| Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning（Henderson 等，2020） | https://jmlr.org/papers/v21/20-312.html | `experiments/energy/materials/`；JMLR 公开 CC-by 政策 |

原 PDF 未修改；逐页文字和页面图片是定位辅助，不替代原件。原出版方许可说明、取得时的来源快照和具体版本见两个实验的 `materials/source-and-rights.md`。第三方材料保留原许可，本项目不将原创代码的使用条件覆盖到论文。

本次分享复用本项目已经完成的两轮论文阅读实践、14 次独立 CLI 会话和原始 Skill。新增贡献是跨案例技术分析、材料导航、四层核验方法的解释，以及 `quick_check.py` 的离线复算入口。新的离线检查属于既有结果复核，没有新增论文阅读实验。

用户提出任务方向和约束，AI 完成代码、阅读、核查和文章整理。作者侧 AI 的核查不冒充人类科学审阅或独立第三方复现。B 的用户测量数据、C 的异常材料明确为合成；不声称真实生产测量。

本作品未使用玻尔科学空间完成论文阅读，不申报该项实践经验或其 10 分生态贡献。比赛网页和提交 CLI 的使用本身不冒充科学空间实践。

本次没有引入第三方 Skill 代码依赖。更多来源和采集器导出边界见 [原生记录说明](verification/native-export-limit.md)。
