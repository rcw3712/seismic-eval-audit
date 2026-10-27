# Audit a saved SeisBench metadata table

Use this workflow to check an existing evaluation partition before interpreting predictions. It consumes saved identifiers and memberships; it does not train a model, infer earthquake identity, or certify an independent test set. The commands use the unchanged v0.1.3 package. This guide and its verification script were added after the DOI archive; they are identified by the current Git commit and CHECKSUMS.csv, not by the archived document bytes.

## 1 Choose the contract and inspect the input

For source exclusion, each supplied `source_id` must occur in only one split. Native SeisBench-shaped input can be passed directly with `--record trace_name`; manual column renaming is unnecessary. Required values are nonempty strings. `dev`, `val`, `Train` and `train` remain distinct strings. Resolve scientific identity questions before interpreting a successful check.

For an unseen-station question, use a separate network.station key. A failure of that requirement does not invalidate a source-disjoint experiment. Neither contract establishes independence from earlier development decisions.

## 2 Install the archived wheel and obtain metadata

From a checkout containing the supplied wheel, install it into a Python 3.10+ environment:

```text
python -m pip install --no-deps dist/seismic_eval_audit-0.1.3-py3-none-any.whl
python fetch_ethz.py --output ETHZ_METADATA.csv
```

The downloader rejects bytes differing from SHA-256 `542d2e9cfc35847668521fe335bc955b00a42f59f06eaa921ffb92f6009a1dee`. If it fails, inspect the cause. Do not remove the checksum check to obtain the published counts. The cached, hash-identical CSV can also be used; no waveform files are required. Use fresh output paths for every command.

## 3 Audit the supplied source partition

```text
python -m seismic_eval_audit ETHZ_METADATA.csv --record trace_name --group source_id --split split --strict --output SOURCE_REPORT
```

Expected exit: 0. The recorded input produces:

```json
{"status":"PASS","group_column":"source_id","records":36743,"sources":2231,"shared_sources":0,"affected_records":0}
```

This is an excerpt, not the whole JSON. `SOURCE_REPORT` contains `report.json`, `report.md` and `violations.csv`. Read the declared group and the pairwise counts in the JSON. PASS means supplied source IDs do not span subsets. It does not validate the underlying catalogue or earlier data use.

## 4 Ask a separate station-exclusion question

Save the following as `station_audit.py`, then run `python station_audit.py` in the directory containing the metadata. This is an API check; the source CLI does not run it automatically.

```python
from seismic_eval_audit import read_csv, audit_split, write_report
raw = read_csv('ETHZ_METADATA.csv')
rows = [dict(record_id=r['trace_name'],
             station_key=r['station_network_code']+'.'+r['station_code'],
             split=r['split']) for r in raw]
report = audit_split(rows, group='station_key')
write_report(report, 'STATION_REPORT')
print(report['status'], report['shared_sources'])
```

Expected output: `FAIL 190` for all subset combinations. In `pairs`, the train/test comparison has **180** shared station keys, covering **9,637 of 10,485** test records. The remaining 848 test records use keys absent from training under this definition; no predictive performance is established for them. JSON retains the names `sources` and `shared_sources`, but `group_column=station_key` identifies what is counted. The key does not distinguish station deployment epochs or location codes.

Decision: retain the source-exclusion claim if that was the intended contract. Do not claim unseen-station evaluation for the complete supplied test partition. Do not automatically replace an official split merely to make an unrelated audit pass.

## 5 Interpret failure, warning and invalid input

| Outcome | CLI exit | Action |
|---|---:|---|
| PASS | 0 | Report the specific checked contract and input hash. |
| FAIL | 1 | Inspect affected records; resolve the mapping or allocation before claiming exclusion. |
| WARNING | 0 by default; 1 with `--strict` | Inspect incomplete evidence; do not interpret it as certification. |
| Invalid input or I/O error | 2 | Correct the input/path and rerun into a fresh directory. |

`docs/verify_walkthrough.py` creates explicitly synthetic inputs to exercise all five exit/status combinations (including strict WARNING). It also gives executable lineage, OOF, schema, artifact and history API examples. The history example returns WARNING for documented earlier training and for unknown history. These fixtures do not establish real augmentation lineage or actual model execution.

## 6 Verify use of an installed wheel outside the checkout

Use fresh directories. These commands install locally from the provided wheel without downloading dependencies:

```text
python -m pip install --no-deps --no-index --target INSTALLED_WHEEL dist/seismic_eval_audit-0.1.3-py3-none-any.whl
python docs/verify_walkthrough.py --installed INSTALLED_WHEEL --output USAGE_RUN --metadata ETHZ_METADATA.csv
```

The driver verifies the import location, invokes the CLI with the output directory as its working directory, records stdout/stderr and exit codes, and checks the ETHZ source and station results against direct set calculations. Outputs include `receipt.json`, `SUMMARY.md`, CLI reports and synthetic API JSON. Omitting `--metadata` runs only the offline synthetic examples. The repository CI uses that offline form on Linux/Windows and Python 3.10/3.12, in addition to the existing 27 tests and manifest check; CI does not download or audit ETHZ.

The recorded full example was run by the authors on Windows with Python 3.12.14, using the hash-identical cached ETHZ metadata. See `case_studies/verification/wheel_usage_receipt.json` and `walkthrough_logs/`. This demonstrates executable instructions and wheel separation; it is **not an independent-user adoption study**. The package, wheel, original 27 tests and historical model artifacts are unchanged.

## Where this fits with existing utilities

| Need | GroupKFold / GroupShuffleSplit interfaces | This workflow |
|---|---|---|
| Construct grouped allocations | Produce split indices from supplied groups. | Not a replacement or a new splitting algorithm. |
| Inspect a saved partition | Users can write checks around those indices. | Reads saved rows; produces violations, pairwise counts and status. |
| Check other saved evidence | Outside these two splitting interfaces. | Separate APIs consume OOF, lineage, schema, hash and history inputs. |
| Decide whether evaluation is independent | Split construction alone cannot establish this. | Recorded history remains qualified; no status certifies independence. |

This comparison concerns the two splitting interfaces, not all capabilities of scikit-learn or SeisBench. Primary documentation: [GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html), [GroupShuffleSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html), checked 27 October 2026.
