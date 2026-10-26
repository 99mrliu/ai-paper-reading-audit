from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parent;rows=[];images=[];pdfs=[]
for p in sorted(r.rglob('*')):
 if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts or p.suffix=='.pyc':continue
 raw=p.read_bytes();name=str(p.relative_to(r))
 if raw.startswith(b'\x89PNG\r\n\x1a\n') or raw.startswith(b'\xff\xd8\xff'):images.append(name);continue
 if raw.startswith(b'%PDF'):
  assert len(raw)<=10*1024**2
  sizes={}
  for mode in ('-layout','-raw'):
   q=subprocess.run(['pdftotext',mode,str(p),'-'],capture_output=True,check=True)
   text=q.stdout.decode('utf-8');sizes[mode]=len(text.encode('utf-8'))
  n=max(sizes.values());pdfs.append({'path':name,'extractions':sizes,'counted_bytes':n});rows.append({'path':name,'text_bytes':n});continue
 if p.suffix.lower()=='.ipynb':raise SystemExit('Notebook requires explicit conversion')
 raw.decode('utf-8');assert b'\x00' not in raw and len(raw)<=2*1024**2
 rows.append({'path':name,'text_bytes':len(raw)})
total=sum(x['text_bytes'] for x in rows);reserve=8192*len(pdfs);budget=total+reserve
print(json.dumps({'status':'passed' if budget<=245760 else 'over_limit','measured_text_bytes':total,
 'PDF_conversion_reserve_bytes':reserve,'conservative_budget_bytes':budget,'budget_KiB':round(budget/1024,3),
 'below_recommended_200_KiB':budget<=204800,'hard_limit':245760,'PDFs':pdfs,'images':images,'files':rows},ensure_ascii=False,indent=2))
sys.exit(0 if budget<=245760 else 1)
