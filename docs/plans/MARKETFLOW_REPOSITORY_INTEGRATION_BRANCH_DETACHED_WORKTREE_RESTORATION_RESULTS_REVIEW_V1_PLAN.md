# MarketFlow Repository Integration Branch Detached Worktree Restoration Results Review v1 Plan

## Purpose

Create a deterministic, digest-bound, read-only review of the registered
detached worktree produced by the approved restoration execution.

## Source Restoration Execution

Bind execution digest
`b037b1f51df52570a63b417054276fb0bd867dc7a2750b2851a88934a104de0c`,
worktree manifest digest
`e55415c8abc798086760ce9e37001acd6c16b725213e73f83dbdd448f732a001`,
and approval digest
`6ca8b958949667264419a1b5f59e08c7ae335c5e1b836e93541f87519a2b055d`.

## Review Scope

The scope is
`REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN`.
Only deterministic artifact construction and read-only Git inspection are in
scope.

## Registered Worktree Review

Require the exact deterministic path to exist in `git worktree list
--porcelain`. If it is missing or mismatched, stop without creating, removing,
resetting, or repairing anything.

## Worktree Head Verification

Require the worktree HEAD and registered HEAD to equal
`220fbc220365fce9cae13ab4853cddff118c0187`. Require detached HEAD and no branch
checkout.

## Worktree Cleanliness Review

Require an empty porcelain status, no `.marketflow` directory copied into the
detached worktree, and zero tracked repository files under `.marketflow`.

## Origin/Main Protection

Require `origin/main` to remain
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`. Do not push, merge, rebase,
reset, or otherwise modify main.

## Remote Integration Branch Check

Require the remote integration branch to remain absent. Do not push, delete,
or recreate it.

## Authority Boundaries

Do not execute remediation or an integration retry; stage or copy evidence;
commit `.marketflow`; create an integration results review; call providers;
acquire or regenerate data; recompute metrics; train or score models; generate
recommendations; accept predictive usefulness or profitability; or authorize
runtime, strategy, paper trading, broker access, or execution.

## Next Chain

1. Remediation Execution v1 retry, now allowed after worktree restoration review.
2. Remediation Results Review v1.
3. Integration Branch Retry Candidate v1.
4. Integration Branch Retry Approval v1.
5. Integration Branch Retry Execution v1.
6. Integration Branch Retry Results Review v1.
7. Main Merge Approval only if retry results review passes.

## Next Gates

- `remediation_execution_after_worktree_restoration_review`
- `remediation_results_review`
- `integration_branch_retry_candidate_after_remediation`
- `integration_branch_retry_approval_if_selected`
- `integration_branch_retry_execution_if_approved`
- `integration_branch_retry_results_review`
- `main_merge_approval_if_retry_passes`

## Risk Controls

The review is read-only: no worktree creation/deletion, branch reset/deletion,
evidence staging/copy/commit, retry, remediation execution, results review,
protected-ref push, force push, remote pruning, tag mutation, provider access,
data/model action, acceptance decision, or runtime/broker authorization. The
existing integration branch, failed gate, published governance tags, and META
limitation remain preserved.

## Guardrails

Readiness authorizes only the next separately invoked remediation execution
retry. It does not execute remediation and does not establish integration
success.

Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_V1_RETRY_AFTER_WORKTREE_RESTORATION`.
