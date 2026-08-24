# MarketFlow Signal or Feature Generation Candidate v1 Plan

## Purpose

Create an offline, digest-bound, research-only candidate for future historical signal or feature generation. This plan creates neither approval nor generated values.

## Source Target Results Review

The source is `MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_RESULTS_REVIEW_PACKAGE`, ready under review digest `41afa9e7159f2788f8dce3c44343c2058414fb51efb95b5d6714246ab866e47c`. Its execution, output-binding, target-values, approval, and full upstream evidence digests are immutable candidate inputs.

## Dataset and Universe

Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily bars from 2022-01-01 through 2025-12-31, 11,946 records, and the exact ordered universe MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT. Preserve META at 913 records and every other ticker at 1,003.

## Candidate Basis

Use reviewed package `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET` and objective path `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`. Preserve 15 target profiles, 179,190 target rows, 177,090 available rows, 2,100 unavailable rows, and target-values digest `61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119`.

## Candidate Philosophy

Prepare history-only signal and feature definitions that may later explain or anticipate the research-only expectancy targets. Target values, target classes, forward outcomes, strategy scores, recommendations, and future data are never predictor inputs. Generation requires a separate operator review, selection, and approval.

## Signal Families

Define, but do not generate, trend structure; volume-price analysis; close location and spread; effort-result behavior; relative strength; volatility compression/expansion; breakout/pullback structure; absorption/distribution; regime context; and noise/abstention filtering.

## Feature Families

Define, but do not generate, price return/range; volume/liquidity; volume-price relationship; volatility/ATR; momentum/trend; relative strength/ranking; regime/market context; abstention/noise context; target-alignment metadata only; and data-quality/META-limitation features.

## Recommended Package

`PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET` is recommended for operator review, not selected. It combines historical trend quality, volume-price confirmation, relative strength, volatility context, and abstention/noise filtering.

## Supporting Package

`PACKAGE_REGIME_CONTEXT_SIGNAL_SET` is available for operator review, not selected. It covers regime, setup context, metadata-only target alignment, and later VPA/Wyckoff baseline preparation.

## Feature Groups

Define 17 candidate-only groups spanning return/range/body, close location, volume change, spread-volume and effort-result interactions, ATR/volatility, trend slope, setup context, relative strength, market/ticker regime, abstention/noise, metadata-only target profile, availability, and META-limitation flags.

## No-Peek and Target-Separation Rules

Require current-or-prior OHLCV only; prohibit forward returns, target values, and target classes as predictors; limit target profile/horizon to metadata; separately approve chronological splits; use per-ticker history-only windows; preserve META without repair; and require a feature digest manifest.

## Planned Quality Checks

Plan schema completeness, history-only windows, target-value/class exclusion, forward-return exclusion, per-ticker coverage, META preservation, missingness/availability, digest-manifest, and research-only authority-boundary checks. None executes in this candidate.

## Future Outputs

Plan a generation manifest, schema, feature-values JSONL, coverage report, feature-group report, no-peek report, per-ticker report, META limitation report, operator summary, and digest manifest. Every output remains `PLANNED_NOT_GENERATED`.

## Next Chain

Proceed only through candidate operator review; approval if selected; generation execution if approved; generation results review; separately approved feature-label matrix, VPA/Wyckoff, and expectancy-backtest candidates; results-review and readiness gates; and runtime migration only if ever independently authorized.

## Next Gates

The immediate gate is `signal_or_feature_generation_candidate_operator_review`. Every later approval, execution, results-review, matrix, baseline, backtest, reassessment, and runtime gate remains separate.

## Risk Controls

Do not call providers, acquire data, mutate frozen data or ignored evidence outputs, rerun target execution/review, generate signal or feature values, create matrix rows, run backtests, train models, compute metrics, score strategies, generate recommendations, accept usefulness/profitability, or authorize runtime/trading. Preserve research-only and non-actionable labeling throughout.

## Non-Goals

This plan does not select or approve a package, generate values, create a feature-label matrix, evaluate performance, change strategy semantics, migrate runtime behavior, or create trading authority.

## Guardrails

Default validation remains deterministic and offline. Generated `.marketflow` artifacts stay ignored and untracked. All per-ticker facts preserve source row and target counts, especially META's 913-record limitation.

## Next Task

Signal or Feature Generation Candidate v1 is complete, and its Operator Review v1 is implemented.

Feature package selection and Signal or Feature Generation Approval v1 remain future work. Selection, approval, generation, signal values, feature values, feature-label matrix creation, backtesting, model training, metric computation, strategy scoring, recommendations, predictive-usefulness acceptance, profitability acceptance, and runtime authority remain closed.
