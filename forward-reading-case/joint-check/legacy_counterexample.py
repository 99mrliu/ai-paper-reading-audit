"""Actual existing-tool output for a synthetic case; not a paper observation."""
from pathlib import Path
import importlib.util,json
r=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('legacy',r/'skill/scripts/audit_energy.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
record={'id':'separate_not_joint','source':'synthetic: same nonnegative duration, E=t kWh, C=t lb; duration displayed0 with quantum20 means coarse [0,10] envelope', 'power':{'value':'1','unit':'kW'},'power_scope':'aggregate','duration':{'value':'0','unit':'h','quantum':'20'},'measurement_scope':'facility','intensity':{'value':'1','unit':'lb/kWh'},'reported_energy':{'value':'2','unit':'kWh','quantum':'1'},'reported_carbon':{'value':'8','unit':'lb','quantum':'1'}}
row=m.run({'records':[record]})['records'][0]
assert row['energy_check']['conditional_rounding_overlap'] and row['carbon_check']['conditional_rounding_overlap']
print(json.dumps({'input':record,'actual_existing_tool_output':row,'interpretation':'two independent necessary checks pass; no common t can belong to both [1.5,2.5) and [7.5,8.5). Existing tool never claims joint feasibility; do not infer it.'},ensure_ascii=False,indent=2))
