# MarketFlow SWING Canonical Dataset Candidate Status

## Candidate
- Artifact kind: `SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `SWING_CANONICAL_DATASET_REQUIRES_FROZEN_ACQUISITION_ROWS`
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Candidate digest: `f2832bdae6a3f7cb64cd17c891a426d123028bf7629236e8d07e60392a66392a`

## Source Rows
- Source row data available: `False`
- Source row digest matched: `False`
- Source row digest verification mode: `MISSING_SOURCE_ROW_ARTIFACT`
- Normalized source rows digest bound: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Source rows: `63804 total / 25970 RTH / 37834 extended-hours / 0 unknown`

## Frozen Acquisition Binding
- Acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Acquisition receipt digest: `63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed`
- Targeted diagnostic receipt digest: `82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8`
- Per-session diagnostics digest: `f810bfd3fcb1d2056bbf5ba0cff8b1aa4276119721c697ce17eaef6bab069faa`

## SWING Dataset Summary
- SWING bar count: `0`
- Source RTH rows consumed: `0`
- Source RTH rows excluded: `25970`
- Full sessions used: `0`
- Special sessions excluded: `0`
- Invalid sessions: `0`
- Dataset digest: `None`
- Dataset manifest digest: `None`

## 2025-01 SWING Cross-Check
- Expected full ordinary sessions: `20`
- Expected source RTH rows: `520`
- Expected SWING bars: `40`
- Actual SWING bars: `None`
- Result: `UNVALIDATED_MISSING_SOURCE_ROWS`

## Special-Session Policy
- full_ordinary_sessions_only_for_RTH_HALF_SESSION_195M: `True`
- special_sessions_excluded_from_swing_bars: `True`
- special_sessions_recorded_in_exclusion_inventory: `True`
- Special-session count: `0`
- Special-session exclusion count: `0`
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
- Persist the frozen normalized acquisition source rows under ignored `.marketflow` output, then rebuild this candidate for SWING operator review.
