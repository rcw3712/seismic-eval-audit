# Seismic evaluation audit

A small Python tool for checking supplied earthquake identifiers across data splits. It does not train or recommend a picker. Python 3.10+; core checks use only the standard library. MIT software license. Version 0.1.3. Versioned source and assets: https://github.com/rcw3712/seismic-eval-audit/releases/tag/v0.1.3

## Five-minute start

From the repository root:

```powershell
python -m unittest discover -s tests -v
python -m seismic_eval_audit examples/metadata.csv --output NEW_REPORT
```

Or install with `python -m pip install .` and use `seismic-eval-audit` from any directory. Existing output directories are never overwritten. Exit codes: 0 for PASS or WARNING, 1 for detected overlap, 2 for invalid input or I/O failure. Read the report status; exit zero is not a general certification.

Your CSV must have unique record_id, source_id and split text columns. Existing column names can be selected:

```powershell
python -m seismic_eval_audit YOUR_METADATA.csv --record trace_name --group source_id --split split --output NEW_REPORT
```

IDs remain text, including leading zeros. Missing IDs, duplicate record IDs, null-like IDs and surrounding whitespace are rejected. A one-split file produces WARNING. Dev and val are not silently merged; harmonize documented split labels before use.

## Python API

```python
from seismic_eval_audit import read_csv, audit_split, assign_split, write_report
rows = read_csv('examples/metadata.csv')
report = audit_split(rows)
print(report['status'], report['pairs'])
new_rows = assign_split(rows, grouped=True, seed=42)
assert audit_split(new_rows)['shared_sources'] == 0
write_report(report, 'NEW_REPORT')
```

Additional APIs: check_lineage(parents, children), check_oof(held, fit, inner_validation), check_schema(actual, expected), check_artifacts(root, entries), audit_history(current, history). See tests for executable schemas and positive/negative examples. The CLI runs the split check only; no other check is implied. For dataframe users, pass `df.to_dict('records')` after preserving text identifiers. No dependency on SeisBench or MATLAB is needed.

The grouped splitter sorts IDs, uses Python random.Random(seed), allocates floor(0.7*N) and floor(0.15*N) groups to train/dev, and assigns remaining groups to test. Fractions are by group, not by record; no stratification or optimal balancing is claimed. Its output changes the evaluation population and is not a fair before/after performance comparison.

## ETHZ reproduction

Download only metadata with `python fetch_ethz.py --output NEW_METADATA.csv`. The expected SHA256 identifies the tested version; the downloader rejects changed bytes. Then run:

```powershell
python run_ethz.py --metadata NEW_METADATA.csv --output NEW_ETHZ_RESULTS
```

The three conditions are the supplied split, an intentionally created random record split, and a grouped split. Reported overlap in the random control is not a claim about the supplied SeisBench split. Actual run receipts accompany this package. No waveform, neural inference, model accuracy or source catalogue truth is checked.

## Interpretation

FAIL means the declared exclusion rule is violated under supplied IDs. PASS does not establish physical correctness of IDs, absence of near duplicates, independent development history, or station/region transfer. All history reports remain WARNING: recorded roles do not certify independence. Hash agreement establishes identity with a reference, not correctness of that reference. No fuzzy event grouping is provided. The separate legacy HDF5 reconstruction utility belongs to the retained STEAD case study and is not required by this tool.

STEAD-derived identifier tables retain CC BY 4.0 attribution; see [DATA_ATTRIBUTION.md](DATA_ATTRIBUTION.md) for original providers, licence links and changes. The MIT license applies to software only. The older DOI identifies the historical model/result archive, not this new package. The v0.1.3 source and evidence are archived at https://doi.org/10.5281/zenodo.23684054.

## Worked user workflow

Start with [docs/WALKTHROUGH.md](docs/WALKTHROUGH.md): native SeisBench CSV columns, source versus station contracts, report interpretation, error exits and separate API examples. `docs/verify_walkthrough.py` exercises the unchanged v0.1.3 wheel from an isolated installation and outside the checkout. The author-run full ETHZ receipt is `case_studies/verification/wheel_usage_receipt.json`; stdout/stderr are in `case_studies/verification/walkthrough_logs/`.

The walkthrough reproduces the existing ETHZ source and station counts; it does not add a dataset, train a model or claim independent-user adoption. The original 27 tests remain unchanged. CI additionally installs the wheel and runs the offline synthetic usage checks in all four OS/Python combinations; it does not download ETHZ. The guide, usage driver, receipts and revised documents postdate the immutable DOI archive and are identified by the current Git commit and manifest. The library and wheel remain byte-identical to the archived v0.1.3 release.

## Real artifact demonstration

27 automated tests pass. `audit_history` now separates prior train/val, prior-test-only, unknown and other documented roles and counts both sources and records. Role labels are explicit and configurable. `--strict` maps CLI warnings to exit 1 for CI; invalid input remains exit 2.

```powershell
python -m seismic_eval_audit examples/historical_stead.csv --output NEW_REPORT
python audit_case_studies.py --stead-root PATH_TO_LEGACY_SOURCE_VERIFIED_V2 --ethz NEW_METADATA.csv --output NEW_CASE_RESULTS
```

The first command intentionally returns exit 1: the recovered historical split has 283 sources spanning subsets; 151/335 test records share training sources, or 168/335 training/validation sources. This is a real historical failure, not an injected control. The corrected split passes. Current test history reports 196 sources/304 records with prior development roles, and 25 sources/26 records with prior-test-only roles.

Six saved OOF tables (five folds each) pass 30 configuration/fold checks against the actual inner-fold tables. Actual bytes of 106 checkpoints and 93 public code files match their existing manifests. All checks read artifacts only; no MATLAB, inference or training is invoked.

Lineage evidence is narrower: 9,264 child audit keys and training labels are reconstructed from existing OOF replay receipts; their source/fold linkage agrees with frozen parents. This is not an original training-time augmentation manifest and does not audit child waveform bytes. Feature-schema behavior remains demonstrated by synthetic controls only.

For ETHZ, 180 network.station keys are shared by training and testing (9,637/10,485 test records), although the supplied split has no shared source IDs. The generic report retains legacy JSON keys `sources` and `shared_sources`; for station audits these count station keys, as specified by `group_column=station_key`. This fails an unseen-station exclusion contract, not the intended source-disjoint contract. The key does not distinguish deployment epochs.

`case_studies/results` provides reports; `case_studies/results/input_hashes.csv` identifies the frozen inputs. Raw ETHZ metadata and waveforms are not redistributed. Tests for additional APIs are executable usage examples.

## Relationship to grouped split utilities

GroupKFold and GroupShuffleSplit in scikit-learn generate indices from supplied groups. This tool provides explicit contracts for checking saved memberships and related provenance tables, including derived-record links, multistage OOF exclusions, artifact hashes and historical roles. It does not introduce a new grouped splitting algorithm. The CLI checks partition membership and writes record-level violations; the other checks use Python APIs. See Pedregosa et al. (2011), https://jmlr.org/papers/v12/pedregosa11a.html, and the scikit-learn documentation for those splitting interfaces.

## Verification and evidence boundaries

Continuous integration runs 27 tests and `python verify_package.py` on Linux and Windows, with Python 3.10 and 3.12 (four combinations). Python 3.11 and macOS are not part of this matrix. The earlier local verification used Python 3.12.14 on Windows. See the Actions tab for status against the exact commit.

The manuscript labels receipt-derived lineage **Consistent (reconstructed)**. The API's PASS checks only consistency of supplied tables; reconstructed parent keys and training labels do not establish an independently observed augmentation-time history. Scientific counts and the 27 tests are unchanged from v0.1.2.

The historical artifacts needed by `--stead-root` are separate from this small repository. Obtain the preserved `source_verified_v2` package from https://github.com/rcw3712/ICNN_MetaPicker_Curated_STEAD_MATLAB and the corresponding historical archive at https://doi.org/10.5281/zenodo.22824997. Point the argument to the directory containing its `inputs`, `results`, `audit`, and model artifacts. This dedicated repository does not duplicate the model checkpoints.

## Archival status

The earlier package remains at the immutable historical commit 872a4ac93eb24cad10b2473581471dddfd09154d and tag seismic-eval-audit-v0.1.2 in the original repository. This dedicated repository begins with v0.1.3. `.zenodo.json` supplies archive metadata. The verified version DOI is https://doi.org/10.5281/zenodo.23684054; it identifies tag archive-v0.1.3, which points to the same original v0.1.3 commit (287138537796c577a383844a6faa57f126e17568). The older DOI must not be used to identify this Python release. PyPI publication is not claimed; install the provided wheel or source locally.

## Verified Zenodo archive

Software version 0.1.3: https://doi.org/10.5281/zenodo.23684054. Public record: https://zenodo.org/records/23684054. DataCite registration is findable. The Zenodo ZIP checksum and all 76 hashes in its embedded manifest match the immutable release. See case_studies/verification/zenodo_archive_verification.json.

This branch includes manuscript and citation updates made after DOI verification. The DOI identifies the tagged source/evidence snapshot, not later changes to this branch. Current CHECKSUMS.csv verifies the current package; the archive retains its original manifest. Both v0.1.3 and archive-v0.1.3 point to commit 287138537796c577a383844a6faa57f126e17568. No training or inference was performed for archival. The previous model/result DOI 10.5281/zenodo.22824997 is unchanged.

## Software authorship

Rahmat Catur Wibowo developed the Python package seismic-eval-audit. The Software contributions of Razki Alfatah Khairu Mahli and Karyanto in the manuscript relate to the historical MATLAB pipeline, not to this Python package. The single-author CITATION.cff and Zenodo software record therefore describe a different contribution scope from the multi-author manuscript and historical model/result archive. Manuscript authorship is not inferred from Git commit authorship.

The current branch contains minor pre-submission editorial and attribution updates made after the v0.1.3 archive. No library implementation, original tests, numerical model results, checkpoint files or immutable release tags were changed. Later usage documentation and its verification driver are additions outside the archived release.

## Four-item editorial closure — 28 October 2026

The manuscript now follows a candidate Software Article structure: Design and Implementation, Availability and Requirements after Conclusions, and Software Files after Tables and captions. This is a prepared candidate, not editorial confirmation of category or permission to resubmit. Online Resource sections and tables are ordered consecutively; source PASS and station FAIL are linked to explicit user decisions. All table contents and scientific results are unchanged.

The post-archive walkthrough and its verification receipt are fixed at commit [502b5415bead677ec810207affed55a0e76a9f82](https://github.com/rcw3712/seismic-eval-audit/tree/502b5415bead677ec810207affed55a0e76a9f82). Its [CHECKSUMS.csv](https://github.com/rcw3712/seismic-eval-audit/blob/502b5415bead677ec810207affed55a0e76a9f82/CHECKSUMS.csv) has SHA-256 `a2701d79c075badc3f9118e67852783182fc9eda577902ad2c6a327ae2f6e79d`. The current commit and current manifest identify the later editorial documents separately. Neither set of additions is attributed to the original v0.1.3 DOI snapshot.

This limited editing cycle is closed pending feedback from the editor or an independent user. No new training, inference, dataset, library, wheel, original-test or model-result changes were made in this pass. The usage verification remains author-run; independent adoption is not claimed.

## Final declaration and presentation corrections

The 28 October 2026 correction adds the ethics approval/participation and publication-consent declarations, explains earlier development exposure in the abstract, removes editorial-process wording from public availability statements, and places the three-sentence Table 3 note below the table. Section 4.2 now names both source and station membership outcomes; the installation instruction explicitly starts from the repository root. Table 1–3 first mentions remain ordered. Numerical table contents, library, wheel, original tests, case results and immutable archives are unchanged. Minimum hardware requirements remain unbenchmarked; independent-user adoption is not claimed. Editing is closed pending editor or independent-user feedback.


## Cross-dataset metadata evidence (28 October 2026)

The separate [I-A1/I-A2 evidence package](case_studies/metadata_ia1_ia2/README.md) applies the unchanged v0.1.3 wheel to four complete metadata snapshots (515,692 records). It adds 28 verified contracts, positive controls against documented ETHZ/GEOFON chronology, 12 ETHZ spatial configurations and nine temporal definitions. Iquique remains unassessable for source exclusion because its source-ID field is absent. ISC-EHB is interpreted against the primary paper’s event-grouped split. See the package report for limits and snapshot discrepancies.

Raw metadata and record-level tables are excluded from this new public bundle; exact input hashes and official-source acquisition/regeneration scripts are included. This is author-run metadata evidence, not independent adoption or model-performance testing. The software wheel, prior release tags/DOIs, historical model artifacts and completed manuscript are unchanged. The new evidence release is metadata-audit-20261028-r1; its DOI must be verified before citation (see ARCHIVING.md).
