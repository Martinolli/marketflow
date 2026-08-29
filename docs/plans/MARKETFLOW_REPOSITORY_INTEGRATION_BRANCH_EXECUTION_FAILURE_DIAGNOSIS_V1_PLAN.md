# MarketFlow Repository Integration Branch Execution Failure Diagnosis v1 Plan

## Purpose

Create a deterministic offline diagnosis of the failed first integration pytest
gate. Preserve the failure as authoritative and prepare only a future remediation
recommendation.

## Source Merge-Strategy Approval

- Approval artifact: `MARKETFLOW_REPOSITORY_MERGE_STRATEGY_APPROVED`.
- Approval digest: `34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.
- Selected package: `PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION`.

## Attempted Execution and Integration Branch State

- Attempted execution branch/commit:
  `feature/marketflow-repository-integration-branch-execution-v1` /
  `9d3dbc488747a0e17921bd4dcab7be2fadefc5ba`.
- Integration branch/head:
  `integration/marketflow-terminal-evidence-stack-validation-v1` /
  `220fbc220365fce9cae13ab4853cddff118c0187`.
- Base/source:
  `eda58d9a56656641d4e0c2a80a6e572b6e949fc2` /
  `71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`.
- Merge method: `NO_FF_MERGE_COMMIT`.

## Authoritative Pytest Failure

The first integration run reported `24481 passed, 1300 failed, 500 errors,
7 skipped`. It remains the authoritative execution gate. No successful execution
or validation digest may be issued.

## Later Diagnostic Rerun

The recorded `26842 passed, 7 skipped` rerun does not override the failure. Its
shell created a detached worktree but did not change pytest's working directory,
so pytest ran on the feature worktree rather than the preserved integration
worktree.

## Representative Failure and Root Cause

- Required frozen ready-package digest: `57c0a06e...`.
- Actual blocked-package digest: `783e0013...`.
- Missing input: `acquisition_provider_evidence_run_manifest.json`.
- The integration worktree intentionally contains tracked files only; ignored
  `.marketflow/acquisition_provider_evidence/expanded_universe_v1` evidence is
  absent there.
- The acquisition evidence review builder therefore emits its deterministic
  missing-output package, while acquisition-generation approval requires the
  frozen ready-package digest.

## Diagnosis Domains

The artifact records failure-gate status, later-rerun status, digest mismatch,
state/order suspicion, source-constant consistency, pytest isolation, local-only
integration status, main protection, authority boundaries, remediation direction,
evidence-root dependency, and rerun working-directory trace.

## Root-Cause Questions

The artifact preserves the required diagnostic questions about the first test,
digest producers, ordering, environment, caches, branch content, historical
constants, and deterministic repair. Confirmed findings answer the evidence-root
and rerun-working-directory portions; remediation design remains deliberately
open.

## Recommendation

- Next task: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1`.
- Status: `FUTURE_CANDIDATE_NOT_CREATED`.
- Action: `CREATE_REMEDIATION_CANDIDATE_FOR_DIGEST_MISMATCH_AND_STATE_ORDER_DEPENDENCE`.
- Integration results review remains blocked; retry is not currently allowed.

## Next Chain

1. Remediation Candidate v1.
2. Remediation Candidate Operator Review v1.
3. Remediation Approval v1, if selected.
4. Remediation Execution v1, if approved.
5. Remediation Results Review v1.
6. Integration Retry Candidate v1 after remediation review.
7. Integration Retry Approval v1, if selected.
8. Integration Retry Execution v1, if approved.
9. Integration Retry Results Review v1.
10. Main Merge Approval only if retry review passes.

## Next Gates

The gates run from `integration_failure_remediation_candidate` through
`integration_branch_retry_results_review`, ending with
`main_merge_approval_if_retry_passes`. None is opened by diagnosis.

## Risk Controls and Guardrails

Diagnosis does not retry integration, create results review, generate successful
execution/validation digests, modify or push integration/main, delete branches,
prune or force-update refs, mutate tags or `.marketflow`, or perform provider,
data, metric, model, scoring, recommendation, runtime, broker, or trading work.
The integration branch, terminal archive evidence, published governance tags,
and META's preserved limitation remain unchanged.

## Non-Goals

No remediation implementation, retry, results review, main merge approval,
cleanup candidate, predictive/profitability acceptance, or runtime activation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1`.
