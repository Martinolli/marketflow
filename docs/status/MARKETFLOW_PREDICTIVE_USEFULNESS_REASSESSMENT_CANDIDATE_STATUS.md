# MarketFlow Predictive Usefulness Reassessment Candidate Status

## Branch And Commit

- Branch: `feature/predictive-usefulness-reassessment-candidate-v1`.
- Base commit: `0d21d4331bd82d597dc378961a38b7ff4d7a14a5`.
- Implementation commit: `Add predictive usefulness reassessment candidate` (recorded by Git after this document is staged).

## Candidate Artifact And Status

- Artifact kind: `PREDICTIVE_USEFULNESS_REASSESSMENT_CANDIDATE`.
- Schema: `predictive_usefulness_reassessment_candidate_v1`.
- Candidate status: `PREDICTIVE_USEFULNESS_REASSESSMENT_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `d1fb7dca18ff8b5565a3807be45b936d869e7fe9394af41c0b0ef125aeda4efe`.
- Checklist: `62 / 62` passed, `0` failed, `0` blockers.
- Ready for candidate operator review: `True`.
- Ready for the reassessment review itself: `False`.
- Ready for predictive-usefulness acceptance: `False`.

## Source Additional Predictive Evidence Results Review

- Results-review digest: `167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8`.
- Execution digest: `61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3`.
- Execution approval digest: `01cc79720ec9a27eb15a88214dfd5d152f5a6ae95082e7e13167239601c8afd9`.
- Execution-candidate review digest: `ab41b9e28693ca770c85a7e872d640f04b7c59c97b3b8eb40b28c9b101652ff7`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical-dataset freeze digest: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc`.
- Canonical-dataset generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Source profile: `RTH_FULL_SESSION_1D`.
- Date range/timeframe: `2022-01-01` through `2025-12-31` / `1d`.
- Universe/records: `12 / 11946`.
- Data quality: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Registry label: `RESEARCH_ONLY_NON_ACTIONABLE`.

## Target Universe

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- `META`: exactly `913` records with its reduced-count flag set.
- Every non-META ticker: exactly `1003` records.

## Evidence Summary

- Summary status: `READY_FOR_OPERATOR_REVIEW`.
- Label coverage entries: `84`; available/unavailable values: `82854 / 768`.
- Feature rows/fields: `11946 / 22`.
- Walk-forward folds: `4`; OOS evaluation rows: `2988`.
- Leakage status/failed controls: `PASS / 0`.
- Evidence supports future reassessment review: `True`.
- Evidence supports direct acceptance: `False`.
- Acceptance recommendation: `NOT_RECOMMENDED_AT_CANDIDATE_STAGE`.

## Performance Interpretation

- Walk-forward majority-accuracy range: `0.498698 to 0.562842`.
- Walk-forward stability: `MIXED_REQUIRES_OPERATOR_REVIEW`.
- OOS majority accuracy: `0.539491`.
- OOS previous-direction accuracy: `0.495984`.
- OOS ticker cross-sectional accuracy: `0.502677`.
- OOS Brier score: `0.24875351`.
- Performance signal: `REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE`.
- Baseline outperformance: `MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE`.
- These are reviewed facts and conservative classifications, not stronger inferred findings.

## Per-Ticker Reassessment Candidate Summary

- Twelve entries preserve the exact universe order.
- Each entry is `READY_FOR_OPERATOR_REVIEW`, `REVIEWED_RESEARCH_ONLY`, and digest-bound.
- Each entry keeps predictive usefulness and profitability `not accepted`.
- Each entry keeps runtime, Strategy, paper trading, and broker execution `NOT_AUTHORIZED`.
- META's digest-bound entry preserves `913` records and `meta_reduced_record_count_flag = true`; every other entry preserves `1003` and `false`.

## Reassessment Domains

- Label and feature coverage review.
- Walk-forward stability and OOS performance review.
- Baseline, calibration, stability, and false-positive/false-negative review.
- Leakage-control and data-quality review.
- META reduced-record-count review.
- Operator acceptance-boundary review.
- Every domain is `CANDIDATE_READY_FOR_OPERATOR_REVIEW`, `NOT_ACCEPTANCE`, and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Future Reassessment Chain

1. Predictive usefulness reassessment candidate operator review package.
2. Predictive usefulness reassessment review package.
3. Predictive usefulness acceptance-readiness review.
4. Predictive usefulness acceptance ceremony only if evidence is sufficient.
5. Profitability review chain if separately required.
6. Runtime migration chain if ever separately authorized.

## Future Gates

- Candidate operator review.
- Reassessment review.
- Acceptance-readiness review.
- Acceptance ceremony only if ready.
- Separate profitability review chain if required.
- Separate runtime migration chain if ever authorized.

## Risk Controls And Planned Outputs

- No acceptance may arise from this candidate or without a separate readiness review.
- No profitability acceptance, runtime source switch, automatic stitching, broker execution, paper trading, or trade recommendation is allowed.
- The frozen dataset must not be mutated and predictive evidence must not be rerun.
- Seven planned review templates remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Predictive Usefulness Boundary

- Candidate created/ready for operator review: `True / True`.
- Reassessment review created: `False`.
- Predictive usefulness remains `not accepted`.
- Acceptance ready/recommended/candidate created: `False / False / False`.
- No acceptance artifact is created.

## Profitability Boundary

- Profitability remains `not accepted`.
- Acceptance ready/recommended: `False / False`.
- No profitability acceptance is created.

## Runtime Boundary

- Runtime migration approved/active: `False / False`.
- Runtime, Strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- Automatic stitching, strategy scoring, and trade recommendations remain `False`.

## Offline Guardrails

- Provider requests, live transport, and market-data acquisition: `False`.
- Dataset generation and canonical-dataset regeneration: `False`.
- Predictive execution, label/feature generation, walk-forward/OOS evaluation, and metrics recomputation reruns: `False`.
- No `.env`, credential, provider transport, Strategy runtime, default dataset behavior, broker, or IBKR code was inspected or changed.

## Next Task Recommendation

- `Predictive Usefulness Reassessment Candidate Operator Review Package v1` remains the next separate task.
