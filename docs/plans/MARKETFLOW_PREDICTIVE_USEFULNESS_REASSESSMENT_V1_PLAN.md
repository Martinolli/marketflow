# MarketFlow Predictive Usefulness Reassessment v1 Plan

## Purpose

Organize the completed additional predictive evidence results review into a deterministic, research-only candidate, candidate operator review, and reassessment review. The completed reassessment review creates no predictive-usefulness acceptance, profitability acceptance, or runtime authority.

## Source Additional Predictive Evidence Results Review

- Results-review artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE` / `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY`.
- Results-review digest: `167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8`.
- Execution/approval digests: `61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3` / `01cc79720ec9a27eb15a88214dfd5d152f5a6ae95082e7e13167239601c8afd9`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical freeze/records digests: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Range/profile/timeframe: `2022-01-01` through `2025-12-31` / `RTH_FULL_SESSION_1D` / `1d`.
- Universe/records: `12 / 11946`.
- META remains exactly `913`; every other ticker remains exactly `1003`.
- Quality/label: `PASS_WITH_PRESERVED_SOURCE_LIMITATION` / `RESEARCH_ONLY_NON_ACTIONABLE`.

## Evidence Summary

- Label coverage entries and available/unavailable values: `84`, `82854 / 768`.
- Feature rows/fields: `11946 / 22`.
- Walk-forward folds/OOS rows: `4 / 2988`.
- Leakage status/failed controls: `PASS / 0`.
- Evidence supports a future operator reassessment review but not direct acceptance.

## Performance Interpretation

- Walk-forward majority accuracy spans `0.498698 to 0.562842` and is `MIXED_REQUIRES_OPERATOR_REVIEW`.
- OOS majority, previous-direction, and ticker cross-sectional accuracies are `0.539491`, `0.495984`, and `0.502677`.
- OOS Brier score is `0.24875351`.
- Performance remains `REVIEW_REQUIRED_NOT_ACCEPTANCE_EVIDENCE`.
- Baseline outperformance remains `MIXED_OR_INSUFFICIENT_FOR_ACCEPTANCE`.

## Reassessment Domains

- Label and feature coverage.
- Walk-forward stability and OOS performance.
- Baseline comparison, calibration, stability analysis, and false-positive/false-negative review.
- Leakage controls, data quality, and META reduced-record-count handling.
- Operator acceptance-boundary review.
- Every domain remains candidate-only, not acceptance, and research-only non-actionable.

## Future Reassessment Chain

1. Predictive usefulness reassessment candidate operator review package.
2. Predictive usefulness reassessment review package.
3. Predictive usefulness acceptance-readiness review.
4. Predictive usefulness acceptance ceremony only if ready.
5. Separate profitability review chain if required.
6. Separate runtime migration chain if ever authorized.

## Future Gates

- `predictive_usefulness_reassessment_candidate_operator_review`
- `predictive_usefulness_reassessment_review`
- `predictive_usefulness_acceptance_readiness_review`
- `predictive_usefulness_acceptance_ceremony_if_ready`
- `profitability_review_chain_if_required`
- `runtime_migration_chain_if_ever_authorized`

## Risk Controls

- No predictive-usefulness acceptance from the candidate or without a readiness review.
- No profitability acceptance without separate review.
- No runtime source switch, automatic stitching, broker execution, paper trading, or trade recommendations.
- Do not mutate the frozen canonical dataset or rerun predictive evidence.
- Keep all planned outputs research-only and not generated.

## Non-Goals

- Provider calls, market-data acquisition, dataset regeneration, predictive reruns, label/feature regeneration, metrics recomputation, strategy scoring, or recommendations.
- Predictive-usefulness or profitability acceptance.
- Runtime migration, Strategy changes, paper/broker execution, or IBKR changes.

## Guardrails

- The candidate is deterministic, digest-bound, canonical, offline, and no-overwrite.
- Each ticker entry has a deterministic semantic digest and preserves the exact frozen record count.
- Planned review outputs remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Operator review remains required before any later reassessment review or acceptance-readiness step.

## Implementation Progress

- Predictive Usefulness Reassessment Candidate v1 is completed.
- Predictive Usefulness Reassessment Candidate Operator Review Package v1 is completed.
- Predictive Usefulness Reassessment Review Package v1 is implemented and binds the candidate review as source evidence.
- The reassessment review preserves all evidence, per-ticker counts and digests, domains, gates, controls, and planned-output boundaries.
- It is ready only for the separate Predictive Usefulness Acceptance Readiness Review v1.
- Predictive Usefulness Acceptance Readiness Review v1 remains future work.
- Predictive Usefulness Acceptance Ceremony v1 remains future work only if ready.
- Profitability remains `not accepted`; runtime activation remains future and separate.

## Next Tasks

1. Predictive Usefulness Acceptance Readiness Review v1.
2. Predictive Usefulness Acceptance Candidate v1, only if readiness supports it.
3. Predictive Usefulness Acceptance Ceremony v1, only if ready and explicitly approved.
4. Separate profitability and runtime-migration chains, only if later required and authorized.
