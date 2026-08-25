# MarketFlow Feature-Label Matrix Execution Status

## Execution Artifact

- Artifact: `MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED`.
- Status: `MARKETFLOW_FEATURE_LABEL_MATRIX_EXECUTED_RESEARCH_ONLY`.
- Scope: `FEATURE_LABEL_MATRIX_EXECUTION_ONLY_NOT_BACKTEST_NOT_MODEL_TRAINING`.
- Schema: `marketflow_feature_label_matrix_execution_v1`.
- Execution digest: `badaff7e1b34023d0ea2f2daa5b08e9cabaef0538b1da5c3c3b57f2b72d872f1`.
- Output binding digest: `697c74dd19f5c1ec60b372e39afc335fd9ea416ccf2a6b0c0600160a44b2ef8f`.
- Matrix rows digest: `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7`.
- Checklist: 104 / 104 passed, 0 failed, 0 blockers.

## Source Approval and Outputs

- The execution binds approval digest `0f438427e1b5149b4afb15a8cf0c9af6bb39a95f18e47b8413da6d4e34a9f888` and candidate-review/candidate digests `0a7f440b6bfa79a8ddb0e73d24270f4004b95ef79a0cded3f188acfea4487e56` / `ef3d42d39a5ae353044d29d645a7ca1ad01143e5557951b05b85f837413187b4`.
- Reviewed feature values digest: `7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e`.
- Reviewed target values digest: `61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119`.
- Records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Both ignored source files were verified before and after construction and remained unchanged.
- The complete upstream target, signal/feature, expectancy, charter, archive, readiness, reassessment, improved-evidence, registry, and records digest chain remains bound.

## Selected Matrix Contract

- Package: `PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX`.
- Layout: `MATRIX_LAYOUT_TARGET_PROFILE_WITH_WIDE_FEATURE_BUNDLE`.
- Feature package: `PACKAGE_TREND_FLOW_EXPECTANCY_SIGNAL_SET`.
- Target package: `PACKAGE_EXPECTANCY_PAYOFF_ABSTENTION_LABEL_SET`.
- Objective: `EXPECTANCY_PAYOFF_WITH_ABSTENTION_SUPPORT`.
- Each target row is joined to all thirteen approved feature groups by dataset, source profile, timeframe, ticker, date, and canonical record index.
- Target value and class remain top-level outcome fields. They are never inserted into the feature bundle.
- Unavailable targets remain in the matrix with null outcomes. Unavailable feature values remain null inside their feature-group entries.

## Dataset, Coverage, and META Limitation

- Dataset: `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily, 2022-01-01 through 2025-12-31.
- Ordered universe: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- Canonical records: 11,946; feature source rows: 155,298; target source rows: 179,190.
- Matrix rows: 179,190; available target rows: 177,090; unavailable target rows: 2,100.
- Feature references: 2,329,470, representing thirteen groups in every matrix row.
- Every non-META ticker has 1,003 historical records, 13,039 feature rows, 15,045 matrix rows, 14,870 available rows, and 175 unavailable rows.
- META remains exactly 913 historical records, 11,869 feature rows, 13,695 matrix rows, 13,520 available rows, and 175 unavailable rows.
- META was not repaired, inferred, smoothed, normalized, backfilled, or fabricated.

## Generated Research Outputs

- Exactly twelve sanitized outputs were written under ignored `.marketflow/feature_label_matrix/expanded_universe_v1/`.
- They include the execution manifest, matrix/feature/target schemas, matrix JSONL, coverage/no-peek/availability/per-ticker/META/operator reports, and digest manifest.
- The digest manifest uses `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` for itself and a separate self-reference policy for the execution artifact.
- Generated `.marketflow` files remain ignored and untracked.

## Authority Boundary and Next Gate

- This execution constructed only a research-only, non-actionable feature-label matrix.
- It did not call providers, acquire data, regenerate the dataset, or rerun source generation/review/approval steps.
- It did not run a backtest, train a model, compute performance metrics, score a strategy, or generate recommendations.
- Predictive usefulness and profitability remain not accepted.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- Follow-on Feature-Label Matrix Results Review v1 is implemented as an offline, digest-bound review of the twelve generated research-only matrix outputs.
- The execution remains the source evidence and was not rerun or modified by that review.
- The results review does not create a VPA/Wyckoff baseline candidate, expectancy backtest lab candidate, backtests, models, performance metrics, recommendations, predictive-usefulness or profitability acceptance, or runtime authority.
- The next task is VPA/Wyckoff Rule Baseline Candidate v1, invoked separately.
