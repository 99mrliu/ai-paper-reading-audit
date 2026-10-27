"""Author-side exact conditional checks, not original measurements or AI output."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json

def show(x):
    with localcontext() as c:
        c.prec = 32
        return {"fraction": str(x), "decimal": str(Decimal(x.numerator)/Decimal(x.denominator))}

def calculate():
    power, pue, factor, hours = map(F, ("12041.51", "1.58", "0.477", "79"))
    rate = power*pue/1000
    energy, carbon = rate*hours, rate*hours*factor
    # Positive round-half-up: lower endpoint included, upper excluded.
    constraints = {"displayed_hours": (F("78.5"), F("79.5")),
                   "displayed_energy": (F("1506.5")/rate, F("1507.5")/rate),
                   "displayed_carbon": (F("718.5")/(rate*factor), F("719.5")/(rate*factor))}
    lo, hi = max(v[0] for v in constraints.values()), min(v[1] for v in constraints.values())
    assert lo < hi
    assert energy == F("1503.0212782") and carbon == F("716.9411497014")
    assert F("1507")*factor == F("718.839")
    assert not (energy == F("1507"))
    # One common t must satisfy all three displays: no independent-overlap shortcut.
    candidate = F("79.21")
    assert all(a <= candidate < z for a,z in constraints.values())
    assert not all(a <= hours < z for a,z in constraints.values())
    return {"kind":"author exact arithmetic, conditional, not scientific validation",
      "nominal": {"formula":"E_kWh = W * h * PUE / 1000; C_lb = E_kWh * lb_per_kWh",
        "energy_kWh":show(energy), "carbon_lb":show(carbon),
        "energy_residual_kWh":show(energy-1507), "carbon_residual_lb":show(carbon-719),
        "carbon_residual_kg":show((carbon-719)*F("0.45359237"))},
      "display_products": {"1507_x_0477":show(1507*factor), "1507_x_0954":show(1507*F("0.954")),
        "warning":"718.839 rounds to719; compatible arithmetic does not identify authors' internal input/order"},
      "zero_quantum_energy_point_overlap":False,
      "duration_quantum_1h_closed_envelope_kWh":[show(rate*F("78.5")),show(rate*F("79.5"))],
      "reported_energy_quantum_only_overlap":False,
      "three_display_joint_half_up_hours":{
        "assumptions":"Fixed exact displayed power/PUE/factor; hours,energy,carbon shown at step1, all positive round-half-up. Article did not specify this implementation. No2020body79.2 constraint.",
        "constraints":{k:[show(a),show(z)] for k,(a,z) in constraints.items()},
        "intersection":[show(lo),show(hi)], "lower_included":True,"upper_included":False,
        "candidate79.21_is_compatible":True,"exact79_is_compatible":False},
      "scope_limits":["calculator closed envelopes are not exact half-up membership at upper ties",
        "individual energy/carbon envelope overlaps do not generally imply one shared feasible time",
        "a possible duration is not the actual training time; no measurements, logs or universal factor inferred"]}

if __name__ == '__main__':
    print(json.dumps(calculate(),ensure_ascii=False,indent=2))
