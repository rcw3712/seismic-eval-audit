"""Exercise documented use of the unchanged v0.1.3 wheel outside the checkout.

This is an author-run usage demonstration, not independent adoption evidence.
No model, waveform, training or inference is involved.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--installed', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--metadata', type=Path, help='Optional checksum-verified ETHZ CSV')
    a = p.parse_args()
    installed = a.installed.resolve()
    if not (installed / 'seismic_eval_audit').is_dir():
        p.error('Install the provided wheel into --installed first')
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(installed))
    import seismic_eval_audit as api
    assert installed in Path(api.__file__).resolve().parents
    env = os.environ.copy()
    env['PYTHONPATH'] = str(installed)
    env['PYTHONUTF8'] = '1'
    receipt = {'scope': 'Author-run installed-wheel usage demonstration',
               'python': platform.python_version(), 'os': platform.system(),
               'imported_from_install_target': True, 'training': False,
               'inference': False, 'synthetic_cli': {}, 'synthetic_api': {}}

    def csv_file(name, rows):
        path = out / name
        with path.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        return path

    def cli(name, path, code, status=None, strict=False):
        args = [sys.executable, '-m', 'seismic_eval_audit', str(path),
                '--record', 'trace_name', '--output', str(out / name)]
        if strict:
            args.append('--strict')
        r = subprocess.run(args, cwd=out, env=env, capture_output=True,
                           text=True, encoding='utf-8', timeout=120)
        (out / (name + '.stdout.txt')).write_text(r.stdout, encoding='utf-8')
        (out / (name + '.stderr.txt')).write_text(r.stderr, encoding='utf-8')
        assert r.returncode == code, (name, r.returncode, r.stderr)
        data = None
        if status:
            data = json.loads((out / name / 'report.json').read_text(encoding='utf-8'))
            assert data['status'] == status, (name, data)
        return {'exit': r.returncode, 'status': status or 'INPUT_ERROR'}, data

    rows = [dict(trace_name='001', source_id='event-A', split='train'),
            dict(trace_name='002', source_id='event-B', split='dev'),
            dict(trace_name='003', source_id='event-C', split='test')]
    valid = csv_file('synthetic_valid.csv', rows)
    receipt['synthetic_cli']['valid'], _ = cli('valid', valid, 0, 'PASS')
    overlap = csv_file('synthetic_overlap.csv', [dict(r, source_id='event-A') for r in rows])
    receipt['synthetic_cli']['overlap'], result = cli('overlap', overlap, 1, 'FAIL')
    assert result['shared_sources'] == 1 and result['affected_records'] == 3
    single = csv_file('synthetic_single.csv', rows[:1])
    receipt['synthetic_cli']['warning'], _ = cli('warning', single, 0, 'WARNING')
    receipt['synthetic_cli']['warning_strict'], _ = cli('warning_strict', single, 1, 'WARNING', True)
    invalid = csv_file('synthetic_invalid.csv', [dict(rows[0], source_id='')])
    receipt['synthetic_cli']['invalid'], _ = cli('invalid', invalid, 2)

    parent = [dict(record_id='p', source_id='A', split='train')]
    child = [dict(record_id='c', parent_id='p', source_id='A', split='train')]
    held = [dict(record_id='h', source_id='B')]
    inner = [dict(record_id='v', source_id='C')]
    current = [dict(record_id='t1', source_id='A', split='test'),
               dict(record_id='t2', source_id='D', split='test')]
    checks = {'lineage': api.check_lineage(parent, child),
              'oof': api.check_oof(held, parent, inner),
              'schema': api.check_schema(['Z', 'N', 'E'], ['Z', 'N', 'E']),
              'history': api.audit_history(current, [dict(source_id='A', role='train')])}
    artifact = out / 'synthetic_artifact.txt'; artifact.write_bytes(b'example\n')
    checks['artifact'] = api.check_artifacts(out, [dict(path=artifact.name,
                                            sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())])
    for name, data in checks.items():
        assert data['status'] == ('WARNING' if name == 'history' else 'PASS')
        (out / (name + '.json')).write_text(json.dumps(data, indent=2), encoding='utf-8')
        receipt['synthetic_api'][name] = data['status']
    assert checks['history']['categories']['prior_development']['sources'] == 1
    assert checks['history']['categories']['unknown']['sources'] == 1

    if a.metadata:
        path = a.metadata.resolve()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == '542d2e9cfc35847668521fe335bc955b00a42f59f06eaa921ffb92f6009a1dee', 'ETHZ input differs'
        _, source = cli('ethz_source', path, 0, 'PASS')
        raw = api.read_csv(path)
        stations = [dict(record_id=r['trace_name'],
                         station_key=r['station_network_code']+'.'+r['station_code'],
                         split=r['split']) for r in raw]
        station = api.audit_split(stations, group='station_key')
        api.write_report(station, out / 'ethz_station')
        pair = next(x for x in station['pairs'] if {x['a'], x['b']} == {'train', 'test'})
        test_records = pair['a_records'] if pair['a'] == 'test' else pair['b_records']
        # Independent direct set calculations, not a second call to the audit API.
        source_sets = {k: {r['source_id'] for r in raw if r['split'] == k} for k in ('train', 'dev', 'test')}
        station_sets = {k: {r['station_network_code']+'.'+r['station_code'] for r in raw if r['split'] == k} for k in ('train', 'test')}
        assert all(not source_sets[k] & source_sets[j] for k, j in [('train','dev'),('train','test'),('dev','test')])
        assert len(station_sets['train'] & station_sets['test']) == pair['shared_sources'] == 180
        assert (source['records'], source['sources'], source['shared_sources']) == (36743, 2231, 0)
        assert station['status'] == 'FAIL' and station['shared_sources'] == 190 and test_records == 9637
        receipt['ethz'] = {'input_sha256': digest, 'records': 36743, 'source_ids': 2231,
                           'source_status': 'PASS', 'station_status': 'FAIL',
                           'station_keys_shared_any_subsets': 190,
                           'station_keys_shared_train_test': 180,
                           'test_records_on_train_station_keys': test_records,
                           'direct_set_crosscheck': 'PASS'}

    receipt['status'] = 'PASS'
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    (out / 'SUMMARY.md').write_text(
        '# Usage verification\n\nAuthor-run installed-wheel demonstration; no independent adoption claim.\n\n'
        'Valid membership: PASS / exit 0. Injected source overlap: FAIL / exit 1.\n'
        'One subset: WARNING / exit 0; with --strict: exit 1. Missing source: input error / exit 2.\n\n'
        'Additional API examples are synthetic; they are not evidence of real augmentation or model execution.\n\n'
        + ('ETHZ supplied source membership passes. The same split fails a separately declared unseen-station contract (180 train-test keys). This does not invalidate its source-disjoint purpose.\n' if a.metadata else 'ETHZ was not run in this offline smoke check.\n')
        + '\nPASS never certifies physical source identity or historical independence.\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
