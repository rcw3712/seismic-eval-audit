# seismic-eval-audit v0.1.3

Dedicated repository and targeted manuscript/documentation revision. The runtime audit contracts and scientific results remain unchanged from v0.1.2; no training or inference was performed.

- Clarifies the relationship to grouped split utilities, citing Pedregosa et al. (2011).
- Labels reconstructed lineage consistently within its evidence boundary.
- Adds a separate test earthquake to Fig. 1.
- Clarifies the absence-of-prior-exposure limitation.
- Documents data attribution and Linux/Windows CI with Python 3.10 and 3.12.
- Provides Zenodo metadata for archival. Post-release verification confirmed DOI 10.5281/zenodo.23684054 for the immutable v0.1.3 source/evidence snapshot; later manuscript and citation updates are outside that snapshot.

The original MATLAB repository, checkpoint/results archive and DOI 10.5281/zenodo.22824997 are retained. That DOI does not identify this package. Prior v0.1.2 reports remain under case_studies; their receipts describe the original checks, not new model execution. CHECKSUMS.csv verifies package bytes. The figure generator uses matplotlib optionally; core audit code uses only the Python standard library.
