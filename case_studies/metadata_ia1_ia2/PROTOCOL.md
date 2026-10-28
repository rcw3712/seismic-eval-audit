# I-A1 and I-A2 metadata audit protocol

Defined 28 October 2026 before calculating overlap outcomes. This is an analysis plan, not an externally registered preregistration. Existing ETHZ source/station results are already known.

## Scope and selection

Use the supplied SeisBench metadata partitions, without training, inference, waveform downloads, or reassignment of published split labels. Initial datasets: ETHZ (Swiss regional seismicity), GEOFON (global/regional events), Iquique (Chilean aftershock sequence). These were selected for public metadata availability, contrasting geographic/settings and manageable full-table size, not observed overlap outcomes. Require trace identity, source identity, supplied split and station fields. Missing fields or unusable contracts are reported, not invented. Preserve all original rows and exact input hashes; any contract-specific exclusions must be enumerated. At least three assessable datasets are intended; an unavailable dataset may be replaced with an explicitly logged reason before computing its overlap.

BohemiaSaxony was considered but excluded: official documentation says restricted WEBNET data and no precompiled dataset. CEED was considered but deferred: the complete metadata is about 2.1 GB; do not use a convenient subset and label it the full dataset. These limitations are practical selection limits, not evidence about their splits.

## I-A1

Audit exact supplied source IDs and the tuple (station_network_code, station_code) on each complete eligible metadata table. Record all pairwise overlaps, distinct groups, record counts, test records and distinct test sources on groups also present in training. Use the archived seismic-eval-audit 0.1.3 wheel without changing the core. Verify results against independently implemented pandas group-by/crosstab calculations. Separate missing/invalid inputs from a genuine zero-overlap result. Never interpret a station FAIL as a defect unless unseen-station evaluation was intended. Catalog aliases and duplicate physical events are outside the audit.

## I-A2 ETHZ

Use source_origin_time (UTC) and source epicentre coordinates, not trace start times or station locations. Check that repeated observations of each source have a unique time and coordinate pair; report and exclude conflicted/missing source properties from the corresponding group audit. Preserve supplied split labels. Report both trace-weighted and distinct-source-weighted fractions with eligible denominators.

- Primary temporal grouping: calendar month in UTC. Sensitivity: calendar day and year; nonoverlapping 7-, 30- and 90-day windows anchored at 1970-01-01T00:00:00Z, with offsets 0 and half the window width. Explicit half-open bins.
- Primary spatial grouping: 25 km square cells in ETRS89 / LAEA Europe (EPSG:3035), x/y origin (0,0), floor indexing. Sensitivity: 10,25,50 km side lengths, each at origin offsets (0,0), (s/2,0), (0,s/2), (s/2,s/2). Use WGS84 input longitude/latitude with always_xy=True. Check validity/domain before interpreting cells. These are planar grid memberships, not exact distance buffers; a boundary can separate near neighbours.
- Report per-split origin-time ranges and whether every training source precedes every test source. Calendar-bin overlap and prospective temporal separation are different claims. A PASS for bins does not imply statistical independence, a minimum temporal gap or spatial distance.

All listed sensitivity configurations will be reported, including PASS or contrary outcomes; no threshold will be selected to maximize overlap. Results describe finite metadata snapshots, not model accuracy, causal leakage effects, or a representative survey of all seismic datasets. Author-run verification is not independent-user adoption.

## Outputs and preservation

Deliver executable acquisition/audit/verification scripts, exact input checksums and retrieval information, mapping/schema quality tables, group membership and violation records, compact summary tables, sensitivity figures, and a bounded interpretation report. Keep this evidence package separate from the completed manuscript, previous releases and DOI archives. Do not silently change the frozen software or existing results.
