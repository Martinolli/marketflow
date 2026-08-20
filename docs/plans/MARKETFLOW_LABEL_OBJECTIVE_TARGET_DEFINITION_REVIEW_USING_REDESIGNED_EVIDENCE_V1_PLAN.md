# MarketFlow Label Objective / Target Definition Review Using Redesigned Evidence v1 Plan

## Purpose

Create a deterministic, offline, digest-bound candidate for reviewing whether the current label objective and target definition explain the redesigned-evidence `NOT READY` result. This phase creates only a candidate; it does not approve or execute review, regenerate labels, or create targets.

## Source Method / Evidence Path Selection

- Source artifact/scope: `METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTED_USING_REDESIGNED_EVIDENCE` / `METHOD_EVIDENCE_IMPROVEMENT_PATH_SELECTION_ONLY`.
- Bound digest: `d56519f9eb9dbb3249a365893db080d65fee8fcccbea2a8f0839300f8d006c22`.
- Selected option: `OPTION_A_REVIEW_LABEL_OBJECTIVE_AND_TARGET_DEFINITION`.

## Dataset And Universe

- Dataset: `expanded_universe_canonical_dataset_v1`; `RTH_FULL_SESSION_1D`; `1d`; `2022-01-01` through `2025-12-31`; `11946` records.
- Ordered universe: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- META remains `913`; every other ticker remains `1003`. The limitation must not be repaired, inferred, smoothed, normalized, or fabricated.

## Problem Basis

- Cross-sectional OOS accuracy exceeds majority by only `0.00309917`; the local model matches majority with delta `0`.
- Signal, baseline, local-model, and stability readiness remain `NOT_READY`.
- Calibration requires operator review and optional model coverage remains unmet.
- The label objective and signal definition must be reviewed before more execution.

## Review Dimensions

Twelve planned dimensions cover tradeable-signal alignment, majority-class structure, cross-sectional edge materiality, local-model equivalence, horizon noise, threshold materiality, class balance, per-ticker behavior, the META limitation, calibration relevance, acceptance prerequisites, and the stop/continue decision. Each is `PLANNED_NOT_EXECUTED`, approval-gated, research-only, and non-actionable.

## Current Label Family Review Plan

The candidate lists ten current families: direction with a flat zone, return buckets, 5/10/20 horizons, benchmark-relative return, volatility-adjusted return, drawdown avoidance, asymmetric risk/reward, regime-conditioned direction, per-ticker calibration, and a no-trade class. Review is planned only; regeneration and target-definition changes remain unauthorized.

## Diagnostic Questions

Ten unanswered questions test signal versus majority membership, edge materiality, target-versus-feature diagnosis, horizon alignment, threshold sensitivity, class balance, global versus per-ticker targets, the META limitation, acceptance prerequisites, and whether to retain, modify, or retire the current target.

## Decision Options

Seven unselected future options cover retaining the current objective, refining thresholds or horizons, redefining the objective, splitting by ticker/regime, adding abstention, or stopping the acceptance path pending stronger evidence. None is approved or executed and none creates labels.

## Future Chain

1. Candidate operator review using redesigned evidence.
2. Review approval, if selected.
3. Review execution and results review.
4. Optional redesign or threshold/horizon refinement candidate.
5. Optional improved-evidence planning and separately approved execution.
6. Reassessment and acceptance-readiness reruns only after new evidence.
7. Acceptance candidacy only if readiness passes.
8. Separate profitability and runtime chains, if ever authorized.

## Future Gates

Operator review, approval, execution, results review, redesign/refinement, improved-evidence planning and execution, predictive reassessment/readiness, acceptance, profitability, and runtime migration remain separate gates.

## Risk Controls

- Do not approve or execute review from this candidate.
- Do not regenerate labels, create targets or evidence, rerun predictive evidence, recompute metrics, or train models.
- Do not mutate frozen dataset, label, feature, or predictive-evidence outputs.
- Do not accept predictive usefulness or profitability or create an acceptance candidate.
- Do not authorize runtime, strategy, paper trading, broker execution, or recommendations.
- Preserve the META limitation and keep all outputs research-only.

## Non-Goals

This plan does not call providers, inspect credentials, acquire data, regenerate datasets, labels, or features, execute predictive evidence, answer diagnostic questions, select a target decision, approve review, create new targets, accept usefulness or profitability, activate runtime, or generate recommendations.

## Guardrails

- Default tests remain deterministic, offline, credential-free, and network-free.
- Candidate artifacts are canonical and digest-bound; generated `.marketflow` outputs remain ignored and untracked.
- MarketFlow remains research and decision-support software, not execution software.

## Next Task

The label-objective/target-definition review candidate is complete, and its operator review package is implemented. The candidate remains source evidence for that offline review.

Review approval remains future work if selected; review execution remains future and separately gated. Label regeneration and new-target creation remain closed, predictive-usefulness acceptance remains closed, profitability remains not accepted, and runtime activation remains future and separate.
