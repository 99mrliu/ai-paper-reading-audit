#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
来源推断验收（第二轮，不覆盖 verify_acl_energy.py）。

检查三件事：
  1) Table 3 逐行内部一致性（Power*Hours*1.58/1000 是否等于 kWh·PUE）；
  2) “共同 p_g、p_c+p_r”模型能否预测未参与拟合的行（留出检验）；
  3) 191.88/0.954 与 1515.43*84*1.58/1000 是否精确相等。
"""
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 40
PUE = Fraction(158, 100)      # 1.58
EPA = Fraction(954, 1000)     # 0.954


def F(s):
    return Fraction(s)


def main():
    rows = {
        # name: (g, Power_W, Hours, kWhPUE_table, CO2e_table)
        "T2Tbase": (8,  "1415.78", "12",     "27",     "26"),
        "T2Tbig":  (8,  "1515.43", "84",     "201",    "192"),
        "ELMo":    (3,  "517.66",  "336",    "275",    "262"),
        "BERT":    (64, "12041.51", "79.2",  "1507",   "1438"),
        "NAS":     (8,  "1515.43", "274120", "656347", "626155"),
    }

    print("== 1) 逐行内部一致性（原文实际模型：每行各自 Power）==")
    for name, (g, P, h, k, _) in rows.items():
        calc = F(P) * F(h) * PUE / Fraction(1000)
        print(f"  {name:9s} g={g:3d} 计算={float(calc):12.4f} 表值={k:>7s}")

    print()
    print("== 2) 共同参数模型 Power = a + g*b（仅 T2Tbig、BERT 两点拟合）==")
    b = (F("12041.51") - F("1515.43")) / Fraction(56)
    a = F("1515.43") - Fraction(8) * b
    print(f"  a={float(a):.6f} W, b={float(b):.6f} W（纯两点拟合，非原文模型）")
    print("  留出检验（残差 = 预测 - 表值）：")
    for name, (g, P, _, _, _) in rows.items():
        pred = a + Fraction(g) * b
        resid = pred - F(P)
        note = "拟合点" if name in ("T2Tbig", "BERT") else "留出"
        if name == "NAS":
            note += "（g=8 与 T2Tbig 同点，非判别）"
        print(f"    {name:9s} g={g:3d} 预测={float(pred):10.3f} 表值={P:>9s} "
              f"残差={float(resid):+9.3f} W  [{note}]")

    print()
    print("== 3) 精确除法 vs 乘积 ==")
    x1 = F("191.88") / EPA
    x2 = F("1515.43") * F("84") * PUE / Fraction(1000)
    print(f"  191.88/0.954       = {x1} = {x1.numerator/x1.denominator:.20f}")
    print(f"  1515.43*84*1.58/1000 = {x2} = {float(x2):.20f}")
    print(f"  精确相等? {x1 == x2}；差 = {x1 - x2} = {float(x1 - x2):.20f} kWh")
    prod = EPA * x2
    print(f"  0.954 * (1515.43*84*1.58/1000) = {float(prod):.12f} "
          f"-> 2位={Decimal(prod.numerator)/Decimal(prod.denominator):.2f}")


if __name__ == "__main__":
    main()
