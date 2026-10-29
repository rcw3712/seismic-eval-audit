# Data attribution and modifications

## STEAD-derived identifiers

Original dataset: Mousavi SM, Sheng Y, Zhu W, Beroza GC (2019), Stanford Earthquake Dataset (STEAD): A global data set of seismic signals for AI. IEEE Access 7:179464–179476. https://doi.org/10.1109/ACCESS.2019.2947848.

Provider: https://github.com/smousavi05/STEAD. The upstream repository supplies the Creative Commons Attribution 4.0 International licence: https://github.com/smousavi05/STEAD/blob/master/LICENSE and https://creativecommons.org/licenses/by/4.0/.

`examples/historical_stead.csv` and STEAD-derived identifier tables under `case_studies/results` select retained observations and combine recovered source associations with local split, fold, historical-role or reconstructed-lineage fields. These are documented adaptations of the metadata and workflow, not unmodified upstream tables. The original extraction criteria cannot be fully reconstructed. No upstream endorsement is implied. Credit the original dataset and this audit package when reusing these tables. The original CC BY 4.0 terms remain applicable to upstream material.

## ETHZ and SeisBench metadata

Provider: SeisBench, https://github.com/seisbench/seisbench; metadata URL and tested SHA-256 are recorded by fetch_ethz.py and the run receipts. Full raw metadata and waveform files are not redistributed here. Derived membership tables and audit reports identify the tested records and transformations. Upstream data terms remain applicable; the software MIT licence does not relicense third-party data.

Network attribution follows SeisBench's ETHZ adapter and Online Resource 1 Table S9: Swiss Seismological Service at ETH Zurich (1983), National Seismic Networks of Switzerland, https://doi.org/10.12686/sed/networks/ch; CERN (2016), CERN Seismic Network, https://doi.org/10.12686/sed/networks/c4; Swiss Seismological Service at ETH Zurich (2005), Temporary deployments in Switzerland associated with aftershocks and other seismic sequences, https://doi.org/10.12686/sed/networks/8d; Swiss Seismological Service at ETH Zurich (2008), Seismology at School Program, https://doi.org/10.12686/sed/networks/s; AlpArray Seismic Network (2014), Eastern Alpine Seismic Investigation (EASI) - AlpArray Complimentary Experiment, https://doi.org/10.12686/alparray/xt_2014.

The source-grouped and record-random controls are explicitly constructed transformations; the supplied split is retained separately. The network.station key joins the supplied network and station strings and does not resolve deployment epochs.

## Software

LICENSE applies to original software under MIT. Third-party data attribution and licence conditions above are retained separately.


## I-A1/I-A2 metadata extension

The new case_studies/metadata_ia1_ia2 bundle redistributes no raw ETHZ, GEOFON, Iquique or ISC-EHB metadata and no record-level membership/location tables. The upstream dataset licenses are not inferred from SeisBench’s GPL software license or this project’s MIT license. The 35 per-file decisions, official URLs and hashes are supplied in the bundle. Aggregate findings, original scripts and derived figures are provided with bibliographic and network attribution. See its LICENSE_REVIEW.md.

## Scope clarification checked 29 October 2026

The exclusion of row-level outputs applies to the **new case_studies/metadata_ia1_ia2 extension**, not the entire repository or either DOI archive. Both software DOI 10.5281/zenodo.23684054 and evidence DOI 10.5281/zenodo.23758930 contain four legacy identifier-only ETHZ membership tables: three under case_studies/ethz_source/*/membership.csv and one at case_studies/results/ethz_station/membership.csv. Each has 36,743 rows. Their fields are record_id, source_id or station_key, and split; these tables contain no waveforms, coordinates or additional metadata fields. The evidence archive retains these earlier files unchanged outside the extension directory.

Rechecking the [SED waveform-access page](https://www.seismo.ethz.ch/en/knowledge/earthquake-data-and-analysis-tools/waveform-data/), [CH network DOI page](https://networks.seismo.ethz.ch/networks/ch/), [C4 network page](https://networks.seismo.ethz.ch/networks/c4/), [XT network DOI page](https://doi.org/10.12686/alparray/xt_2014), [SED disclaimer](https://www.seismo.ethz.ch/en/service/Disclaimer/) and [SeisBench imprint](https://seisbench.gfz-potsdam.de/imprint/) did not establish a named redistribution license covering the complete converted ETHZ metadata table or derived identifier tables. SED provides open data access and asks for network DOI attribution; this is not treated as a blanket grant to relicense converted tables. The general website disclaimer is not substituted for a dataset-specific license. NOT_ESTABLISHED records a limit in the inspected evidence, not a finding that redistribution is prohibited. Existing archive contents do not themselves establish permission.

The original immutable archives and their manifests have not been rewritten. This clarification is current-branch documentation; it does not retroactively license the archived tables. Upstream confirmation of applicable terms remains unresolved. No third-party data are relicensed as MIT.
