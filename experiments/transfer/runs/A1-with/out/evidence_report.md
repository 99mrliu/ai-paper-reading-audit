# 论文方法适配审计：Random Search for Hyper-Parameter Optimization

目标：六个超参数、每任务36次完整训练、跨任务分布不同且重要参数未知：是否采用随机搜索作为第一版基线？
材料：paper.pdf，所供 PDF 25 页，范围 provided_document。
原件 SHA-256：`01e88a175a36afa399e05dc97dce9c5de980130445269cc0e5100d0471887029`

**核验边界：通过仅表示引文位置、数值字面或算术检查通过；结论语义、实验条件和迁移建议仍须依据上下文审阅。**

## 材料和解释限制

- 仅取得INPUT/paper.pdf（JMLR 2012，25页含参考文献）和任务说明；未取得补充材料、实现代码或用户数据。索引页数符合任务描述，但不独立证明出版物及补充材料完整。
- 已直接查看PDF第4页图1及第20页图9渲染图，阅读图注和相邻上下文；图9小面板不作精确准确率估读，结论采用正文定性分类。
- 第1页摘要七数据集与图9/结果正文八数据集不一致，未能解释；初始化乘数范围文字亦有歧义。
- 未联网、未运行训练、未执行复现。所有页码为从1开始的PDF页码（印刷页码=PDF页码+280）。
- Only supplied pages are indexed; supplements and completeness are not assumed.

## 任务覆盖

| 关注项 | 状态 | 证据 |
| --- | --- | --- |
| 方法与候选选择 | covered | C1, C2 |
| 低有效维数与图1 | covered | C3, C4, C5, I1 |
| 有利实验、预算和评价对象 | covered | C6, C7, C8, C9, C16, C21, C22 |
| DBN反例、图注及上下文 | covered | C11, C12, C13, C14, C15, C16, C17, C18 |
| 搜索空间和抽样分布 | covered | C8, C10, I2 |
| 随机与自适应搜索关系 | covered | C14, C19 |
| 表格分类迁移与36次限制 | covered | I1, I2, U1 |
| 边界与网格有利情形 | covered | C20 |

## 结论与证据

### C1 · FACT
方法：在指定搜索空间内产生候选配置，逐一训练并用验证损失评价，返回验证表现最好的配置；测试集用于最终泛化评价。
值：；机械检查：PASS。
原文位置：PDF p.2；正文及图注。
> to evaluate Ψ(λ) for each one, and return the λ(i) that worked the best as λ̂.
成立条件：式2–4；训练、验证和测试用途须区分。

### C2 · FACT
本文随机搜索是从定义的配置空间独立抽样；不根据已经观察的分数改变后续抽样。
值：；机械检查：PASS。
原文位置：PDF p.3；正文及图注。
> independent draws from a uniform density from the same configuration space as would be spanned by a regular grid
成立条件：“均匀”依赖坐标定义；实际实验含对数域抽样、离散选择及条件参数，不能理解为所有原始参数线性均匀。

### C3 · FACT
图1：九点规则网格在重要的x方向只试三个值，九个随机点在示意图中试九个不同x值；y的影响很小。
值：；机械检查：PASS。
原文位置：PDF p.4；正文及图注。
> With grid search, nine trials only test g(x) in three distinct places. With random search, all nine trials explore distinct values of g.
成立条件：f(x,y)=g(x)+h(y)≈g(x)，这是机制示意图，不是分类精度实验；随机投影不保证等间距。

### C4 · FACT
图7的GP/ARD分析支持：单个数据集上少数参数主导性能，但参数重要性随数据集改变。
值：；机械检查：PASS。
原文位置：PDF p.14；正文及图注。
> For each data set, a small number of hyperparameters dominate performance, but the relative importance of each hyper-parameter varies from each data set to the next.
成立条件：神经网络、所选搜索域及采样点下的拟合分析，不是所有模型的定理，也不是因果识别。

### C5 · FACT
作者对七维神经网络搜索响应面的分析给出依数据集而异的1–4有效维数。
值：；机械检查：PASS。
原文位置：PDF p.15；正文及图注。
> Even in this simple 7-d problem, Ψ has a much lower effective dimension of between 1 and 4, depending on the data set.
成立条件：长度尺度拟合存在局部最优；PDF p.13说明多次子采样与随机初始化；不能据此外推我们的有效维数。

### C6 · FACT
有利实验：图5无预处理的单隐层神经网络、八个图像分类数据集、七个待调参数；8次随机搜索可匹配或超过平均100次网格搜索。
值：；机械检查：PASS。
原文位置：PDF p.12；正文及图注。
> Random searches of 8 trials match or outperform grid searches of (on average) 100 trials.
成立条件：纵轴为验证选择后的测试准确率（按第2.1节估计），横轴为候选模型数；比较来自Larochelle等既有网格实验，不是我们的36次对照。

### C7 · FACT
每个数据集随机抽取256次；效率曲线利用i.i.d.试验拆成较小实验描述分布。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> We formed experiments for each data set by drawing S = 256 trials from this distribution.
成立条件：无预处理子集只有71/256次（同页）；小预算曲线不是为每个预算另行大量独立重复的全部新训练。

### C8 · FACT
扩大到含标准化/PCA的搜索域后，需要32次而非8次才能稳定超过既有网格结果；更多选择可能稀释好配置的抽样概率。
值：；机械检查：PASS。
原文位置：PDF p.11；正文及图注。
> In the larger space, 32 trials were necessary to consistently outperform grid search rather than 8, indicating that there are many harmful ways to preprocess the data.
成立条件：同页说明64次或更多可超过较受限搜索；这一阈值只属于该实验。

### C9 · FACT
图6：九参数随机搜索64次足以在更大、较不利空间找到更好模型；对照仍是平均100次且不含预处理的旧网格。图注估算加入四个PCA方差档的网格平均需500次。
值：；机械检查：PASS。
原文位置：PDF p.13；正文及图注。
> Exploring just four PCA variance levels by grid search would have required 5 times as many (average 500) trials per data set.
成立条件：不是同一扩展空间下64次随机与已执行500次网格的实测对照，也不是等墙钟时间比较。

### C10 · FACT
抽样分布须显式定义：文中drawn geometrically指对数域均匀后取指数并四舍五入；drawn exponentially不取整。
值：；机械检查：PASS。
原文位置：PDF p.10；正文及图注。
> drawing uniformly in the log domain between log(A) and log(B), exponentiating to get a number between A and B, and then rounding to the nearest integer.
成立条件：用于指定正数参数；分类选项、是否启用正则及PCA条件参数另有概率。原文对初始化乘数范围存在0.1–10与0.2–2两处表述，不能当作可直接复现的统一范围。

### C11 · FACT
DBN随机搜索把层数也作为选择：等概率抽一、二、三层，而不是只调固定三层。
值：；机械检查：PASS。
原文位置：PDF p.18；正文及图注。
> We chose 1, 2, or 3 layers with equal probability.
成立条件：每层有条件参数；p.19说明8个全局参数加每层8个，三层最多32维。

### C12 · FACT
图9反例：128次随机搜索相较三层DBN专家搜索，三个数据集较差、四个相当、convex一个更好，共八个数据集。
值：；机械检查：PASS。
原文位置：PDF p.20；正文及图注。
> Random experiments of 128 random trials found an inferior best model for three data sets, a competitive model in four, and superior model in one (convex).
成立条件：图注及p.21正文一致；相当不表示本审计重新进行了显著性检验。

### C13 · FACT
DBN-3专家对照平均41次试验，并非与128次随机搜索等次数预算。
值：；机械检查：PASS。
原文位置：PDF p.20；正文及图注。
> of trials across data sets for the DBN-3 model was 41.
成立条件：p.19列极端：mnist background images为102次，mnist background random为13次；41不是所有模型、所有数据集的固定次数。

### C14 · FACT
专家对照结合手工、多分辨率网格与坐标下降，并跨数据集利用先前经验，带有顺序自适应性质。
值：；机械检查：PASS。
原文位置：PDF p.20；正文及图注。
> later experiments benefited from the experience the authors had drawn from earlier ones.
成立条件：不能把其标签简化成纯规则网格，也不能把专家知识与配置空间差异的效应归因于单一算法。

### C15 · FACT
随机搜索落后的三组为带图像背景、随机背景、旋转加图像背景的MNIST变体；四个相当为mnist basic、mnist rotated、rectangles、rectangles images。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> an inferior model in three (mnist background images, mnist background random, mnist rotated background images).
成立条件：与三层DBN对照；同页另称随机探索一至三层的结果对一层DBN对照均至少相当。两种对照不可混用。

### C16 · FACT
旧实验和本文评分汇总方式不完全一致；本文认为自己的平均方式略偏向低估表现。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> the scores in the original experiments were not computed using the same score-averaging technique that we described in Section 2.1
成立条件：不能把所有图线差异视为纯搜索策略效应；第2.1节按验证最优的不确定性加权测试分数，而不是模型集成预测。

### C17 · FACT
DBN即使64次以上仍有明显波动；作者解释优质区域小，i.i.d.抽样不能可靠命中。
值：；机械检查：PASS。
原文位置：PDF p.21；正文及图注。
> even experiments with larger numbers of trials (64 and larger) feature significant variability.
成立条件：随机搜索不提供小预算最优性保证。

### C18 · FACT
保留原文不一致：摘要写七个数据集中的四个相当、一个更好；图9及p.21逐项结果却为三差、四平、一优，共八个。
值：；机械检查：PASS。
原文位置：PDF p.1；正文及图注。
> statistically equal performance on four of seven data sets, and superior performance on one of seven.
成立条件：本报告采用有图注和逐项名称支持的八个口径；无补充材料/代码，不能确定差异成因。

### C19 · FACT
随机搜索在本文中的角色是后续自适应搜索的比较基线；本文没有在我们的任务上比较现代自适应实现。
值：；机械检查：PASS。
原文位置：PDF p.23；正文及图注。
> We hope that future work in that direction will consider random search of the form studied here as a baseline for performance, rather than grid search.
成立条件：作者将顺序自适应方法列为未来方向；DBN专家顺序搜索是相关证据，不是系统比较各种自动自适应算法。

### C20 · FACT
不利边界：人工区间定位模拟中有些网格在立方体目标上最好；低维或已知重要坐标时不能一概排除网格。
值：；机械检查：PASS。
原文位置：PDF p.16；正文及图注。
> There were some grids that were best at finding cubes and hyper-cubes in 3-d and 5-d, but most grids were the worst performers.
成立条件：模拟目标占单位超立方体1%体积，不是训练真实分类器；p.17指出目标与网格轴的对齐关系也影响结果。

### C21 · FACT
数据迁移限制：MNIST变体及合成图像分类构成主要实验，并有固定训练/验证/测试划分；不是通用表格分类基准。
值：；机械检查：PASS。
原文位置：PDF p.8；正文及图注。
> We shuffled the original splits randomly, and used 10 000 training examples, 2000 validation examples, and 50 000 testing examples.
成立条件：该数目用于mnist basic等；rectangles为1000训练、200验证、50000测试（p.9），不得把一种划分套到所有数据集。

### I1 · INFERRED
建议随机搜索作为第一版基线，但需为表格模型改造搜索域、抽样分布和评价协议。
值：；机械检查：PASS。
原文位置：PDF p.4；基于原文的任务适配推断。
> Random search has the same efficiency in the relevant subspace as if it had been used to search only the relevant dimensions.
推断过程：用户六个参数的重要性未知且随任务分布可能改变；独立随机投影不会因不重要维度的笛卡尔组合而重复同一重要坐标，因此有预算利用理由。该理由依赖优质区域在所选分布下有足够质量，不能推出36次胜出。

### I2 · INFERRED
可用命中概率解释风险：若“足够好”的配置在事先固定抽样分布下概率质量为q，36次独立抽样至少命中一次的概率为1−(1−q)^36；本文不能给出我们的q。
值：；机械检查：PASS。
原文位置：PDF p.16；基于原文的任务适配推断。
> The expected probability of finding the target is 1.0 minus the probability of missing the target with every single one of T trials in the experiment.
推断过程：独立事件全部未命中的概率相乘；这是条件概率公式，不是从论文精度数据拟合的本任务预测。训练噪声、何为足够好、条件空间及失败配置均影响q的含义。

### C22 · FACT
训练成本不等同于固定次数完整训练：神经网络实验允许100至1000轮，并根据验证表现提前停止；本文次数比较不保证等计算量。
值：；机械检查：PASS。
原文位置：PDF p.10；第2.4节训练设置。
> We permitted a minimum of 100 and a maximum of 1000 iterations over the training data
成立条件：随后给出提前停止条件；不同配置还可能有不同网络规模。用户36次完整训练须另定统一资源规则。

### U1 · UNKNOWN
尚不能确定我们的六参数表格模型在36次预算下的收益、有效维数、好配置概率或对自适应方法的相对表现。
值：；机械检查：WARN。
检索范围：所供25页PDF及INPUT/task.md；未提供我们的数据、模型、试验结果、补充材料或代码。
不确定性：已阅读全文方法、实验与结论；命中classification/effective dimension/adaptive的是本文图像分类和方法讨论，不能替代用户模型证据。即使36有字面命中，也不能证明同预算迁移效果。
- `36`：无关键词命中。
- `classification`：8, 9, 11, 18。
- `effective dimension`：3, 4, 11, 15, 16, 21, 23。
- `adaptive`：1, 20, 21, 23。
关键词检索不证明论文语义上没有讨论此项；这里只描述所供材料的证据不足。


## 方法适配判断

| 环节 | 判断 | 依据 | 待补条件 |
| --- | --- | --- | --- |
| 独立采样、验证选择、记录配置 | 可直接用 | C1, C2 | 固定随机种子并保存全部候选、失败和评价记录。 |
| 六参数搜索域与分布 | 需改造 | C8, C10, I1 | 明确参数类型、合法范围、尺度、条件依赖、约束及失败配置处理；不能照搬神经网络范围。 |
| 跨任务数据划分和指标 | 需改造 | C16, C21 | 确认类别不平衡、分组或时间依赖、目标指标；预处理只拟合训练集，测试集不参与选择。 |
| 36次预算下效果与优越性 | 信息不足 | I2, U1 | 确认预算是否含重试、随机种子重复和重训；取得代表性表格任务的同预算对照。 |
| 未来自适应搜索对照 | 需改造 | C14, C19, U1 | 保持空间、训练成本与评价口径一致，跨任务报告分布和失败；需另取具体方法证据。 |

**总体判断：需改造**

## 后续阅读与核验

- 六参数定义及先验未知；影响：无法指定合理边际分布与合法条件空间；下一步：确认模型族、六参数名称/类型/范围、条件依赖、历史默认值来源。。
- 数据结构与目标指标未知；影响：验证选择可能不代表部署目标；下一步：确认数据量、类比例、分组/时间结构、任务间差异及评价指标。。
- 缺少我们的36次实测；影响：无法量化收益或计算好配置概率；下一步：未来在代表性任务上用相同36次预算比较预先规定的随机与网格；若要比较多次搜索波动，需另批预算。。
- DBN计数与实现细节有歧义；影响：不能完成严格数值复现或归因；下一步：如后续要复现，另获取作者补充材料、当年代码与Larochelle等2007原研究，核对拆分、预算和评分；本次均未取得。。
- 可作为基线不等于36次保证胜出、保证全局最优，亦不证明六参数具有低有效维数。
- 机械定位与字面匹配不证明科学语义；已另检查比较对象、条件、预算、指标和外推边界。
