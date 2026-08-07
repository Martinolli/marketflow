# MarketFlow Acquisition Per-Session Reconciliation Diagnostics Status

## Scope
- Artifact kind: `ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS`
- Diagnostics status: `ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA`
- Source acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Source monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Target month count: `9`
- Target months: `2022-11, 2023-07, 2023-11, 2024-07, 2024-11, 2024-12, 2025-07, 2025-11, 2025-12`
- Row-level source available: `False`
- Session diagnostics available: `False`
- Blocked reason: `ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE`
- Instrumentation added for future generation runs: `True`
- 2025-01 cross-check status: `PASSED_FROM_MONTHLY_TRIAGE`
- Acquisition operator review: `BLOCKED`

## Session Summary
- Total sessions evaluated: `0`
- Reconciled sessions: `0`
- Non-reconciled sessions: `0`
- Missing-bar sessions: `0`
- Extra-bar sessions: `0`
- Calendar-duration review sessions: `0`
- Blocker count: `0`
- High count: `0`
- Issue category summary: `{}`
- Issue severity summary: `{}`

## Blocked Detail
- Row-level normalized source artifacts for the target months were not available in the local ignored runtime artifacts.
- No per-session rows were fabricated from monthly totals.
- Acquisition review remains blocked until row-level per-session diagnostics can be generated and reviewed.

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

## Non-Goals
- No provider refresh was performed.
- No full acquisition generation rerun was performed.
- No API key, raw provider payload, generated bars, personal, broker, or tax data is included.
- No acquisition-generation freeze was created.
- No canonical, registry, runtime, predictive, or profitability approval occurred.

## Next Task Recommendation
- Run a separately gated generation that emits row-level per-session reconciliation diagnostics.
