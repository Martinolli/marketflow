# MarketFlow Additional Predictive Evidence Using Redesigned Labels v1 Plan

## Purpose

Create an offline, digest-bound execution candidate for future additional predictive evidence using reviewed redesigned labels and generated feature values. This stage is candidate-only: it creates no approval, authorization, execution, metrics, training, acceptance, profitability, runtime authority, or recommendations.

## Source Feature Generation Results Review

- Source artifact/status: `FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS` / `FEATURE_GENERATION_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY`.
- Source review digest: `e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3`.
- Feature-generation execution and feature-values digests remain `d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f` and `63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1`.

## Dataset And Universe

- Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, and `2022-01-01` through `2025-12-31`.
- Preserve `11946` records and exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Preserve META at `913` records and every other ticker at `1003`.
- Bind records digest `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Source Redesigned Label Profile

- Preserve `143352` rows, `142200` available values, `1152` unavailable values, `10` families, `7` threshold strategies, and `5` horizon strategies.
- Bind label-values digest `2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f`.

## Source Feature Profile

- Preserve `12` reviewed outputs, `10` feature families, `17` groups, `16` schema fields, and `203082` rows.
- Preserve `190848` available and `12234` unavailable feature values.
- Bind feature-values digest `63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1`.

## Source Inputs

Use only the reviewed canonical dataset, redesigned-label review and values, feature-generation review and values, family/group/schema/alignment/quality reports, per-ticker summary, and META handling report. Every source remains `SOURCE_REVIEWED_NOT_REGENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Planned Feature And Label Matrix

- Matrix status: `PLANNED_NOT_GENERATED`.
- Bind feature-values, redesigned-label-values, and canonical-record digests.
- Plan `TICKER_DATE_HORIZON_AND_LABEL_FAMILY_ALIGNMENT_PLANNED` without executing the join or creating a matrix.

## Planned Execution Activities

Plan binding, matrix candidacy, alignment verification, chronological splits, walk-forward and OOS protocols, baseline/model comparisons, metric computation, calibration/stability, leakage/quality, per-ticker/cross-sectional review, and an operator summary. Every activity remains `PLANNED_NOT_EXECUTED`, unauthorized, research-only, and non-actionable.

## Planned Splits

- Training: `2022-01-01 through 2023-12-31`.
- Validation: `2024-01-01 through 2024-12-31`.
- OOS: `2025-01-01 through 2025-12-31`.
- Shuffling is prohibited, chronological order is required, and the embargo policy is `PLANNED_FOR_OPERATOR_REVIEW`.

## Planned Model And Baseline Families

Plan four reference baselines plus regularized-linear, optional tree, optional ensemble, per-ticker comparison, and global cross-sectional comparison families. All nine remain `PLANNED_NOT_EVALUATED`; training and metric computation are unauthorized and unperformed.

## Planned Metric Families

Plan accuracy, macro precision/recall/F1, confusion matrix, Brier score, calibration, class balance, walk-forward stability, and baseline-outperformance delta. Every metric remains `PLANNED_NOT_COMPUTED` and unauthorized.

## Future Chain And Gates

Proceed only through a separate candidate operator review, possible execution approval, execution, results review, usefulness reassessment, acceptance-readiness review, possible acceptance candidate, possible profitability review, and possible runtime migration. Each stage remains a separate future gate.

## Risk Controls

The candidate cannot execute predictive evidence, train models, recompute metrics, accept usefulness or profitability, authorize runtime/strategy/paper/broker activity, or generate recommendations. The frozen dataset, redesigned-label outputs, feature outputs, unavailable values, and META limitation must remain unchanged. All planned outputs remain research-only.

## Non-Goals And Guardrails

- No provider calls, market-data acquisition, `.env` inspection, live transport, dataset/label/feature regeneration, matrix generation, predictive execution, metrics, training, scoring, recommendations, acceptance, profitability, runtime activation, or broker/IBKR changes.
- No automatic stitching and no tracked `.marketflow` output.
- Candidate creation is not operator review, approval, authorization, or execution.

## Next Task

- `Additional Predictive Evidence Execution Candidate Using Redesigned Labels v1` is complete.
- `Additional Predictive Evidence Execution Candidate Operator Review Package Using Redesigned Labels v1` is implemented and the candidate is reviewed.
- `Additional Predictive Evidence Execution Approval Using Redesigned Labels v1` is completed as the offline, attestation-gated source authority.
- `Additional Predictive Evidence Execution Using Redesigned Labels v1` is implemented and executed research-only with a horizon-aware training embargo.
- Additional predictive-evidence results review remains future and separately gated.
- Predictive-usefulness reassessment remains future and separately gated; usefulness acceptance remains closed.
- Predictive-usefulness acceptance remains closed, profitability remains `not accepted`, and runtime activation remains a future, separate authority chain.
