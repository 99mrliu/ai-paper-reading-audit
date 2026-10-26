from pathlib import Path
from decimal import Decimal as D
import json, subprocess, hashlib
root=Path('.')
def c(i,r,y,q=1): return dict(id=i,rate=str(r),display=str(y),quantum=str(q))
e=D('12041.51')*D('1.58')/1000
b=e*D('0.954')
cases={
'A':dict(rounding='half_up',constraints=[c('time',1,0,20),c('energy',1,2),c('carbon',1,8)]),
'C_half_up':dict(rounding='half_up',constraints=[c('y1',1,2),c('y2',3,8)]),
'C_half_even':dict(rounding='half_even',constraints=[c('y1',1,2),c('y2',3,8)])}
for rule in ['half_up','half_even']:
 for t in ['79','79.2','79.21']:
  cases[f'B_{rule}_{t}']=dict(rounding=rule,constraints=[c('time',1,79),c('energy',e,1507),c('carbon',b,1438)],fixed_parameter=t)
logs=[]
for name,data in cases.items():
 ip=Path(f'out/{name}.input.json');op=Path(f'out/{name}.result.json')
 ip.write_text(json.dumps(data,indent=2)+'\n')
 cmd=['python3','skill/scripts/joint_bounds.py',str(ip),'--out',str(op)]
 p=subprocess.run(cmd,capture_output=True,text=True)
 logs.append(dict(case=name,argv=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr))
 result=json.loads(op.read_text())
 print(name,json.dumps(result,ensure_ascii=False))
Path('out/execution-log.json').write_text(json.dumps(logs,indent=2)+'\n')
nominal=[]
for t in ['79','79.2','79.21']:
 v=D(t);nominal.append(dict(t=t,energy=str(e*v),carbon=str(b*v)))
Path('out/normalization.json').write_text(json.dumps(dict(energy_rate=str(e),carbon_rate=str(b),candidates=nominal,sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in ['INPUT/paper.pdf','skill/SKILL.md','skill/scripts/joint_bounds.py']}),indent=2)+'\n')
print('NORMALIZATION',e,b,nominal)
