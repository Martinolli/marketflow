# MarketFlow Repository Integration Branch Validation Failure Remediation Candidate Operator Review v1 Plan

## Purpose

Create an offline, digest-bound operator review of the integration validation
failure remediation candidate. Review planning evidence without selecting,
approving, authorizing, or executing a remediation package.

## Source Remediation Candidate

- Candidate digest: `2d45ef960b45d6a81b6e494b77a44f3dba482567e973e83999844ce9ce351fc2`.
- Diagnosis digest: `a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947`.
- Approval digest: `34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.
- Attempted execution commit: `9d3dbc488747a0e17921bd4dcab7be2fadefc5ba`.
- Integration head: `220fbc220365fce9cae13ab4853cddff118c0187`.

## Failure Summary

The authoritative integration run remains
`24481 passed, 1300 failed, 500 errors, 7 skipped`. The later
`26842 passed, 7 skipped` run was launched from the feature worktree and remains
diagnostic-only. It cannot override the failed gate.

## Root Cause Review

The detached integration worktree lacked the ignored frozen acquisition
evidence root, including `acquisition_provider_evidence_run_manifest.json`.
This produced blocked digest prefix `783e0013` rather than ready prefix
`57c0a06e`.

## Review Scope

`REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY`

## Reviewed Remediation Philosophy

Future integration validation must run from the detached integration worktree
with required ignored frozen evidence available read-only. It must not
regenerate evidence, commit `.marketflow`, weaken digest checks, or accept a
wrong-worktree rerun. This review is `REVIEWED_PLANNING_ONLY`.

## Reviewed Remediation Packages

1. Frozen ignored-evidence staging — reviewed recommended, not selected.
2. Parameterized read-only evidence root — reviewed available, not selected.
3. Fail-closed missing-root precheck — reviewed available, not selected.
4. Minimal committed acquisition-review fixtures — reviewed available, not selected.
5. Acquisition-evidence regeneration — reviewed blocked and not recommended.
6. Accepting the later rerun — reviewed blocked and not allowed.

Every package remains unselected, unapproved, and unexecuted.

## Reviewed Remediation Requirements

All sixteen requirements are `REVIEWED_REQUIRED_FOR_FUTURE_REMEDIATION` and
`NOT_EXECUTED`. They cover evidence inventory, source existence, read-only use,
untracked staging, no commits or regeneration, manifest and digest verification,
detached-worktree pytest, recorded working directory, wrong-worktree rejection,
and separate remediation and retry governance.

## Reviewed Future Remediation Plan

All ten source steps are `REVIEWED_PLANNED_NOT_EXECUTED`: inventory roots;
verify source evidence; verify manifests and digests; stage read-only untracked
evidence; precheck; run full pytest from the detached tree; record execution
evidence; avoid `.marketflow` commits; require a passing authoritative retry;
and create separate execution/results review artifacts.

## Reviewed Non-Goals

All twenty non-goals remain `REVIEWED_ACTIVE`, including no current staging,
retry, regeneration, provider access, `.marketflow` commit, digest weakening,
ref or tag mutation, results review, acceptance, runtime, or trading authority.

## Root-Cause Question Review

Four questions were answered by diagnosis: the missing root, blocked digest,
later pass, and non-overriding status. Five items remain open: the full ready
digest if unbound, complete ignored-root inventory, whether acquisition evidence
alone suffices, the exact precheck, and the exact approved retry plan.

Status: `REVIEWED_WITH_OPEN_ITEMS_FOR_FUTURE_REMEDIATION`.

## Recommendation

The candidate has been reviewed, but no package is selected or approved.
An optional operator selection and separate approval are required before any
remediation execution. `ready_for_remediation_approval` remains false.

## Next Chain and Gates

If selected: remediation approval, execution, and results review; then a retry
candidate, approval, execution, and results review; then Main Merge Approval only
if the authoritative retry review passes. All eight matching gates remain closed.

## Risk Controls and Guardrails

The forty controls prohibit remediation selection or execution, evidence
staging, retry, results review, protected-ref changes, `.marketflow` commits,
provider or data work, strategy work, acceptance, and runtime or broker authority.
They preserve the failed gate, diagnostic-only rerun status, integration branch,
terminal archive evidence, published tags, `origin/main`, and META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_APPROVAL_V1_IF_SELECTED`
