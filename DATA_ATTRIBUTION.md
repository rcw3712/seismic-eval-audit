# Data attribution and modifications

## STEAD-derived identifiers

Original dataset: Mousavi SM, Sheng Y, Zhu W, Beroza GC (2019), Stanford Earthquake Dataset (STEAD): A global data set of seismic signals for AI. IEEE Access 7:179464–179476. https://doi.org/10.1109/ACCESS.2019.2947848.

Provider: https://github.com/smousavi05/STEAD. The upstream repository supplies the Creative Commons Attribution 4.0 International licence: https://github.com/smousavi05/STEAD/blob/master/LICENSE and https://creativecommons.org/licenses/by/4.0/.

`examples/historical_stead.csv` and STEAD-derived identifier tables under `case_studies/results` select retained observations and combine recovered source associations with local split, fold, historical-role or reconstructed-lineage fields. These are documented adaptations of the metadata and workflow, not unmodified upstream tables. The original extraction criteria cannot be fully reconstructed. No upstream endorsement is implied. Credit the original dataset and this audit package when reusing these tables. The original CC BY 4.0 terms remain applicable to upstream material.

## ETHZ and SeisBench metadata

Provider: SeisBench, https://github.com/seisbench/seisbench; metadata URL and tested SHA-256 are recorded by fetch_ethz.py and the run receipts. Full raw metadata and waveform files are not redistributed here. Derived membership tables and audit reports identify the tested records and transformations. Upstream data terms remain applicable; the software MIT licence does not relicense third-party data.

Network attribution follows SeisBench's ETHZ adapter and Online Resource 1 Table S4: Swiss Seismological Service at ETH Zurich (1983), National Seismic Networks of Switzerland, https://doi.org/10.12686/sed/networks/ch; CERN (2016), CERN Seismic Network, https://doi.org/10.12686/sed/networks/c4; Swiss Seismological Service at ETH Zurich (2005), Temporary deployments in Switzerland associated with aftershocks and other seismic sequences, https://doi.org/10.12686/sed/networks/8d; Swiss Seismological Service at ETH Zurich (2008), Seismology at School Program, https://doi.org/10.12686/sed/networks/s; AlpArray Seismic Network (2014), Eastern Alpine Seismic Investigation (EASI) - AlpArray Complimentary Experiment, https://doi.org/10.12686/alparray/xt_2014.

The source-grouped and record-random controls are explicitly constructed transformations; the supplied split is retained separately. The network.station key joins the supplied network and station strings and does not resolve deployment epochs.

## Software

LICENSE applies to original software under MIT. Third-party data attribution and licence conditions above are retained separately.
