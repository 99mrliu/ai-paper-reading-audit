# 核算账本接口

输入为 `{"records": [...]}`。每行有唯一 `id` 和非空 `source` 字符串（PDF页/表/行及录入数；用户数据标明来源）。不支持单位时明确 invalid，不猜测。数值建议字符串，禁止逗号分组、NaN、Infinity。缺失值写 null。

最小例子（合成说明，不是任何论文答案）：

```json
{"records":[{"id":"trial","source":"用户给定的合成测量，非论文实测","power":{"value":"2","unit":"kW"},"power_scope":"aggregate","duration":{"value":"30","unit":"min"},"measurement_scope":"it","pue":{"value":"1.2"},"intensity":{"value":"200","unit":"g/kWh"}}]}
```

- `power`: `{value, unit, quantum?}`，支持 W/kW/MW。`power_scope` 必须是 aggregate 或 per_device；后者还需整数 `devices`≥1。已有总功率使用 aggregate，不添加设备乘数。
- `duration`: 同样结构，支持 s/min/h/day。
- `measurement_scope`: it 或 facility。it 需要 `pue:{value, quantum?}`且 value≥1；facility 应省略 PUE 或明确为1，其他值会被拒绝。
- 可把 power 换为 `components:[{power, power_scope, devices?, allocation?}, ...]` 以求 CPU/DRAM/GPU 分项之和。分摊比例 allocation 默认为1，若提供则须在[0,1]；它是用户/文献假设，不是脚本测得。
- 可把 power+duration 换为 `energy:{value, unit, quantum?}`，支持 Wh/kWh/MWh。仍须注明 it/facility 边界。不要同时提供 energy 与 power/components/duration，以免双计。
- `intensity`: 可选 `{value,unit,quantum?}`，单位 g/kWh、kg/kWh、lb/kWh。缺失时仍可核算能量，碳排为 unknown。
- `reported_energy`（Wh/kWh/MWh）和 `reported_carbon`（g/kg/lb）可选，用于和名义复算比较。
- `quantum` 是与该数值相同单位的显示取整步长，须>0；只有明确声明“假设按此步长舍入”时使用。未提供的数按给定值作点计算，不自动从小数位猜测精度。输出 `conditional_rounding_overlap`，不是统计检验。
- `group` 可选。确属互不重叠时段且同一核算对象时才指定共同 group，以计算总能耗和总碳排。表中不同模型、训练/NAS/R&D 不应自动相加。任何组员相关输出未知/非法，则该组对应总数为 unknown，而非只加已知部分并冒充完整总数。

输出包含来源、规范化单位、名义值、条件区间、报告值的名义残差与区间是否重叠、行级状态和错误；输入文件 SHA256 用于绑定本次账本。它不绑定 PDF 引文，必须自行核对转录与原文。退出码0=结构有效且没有 invalid 行（允许 unknown），2=有 invalid 行或输入格式错误。非空 records 必需，重复 ID 会拒绝整个文件。
