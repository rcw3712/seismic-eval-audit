# Schema-driven addition before overlap calculations

28 October 2026. Inspecting the first CSV header showed that Iquique has source origin properties but no source_id column. Its source-ID contract is therefore not assessable; no origin-time proxy will be presented as a supplied source identifier. Keep Iquique as a transparent schema/coverage case and audit station membership where split labels are valid.

Add ISC-EHB Depth Phases, using all 32 metadata chunks listed by its SeisBench adapter (1987 through 2018), not a chosen year subset. The schema contains source_id, split and station fields. Selection is based on complete ID/split availability, public metadata and an additional global depth-phase setting, before calculating its overlap. The original three-dataset plan and this amendment are both retained.

Native trace names are scoped to chunks; represent record identity as the tuple (chunk filename, trace_name), encoded unambiguously in JSON. Source IDs remain unchanged. This prevents collisions between waveform bucket addresses from different chunks without merging records.

Official adapter: https://github.com/seisbench/seisbench/blob/e5616ad33c00aba75d5130b44222df46b41e4094/seisbench/data/isc_ehb.py
Dataset reference: Münchmeyer, Saul and Tilmann (2023), https://doi.org/10.1785/0220230187.
