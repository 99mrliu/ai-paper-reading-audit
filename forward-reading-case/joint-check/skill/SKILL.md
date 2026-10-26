---
name: paper-joint-rounding
description: Check whether rounded quantitative results in a paper can share one underlying parameter, distinguishing separate interval overlap from joint feasibility. Use for fixed positive linear rates with an explicitly stated rounding rule.
metadata:
  version: "1.0.0"
---

# 同一参数，联合核查

当论文多个显示结果共享一个未知时长/尺度，分别兼容不足以证明同时兼容。先保留原文、名义失败及每项条件，再统一为同一参数的约束。用当前核算器时，不把energy_check与carbon_check各自true写成joint true。

对 y_i = rate_i × t，rate_i为已知正数、单位已统一、t非负时，可运行：

`python3 scripts/joint_bounds.py input.json --out result.json`

输入为`rounding`（half_up或half_even），`constraints`列表，每条含id、rate、display、quantum；可选fixed_parameter检查给定候选。display须为quantum整倍数。它使用有理数精确交集，并按取整规则保留端点开闭，不把仅相接的开端点判成可行。joint_feasible仅证明明示假设下至少存在一个共同参数；witness是数学构造，不能说原作者采用过它。给出处仍不能证明舍入规则，规则未知时分情景报告。

零/负系数、多参数不确定、关联测量误差、非线性和未知单位不在工具范围，明确停止或另建模型，不能把unsupported说成论文不兼容。不把不同记录的参数误设为共享，也不能为了得到交集而把共享变量拆成独立变量。计量边界、来源、原文解释和物理有效性仍须另行核查。
