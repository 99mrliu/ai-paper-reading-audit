"""Probe a declared two-parameter power model; source provenance always remains unidentified.
Usage: python3 table_probe.py INPUT.json
Input values are finite decimal strings. Power intervals are conservative CLOSED display bins,
not statistical confidence intervals or strict half-up feasibility certificates.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext, InvalidOperation
from pathlib import Path
import json,sys

def finite(x):
 if not isinstance(x,str):raise ValueError('numeric inputs must be decimal strings')
 try:v=D(x)
 except InvalidOperation:raise ValueError("invalid decimal string")
 if not v.is_finite():raise ValueError('non-finite numeric input')
 return F(v)
def describe(v):
 with localcontext() as c:
  c.prec=40
  return {'exact':str(v),'decimal':str(D(v.numerator)/D(v.denominator))}
def row(r):
 for key in ['id','hardware','source_location']:
  if not isinstance(r.get(key),str) or not r[key]:raise ValueError('row needs '+key)
 g=finite(r['gpu_count']);p=finite(r['power_W']);q=finite(r['display_quantum_W'])
 if g<0 or g.denominator!=1 or p<0 or q<=0:raise ValueError('nonnegative integer count, nonnegative power and positive quantum required')
 return g,p,q
def probe(data):
 if data.get('model')!='P=a+g*b':raise ValueError('only explicit P=a+g*b model is supported')
 fit=data['fit_rows'];checks=data['validation_rows']
 if len(fit)!=2 or not checks:raise ValueError('exactly two fit rows and at least one validation row required')
 all_ids=[r['id'] for r in fit+checks]
 if len(set(all_ids))!=len(all_ids):raise ValueError('duplicate row ID')
 (g0,p0,q0),(g1,p1,q1)=map(row,fit)
 if g0==g1:raise ValueError('fit rows have same count: slope is not identified')
 b=(p1-p0)/(g1-g0);a=p0-g0*b
 results=[]
 for record in checks:
  g,p,q=row(record);w1=(g-g0)/(g1-g0);w0=1-w1
  prediction=w0*p0+w1*p1
  # Conservative display uncertainty propagated with signed interpolation weights.
  radius=abs(w0)*q0/2+abs(w1)*q1/2
  pred=(prediction-radius,prediction+radius);observed=(p-q/2,p+q/2)
  disjoint=pred[1]<observed[0] or observed[1]<pred[0]
  gap=max(F(0),pred[0]-observed[1],observed[0]-pred[1])
  results.append({'id':record['id'],'source_location':record['source_location'],
   'prediction_point_W':describe(prediction),'prediction_minus_display_W':describe(prediction-p),
   'prediction_closed_envelope_W':list(map(describe,pred)),
   'validation_closed_envelope_W':list(map(describe,observed)),
   'disjoint_envelopes':disjoint,'minimum_envelope_gap_W':describe(gap),
   'input_coordinate_duplicates_fit_row':g in (g0,g1),
   'interpretation':'declared common-parameter model rejected by this row even under supplied display uncertainty' if disjoint else 'not rejected by this row; does not establish common measurement/source'})
 return {'model':data['model'],'status':'completed','input_source':data['paper'],
  'fit_parameters_from_display_centres':{'a_W':describe(a),'b_W_per_GPU':describe(b)},
  'cross_hardware_fit':fit[0]['hardware']!=fit[1]['hardware'],
  'assumptions':data['declared_assumptions'],'validation':results,
  'common_model_rejected_within_supplied_envelopes':any(r['disjoint_envelopes'] for r in results),
  'physical_or_causal_parameter_identification':'not established by algebraic fit',
  'measurement_source_provenance':'not identified, including when all validation rows overlap',
  'scope':'only stated linear common-parameter model and supplied closed display envelopes; no automatic transcription, unit conversion, hardware equivalence or source validation'}
if __name__=='__main__':
 try:
  if len(sys.argv)!=2:raise ValueError('Usage: python3 table_probe.py INPUT.json')
  print(json.dumps(probe(json.loads(Path(sys.argv[1]).read_text())),ensure_ascii=False,indent=2))
 except (ValueError,KeyError,TypeError) as e:
  print(json.dumps({'status':'invalid','reason':str(e)},ensure_ascii=False));sys.exit(2)
