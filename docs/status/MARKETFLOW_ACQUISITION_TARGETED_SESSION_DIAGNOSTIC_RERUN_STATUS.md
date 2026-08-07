# MarketFlow Acquisition Targeted Session Diagnostic Rerun Status

## Scope
- Artifact kind: `ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN`
- Rerun status: `ACQUISITION_TARGETED_SESSION_DIAGNOSTIC_RERUN_COMPLETE`
- Acquisition operator review status: `READY_AFTER_TRIAGE`
- Target months: `2022-11, 2023-07, 2023-11, 2024-07, 2024-11, 2024-12, 2025-07, 2025-11, 2025-12`
- Endpoint used: `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}`
- Request mode: `LIVE_PROVIDER_REQUEST`
- Expected target chunks: `9`
- Completed target chunks: `9`
- Failed target chunks: `0`
- All 9 monthly mismatches explained: `True`

## Per-Month Results
| month | provider_status | raw_rows | normalized_rows | rth_rows | extended_hours_rows | monthly_status | legacy_delta | session_expected | session_observed | explanation |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 2022-11 | OK | 1321 | 1321 | 534 | 787 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 534 | 534 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2023-07 | OK | 1253 | 1253 | 508 | 745 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 508 | 508 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2023-11 | OK | 1310 | 1310 | 534 | 776 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 534 | 534 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2024-07 | OK | 1382 | 1382 | 560 | 822 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 560 | 560 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2024-11 | OK | 1250 | 1250 | 508 | 742 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 508 | 508 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2024-12 | OK | 1312 | 1312 | 534 | 778 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 534 | 534 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2025-07 | OK | 1383 | 1383 | 560 | 823 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 560 | 560 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2025-11 | OK | 1186 | 1186 | 482 | 704 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 482 | 482 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |
| 2025-12 | OK | 1357 | 1357 | 560 | 797 | RTH_SOURCE_ROWS_NOT_RECONCILED | 14 | 560 | 560 | EXPLAINED_BY_SPECIAL_SESSION_EXPECTATION |

## Session Diagnostics
- Issue category summary: `{"RECONCILED":188}`
- Issue severity summary: `{"INFO":188}`
- Non-reconciled session count: `0`

## Non-Reconciled Sessions
- None identified in compact per-session diagnostics.

## Digests
- Targeted chunk manifest digest: `aac91eaa82859c88c29cfcef07c9f2f2f8da68d198a17572affc2cd3a0a9239c`
- Targeted provider raw response digest: `041c7da634d43463c8ce37a6b3da7aa1bf77c558f02aa18a2b820f290368dc1f`
- Targeted normalized rows digest: `b5a82e3d8266a55fa520a2c2a5c01d3bd15ccbe27db806cfa0e4b21225e07c28`
- Targeted monthly reconciliation digest: `f002b833511b102e8136d00354dbe6c410abd30a947242e881e44e12d3cc9191`
- Per-session diagnostics digest: `f810bfd3fcb1d2056bbf5ba0cff8b1aa4276119721c697ce17eaef6bab069faa`
- Targeted diagnostic receipt digest: `82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8`

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Safeguards
- API key stored: `False`
- Raw provider payload stored: `False`
- Generated bars stored: `False`
- No acquisition-generation freeze was created.
- No canonical, registry, runtime, predictive, or profitability approval occurred.
- No full 48-month acquisition rerun was performed.

## Next Task Recommendation
- Acquisition operator review may proceed after human review of targeted triage evidence.
