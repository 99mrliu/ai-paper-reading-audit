# AAAI2020原文材料与边界

Emma Strubell, Ananya Ganesh, Andrew McCallum. *Energy and Policy Considerations for Modern Deep Learning Research*. AAAI2020,34(09),13693–13696. DOI10.1609/aaai.v34i09.7123。来源为[出版页](https://ojs.aaai.org/index.php/AAAI/article/view/7123)及[官方PDF](https://ojs.aaai.org/index.php/AAAI/article/download/7123/6977)。必要[短引、事实转录与单位](evidence.txt)另有UTF-8文字，关键证据不只靠图片。原件4页、哈希与各裁片坐标在[source-record.json](source-record.json)。

原件显示Copyright2020AAAI/all rights reserved，不假定全文再分发许可。本包为批评、核查这一具体解读，仅提供必要的署名原文裁片与事实转录；不分发2020全文。实际模型在本地导入并读取了原完整PDF，不能把包内裁片说成它当时收到的唯一输入。离线审阅关键解读可用以下材料；重做完整原文阅读需自行从合法来源取得同哈希原件。

| 裁片 | 位置、说明 |
| --- | --- |
| [training-method.png](training-method.png) | PDF1/13693，Case study1，采样功率及按既有论文时长/硬件估算的流程；没有逐行采样日志。 |
| [bert-models.png](bert-models.png) | PDF2/13694，Models/BERT完整段；所附段没有给79.2h。不能以有限段落证明其他材料不存在。 |
| [method-definitions.png](method-definitions.png) | PDF2/13694，CPU/DRAM/GPU与g的定义。 |
| [method-pue-equation.png](method-pue-equation.png) | 同页，PUE1.58、合计方法与式(1)；W→kW含/1000。 |
| [factor-assumptions.png](factor-assumptions.png) | 同页，0.954→0.477、AWS50%可再生及剩余来源比例假设、数据可得性限制；不是当前普适因子。 |
| [table2.png](table2.png) | PDF3/13695，Table2表头、数字、硬件标签及完整表注；BERT719、TPU缺值、T2T/NAS功率比较所需上下文。 |

裁片未修改原字，只裁去无关页区域。中文解释为作者概述；公式、数值及图像来自论文。source-record.json的检索是对四页pdftotext-layout输出查特定字符串，无命中不能排除OCR失败、不同表述、其他版本或补充材料，不将搜索输出当科学事实证明。
