# MarketFlow Signal or Feature Generation Candidate Status

## Candidate

- Artifact: `MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_V1`.
- Status: `MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `SIGNAL_OR_FEATURE_GENERATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION`.
- Deterministic candidate digest: `e9369666fdc7efc35321d6c3c028071b012e139b84c8633177946ab842201f59`.
- Checklist: 82 / 82 passed, 0 failed, 0 blockers.
- The candidate is offline, digest-bound, research-only, non-actionable, and requires operator review.

## Source Target Results Review

- Source results-review digest: `41afa9e7159f2788f8dce3c44343c2058414fb51efb95b5d6714246ab866e47c`.
- Source execution digest: `fa15e57e4d767c48578e124cd0c00155560d7ee9a3c275b5c5d2ab6065b44533`.
- Source output-binding digest: `f6d0432538c23173bef59c81f93c7834ab7c5c933c5bcf039bb4cf0347ffb257`.
- Source target-values digest: `61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119`.
- Source approval digest: `df3ee8758ca86a04f944ed1a46ede444693833009c99692e490f6cae5e21414b`.
- The complete upstream strategy-charter, expectancy-objective, target-candidate, predictive-evidence, matrix, feature-values, redesigned-label, registry, and records digest chain is bound.
- The source results review remains the evidence authority. It was not rerun, and its ignored outputs were not modified.

## Dataset and Target Basis

- Dataset/profile/timeframe/range: `expanded_universe_canonical_dataset_v1` / `RTH_FULL_SESSION_1D` / `1d` / 2022-01-01 through 2025-12-31.
- Ordered universe: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- Records: 11,946 total; every non-META ticker remains 1,003 and META remains exactly 913.
- Records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Selected package/path: `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET` / `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`.
- Target basis: 15 profiles, 179,190 rows, 177,090 available, and 2,100 unavailable.
- Each non-META ticker preserves 15,045 target rows: 14,870 available and 175 unavailable.
- META preserves 13,695 target rows: 13,520 available and 175 unavailable. Its reduced history is not repaired or inferred.

## Candidate Design

- Philosophy: prepare future historical predictors for the reviewed expectancy targets using only current or prior history, never target values, target classes, forward returns, strategy scores, or recommendations as features.
- Primary question: which history-only price, volume, relative-strength, volatility, regime, and abstention-context features should be generated first?
- Ten proposed signal families cover trend structure, volume-price behavior, close location/spread, effort-result behavior, relative strength, volatility state, breakout/pullback structure, absorption/distribution, regime context, and noise/abstention filtering.
- Ten proposed feature families cover price/range, volume/liquidity, volume-price relationships, volatility/ATR, momentum/trend, relative strength/ranking, regime context, abstention/noise, metadata-only target alignment, and data-quality/META flags.
- Recommended package: `PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET`, recommended for operator review and not selected.
- Supporting package: `PACKAGE_REGIME_CONTEXT_SIGNAL_SET`, available for operator review and not selected.
- The candidate defines 17 feature groups, 10 no-peek and target-separation rules, 10 planned quality checks, and 10 planned-but-not-generated outputs.
- All 12 ticker entries bind the source review and target-values digests and carry deterministic per-ticker candidate digests.

## Authority Boundary and Next Gate

- Candidate creation/readiness and readiness for its operator review are true.
- Selection, approval, authorization, and generation remain false.
- No signal values, feature values, feature-label matrix rows, backtests, models, metrics, strategy scores, or recommendations were created.
- Predictive usefulness and profitability remain not accepted.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, market-data acquisition, dataset regeneration, target-generation rerun, target-results-review rerun, runtime activation, or trading action occurred.
- Follow-on Signal or Feature Generation Candidate Operator Review v1 is implemented as an offline, digest-bound, review-only package.
- This candidate remains the source evidence; the review does not select or approve either feature package.
- The review does not generate signal values, feature values, matrix rows, backtests, models, metrics, recommendations, predictive-usefulness or profitability acceptance, or runtime authority.
- Signal or Feature Generation Approval v1 remains future work only if an operator separately selects a package.
