# MarketFlow VPA/Wyckoff Rule Baseline Execution Status

## Execution Artifact

- Artifact: `MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED`.
- Status: `MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_EXECUTED_RESEARCH_ONLY`.
- Scope: `VPA_WYCKOFF_RULE_BASELINE_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING`.
- Selected package: `PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE`.
- Execution digest: `5b453c45ddd39fa4a059cd78a02254a241876443794213f6238bde69a534eaec`.
- Output-binding digest: `3bcaa233d6dab9d13e85f9a80f3ef2c0503d6a64f4707560a3f117ba9ab6afc7`.
- Rule-values digest: `bef559f34d42777b577a89a1842a2cffd6e7ff712b0c3191776901c12f4dbcad`.
- Checklist: 83 / 83 passed, 0 failed, 0 blockers.

## Source Approval and Matrix

- Source approval digest: `e8807862a69b4f688becfc2abec3ffade7e1cbb86a884abfc08ac2488db8ed1d`.
- Source candidate-review/candidate digests: `8447ca124e62ef8ea346aa2ee23d0a0c209791bf960659adf7cd75dc363dfbd9` / `7f5bd67e553834978bf6e2fb0a5142e450e55941696704d6da489c1a23b97d66`.
- Source matrix results-review/execution/output-binding/rows digests remain bound, including rows digest `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7`.
- Source feature/target/records digests remain bound. The complete upstream evidence chain carried by the approval is preserved.
- The existing 1.383 GB matrix was read using streaming JSONL and verified before and after execution. Its digest and modification time remained unchanged.

## Generated Research Outputs

- Exactly 179,190 rule-value rows and 179,190 state-value rows were generated from 179,190 matrix rows.
- Eight selected rule families produced 1,433,520 rule references; six selected state families produced 1,075,140 state references.
- Exactly ten deterministic sanitized outputs were written beneath ignored `.marketflow/vpa_wyckoff_rule_baseline/expanded_universe_v1/`.
- The threshold policy is `STATIC_TRANSPARENT_BASELINE_NOT_OPTIMIZED`; coverage counts are descriptive tagging coverage, not performance metrics or predictive evidence.
- Eleven tickers retain 1,003 historical records and 15,045 rows each. META retains exactly 913 historical records and 13,695 rows without repair or inference.

## No-Peek and Authority Boundary

- Rule rows preserve identity and target availability metadata only. Target values, target classes, forward returns, future labels, predictions, scores, recommendations, orders, provider payloads, and API-key fields are absent.
- No provider request, acquisition, dataset regeneration, matrix rerun, candidate/review/approval rerun, backtest, model training, performance-metric computation, strategy scoring, or recommendation occurred.
- Predictive usefulness and profitability remain not accepted.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- The next task is VPA/Wyckoff Rule Baseline Results Review v1, invoked separately.
