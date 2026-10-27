"""Repair/diagnosis arithmetic only (labeled; NOT part of the first answer).

Computes exact vs display-rounded products and the carbon residual unit,
using only numbers already transcribed from the current AAAI-20 paper and the
already-generated calculations.json. No internet, no training, no old reports.
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
import json

getcontext().prec = 28
D = Decimal
LB_TO_KG = D("0.45359237")

KWH = D("1507")          # Table 2, printed page 13695 (BERTbase V100x64, kWh·PUE)
FACTOR_0477 = D("0.477") # method, printed page 13694 (Eq. 2)
EPA_0954 = D("0.954")    # method, printed page 13694 (EPA US avg before halving)
CO2E_PRINTED = D("719")  # Table 2, printed page 13695

out = {}

# --- Item 1: exact vs display rounding ---
p_0477 = KWH * FACTOR_0477
p_0954 = KWH * EPA_0954
out["products"] = {
    "1507_x_0.477_exact": str(p_0477),
    "1507_x_0.477_rounded_to_integer": str(p_0477.quantize(D("1"), rounding=ROUND_HALF_UP)),
    "1507_x_0.477_is_exactly_719": bool(p_0477 == CO2E_PRINTED),
    "1507_x_0.954_exact": str(p_0954),
    "1507_x_0.954_rounded_to_integer": str(p_0954.quantize(D("1"), rounding=ROUND_HALF_UP)),
    "1507_x_0.954_is_exactly_1438": bool(p_0954 == D("1438")),
}

# --- carbon residual unit: kg (script canonicalizes g/kg/lb all to kg) ---
# values from the already-saved calculations.json
CARBON_NOMINAL_KG = D("325.199035243582818318")
CARBON_REPORTED_KG = D("326.13291403")   # = 719 lb * 0.45359237
RESIDUAL_KG = CARBON_NOMINAL_KG - CARBON_REPORTED_KG
RESIDUAL_LB = RESIDUAL_KG / LB_TO_KG
out["carbon_residual"] = {
    "unit_of_nominal_residual_field": "kg (script canonical unit)",
    "residual_kg": str(RESIDUAL_KG),
    "residual_lb": str(RESIDUAL_LB),
    "check_719lb_in_kg": str(D("719") * LB_TO_KG),
}

print(json.dumps(out, ensure_ascii=False, indent=2))
