# MarketFlow Label Objective Redesign v1 Plan

## Purpose

Create a deterministic, offline planning candidate that frames a future redesign of the predictive label objective and prediction target after two readiness gates remained not ready. The artifact is research-only and non-actionable.

## Source Operator Method Path Selection

- Source artifact/status: `PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTION` / `PREDICTIVE_EVIDENCE_OPERATOR_METHOD_PATH_SELECTED`.
- Bound selection digest: `2f771999ff5e31dbd959ea1a33b08852cda46913ff1b5dfc6fe17bc0853ee14a`.
- Selected path: `OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE`.
- The selection remains source evidence and does not itself authorize redesign or execution.

## Problem Basis

The original and refined readiness decisions remain not ready. Their preserved evidence reports weak or mixed signals, insufficient or mixed baseline outperformance, and low-to-mixed out-of-sample generalization. The objective is to plan diagnosis of label-to-decision alignment and target design before any further model or execution work.

## Diagnostic Hypotheses

The candidate records thirteen untested hypotheses covering tradeability alignment, horizon-feature mismatch, noisy or imbalanced thresholds, regime-insensitive absolute returns, weak daily direction, missing flat/no-trade zones, risk-adjusted and benchmark-relative targets, per-ticker calibration, global threshold mismatch, window-level class stability, late-window label availability, and preservation of the META limitation.

## Redesign Dimensions

Fourteen planned dimensions cover tradeability, horizon, return threshold, flat tolerance, class balance, absolute versus relative return, risk adjustment, drawdown avoidance, volatility regime, benchmark-relative performance, per-ticker calibration, global versus ticker-specific thresholds, late-window availability, and the META record limitation. Every dimension remains undesigned, unauthorized, and unexecuted.

## Planned Label Family Candidates

Ten candidate families cover flat-zone direction, redesigned return buckets, 5/10/20 multi-horizon targets, benchmark-relative return, volatility-adjusted return, drawdown avoidance, asymmetric risk/reward, regime-conditioned direction, per-ticker calibration, and a no-trade-zone class. All remain planned and ungenerated.

## Evaluation Questions

Ten unanswered questions test future design relevance: tradeable-decision alignment, horizon fit, noise reduction from flat zones, market-beta noise reduction, ticker calibration, risk-adjusted stability, drawdown signal, regime stability, walk-forward class balance, and the META availability limitation. This planning candidate performs no evaluation.

## Future Chain

1. Label Objective Redesign Candidate Operator Review Package v1.
2. Label Objective Redesign Approval Ceremony v1, if selected.
3. Label Objective Redesign Execution Candidate v1.
4. Label Objective Redesign Execution Approval v1, if selected.
5. Label Objective Redesign Execution v1.
6. Label Objective Redesign Results Review v1.
7. Additional Predictive Evidence Execution Candidate using redesigned labels, if results support it.
8. Additional Predictive Evidence Execution and Results Review, if separately approved.
9. Predictive Usefulness Reassessment and Readiness Review, only after new evidence.
10. Predictive Usefulness Acceptance Candidate, only if readiness passes.
11. Profitability review chain, if separately required.
12. Runtime migration chain, if ever separately authorized.

## Future Gates

The candidate records separate gates for operator review, redesign approval, execution candidacy, execution approval, execution, results review, any new-evidence execution and review, reassessment/readiness, acceptance candidacy, profitability review, and runtime migration. Recording a gate does not open it.

## Risk Controls

The candidate cannot authorize label generation or execution; accept predictive usefulness or profitability; authorize runtime, strategy, paper trading, or broker execution; generate recommendations; mutate the frozen dataset; repair META's reduced record count; or initiate more execution without operator approval. Every output remains research-only.

## Non-Goals And Guardrails

- No provider access, market-data acquisition, `.env` inspection, live transport, dataset regeneration, evidence rerun, label or feature generation, metric recomputation, model training, strategy scoring, recommendation generation, acceptance, profitability approval, runtime activation, or broker/IBKR change.
- Preserve the exact 12-ticker order, `11946` frozen records, records digest, and META's `913`-record limitation.
- Default validation remains deterministic, offline, credential-free, and isolated in pytest temporary directories.

## Next Task

- Label Objective Redesign Candidate v1 is completed.
- Label Objective Redesign Candidate Operator Review Package v1 is completed and digest-bound to the candidate.
- Label Objective Redesign Approval Ceremony v1 is implemented with explicit operator attestation and approval-only scope.
- Label Objective Redesign Execution Candidate v1 remains future work and requires a separate request.
- Label Objective Redesign execution remains future, unapproved, unauthorized, and unperformed.
- Predictive usefulness acceptance remains closed; profitability remains not accepted.
- Runtime activation remains future and separate.
