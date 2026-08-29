# MarketFlow Repository Integration Branch Validation Failure Remediation Approval v1 Plan

## Purpose

Create an offline, attestation-bound approval selecting the reviewed frozen
ignored-evidence staging package for future remediation execution. Approval is
not remediation execution, evidence staging, integration retry, or results review.

## Source Operator Review

The approval binds operator-review digest
`f32d7ded083256f4301903de41e1fdf06562b4af0e5bd0fc2c75685d4fd8a301`,
candidate digest `2d45ef960b45d6a81b6e494b77a44f3dba482567e973e83999844ce9ce351fc2`,
diagnosis digest `a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947`,
and merge-strategy approval digest
`34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.

## Operator Attestation

Require the exact non-secret phrase:

`APPROVE INTEGRATION BRANCH VALIDATION FAILURE REMEDIATION PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE MARKETFLOW STAGE FROZEN IGNORED EVIDENCE ROOTS DETACHED INTEGRATION WORKTREE ACQUISITION MANIFEST REQUIRED NO REGENERATION NO MARKETFLOW COMMIT NO RETRY REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW`

The attestation must confirm all four source digests, attempted execution commit,
integration branch and head, authoritative failed pytest, diagnostic-only rerun,
selected package, approval-only scope, and every no-execution, no-staging,
no-retry, repository, provider, data, model, acceptance, runtime, broker, secret,
and raw-payload boundary. Partial or altered attestations fail closed.

## Failure Summary and Root Cause

The first integration run remains authoritative at
`24481 passed, 1300 failed, 500 errors, 7 skipped`. The later passing run remains
diagnostic-only because it executed from the feature worktree. The detached
integration worktree lacked the ignored frozen acquisition-evidence root,
including `acquisition_provider_evidence_run_manifest.json`.

## Approval Scope

`REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW`

## Selected Remediation Package

Approve `PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE`
for future remediation execution only. Selection, approval, authorization, and
readiness become true; execution remains false.

## Approved Future Requirements

Approve all sixteen candidate controls: complete evidence-root inventory;
acquisition manifest availability; read-only source use; untracked and
uncommitted staging; no regeneration; manifest and digest verification; ready
digest acceptance and blocked digest rejection; detached-worktree pytest;
recorded working directory; wrong-worktree rejection; and separate remediation,
retry, and results-review governance.

## Approved Future Plan

Approve the ten-step source plan for future execution only: inventory roots,
verify source evidence and manifests, stage read-only untracked evidence, run the
precheck and full suite from the detached integration worktree, record paths and
digests, avoid `.marketflow` commits, require a passing authoritative retry, and
create separate retry execution/results-review artifacts. Status remains
`NOT_EXECUTED`.

## Supporting and Blocked Packages

Read-only evidence-root parameterization, a missing-root precheck, and minimal
committed acquisition-review fixtures remain `AVAILABLE_NOT_SELECTED`.
Acquisition-evidence regeneration and accepting the wrong-worktree rerun remain
`BLOCKED_NOT_APPROVED`.

## Next Chain and Gates

Separately invoked remediation execution and results review come first. Only
after remediation review may the integration retry candidate, approval,
execution, and results review proceed. Main Merge Approval is possible only
after a passing retry review. All seven matching gates remain separately closed.

## Risk Controls and Guardrails

The forty-one controls prohibit current remediation, evidence staging/copy,
`.marketflow` commits, regeneration, retry, results review, protected-ref or tag
changes, provider/data/model actions, recommendations, acceptance, runtime, and
broker authority. They preserve the authoritative failure, diagnostic-only
rerun, blocked digest, integration branch, archive evidence, published tags,
`origin/main`, and META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_V1`
