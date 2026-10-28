"""Author-side conditional comparison; different papers, not a correction or new experiment."""
from fractions import Fraction as F
from decimal import Decimal as D,localcontext,ROUND_HALF_UP
import json

def shown(f):
 with localcontext() as c:
  c.prec=40
  x=D(f.numerator)/D(f.denominator)
  return {'exact':str(f),'decimal':str(x),'integer_half_up':str(x.quantize(D('1'),rounding=ROUND_HALF_UP))}
def calculate():
 energy=F('12041.51')*F('79.2')*F('1.58')/1000
 out=[]
 for venue,year,factor,table,page,printed,co2 in [('ACL',2019,'0.954','Table3',4,3648,1438),('AAAI',2020,'0.477','Table2',3,13695,719)]:
  out.append({'paper':venue+str(year),'table':table,'PDF_page':page,'printed_page':printed,'power_W':'12041.51','displayed_hours':'79','displayed_energy_kWh':'1507','factor_lb_per_kWh':factor,'displayed_carbon_lb':co2,'displayed_energy_times_factor':shown(F('1507')*F(factor)),'unrounded_79_2h_energy_kWh':shown(energy),'unrounded_energy_times_factor':shown(energy*F(factor))})
 assert [x['unrounded_energy_times_factor']['integer_half_up'] for x in out]==['1438','719']
 return {'case':'same model row, distinct publications and conversion assumptions','rows':out,'factor_ratio_AAAI2020_over_ACL2019':shown(F('.477')/F('.954')),'energy_change_from_these_table_displays':'none: both display1507; not a new measurement','erratum_status':'not established by supplied material','actual_hardware_or_meter_energy_change':'not established','source_power_mapping':'still not identified','limitations':'AAAI2020source is a limited legal excerpt; applying one paper factor to another version without label is unsupported; not current local emission factors'}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2))
