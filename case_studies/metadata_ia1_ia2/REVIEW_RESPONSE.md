# Follow-up corrections to the I-A1/I-A2 evidence

All overlap counts remain unchanged. The review improves interpretation and traceability; its numerical editorial score is a simulation, not an estimate of acceptance probability.

1. **Chronology as a positive control.** Every ETHZ and GEOFON split label was checked against the pinned adapter cutoffs; mismatches are zero for all 36,743 and 275,274 records. ETHZ's January/September month sharing is explained by the 8 January and 4 September boundaries. The useful contrast is chronological source separation with extensive spatial-cell sharing.
2. **Iquique as an untestable requirement.** The adapter documents random sampling of records. Without source IDs, event separation cannot be checked. This illustrates a consequential metadata omission; it neither proves source overlap nor establishes Iquique as the highest-risk dataset.
3. **Adapter-local IDs.** ETHZ has 14 `sb_id_` source IDs and 376 records: 13 IDs/292 records in train, 1 ID/84 records in dev, none in test. The adapter assigns these once per event when the resource suffix is `/1`; grouping remains possible, but that field alone cannot resolve the original catalog identifier. See `audit_context.py` and `provenance/context_verification.json`.
4. **ISC-EHB split definition.** Section 2.1 of the primary paper specifies random 70/10/20 allocation with event groups intact. The downloaded source-disjoint snapshot is consistent with this design; the adapter itself only lists chunks. Reusing global observing stations is compatible with its purpose. The publication-count discrepancy remains disclosed.

The full journal citation is Münchmeyer, Saul and Tilmann (2024), *Seismological Research Letters* 95(3), 1543–1557, DOI 10.1785/0220230187; online publication was 17 October 2023. The article's Section 2.1 was inspected in the GFZ-hosted postprint (PDF page 7 / printed page 5, lines 94–98). Source URL and hash are in `provenance/review_source_manifest.json`; the paper itself is not redistributed.

The GEOFON dataset was used in Münchmeyer et al. (2022), DOI 10.1029/2021JB023499. Neither that use nor network GE's DOI is asserted to be a dedicated identifier for the benchmark snapshot. SeisBench's own dataset citation remains incomplete.

## Publication corrections

The public bundle excludes all 35 raw CSVs and detailed row/group tables. Official-source acquisition, frozen hashes, aggregate results and regeneration scripts remain available. A Git tag alone does not mint a DOI: a public GitHub release must be archived through Zenodo, and the resulting record and bytes must be verified before claiming archival coverage. See ARCHIVE_STATUS.md for actual status.

Do not paste the review's abstract unmodified: the percentages 92–100% combine source-assessable datasets and Iquique, so the denominator scope must be explicit. Prefer the exact 91.91–100% range across all four datasets and separate the three assessable source-ID results. The protocol was written before new counts, but the earlier ETHZ source/station results were already known, and ISC-EHB was added through a documented schema-driven amendment.
