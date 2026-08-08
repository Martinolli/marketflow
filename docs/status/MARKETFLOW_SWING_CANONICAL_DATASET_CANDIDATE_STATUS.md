# MarketFlow SWING Canonical Dataset Candidate Status

## Candidate
- Artifact kind: `SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Candidate digest: `1bb6e2d7354c30c88e55738e0c549769d9daae678b47899a776de337571cf671`
- Candidate receipt digest: `e18f3a25c7a3e6ffd04ea478e3f6f5402805fe9b72d53e17e8adf7d4057f495c`

## Source Rows
- Source row data available: `True`
- Source row digest matched: `True`
- Source row digest verification mode: `MATCHED_FROZEN_DIGEST`
- Source rows path: `.marketflow/frozen_acquisition_sources/AAPL/2022_2025/AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv`
- Normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Actual normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Source rows: `63804 total / 25970 RTH / 37834 extended-hours / 0 unknown`

## Frozen Acquisition Binding
- Acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Acquisition receipt digest: `63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`

## SWING Dataset Summary
- SWING bar count: `1988`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special sessions excluded: `9`
- Special session rows excluded: `126`
- Invalid sessions: `0`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Ignored dataset output path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- Ignored manifest output path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json`

## 2025-01 SWING Cross-Check
- Expected full ordinary sessions: `20`
- Expected source RTH rows: `520`
- Expected SWING bars: `40`
- Actual SWING bars: `40`
- Result: `PASSED`

## Special-Session Policy
- full_ordinary_sessions_only_for_RTH_HALF_SESSION_195M: `True`
- special_sessions_excluded_from_swing_bars: `True`
- special_sessions_recorded_in_exclusion_inventory: `True`
- Special-session count: `9`
- Special-session exclusion count: `9`
- Special-session exclusion reason: `SPECIAL_SESSION_EXCLUDED_BY_CONSERVATIVE_FULL_SESSION_ONLY_POLICY`
- Excluded special sessions are not provider data defects.

## Dividend Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`
- Source adjusted data used: `True`

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- canonical_dataset_frozen: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Guardrails
- Created offline: `True`
- Provider requests made: `False`
- No provider requests were made.
- No canonical dataset freeze was created.
- No canonical eligibility, registry eligibility, or strategy runtime migration approval occurred.
- No predictive usefulness or profitability acceptance occurred.
- No raw OHLCV rows or provider payloads are included in this document.

## Next Task Recommendation
- Prepare the SWING operator review package; a separate operator freeze ceremony remains required before any canonical freeze, registry approval, or runtime use.
