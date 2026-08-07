# MarketFlow Acquisition Frozen Source Rows Materialization Status

## Materialization
- Artifact kind: `ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZATION`
- Materialization status: `ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED`
- Materialization mode: `LIVE_RECONSTRUCTION_OF_FROZEN_NORMALIZED_ROWS`
- Local matching rows already available before materialization: `False`
- Live materialization ran: `True`
- Provider response injected: `False`
- Blocked reason: `None`

## Frozen Acquisition Binding
- Source acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Expected normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Actual normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Digest match result: `True`

## Row Summary
- Row count: `63804`
- RTH row count: `25970`
- Extended-hours row count: `37834`
- Unknown row count: `0`
- Out-of-calendar row count: `0`
- Materialized rows path: `.marketflow/frozen_acquisition_sources/AAPL/2022_2025/AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv`
- Materialization manifest path: `.marketflow/frozen_acquisition_sources/AAPL/2022_2025/AAPL_15m_adjusted_2022_2025_source_rows_manifest.json`

## Materialization Digests
- Chunk manifest digest: `8a4bf37f501fb7da5ea23e04d5ebe90da2cdfda1bf9e06e55e4c459be53fa374`
- Provider raw response digest from materialization run: `afaa5818fbc6f8db47dcc9d031da0a45a835e8437a09ff331ac54e06d066efd6`
- Monthly reconciliation digest from materialization run: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Monthly reconciliation digest matched frozen: `True`
- Monthly reconciliation mismatch explanation: `None`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- Materialization status digest: `f65e0fae7aedaa9a91c1250501684a9f3c00433b6931c01b8d31094d1b224bd7`

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Guardrails
- API key stored: `False`
- Raw provider payload stored: `False`
- New acquisition authority created: `False`
- Frozen acquisition digest replaced: `False`
- Acquisition generation frozen created: `False`
- SWING canonical dataset frozen created: `False`
- Canonical dataset approved: `False`
- Registry eligible: `False`
- No raw/generated OHLCV rows are included in this document.
- No API key, personal, broker, or tax information is included in this document.

## Next Task Recommendation
- SWING candidate should be rerun using verified materialized frozen source rows.
