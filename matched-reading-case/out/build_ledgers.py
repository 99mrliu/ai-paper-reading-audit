import json
from pathlib import Path
q=lambda v,u,**kw:dict(value=str(v),unit=u,**kw)
def row(i,p,t,e,c,source):
 return dict(id=i,source=source,power=q(p,'W'),power_scope='aggregate',duration=q(t,'h'),measurement_scope='it',pue={'value':'1.58'},intensity=q('.954','lb/kWh'),reported_energy=q(e,'kWh'),reported_carbon=q(c,'lb'))
rows=[row('bert_table_nominal','12041.51','79','1507','1438','PDF4 Table3 BERT V100x64; aggregate IT power inferred from equation1, not per GPU'),row('t2tbig_nominal','1515.43','84','201','192','PDF4 Table3 T2Tbig P100x8'),row('nas_nominal','1515.43','274120','656347','626155','PDF4 Table3 NAS P100x8; extrapolated GPU scenario, not TPU meter')]
Path('out/ledger-nominal.json').write_text(json.dumps({'records':rows},indent=2))
candidates=[]
for t in ['79.2','79.21']:
 r=row('bert_candidate_'+t,'12041.51',t,'1507','1438','Candidate: PDF3 gives79.2h;79.21h is constructed counterexample, not observed')
 r['reported_energy']['quantum']='1';r['reported_carbon']['quantum']='1';candidates.append(r)
r=row('bert_display_rounding','12041.51','79','1507','1438','Conditional display rounding only; PDF4 table input retained')
r['duration']['quantum']='1';r['power']['quantum']='0.01';r['reported_energy']['quantum']='1';r['reported_carbon']['quantum']='1';candidates.append(r)
candidates += [dict(id='paper_201_factor',source='PDF4 Table3 T2Tbig facility-equivalent estimate already includes PUE; PDF2 factor .954',energy=q('201','kWh'),measurement_scope='facility',intensity=q('.954','lb/kWh')),dict(id='user_201_unknown_boundary',source='INPUT/task.md hypothetical local meter201kWh; time covers training; physical boundary/location/attribution/intensity unknown',energy=q('201','kWh')),dict(id='user_201_if_facility',source='INPUT/task.md hypothetical201kWh; conditional assumption dedicated facility meter; local intensity remains missing',energy=q('201','kWh'),measurement_scope='facility')]
Path('out/ledger-candidates.json').write_text(json.dumps({'records':candidates},indent=2))
