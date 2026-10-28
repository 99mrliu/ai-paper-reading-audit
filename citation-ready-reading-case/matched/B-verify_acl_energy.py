#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核对 Strubell et al., ACL 2019 (Energy and Policy Considerations for Deep
Learning in NLP) 笔记中的数值与推理。

常量来源（原文）：
  PUE = 1.58        Eq.(1)，2018 全球数据中心平均 PUE（p.3646）
  EPA = 0.954       Eq.(2)，美国 EPA eGRID 平均 lb CO2e/kWh（p.3646）
  Table 3          p.3648：BERTbase V100x64: Power=12,041.51 W, Hours=79,
                   kWh·PUE=1507, CO2e=1438
  正文 79.2 h      p.3647 §2.1 BERT：“3.3 days (79.2 hours) … 64 V100”
"""
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext

getcontext().prec = 40
D = Decimal

PUE = D("1.58")
EPA = D("0.954")


def kwh(power_w, hours):
    return power_w * hours * PUE / D(1000)


def co2(power_w, hours):
    return EPA * kwh(power_w, hours)


def main():
    # ---- BERT，Power=12,041.51 W ----
    P = D("12041.51")
    h_body = D("79.2")
    h_tbl = D("79")
    print("== BERT (Table 3) ==")
    for name, h in [("79.2 (正文)", h_body), ("79 (表内显示)", h_tbl)]:
        k, c = kwh(P, h), co2(P, h)
        print(f"  h={name}: kWh·PUE={k} -> {k.quantize(D('1'), ROUND_HALF_UP)}; "
              f"CO2e={c} -> {c.quantize(D('1'), ROUND_HALF_UP)}")

    # 唯一性：使 kWh·PUE 舍入为 1507 且 CO2e 舍入为 1438 的 h 区间
    kwh_ph = P * PUE / D(1000)
    co2_ph = EPA * kwh_ph
    lo = max(D("1506.5") / kwh_ph, D("1437.5") / co2_ph)
    hi = min(D("1507.5") / kwh_ph, D("1438.5") / co2_ph)
    print(f"  满足 1507/1438 的 h 区间: [{lo:.6f}, {hi:.6f}) h, "
          f"宽 {(hi - lo) * 60:.1f} min; 79.2 在内={lo <= h_body < hi}; "
          f"79.0 在内={lo <= h_tbl < hi}")
    print(f"  截断检验: trunc(1506.83)={kwh(P, h_body).quantize(D('1'), ROUND_DOWN)}, "
          f"trunc(1437.51)={co2(P, h_body).quantize(D('1'), ROUND_DOWN)}")

    # ---- T2Tbig / NAS 功率相等 ----
    print("== NAS vs T2Tbig ==")
    P8, P64 = D("1515.43"), D("12041.51")
    pg = (P64 - P8) / D(56)      # g=64 与 g=8 两行反解
    pc_pr = P8 - D(8) * pg
    print(f"  反解: pg(每 GPU)={pg} W, pc+pr={pc_pr} W")
    print(f"  NAS(g=8) Power={pc_pr + D(8) * pg} == T2Tbig={P8}")

    # ---- 外部 PDU 假设 ----
    print("== 外部 PDU = 201 kWh ==")
    print(f"  201 * 0.954 = {D('201') * EPA} lb  (笔记写 191.88 -> 错)")
    print(f"  191.88 = 0.954 * {D('191.88') / EPA} kWh "
          f"(即未舍入的 T2Tbig kWh·PUE≈201.128, 而非显示值 201)")
    print(f"  0.954 * 未舍入 201.128 = {EPA * kwh(P8, D('84'))} lb -> 舍入 192")


if __name__ == "__main__":
    main()
