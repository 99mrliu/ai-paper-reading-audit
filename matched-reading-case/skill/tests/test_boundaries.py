"""Synthetic boundary checks with hand-derived expectations; not model experiments."""
from pathlib import Path
import copy,importlib.util,json,sys
p=Path(__file__).resolve().parents[1]/'scripts/audit_energy.py'
if len(sys.argv)>1:p=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('calculator',p);a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def q(v,u):return {'value':str(v),'unit':u}
base={'id':'x','source':'synthetic: 1kW * 2h * PUE1.5 * 0.4kg/kWh', 'power':q(1,'kW'),'power_scope':'aggregate','duration':q(2,'h'),'measurement_scope':'it','pue':q(1.5,''),'intensity':q(.4,'kg/kWh')}
cases=[]
def check(name,mutate,expected,energy=None,carbon=None):
 d=copy.deepcopy(base);mutate(d)
 try:
  result=a.run({'records':[d]})['records'][0]
  passed=result['status']==expected
  if energy is not None:passed &= a.D(result['energy_kWh']['nominal'])==a.D(str(energy))
  if carbon is not None:passed &= a.D(result['carbon_kg']['nominal'])==a.D(str(carbon))
  cases.append({'test':name,'passed':bool(passed),'expected_status':expected,'actual':result})
 except Exception as e:cases.append({'test':name,'passed':False,'error':type(e).__name__+': '+str(e)})
check('nominal hand oracle',lambda d:None,'ok',3,1.2)
check('W equivalent',lambda d:d.update(power=q(1000,'W')),'ok',3,1.2)
check('minutes equivalent',lambda d:d.update(duration=q(120,'min')),'ok',3,1.2)
check('grams equivalent',lambda d:d.update(intensity=q(400,'g/kWh')),'ok',3,1.2)
check('per-device sum',lambda d:d.update(power=q(.25,'kW'),power_scope='per_device',devices=4),'ok',3,1.2)
check('aggregate double-count rejected',lambda d:d.update(devices=4),'invalid')
check('facility PUE double-count rejected',lambda d:d.update(energy=q(3,'kWh'),measurement_scope='facility',power=None),'invalid')
def facility(d):
 for k in ['power','power_scope','duration','pue']:d.pop(k)
 d.update(energy=q(3,'kWh'),measurement_scope='facility')
check('facility direct meter',facility,'ok',3,1.2)
def twice(d):facility(d);d['pue']=q(1.5,'')
check('facility genuine double PUE',twice,'invalid')
check('unknown intensity retains energy',lambda d:d.pop('intensity'),'partial',3)
check('unknown PUE stays unknown',lambda d:d.pop('pue'),'unknown')
check('unknown power is not zero',lambda d:d.update(power=q(None,'kW')),'invalid')
check('missing power is unknown',lambda d:d.update(power={'value':None,'unit':'kW'}),'unknown')
check('boolean rejected',lambda d:d.update(duration={'value':True,'unit':'h'}),'invalid')
check('NaN rejected',lambda d:d.update(power=q('NaN','kW')),'invalid')
check('negative rejected',lambda d:d.update(duration=q(-2,'h')),'invalid')
check('fractional devices rejected',lambda d:d.update(power_scope='per_device',devices=1.5),'invalid')
check('allocation greater than one rejected',lambda d:d.update(allocation=1.1),'invalid')
check('PUE under one rejected',lambda d:d.update(pue=q(.9,'')),'invalid')
def malformed(d):d.pop('power');d['components']=[None]
check('malformed component returns invalid without crash',malformed,'invalid')
# Partition invariance and energy-weighted intensity: 1 kWh*.2 + 3kWh*.8 =2.6kg,
# whereas unweighted mean intensity *. total is .5*4=2kg, demonstrably wrong.
rows=[]
for i,(energy,intensity) in enumerate([(1,.2),(3,.8)]):
 d={'id':str(i),'source':'synthetic disjoint periods','energy':q(energy,'kWh'),'measurement_scope':'facility','intensity':q(intensity,'kg/kWh'),'group':'time'};rows.append(d)
g=a.run({'records':rows})['groups']['time'];cases.append({'test':'time-weighted carbon oracle','passed':a.D(g['energy_kWh']['nominal'])==4 and a.D(g['carbon_kg']['nominal'])==a.D('2.6'),'actual':g,'wrong_unweighted_carbon_kg':'2.0'})
# A malformed component must not suppress the following valid record.
bad=copy.deepcopy(base);malformed(bad);good=copy.deepcopy(base);good['id']='next'
try:
 out=a.run({'records':[bad,good]});cases.append({'test':'bad-record isolation','passed':[x['status'] for x in out['records']]==['invalid','ok']})
except Exception as e:cases.append({'test':'bad-record isolation','passed':False,'error':type(e).__name__})
print(json.dumps({'tests':len(cases),'passed':sum(x['passed'] for x in cases),'cases':cases},ensure_ascii=False,indent=2))
sys.exit(0 if all(x['passed'] for x in cases) else 1)
