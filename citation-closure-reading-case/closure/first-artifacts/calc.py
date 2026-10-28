#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核查 Strubell, Ganesh, McCallum (2019, ACL): "Energy and Policy Considerations
for Deep Learning in NLP"。按论文式(1)(2)复算 Table 3 的 kWh·PUE 与 CO2e，
并回解 BERT_base 名义时长（表列 79 h vs 正文 3.3 天 = 79.2 h）。

式(1): pt = 1.58 * t * (pc + pr + g*pg) / 1000      [kWh·PUE]
式(2): CO2e = 0.954 * pt                             [lb]
Table 3 "Power (W)" 列 = (pc + pr + g*pg)，即含 CPU/DRAM/GPU 的总功率(W)。
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
import json, os

getcontext().prec = 50

PUE = Decimal("1.58")
CO2_FACTOR = Decimal("0.954")  # lb CO2e / kWh，美国电网 (EPA eGRID)

def kwh(power_w, hours):
    """kWh·PUE，按式(1)。"""
    return PUE * hours * power_w / Decimal(1000)

def co2e(kwh_value):
    """CO2e (lb)，按式(2)。"""
    return CO2_FACTOR * kwh_value

def rnd(x):
    return x.to_integral_value(rounding=ROUND_HALF_UP)

# Table 3 输入：模型, 硬件, Power(W), Hours(表列), kWh·PUE(表列), CO2e(表列)
rows = [
    ("T2Tbase",  "P100x8",  Decimal("1415.78"), Decimal("12"),    27,      26),
    ("T2Tbig",   "P100x8",  Decimal("1515.43"), Decimal("84"),   201,     192),
    ("ELMo",     "P100x3",  Decimal("517.66"),  Decimal("336"),  275,     262),
    ("BERTbase", "V100x64", Decimal("12041.51"), Decimal("79"),  1507,    1438),
    ("NAS",      "P100x8",  Decimal("1515.43"), Decimal("274120"), 656347, 626155),
]

row_out = {}
for name, hw, pw, hours, kwh_tab, co2_tab in rows:
    k = kwh(pw, hours)
    k_r = int(rnd(k))
    c = co2e(k)
    c_r = int(rnd(c))
    row_out[name] = {
        "hardware": hw,
        "power_W": str(pw),
        "hours_table": str(hours),
        "kWh_PUE_exact": str(k),
        "kWh_PUE_rounded": k_r,
        "kWh_PUE_table": kwh_tab,
        "CO2e_exact": str(c),
        "CO2e_rounded": c_r,
        "CO2e_table": co2_tab,
    }

# BERT_base：正文值 3.3 天 = 79.2 h 与表列 79 h 对比
pw_bert = Decimal("12041.51")
t_text = Decimal("79.2")
k_text = kwh(pw_bert, t_text)
c_text = co2e(k_text)
k_79 = kwh(pw_bert, Decimal("79"))
c_79 = co2e(k_79)

# 回解：由取整后的 kWh·PUE=1507 与 CO2e=1438 反推 t 的区间
denom = PUE * pw_bert / Decimal(1000)  # 每小时产生的 kWh·PUE
def t_for(kwh_target):
    return kwh_target / denom
# 条件A：round(kWh·PUE)=1507 -> 精确值 ∈ [1506.5, 1507.5)
t_kwh_lo = t_for(Decimal("1506.5"))
t_kwh_hi = t_for(Decimal("1507.5"))
# 条件B：round(0.954*精确kWh)=1438 -> 精确kWh ∈ [1437.5/0.954, 1438.5/0.954)
kwh_co2_lo = Decimal("1437.5") / CO2_FACTOR
kwh_co2_hi = Decimal("1438.5") / CO2_FACTOR
t_co2_lo = t_for(kwh_co2_lo)
t_co2_hi = t_for(kwh_co2_hi)
t_lo = max(t_kwh_lo, t_co2_lo)
t_hi = min(t_kwh_hi, t_co2_hi)

# 换算关系检查
ratio_1438_1507 = Decimal("1438") / Decimal("1507")          # ≈0.954
half_factor = CO2_FACTOR / Decimal(2)                        # 0.477 lb/kWh（碳强度减半）
co2_half_intensity = half_factor * Decimal("1507")           # 同 1507 kWh、碳强度减半
k_half_power = kwh(pw_bert / Decimal(2), t_text)             # 硬件功率减半（0.954 不变）
co2_half_power = co2e(k_half_power)

nas_eq_t2tbig = (Decimal("1515.43") == Decimal("1515.43"))

out = {
    "source": "Strubell, Ganesh, McCallum (2019), ACL, 'Energy and Policy Considerations for Deep Learning in NLP'",
    "constants": {
        "PUE": str(PUE),
        "CO2e_factor_lb_per_kWh_US_grid_EPA_eGRID": str(CO2_FACTOR),
        "formula_kWh_PUE": "pt = 1.58 * t * (pc+pr+g*pg) / 1000",
        "formula_CO2e_lb": "CO2e = 0.954 * pt",
    },
    "table3_recomputation": row_out,
    "BERTbase_79h_vs_79.2h": {
        "hours_table": "79",
        "hours_text": "79.2 (=3.3 days, NVIDIA via Forster et al. 2019)",
        "kWh_PUE_exact_h79": str(k_79),
        "kWh_PUE_rounded_h79": int(rnd(k_79)),
        "CO2e_rounded_h79": int(rnd(c_79)),
        "kWh_PUE_exact_h79.2": str(k_text),
        "kWh_PUE_rounded_h79.2": int(rnd(k_text)),
        "CO2e_rounded_h79.2": int(rnd(c_text)),
        "table_kWh_PUE": 1507,
        "table_CO2e": 1438,
    },
    "back_solve_interval_hours": {
        "t_kWh_low": str(t_kwh_lo),
        "t_kWh_high": str(t_kwh_hi),
        "t_CO2_low": str(t_co2_lo),
        "t_CO2_high": str(t_co2_hi),
        "t_intersection_low": str(t_lo),
        "t_intersection_high": str(t_hi),
        "note": "反推区间仅由两列取整后的整数约束给出；79.2 落在区间内，79 不在。",
    },
    "factor_checks": {
        "1438_div_1507": str(ratio_1438_1507),
        "half_of_CO2_factor": str(half_factor),
        "CO2e_if_1507kWh_x_0.477_lb_per_kWh": str(co2_half_intensity),
        "CO2e_if_hardware_power_halved_0.954_kept": str(co2_half_power),
        "kWh_if_hardware_power_halved": str(k_half_power),
        "note": "0.477 lb/kWh 是碳强度减半（更清洁电力），并非硬件功率减半；硬件减半应使 kWh 减半而 0.954 不变。",
    },
    "NAS_vs_T2Tbig_power_equal": nas_eq_t2tbig,
}

here = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(here, "calc.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(json.dumps(out, ensure_ascii=False, indent=2))
