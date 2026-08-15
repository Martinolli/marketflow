# MarketFlow Predictive Evidence Improvement v1 Plan

## Purpose

Plan research-only improvements in response to the failed predictive-usefulness acceptance-readiness criteria. This plan creates no execution, acceptance, profitability, or runtime authority.

## Source Acceptance Readiness Review

- Artifact/status/decision: `PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW` / `PREDICTIVE_USEFULNESS_ACCEPTANCE_READINESS_REVIEW_COMPLETED` / `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY`.
- Readiness-review digest: `d4ea4dc23590d9746727d5028116e2d0711fbc55dc8853f0b455d6ee4344a3e3`.
- Reason: `MIXED_STABILITY_AND_INSUFFICIENT_BASELINE_OUTPERFORMANCE`.

## Readiness Failure Summary And Evidence Basis

- Stability and baseline-outperformance consistency remain `FAIL_OR_NOT_MET`.
- Walk-forward accuracy range: `0.498698 to 0.562842`.
- OOS majority/previous-direction/cross-sectional accuracy: `0.539491 / 0.495984 / 0.502677`.
- OOS Brier score: `0.24875351`.
- Leakage status/failed controls: `PASS / 0`.

## Improvement Themes

- Improve feature signal quality, labels, baseline outperformance, walk-forward stability, OOS generalization, calibration, and error balance.
- Review cross-sectional signals, META limitation handling, data-quality flags, and model-family comparison planning.
- Every theme is planned, research-only, non-actionable, and not acceptance evidence.

## Refinement Options

- Review return thresholds, 5/10/20-session horizons, volatility regimes, and drawdown-risk labels.
- Add or refine VPA, relative-strength, cross-sectional, quality, and missingness features.
- Plan baseline/model comparison and improved walk-forward and stability policies.
- Every option requires separate operator review and execution approval.

## Future Improvement Chain And Gates

1. Candidate operator review package.
2. Feature/label refinement candidate, if selected.
3. Improved-evidence execution candidate.
4. Separate approval and execution.
5. Results review, reassessment rerun, and readiness rerun.
6. Acceptance candidate only if readiness later passes.
7. Separate profitability and runtime chains, if required and authorized.

All future gates remain distinct and closed until their prerequisite review or approval occurs.

## Risk Controls

- No improvement, refinement, feature generation, model comparison, or evidence rerun without separate approval.
- No acceptance while readiness is not met.
- No profitability acceptance, runtime migration, stitching, paper/broker execution, or recommendations.
- Preserve the frozen dataset and META's 913-record limitation.
- Keep all outputs research-only.

## Non-Goals

- Provider calls, market-data acquisition, dataset regeneration, label/feature generation, walk-forward/OOS execution, or metric recomputation.
- Model comparison execution, strategy scoring, or recommendations.
- Predictive-usefulness or profitability acceptance.
- Runtime, Strategy, paper, broker, or IBKR changes.

## Guardrails

- Bind the exact not-ready review and upstream digests.
- Use deterministic canonical JSON, semantic digests, strict validation, and no-overwrite output.
- Planned themes, options, and outputs do not imply execution or authority.

## Implementation Progress

- Predictive Evidence Improvement Candidate v1 is completed.
- Predictive Evidence Improvement Candidate Operator Review Package v1 is implemented and binds the candidate as source evidence.
- The operator review preserves all themes, options, per-ticker digests, future gates, controls, and planned-output boundaries.
- Feature/Label Refinement Plan Candidate v1 remains future work if selected.
- Additional Predictive Evidence Execution Candidate remains future and requires a separate chain.
- Predictive usefulness acceptance remains closed; profitability remains `not accepted`; runtime activation remains future and separate.

## Next Tasks

1. Feature/Label Refinement Plan Candidate v1, if selected.
2. Additional Predictive Evidence Execution Candidate for improved evidence, only after the required reviews.
3. Separate execution approval and execution, only if later explicitly authorized.
