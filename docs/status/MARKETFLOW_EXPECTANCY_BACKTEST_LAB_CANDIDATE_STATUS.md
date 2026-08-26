# MarketFlow Expectancy Backtest Lab Candidate Status

## Candidate Artifact

- Artifact: `MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_V1`.
- Status: `MARKETFLOW_EXPECTANCY_BACKTEST_LAB_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `EXPECTANCY_BACKTEST_LAB_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION`.
- Candidate digest: `8dbca7083455dffa91d42610b7b12ae6407176d9b87e8a9dda1c6bc8f0cf6ad9`.
- Checklist: 67 / 67 passed, 0 failed, 0 blockers.

## Bound Source Evidence

- Source VPA/Wyckoff results-review digest: `afdb0f141a412652b2dfca5abc08033f3858a6a5fb4b7a9e9eefc032643405fe`.
- Source VPA/Wyckoff execution/output-binding/rule-values digests: `5b453c45ddd39fa4a059cd78a02254a241876443794213f6238bde69a534eaec` / `3bcaa233d6dab9d13e85f9a80f3ef2c0503d6a64f4707560a3f117ba9ab6afc7` / `bef559f34d42777b577a89a1842a2cffd6e7ff712b0c3191776901c12f4dbcad`.
- Source matrix results-review/rows digests: `7def4b9c9b7d9c51dd454246e7f7718e86640d971f0b5da1c88bd240796aae30` / `edc8de9290c94561de344e1a86c39f2ecbe9ed2cc1ca6d54dd081c278c92c0c7`.
- Feature, target, records, expectancy, charter, archive, readiness, reassessment, improved-evidence, and registry digests remain bound through the complete upstream evidence chain.

## Candidate Basis and Package

- Dataset: `expanded_universe_canonical_dataset_v1`, ordered 12-ticker universe, 11,946 records, and META 913 preserved.
- Basis: 179,190 matrix rows, 177,090 evaluable target rows, 2,100 unavailable target rows, 179,190 rule/state rows, eight rule families, six state families, thirteen feature groups, and fifteen target profiles.
- Recommended but unselected package: `PACKAGE_EXPECTANCY_VPA_WYCKOFF_RESEARCH_BACKTEST_LAB`.
- Supporting unselected packages cover feature-only, abstention-quality, and cost-sensitivity diagnostics.

## Planned Research Design

- Ten candidate objectives, seven candidate baselines, fourteen candidate metric families, and eleven planned no-peek controls are defined but not executed.
- Chronological windows are 2022-2023 calibration, 2024 validation, and 2025 holdout under `CHRONOLOGICAL_NO_SHUFFLE` with a required future-horizon-aware embargo.
- Randomized-null and bootstrap/confidence-interval paths remain blocked pending separate operator approval because of chronological-dependence concerns.
- Fourteen future outputs are `PLANNED_NOT_GENERATED`; no backtest rows, results, or metric values exist.

## Per-Ticker and META Boundary

- Each non-META ticker plans 15,045 rows, including 14,870 evaluable and 175 unavailable target rows.
- META plans exactly 13,695 rows, including 13,520 evaluable and 175 unavailable target rows, without repair or inference.
- All twelve candidate entries have deterministic per-ticker digests.

## Authority Boundary

- Candidate creation/readiness and readiness for a separate operator review are true.
- Selection, approval, authorization, execution, backtest rows/results, metric computation, model training, strategy scoring, and recommendations remain false.
- Predictive usefulness and profitability remain not accepted. Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, market-data acquisition, dataset regeneration, prior execution/review rerun, runtime activation, or trading action occurred.

## Next Task

Expectancy Backtest Lab Candidate Operator Review v1.
