import json
from pathlib import Path
rows=[('t2t_base','1415.78','12','27','26'),('t2t_big','1515.43','84','201','192'),('elmo','517.66','336','275','262'),('bert_gpu','12041.51','79','1507','1438'),('nas_gpu','1515.43','274120','656347','626155')]
records=[]
for ident,p,t,e,c in rows:
 for mode in ['nominal','round_display','round_all']:
  r=dict(id=ident+'_'+mode,source=f'PDF p4 Table 3 {ident}: {p} W, {t} h, {e} kWh·PUE, {c} lb; aggregate IT interpretation from Eq(1)',power=dict(value=p,unit='W'),power_scope='aggregate',duration=dict(value=t,unit='h'),measurement_scope='it',pue=dict(value='1.58'),intensity=dict(value='0.954',unit='lb/kWh'),reported_energy=dict(value=e,unit='kWh'),reported_carbon=dict(value=c,unit='lb'))
  if mode!='nominal':
   for k,q in [('power','0.01'),('duration','1'),('reported_energy','1'),('reported_carbon','1')]:r[k]['quantum']=q
  if mode=='round_all':
   r['pue']['quantum']='0.01';r['intensity']['quantum']='0.001'
  records.append(r)
records += [dict(id='bert_79_2',source='PDF p3 §2.1 reports 79.2 h; Table 3 p4 power 12041.51 W',power=dict(value='12041.51',unit='W'),power_scope='aggregate',duration=dict(value='79.2',unit='h'),measurement_scope='it',pue=dict(value='1.58'),intensity=dict(value='0.954',unit='lb/kWh')),
 dict(id='local_it',source='INPUT/task.md: 8 GPUs aggregate IT mean 1.51543 kW, 84 h; conditional use of paper PUE/intensity',power=dict(value='1.51543',unit='kW'),power_scope='aggregate',duration=dict(value='84',unit='h'),measurement_scope='it',pue=dict(value='1.58'),intensity=dict(value='0.954',unit='lb/kWh')),
 dict(id='local_facility',source='INPUT/task.md: facility meter 201 kWh; local intensity not supplied',energy=dict(value='201',unit='kWh'),measurement_scope='facility'),
 dict(id='local_facility_paper_factor',source='INPUT/task.md: facility meter 201 kWh; conditional historical paper factor',energy=dict(value='201',unit='kWh'),measurement_scope='facility',intensity=dict(value='0.954',unit='lb/kWh')),
 dict(id='tpu_unknown',source='PDF p4 Table 3 TPU rows omit power, energy, carbon',power=None,power_scope='aggregate',duration=dict(value='96',unit='h'),measurement_scope='it',pue=dict(value='1.58'),intensity=dict(value='0.954',unit='lb/kWh'))]
Path('out/ledger.json').write_text(json.dumps(dict(records=records),ensure_ascii=False,indent=2)+'\n')
