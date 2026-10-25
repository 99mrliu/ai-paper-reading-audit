import json
from pathlib import Path
rows=[]
for name,p,t,e,c in [('T2Tbase','1415.78','12','27','26'),('T2Tbig','1515.43','84','201','192'),('ELMo','517.66','336','275','262'),('BERTbase_GPU','12041.51','79','1507','1438'),('NAS_GPU','1515.43','274120','656347','626155')]:
 r={'id':name,'source':f'PDF p4 (3648), Table 3 {name}: {p} W, {t} h, {e} kWh·PUE, {c} lb; aggregate IT interpretation under Eq.1','power':{'value':p,'unit':'W'},'power_scope':'aggregate','duration':{'value':t,'unit':'h'},'measurement_scope':'it','pue':{'value':'1.58'},'intensity':{'value':'0.954','unit':'lb/kWh'},'reported_energy':{'value':e,'unit':'kWh'},'reported_carbon':{'value':c,'unit':'lb'}}
 rows.append(r)
 q=json.loads(json.dumps(r));q['id']+='_rounding';q['source']+='; conditional nearest rounding: power .01W, hours 1h, outputs 1kWh/1lb; PUE and intensity fixed'
 for key,quantum in [('power','.01'),('duration','1'),('reported_energy','1'),('reported_carbon','1')]:q[key]['quantum']=quantum
 rows.append(q)
 rows.append({'id':name+'_printed_energy_to_carbon','source':f'PDF p4 Table 3: test printed facility energy {e} kWh times Eq.2 .954 lb/kWh against {c} lb; conditional nearest integer displays','energy':{'value':e,'unit':'kWh','quantum':'1'},'measurement_scope':'facility','intensity':{'value':'.954','unit':'lb/kWh'},'reported_carbon':{'value':c,'unit':'lb','quantum':'1'}})
rows.extend([
{'id':'BERT_79_2_sensitivity','source':'PDF p3 (3647) §2.1 reports 79.2h; use Table3 power and compare its outputs','power':{'value':'12041.51','unit':'W'},'power_scope':'aggregate','duration':{'value':'79.2','unit':'h'},'measurement_scope':'it','pue':{'value':'1.58'},'intensity':{'value':'.954','unit':'lb/kWh'},'reported_energy':{'value':'1507','unit':'kWh'},'reported_carbon':{'value':'1438','unit':'lb'}},
{'id':'local_IT_model','source':'User data: aggregate average IT 1.51543kW for 84h; conditional paper PUE and US historical factor','power':{'value':'1.51543','unit':'kW'},'power_scope':'aggregate','duration':{'value':'84','unit':'h'},'measurement_scope':'it','pue':{'value':'1.58'},'intensity':{'value':'.954','unit':'lb/kWh'}},
{'id':'local_facility_model','source':'User data: facility meter 201kWh; conditional paper historical US intensity','energy':{'value':'201','unit':'kWh'},'measurement_scope':'facility','intensity':{'value':'.954','unit':'lb/kWh'}},
{'id':'local_facility_actual_carbon_unknown','source':'User facility meter 201kWh; applicable site/time intensity not supplied','energy':{'value':'201','unit':'kWh'},'measurement_scope':'facility'},
{'id':'TPU_unknown','source':'PDF p4 Table3 TPU power and energy omitted; no zero substitution','power':{'value':None,'unit':'W'},'power_scope':'aggregate','duration':{'value':'96','unit':'h'},'measurement_scope':'it','pue':{'value':'1.58'},'intensity':{'value':'.954','unit':'lb/kWh'}}])
Path('out/ledger.json').write_text(json.dumps({'records':rows},ensure_ascii=False,indent=2)+'\n')
