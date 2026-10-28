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
m=r/'matched'
for script,expected in [('A-verify_acl_energy.py','A-author-replay.stdout'),('B-verify_acl_energy.py','B-author-replay.stdout'),('B-acceptance.py','B-acceptance-author-replay.stdout')]:
 q=subprocess.run([sys.executable,str(m/script)],capture_output=True,text=True,check=True)
 assert q.stdout==(m/expected).read_text(),script
for script,expected in [('author_verify.py','author-verification.json'),('probe_shared_power.py','power-probe.json')]:
 q=subprocess.run([sys.executable,str(m/script)],capture_output=True,text=True,check=True)
 assert json.loads(q.stdout)==json.loads((m/expected).read_text()),script
cfg=json.loads((m/'design-frozen.json').read_text())
for name,digest in cfg['sha256'].items():assert hashlib.sha256((m/name).read_bytes()).hexdigest()==digest
assert (m/'B-prompt.txt').read_text()==(m/'task.txt').read_text()+'\n'+(m/'workflow.txt').read_text()
meta=json.loads((m/'provenance.json').read_text())
for name,digest in meta['sha256'].items():assert hashlib.sha256((m/name).read_bytes()).hexdigest()==digest
review=json.loads((m/'author-review.json').read_text())
for arm in ['A','B']:
 assert [row['id'] for row in review[arm]]==list(cfg['evaluation_predefined'])
 for row in review[arm]:assert row['exact_quote'] in (m/(arm+'-final-ax.txt')).read_text()
v=r/'version-check'
q=subprocess.run([sys.executable,str(v/'verify_versions.py')],capture_output=True,text=True,check=True)
assert json.loads(q.stdout)==json.loads((v/'author-version-results.json').read_text())
meta=json.loads((v/'practice-provenance.json').read_text())
for name,digest in meta['files'].items():assert hashlib.sha256((v/name).read_bytes()).hexdigest()==digest
for row in json.loads((v/'author-review.json').read_text())['not_adopted_or_qualified']:assert row['quote'] in (v/'answer-ax.txt').read_text()
subprocess.run([sys.executable,str(r/"closure/verify_delivery.py")],check=True,stdout=subprocess.DEVNULL)
print(json.dumps({'status':'passed','recomputed_json_artifacts':9,'boundary_tests':22,'actual_AI_script_author_replays':3,'author_fraction_models':2,'frozen_criteria_quote_integrity':True,'distinct_publication_factor_replay':True,'scope':'saved arithmetic and PDF integrity, not semantic or model performance proof'}))

