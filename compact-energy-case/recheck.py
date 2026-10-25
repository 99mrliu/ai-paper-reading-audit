from pathlib import Path
from decimal import Decimal as D
import hashlib,json,subprocess,sys,tempfile
r=Path(__file__).resolve().parent;p=json.loads((r/'provenance.json').read_text())
for name,item in p['original_files'].items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==item['sha256'],name
assert hashlib.sha256((r/'evidence/selected-operations.jsonl').read_bytes()).hexdigest()==p['selected_events_sha256']
with tempfile.TemporaryDirectory() as tmp:
 out=Path(tmp)/'calculations.json'
 q=subprocess.run([sys.executable,str(r/'skill/scripts/audit_energy.py'),str(r/'evidence/ledger.json'),'--out',str(out)],capture_output=True,text=True,check=True)
 actual=json.loads(out.read_text());saved=json.loads((r/'evidence/calculations.json').read_text());assert actual==saved
 rows={x['id']:x for x in actual['records']};assert len(rows)==25
 assert rows['BERTbase_GPU_fixed_hours_rounding']['energy_check']['conditional_rounding_overlap'] is False
 assert rows['BERTbase_GPU_fixed_hours_rounding']['carbon_check']['conditional_rounding_overlap'] is False
 assert rows['BERTbase_GPU']['energy_kWh']['nominal']=='1503.0212782'
 assert rows['BERT_79_2_sensitivity']['energy_kWh']['nominal']=='1506.82639536'
 statuses={s:sum(x['status']==s for x in rows.values()) for s in {x['status'] for x in rows.values()}}
 assert statuses=={'ok':23,'partial':1,'unknown':1}
 print(json.dumps({'status':'passed','records':25,'record_statuses':statuses,'original_ledger_hash_verified':actual['ledger_sha256'],
   'BERT_fixed_79h_comparison':'retained failure','scope':'Exact saved-ledger arithmetic and file integrity; not source semantics, physical validation or new AI reading.'},ensure_ascii=False,indent=2))
