"""Run the preregistered tasks in new, independent Codex CLI sessions.
Requires an authenticated Codex CLI plus pdftotext (or pypdf).
Never writes into the original runs; destination must not already exist.
"""
import argparse,concurrent.futures,json,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--destination',required=True);p.add_argument('--jobs',type=int,default=2);p.add_argument('--runs',nargs='*');a=p.parse_args()
r=Path(__file__).resolve().parent;dest=Path(a.destination).resolve()
if dest.exists():raise SystemExit('Destination already exists; choose a fresh directory')
dest.mkdir(parents=True)
all_runs=json.loads((r/'cases/preregistration.json').read_text())['formal_runs']
selected=a.runs or all_runs
if any(x not in all_runs for x in selected):raise SystemExit('Unregistered run ID')
materials={'A':'random_search.pdf','B':'scikit_learn.pdf','C':'invalid_input.pdf'}
def one(name):
 case=name[0];d=dest/name;(d/'INPUT').mkdir(parents=True)
 shutil.copy2(r/'cases'/case/'task.md',d/'INPUT/task.md');shutil.copy2(r/'materials'/materials[case],d/'INPUT/paper.pdf')
 use=name.endswith('-with')
 if use:shutil.copytree(r/'skill',d/'skill',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 cmd=[sys.executable,str(r/'run_session.py'),str(d)]
 if use:cmd+=['--with-skill']
 p=subprocess.run(cmd,capture_output=True,text=True)
 print(p.stdout.strip() or p.stderr.strip(),flush=True)
 return {'id':name,'harness_exit':p.returncode,'session':json.loads((d/'session.json').read_text()) if (d/'session.json').exists() else None}
with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(3,a.jobs))) as ex:
 result=list(ex.map(one,selected))
(dest/'batch.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
