# MarketFlow VPA/Wyckoff Rule Baseline Execution v1 Plan

## Purpose

Execute the approved transparent VPA/Wyckoff package as offline, research-only rule and state tagging. This plan does not authorize or perform backtesting, performance evaluation, model training, strategy scoring, recommendations, acceptance, runtime migration, or trading.

## Source Approval

Bind `MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_APPROVED`, approval digest `e8807862a69b4f688becfc2abec3ffade7e1cbb86a884abfc08ac2488db8ed1d`, its exact selected packages, and its complete upstream evidence chain without rerunning the approval.

## Source Matrix Input

- Read ignored `.marketflow/feature_label_matrix/expanded_universe_v1/matrix_rows.jsonl` only through streaming JSONL.
- Require SHA-256 `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7` before execution and verify it remains unchanged afterward.
- Fail closed with a blocked artifact when the source is absent, invalid, changed, or has incorrect counts.

## Dataset and Universe

Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily, 2022-01-01 through 2025-12-31, the exact ordered 12-ticker universe, 11,946 records, META's 913 records, and every other ticker's 1,003 records.

## Selected VPA/Wyckoff Package

Execute `PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE`. Keep `PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT`, its two rules, and its two states available but unselected and unexecuted.

## Rule Threshold Policy

Use `STATIC_TRANSPARENT_BASELINE_NOT_OPTIMIZED` and the fixed approved thresholds for volume effort, close location, relative strength, volatility compression/expansion, noise, slope direction, spread-volume interaction, and effort-result divergence.

## Executed Rule and State Families

- Execute the eight selected volume-confirmation, effort/result, close-pressure, breakout-effort, pullback-quality, relative-strength, volatility, and noise-abstention rule families.
- Execute the six selected accumulation, markup/uptrend, distribution, markdown/downtrend, trading-range/balance, and no-clear-structure state families.
- Use only the thirteen approved history-only feature groups from each matrix row.

## Rule Logic and Values Schema

- Apply the explicit fixed comparisons defined in the execution service; do not fit or optimize any threshold.
- Emit one sanitized rule/state row per matrix row.
- Preserve identity fields and target availability metadata only, plus rule/state tags, availability, evidence digests, and research-only boundaries.

## No-Peek Controls

Never copy target values, target classes, forward returns, future outcome fields, predictions, strategy scores, recommendations, orders, provider payloads, or API keys into rule outputs. Validate exact row fields and selected family identifiers.

## Coverage, Per-Ticker, and META Reports

- Count descriptive tags and unavailable cases by family without computing performance metrics.
- Preserve 15,045 rows for every non-META ticker and 13,695 for META.
- Report META's shorter history explicitly without repair, inference, smoothing, normalization, or fabrication.

## Output Digest Manifest

Write exactly ten ignored outputs and bind their file digests. Use `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` for the digest manifest's own entry and derive a deterministic output-binding digest.

## Next Chain and Gates

Execution → VPA/Wyckoff Rule Baseline Results Review → separately approved Expectancy Backtest Lab Candidate → reassessment and conditional acceptance gates → runtime migration only if ever separately authorized.

## Risk Controls, Non-Goals, and Guardrails

- Do not call providers, inspect credentials, acquire data, regenerate datasets, or rerun prior matrix/candidate/review/approval work.
- Do not mutate source outputs or commit generated `.marketflow` files.
- Do not backtest, train, compute performance metrics, score strategies, recommend trades, accept usefulness/profitability, or authorize runtime/trading.
- Keep all outputs research-only and non-actionable.

## Next Task

VPA/Wyckoff Rule Baseline Execution v1 is complete. Its follow-on Results Review v1 is implemented and verifies all ten ignored research outputs, the streamed rule/state rows, digest bindings, no-peek controls, per-ticker counts, and META limitation without mutating or regenerating source evidence.

Expectancy Backtest Lab Candidate v1 remains future, separately governed work. Backtesting, model training, performance-metric computation, strategy scoring, recommendations, predictive-usefulness acceptance, profitability acceptance, runtime migration, and trading authority remain closed.
