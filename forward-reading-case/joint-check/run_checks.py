from pathlib import Path
import importlib.util,json,sys
r=Path(__file__).resolve().parent
p=r/'skill/scripts/joint_bounds.py';s=importlib.util.spec_from_file_location('joint',p);j=importlib.util.module_from_spec(s);s.loader.exec_module(j)
def c(i,rate,y,q):return {'id':i,'rate':str(rate),'display':str(y),'quantum':str(q)}
bert=[c('energy_kWh','19.0255858',1507,1),c('carbon_lb','18.1504088532',1438,1),c('displayed_hours',1,79,1)]
tests=[]
for t,expect in [('79',False),('79.2',True),('79.21',True),('79.24',False)]:tests.append({'id':'BERT_'+t,'input':{'rounding':'half_up','constraints':bert,'fixed_parameter':t},'expect_joint':True,'expect_fixed':expect})
tests += [
 {'id':'separate_pass_joint_fail','input':{'rounding':'half_up','constraints':[c('energy',1,2,1),c('carbon',1,8,1),c('broad_hours',1,0,20)]},'expect_joint':False},
 {'id':'open_touch_is_empty','input':{'rounding':'half_up','constraints':[c('a',1,2,1),c('b',3,8,1)]},'expect_joint':False},
 {'id':'even_closed_touch_has_one_witness','input':{'rounding':'half_even','constraints':[c('a',1,2,1),c('b',3,8,1)]},'expect_joint':True},
 {'id':'half_even_exact_tie','input':{'rounding':'half_even','constraints':[c('a',1,2,1)],'fixed_parameter':'2.5'},'expect_joint':True,'expect_fixed':True},
 {'id':'half_up_exact_tie','input':{'rounding':'half_up','constraints':[c('a',1,2,1)],'fixed_parameter':'2.5'},'expect_joint':True,'expect_fixed':False},
 {'id':'zero_display','input':{'rounding':'half_even','constraints':[c('a',1,0,1)],'fixed_parameter':'0'},'expect_joint':True,'expect_fixed':True},
 {'id':'unsupported_zero_rate','input':{'rounding':'half_up','constraints':[c('a',0,1,1)]},'expect_error':True},
 {'id':'invalid_display_quantum','input':{'rounding':'half_up','constraints':[c('a',1,'2.1',1)]},'expect_error':True},
]
results=[]
for t in tests:
 try:
  out=j.solve(t['input']);passed=not t.get('expect_error') and out['joint_feasible']==t['expect_joint']
  if 'expect_fixed' in t:passed &= out['fixed_parameter_feasible']==t['expect_fixed']
 except (ValueError,ArithmeticError) as e:out={'error':str(e)};passed=t.get('expect_error',False)
 results.append({'id':t['id'],'passed':bool(passed),'input':t['input'],'expected':{k:v for k,v in t.items() if k.startswith('expect_')},'actual':out})
result={'tests':len(results),'passed':sum(x['passed'] for x in results),'results':results}
print(json.dumps(result,ensure_ascii=False,separators=(',',':')))
sys.exit(0 if all(x['passed'] for x in results) else 1)
