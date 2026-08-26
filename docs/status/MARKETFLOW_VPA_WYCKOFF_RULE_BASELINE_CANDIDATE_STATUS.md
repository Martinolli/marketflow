# MarketFlow VPA/Wyckoff Rule Baseline Candidate Status

## Candidate Artifact

- Artifact: `MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_V1`.
- Status: `MARKETFLOW_VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `VPA_WYCKOFF_RULE_BASELINE_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION`.
- Deterministic candidate digest: `7f5bd67e553834978bf6e2fb0a5142e450e55941696704d6da489c1a23b97d66`.
- Checklist: 92 / 92 passed, 0 failed, 0 blockers.
- The artifact is offline, digest-bound, research-only, non-actionable, and requires operator review.

## Source Matrix Review and Dataset

- Source matrix results-review digest: `7def4b9c9b7d9c51dd454246e7f7718e86640d971f0b5da1c88bd240796aae30`.
- Source execution/output-binding/matrix-row digests: `badaff7e1b34023d0ea2f2daa5b08e9cabaef0538b1da5c3c3b57f2b72d872f1` / `697c74dd19f5c1ec60b372e39afc335fd9ea416ccf2a6b0c0600160a44b2ef8f` / `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7`.
- Source feature/target/records digests: `7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e` / `61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Dataset: `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily, 2022-01-01 through 2025-12-31.
- The ordered 12-ticker universe and 11,946 records remain preserved. META remains exactly 913 records; other tickers remain at 1,003.
- The committed source review remains evidence. It was not rebuilt, and ignored matrix outputs were not read or modified.

## Candidate Basis and Philosophy

- The basis remains 179,190 reviewed matrix rows, 177,090 available targets, 2,100 unavailable targets, thirteen feature groups, and 2,329,470 feature references.
- The candidate prepares a transparent, explainable VPA/Wyckoff rule baseline for later comparison with expectancy target profiles.
- It does not train models, optimize thresholds, generate recommendations, or establish runtime authority.
- Threshold selection and rule design remain twelve explicitly unanswered operator-review questions.

## Proposed Rule, State, and Package Design

- Ten candidate-only VPA rule families cover volume confirmation, effort/result, close location, climax/exhaustion, absorption, breakout effort, pullback quality, relative strength, volatility compression/expansion, and noise abstention.
- Eight candidate-only Wyckoff state families cover accumulation, markup, distribution, markdown, balance, possible spring, possible upthrust, and no-clear-structure contexts.
- `PACKAGE_VPA_WYCKOFF_TRANSPARENT_RULE_BASELINE` is recommended for operator review but not selected. It contains eight rule families and six state families.
- `PACKAGE_VPA_WYCKOFF_EXTENDED_REVERSAL_CONTEXT` is an available but unselected supporting package for reversal/exhaustion context.
- All thirteen existing feature groups have planned, no-future-data mappings. Target values are not used in rule inputs.
- Ten future output types are declared `PLANNED_NOT_GENERATED`.

## Planned Counts and META Limitation

- Planned rule families/states: 10 / 8; planned primary-package rule families/states: 8 / 6.
- Planned rule-value/state rows: 179,190 / 179,190, for future research-only tagging—not backtesting.
- Each non-META ticker plans 15,045 matrix-linked rows. META plans 13,695 and retains its reduced-history flag.
- No metric counts are approved.

## Authority Boundary and Next Gate

- Candidate creation/readiness and readiness for Candidate Operator Review v1 are true.
- Selection, approval, authorization, execution, rule values, and baseline outputs remain false.
- Backtests, training, metrics, scoring, recommendations, predictive-usefulness acceptance, and profitability acceptance remain closed.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider, acquisition, dataset regeneration, source rerun, rule execution, runtime, or trading action occurred.
- Follow-on VPA/Wyckoff Rule Baseline Candidate Operator Review v1 is implemented as an offline, digest-bound, review-only package.
- This candidate remains its source evidence and was not regenerated or modified.
- The review does not select or approve either VPA/Wyckoff package and creates no rule values, baseline outputs, backtests, models, metrics, recommendations, predictive-usefulness or profitability acceptance, or runtime authority.
- The next possible task is VPA/Wyckoff Rule Baseline Approval v1 only if separately selected and authorized.
