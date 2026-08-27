# MarketFlow Expectancy Backtest Lab Execution v1 Plan

## Purpose

Create digest-bound, offline, research-only expectancy-lab rows and descriptive reports for the operator-approved package. The work is evidence generation, not model training, predictive acceptance, profitability acceptance, or runtime migration.

## Source Approval and Inputs

- Source approval: `MARKETFLOW_EXPECTANCY_BACKTEST_LAB_APPROVED` with digest `b6a6289dcfe9b4fa1888e697025187e6f287429e54756b9bbd0528ab0138d16e`.
- Matrix input: ignored `matrix_rows.jsonl`, digest `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7`.
- VPA/Wyckoff input: ignored `vpa_wyckoff_rule_values.jsonl`, digest `bef559f34d42777b577a89a1842a2cffd6e7ff712b0c3191776901c12f4dbcad`.
- Dataset: `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, 2022-01-01 through 2025-12-31.
- Universe order: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.

## Construction Method and Row Schema

Stream both JSONL inputs together and reject any identity mismatch. Preserve identity, target outcomes, forward-horizon metadata, reviewed VPA/Wyckoff rule/state conditions, chronological split, embargo status, deterministic baseline references, metric eligibility, and source digests. Target value and class remain top-level outcomes and never enter condition or predictor-like fields.

## Chronological Split Plan

- Calibration: 2022-01-01 through 2023-12-31.
- Validation: 2024-01-01 through 2024-12-31.
- Holdout: 2025-01-01 through 2025-12-31.
- Policy: `CHRONOLOGICAL_NO_SHUFFLE`.
- Horizon-aware embargo: retain cross-boundary rows for coverage but exclude them from aggregate metrics.
- Prior rates: validation uses calibration only; holdout uses calibration and validation only.

## Baselines and Metric Families

Execute always-abstain, always-available-target, simple buy-and-hold distribution, previous-direction, VPA/Wyckoff rule-tag, and target-profile prior-rate references. Do not execute the blocked randomized-null reference.

Compute the thirteen approved descriptive families covering expectancy/average outcome, positive rate, payoff and reward-risk alignment, participation, abstention, adverse proxy, material-move capture, ticker and chronological stability, rule/state contribution, and baseline delta. Do not compute blocked bootstrap/confidence intervals.

## Reports and Output Digests

Create the row schema, result and metric summaries, baseline comparison, VPA/Wyckoff alignment, abstention quality, per-ticker, chronological split, META limitation, no-peek, and operator reports. Bind all fourteen outputs in a deterministic digest manifest with `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` for the digest manifest itself.

## META Limitation

Preserve META's exact 913 records, 13,695 lab rows, 13,520 evaluable target rows, and 175 unavailable target rows. Do not repair, infer, smooth, or fabricate the reduced history.

## No-Peek Controls

No shuffling, outcome-defined rule tags, future features, same-row prior rate, prediction field, strategy score, recommendation, broker/order field, provider payload, or API key is allowed. Unavailable targets stay unavailable and remain excluded from aggregate values.

## Next Chain and Gates

The next task is Expectancy Backtest Lab Results Review v1, followed by predictive-usefulness reassessment. Acceptance-readiness and any acceptance candidate require separate later gates. Runtime migration remains closed unless ever separately authorized.

## Risk Controls, Non-Goals, and Guardrails

Do not call providers, acquire market data, regenerate the canonical dataset, rerun upstream generation/review/approval stages, mutate frozen or ignored source outputs, train models, score strategies, create recommendations, accept usefulness/profitability, or authorize runtime/trading. Generated `.marketflow` outputs remain ignored and untracked.
