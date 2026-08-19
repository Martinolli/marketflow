# MarketFlow Additional Predictive Evidence Results Review Using Redesigned Labels Status

## Review Artifact

- Artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS` / `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_LABELS_READY`.
- Schema: `additional_predictive_evidence_results_review_using_redesigned_labels_v1`.
- Review digest: `90bc6627a315d1de48976c42ad88c93923ae9b2f43335187f0e9afdccf73e2ed`.
- Review checklist: `71 / 71` passed, `0` failed, `0` blockers.
- The package was built offline by inspecting and hashing the existing ignored execution outputs. It did not rerun predictive evidence or recompute any result.

## Source Execution

- Source artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS` / `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY`.
- Execution digest: `8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b`.
- Feature/label matrix digest: `275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad`.
- Execution approval digest: `cc45d6692f1f249cc76554f7019f148c8510efedeade22adb3ccb3fcbc54fe96`.
- All 13 expected files were present. The 12 non-self hashes matched the source digest manifest, and the digest manifest preserved its explicit `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` null policy.

## Dataset, Labels, Features, And Matrix

- Dataset: `expanded_universe_canonical_dataset_v1`; ordered 12-ticker universe `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Canonical records: `11946`; META remains `913`, while every other ticker remains `1003`.
- Redesigned labels: `143352` rows, `142200` available, `1152` unavailable.
- Features: `203082` rows, `190848` available, `12234` unavailable.
- Matrix: `143352` rows, `142200` evaluable, `1152` unavailable targets.
- Matrix inspection confirmed research-only/non-actionable labels and exclusion of future labels, forward returns, label values, and threshold values from feature inputs.

## Results Review

- Four chronological expanding walk-forward folds were verified, followed by the 2025 OOS holdout with `34848` evaluated rows.
- Majority OOS accuracy/macro F1/Brier: `0.58626033 / 0.21557412 / 0.04867526`.
- Ticker cross-sectional OOS accuracy/macro F1/Brier: `0.58935950 / 0.28155252 / 0.04831065`.
- Regularized local-model OOS accuracy/macro F1/Brier: `0.58626033 / 0.21557412 / 0.04867526`.
- The cross-sectional accuracy delta versus majority is `0.00309917`: a small research-only edge that requires separate reassessment and is not acceptance evidence.
- The local model delta versus majority is `0.00000000`; the local model did not outperform the majority baseline.
- Optional tree and ensemble families remain `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`.
- Leakage controls remain `PASS` with `0` failed controls and a horizon-aware training embargo.

## Interpretation And Limitations

- Predictive evidence interpretation: `GENERATED_RESEARCH_ONLY`.
- Baseline interpretation: `SMALL_CROSS_SECTIONAL_EDGE_NOT_ACCEPTANCE_EVIDENCE`.
- Local-model interpretation: `MATCHES_MAJORITY_BASELINE_NOT_ACCEPTANCE_EVIDENCE`.
- Stability interpretation: `REQUIRES_REASSESSMENT`.
- Predictive usefulness remains `not accepted` and requires a separate reassessment package.
- Profitability was not evaluated and remains `not accepted`.
- META's reduced record count, unavailable optional model families, and the need for operator review are explicit limitations.

## Authority Boundary

- This review sets only `additional_predictive_evidence_results_review_created`, `additional_predictive_evidence_results_review_ready`, and `ready_for_predictive_usefulness_reassessment_using_redesigned_evidence` to true.
- It does not create a predictive-usefulness reassessment, acceptance-readiness review, acceptance candidate, usefulness acceptance, profitability acceptance, runtime migration, strategy authority, or trade recommendations.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, live transport, market-data acquisition, dataset regeneration, label regeneration, feature regeneration, predictive-evidence rerun, metric recomputation, model training, scoring, runtime, broker, or trading action occurred in review.

## Next Chain

1. Predictive Usefulness Reassessment Using Redesigned Evidence v1.
2. Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1.
3. Predictive Usefulness Acceptance Candidate, only if readiness passes.
4. Profitability review chain, if separately required.
5. Runtime migration chain, if ever separately authorized.

## Follow-On Reassessment

- Follow-on `Predictive Usefulness Reassessment Using Redesigned Evidence v1` is implemented as a separate offline, digest-bound package.
- This results review remains source evidence for the reassessment.
- The reassessment does not accept predictive usefulness, approve profitability, authorize runtime, or create trade recommendations.
- Predictive Usefulness Acceptance Readiness Review Using Redesigned Evidence v1 remains the next future, separate gate.
