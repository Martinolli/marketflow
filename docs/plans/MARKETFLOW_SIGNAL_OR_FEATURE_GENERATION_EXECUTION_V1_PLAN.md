# MarketFlow Signal or Feature Generation Execution v1 Plan

## Purpose

Generate the approved trend/flow/expectancy signal and feature package from frozen canonical rows, producing deterministic, digest-bound, research-only evidence.

## Source Approval

Use `MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_APPROVED` and approval digest `d174f5d775cb7b423121333838ab74956384068b8a46240760d399f02e229a8c` as immutable source evidence. Carry the complete candidate, target-generation, expectancy-design, charter, archive, improved-evidence, registry, and records digest chain forward without rerunning it.

## Dataset and Universe

Read `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, 2022-01-01 through 2025-12-31, locally and read-only. Preserve 11,946 rows and the ordered universe MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT. META remains exactly 913 records; every other ticker remains 1,003.

## Selected Packages and Objective Path

Generate `PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET` in support of the separately generated target package `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET` and objective path `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`. Target facts are metadata only and are never feature inputs.

## Signal Families

- `SIGNAL_TREND_STRUCTURE`
- `SIGNAL_VOLUME_PRICE_ANALYSIS`
- `SIGNAL_CLOSE_LOCATION_AND_SPREAD`
- `SIGNAL_EFFORT_RESULT_BEHAVIOR`
- `SIGNAL_RELATIVE_STRENGTH`
- `SIGNAL_VOLATILITY_COMPRESSION_EXPANSION`
- `SIGNAL_NOISE_AND_ABSTENTION_FILTER`

## Feature Families

- `FEATURE_PRICE_RETURN_AND_RANGE`
- `FEATURE_VOLUME_AND_LIQUIDITY`
- `FEATURE_VOLUME_PRICE_RELATIONSHIP`
- `FEATURE_VOLATILITY_AND_ATR`
- `FEATURE_MOMENTUM_AND_TREND`
- `FEATURE_RELATIVE_STRENGTH_AND_RANKING`
- `FEATURE_ABSTENTION_AND_NOISE_CONTEXT`
- `FEATURE_DATA_QUALITY_AND_META_LIMITATION`

## Feature Groups and Formula Definitions

Generate one row per canonical record and each of thirteen groups: close-to-close returns; intraday range/body/wicks; close-location values; volume change and 20-row z-score; spread-volume interaction; effort-result divergence; true range, ATR, and volatility compression; moving-average levels and slopes; relative strength versus the universe; relative-strength ranks and percentiles; abstention/noise context; data-availability flags; and META-limitation flags.

All returns, rolling means, standard deviations, ATRs, slopes, and ratios are deterministic and use only current/prior same-ticker OHLCV. Relative-strength ranks use same-date history-only trailing returns across available universe members. Division-by-zero and insufficient-history values are null. Rows are never dropped.

## No-Peek and Target-Separation Controls

Enforce the ten approved rules: current/prior OHLCV only; no forward return, target value, or target class as a feature; target profile/horizon as metadata only; chronological splits require separate approval; windows remain per ticker; META is not repaired; and the digest manifest is mandatory.

## Feature Values and Coverage Outputs

Write 155,298 long-form JSONL rows across thirteen groups. The feature-values schema records source identity, feature/signal families, values and availability, history counts, package/path metadata, research-only flags, and bound source digests. Coverage and group reports preserve available/null counts and formula documentation.

## Per-Ticker Report and META Limitation

Every non-META ticker has 13,039 rows. META has 11,869 rows from exactly 913 canonical records. Preserve that limitation explicitly; do not repair, backfill, infer, fabricate, smooth, or normalize it. Bind each ticker entry with its own deterministic execution digest.

## Output Digest Manifest

Write exactly ten ignored outputs under `.marketflow/signal_or_feature_generation/expanded_universe_v1/`. Bind ordinary file SHA-256 values, the feature-values digest, and the path-independent output-binding digest. Mark the digest manifest `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.

## Next Chain and Gates

The immediate next task is Signal or Feature Generation Results Review v1. A feature-label matrix candidate, VPA/Wyckoff baseline candidate, expectancy backtest lab, results/reassessment, predictive-usefulness acceptance candidate, and any runtime migration remain separate future gates.

## Risk Controls, Non-Goals, and Guardrails

This execution does not call providers, acquire data, mutate frozen inputs, rerun upstream ceremonies, create a feature-label matrix, backtest, train models, compute performance metrics, score strategies, generate recommendations, accept predictive usefulness or profitability, or authorize runtime/trading. Generated files remain ignored and untracked. Missing or digest-invalid canonical records yield a closed blocked artifact and no feature outputs.
