from pathlib import Path
import argparse,shutil
p=argparse.ArgumentParser();p.add_argument('--destination',required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;d=Path(a.destination).resolve();d.mkdir(parents=True,exist_ok=False)
(d/'INPUT').mkdir();(d/'out').mkdir()
shutil.copy2(r/'paper/acl-energy.pdf',d/'INPUT/paper.pdf')
shutil.copy2(r/'evidence/task.md',d/'INPUT/task.md')
shutil.copytree(r/'skill',d/'skill',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copy2(r/'evidence/prompt.txt',d/'prompt.txt')
print('Prepared the original full PDF, task, frozen Skill and actual prompt; no old answer or new model run.')
