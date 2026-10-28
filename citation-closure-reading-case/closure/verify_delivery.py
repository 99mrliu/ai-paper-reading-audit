"""Author replay and exact numeric checks; does not judge citation semantics."""
from pathlib import Path
from fractions import Fraction as F
import json,subprocess,sys,tempfile,shutil,hashlib
r=Path(__file__).resolve().parent;a=r/'first-artifacts'
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);shutil.copy2(a/'calc.py',t/'calc.py')
 p=subprocess.run([sys.executable,'calc.py'],cwd=t,capture_output=True,text=True,check=True)
 saved=json.loads((a/'calc.json').read_text());assert json.loads(p.stdout)==saved==json.loads((t/'calc.json').read_text())
 for row in saved['table3_recomputation'].values():
  e=F(row['power_W'])*F(row['hours_table'])*F('1.58')/1000
  assert F(row['kWh_PUE_exact'])==e
  assert F(row['CO2e_exact'])==e*F('.954')
 assert F(saved['BERTbase_79h_vs_79.2h']['kWh_PUE_exact_h79.2'])==F('12041.51')*F('79.2')*F('1.58')/1000
 assert saved['BERTbase_79h_vs_79.2h']['kWh_PUE_rounded_h79']==1503
 assert saved['BERTbase_79h_vs_79.2h']['CO2e_rounded_h79']==1434
 # Strict endpoints from exact rational input; Decimal endpoint strings are finite approximations.
 d=F('12041.51')*F('1.58')/1000
 lo=max(F('1506.5')/d,F('1437.5')/F('.954')/d)
 hi=min(F('1507.5')/d,F('1438.5')/F('.954')/d)
 assert lo<=F('79.2')<hi and not lo<=F('79')<hi
 assert lo<=F('79.21')<hi
 v=saved['back_solve_interval_hours'];assert abs(F(v['t_intersection_low'])-lo)<F(1,10**45)
 assert abs(F(v['t_intersection_high'])-hi)<F(1,10**45)
 assert F(saved['factor_checks']['CO2e_if_1507kWh_x_0.477_lb_per_kWh'])==F('718.839')
print(json.dumps({'saved_AI_calc_replay':'equal','row_energy_and_carbon_fraction_checks':5,'shared_interval_not_unique':True,'semantics':'Author review required: replay does not validate equals signs in prose, source provenance or causal claims.'},ensure_ascii=False))
