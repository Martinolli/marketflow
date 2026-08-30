# MarketFlow Repository Integration Branch Retry Execution v1 Plan

## Purpose and Source Approval

Execute the selected authoritative retry package exactly once from the
remediated detached integration worktree, bound to retry-approval digest
`5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1`.

## Failure and Remediation Context

Preserve the historical first integration failure and the diagnostic-only
wrong-worktree rerun. Verify the remediated detached worktree and frozen staged
evidence without copying, repairing, regenerating, or modifying evidence.

## Execution Scope and Prechecks

Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN`.
Before pytest, verify the source approval, `origin/main`, local/remote
integration refs, detached worktree path/head/state/cleanliness, required
manifest, exact evidence digest, ignored/untracked boundaries, and root
virtualenv Python.

## Authoritative Retry Command

Use root virtualenv Python:
`C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q`
with the current working directory set to
`C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1`.

## Result Handling

The first retry result is authoritative. On success, create execution and
validation digests and open only the results-review gate. On failure, create a
blocked artifact, create no success digests, do not rerun, and route to failure
diagnosis.

## Recorded Disposition

The authoritative retry exited `1` with `24877 passed, 1292 failed, 112 errors,
7 skipped`. The disposition is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED`.
No successful execution or validation digest exists.

## Repository and Worktree Boundaries

Preserve `origin/main`, the local-only integration branch, detached worktree,
staged frozen evidence, terminal archive evidence, published governance tags,
and the META limitation. Do not push or delete protected state.

## Next Chain and Gates

1. Integration Branch Retry Failure Diagnosis v1.
2. Remediation or retry-method candidate, only after diagnosis.
3. No main merge approval.

The active gates are
`integration_branch_retry_failure_diagnosis_if_failed`,
`retry_failure_remediation_candidate_if_needed`, and
`main_merge_blocked_until_retry_review_passes`.

## Risk Controls and Guardrails

Run only from the exact detached worktree with root virtualenv Python; preserve
the first result; verify frozen evidence before and after; and prohibit rerun
override, evidence mutation/regeneration, provider calls, `.marketflow`
tracking/commit, results-review creation, branch pushes/deletions, force-push,
pruning, tag mutation, data/model actions, predictive/profitability acceptance,
and runtime/broker/trading authority.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1`
