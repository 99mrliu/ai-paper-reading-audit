"""Recompute saved arithmetic without calling AI, networking or modifying frozen results."""
from pathlib import Path
import subprocess,sys,tempfile,shutil,json,hashlib
r=Path(__file__).resolve().parent
assert hashlib.sha256((r/'INPUT/paper.pdf').read_bytes()).hexdigest()=='184c42b148a3db99f4a59ed8336c403dc2229bf3100bbc934212116acd8c61d9'
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);shutil.copytree(r/'skill',t/'skill');shutil.copytree(r/'out',t/'out')
 def run(*args):return subprocess.run([sys.executable,*args],cwd=t,capture_output=True,text=True,check=True)
 run('out/build_ledgers.py');run('out/finalize_evidence.py')
 b=run('skill/tests/test_boundaries.py');(t/'out/boundary-tests.json').write_text(b.stdout);assert json.loads(b.stdout)['passed']==22
 run('out/independent_check.py')
 for n in ['nominal','candidates','rounding']:
  run('skill/scripts/audit_energy.py','out/ledger-'+n+'.json','--out','out/calculations-'+n+'.json')
 for n in ['ledger-nominal.json','ledger-candidates.json','ledger-rounding.json','calculations-nominal.json','calculations-candidates.json','calculations-rounding.json','independent-results.json','claims.json','boundary-tests.json']:
  assert json.loads((t/'out'/n).read_text())==json.loads((r/'out'/n).read_text()),n
 a=json.loads((t/'out/independent-results.json').read_text());assert a['paper_factor_applied_to_201_lb']=='191.754'
 assert a['bert_point_calculations']['79.21']['carbon_lb']=='1437.693885261972'
v=subprocess.run([sys.executable,str(r/'science-space/author_verify.py')],capture_output=True,text=True,check=True)
assert json.loads(v.stdout)==json.loads((r/'science-space/author-verification.json').read_text())
print(json.dumps({'status':'passed','recomputed_json_artifacts':9,'boundary_tests':22,'added_author_fraction_models':2,'scope':'saved arithmetic and PDF integrity, not semantic or model performance proof'}))
