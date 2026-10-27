"""Supplementary labeled checks for paper-budget-audit (no net, no training).

All values transcribed from the single current paper:
  Strubell, Ganesh & McCallum, "Energy and Policy Considerations for Modern
  Deep Learning Research", AAAI-20 (Thirty-Fourth AAAI Conference on AI, 2020),
  printed pages 13693-13696. Table 2 (BERTbase row) is on printed page 13695
  (PDF page 3); the method with PUE=1.58 and 0.954->0.477 is on printed page
  13694 (PDF page 2).

This script only does arithmetic on the transcribed numbers plus explicitly
labeled conditional candidates. It does NOT assert any candidate as a paper fact.
"""
from decimal import Decimal, getcontext
import json

getcontext().prec = 28
D = Decimal

# --- Transcribed from Table 2 (printed page 13694) ---
POWER_W = D("12041.51")          # BERTbase V100x64, "Power (W)" (pc+pr+g*pg aggregate)
HOURS = D("79")                  # BERTbase V100x64, "Hours"
KWH_PUE_PRINTED = D("1507")      # BERTbase V100x64, "kWh·PUE"
CO2E_PRINTED = D("719")          # BERTbase V100x64, "CO2e (lb)"
PUE = D("1.58")                  # method, Eq. (1)
EPA_FACTOR = D("0.954")          # method text: EPA US average lb/kWh
FACTOR = D("0.477")              # method Eq. (2): EPA halved for AWS 50% renewable

out = {}

# --- 1) Nominal recompute of the printed 79 hours ---
it_kwh = POWER_W * HOURS / D("1000")          # 12,041.51 W * 79 h -> kWh (before PUE)
total_kwh = it_kwh * PUE                       # kWh·PUE
co2_lb_from_nominal = total_kwh * FACTOR       # lb using recomputed energy
out["nominal_79h"] = {
    "note": "Power(W)/1000 * Hours * PUE; Power column is whole-system aggregate, NOT per-GPU",
    "it_energy_kWh_before_PUE": str(it_kwh),
    "total_energy_kWh_PUE": str(total_kwh),
    "printed_kWh_PUE": str(KWH_PUE_PRINTED),
    "gap_kWh": str(total_kwh - KWH_PUE_PRINTED),
    "gap_pct": str((total_kwh - KWH_PUE_PRINTED) / KWH_PUE_PRINTED * D("100")),
    "co2_lb_from_nominal_energy": str(co2_lb_from_nominal),
    "printed_co2e_lb": str(CO2E_PRINTED),
}

# --- 2) Printed kWh·PUE vs printed CO2e: is CO2e = 0.477 * kWh·PUE? ---
co2_from_printed_kwh = KWH_PUE_PRINTED * FACTOR
out["co2e_vs_printed_kwh"] = {
    "note": "CO2e printed column = 0.477 * printed kWh·PUE (factor applied to the *printed* 1507, not to the 1503 recompute)",
    "0.477_times_1507": str(co2_from_printed_kwh),
    "rounds_to_719": str(co2_from_printed_kwh.quantize(D("1"))),
    "printed_co2e_lb": str(CO2E_PRINTED),
}

# --- 3) Factor derivation: 0.954 / 2 ---
out["factor_derivation"] = {
    "note": "Paper states EPA US avg = 0.954 lb/kWh, then 'we cut this number in half' for AWS 50% renewable. So 0.477 is a constructed AWS-assumption factor, NOT a current universal measured US-grid intensity.",
    "epa_halved": str(EPA_FACTOR / D("2")),
    "uses_epa_2018": True,
    "is_universal_measured_intensity": False,
}

# --- 4) Labeled conditional candidates (NOT paper facts) ---
# (a) If printed 1507 kWh and PUE=1.58 are exact and Power=12,041.51 W exact,
#     the implied wall-clock hours.
implied_hours = KWH_PUE_PRINTED * D("1000") / (POWER_W * PUE)
# (b) If printed 1507 kWh, Hours=79, PUE=1.58 exact, implied aggregate power.
implied_power = KWH_PUE_PRINTED * D("1000") / (HOURS * PUE)
# (c) What the OLD factor (0.954, the ACL-2019 paper's factor) would give; NOT in this paper.
co2_old_factor = KWH_PUE_PRINTED * EPA_FACTOR
out["conditional_candidates"] = {
    "candidate_A_implied_hours_if_power_and_pue_exact": {
        "label": "conditional candidate, NOT a paper fact",
        "value_hours": str(implied_hours),
        "rounds_to": str(implied_hours.quantize(D("0.1"))),
    },
    "candidate_B_implied_power_W_if_hours_and_pue_exact": {
        "label": "conditional candidate, NOT a paper fact",
        "value_watts": str(implied_power),
    },
    "candidate_C_old_factor_0p954_never_in_this_paper": {
        "label": "old EPA factor result, from the earlier ACL-2019 paper, NOT this AAAI-20 paper",
        "0p954_times_1507_lb": str(co2_old_factor),
        "rounds_to": str(co2_old_factor.quantize(D("1"))),
    },
}

# --- 5) NAS vs T2Tbig power equality (observation only, not proof of copying) ---
out["nas_vs_t2tbig"] = {
    "observation": "Table 2 lists identical Power = 1515.43 W for 'NAS P100x8' and 'T2Tbig P100x8'.",
    "claim_evaluated": "NAS与T2Tbig功率相同，证明直接复制了同一测量值",
    "verdict": "Equality is real in the table, but the paper does not state that one was copied from the other; same value alone cannot prove shared origin or non-independence. Keep as an unchecked inference requiring method/log evidence.",
}

print(json.dumps(out, ensure_ascii=False, indent=2))
