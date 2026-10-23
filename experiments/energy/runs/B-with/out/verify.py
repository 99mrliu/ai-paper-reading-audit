"""Independent arithmetic and artifact checks; no scientific validation."""
from pathlib import Path
from decimal import Decimal as D
import hashlib,json
root=Path(__file__).resolve().parent
calc=json.loads((root/'calculations.json').read_text())
ev=json.loads((root/'evidence.json').read_text())
checks=[]
def check(name,actual,expected):
 checks.append({'check':name,'actual':str(actual),'expected':str(expected),'passed':actual==expected})
p1=D(200)*D('.25')+D(80)*D('.25')+D(240)*D('.5')
p2=D(100)*D('.5')+D(40)*D('.5')+D(160)*D('.25')
e1=p1*D('.5')/1000*D('1.2');e2=p2/1000*D('1.2')
check('allocated power segment 1 W',p1,D(190))
check('allocated power segment 2 W',p2,D(110))
check('facility total kWh',D(calc['groups']['allocated']['energy_kWh']['nominal']),e1+e2)
check('carbon total kg',D(calc['groups']['allocated']['carbon_kg']['nominal']),(e1*100+e2*500)/1000)
check('arithmetic mean intensity method g',(e1+e2)*300,D('73.8'))
check('arithmetic mean underestimate g',e1*100+e2*500-(e1+e2)*300,D('3.6'))
check('whole machine total kWh',D(calc['groups']['whole_machine']['energy_kWh']['nominal']),D('.672'))
check('whole machine total carbon kg',D(calc['groups']['whole_machine']['carbon_kg']['nominal']),D('.2112'))
check('ledger SHA256 binding',calc['ledger_sha256'],hashlib.sha256((root/'ledger.json').read_bytes()).hexdigest())
check('all ledger rows arithmetically ok',all(r['status']=='ok' for r in calc['records']),True)
for e in ev['evidence']:check(e['id']+' literal quote match only',e['literal_match'],True)
for f in ['report.md','claims.md','method_pages.txt']:check(f+' nonempty',(root/f).stat().st_size>0,True)
result={'scope':'Arithmetic, transcription and artifact checks only; no scientific meaning established by matching','audit_script_exit_code_observed':0,'checks':checks,'failed_checks':[x for x in checks if not x['passed']],'unresolved':['PDF states default PUE follows Strubell et al. but does not directly supply its numerical value; external source/code not supplied or accessed.','No real measurement logs or sensor calibration; true workload constancy, allocation validity and metering-domain independence unverified.','Exact cloud PUE and supply composition unknown; missing-sample recovery behavior not verified from source code.'],'quantum_policy':'No quantum assumed; point calculations are not uncertainty bounds.'}
(root/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'failed_checks':result['failed_checks'],'unresolved':len(result['unresolved'])},ensure_ascii=False))
