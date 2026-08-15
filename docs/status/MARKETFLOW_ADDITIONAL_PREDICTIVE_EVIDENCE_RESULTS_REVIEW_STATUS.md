# MarketFlow Additional Predictive Evidence Results Review Status

## Branch And Commit

- Branch: `feature/additional-predictive-evidence-results-review-v1`.
- Base commit: `6b8f5d57a750d9c8e593002e719d333b80e88a84`.
- Implementation commit: `Add additional predictive evidence results review package` (recorded by Git after this document is staged).

## Review Artifact And Status

- Artifact kind: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE`.
- Schema: `additional_predictive_evidence_results_review_v1`.
- Review status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY`.
- Review digest: `167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8`.
- Checklist: `82 / 82` passed, `0` failed, `0` blockers.
- Operator review ready: `True`.
- Ready for a future predictive-usefulness reassessment candidate: `True`.
- Ready for predictive-usefulness acceptance: `False`.

## Source Predictive Evidence Execution

- Artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED` / `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_RESEARCH_ONLY`.
- Execution digest: `61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3`.
- Execution approval digest: `01cc79720ec9a27eb15a88214dfd5d152f5a6ae95082e7e13167239601c8afd9`.
- Execution-candidate review digest: `ab41b9e28693ca770c85a7e872d640f04b7c59c97b3b8eb40b28c9b101652ff7`.
- Execution-candidate digest: `d7f83a8b7be2be3a663ddb04097bf08b346071f70c9e770dd8f25e9fd9f4947e`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical-dataset freeze digest: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc`.
- Canonical-dataset generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Canonical records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Source profile: `RTH_FULL_SESSION_1D`.
- Date range/timeframe: `2022-01-01` through `2025-12-31` / `1d`.
- Universe/record count: `12 / 11946`.
- Data-quality status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Registry label: `RESEARCH_ONLY_NON_ACTIONABLE`.

## Target Universe

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- `META`: exactly `913` records, preserved without repair, inference, smoothing, normalization, backfill, or fabrication.
- Every non-META ticker: exactly `1003` records.

## Label Generation Review

- Seven forward-only label families are present.
- Coverage entries: `84`.
- Available/unavailable label values: `82854 / 768`.
- Unavailable reason: `label_unavailable_due_to_insufficient_future_bars`.
- Label-generation digest: `08e9aa9458c462dc3552fe25d6db9230d384228767848110bce76f8457e3eda3`.

## Feature Generation Review

- Feature families/fields/rows: `10 / 22 / 11946`.
- Feature coverage entries: `120`.
- Expected rolling-window null count: `1428`.
- Feature-generation digest: `ab543dc38aa75ea6a0bdc654a538bcb31d0081c8a1030fa1cf71665b23bcdd2d`.
- Future labels used as features: `False`.

## Walk-Forward Validation Review

- Fold count: `4`; shuffle: `False`.
- `2024_Q1`: `732` evaluation rows; majority accuracy `0.562842`.
- `2024_Q2`: `756` evaluation rows; majority accuracy `0.541005`.
- `2024_Q3`: `768` evaluation rows; majority accuracy `0.552083`.
- `2024_Q4`: `768` evaluation rows; majority accuracy `0.498698`.

## Out-Of-Sample Evaluation Review

- Holdout: `2025`; evaluation rows: `2988`.
- Majority-class accuracy: `0.539491`.
- Deterministic-random accuracy: `0.324967`.
- Previous-direction accuracy: `0.495984`.
- Zero-return accuracy: `0.001004`.
- Buy-and-hold reference-only accuracy: `0.539491`.
- Ticker cross-sectional accuracy: `0.502677`.

## Baseline, Metric, Calibration, Stability, And Leakage Review

- Baseline/metric-family counts: `6 / 9`.
- OOS up-vs-not-up Brier score: `0.24875351`.
- Stability evidence retains four walk-forward fold values and OOS values for all six baselines.
- Leakage-control status/failed controls: `PASS / 0`.
- Majority-class accuracy alone is not predictive-usefulness acceptance evidence.
- Buy-and-hold is a non-actionable comparison reference, not a trade recommendation.

## Data-Quality Review

- Status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Failures/warnings: `0 / 1`.
- Warning: `META` reduced record count preserved at exactly `913` records.

## Generated Output And Digest Manifest Review

- Ignored output root: `.marketflow/additional_predictive_evidence/expanded_universe_v1/`.
- Expected/actual/valid output count: `15 / 15 / 15`.
- All outputs use `RESEARCH_ONLY_NON_ACTIONABLE` and `ADDITIONAL_PREDICTIVE_EVIDENCE_RESEARCH_ONLY`.
- Fourteen non-self file digests match the execution digest manifest.
- The digest manifest's own entry is `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` with no declared SHA-256.
- A local SHA-256 is nevertheless bound for each of all 15 files, including the digest-manifest file.
- Digest mismatches: `0`.
- Raw provider payloads and API keys detected: `False / False`.

## Predictive Usefulness Boundary

- Results support future reassessment planning: `True`.
- Predictive usefulness remains `not accepted`.
- Acceptance ready/recommended/candidate created: `False / False / False`.
- No `PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE`, acceptance candidate, or acceptance artifact is created by this review.

## Profitability Boundary

- Profitability remains `not accepted`.
- Acceptance ready/recommended: `False / False`.
- No profitability acceptance is created.

## Runtime Boundary

- Runtime migration approved/active: `False / False`.
- Runtime, Strategy, paper trading, and broker execution: `NOT_AUTHORIZED`.
- Automatic stitching: `False`.
- No runtime authority or activation is created.

## Offline And Non-Execution Guardrails

- Provider requests and live transport in review: `False / False`.
- Market-data acquisition, dataset generation, and canonical-dataset regeneration in review: `False / False / False`.
- Predictive execution, label generation, feature generation, walk-forward validation, OOS evaluation, baseline comparison, and metric recomputation rerun in review: all `False`.
- New strategy scoring and trade recommendations: `False / False`.
- No `.env` or credential was inspected.
- No Strategy runtime, default dataset behavior, broker, or IBKR code was changed.

## Limitations

- Results are research-only and require operator interpretation.
- Predictive usefulness and profitability are not accepted.
- Runtime, Strategy, paper trading, and broker execution remain unauthorized.
- META's reduced record count remains a preserved source limitation.
- Operator review is required before a predictive-usefulness reassessment candidate.
- Any future acceptance or runtime migration requires a separate operator ceremony and authority chain.

## Next Gates

1. Additional predictive evidence results operator review.
2. Predictive Usefulness Reassessment Candidate v1.
3. Predictive usefulness reassessment review.
4. Predictive usefulness acceptance-readiness review.
5. A separate predictive-usefulness acceptance ceremony only if ready.
6. Separate profitability and runtime-migration chains only if later required and authorized.

## Next Task Recommendation

- `Predictive Usefulness Reassessment Candidate v1` is the next possible research-governance task; it remains future work and is not created here.
