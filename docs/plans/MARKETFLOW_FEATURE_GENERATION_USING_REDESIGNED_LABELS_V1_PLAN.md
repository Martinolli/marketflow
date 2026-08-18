# MarketFlow Feature Generation Using Redesigned Labels v1 Plan

## Purpose

Prepare an offline, digest-bound feature-generation candidate for operator review. This plan defines future feature design only and creates no feature values, approval, execution, predictive evidence, or downstream authority.

## Source Planning Approval

- Approval artifact: `FEATURE_PREDICTIVE_EVIDENCE_PLANNING_APPROVED_USING_REDESIGNED_LABELS`.
- Approval digest: `6f4c1ce989e76e2b2ee835056e146f362b6d7c70b44bb6fc864f3f125c9dc54d`.
- The approval is source evidence for candidate creation only; it does not authorize feature generation.

## Dataset And Universe

- Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, and `2022-01-01` through `2025-12-31`.
- Preserve `11946` frozen records and exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Preserve META at `913` records and every other ticker at `1003`.
- Bind records digest `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Redesigned Label Profile

- Preserve `11` reviewed outputs, `10` label families, `7` threshold strategies, `5` horizon strategies, `143352` label rows, and `144` family coverage entries.
- Preserve `142200` available and `1152` unavailable label values.
- Bind label-values digest `2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f`.

## Source Inputs

Use only the frozen canonical dataset, reviewed redesigned-label package and its label/coverage/threshold/horizon/availability/per-ticker/META outputs, plus the feature/predictive planning approval. Every input remains `SOURCE_REVIEWED_NOT_REGENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Planned Feature Families And Groups

- `FEATURE_FAMILY_OHLCV_RETURNS_AND_RANGES`: return lags and range features.
- `FEATURE_FAMILY_VOLUME_PRICE_ANALYSIS`: volume effort and price-volume spread features.
- `FEATURE_FAMILY_VOLATILITY_AND_REALIZED_RANGE`: realized-volatility windows.
- `FEATURE_FAMILY_MOMENTUM_AND_TREND`: momentum windows and trend slopes.
- `FEATURE_FAMILY_RELATIVE_STRENGTH_AND_CROSS_SECTIONAL_CONTEXT`: universe-median relative strength and cross-sectional ranks.
- `FEATURE_FAMILY_CALENDAR_AND_SESSION_CONTEXT`: calendar and session-sequence fields.
- `FEATURE_FAMILY_LABEL_ALIGNED_HORIZON_CONTEXT`: label-horizon and label-family alignment flags.
- `FEATURE_FAMILY_QUALITY_MISSINGNESS_AND_META_LIMITATION_FLAGS`: missingness and META-limitation flags.
- `FEATURE_FAMILY_REGIME_AND_INTERACTION_TERMS`: regime interaction candidates.
- `FEATURE_FAMILY_BASELINE_ERROR_CONTEXT`: baseline-error context candidates.

Every family is `PLANNED_READY_FOR_OPERATOR_REVIEW`; every group is `PLANNED_NOT_GENERATED`. Authorization, performance, and feature-value flags remain false.

## Planned Feature Schema Contract

Plan the fields `ticker`, `date`, `record_index_for_ticker`, `window_partition`, `feature_family`, `feature_group`, `feature_name`, `feature_value`, `feature_available`, `availability_reason`, `source_history_window`, `label_family_alignment`, `label_horizon_alignment`, `meta_reduced_record_count_flag`, `research_only`, and `non_actionable`. The contract is `PLANNED_NOT_GENERATED`.

## Planned Alignment Controls

Require history-only features, prohibit future labels and forward returns as predictors, treat thresholds as label metadata unless separately approved, prevent date peeking, preserve chronological splits, avoid threshold refitting, bind redesigned labels by digest, preserve the META limitation, and preserve unavailable label rows. All controls await operator review and remain `NOT_EXECUTED`.

## Planned Quality Checks

Plan digest, universe order, META count, feature-row expectation, null policy, leakage, feature/label alignment, schema-contract, and operator-summary checks. All remain `PLANNED_NOT_EXECUTED`.

## Future Chain And Gates

The chain proceeds only through separate operator review, feature-generation approval, execution, results review, additional predictive-evidence candidacy/approval/execution/results review, usefulness reassessment/readiness, possible acceptance candidacy, possible profitability review, and possible runtime migration. Each stage remains a separate future gate.

## Risk Controls

The candidate cannot generate or authorize features, execute predictive evidence, train models, recompute metrics, accept usefulness or profitability, authorize runtime/strategy/paper/broker activity, or generate recommendations. The frozen dataset, reviewed label outputs, unavailable rows, and META limitation must remain unchanged. All outputs remain research-only.

## Non-Goals And Guardrails

- No provider calls, market-data acquisition, `.env` inspection, live transport, dataset regeneration, label regeneration, feature generation, metrics, training, scoring, recommendations, acceptance, profitability, runtime activation, or broker/IBKR changes.
- No automatic stitching and no tracked `.marketflow` output.
- Candidate creation does not imply approval or execution.

## Next Task

- `Feature Generation Candidate Using Redesigned Labels v1` is complete.
- `Feature Generation Candidate Operator Review Package Using Redesigned Labels v1` is implemented.
- The feature-generation candidate using redesigned labels is reviewed.
- `Feature Generation Approval Using Redesigned Labels v1` is implemented.
- Feature-generation approval is complete and `Feature Generation Execution Using Redesigned Labels v1` is implemented and executed.
- Research-only feature values were created and `Feature Generation Results Review Using Redesigned Labels v1` is implemented.
- An additional predictive-evidence execution candidate remains future work and requires a separate operator-review and approval chain.
- Predictive-evidence execution remains future and separately gated.
- Predictive-usefulness acceptance and profitability remain closed and `not accepted`.
- Runtime activation remains a future, separate authority chain.
