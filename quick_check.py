"""Offline arithmetic and provenance checks; does not call AI or modify evidence."""
from pathlib import Path
from decimal import Decimal
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    saved = json.loads((ROOT / 'verification/results.json').read_text())
    pairs = {}
    count = 0
    for experiment in ['transfer', 'energy']:
        rows = {}
        for path in sorted((ROOT / 'experiments' / experiment / 'runs').glob('*/session.json')):
            record = json.loads(path.read_text())
            rid = path.parent.name
            assert sha(path) == saved[experiment]['runs'][rid]['session_sha256'], path
            assert record['duration_seconds'] == saved[experiment]['runs'][rid]['seconds'], path
            assert record['usage'] == saved[experiment]['runs'][rid]['usage'], path
            rows[rid] = record
        assert len(rows) == 7
        count += len(rows)
        with_mean = sum(rows[r + '-with']['duration_seconds'] for r in ['A1', 'A2']) / 2
        without_mean = sum(rows[r + '-without']['duration_seconds'] for r in ['A1', 'A2']) / 2
        increase = (with_mean / without_mean - 1) * 100
        assert abs(increase - saved[experiment]['relative_increase_percent']) < 1e-10
        pairs[experiment] = {'with_mean_seconds': with_mean, 'without_mean_seconds': without_mean,
                             'relative_increase_percent': increase}
    base = ROOT / 'experiments/energy'
    ledger_path = base / 'runs/A1-with/out/ledger.json'
    expected = json.loads((base / 'runs/A1-with/out/calculations.json').read_text())
    spec = importlib.util.spec_from_file_location('preserved_energy_audit', base / 'skill/scripts/audit_energy.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    recalculated = module.run(json.loads(ledger_path.read_text()))
    recalculated['ledger_sha256'] = sha(ledger_path)
    assert recalculated == expected, 'Recalculation differs from preserved original output'
    by_id = {r['id']: r for r in recalculated['records']}
    bert_printed = Decimal(by_id['BERTbase_GPU']['energy_kWh']['nominal'])
    bert_context = Decimal(by_id['BERT_79_2_sensitivity']['energy_kWh']['nominal'])
    assert bert_printed == Decimal('1503.0212782')
    assert bert_context == Decimal('1506.82639536')
    result = {'status': 'passed', 'original_sessions_verified': count, 'paired_comparisons': pairs,
              'energy_ledger_records_recomputed': len(recalculated['records']),
              'bert_79h_kWh': str(bert_printed), 'bert_79_2h_kWh': str(bert_context),
              'bert_79h_lb': str(bert_printed * Decimal('.954')),
              'bert_79_2h_lb': str(bert_context * Decimal('.954')),
              'scope': 'Offline consistency of preserved records and arithmetic, not new AI runs, source semantics or physical measurements.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
