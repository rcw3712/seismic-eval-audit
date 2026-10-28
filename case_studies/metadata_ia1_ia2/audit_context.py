"""Check documented chronological controls and count adapter-local ETHZ IDs."""
from pathlib import Path
import csv
import datetime as dt
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'provenance/input_manifest.json').read_text())
controls = {}
synthetic = {}
for dataset, first, second in [('ethz', '2019-01-08', '2019-09-04'),
                                ('geofon', '2012-11-01', '2013-03-15')]:
    path = root / 'inputs' / (dataset + '.csv')
    entry = next(m for m in manifest if m['dataset'] == dataset)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']
    with path.open(newline='', encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(stream))
    boundaries = [dt.datetime.fromisoformat(x).replace(tzinfo=dt.timezone.utc)
                  for x in (first, second)]
    mismatches = 0
    by_split = {s: [] for s in ['train', 'dev', 'test']}
    for row in rows:
        t = dt.datetime.fromisoformat(row['source_origin_time'].replace('Z', '+00:00'))
        assert t.tzinfo is not None
        expected = 'train' if t < boundaries[0] else 'dev' if t < boundaries[1] else 'test'
        mismatches += expected != row['split']
        by_split[row['split']].append(row)
    assert mismatches == 0, (dataset, mismatches)
    controls[dataset] = {'records': len(rows), 'cutoffs_UTC': [first, second],
                         'label_mismatches': mismatches, 'status': 'PASS',
                         'interpretation': 'Positive control for documented adapter design, not a novel splitting result'}
    if dataset == 'ethz':
        synthetic = {'prefix': 'sb_id_', 'source_ids': len({r['source_id'] for r in rows if r['source_id'].startswith('sb_id_')}),
                     'records': sum(r['source_id'].startswith('sb_id_') for r in rows), 'by_split': {}}
        for split, subset in by_split.items():
            chosen = [r for r in subset if r['source_id'].startswith('sb_id_')]
            synthetic['by_split'][split] = {'source_ids': len({r['source_id'] for r in chosen}), 'records': len(chosen)}
        synthetic['interpretation'] = ('The adapter creates a local identifier once per event when the catalog resource suffix is /1. '
            'Repeated recordings remain grouped; this field alone does not preserve a resolvable catalog identifier.')
result = {'chronological_positive_controls': controls, 'ethz_adapter_local_ids': synthetic,
          'new_training_or_inference': False}
(root / 'provenance/context_verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
