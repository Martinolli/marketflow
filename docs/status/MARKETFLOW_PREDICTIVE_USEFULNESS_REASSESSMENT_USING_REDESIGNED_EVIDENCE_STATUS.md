# MarketFlow Predictive Usefulness Reassessment Using Redesigned Evidence Status

## Reassessment Package

- Artifact/status: `PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE` / `PREDICTIVE_USEFULNESS_REASSESSMENT_USING_REDESIGNED_EVIDENCE_PACKAGE_READY`.
- Schema: `predictive_usefulness_reassessment_using_redesigned_evidence_v1`.
- Reassessment digest: `32cd6e52de25584df7b54866034fbb378fad8dfe1e3f1656994dbd554d1b4985`.
- Checklist: `51 / 51` passed, `0` failed, `0` blockers.
- The package is offline, research-only, non-actionable, and requires operator review.

## Source Results Review And Bound Evidence

- Source results-review artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS` / `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY`.
- Results-review digest: `90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed`.
- Execution digest: `8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b`.
- Feature/label matrix digest: `275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad`.
- Feature values, redesigned-label values, research registry, and canonical records remain bound to their reviewed digests.
- No source output was regenerated, rerun, recomputed, retrained, or mutated.

## Dataset And Universe

- Dataset/profile/timeframe/range: `expanded_universe_canonical_dataset_v1` / `RTH_FULL_SESSION_1D` / `1d` / `2022-01-01` through `2025-12-31`.
- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Canonical records: `11946`; META remains `913` and every other ticker remains `1003`.
- Each ticker has a deterministic reassessment digest. META carries `PRESERVE_META_LIMITATION_IN_PREDICTIVE_USEFULNESS_REASSESSMENT`.

## Reviewed Evidence Summary

- Majority OOS accuracy/macro F1/Brier: `0.58626033 / 0.21557412 / 0.04867526`.
- Ticker cross-sectional OOS accuracy/macro F1/Brier: `0.58935950 / 0.28155252 / 0.04831065`.
- Regularized local-model OOS accuracy/macro F1/Brier: `0.58626033 / 0.21557412 / 0.04867526`.
- Cross-sectional and local accuracy deltas versus majority: `0.00309917 / 0.00000000`.
- Four chronological walk-forward folds and the 2025 OOS holdout with `34848` evaluated rows remain the reviewed evidence.
- Leakage remains `PASS` with `0` failed controls.
- Optional tree and ensemble model families remain `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`.

## Reassessment Domains And Classification

- Seventeen domains cover integrity, scope, stability, baseline/model evidence, metrics, calibration, leakage, per-ticker consistency, META awareness, and all authority boundaries.
- Reassessment classification: `COMPLETED_RESEARCH_ONLY`.
- Predictive signal classification: `WEAK_TO_MODEST_MIXED`.
- Cross-sectional baseline classification: `SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE`.
- Local-model classification: `MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE`.
- Stability/calibration require a separate acceptance-readiness review.
- Acceptance recommendation: `DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE`.

## Authority Boundary

- `predictive_usefulness_reassessment_created`, `predictive_usefulness_reassessment_ready`, and readiness for a future acceptance-readiness review are true.
- The reassessment does not accept predictive usefulness and does not create an acceptance-readiness review or acceptance candidate.
- Predictive usefulness and profitability remain `not accepted`.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- New strategy scoring and trade recommendations remain false.
- No provider request, market-data acquisition, regeneration, predictive-evidence rerun, metric recomputation, model training, runtime, broker, or trading action occurred.

## Next Gate

- `Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1` remains future and separately gated.
- An acceptance candidate is permitted only if that future readiness review passes.
