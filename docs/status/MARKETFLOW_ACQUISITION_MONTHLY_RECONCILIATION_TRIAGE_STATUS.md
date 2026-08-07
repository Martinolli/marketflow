# MarketFlow Acquisition Monthly Reconciliation Triage Status

## Scope
- Artifact kind: `ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE`
- Triage status: `ACQUISITION_MONTHLY_RECONCILIATION_TRIAGE_BLOCKS_ACQUISITION_REVIEW`
- Source acquisition candidate digest: `5b1f7507c4549b0cd590737e37571cd0ff18f5710c5bfb853bd04aeec6b3f1cb`
- Source monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Total months: `48`
- Reconciled months: `39`
- Non-reconciled months: `9`
- Non-reconciled month list: `2022-11, 2023-07, 2023-11, 2024-07, 2024-11, 2024-12, 2025-07, 2025-11, 2025-12`
- Issue category summary: `{"INSUFFICIENT_DETAIL":9,"RECONCILED":39}`
- Issue severity summary: `{"HIGH":9,"INFO":39}`
- 2025-01 cross-check status: `PASSED`
- Acquisition operator review: `BLOCKED`

## Triage Table
| month | status | normalized_rows | rth_rows | extended_hours_rows | expected_rth_rows | validated_rth_rows | rth_delta | full_sessions | incomplete_sessions | swing_bars | position_bars | category | severity | operator_review | provider_recheck | calendar_review | algorithm_review | reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| 2022-01 | RTH_SOURCE_ROWS_RECONCILED | 1280 | 520 | 760 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-02 | RTH_SOURCE_ROWS_RECONCILED | 1211 | 494 | 717 | 494 | 494 | 0 | 19 | None | 38 | 19 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-03 | RTH_SOURCE_ROWS_RECONCILED | 1470 | 598 | 872 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-04 | RTH_SOURCE_ROWS_RECONCILED | 1278 | 520 | 758 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-05 | RTH_SOURCE_ROWS_RECONCILED | 1343 | 546 | 797 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-06 | RTH_SOURCE_ROWS_RECONCILED | 1342 | 546 | 796 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-07 | RTH_SOURCE_ROWS_RECONCILED | 1280 | 520 | 760 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-08 | RTH_SOURCE_ROWS_RECONCILED | 1470 | 598 | 872 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-09 | RTH_SOURCE_ROWS_RECONCILED | 1344 | 546 | 798 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-10 | RTH_SOURCE_ROWS_RECONCILED | 1343 | 546 | 797 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2022-11 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1321 | 534 | 787 | 520 | 534 | 14 | 20 | None | 40 | 20 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2022-12 | RTH_SOURCE_ROWS_RECONCILED | 1342 | 546 | 796 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-01 | RTH_SOURCE_ROWS_RECONCILED | 1280 | 520 | 760 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-02 | RTH_SOURCE_ROWS_RECONCILED | 1216 | 494 | 722 | 494 | 494 | 0 | 19 | None | 38 | 19 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-03 | RTH_SOURCE_ROWS_RECONCILED | 1471 | 598 | 873 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-04 | RTH_SOURCE_ROWS_RECONCILED | 1211 | 494 | 717 | 494 | 494 | 0 | 19 | None | 38 | 19 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-05 | RTH_SOURCE_ROWS_RECONCILED | 1400 | 572 | 828 | 572 | 572 | 0 | 22 | None | 44 | 22 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-06 | RTH_SOURCE_ROWS_RECONCILED | 1339 | 546 | 793 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-07 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1253 | 508 | 745 | 494 | 508 | 14 | 19 | None | 38 | 19 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2023-08 | RTH_SOURCE_ROWS_RECONCILED | 1469 | 598 | 871 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-09 | RTH_SOURCE_ROWS_RECONCILED | 1280 | 520 | 760 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-10 | RTH_SOURCE_ROWS_RECONCILED | 1405 | 572 | 833 | 572 | 572 | 0 | 22 | None | 44 | 22 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2023-11 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1310 | 534 | 776 | 520 | 534 | 14 | 20 | None | 40 | 20 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2023-12 | RTH_SOURCE_ROWS_RECONCILED | 1266 | 520 | 746 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-01 | RTH_SOURCE_ROWS_RECONCILED | 1343 | 546 | 797 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-02 | RTH_SOURCE_ROWS_RECONCILED | 1275 | 520 | 755 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-03 | RTH_SOURCE_ROWS_RECONCILED | 1280 | 520 | 760 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-04 | RTH_SOURCE_ROWS_RECONCILED | 1402 | 572 | 830 | 572 | 572 | 0 | 22 | None | 44 | 22 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-05 | RTH_SOURCE_ROWS_RECONCILED | 1401 | 572 | 829 | 572 | 572 | 0 | 22 | None | 44 | 22 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-06 | RTH_SOURCE_ROWS_RECONCILED | 1215 | 494 | 721 | 494 | 494 | 0 | 19 | None | 38 | 19 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-07 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1382 | 560 | 822 | 546 | 560 | 14 | 21 | None | 42 | 21 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2024-08 | RTH_SOURCE_ROWS_RECONCILED | 1405 | 572 | 833 | 572 | 572 | 0 | 22 | None | 44 | 22 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-09 | RTH_SOURCE_ROWS_RECONCILED | 1277 | 520 | 757 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-10 | RTH_SOURCE_ROWS_RECONCILED | 1461 | 598 | 863 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2024-11 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1250 | 508 | 742 | 494 | 508 | 14 | 19 | None | 38 | 19 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2024-12 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1312 | 534 | 778 | 520 | 534 | 14 | 20 | None | 40 | 20 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2025-01 | RTH_SOURCE_ROWS_RECONCILED | 1277 | 520 | 757 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-02 | RTH_SOURCE_ROWS_RECONCILED | 1215 | 494 | 721 | 494 | 494 | 0 | 19 | None | 38 | 19 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-03 | RTH_SOURCE_ROWS_RECONCILED | 1344 | 546 | 798 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-04 | RTH_SOURCE_ROWS_RECONCILED | 1343 | 546 | 797 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-05 | RTH_SOURCE_ROWS_RECONCILED | 1343 | 546 | 797 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-06 | RTH_SOURCE_ROWS_RECONCILED | 1279 | 520 | 759 | 520 | 520 | 0 | 20 | None | 40 | 20 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-07 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1383 | 560 | 823 | 546 | 560 | 14 | 21 | None | 42 | 21 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2025-08 | RTH_SOURCE_ROWS_RECONCILED | 1339 | 546 | 793 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-09 | RTH_SOURCE_ROWS_RECONCILED | 1341 | 546 | 795 | 546 | 546 | 0 | 21 | None | 42 | 21 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-10 | RTH_SOURCE_ROWS_RECONCILED | 1470 | 598 | 872 | 598 | 598 | 0 | 23 | None | 46 | 23 | RECONCILED | INFO | False | False | False | False | Monthly RTH row count reconciles against the available calendar expectation. |
| 2025-11 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1186 | 482 | 704 | 468 | 482 | 14 | 18 | None | 36 | 18 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |
| 2025-12 | RTH_SOURCE_ROWS_NOT_RECONCILED | 1357 | 560 | 797 | 546 | 560 | 14 | 21 | None | 42 | 21 | INSUFFICIENT_DETAIL | HIGH | True | True | True | True | The committed status document identifies a monthly RTH mismatch but lacks per-session detail for root-cause classification. |

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
- No API key, raw provider payload, generated bars, personal, broker, or tax data is included.
- No acquisition-generation freeze was created.
- No canonical, registry, runtime, predictive, or profitability approval occurred.

## Follow-On Per-Session Diagnostics
- Per-session diagnostics status: `ACQUISITION_PER_SESSION_DIAGNOSTICS_BLOCKED_MISSING_ROW_LEVEL_DATA`
- Status document: `docs/status/MARKETFLOW_ACQUISITION_PER_SESSION_RECONCILIATION_DIAGNOSTICS_STATUS.md`
- Blocked reason: `ROW_LEVEL_NORMALIZED_SOURCE_DATA_NOT_AVAILABLE`
- Acquisition review remains blocked until row-level per-session evidence is generated and reviewed.

## Next Task Recommendation
- Build a per-session reconciliation diagnostic from ignored local runtime artifacts or a separately gated rerun before acquisition operator review.
