# Cross-dataset and ETHZ space–time metadata audits

## Main finding

The supplied source-ID contracts pass for ETHZ, GEOFON and ISC-EHB Depth Phases, while their station memberships overlap between training and testing. Iquique supports a station audit but does not supply source IDs. ETHZ reproduces the documented chronological partition as a positive control; the substantive contrast is that its source-disjoint, chronological split nevertheless shares many spatial grid cells. These findings distinguish evaluation targets rather than demonstrate an error in the datasets or a change in predictive accuracy.

## Scope and provenance

This author-run audit uses the unchanged seismic-eval-audit 0.1.3 wheel. PROTOCOL.md was written before calculating the new overlap outcomes; previously reported ETHZ source/station outcomes were already known. PROTOCOL_AMENDMENT_1.md records the schema-driven addition of ISC-EHB when Iquique lacked source_id. No model training, inference or waveform processing was performed. The completed manuscript and its DOI archives are unchanged.

All 35 metadata files were downloaded from the official SeisBench distribution on 28 October 2026. ISC-EHB includes every adapter-listed yearly chunk from 1987 through 2018. Native record identity is the pair (chunk filename, trace_name); catalog source IDs and split labels are preserved. Station keys are JSON-encoded (network,station) pairs, with no location-code or deployment-epoch distinction. Every assessed source/station contract covers its complete snapshot; Iquique source-ID auditing is explicitly not assessable. Its pinned adapter documents standard random sampling of records, which does not guarantee event separation. Missing source IDs prevent testing that requirement precisely where record-level allocation can be consequential; neither actual overlap nor a ranking as the highest-risk dataset is established. There is no invented origin-time proxy for source identity.

The snapshots comprise 515,692 metadata rows. ISC-EHB contains 190,275 rows and 45,028 supplied source IDs in the downloaded files, whereas the current overview documentation lists 174,436 traces and 44,106 events. This discrepancy is disclosed rather than reconciled speculatively: results apply to the exact 32-file snapshot identified by hashes, not an assumed publication count. The retrieved metadata may differ from the snapshot described on that overview page. No duplicated (chunk,trace_name) keys were found.

Selection was purposive: public metadata, compatible fields and contrasting seismic settings, with manageable full-table sizes. It is not a representative survey of SeisBench. BohemiaSaxony lacks a public precompiled dataset because of restricted network data; CEED's approximately 2.1 GB full metadata was deferred. No outcome-based dataset substitution was performed.

## I-A1 supplied source and station memberships

| Dataset | Metadata records | Supplied source IDs | Source train–test overlap | Station keys shared train–test | Test records on training station keys |
|---|---:|---:|---:|---:|---:|
| ETHZ | 36,743 | 2,231 | 0 | 180 | 9,637/10,485 (91.91%) |
| GEOFON | 275,274 | 2,270 | 0 | 643 | 80,798/86,261 (93.67%) |
| ISC-EHB Depth Phases | 190,275 | 45,028 | 0 | 1,576 | 37,540/37,566 (99.93%) |
| Iquique | 13,400 | Not supplied | Not assessable | 51 | 4,020/4,020 (100.00%) |

All three assessable source-ID audits have zero shared source IDs across all supplied subsets. ETHZ and GEOFON reproduce the chronological cutoffs in their pinned adapters (2019-01-08 / 2019-09-04 and 2012-11-01 / 2013-03-15, respectively), with zero label mismatches across 36,743 and 275,274 rows. These are positive controls against documented designs. The ISC-EHB adapter lists yearly chunks but does not define the split. The primary paper (Münchmeyer, Saul and Tilmann, 2024, Section 2.1; online 2023) describes random allocation of events to 70% training, 10% development and 20% testing, keeping all traces of each event together. Our source-ID result is consistent with that design; it does not reconstruct the original random assignment or establish byte identity with the smaller publication snapshot. All four station audits fail a separately stated unseen-station exclusion contract. This is not evidence that station exclusion was the dataset designers' intended target. In a global teleseismic dataset such as ISC-EHB, extensive reuse of the observing network is compatible with its purpose; unseen-station exclusion is only an optional additional target, not a quality criterion imposed on that dataset. Counts are within each dataset; no cross-catalog matching of physically identical events between datasets is claimed. The legacy report fields sources/shared_sources count the grouping unit identified by group_definition.

## I-A2 spatial membership in ETHZ

ETHZ contains 14 adapter-local source IDs beginning sb_id_, covering 376 records (train: 13 IDs/292 records; dev: 1 ID/84 records; test: 0). The adapter generates such an ID once per event when the catalog resource identifier ends in /1; within-event grouping is retained, but the field alone is not a resolvable catalog identifier. All 2,231 ETHZ source IDs have internally consistent, valid origin times and epicentre coordinates across their repeated records; all fall within the EPSG:3035 domain. All 36,743 records are retained. Coordinates are transformed from WGS84 longitude/latitude using always_xy=True to ETRS89-extended / LAEA Europe. Square cells use floor indexing, with a primary width of 25 km and origin (0,0). Widths 10,25,50 km and four origin offsets were specified before inspecting these results.

At the primary grid, 93 cells are shared between training and testing. 512/524 test source IDs (97.71%) and 10,382/10,485 test records (99.02%) occupy training-represented cells.

| Cell side | Test source IDs on training cells, range across four origins | Test records on training cells, range |
|---|---:|---:|
| 10 km | 424/524–442/524 (80.92%–84.35%) | 82.45%–84.85% |
| 25 km | 509/524–516/524 (97.14%–98.47%) | 98.77%–99.44% |
| 50 km | 520/524–523/524 (99.24%–99.81%) | 99.67%–99.89% |

The ranges describe sensitivity to four grid origins, not confidence intervals. All twelve spatial configurations contain shared train–test cells. A cell label is not an exact distance buffer: nearby sources can fall on opposite sides of a boundary, and within-cell distances vary. Neither a spatial FAIL nor a PASS establishes a causal effect on model performance or statistical independence.

## I-A2 temporal membership in ETHZ

As a positive control for the documented chronological design, every training origin time precedes every test origin time. The latest training source is 2019-01-07T13:21:19.080879Z and the earliest test source is 2019-09-04T13:43:22.273780Z, separated by 240.015315 days. This is the separation between training and testing, with the development interval between them; it is not an empty period with no observed events.

Calendar months have no training–test overlap. The adapter cutoffs fall within January (8 January) and September (4 September) 2019, explaining why those calendar months straddle adjacent subsets. The three-subset month audit reports FAIL because January 2019 is shared by train/dev and September 2019 by dev/test: two months and 935 affected records in total. Calendar days are disjoint across all three subsets. The broad year-2019 bin is shared between training and testing despite their chronological order. All predefined 7-,30-,90-day configurations have zero training–test overlap. These distinctions prevent an arbitrary time-bin FAIL from being described as temporal leakage.

| Origin-time groups | Shared groups across any subsets | Shared train–test groups | Test source IDs on training groups |
|---|---:|---:|---:|
| calendar_month | 2 | 0 | 0/524 |
| calendar_day | 0 | 0 | 0/524 |
| calendar_year | 1 | 1 | 157/524 |
| window_7d_offset_0d | 2 | 0 | 0/524 |
| window_7d_offset_3.5d | 2 | 0 | 0/524 |
| window_30d_offset_0d | 2 | 0 | 0/524 |
| window_30d_offset_15d | 2 | 0 | 0/524 |
| window_90d_offset_0d | 2 | 0 | 0/524 |
| window_90d_offset_45d | 2 | 0 | 0/524 |

## Verification and limits

Twenty-eight assessable contract outputs were recomputed from the original CSVs by a separate pandas/vectorized implementation that does not import audit.py or the audit core. The follow-up context check also verifies every ETHZ/GEOFON split label against its documented time cutoffs and counts ETHZ adapter-local IDs (provenance/context_verification.json). The primary runner also checks report counts and pairwise overlaps against independent group-by aggregation. All 35 input hashes and the original wheel hash were verified. Projection-origin, forward/inverse transformation, negative-coordinate floor, UTC conversion and half-open time-boundary checks passed. See provenance/verification.json and the group-level reports.

This is author-run computational cross-checking, not independent-user adoption. Source IDs are supplied metadata, not independently verified physical earthquake associations. Iquique's missing source_id is a contract limitation, not evidence of zero overlap. No performance metric, causal leakage estimate or claim that all seismic datasets behave alike is supported. The additions strengthen demonstrated metadata portability and the distinction among evaluation units; they do not establish a new audit algorithm or guarantee editorial acceptance.

## Reusable results wording for a later manuscript decision

Across three complete metadata snapshots with supplied source identifiers (ETHZ, GEOFON and ISC-EHB Depth Phases), source memberships were disjoint, while 91.91%, 93.67% and 99.93% of test records, respectively, used station keys represented in training. Iquique shared all test station keys but did not provide the source-ID field required for the source contract. In ETHZ, all training sources preceded test sources, while 512/524 test source IDs occupied training-represented 25 km cells. Thus, source exclusion, station exclusion, temporal ordering and spatial-cell exclusion describe different evaluation requirements; the metadata audit does not equate an unmet additional requirement with an error in the supplied split.

## Sources

- SeisBench benchmark metadata descriptions and dataset references: https://seisbench.readthedocs.io/en/main/pages/data/benchmark_datasets.html
- Pinned adapter code and default chronological cutoffs: https://github.com/seisbench/seisbench/tree/e5616ad33c00aba75d5130b44222df46b41e4094/seisbench/data
- SeisBench software: Woollam et al. (2022), https://doi.org/10.1785/0220210324.
- Iquique: Woollam, J., Rietbrock, A., Bueno, A., and De Angelis, S. (2019). Convolutional Neural Network for Seismic Phase Classification, Performance Demonstration over a Local Seismic Network. Seismological Research Letters 90(2A), 491–502. https://doi.org/10.1785/0220180312.
- ISC-EHB Depth Phases: Münchmeyer, J., Saul, J., and Tilmann, F. (2024; online 2023). Learning the Deep and the Shallow: Deep-Learning-Based Depth Phase Picking and Earthquake Depth Estimation. Seismological Research Letters 95(3), 1543–1557. https://doi.org/10.1785/0220230187.
- GEOFON benchmark context: Münchmeyer et al. (2022), Which picker fits my data? A quantitative evaluation of deep learning based seismic pickers. Journal of Geophysical Research: Solid Earth 127, e2021JB023499. https://doi.org/10.1029/2021JB023499. This is a benchmark reference, not a verified dedicated DOI for the distributed GEOFON snapshot. Network GE attribution: GEOFON Data Centre (1993), https://doi.org/10.14470/TR560404; this network DOI does not identify the entire multi-network benchmark.
- CRS definition: EPSG:3035, retained as WKT in results/I_A2/geometry.json; PROJ/pyproj provenance in verification.json.
- ETHZ network attribution remains CH 10.12686/sed/networks/ch; C4 10.12686/sed/networks/c4; 8D 10.12686/sed/networks/8d; S 10.12686/sed/networks/s; XT 10.12686/alparray/xt_2014.

Original dataset and network attribution/licensing remains separate from the MIT software license. Raw metadata are retained locally for reproducibility. The public evidence bundle excludes raw metadata and record-level tables; it provides hashes, official-source acquisition, original analysis scripts and aggregate outputs. Dataset redistribution permission has not been established uniformly for these 35 files; no software license is extended to them. See LICENSE_REVIEW.md and ARCHIVE_STATUS.md. The old DOI does not identify this new evidence.
