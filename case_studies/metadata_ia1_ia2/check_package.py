"""Verify delivered files without installing third-party dependencies."""
from pathlib import Path
import csv
import hashlib

root = Path(__file__).resolve().parent
with (root / 'MANIFEST_SHA256.csv').open(newline='', encoding='utf-8') as stream:
    rows = list(csv.DictReader(stream))
failures = []
for row in rows:
    path = (root / row['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failures.append(row['path'] + ': missing or invalid path')
        continue
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    if str(path.stat().st_size) != row['bytes'] or digest.hexdigest() != row['sha256']:
        failures.append(row['path'] + ': size/hash mismatch')
if failures:
    raise SystemExit('\n'.join(failures))
print(f'PASS: {len(rows)} delivered file hashes match')
