"""Independent inverse bounds; only a display-rounding assumption, no measurement CI."""
from decimal import Decimal as D,getcontext
import json
getcontext().prec=36
p=D('12.04151');pue=D('1.58');factor=D('.954')
def bounds(rate,lower,upper):return [D(lower)/rate,D(upper)/rate]
def overlap(a,b):return [max(a[0],b[0]),min(a[1],b[1])]
# Whole-number table displays assumed rounded within +/- .5; endpoints enclosed conservatively.
t_energy=bounds(p*pue,'1506.5','1507.5');t_carbon=bounds(p*pue*factor,'1437.5','1438.5');t=overlap(t_energy,t_carbon)
u_energy=bounds(p*D(79),'1506.5','1507.5');u_carbon=bounds(p*D(79)*factor,'1437.5','1438.5');u=overlap(u_energy,u_carbon)
assert t[0]<=D('79.2')<=t[1] and not t[0]<=D(79)<=t[1]
assert u[0]<=D('1.5841')<=u[1]
result={'assumptions':'power 12041.51 W and intensity .954 lb/kWh fixed, whole table values within +/-0.5; closed bounds conservative, not confidence interval', 'duration_hours_at_fixed_PUE_1.58':{'energy_constraint':t_energy,'carbon_constraint':t_carbon,'intersection':t,'79_2_compatible':True,'79_compatible':False},'PUE_at_fixed_79_hours':{'intersection':u,'example_1_5841_compatible':True},'counterexample_79_21_hours':{'energy_kWh':p*pue*D('79.21'),'carbon_lb':p*pue*D('79.21')*factor},'facility_201_kWh_historical_carbon_lb':D(201)*factor,'interpretation':'79.2 has direct source support on PDF page3. Alternative PUE is hypothetical, not observed. Arithmetic compatibility cannot identify authors internal computation or establish measurement validity.'}
print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
