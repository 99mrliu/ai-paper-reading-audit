from decimal import Decimal as D, localcontext, ROUND_HALF_UP
from fractions import Fraction as F
import json

def fraction(x):return F(str(x))
def show(f):
 with localcontext() as ctx:
  ctx.prec=50
  return {'exact':str(f),'decimal':str(D(f.numerator)/D(f.denominator))}
def calculate():
 rate=fraction('12041.51')*fraction('1.58')/1000
 carbon_rate=rate*fraction('0.954')
 energy=(fraction('1506.5')/rate,fraction('1507.5')/rate)
 carbon=(fraction('1437.5')/carbon_rate,fraction('1438.5')/carbon_rate)
 time=(fraction('78.5'),fraction('79.5'))
 body=(fraction('79.15'),fraction('79.25'))
 low=max(energy[0],carbon[0],time[0],body[0]);high=min(energy[1],carbon[1],time[1],body[1])
 trunc_low=max(fraction(79),fraction("79.2"),fraction(1507)/rate,fraction(1438)/carbon_rate)
 trunc_high=min(fraction(80),fraction("79.3"),fraction(1508)/rate,fraction(1439)/carbon_rate)
 assert low<high and trunc_low<trunc_high and low!=trunc_low and high!=trunc_high
 points={}
 for t in ['79','79.2','79.21','79.24']:
  e=rate*fraction(t);c=carbon_rate*fraction(t)
  points[t]={'energy_kWh':show(e),'carbon_lb':show(c),'same_t_jointly_compatible':low<=fraction(t)<high}
 disp=fraction('201')*fraction('0.954');unr=fraction('1515.43')*84*fraction('1.58')/1000
 assert disp==fraction('191.754')
 assert unr==fraction('201.1278696')
 assert unr*fraction('0.954')==fraction('191.8759875984')
 assert points['79']['same_t_jointly_compatible'] is False
 assert points['79.2']['same_t_jointly_compatible'] and points['79.21']['same_t_jointly_compatible']
 assert not points['79.24']['same_t_jointly_compatible']
 return {'scope':'author arithmetic verification; not model output, source validation, measurement or confidence interval',
 'rounding_assumption':'nonnegative round-half-up, time/energy/carbon quantum 1; coefficients held fixed; independent direct outputs, not intermediate rounded energy',
 'displayed_201_times_factor_lb':show(disp),'unrounded_energy_kWh':show(unr),'unrounded_energy_times_factor_lb':show(unr*fraction('0.954')),
 'energy_time_interval':{'lower':show(energy[0]),'upper':show(energy[1]),'endpoints':'[lower,upper)'},
 'carbon_time_interval':{'lower':show(carbon[0]),'upper':show(carbon[1]),'endpoints':'[lower,upper)'},
 'joint_time_interval':{'lower':show(low),'upper':show(high),'endpoints':'[lower,upper)'},'points':points,
 'truncation_joint_time_interval':{'lower':show(trunc_low),'upper':show(trunc_high),'endpoints':'[lower,upper)'},
 'body_79_2_half_up_interval':['79.15','79.25'],
 'semantic_checks_not_automated':['PDF transcription and original source attribution','physical meter boundary and allocation choice','internal author calculation and power provenance']}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2))
