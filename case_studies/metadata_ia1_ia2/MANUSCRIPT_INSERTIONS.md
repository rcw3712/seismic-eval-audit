# Candidate integration text — retain as a separate proposal pending manuscript decision

The completed manuscript has not been edited in this audit task. Use the verified public evidence identifier from ARCHIVE_STATUS.md when integrating these paragraphs; do not attribute them to the previous software DOI. Confirm section/table numbering against the manuscript version being edited.

## Methods

To test transfer of the membership audit beyond one metadata table, we applied the unchanged seismic-eval-audit v0.1.3 wheel to four complete SeisBench metadata snapshots retrieved on 28 October 2026: ETHZ, GEOFON, ISC-EHB Depth Phases and Iquique (515,692 records). Selection was purposive, based on public metadata availability, compatible fields and contrasting settings. A written protocol preceded the new overlap calculations; earlier ETHZ source/station results were already known, and ISC-EHB was added through a documented amendment when Iquique lacked source identifiers. Record keys combined chunk filename and trace_name; supplied source IDs and split labels were retained, and station keys paired network and station codes. Iquique's source contract was not assessable. ETHZ source epicentres were grouped into 10, 25 and 50 km cells in EPSG:3035 at four grid origins, while source-origin times were grouped by calendar day, month and year and by 7-, 30- and 90-day windows at two offsets. A separate pandas implementation recomputed all 28 assessable contract outputs from the original files. Documented ETHZ and GEOFON chronological cutoffs served as positive controls.

## Results

The three datasets supplying source identifiers had disjoint source memberships across their supplied subsets. Across all four datasets, 91.91% (ETHZ), 93.67% (GEOFON), 99.93% (ISC-EHB) and 100% (Iquique) of test records used network–station keys represented in training. Iquique's adapter documents random record sampling, which does not guarantee source separation; missing source IDs prevent measuring actual source overlap. The ISC-EHB paper describes random 70/10/20 partitioning with event groups kept intact (Münchmeyer et al., 2024); station reuse in this global teleseismic setting is compatible with its intended evaluation. ETHZ and GEOFON reproduced their documented chronological partitions with zero label mismatches. In ETHZ, no predefined 7-, 30- or 90-day bin was shared between training and testing, yet 512/524 test source IDs (97.71%) occupied training-represented 25 km cells, and all twelve spatial configurations shared cells. A chronological split therefore does not imply spatial-cell exclusion. January and September 2019 monthly sharing arose at the within-month boundaries of adjacent subsets, rather than train–test overlap.

ETHZ contained 14 adapter-generated sb_id_ identifiers covering 376 records (292 train, 84 development, no test records). These preserve within-event grouping but do not themselves provide resolvable catalog identifiers.

## Abstract replacement

Metadata audits of four SeisBench datasets (515,692 records) verify source-disjoint supplied splits in all three with source identifiers; across all four datasets, 91.91–100% of test records use training-represented station keys. ETHZ reproduces its documented chronological split, yet 97.71% of test sources occupy training-represented 25 km cells.

## Limitations

The four datasets were selected purposively and do not constitute a representative survey. Supplied source IDs were not independently reconciled with physical earthquake identities. The downloaded ISC-EHB snapshot (190,275 records; 45,028 source IDs) differs from the published 174,436 traces and 44,106 events, so results apply to the hashed snapshot. Spatial cells are not distance buffers, temporal bins do not establish statistical independence, and neither audit estimates an effect on model accuracy. Verification remains author-run rather than independent adoption. Raw metadata are obtained from upstream providers and excluded from the evidence release; regeneration requires availability of the exact hashed inputs.

Retain the existing historical-development-exposure limitation unchanged. These additions demonstrate portability and different evaluation requirements, not a new splitting algorithm or an independently confirmed improvement in picker accuracy.
