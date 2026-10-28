"""Local Decimal energy/carbon ledger. No PDF parser, networking, or semantic judge."""
import argparse
import hashlib
import json
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path

getcontext().prec = 36
D = Decimal
UNITS = {
    'power': {'W': D('.001'), 'kW': D(1), 'MW': D(1000)},
    'duration': {'s': D(1), 'min': D(60), 'h': D(3600), 'day': D(86400)},
    'energy': {'Wh': D('.001'), 'kWh': D(1), 'MWh': D(1000)},
    'carbon': {'g': D('.001'), 'kg': D(1), 'lb': D('.45359237')},
    'intensity': {'g/kWh': D('.001'), 'kg/kWh': D(1), 'lb/kWh': D('.45359237')},
    'factor': {'': D(1)},
}


class Missing(ValueError):
    pass


def number(x):
    if x is None:
        raise Missing('Missing numerical value')
    if isinstance(x, bool):
        raise ValueError('Boolean is not a number')
    try:
        n = D(str(x))
    except (InvalidOperation, ValueError):
        raise ValueError('Invalid decimal: ' + str(x))
    if not n.is_finite() or n < 0:
        raise ValueError('Value must be finite and nonnegative')
    return n


def quantity(x, kind):
    if x is None:
        raise Missing('Missing ' + kind)
    if not isinstance(x, dict):
        raise ValueError(kind + ' must be an object')
    unit = x.get('unit', '' if kind == 'factor' else None)
    if unit is None:
        raise Missing('Missing unit for ' + kind)
    if unit not in UNITS[kind]:
        raise ValueError('Unsupported ' + kind + ' unit: ' + str(unit))
    n = number(x.get('value'))
    q = D(0)
    if 'quantum' in x:
        q = number(x['quantum'])
        if q <= 0:
            raise ValueError('quantum must be positive')
    f = UNITS[kind][unit]
    values = n*f, max(D(0), n-q/2)*f, (n+q/2)*f
    return tuple(v/D(3600) for v in values) if kind == 'duration' else values


def multiply(*xs):
    result = (D(1),)*3
    for x in xs:
        result = tuple(a*b for a, b in zip(result, x))
    return result


def plus(xs):
    return tuple(sum((x[i] for x in xs), D(0)) for i in range(3))


def packed(x):
    return {'nominal': str(x[0]), 'conditional_interval': [str(x[1]), str(x[2])]}


def compare(calculated, reported):
    return {'reported': packed(reported), 'nominal_residual': str(calculated[0]-reported[0]),
            'conditional_rounding_overlap': calculated[1] <= reported[2] and reported[1] <= calculated[2]}


def power(component):
    if not isinstance(component, dict):
        raise ValueError('Each component must be an object')
    p = quantity(component.get('power'), 'power')
    scope = component.get('power_scope')
    if scope is None:
        raise Missing('Missing power_scope: aggregate or per_device')
    if scope not in ('aggregate', 'per_device'):
        raise ValueError('Unsupported power_scope')
    if scope == 'aggregate' and 'devices' in component:
        raise ValueError('Remove devices for aggregate power to avoid double counting')
    devices = D(1)
    if scope == 'per_device':
        devices = number(component.get('devices'))
        if devices < 1 or devices != devices.to_integral_value():
            raise ValueError('devices must be an integer >= 1')
    allocation = number(component.get('allocation', 1))
    if allocation > 1:
        raise ValueError('allocation must be between 0 and 1')
    return multiply(p, (devices,)*3, (allocation,)*3)


def audit(record):
    out = {'id': record['id'], 'source': record['source'], 'status': 'ok', 'energy_kWh': None, 'carbon_kg': None}
    if 'group' in record:
        if not isinstance(record['group'], str) or not record['group'].strip():
            raise ValueError('group must be a nonempty string')
        out['group'] = record['group']
    try:
        if 'energy' in record:
            if any(k in record for k in ('power', 'components', 'duration')):
                raise ValueError('Use either energy or power/components plus duration')
            energy = quantity(record['energy'], 'energy')
        else:
            if 'components' in record:
                if 'power' in record:
                    raise ValueError('Use either power or components')
                components = record['components']
                if not isinstance(components, list) or not components:
                    raise ValueError('components must be a nonempty list')
                p = plus([power(c) for c in components])
            else:
                p = power(record)
            energy = multiply(p, quantity(record.get('duration'), 'duration'))
        scope = record.get('measurement_scope')
        if scope is None:
            raise Missing('Missing measurement_scope: it or facility')
        if scope == 'it':
            pue = quantity(record.get('pue'), 'factor')
            if pue[0] < 1 or pue[1] < 1:
                raise ValueError('PUE and its conditional interval must be >= 1')
            energy = multiply(energy, pue)
        elif scope == 'facility':
            if 'pue' in record and quantity(record['pue'], 'factor') != (D(1),)*3:
                raise ValueError('Facility energy already includes overhead; do not multiply PUE again')
        else:
            raise ValueError('Unsupported measurement_scope')
        out['energy_kWh'] = packed(energy)
        if 'reported_energy' in record:
            out['energy_check'] = compare(energy, quantity(record['reported_energy'], 'energy'))
        try:
            carbon = multiply(energy, quantity(record.get('intensity'), 'intensity'))
        except Missing as e:
            out['status'] = 'partial'
            out['carbon_status'] = 'unknown'
            out['reason'] = str(e)
            return out
        out['carbon_kg'] = packed(carbon)
        if 'reported_carbon' in record:
            out['carbon_check'] = compare(carbon, quantity(record['reported_carbon'], 'carbon'))
    except Missing as e:
        out['status'] = 'unknown'
        out['reason'] = str(e)
    except (ValueError, TypeError, KeyError) as e:
        out['status'] = 'invalid'
        out['reason'] = str(e)
    return out


def run(data):
    if not isinstance(data, dict) or not isinstance(data.get('records'), list) or not data['records']:
        raise ValueError('records must be a nonempty list')
    seen = set()
    for record in data['records']:
        if not isinstance(record, dict) or not isinstance(record.get('id'), str) or not record['id'].strip():
            raise ValueError('Every record requires a nonempty string id')
        if record['id'] in seen:
            raise ValueError('Duplicate id: ' + record['id'])
        seen.add(record['id'])
        if not isinstance(record.get('source'), str) or not record['source'].strip():
            raise ValueError('Every record requires a source description')
    rows = []
    for record in data['records']:
        try:
            rows.append(audit(record))
        except (ValueError, TypeError, KeyError) as e:
            rows.append({'id': record['id'], 'source': record['source'], 'status': 'invalid', 'reason': str(e)})
    groups = {}
    for name in sorted({r['group'] for r in rows if 'group' in r}):
        members = [r for r in rows if r.get('group') == name]
        group = {'members': [r['id'] for r in members]}
        for key in ('energy_kWh', 'carbon_kg'):
            values = [r.get(key) for r in members]
            if any(v is None or r['status'] == 'invalid' for r, v in zip(members, values)):
                group[key] = None
            else:
                xs = [(D(v['nominal']), D(v['conditional_interval'][0]), D(v['conditional_interval'][1])) for v in values]
                group[key] = packed(plus(xs))
        groups[name] = group
    return {'schema_version': 1, 'scope': 'Arithmetic for user-entered ledger; not source or scientific validation',
            'interval_meaning': 'Conditional display-rounding bounds, not measured uncertainty or confidence intervals',
            'records': rows, 'groups': groups}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        raw = Path(args.ledger).read_bytes()
        data = json.loads(raw)
        result = run(data)
        result['ledger_sha256'] = hashlib.sha256(raw).hexdigest()
        code = 2 if any(r['status'] == 'invalid' for r in result['records']) else 0
    except (ValueError, OSError, TypeError, KeyError) as e:
        result = {'status': 'invalid', 'reason': str(e)}
        code = 2
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'out': args.out, 'exit_code': code, 'records': len(result.get('records', []))}))
    raise SystemExit(code)


if __name__ == '__main__':
    main()
