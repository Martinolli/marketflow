# MarketFlow Objective Label or Target Generation Execution v1 Plan

## Purpose

Generate the already approved expectancy/payoff/abstention target package from frozen local canonical rows, producing digest-bound research evidence only.

## Source Approval

The immutable source is `MARKETFLOW_OBJECTIVE_LABEL_OR_TARGET_GENERATION_APPROVED` with approval digest `df3ee8758ca86a04f944ed1a46ede444693833009c99692e490f6cae5e21414b`. The complete upstream candidate, design, charter, archive, readiness, reassessment, improved-evidence, feature, label, registry, and records digest chain is carried forward.

## Dataset and Universe

Use `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, 2022-01-01 through 2025-12-31, read-only. Preserve the ordered twelve-ticker universe and 11,946 rows. META remains exactly 913 rows; every other ticker remains 1,003.

## Selected Package and Target Families

The selected package/path is `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET` / `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`. Generate these families for 5, 10, and 20 sessions:

- `TARGET_EXPECTANCY_SCORE`
- `TARGET_PAYOFF_ASYMMETRY_SCORE`
- `TARGET_REWARD_TO_RISK_CLASS`
- `TARGET_NO_TRADE_ABSTAIN_CLASS`
- `TARGET_MATERIAL_MOVE_AFTER_COST_CLASS`

## Formula Definitions

Use deterministic same-ticker forward OHLCV windows. Compute cost-adjusted forward return, maximum favorable/adverse excursion, drawdown magnitude, reward-to-risk, payoff asymmetry, expectancy score, abstention class, and material-move-after-cost class exactly as documented by the execution service.

## Availability and No-Peek Controls

Only target outputs may inspect future rows. No future outcome is emitted as a feature. The final 5/10/20-session tails remain unavailable with null value/class and `INSUFFICIENT_FUTURE_BARS`. Any future train/validation/OOS split requires separate approval.

## Cost and Slippage Assumptions

Declare, do not estimate: round-trip cost `0.0010`, risk floor `0.0050`, material-move threshold `0.0150`, favorable reward-to-risk threshold `1.5`, and positive payoff-asymmetry threshold `1.2`.

## Target Values and Coverage

Write 179,190 JSONL target rows across 15 profiles. Preserve 177,090 available rows and 2,100 unavailable rows. The coverage report records per-profile distributions and the per-ticker report records exact historical, total, available, and unavailable counts plus deterministic ticker digests.

## META Limitation

META's exact 913-row source limitation is preserved. Do not repair, backfill, infer, fabricate, smooth, or normalize the discrepancy.

## Output Digest Manifest

Write exactly eleven ignored `.marketflow` outputs. Bind ordinary output file SHA-256 values, the target-values digest, and the path-independent output-binding digest. Mark the digest manifest with `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.

## Next Chain and Gates

The immediate next task is Objective Label or Target Generation Results Review v1. Signal/feature planning, a VPA/Wyckoff baseline, an expectancy backtest lab, predictive-usefulness acceptance, and any runtime migration remain separate future gates.

## Risk Controls and Non-Goals

This task does not call providers, acquire data, regenerate the canonical dataset, rerun candidate/review/approval steps, generate features, create matrix rows, backtest, train models, compute performance metrics, score strategies, generate recommendations, accept predictive usefulness or profitability, or authorize runtime/trading.

## Guardrails

All generated files remain ignored and untracked under `.marketflow`. Default tests remain deterministic and offline. The execution fails closed with a blocked artifact when canonical source rows are missing, invalid, or digest-mismatched.
