# MarketFlow Additional Predictive Evidence Execution Status

## Branch And Commit

- Branch: `feature/additional-predictive-evidence-execution-v1`.
- Base commit: `3845b5c5ecc928683037203df22a29f458e26a71`.
- Implementation commit: `Execute additional predictive evidence research run` (recorded by Git after this document is staged).

## Execution Artifact And Status

- Artifact kind: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED`.
- Schema: `additional_predictive_evidence_executed_v1`.
- Execution status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY`.
- Execution digest: `61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3`.
- Fixed offline run timestamp: `2026-08-15T00:00:00Z`.
- Execution authorized/performed/results created: `True / True / True`.
- Failures/warnings: `0 / 1`.

## Source Execution Approval

- Execution approval digest: `01cc79720ec9a27eb15a88214dfd5d152f5a6ae95082e7e13167239601c8afd9`.
- Execution-candidate review digest: `ab41b9e28693ca770c85a7e872d640f04b7c59c97b3b8eb40b28c9b101652ff7`.
- Execution-candidate digest: `d7f83a8b7be2be3a663ddb04097bf08b346071f70c9e770dd8f25e9fd9f4947e`.
- Chain-candidate review/candidate digests: `41e7b4db107a056790b1caa749b789d434698c6416333328297b894fa0832c82` / `672b6d8d6299078df718247f3accea1250ea0c0228fa5315738d6e9ad7e055cf`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical-dataset freeze digest: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc`.
- Canonical-dataset generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Canonical records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Source profile: `RTH_FULL_SESSION_1D`.
- Date range/timeframe: `2022-01-01` through `2025-12-31` / `1d`.
- Data-quality status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Registry label: `RESEARCH_ONLY_NON_ACTIONABLE`.

## Target Universe And Per-Ticker Records

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Total canonical records: `11946`.
- `META`: exactly `913` records, preserved without repair, inference, smoothing, normalization, backfill, or fabrication.
- Every non-META ticker: exactly `1003` records.

## Label Generation Summary

- Seven forward-only label families were generated: next-bar direction/return bucket, next-session direction/return bucket, multi-horizon return bucket, future volatility regime, and future drawdown risk.
- NEXT_BAR and NEXT_SESSION remain separate named families with explicit one-session horizons for the daily profile.
- Multi-horizon return buckets use `1`, `5`, and `20` future sessions.
- Fixed return, volatility, and drawdown thresholds are recorded in `label_generation_manifest.json`; no validation or OOS data was used to fit them.
- Labels without enough future bars are represented as null with `label_unavailable_due_to_insufficient_future_bars`.
- Coverage entries: `84`; available values across ticker/family entries: `82854`; unavailable values: `768`.
- Label-generation digest: `08e9aa9458c462dc3552fe25d6db9230d384228767848110bce76f8457e3eda3`.
- Future label values were not used as features.

## Feature Generation Summary

- Ten approved feature families and `22` feature fields were generated from current and historical data only.
- Feature rows: `11946`.
- Feature-family coverage entries: `120`.
- Expected rolling-window null/unavailable count across all feature fields: `1428`.
- Feature-matrix digest: `ab543dc38aa75ea6a0bdc654a538bcb31d0081c8a1030fa1cf71665b23bcdd2d`.
- Feature evidence includes OHLCV returns, volume/price, realized volatility, trend/momentum, Wyckoff/VPA, corporate-action context, cross-ticker relative strength, calendar/session fields, data-quality flags, and the META reduced-count flag.

## Walk-Forward Validation Summary

- Policy: `EXPANDING_TRAINING_WITH_QUARTERLY_2024_VALIDATION_FOLDS`.
- Shuffle: `False`.
- One-session label-availability gap applied per ticker.
- `2024_Q1`: `5922` training / `732` evaluation rows; majority accuracy `0.562842`.
- `2024_Q2`: `6654` training / `756` evaluation rows; majority accuracy `0.541005`.
- `2024_Q3`: `7410` training / `768` evaluation rows; majority accuracy `0.552083`.
- `2024_Q4`: `8178` training / `768` evaluation rows; majority accuracy `0.498698`.
- These values are research evidence awaiting operator review, not usefulness or profitability acceptance.

## Out-Of-Sample Evaluation Summary

- Holdout: `2025-01-01` through `2025-12-31`.
- Chronological/no-shuffle evaluation count: `2988`.
- Majority-class accuracy: `0.539491`.
- Deterministic random accuracy: `0.324967`.
- Previous-direction accuracy: `0.495984`.
- Zero-return accuracy: `0.001004`.
- Buy-and-hold reference-only accuracy: `0.539491`.
- Ticker cross-sectional accuracy: `0.502677`.
- The buy-and-hold value is a non-actionable reference and is not a recommendation.

## Metric, Calibration, Stability, And Leakage Summary

- Nine metric families were computed where applicable: classification, regression, calibration, ranking/lift, baseline comparison, stability, false-positive/false-negative, leakage-control, and data-quality metrics.
- Unsupported label/metric combinations are recorded as `NOT_EVALUATED_FOR_LABEL_TYPE`; no values were fabricated.
- Majority-class OOS balanced accuracy/macro F1: `0.333333 / 0.233623`.
- Ticker cross-sectional OOS balanced accuracy/macro F1: `0.335496 / 0.334769`.
- OOS UP-vs-not-UP Brier score: `0.24875351` using the training-window probability.
- Stability results retain all four walk-forward fold values plus OOS values for every baseline.
- Leakage-control status: `PASS`; failed controls: `0`.
- Controls confirm forward labels, history-only features, chronological splits, no shuffle, fixed thresholds, disabled provider transport, and closed runtime/trading paths.

## Data-Quality Summary

- Status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Failures: `0`.
- Warning: `META_REDUCED_RECORD_COUNT_PRESERVED` with exactly `913` records.
- All nine frozen canonical source files and their manifest digests were verified before execution.
- The canonical digest-manifest self-reference remains `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` and is not treated as missing evidence.
- The frozen canonical source files were not modified.

## Generated Outputs

- Ignored output root: `.marketflow/additional_predictive_evidence/expanded_universe_v1/`.
- Generated output count: `15`.
- Every output is labeled `RESEARCH_ONLY_NON_ACTIONABLE` with scope `ADDITIONAL_PREDICTIVE_EVIDENCE_RESEARCH_ONLY`.
- Generated `.marketflow` outputs are evidence artifacts, not tracked source files.

Output SHA-256 summary:

- `additional_predictive_evidence_execution_manifest.json`: `5360f73672b0d5179970703f4df5280c5c368a7c507bb5fa13164783908edf5b`
- `label_generation_manifest.json`: `bbce88ae5c562e32767514cc00d64f581695ffb20ca92d01c64c7d9b4bc0b1d1`
- `label_distribution_report.json`: `87243e8c7acfc0d743b4428fa9d65d97e99565ba4cdfebb2a270743dfdfc8f1a`
- `feature_matrix_manifest.json`: `bb92fc2dfe3bdf54f9ff05fefc37aee4e85bd26a59de58cddc6caf548b220745`
- `feature_quality_report.json`: `391dc53f0f9cab6a06d029763f83260d4cf51129c7ba543297c39f384ac4bdf0`
- `walk_forward_results_report.json`: `427c694076fec4a9d65f63ad64efbacb119572e55d78aabb74ccdec278c80727`
- `out_of_sample_results_report.json`: `cacd154831a4e5652f032b0302baaaf50c7f5c542e3f65d785dd9c215f897815`
- `baseline_comparison_report.json`: `5229a373ec4d3e0b53699d3d48e73485fa37ada1370500875163d0839a2d964c`
- `calibration_report.json`: `c38cfed6a3ed76b2c01697cb48bd0cbfb6ee0d2bddea0b2b47a4db2a4e711ddc`
- `stability_analysis_report.json`: `49bbb9f0ad25fd9f6dc34170f3ba82a185ba73039f6ff2ed7eb584556d4984d0`
- `false_positive_false_negative_report.json`: `235fceef4ea8dfde34a5ac90f19b39c27b4d9cd79ec2782c12012f3d4a2c1369`
- `leakage_control_report.json`: `2044aca4d70def349ef6ef0bc4f33c3edc7c973c36712d0c183b3e864f908fcd`
- `data_quality_report.json`: `4c83db86a04677c363540530fa288315c43c13034600b79a6740629f67981c9e`
- `operator_review_summary.json`: `c45b1f8a0766bb58bc2dc3d544f33716374cd5f85b912683ea6a112d7a8d89e9`
- `execution_digest_manifest.json`: `00ada4437ac50715d8074763717e8dcec31f98ec8ccc46a6d55035da6128be3c`; its internal self-reference is explicitly non-applicable.

## Authority Boundaries And Non-Goals

- Predictive usefulness remains `not accepted`; acceptance ready/recommended/candidate created remain `False / False / False`.
- Profitability remains `not accepted`; acceptance ready/recommended remain `False / False`.
- Runtime migration approved/active remains `False / False`.
- Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- Automatic stitching, new strategy scoring, and trade recommendations remain `False`.
- No Massive.com / Polygon request, provider transport, market-data acquisition, dataset generation, or canonical-dataset regeneration occurred.
- No default dataset source, Strategy runtime, broker, or IBKR code was modified.

## Next Task Recommendation

- `Additional Predictive Evidence Results Review Package v1` must review these results before any predictive-usefulness reassessment candidate can be considered.
