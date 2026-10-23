"""Engineering invariants, not evidence of paper-reading quality."""
import importlib.util
import json
from copy import deepcopy
from decimal import Decimal as D
from pathlib import Path

r = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('energy', r/'skill/scripts/audit_energy.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
checks = []


def check(name, condition):
    assert condition, name
    checks.append(name)


def one(**overrides):
    row = {'id': 'x', 'source': 'Synthetic engineering fixture, not a paper result',
           'power': {'value': '2', 'unit': 'kW'}, 'power_scope': 'aggregate',
           'duration': {'value': '30', 'unit': 'min'}, 'measurement_scope': 'it',
           'pue': {'value': '1.2'}, 'intensity': {'value': '200', 'unit': 'g/kWh'}}
    row.update(overrides)
    return row


base = one()
a = m.run({'records': [base]})['records'][0]
check('Power times duration, PUE once, grams to kilograms', D(a['energy_kWh']['nominal']) == D('1.2') and D(a['carbon_kg']['nominal']) == D('.24'))
b = one(power={'value': '2000', 'unit': 'W'}, duration={'value': '1800', 'unit': 's'})
converted = m.run({'records': [b]})['records'][0]['carbon_kg']
check('Equivalent physical units yield equal output', D(converted['nominal']) == D(a['carbon_kg']['nominal']) and list(map(D, converted['conditional_interval'])) == list(map(D, a['carbon_kg']['conditional_interval'])))
b = one(power_scope='per_device', devices=4)
check('Per-device count applies once', D(m.audit(b)['energy_kWh']['nominal']) == D('4.8'))
check('Aggregate plus device count rejects double counting', m.audit(one(devices=4))['status'] == 'invalid')
check('Facility plus PUE rejects double counting', m.audit(one(measurement_scope='facility'))['status'] == 'invalid')
b = one(energy={'value': '1', 'unit': 'kWh'})
check('Energy plus power rejects ambiguous duplicate inputs', m.audit(b)['status'] == 'invalid')
b = {'id': 'x', 'source': 'fixture', 'energy': {'value': '1', 'unit': 'kWh'}, 'measurement_scope': 'facility', 'intensity': {'value': '1', 'unit': 'lb/kWh'}}
check('Pounds conversion is exact', D(m.audit(b)['carbon_kg']['nominal']) == D('.45359237'))
check('Unsupported unit is not guessed', m.audit(one(power={'value': '2', 'unit': 'MWatts'}))['status'] == 'invalid')
check('Missing unit remains unknown', m.audit(one(power={'value': '180'}))['status'] == 'unknown')
check('Missing power not zero', m.audit(one(power=None))['energy_kWh'] is None)
check('Missing intensity preserves energy but not carbon', m.audit(one(intensity=None))['status'] == 'partial' and m.audit(one(intensity=None))['carbon_kg'] is None)
check('Nonfinite rejected', m.audit(one(power={'value': 'NaN', 'unit': 'W'}))['status'] == 'invalid')
b = one(power={'value': '12041.51', 'unit': 'W'}, duration={'value': '79', 'unit': 'h', 'quantum': '1'}, pue={'value': '1.58'}, reported_energy={'value': '1507', 'unit': 'kWh', 'quantum': '1'})
result = m.audit(b)
check('Rounded displayed duration can reconcile a nominal mismatch', result['energy_check']['conditional_rounding_overlap'] and abs(D(result['energy_check']['nominal_residual'])) > D(3))
b['duration'].pop('quantum')
check('No hidden precision assumption', not m.audit(b)['energy_check']['conditional_rounding_overlap'])
rows = [one(id='a', group='experiment'), one(id='b', group='experiment', intensity=None)]
g = m.run({'records': rows})['groups']['experiment']
check('Missing carbon invalidates complete group carbon total', g['carbon_kg'] is None and D(g['energy_kWh']['nominal']) == D('2.4'))
rows[1]['power'] = None
check('Missing energy invalidates complete group energy total', m.run({'records': rows})['groups']['experiment']['energy_kWh'] is None)
b = one(); b.pop('power'); b.pop('power_scope'); b['components'] = [dict(power={'value': '200', 'unit': 'W'}, power_scope='aggregate', allocation='.25'), dict(power={'value': '80', 'unit': 'W'}, power_scope='aggregate', allocation='.25'), dict(power={'value': '240', 'unit': 'W'}, power_scope='aggregate', allocation='.5')]
check('Resource-specific allocations', D(m.audit(b)['energy_kWh']['nominal']) == D('.114'))
try:
    m.run({'records': [base, deepcopy(base)]})
except ValueError:
    duplicate_rejected = True
else:
    duplicate_rejected = False
check('Duplicate identities rejected', duplicate_rejected)
(r/'development/engineering-checks.json').write_text(json.dumps({'kind': 'Engineering invariants only, not reading accuracy', 'passed': len(checks), 'checks': checks}, indent=2)+'\n')
print(json.dumps({'passed': len(checks), 'checks': checks}))
