# MarketFlow POSITION_SWING Canonical Dataset Operator Review Package Status

## Purpose
- Create an offline, digest-bound operator review package for the generated POSITION_SWING canonical dataset candidate.
- Preserve the authority boundary: this package does not freeze the POSITION_SWING dataset, approve registry eligibility, activate runtime use, authorize Strategy use, or accept predictive usefulness/profitability.

## Branch and Commit
- Branch: `feature/position-swing-canonical-dataset-operator-review-package-v1`
- Base commit: `ea3ed71e25cb2bd8b63998684401242156525004`
- Implementation commit: the commit containing this document.

## Review Package
- Artifact kind: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE`
- Review status: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY`
- Schema version: `position_swing_canonical_dataset_candidate_review_v1`
- Review package digest: `142d35d8b622e2f2db77fa07f48d3bf307126d5b25c6c0a72086d6d7ce4de8ea`
- Binding mode: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE_STATUS_BINDING`
- Created offline: `True`
- Provider requests made in review: `False`

## Reviewed POSITION_SWING Candidate
- Candidate artifact kind: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916`
- Dataset profile: `POSITION_SWING`
- Dataset bar rule: `RTH_FULL_SESSION_1D`
- Dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- Dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- Normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- Acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`

## Dataset Summary
- POSITION_SWING bar count: `994`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`

## 2025-01 Cross-Check
- Cross-check month: `2025-01`
- Cross-check status: `PASSED`
- 2025-01 POSITION_SWING bars: `20`

## Special-Session Policy
- Policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded from POSITION_SWING bars: `True`
- Special sessions recorded in exclusion inventory: `True`
- Special-session exclusion count: `9`
- Special-session rows excluded: `126`

## Local Artifact Binding
- Ignored candidate file verified: `True`
- Ignored dataset file verified: `True`
- Ignored manifest file verified: `True`
- Ignored dataset path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- Ignored manifest path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json`
- Ignored candidate path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_candidate.json`

## Checklist Summary
- Total checks: `38`
- Passed checks: `38`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator assessment: `True`
- Operator decision required before freeze: `True`
- Software freeze authorized: `False`
- Registry approval authorized: `False`
- Runtime migration authorized: `False`

## Follow-On Freeze Ceremony
- Artifact kind: `POSITION_SWING_CANONICAL_DATASET_FROZEN`
- Freeze status: `POSITION_SWING_CANONICAL_DATASET_FROZEN`
- Frozen semantic digest: `d95b61fd857eec3271fd6172225ad2efc9cafc78726b55eef666f05d183147f8`
- Freeze checklist: `55` total / `55` passed / `0` failed / `0` blockers.
- The review package remains source evidence for the POSITION_SWING canonical dataset freeze.
- The follow-on freeze did not create POSITION_SWING registry approval, registry eligibility, runtime authorization, Strategy use authorization, predictive-usefulness acceptance, or profitability acceptance.

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- swing_canonical_dataset_frozen: `True`
- swing_registry_approval_created: `True`
- swing_registry_eligibility: `True`
- position_swing_canonical_dataset_frozen: `False`
- position_swing_registry_approval_created: `False`
- position_swing_registry_eligibility: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows were regenerated.
- No identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No `POSITION_SWING_CANONICAL_DATASET_FROZEN` artifact was created.
- No `POSITION_SWING_REGISTRY_APPROVED` artifact was created.
- No registry/runtime eligibility or Strategy runtime migration occurred.
- No predictive-usefulness or profitability acceptance occurred.

## Next Step
- POSITION_SWING registry approval candidate.
