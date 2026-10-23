# 阅读判断：建议采用独立随机搜索作为首版基线

**结论：可以采用，但需要为表格模型重新设计搜索空间与验证协议；总体适配为“需改造”。** 六个参数的重要性未知，又随任务分布变化，随机搜索能避免规则网格把大量预算花在不重要维的重复取值组合上。这是本文机制与实验对首版选择的支持，不是本流程36次训练的胜出保证。本文研究图像分类神经网络和DBN，没有验证我们的表格数据或模型。[I1、U1]

这里的“独立随机”是先规定配置的联合分布，再独立抽取候选，训练后按验证目标择优；不根据已观察到的成绩改变后续采样。混合类别、整数和条件分支时，独立的是各次候选抽样，不能据此要求所有参数无条件相互独立。固定种子、保存分布定义及每次训练记录，才能追溯。其输出是已评估配置中的验证优胜者，不是全空间最优解。[C1、C2、C10、I2]

图1（PDF p.4）是机制示意：横轴重要、纵轴不重要，九点网格在重要轴只有三个位置，九个随机点有九个不同位置；无关轴的变化对响应几乎没帮助。预算不因此自动变成九个独立的“成功机会”：离散值可重复、随机点可聚集，多维交互也可能使好区域很窄。图7的GP敏感性分析及p.15把本文七参数问题的有效维数描述为一至四，并指出重要参数跨数据集变化。我们不知道自己的六维问题是否满足这个结构；若少数重要参数早已确定，或目标区形状与规则网格相配，网格仍可能合理。本文模拟中也有网格最好情况，不能宣布随机普遍最优。[C3–C5、C21、I1]

| 实验 | 搜索对象、空间与预算 | 能支持什么及限制 |
| --- | --- | --- |
| 图5，PDF p.11–12 | 八个图像分类任务；单隐藏层神经网络；无预处理、七参数；随机总池256次，取其中71个无预处理试验；旧规则网格平均100次 | 图注明确说8次随机匹配或超过旧网格；是本文条件下的效率证据，不是每次8抽均成功。作者称搜索区域/密度大致相同，而非严格相同离散候选集合。[C6、C7、C11] |
| 图6，PDF p.11、13 | 加入标准化/PCA的九参数随机空间；对照仍是无预处理、平均100次旧网格 | 扩空间后正文称需32次而非8次稳定胜过旧网格，64次及以上可找到更优配置。图注所说扩展网格平均500次是所需组合数的说明，不是已经完成的500次对照实验。[C8、C9] |
| 图9，PDF p.18–21 | 随机在一/二/三层DBN空间抽样，最多32参数；128次随机对比专家辅助网格；旧DBN-3平均41次，各集13至102次 | 对旧三层结果三差、四平、一优；随机对旧一层结果至少一样好，但随机允许选层数。比较非等训练次数，人工还利用跨任务经验，评分加权口径不同。[C14–C17] |

这些预算首先是**候选模型训练次数**。不同配置的规模、停止时机和耗时不同，不能把“8对平均100次”直接当成统一墙钟加速比，也不能把DBN的128对平均41写成公平等预算胜负。神经网络效率曲线由独立随机试验分组，纵轴是按验证不确定性加权后的测试准确率；大预算时分组数少，用散点表示，不能当成大量新跑的重复搜索。验证集负责选择、测试集负责评估，两者不能混用。[C12、C13、C16、C17]

图9已核对八个面板及红/绿虚线：三层人工对照为红粗虚线，一层为绿细虚线。正文较差任务为 mnist background images、mnist background random、mnist rotated background images；convex 更好，其余四集相当。这里只采用图注与正文的描述，不估读曲线精确值或重新宣布统计显著。**尚未解决的原文矛盾：摘要p.1写七集，图9和p.21列八集。** 本报告保留矛盾，按有逐集列名、与面板吻合的正文汇总；无补充材料可供解释。[C14、C15、C19]

搜索空间和抽样概率直接决定有限预算的机会。论文实际含等概率类别、对数尺度数值、条件预处理等，并非所有参数在线性原值上均匀。所谓好配置区域的大小，应按所选抽样分布的概率质量理解；范围过宽或给坏选项过大概率，会让36次消耗在低价值区域。独立抽样的成功机会取决于好区域所占的概率质量；本文p.16给出人工目标区间的命中概率分析，但该模拟不能提供我们36次训练的实测胜率。我们不知道本流程的好区域概率，也不知道验证高分是否对应所需的泛化表现，故不给数值保证。[C8、C10、C11、C18、I2、U1]

随机搜索与自适应搜索的关系应保留开放：随机搜索提供简单、易并行、可追加预算的比较基线；它不利用历史结果，遇到窄好区域可能持续错过。DBN专家顺序法说明借助反馈与经验可能有益，但不是本文对现代贝叶斯优化器等方法的严格同预算试验。论文推荐把随机作为未来自适应方法的基线，并没有证明自适应不值得做；当年对软件工程难度的讨论也不能外推为今天具体工具的限制。[C18、C20、I3]

首版适配建议（以下为推断与设计建议，尚未执行）：

1. 明确六参数的名称、类型、合法组合、合理范围、尺度及类别概率；为不同任务可预先设定有依据的空间，但比较算法时冻结相同空间。跨数量级正参数可考虑对数尺度，不能不加判断地照抄本文区间。[C10、C11、I2]
2. 预先确定独立抽样分布和36次完整训练的记账规则，保存配置、种子、失败状态、验证成绩及耗时。失败/重试是否消耗预算要说清，不能免费补成36个成功候选；若需要多折或多种子，每次拟合都要计入36次。不能只跑一次随机搜索就声称已测得稳定优势。[C2、C18、I2、U1]
3. 按数据特点确定固定划分和指标；确认是否存在类别不平衡、分组、时间顺序或预处理泄漏。预处理只从训练部分拟合；只用验证成绩选择，最终用独立测试数据评价。本文图像准确率不自动等于业务所需指标。[C1、C12、C13、U1]
4. 后续若比较规则网格或自适应方法，采用相同可行空间、训练次数和验证协议，另报耗时及搜索随机性；明确是否允许借用其他任务经验。若总共只有36次训练，就不能同时声称每种算法都获得36次实测；本次只作阅读选择，不安排额外训练。[C16、C17、I3]

还需确认的关键信息为模型族和参数清单、各任务数据规模与分布差异、评价指标与验证划分、训练随机性、单次成本及失败率、是否有可信的历史参数先验。需要更强复现证据时，后续应取得本文指向的实现及 Larochelle 等2007原始对照材料；它们本次未提供，不能作为已读证据。有效维数、36次实际收益和哪种自适应方法最好仍为信息不足。[U1]

下附由所供技能脚本生成的证据审计。引文定位与当前claims/index绑定，**字面匹配不证明科学含义、完整覆盖或迁移有效性**。完整记录见 `claims.json`、`verification.json`、`index/`，图像核对件见 `figures/`。

---

# 论文方法适配审计：Random Search for Hyper-Parameter Optimization（Bergstra 与 Bengio，JMLR 2012）

目标：六个超参数、36次完整训练、跨任务重要性未知时，是否采用独立随机搜索为首版基线？
材料：paper.pdf，所供 PDF 25 页，范围 provided_document。
原件 SHA-256：`01e88a175a36afa399e05dc97dce9c5de980130445269cc0e5100d0471887029`

**核验边界：通过仅表示引文位置、数值字面或算术检查通过；结论语义、实验条件和迁移建议仍须依据上下文审阅。**

## 材料和解释限制

- 仅提供INPUT/paper.pdf，25页，与任务给定页数一致；无另附补充材料、代码、原始实验记录或表格数据。页数吻合不独立证明版本完整。
- 所有页号为PDF从1计数；论文印刷页为281–305。已阅读索引全文并视觉核对图1及图9；未数字化曲线、不报估读精确值。
- 保留摘要七集与正文八集矛盾，不能在所供材料内判定成因。
- 本次未训练模型、未联网、未取得参考文献原件；机械定位通过不证明科学语义或迁移有效性。
- Only supplied pages are indexed; supplements and completeness are not assumed.

## 任务覆盖

| 关注项 | 状态 | 证据 |
| --- | --- | --- |
| 方法与输入输出 | covered | C1, C2 |
| 图1及低有效维数 | covered | C3, C4, C5, I1 |
| 有利实验及预算比较 | covered | C6, C7, C8, C9, C11 |
| DBN不利结果与图注上下文 | covered | C14, C15, C16, C17, C18, C19 |
| 抽样分布与搜索空间 | covered | C10, C11, I2 |
| 验证与测试指标 | covered | C12, C13 |
| 自适应搜索关系及模拟边界 | covered | C20, C21, I3 |
| 表格任务迁移与缺口 | covered | I1, I2, I3, U1 |

## 结论与证据

### C1 · FACT
方法：训练候选配置，在验证集计算目标响应 Ψ，返回验证表现最好的配置；测试集用于最后评估。
值：；机械检查：PASS。
原文位置：PDF p.2；正文及图注。
> to evaluate Ψ(λ) for each one, and return the λ(i) that worked the best as λ̂.
成立条件：训练参数的内层优化与超参数外层选择不同；不能用测试集择优。

### C2 · FACT
本文的基本随机搜索是从指定配置空间独立抽样，不根据之前得分调整后续候选。
值：；机械检查：PASS。
原文位置：PDF p.3；正文及图注。
> independent draws from a uniform density from the same configuration space as would be spanned by a regular grid
成立条件：“均匀”依赖坐标参数化，实际实验还含对数尺度、类别和条件分支，不能理解为所有原始参数都线性均匀。

### C3 · FACT
图1用九次试验说明低有效维数：若 f(x,y)=g(x)+h(y)≈g(x)，网格在重要轴只试三个位置，随机点试九个不同位置。
值：；机械检查：PASS。
原文位置：PDF p.4；正文及图注。
> With grid search, nine trials only test g(x) in three distinct places. With random search, all nine trials explore distinct values of g.
成立条件：已视觉核对图1：重要参数为横轴，不重要参数为纵轴，绿曲线为g，黄曲线为h。这是示意图，不是胜率测量。

### C4 · FACT
图7的 GP/ARD 分析支持：少数参数主导表现，但重要性随数据集变化。
值：；机械检查：PASS。
原文位置：PDF p.14；正文及图注。
> For each data set, a small number of hyperparameters dominate performance, but the relative importance of each hyper-parameter varies from each data set to the next.
成立条件：针对本文神经网络响应面；拟合长度尺度是敏感性刻画，不是普遍因果证明。

### C5 · FACT
作者把七维神经网络问题的有效维数估为一至四维，依数据集而异。
值：；机械检查：PASS。
原文位置：PDF p.15；正文及图注。
> Even in this simple 7-d problem, Ψ has a much lower effective dimension of between 1 and 4, depending on the data set.
成立条件：不是说任何六参数表格模型一定低有效维；有效维数也依范围和参数化而变。

### C6 · FACT
有利实验：图5在八个图像分类数据集、单隐藏层神经网络、无预处理、七个超参数条件下，八次随机试验可匹配或超过平均一百次网格。
值：；机械检查：PASS。
原文位置：PDF p.12；正文及图注。
> Random searches of 8 trials match or outperform grid searches of (on average) 100 trials.
成立条件：图注概括的是该实验；蓝虚线来自 Larochelle 等既有网格结果，不能当成我们数据上的逐次保证。

### C7 · FACT
神经网络每数据集先抽取256个候选，图5再看其中无预处理的子集，正文给出71/256。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> We formed experiments for each data set by drawing S = 256 trials from this distribution.
成立条件：图5小预算效率曲线由已有随机试验拆分估计，不是每个预算都新跑256个完整搜索。

### C8 · FACT
扩大空间会伤害小预算表现：加入标准化/PCA后，正文称需32次而非8次才能稳定超过原网格。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> In the larger space, 32 trials were necessary to consistently outperform grid search rather than 8, indicating that there are many harmful ways to preprocess the data.
成立条件：扩大空间还可能带来更高上限；不能把坏预处理占用的抽样质量忽略。

### C9 · FACT
图6在含预处理的九超参数空间报告64次随机能找到更好模型。
值：；机械检查：PASS。
原文位置：PDF p.13；正文及图注。
> with random search 64 trials are enough to find better models in a larger less promising space.
成立条件：对照仍是平均100次且无预处理的旧网格；图注说网格若再探索四个PCA保留量需平均500次。这不是同空间同预算的直接实测。

### C10 · FACT
抽样分布是方法的一部分：隐单元数采用对数尺度后取整；学习率也用跨数量级抽样，类别如预处理等概率选择。
值：；机械检查：PASS。
原文位置：PDF p.10；正文及图注。
> The number of hidden units was drawn geometrically3 from 18 to 1024.
成立条件：p.10脚注定义 geometrically 为先在log域均匀、指数还原再取整；exponentially 不取整。本文参数与取值区间不能照搬表格模型。

### C11 · FACT
作者称神经网络随机分布与旧网格的区域及密度大致相同，预处理选项除外。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> This sampling process covers roughly the same domain with the same density as the grid used in Larochelle et al. (2007), except for the optional preprocessing steps.
成立条件：roughly不是严格同一离散支持；必须把无预处理对比与扩展空间对比分开。

### C12 · FACT
论文报告分数并非一律为唯一验证冠军的原始测试分数：第2.1节按验证集不确定性，对候选的测试分数加权。
值：；机械检查：PASS。
原文位置：PDF p.5；正文及图注。
> we report a weighted average of all the test set scores, in which each one is weighted by the probability that its particular λ(s) is in fact the best.
成立条件：图2/神经网络/DBN随机效率曲线使用此口径；权重以模拟验证得分估计，不能用测试分数挑选模型。

### C13 · FACT
效率曲线横轴是候选训练次数，纵轴为按式5估计的所选模型测试准确率；箱线或散点表达不同大小随机实验的表现分布。
值：；机械检查：PASS。
原文位置：PDF p.7；正文及图注。
> The vertical axis shows the test accuracy of the best trial(s) from experiments of a given size, as determined by Equation 5.
成立条件：p.6–7：利用i.i.d.试验拆分互不重叠的小实验；大预算可拆分组数少，散点不是额外独立重复次数。准确率不是我们尚未确定的业务指标。

### C14 · FACT
DBN图9的结论为128次随机：三集较差、四集有竞争力、一集convex更好；共八集。
值：；机械检查：PASS。
原文位置：PDF p.20；正文及图注。
> Random experiments of 128 random trials found an inferior best model for three data sets, a competitive model in four, and superior model in one (convex).
成立条件：图注：最多32个参数，绿细虚线为DBN-1，红粗虚线为DBN-3，人工辅助网格平均41次。已视觉核对八面板；不从曲线猜精确准确率或显著性。

### C15 · FACT
DBN负结果明确针对旧三层DBN：差于人工的三个任务为背景图、随机背景、旋转加背景；四个持平任务和一个胜出任务如引文。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> Comparing to the 3-layer DBN results in Larochelle et al. (2007), random search found a better model than the manual search in one data set (convex), an equally good model in four (mnist basic, mnist rotated, rectangles, and rectangles images), and an inferior model in three (mnist background images, mnist background random, mnist rotated background images).
成立条件：p.21另说相对于旧一层DBN，随机搜索一/二/三层配置空间在所有任务至少一样好；这涉及模型层数选择，不能混成三层对三层。

### C16 · FACT
DBN人工对照不是纯规则网格：人工、多分辨率网格和坐标下降组合；后做数据集还借用了先前经验。
值：；机械检查：PASS。
原文位置：PDF p.20；正文及图注。
> later experiments benefited from the experience the authors had drawn from earlier ones.
成立条件：p.19给出DBN-3旧试验从13至102次不等，p.20续接平均41；不是每集41次，也非随机128次与人工41次等预算比较。

### C17 · FACT
DBN还存在评价口径差异：旧实验没有同样的分数加权，作者称其随机实验的加权口径略偏低估。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> the scores in the original experiments were not computed using the same score-averaging technique that we described in Section 2.1, and our averaging technique is slightly biased toward underestimation.
成立条件：不能仅由图9差距推出优化算法的纯因果效应；训练耗时也随配置变化。

### C18 · FACT
不利机制：最佳区域很小时，随机独立试验不能可靠命中；DBN在64次及更大预算仍有明显变异。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> the regions of the search space with the best performance are small, and randomly chosen i.i.d. trials do not reliably find them.
成立条件：结论由此处DBN效率曲线提出，不能把36次描述成可靠发现最优。

### C19 · FACT
未解决的原文内部不一致：摘要说七集，其中四集统计相当、一集更优；图9及p.21正文则为八集（三差四平一优）。
值：；机械检查：PASS。
原文位置：PDF p.1；正文及图注。
> found statistically equal performance on four of seven data sets, and superior performance on one of seven.
成立条件：本报告采用有逐数据集列名且与八面板吻合的正文作描述性汇总，保留摘要矛盾；不擅自更正原文，也不把正文“equally good”升级为重新验证统计等价。

### C20 · FACT
随机搜索在本文是未来自适应方法的比较基线，不是自适应方法的替代终点；本文未提供现代自适应优化器的同预算胜负实验。
值：；机械检查：PASS。
原文位置：PDF p.23；正文及图注。
> We hope that future work in that direction will consider random search of the form studied here as a baseline for performance, rather than grid search.
成立条件：p.21讨论贝叶斯/序贯模型方法的前景；p.23承认DBN专家顺序法总体更好。其当年工程成本论述不能当现代工具包事实。

### C21 · FACT
理论/模拟边界：在三维、五维的立方目标模拟中，有些网格反而最好；低有效维长矩形目标时网格不具竞争力，Sobol略优于伪随机。
值：；机械检查：PASS。
原文位置：PDF p.16；正文及图注。
> There were some grids that were best at finding cubes and hyper-cubes in 3-d and 5-d, but most grids were the worst performers.
成立条件：这是找体积占1%的人工目标区间的模拟，不是分类训练，也非随机在任意函数上最优。p.17还讨论目标与轴不对齐时网格效率可接近随机。

### I1 · INFERRED
适配推断：在六参数、重要维未知且随任务变化的情况下，独立随机是合理首版基线；网格在不重要维上的重复会挤占重要维取值的探索预算。
值：；机械检查：PASS。
原文位置：PDF p.4；正文及图注。
> Random search has the same efficiency in the relevant subspace as if it had been used to search only the relevant dimensions.
推断过程：把图1投影机制和跨数据集重要性变化映射到任务条件；六个名义参数不等于已证明低有效维，36次胜率未知。
成立条件：仅在所选分布能给好配置合理概率、响应面存在相关低维结构时构成优势理由；离散参数可能重复，随机也会聚集。

### I2 · INFERRED
适配建议：在固定36次完整训练预算内，先确定可行空间、尺度、类别概率和条件约束，再预先独立抽样、用固定验证协议择优并记录全部试验。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> This tradeoff between exploration and exploitation is central to the design of an effective random search.
推断过程：扩展空间在论文中改变小预算效率，故首版应避免随意加入大量低可信配置；若中途依结果改分布，已变成顺序搜索，需另标阶段和预算。
成立条件：这是阅读后的设计建议，不是论文实测36次方案；不运行训练，不假设工具包行为。

### I3 · INFERRED
适配建议：以后以相同空间、验证协议及预算比较自适应搜索与随机基线，保留自适应在窄好区域或高有效维问题上的潜在收益。
值：；机械检查：PASS。
原文位置：PDF p.23；正文及图注。
> Random search was not generally as good as the sequential combination of manual and grid search from an expert
推断过程：随机不利用历史信息；DBN专家经验展示顺序决策可能有效，但缺严格等预算的自动优化器对照。
成立条件：同训练次数仍可能不同计算成本，应另报训练耗时；不能从旧DBN实验保证现代自适应算法更强。

### U1 · UNKNOWN
现有材料不能确定本流程六参数的类型、范围、有效维数、好配置概率，以及36次随机相对网格或自适应搜索的胜率与收益。
值：；机械检查：WARN。
检索范围：所供25页论文及INPUT/task.md；无补充材料、实现代码或用户数据；脚本检索对象为PDF索引。。
不确定性：已阅读神经网络与DBN方法、八个图像分类任务、模拟及限制；命中的有效维数/validation是论文实验语境，不能回答用户未提供的模型族、特征、划分、指标、噪声和成本。无关键词命中同样不证明研究完全未涉及某概念。
- `tabular`：无关键词命中。
- `36`：无关键词命中。
- `effective dimension`：3, 4, 11, 15, 16, 21, 23。
- `validation`：1, 2, 5, 6, 7, 8, 9, 10, 12, 19, 22。
关键词检索不证明论文语义上没有讨论此项；这里只描述所供材料的证据不足。


## 方法适配判断

| 环节 | 判断 | 依据 | 待补条件 |
| --- | --- | --- | --- |
| 独立抽样与按验证分数择优机制 | 可直接用 | C1, C2 | 记录候选、随机种子和验证得分；测试集留到最终评估。 |
| 六参数空间及概率分配 | 需改造 | C10, C11, I2 | 确认模型族、每个参数类型、合理边界、线性或对数尺度、类别概率、失效组合及条件依赖。 |
| 36次预算下的收益与可靠性 | 信息不足 | C18, U1 | 确认好区域概率、响应噪声、重复训练成本；未来在代表性任务上同协议实测，报告随机性。 |
| 跨分布表格分类验证 | 需改造 | C4, C12, C13, U1 | 按业务确认指标、类别不平衡、分组或时间划分、预处理仅训练集拟合与泄漏风险。 |
| 将来比较自适应搜索 | 需改造 | C16, C17, C20, I3 | 同空间/验证协议、完整训练次数和耗时，明确是否允许历史任务经验及失败重试。 |

**总体判断：需改造**

## 后续阅读与核验

- 表格数据及模型信息缺失；影响：不能确定低有效维和36次实际优势；下一步：取得参数清单、数据规模/类别/任务分布、验证方案、评价指标与单次训练成本后制定分布。。
- 论文比较非全部严格同预算同空间同口径；影响：不能给统一加速倍数或随机胜率；下一步：如需更强复现证据，后续补读Larochelle等2007原论文与本文所指代码/实验记录；本次未取得，不视为证据。。
- DBN摘要与正文数量不一致；影响：不能无条件沿用摘要七集统计表述；下一步：后续查作者勘误或可追溯版本，现保留三差四平一优的正文描述。。
- 缺现代自适应方法等预算实验；影响：不能判定将来采用哪种自适应优化器；下一步：未来在同一表格任务和36次总训练约束下评估；本报告不执行。。
- 建议采用随机搜索作为首版基线，不保证36次胜过网格、自适应搜索或找到全局最优。
- 预算按完整训练计数；若使用多折验证或重复种子，应把每次拟合计入总预算，不能默认为36个配置还免费重复训练。
