#!/usr/bin/env python3
"""Reproduce Strubell et al. ACL 2019 (eq.1/eq.2 + Table 3) arithmetic.

pt    = 1.58 * t * W / 1000        # kWh with PUE (W = pc + pr + g*pg)
CO2e  = 0.954 * pt                 # lb CO2e (US avg grid factor, EPA)
"""

PUE = 1.58
F = 0.954

rows = {
    "T2Tbase":  (1415.78, 12),
    "T2Tbig":   (1515.43, 84),
    "ELMo":     (517.66, 336),
    "BERTbase": (12041.51, 79),     # table shows "Hours 79"
    "BERT 79.2":(12041.51, 79.2),   # body text: 3.3 days = 79.2 h
    "NAS":      (1515.43, 274120),
}

print(f"{'model':<12}{'t(h)':>9}{'pt(kWh)':>13}{'CO2e(lb)':>13}{'pt_rnd':>8}{'co2_rnd':>8}")
for name, (w, t) in rows.items():
    pt = PUE * t * w / 1000.0
    co2 = F * pt
    print(f"{name:<12}{t:>9.6g}{pt:>13.4f}{co2:>13.4f}{round(pt):>8}{round(co2):>8}")

print()
print("Note's arithmetic check (PDU 201 kWh):")
print("  0.954 * 201      =", 0.954 * 201, " <- note writes 191.88")
print("  0.954 * 201.1279 =", 0.954 * 1.58 * 84 * 1515.43 / 1000,
      " <- unrounded T2Tbig pt")

print()
print("Unique t consistent with BERT displayed outputs (t = ...):")
w = 12041.51
for label, target in [("pt=1507", 1507), ("CO2e=1438", 1438)]:
    if label.startswith("pt"):
        t = target * 1000 / (PUE * w)
    else:
        t = target * 1000 / (F * PUE * w)
    print(f"  {label}: t = {t:.4f} h")
print("  t=79  -> pt={:.2f}, CO2e={:.2f}".format(PUE*79*w/1000, F*PUE*79*w/1000))
print("  t=79.2-> pt={:.2f}, CO2e={:.2f}".format(PUE*79.2*w/1000, F*PUE*79.2*w/1000))
