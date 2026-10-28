# Cross-dataset and ETHZ space–time metadata audits

Evidence release **metadata-audit-20261028-r1**, using the unchanged **seismic-eval-audit 0.1.3** wheel. The runtime has not been retrained, modified or renumbered. This extension adds metadata evidence; no model training or inference was performed. See [AUDIT_REPORT.md](AUDIT_REPORT.md), [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md), and [ARCHIVE_STATUS.md](ARCHIVE_STATUS.md).

## Findings and boundaries

- Four full snapshots contain 515,692 records. ETHZ, GEOFON and ISC-EHB have disjoint supplied source IDs; Iquique supplies no source-ID field and is not assessable on that contract.
- Test records using training-represented network–station keys: ETHZ 91.91%, GEOFON 93.67%, ISC-EHB 99.93%, Iquique 100%.
- ETHZ and GEOFON reproduce their documented chronological designs with zero record-label mismatches: positive controls, not novel split designs.
- ETHZ nevertheless places 512/524 test source IDs in training-represented 25 km cells. Twelve spatial configurations and nine temporal definitions are reported without selecting the strongest result.
- ISC-EHB's paper describes event-grouped random 70/10/20 allocation. Network reuse is compatible with its global teleseismic purpose; unseen-station exclusion is not imposed as its intended criterion.
- Iquique's documented record sampling does not guarantee source exclusion. Without source IDs, actual source overlap is unmeasured, not zero or established.
- ETHZ contains 14 adapter-local sb_id_ identifiers covering 376 records, all in train/dev. They retain within-event grouping but do not independently identify catalog events.

These author-run checks demonstrate metadata portability and distinct evaluation requirements. They are not independent-user adoption, a causal estimate of leakage, a representative dataset survey, or a model-accuracy experiment. The original historical-development-exposure limitation remains.

## Public package and input availability

The 35 raw CSVs and detailed membership, violation and source-location tables are **not included** because uniform redistribution permission was not established. See [LICENSE_REVIEW.md](LICENSE_REVIEW.md). Original-source URLs and SHA-256 hashes are preserved in `provenance/input_manifest.json`; the acquisition script rejects changed bytes. Thus numerical regeneration depends on continued access to those exact upstream bytes. The downloaded ISC-EHB snapshot differs in size from the paper/overview; the report explicitly discloses this.

`reference_results/` contains aggregate outputs from the completed run. The 28-contract verification receipt is retained in `provenance/verification.json`. `figures/` contains PNG 600 dpi and vector PDF figures with captions. Downloaded articles and adapter sources are not republished; URLs/hashes identify them.

## Reproduce

From **this directory**, with Python 3.12, run each command only after the previous one succeeds. Initial dependency installation and metadata acquisition require internet. No MATLAB or GPU is required; minimum hardware has not been benchmarked.

```powershell
python check_package.py
python -m pip install --target .deps -r requirements.txt
python -m pip install --no-deps --no-index --target software/installed software/seismic_eval_audit-0.1.3-py3-none-any.whl
python acquire_ranges.py
python audit.py --section a1
python audit.py --section a2
python verify.py
python audit_context.py
python -c "import json; from pathlib import Path; assert all(json.loads((Path('results')/s/'summary.json').read_text()) == json.loads((Path('reference_results')/s/'summary.json').read_text()) for s in ['I_A1','I_A2']); print('PASS: numerical summaries match')"
python report.py
```

`audit.py` refuses to overwrite an existing result directory. Use a fresh copy for each repeat. `verify.py` reconstructs memberships from the original CSVs with separate pandas/vectorized code and checks the wheel and input hashes. `audit_context.py` verifies the documented chronological cutoffs and counts adapter-local IDs. `check_package.py` verifies delivery bytes **before** regeneration; environment receipts and generated PDF/gzip bytes may change on a new execution. The frozen reference aggregates provide numerical comparisons, not a requirement for bit-identical newly compressed files.

`record_sources.py` optionally fetches pinned SeisBench adapter files for local inspection; these are neither executed nor part of the MIT software distribution. The complete local audit retains detailed rows; this public package provides scripts to regenerate them. All original protocols and the schema-driven ISC-EHB amendment are preserved rather than rewritten retrospectively.
