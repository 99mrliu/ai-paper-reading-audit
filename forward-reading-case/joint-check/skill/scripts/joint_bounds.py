"""Exact joint display-rounding feasibility for y_i = positive fixed rate_i * t.
No unit conversion, uncertain rates, source parsing, measurement or causal inference.
"""
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import argparse,json

def value(x):
 if isinstance(x,bool):raise ValueError('Boolean is not a numeric value')
 d=Decimal(str(x))
 if not d.is_finite():raise ValueError('Finite decimal required')
 return F(d)

def show(x):
 with localcontext() as c:
  c.prec=28
  return {'exact':str(x),'decimal':str(Decimal(x.numerator)/Decimal(x.denominator))}

def band(c,rounding):
 rate=value(c['rate']);y=value(c['display']);q=value(c['quantum'])
 if rate<=0 or q<=0 or y<0:raise ValueError('Positive rate/quantum and nonnegative display required')
 k=y/q
 if k.denominator!=1:raise ValueError('Display must be a multiple of quantum')
 lo=max(F(0),y-q/2)/rate;hi=(y+q/2)/rate
 if rounding=='half_up':lc=True;hc=False
 elif rounding=='half_even':lc=hc=(k.numerator%2==0)
 else:raise ValueError('Only explicit half_up or half_even is supported')
 if lo==0 and y-q/2<0:lc=True
 return (lo,hi,lc,hc)

def intersect(a,b):
 lo=max(a[0],b[0]);hi=min(a[1],b[1])
 lc=(a[2] if a[0]==lo else True) and (b[2] if b[0]==lo else True)
 hc=(a[3] if a[1]==hi else True) and (b[3] if b[1]==hi else True)
 return (lo,hi,lc,hc)

def feasible(b):return b[0]<b[1] or b[0]==b[1] and b[2] and b[3]

def contains(b,t):return (t>b[0] or t==b[0] and b[2]) and (t<b[1] or t==b[1] and b[3])

def packed(b):return {'lower':show(b[0]),'upper':show(b[1]),'lower_closed':b[2],'upper_closed':b[3],'nonempty':feasible(b)}

def solve(data):
 cs=data['constraints'];rounding=data['rounding']
 if not isinstance(cs,list) or not cs:raise ValueError('Nonempty constraints required')
 ids=[c['id'] for c in cs]
 if len(set(ids))!=len(ids):raise ValueError('Duplicate constraint id')
 bs=[band(c,rounding) for c in cs];joint=bs[0]
 for b in bs[1:]:joint=intersect(joint,b)
 witness=None
 if feasible(joint):
  t=(joint[0]+joint[1])/2
  assert all(contains(b,t) for b in bs)
  witness=show(t)
 fixed=None
 if 'fixed_parameter' in data:fixed=all(contains(b,value(data['fixed_parameter'])) for b in bs)
 return {'scope':'one shared nonnegative parameter, fixed positive normalized rates, explicit display-rounding assumption; not physical validation',
  'rounding':rounding,'constraints':{c['id']:packed(b) for c,b in zip(cs,bs)},'joint':packed(joint),
  'joint_feasible':feasible(joint),'witness_parameter':witness,'fixed_parameter_feasible':fixed}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--out',required=True);a=p.parse_args()
 try:out=solve(json.loads(Path(a.input).read_text()));code=0
 except (ValueError,KeyError,TypeError,ArithmeticError) as e:out={'status':'unsupported_or_invalid','reason':str(e)};code=2
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');raise SystemExit(code)
if __name__=='__main__':main()
