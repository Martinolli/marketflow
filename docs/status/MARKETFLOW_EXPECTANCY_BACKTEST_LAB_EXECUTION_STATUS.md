# MarketFlow Expectancy Backtest Lab Execution Status

## Status

- Artifact: `MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED`.
- Status: `MARKETFLOW_EXPECTANCY_BACKTEST_LAB_EXECUTED_RESEARCH_ONLY`.
- Scope: `EXPECTANCY_BACKTEST_LAB_EXECUTION_ONLY_NOT_MODEL_TRAINING_NOT_RUNTIME`.
- Package: `PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB`.
- Source approval digest: `b6a6289dcfe9b4fa1888e697025187e6f287429e54756b9bbd0528ab0138d16e`.

## Offline Execution

The lab streams the frozen `matrix_rows.jsonl` and `vpa_wyckoff_rule_values.jsonl` files in lockstep. It verifies their SHA-256 digests and matching identity keys, retains one lab row per matrix row, assigns chronological splits, and applies a horizon-aware split embargo. The source files remain unchanged.

Exactly 179,190 research rows are created: 177,090 have available target outcomes and 2,100 preserve unavailable outcomes. META remains limited to 913 historical records and 13,695 lab rows. All outputs are written beneath ignored `.marketflow/expectancy_backtest_lab/expanded_universe_v1/` and are not tracked.

## Research Outputs

The execution creates exactly fourteen sanitized outputs: the execution manifest, row schema, lab JSONL, result summary, metric report, baseline comparison, VPA/Wyckoff alignment, abstention quality, per-ticker, chronological split, META limitation, no-peek, operator summary, and digest manifest.

Six deterministic baselines and thirteen descriptive metric families are executed. The randomized-null baseline remains blocked; bootstrap/confidence-interval computation remains blocked. Target outcomes remain outcome fields only, prior-rate references use strictly earlier chronological splits, and cross-boundary forward horizons are excluded from aggregate metrics.

## Authority Boundary

This execution does not train models, optimize thresholds, score a strategy, generate recommendations, simulate orders, accept predictive usefulness or profitability, or authorize runtime, strategy, paper trading, or broker execution. It makes no provider request, acquires no market data, regenerates no dataset, and reruns no upstream source stage.

## Next Task

Expectancy Backtest Lab Results Review v1 is implemented as the read-only follow-on. The execution remains immutable source evidence. The review verifies research-only lab rows, results, metrics, baselines, chronology, no-peek controls, per-ticker counts, META limitations, and all output digests. It does not create reassessment or acceptance readiness, train models, score strategies, generate recommendations, accept usefulness/profitability, or authorize runtime or trading.
