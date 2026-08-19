# MarketFlow Predictive Usefulness Reassessment Using Redesigned Evidence v1 Plan

## Purpose

Create an offline, digest-bound, research-only reassessment of reviewed predictive evidence from the redesigned-label path. The reassessment classifies the evidence conservatively and prepares only a future acceptance-readiness review gate. It does not accept predictive usefulness.

## Source Predictive Evidence Results Review

- Source artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS` / `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY`.
- Bind results-review digest `90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed`.
- Bind execution digest `8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b` and matrix digest `275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad`.
- Treat reviewed results as immutable source evidence; do not rerun execution, recompute metrics, or train models.

## Dataset And Universe

- Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, and `2022-01-01` through `2025-12-31`.
- Preserve 11,946 records and exact ticker order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Preserve META at 913 records and every other ticker at 1,003.
- Bind canonical, registry, redesigned-label, feature, matrix, execution, approval, and results-review digests.

## Evidence Summary

- Preserve reviewed majority/cross-sectional/local OOS accuracy of `0.58626033 / 0.58935950 / 0.58626033`.
- Preserve cross-sectional/local accuracy deltas versus majority of `0.00309917 / 0.00000000`.
- Preserve reviewed macro F1 and Brier values, four walk-forward folds, the 2025 OOS holdout, and 34,848 evaluated rows.
- Preserve leakage `PASS`, zero failed controls, and unavailable optional tree/ensemble model families.

## Reassessment Domains

Cover evidence, dataset, label, feature, matrix, chronological split, walk-forward, OOS, model, metric, calibration, leakage, per-ticker, META-awareness, acceptance, profitability, and runtime domains. Every domain remains research-only, non-actionable, and explicitly not acceptance evidence.

## Classification Policy

- Classify the signal as `WEAK_TO_MODEST_MIXED`.
- Treat the small cross-sectional edge as research evidence, not acceptance evidence.
- Record that the local model matches the majority baseline.
- Require future acceptance-readiness review for stability and calibration.
- Recommend `DO_NOT_ACCEPT_PREDICTIVE_USEFULNESS_AT_REASSESSMENT_STAGE`.

## Future Chain

1. Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.
2. Predictive Usefulness Acceptance Candidate, only if readiness passes.
3. Predictive Usefulness Acceptance Ceremony, only if separately approved.
4. Profitability review chain, if separately required.
5. Runtime migration chain, if ever separately authorized.

## Future Gates

- `predictive_usefulness_acceptance_readiness_using_redesigned_evidence`
- `predictive_usefulness_acceptance_candidate_if_ready`
- `predictive_usefulness_acceptance_ceremony_if_approved`
- `profitability_review_chain_if_required`
- `runtime_migration_chain_if_ever_authorized`

## Risk Controls

The reassessment cannot accept usefulness or profitability, create an acceptance candidate, authorize runtime/strategy/paper/broker activity, generate recommendations, rerun predictive evidence, retrain models, recompute metrics, mutate source outputs, or repair META's limitation. All outputs remain research-only.

## Non-Goals And Guardrails

- No provider calls, `.env` inspection, live transport, market-data acquisition, dataset/label/feature regeneration, predictive execution, metric computation, training, scoring, recommendation, acceptance, profitability, runtime, or broker/IBKR changes.
- No automatic stitching and no tracked `.marketflow` artifacts.
- Reassessment readiness is not predictive-usefulness acceptance readiness or acceptance.

## Next Task

- `Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1` remains future and separately gated.
