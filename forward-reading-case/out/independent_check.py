from decimal import Decimal as D, getcontext
import json
from pathlib import Path
getcontext().prec=36
p=D('12041.51')/1000*D('1.58');i=D('.954')
lo=max(D('1506.5')/p,D('1437.5')/(p*i));hi=min(D('1507.5')/p,D('1438.5')/(p*i))
results={'assumptions':'Fixed power12041.51W, PUE1.58, factor0.954lb/kWh; reported energy/carbon independently rounded to nearest1; interval endpoints depend on tie rule','bert_hours_simultaneously_compatible':[str(lo),str(hi)],'bert_point_calculations':{t:{'energy_kWh':str(p*D(t)),'carbon_lb':str(p*D(t)*i)} for t in ['79','79.2','79.21']},'nominal_other':{name:{'energy_kWh':str(D(w)/1000*D(t)*D('1.58')),'carbon_lb':str(D(w)/1000*D(t)*D('1.58')*i)} for name,w,t in [('t2tbig','1515.43','84'),('nas','1515.43','274120')]},'paper_factor_applied_to_201_lb':str(D(201)*i),'boundary_tests':json.loads(Path('out/boundary-tests.json').read_text())['passed']}
Path('out/independent-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
