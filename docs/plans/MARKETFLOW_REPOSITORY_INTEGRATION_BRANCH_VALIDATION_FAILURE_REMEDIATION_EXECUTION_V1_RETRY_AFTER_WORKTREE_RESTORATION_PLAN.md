# MarketFlow Repository Integration Branch Validation Failure Remediation Execution v1 Retry After Worktree Restoration Plan

## Purpose

Stage only the approved frozen ignored acquisition evidence root into the
reviewed detached integration worktree, verify an exact source/target match,
and leave integration retry and results review for separate tasks.

## Source Worktree Restoration Results Review

Bind results-review digest
`562c6bc4cadb09232ca304efb803d566c0904226314b8f94cceef2e54122159a`
and manifest digest
`415f2445805f93906b5f63035472f8edb95f41f64c57c46eab659e5221cc738d`.

## Source Remediation Approval

Bind remediation approval digest
`681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`
and execute only
`PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE`.

## Failure Summary and Root Cause

Preserve the first integration pytest failure (`24481 passed, 1300 failed,
500 errors, 7 skipped`) as authoritative. Preserve the later passing run as
diagnostic-only. The diagnosed root cause is
`DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT`.

## Execution Scope

The scope is
`REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.
Only local copying and verification of the exact frozen ignored root are in
scope.

## Detached Worktree Verification

Require the exact registered path, detached HEAD
`220fbc220365fce9cae13ab4853cddff118c0187`, no branch checkout, and a clean
pre-staging worktree. Reject any substitute path.

## Evidence Root Inventory and Staging Method

Require exactly seven source files totaling 2,458,181 bytes and the manifest
`acquisition_provider_evidence_run_manifest.json`. Refuse to overwrite an
existing target. Use Python file copying only, preserving file contents and
metadata; do not regenerate or transform evidence.

## Digest Verification

Hash every source and staged file with SHA-256, compare ordered relative paths,
sizes, and hashes, and require identical deterministic manifest digests. Verify
the staged root remains ignored and `git ls-files .marketflow` remains empty.

## Wrong-Worktree Guard

Run prechecks from the exact detached integration worktree. Reject any other
working directory and do not treat a feature-worktree pytest run as acceptance
evidence.

## Authority Boundaries

Do not run integration pytest retry, create retry or results-review artifacts,
mark integration successful, commit `.marketflow`, push protected refs,
delete/reset worktrees or branches, mutate tags, call providers, acquire or
regenerate data, perform model work, accept predictive usefulness or
profitability, or authorize runtime or broker execution.

## Next Chain

1. Remediation Results Review v1.
2. Integration Branch Retry Candidate v1.
3. Integration Branch Retry Approval v1.
4. Integration Branch Retry Execution v1.
5. Integration Branch Retry Results Review v1.
6. Main Merge Approval only if retry results review passes.

## Next Gates

- `integration_failure_remediation_results_review`
- `integration_branch_retry_candidate_after_remediation`
- `integration_branch_retry_approval_if_selected`
- `integration_branch_retry_execution_if_approved`
- `integration_branch_retry_results_review`
- `main_merge_approval_if_retry_passes`

## Risk Controls

Stage only frozen ignored evidence; prohibit regeneration, provider calls,
tracking or committing `.marketflow`, integration retry, results review,
success claims/digests, branch/worktree deletion or reset, protected-ref push,
force push, remote pruning, tag mutation, acquisition/dataset/metric/model
actions, recommendations, acceptance, runtime, and broker authority. Preserve
the authoritative failed gate, integration branch, terminal archive evidence,
published governance tags, and META limitation.

## Guardrails

Successful remediation staging only makes a separate remediation results
review appropriate. It does not establish integration success.

Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1`.
