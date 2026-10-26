from pathlib import Path
import subprocess,json,sys,tempfile,hashlib
r=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,str(r/'run_checks.py')],capture_output=True,text=True,check=True)
raw=p.stdout;d=json.loads(raw);saved=json.loads((r/'results.json').read_text());assert hashlib.sha256(raw.encode()).hexdigest()==saved['full_output_sha256']
for x,y in zip(d['results'],saved['results']):
 x['actual']={k:v for k,v in x['actual'].items() if k in ['error','joint','joint_feasible','witness_parameter','fixed_parameter_feasible']};assert x==y
assert d['tests']==saved['tests']==d['passed']==12
p=subprocess.run([sys.executable,str(r/'legacy_counterexample.py')],capture_output=True,text=True,check=True);assert json.loads(p.stdout)==json.loads((r/'legacy-output.json').read_text())
manifest=json.loads((r/'reading/provenance.json').read_text());assert hashlib.sha256((r/'skill/scripts/joint_bounds.py').read_bytes()).hexdigest()==manifest['frozen_helper_sha256']
count=0
with tempfile.TemporaryDirectory() as tmp:
 for inp in sorted((r/'reading/out').glob('*.input.json')):
  output=Path(tmp)/'result.json'
  subprocess.run([sys.executable,str(r/'skill/scripts/joint_bounds.py'),str(inp),'--out',str(output)],capture_output=True,check=True)
  assert json.loads(output.read_text())==json.loads(inp.with_name(inp.name.replace('.input.json','.result.json')).read_text());count+=1
assert count==11
print(json.dumps({'status':'passed','development_cases':12,'new_reading_saved_calls_recomputed':count,'original_independent_checks_retained':True,'scope':'conditional arithmetic, not source semantics or measured validity'}))
