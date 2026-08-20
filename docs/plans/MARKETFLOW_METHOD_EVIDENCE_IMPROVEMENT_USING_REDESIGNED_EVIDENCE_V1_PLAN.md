# MarketFlow Method / Evidence Improvement Using Redesigned Evidence v1 Plan

## Purpose

Create a deterministic, offline, digest-bound candidate that presents method and evidence improvement paths after the redesigned-evidence acceptance-readiness review returned `NOT READY`. This phase is candidate-only: it neither selects a path nor approves or executes improvement work.

## Source Acceptance-Readiness Review

- Artifact/status: `PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE` / `PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_USING_REDESIGNED_EVIDENCE_COMPLETED`.
- Decision/reason: `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REDESIGNED_EVIDENCE` / `SMALL_CROSS_SECTIONAL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_AND_STABILITY_REQUIRES_REVIEW`.
- Bound digest: `6c6e5019a5ce312b12e4b792ce989524ba5bf16f82b5f6e532ec742f99eba4da`.
- The reassessment, results-review, execution, feature-label matrix, feature-values, redesigned-label-values, research-registry, and records digests remain bound.

## Dataset And Universe

- Dataset: `expanded_universe_canonical_dataset_v1`; `RTH_FULL_SESSION_1D`; `1d`; `2022-01-01` through `2025-12-31`.
- Ordered universe: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- Total records: `11946`; META: `913`; every other ticker: `1003`.
- The META limitation is preserved and must not be repaired, inferred, smoothed, normalized, or fabricated.

## Problem Basis

- Cross-sectional OOS accuracy improves on majority by only `0.00309917`.
- The regularized local model matches the majority baseline with a delta of `0.00000000`.
- Signal, baseline, local-model, and stability readiness are `NOT_READY`.
- Calibration requires operator review and optional model coverage is not met.
- Additional evidence or method improvement is required before the acceptance path can be reconsidered.

## Improvement Themes

The candidate presents 11 planning-only themes: label-objective refinement, feature-family review, model-family expansion, baseline-outperformance criteria, stability-protocol review, calibration review, cross-sectional signal review, per-ticker diagnostics, META limitation handling, optional-model coverage, and acceptance-threshold policy.

Every theme is `PLANNED_NOT_EXECUTED`, requires approval before execution, is not execution-authorized, and is research-only and non-actionable.

## Improvement Options

The candidate offers eight options for operator review, from reviewing the label objective through retaining the current evidence and stopping the acceptance path. No option is selected, approved, or executed. Option A, `OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION`, is recommended because the OOS edge is small and the local model matches the majority baseline.

## Diagnostic Questions

Ten diagnostic questions cover label structure, per-ticker and regime generalization, feature explanation, horizons and thresholds, calibration, walk-forward stability, optional models, the META limitation, explicit acceptance thresholds, and whether the candidate path should stop. All remain `NOT_ANSWERED` and require separate review or execution.

## Future Chain

1. Method / Evidence Improvement Candidate Operator Review Using Redesigned Evidence v1.
2. Method / Evidence Improvement Path Selection Using Redesigned Evidence v1, if selected.
3. A selected label-objective, feature, model, calibration, or evidence-planning candidate.
4. Separate improved-evidence approval and execution, if approved.
5. Predictive-usefulness reassessment rerun after new evidence.
6. Acceptance-readiness rerun only if reassessment supports it.
7. Predictive-usefulness acceptance candidate only if readiness passes.
8. Separate profitability review, if required.
9. Separate runtime migration chain, if ever authorized.

## Future Gates

Path selection, any specific improvement candidate, improved-evidence planning, approval, execution, reassessment, acceptance-readiness, acceptance candidacy, profitability, and runtime migration each remain separate gates.

## Risk Controls

- Do not approve or execute improvement from this candidate.
- Do not generate new evidence, rerun predictive evidence, recompute metrics, or train models.
- Do not mutate frozen dataset, redesigned-label, feature, or predictive-evidence outputs.
- Do not accept predictive usefulness or profitability and do not create an acceptance candidate.
- Do not authorize runtime, strategy, paper trading, broker execution, or trade recommendations.
- Preserve the META record-count limitation and label every output research-only.

## Non-Goals

This plan does not fetch provider data, inspect credentials, generate datasets, regenerate labels or features, execute predictive evidence, select an option, answer diagnostic questions, approve an improvement, create improved-evidence planning, accept usefulness or profitability, activate runtime, or generate recommendations.

## Guardrails

- Default tests remain deterministic, offline, credential-free, and network-free.
- Candidate artifacts are canonical and digest-bound; generated `.marketflow` outputs remain ignored and untracked.
- MarketFlow remains research and decision-support software, not execution software.

## Next Task

The method/evidence improvement candidate is complete, and its operator review package is implemented. The candidate remains the source evidence for that offline review.

`Method / Evidence Improvement Path Selection Using Redesigned Evidence v1` remains future work if an option is separately selected. Improvement approval or execution remains future and separately gated. Predictive-usefulness acceptance remains closed, profitability remains not accepted, and runtime activation remains future and separate.
