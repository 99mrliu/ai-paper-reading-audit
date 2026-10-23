"""Recalculate descriptive results offline from preserved native session metadata."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent
result={}
for name in ['transfer','energy']:
 rows={}
 for p in sorted((r/'experiments'/name/'runs').glob('*/session.json')):
  d=json.loads(p.read_text());rows[p.parent.name]={'seconds':d['duration_seconds'],'tool_calls':d['tool_calls'],'usage':d['usage'],'exit_code':d['exit_code'],'session_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 assert len(rows)==7
 with_mean=sum(rows[x+'-with']['seconds'] for x in ['A1','A2'])/2
 without_mean=sum(rows[x+'-without']['seconds'] for x in ['A1','A2'])/2
 result[name]={'runs':rows,'mean_with_seconds':with_mean,'mean_without_seconds':without_mean,'relative_increase_percent':(with_mean/without_mean-1)*100}
out=r/'verification/results.json';out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{x:y for x,y in v.items() if x!='runs'} for k,v in result.items()},indent=2))
