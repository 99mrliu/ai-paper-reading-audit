# ACL2019必要原文与事实转录

Emma Strubell, Ananya Ganesh, Andrew McCallum. Energy and Policy Considerations for Deep Learning in NLP. ACL2019,P19-1355,3645–3650。[官方页](https://aclanthology.org/P19-1355/)、[PDF](https://aclanthology.org/P19-1355.pdf)，CC BY4.0。实际阅读原件6页SHA256=184c42b148a3db99f4a59ed8336c403dc2229bf3100bbc934212116acd8c61d9。

本包不重复放全文PDF；核查本文所需的2/3/4页均以完整可读页图提供，页图来自原件渲染，不修改内容。以下是作者事实转录，不是额外AI输出。其他章节未作为本文核心结论证据。

| 本地原文页图 | 对应位置及核查事实 |
| --- | --- |
| [PDF2，印刷3646](../figures/source-page-2.png) | Case study1/Methods与式(1)(2)：采样估算、CPU/DRAM/GPU合计、PUE1.58、W→kW的/1000、0.954lb/kWh。估算不是本项目完整训练电表实测。 |
| [PDF3，3647](../figures/source-page-3.png) | Models的BERT段给3.3天(79.2h)和V100×64；NAS预算有其他出处。这一正文时长只绑定2019文章。 |
| [PDF4，3648](../figures/table3-page4.png) | Table3完整表头、各行、表注与Estimated限定；T2Tbase(8卡)1415.78W，T2Tbig(8卡)1515.43W，BERT(64卡)12041.51W。 |

| Table3行 | Hardware | Power W | Hours | kWh·PUE | CO₂e lb |
| --- | --- | --- | --- | --- | --- |
| T2Tbase | P100×8 | 1415.78 | 12 | 27 | 26 |
| T2Tbig | P100×8 | 1515.43 | 84 | 201 | 192 |
| BERTbase | V100×64 | 12041.51 | 79 | 1507 | 1438 |
| NAS | P100×8 | 1515.43 | 274120 | 656347 | 626155 |

其中NAS与T2Tbig显示相等不能识别来源；T2Tbase检验共同参数模型的反例见matched/probe_shared_power.py。转录可回到完整原文页图逐格核查。重做旧完整论文阅读时自行取得上述同哈希PDF，不把阅读这些页图说成已读全篇。
