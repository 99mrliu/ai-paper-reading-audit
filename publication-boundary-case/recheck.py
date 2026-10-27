"""Offline author replay: original artifacts stay immutable; no model/network calls."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile

r=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args,cwd=None):
    return subprocess.run([sys.executable,*map(str,args)],cwd=cwd,capture_output=True,text=True,check=True,
                          env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
def json_replay(script,expected):
    assert json.loads(run(r/script).stdout)==json.loads((r/expected).read_text()),str(script)

manifest=json.loads((r/'file-manifest.json').read_text())
for name,digest in manifest['sha256'].items():
    assert sha(r/name)==digest,name
assert not any(p.is_symlink() for p in r.rglob('*'))
m=r/'matched'
for script,expected in [('A-verify_acl_energy.py','A-author-replay.stdout'),
                        ('B-verify_acl_energy.py','B-author-replay.stdout'),
                        ('B-acceptance.py','B-acceptance-author-replay.stdout')]:
    assert run(m/script).stdout==(m/expected).read_text(),script
json_replay('matched/author_verify.py','matched/author-verification.json')
json_replay('matched/probe_shared_power.py','matched/power-probe.json')
cfg=json.loads((m/'design-frozen.json').read_text())
for name,digest in cfg['sha256'].items(): assert sha(m/name)==digest
assert (m/'B-prompt.txt').read_text()==(m/'task.txt').read_text()+'\n'+(m/'workflow.txt').read_text()
meta=json.loads((m/'provenance.json').read_text())
for name,digest in meta['sha256'].items(): assert sha(m/name)==digest
review=json.loads((m/'author-review.json').read_text())
for arm in ['A','B']:
    assert [x['id'] for x in review[arm]]==list(cfg['evaluation_predefined'])
    for row in review[arm]: assert row['exact_quote'] in (m/(arm+'-final-ax.txt')).read_text()
t=r/'transfer';art=t/'actual-artifacts'
meta=json.loads((t/'provenance.json').read_text())
for name,digest in meta['hashes'].items(): assert sha(t/name)==digest
assert sha(t/'task.txt')==json.loads((t/'design-frozen.json').read_text())['input_sha256']
with tempfile.TemporaryDirectory() as tmp:
    tmp=Path(tmp)
    for ledger,result in [('ledger.json','calculations.json'),
                          ('ledger_quantum_1h.json','calculations_quantum_1h.json'),
                          ('ledger_quantum_reported_kwh.json','calculations_quantum_reported_kwh.json')]:
        out=tmp/result
        run(r/'skill/scripts/audit_energy.py',art/ledger,'--out',out)
        assert json.loads(out.read_text())==json.loads((art/result).read_text()),result
    for script,result in [('supplementary_checks.py','supplementary_checks.txt'),('repair_checks.py','repair_checks.json')]:
        assert json.loads(run(art/script,cwd=tmp).stdout)==json.loads((art/result).read_text()),script
json_replay('transfer/author_verify.py','transfer/author-results.json')
assert json.loads((art/'calculations.json').read_text())['records'][1]['status']=='unknown'
assert not json.loads((art/'calculations.json').read_text())['records'][0]['energy_check']['conditional_rounding_overlap']
assert json.loads((art/'calculations_quantum_1h.json').read_text())['records'][0]['energy_check']['conditional_rounding_overlap']
assert not json.loads((art/'calculations_quantum_reported_kwh.json').read_text())['records'][0]['energy_check']['conditional_rounding_overlap']
boundary=json.loads(run(r/'skill/tests/test_boundaries.py').stdout)
assert boundary['passed']==22
print(json.dumps({'status':'passed','new_actual_ledger_replays':3,'new_actual_AI_script_replays':2,
    'previous_actual_AI_script_replays':3,'author_Fraction_calculations':3,'boundary_tests':22,
    'hashes_checked':len(manifest['sha256']),'nominal_failure_and_TPU_unknown_retained':True,
    'scope':'file integrity and arithmetic only; not semantic verification, new model performance or new scientific experiment'},ensure_ascii=False))
