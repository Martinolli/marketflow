# MarketFlow Signal or Feature Generation Execution Status

## Execution Artifact

- Artifact: `MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED`.
- Status: `MARKETFLOW_SIGNAL_OR_FEATURE_GENERATION_EXECUTED_RESEARCH_ONLY`.
- Schema: `marketflow_signal_or_feature_generation_execution_v1`.
- Scope: `SIGNAL_OR_FEATURE_GENERATION_EXECUTION_ONLY_NOT_FEATURE_LABEL_MATRIX_NOT_BACKTEST`.
- Selected feature package: `PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET`.
- Selected target package/path: `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET` / `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`.
- Source approval digest: `d174f5d775cb7b423121333838ab74956384068b8a46240760d399f02e229a8c`.
- Execution digest: `bcccbdc57616e7ff0c350535628a4a2b2cb752e11b4c98b0b9905fed9f9e4e60`.
- Output-binding digest: `5e0ef154d13782bc58c284b2d664f35e7f0724bb890efc2235e840df62dbf4e8`.
- Feature-values digest: `7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e`.

## Dataset, Features, and Coverage

- The service reads `expanded_universe_canonical_dataset_v1` locally and read-only, verifies the records digest `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044` before and after generation, and never regenerates source data.
- The ordered universe remains MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT: 11,946 daily RTH records from 2022-01-01 through 2025-12-31.
- Seven selected signal families, eight selected feature families, and thirteen selected feature groups produce exactly 155,298 long-form rows.
- Exactly 155,142 rows are available and 156 are unavailable because their entire feature group lacks sufficient history. Individual unavailable trailing values remain null; no row is dropped.
- Every non-META ticker has 13,039 feature rows. META has 11,869 feature rows from its exact 913 source records, with no repair, backfill, inference, or synthetic replacement.

## Outputs and Controls

- Exactly ten deterministic, sanitized outputs are written under ignored `.marketflow/signal_or_feature_generation/expanded_universe_v1/`.
- The digest manifest binds all ordinary output SHA-256 values and applies `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` to itself.
- Features use current or prior same-ticker OHLCV only, except same-date cross-sectional ranks derived from history-only trailing returns.
- Target values, target classes, forward returns, future data, predictions, scores, recommendations, orders, raw provider payloads, and credentials are excluded.
- The 87-check execution checklist passes with zero failures and zero blockers.

## Authority Boundary and Next Gate

- Signal/feature generation and feature-value creation are true only for this offline, research-only evidence set.
- No feature-label matrix, backtest, trained model, performance metric, strategy score, or recommendation was created.
- Predictive usefulness and profitability remain not accepted.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, market-data acquisition, dataset regeneration, candidate/review/approval rerun, runtime activation, or trading action occurred.
- The follow-on Signal or Feature Generation Results Review v1 is now implemented on its stacked branch.
- The execution artifact and ten ignored outputs remain immutable source evidence; the review reads and hashes them in place without regeneration.
- The review verifies the research-only feature schema, counts, families, groups, no-peek controls, per-ticker coverage, META limitation, and digest manifest.
- Review readiness permits only a future Feature-Label Matrix Candidate v1. It creates no matrix rows, backtests, models, performance metrics, scores, recommendations, acceptance, profitability, runtime, or trading authority.
