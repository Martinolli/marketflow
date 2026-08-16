# MarketFlow Predictive Evidence Method Path Selection v1 Plan

## Purpose

Record an explicit, non-secret operator selection of the next predictive-evidence planning path after the diagnosis-only method review. Selection opens only a future candidate gate and does not create the candidate or authorize execution.

## Source Method Diagnostic Review

- Source artifact/status: `PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE` / `PREDICTIVE_EVIDENCE_METHOD_DIAGNOSTIC_REVIEW_PACKAGE_READY`.
- Source digest: `416d0ce614f7bb034b473029e8a98b1d9b94adcde4204b986b898fcbb99c2b51`.
- Source conclusion: `METHOD_REVIEW_REQUIRED_BEFORE_MORE_EXECUTION` after two not-ready readiness gates.
- Source recommendation: `OPERATOR_METHOD_PATH_SELECTION`.

## Method Options

- `OPTION_A_PAUSE_AND_ARCHIVE_RESEARCH_CHAIN`: `NOT_SELECTED`.
- `OPTION_B_METHOD_DIAGNOSTIC_REVIEW`: `COMPLETED`.
- `OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE`: `SELECTED_FOR_FUTURE_CANDIDATE_ONLY`.
- Options D, E, and F: `NOT_SELECTED`.
- `OPTION_G_ACCEPTANCE_CANDIDATE`: `NOT_ALLOWED_CURRENTLY`.

## Selected Path

- Selected method path: `OPTION_C_LABEL_OBJECTIVE_REDESIGN_CANDIDATE`.
- Selected next artifact kind: `LABEL_OBJECTIVE_REDESIGN_CANDIDATE`.
- Selection reason: `LABEL_OBJECTIVE_AND_PREDICTION_TARGET_MUST_BE_DIAGNOSED_BEFORE_MORE_MODEL_OR_EXECUTION_WORK`.
- Selection basis: `TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE`.
- Ready for a future candidate: `True`; candidate created: `False`; execution authorized: `False`.

## Operator Attestation Requirement

- Require decision `SELECT_METHOD_PATH_LABEL_OBJECTIVE_REDESIGN_CANDIDATE` and the exact 12-ticker selection phrase ending in `METHOD_PATH_SELECTION_ONLY`.
- Require a non-secret operator reference and UTC timestamp.
- Confirm the method-diagnostic, planning-tree, readiness, registry, and records digests plus the exact universe and count.
- Confirm both not-ready decisions and every no-execution, no-acceptance, no-profitability, no-runtime, no-strategy, no-paper, no-broker, no-recommendation, no-secret, and no-raw-payload boundary.
- Reject any missing, false, reordered, or mismatched confirmation.

## Selection Boundaries

- The selection scope is `METHOD_PATH_SELECTION_ONLY_NOT_EXECUTION`.
- Selection is not candidate creation, candidate review, approval, execution, new evidence, acceptance, profitability, or runtime migration.
- Predictive usefulness and profitability remain `not accepted`; runtime, strategy, paper, and broker remain `NOT_AUTHORIZED`.

## Next Chain

1. Label Objective Redesign Candidate v1.
2. Label Objective Redesign Candidate Operator Review Package v1.
3. Label Objective Redesign Approval Ceremony v1, if selected.
4. Label Objective Redesign Execution Candidate v1.
5. Future evidence execution chain only after separate approval.
6. Predictive usefulness reassessment/readiness only after new evidence review.
7. Acceptance candidate only if readiness passes.
8. Profitability only if separately required.
9. Runtime migration only if separately authorized.

## Risk Controls

- Selection does not create the redesign candidate or authorize execution.
- Selection does not accept predictive usefulness or profitability.
- Selection does not authorize runtime, strategy, paper trading, broker execution, or recommendations.
- Acceptance remains unavailable; preserve the frozen dataset and META limitation.
- All outputs remain research-only and the next candidate requires its own operator review.

## Non-Goals

- Creating or reviewing the Label Objective Redesign Candidate.
- Provider access, acquisition, regeneration, predictive reruns, metrics, model training, or strategy scoring.
- Predictive-usefulness or profitability acceptance.
- Runtime, strategy, paper, broker, or trade-recommendation authorization.

## Guardrails

- Bind all requested evidence digests and exact attestation confirmations.
- Preserve exact universe order, record counts, evidence comparison, and both not-ready decisions.
- Use deterministic canonical JSON, strict fail-closed validation, and no-overwrite output writing.
- Do not inspect `.env`, store API keys, commit raw payloads, or track `.marketflow` outputs.

## Next Task

- `Label Objective Redesign Candidate v1`, only if separately requested.
