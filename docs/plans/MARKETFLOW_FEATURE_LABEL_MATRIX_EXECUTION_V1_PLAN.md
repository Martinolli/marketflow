# MarketFlow Feature-Label Matrix Execution v1 Plan

## Purpose

Construct the separately approved research-only feature-label matrix from already-reviewed local feature and target outputs. This plan does not authorize backtesting, training, metric computation, strategy scoring, recommendations, acceptance, runtime, or trading.

## Source Approval and Evidence

- Source approval artifact: `MARKETFLOW_FEATURE_LABEL_MATRIX_APPROVED`.
- Approval digest: `0f438427e1b5149b4afb15a8cf0c9af6bb39a95f18e47b8413da6d4e34a9f888`.
- Read only the reviewed `feature_values.jsonl` and `target_values.jsonl` files from ignored `.marketflow` roots.
- Require exact feature, target, and records digests before constructing rows; re-hash both sources afterward.
- Fail closed with `MARKETFLOW_FEATURE_LABEL_MATRIX_BLOCKED_MISSING_OR_INVALID_SOURCE_OUTPUTS` when a source is missing, invalid, changed, or digest-mismatched.

## Dataset and Universe

- Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily, 2022-01-01 through 2025-12-31.
- Preserve the exact ordered twelve-ticker universe and 11,946 canonical records.
- Preserve META's 913-record limitation and all other tickers' 1,003 records without repair or inference.

## Selected Package and Layout

- Matrix package: `PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX`.
- Layout: `MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE`.
- Feature package: `PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET`.
- Target package: `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET`.
- Objective: `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`.

## Construction Method and Row Schema

- Stream one matrix row for every target row.
- Join on dataset, source profile, timeframe, ticker, date, and canonical record index.
- Retain target family, horizon, profile, availability, numeric/class outcomes, unavailable reason, and forward-window dates as outcome metadata.
- Add a wide mapping containing all thirteen feature groups and each group's family, signal family, values, availability, unavailable reason, lookback, and formula version.
- Retain unavailable targets and unavailable feature values. Drop no canonical record or target row.

## No-Peek and Leakage Controls

- Keep target values, target classes, forward returns, and future data outside the feature bundle.
- Emit no prediction, strategy-score, trade-recommendation, broker, order, raw-payload, or API-key fields.
- Create no train/validation/OOS split and perform no model or performance operation.

## Counts and Reports

- Require 155,298 feature source rows and 179,190 target source rows.
- Require 179,190 matrix rows, 177,090 available rows, 2,100 unavailable rows, thirteen groups per row, and 2,329,470 feature-group references.
- Produce coverage, no-peek, target-availability, per-ticker, META-limitation, and operator reports.
- Produce exactly twelve generated outputs under ignored `.marketflow/feature_label_matrix/expanded_universe_v1/`.
- Bind every output through deterministic file digests, matrix rows digest, output binding digest, execution digest, and per-ticker execution digests.

## Next Chain and Gates

1. Feature-Label Matrix Results Review v1.
2. VPA/Wyckoff baseline candidate only after separate approval.
3. Expectancy backtest lab candidate only after separate approval.
4. Results review and readiness gates before any acceptance.
5. Runtime migration only if ever separately authorized.

The gates remain matrix results review, baseline candidacy, backtest-lab candidacy, results review/reassessment, conditional usefulness-acceptance candidacy, and a runtime-migration chain only if ever separately authorized.

## Risk Controls, Non-Goals, and Guardrails

- Work fully offline and never call a provider or acquire market data.
- Never inspect credentials, enable live transport, or commit raw payloads.
- Do not modify either source output or regenerate any upstream artifact.
- Do not commit generated `.marketflow` files.
- Do not backtest, train, compute metrics, score a strategy, recommend trades, accept predictive usefulness/profitability, or authorize runtime/trading.
- Keep MarketFlow research and decision-support only.

## Next Task

Feature-Label Matrix Results Review v1.
