"""Capture an actual independent Codex CLI run, without inheriting task credentials."""
import argparse
import datetime
import json
import os
import subprocess
import time
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('directory')
ap.add_argument('--with-skill',action='store_true')
ap.add_argument('--timeout',type=int,default=900)
a=ap.parse_args()
r=Path(a.directory).resolve()
(r/'out').mkdir(exist_ok=True)
prompt='''You are executing one independent paper-reading task. You have no prior results from other sessions.
Read INPUT/task.md and the supplied INPUT materials. Only use files within this working directory, plus ordinary installed executables/libraries. Do not inspect parent directories, other sessions, credentials, global skills, or project history. No networking, publishing, submitting, or delegating. Do not alter INPUT files or the supplied skill. You may write temporary artifacts and your results within this directory.
Budget: at most 30 tool calls and 15 minutes. Work independently; do not ask the user questions. If material is insufficient, explain the limitation and stop or provide a bounded result. Save the requested Chinese report as out/report.md. Preserve failed checks and report any unresolved problems. Do not claim that literal evidence matching proves scientific meaning.
'''
if a.with_skill:
    prompt+='Use the supplied skill/SKILL.md and its referenced resources to carry out this task. Keep its verification and claims artifacts in out/ as well as the report.\n'
else:
    prompt+='Use your ordinary paper-reading approach with the available base tools.\n'
(r/'prompt.txt').write_text(prompt)
env=os.environ.copy()
for key,value in list(env.items()):
    try:
        key.encode('utf-8'); value.encode('utf-8')
    except UnicodeEncodeError:
        env.pop(key,None)
env['NO_PROXY']='*'
env['no_proxy']='*'
env['PATH']='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS'
for key in list(env):
    if any(x in key.upper() for x in ['PLAYGROUND_TOKEN','BOHR','MIRACLE','MINERU','LARK','GMAIL','VOUCH']):
        env.pop(key,None)
cmd=['codex','--no-daemon','exec','--ignore-user-config','--skip-git-repo-check','--ephemeral','--sandbox','danger-full-access','-c','approval_policy="never"','--json',
     '-C',str(r),'-o',str(r/'out/assistant_final.md'),'-']
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
with (r/'events.jsonl').open('w') as stdout,(r/'stderr.log').open('w') as stderr:
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=stdout,stderr=stderr,text=True,env=env)
    timed_out=False
    try: proc.communicate(prompt,timeout=a.timeout)
    except subprocess.TimeoutExpired:
        timed_out=True;proc.terminate()
        try:proc.wait(timeout=10)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
rows=[]
for line in (r/'events.jsonl').read_text().splitlines():
    try:rows.append(json.loads(line))
    except ValueError:pass
completed=[x for x in rows if x.get('type')=='turn.completed']
calls=[x for x in rows if x.get('type')=='item.started' and x.get('item',{}).get('type') in ['command_execution','mcp_tool_call','web_search']]
meta={'started_at':started,'duration_seconds':round(time.monotonic()-t,3),'exit_code':proc.returncode,
      'timed_out':timed_out,'tool_calls':len(calls),'tool_budget':30,'wall_time_budget_seconds':a.timeout,
      'usage':completed[-1].get('usage') if completed else None,'condition':'with_skill' if a.with_skill else 'without_skill',
      'model':'Codex CLI default; exact snapshot not exposed in event stream','harness':'Codex CLI',
      'independent_session':True,'human_steps':[],'report_exists':(r/'out/report.md').is_file()}
(r/'session.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'directory':r.name,**meta},ensure_ascii=False),flush=True)
