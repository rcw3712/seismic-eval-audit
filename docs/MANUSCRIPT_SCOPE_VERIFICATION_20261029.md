# Manuscript scope and primary-source verification 29 October 2026

## Redistribution statement

Both downloaded Zenodo ZIPs were inspected, not just the current branch. Four identifier-only ETHZ membership tables are present in each archive; schemas, counts and hashes are recorded in case_studies/verification/manuscript_scope_verification_20261029.json. Corresponding files are byte-identical between archives. The new extension excludes its 35 raw inputs and newly generated row-level outputs. Its exclusion is not a claim that the full repository archive contains no identifier tables. LICENSE_REVIEW.md and DATA_ATTRIBUTION.md disclose this distinction and the unresolved scope of upstream permissions.

## Primary literature

Münchmeyer, Saul and Tilmann (2024), DOI https://doi.org/10.1785/0220230187: the author manuscript deposited at [GFZpublic](https://gfzpublic.gfz.de/pubman/item/item_5025323_7/component/file_5035055/5025323.pdf), Section 2.1, printed page 5 (PDF page 7), lines 94–98, supports random 70/10/20 event-grouped allocation and the totals 44,106 events / 174,436 traces. This was visually checked in the PDF. The cover identifies SRL 95(3):1543–1557 (2024); DOI bibliographic metadata confirms volume, issue and pages, with online publication on 17 October 2023. The downloaded metadata snapshot remains different (190,275 records / 45,028 source IDs). A pinned adapter is context, not proof of the version that generated those CSVs; the reason for the difference remains unresolved.

Yang C, Brower-Sinning RA, Lewis GA, Kästner C (2022), Data Leakage in Notebooks: Static Detection and Better Processes, ASE ’22, 12 pp., DOI https://doi.org/10.1145/3551349.3556918. Verified against the [author-hosted paper](https://www.cs.cmu.edu/~ckaestne/pdf/ase22.pdf). The manuscript describes static notebook analysis as complementary to saved-evidence audits, without a comparative performance claim.

## STEAD selection evidence

The inspected legacy config_ICNN_MetaPicker.m records intended distance ≤15 km, magnitude ≥1.5, SNR ≥10 dB and manual P/S status with reapplyAtLoad=false. Recovered metadata contradict an assertion that every retained record passed those criteria: 1,750 exceed 15 km, and only 1,817 have both picks marked manual. Distances span 0–49.99 km; magnitudes 2.5–5.9. All rows have three SNR values; 2,172 have all three ≥10 dB. The original extraction log and trace-level export mapping remain unavailable. The earlier thesis instead describes SNR 5–10 dB and magnitude ≥1.5 for about 28,000 waveforms. These descriptions are not reconciled by inventing a selection rule. Section 3.1 states intended criteria and their evidence limit; OR1 Section 5 reports recovered properties. No rows or model results were changed.

## Manuscript changes and verification

Data availability, Software Files and OR1 now distinguish extension versus archive scope. Section 4.2 punctuation, Fig. S1 reference, conclusion and commit wording follow the requested corrections. Abstract explicitly identifies Iquique as not assessable; transferability is limited to source/station checks. A compact set-based exclusion definition and Yang et al. reference were added. All four main tables and nine supplementary tables retain their numeric contents. Historical exposure, software attribution and AI disclosure remain. DOCX render inspection covers the complete main text and OR1; PDFs/page images are internal QA. These revised DOCX bytes are not attributed to either immutable DOI snapshot.
