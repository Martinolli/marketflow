# MarketFlow POSITION_SWING Canonical Dataset v1 Plan

## Purpose
- Create a candidate-only POSITION_SWING canonical dataset from verified frozen acquisition source rows.
- Preserve the authority boundary: this candidate does not freeze the dataset, approve registry eligibility, activate runtime use, authorize Strategy use, or accept predictive usefulness/profitability.

## Prerequisite Frozen Acquisition Generation
- Required source: `.marketflow\frozen_acquisition_sources\AAPL\2022_2025\AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv`
- Required normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Required acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Required materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- Source row digest must be verified before deriving POSITION_SWING bars.
- Missing or mismatched source rows must fail closed without fabricating bars.

## POSITION_SWING Bar Rule
- Dataset profile: `POSITION_SWING`
- Dataset bar rule: `RTH_FULL_SESSION_1D`
- Source ticker: `AAPL`
- Source range: `2022-01-01` through `2025-12-31`
- Source interval: adjusted 15-minute frozen acquisition rows
- RTH inclusion rule: `calendar_open <= source timestamp < calendar_close`
- Rows starting exactly at market close are excluded from RTH.

## Full-Session Aggregation Logic
- Full ordinary RTH session length: `390` minutes
- 15-minute RTH rows per full session: `26`
- POSITION_SWING bars per full session: `1`
- Source rows per POSITION_SWING bar: `26`
- Bar open: first source row open
- Bar high: max source row high
- Bar low: min source row low
- Bar close: last source row close
- Bar volume: sum source row volume
- Bar transactions: sum source row transactions when available
- Bar VWAP: volume-weighted when source VWAP and volume are available, otherwise `null`

## Special-Session Policy
- full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D: `True`
- special_sessions_excluded_from_position_swing_bars: `True`
- special_sessions_recorded_in_exclusion_inventory: `True`
- Special or early-close sessions are excluded from POSITION_SWING bars and inventoried.
- Excluded special sessions are not provider defects.

## 2025-01 Cross-Check
- Expected full ordinary sessions: `20`
- Expected source RTH rows: `520`
- Expected POSITION_SWING bars: `20`
- Candidate result: `PASSED`

## Current Candidate Status
- Artifact kind: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916`
- Dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- Dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- POSITION_SWING bar count: `994`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`

## Candidate-Only Boundary
- position_swing_canonical_dataset_frozen: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- provider_requests_made: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not refresh identity, calendar, split, dividend, acquisition, SWING, or registry evidence.
- Do not create `POSITION_SWING_CANONICAL_DATASET_FROZEN`.
- Do not create `POSITION_SWING_REGISTRY_APPROVED`.
- Do not approve registry/runtime eligibility.
- Do not modify Strategy runtime behavior.
- Do not accept predictive usefulness or profitability.
- Do not commit generated dataset CSVs or manifests.

## Next Tasks
1. POSITION_SWING operator review package.
2. POSITION_SWING canonical dataset freeze.
3. POSITION_SWING registry approval candidate/review/ceremony.
4. Runtime migration planning.
