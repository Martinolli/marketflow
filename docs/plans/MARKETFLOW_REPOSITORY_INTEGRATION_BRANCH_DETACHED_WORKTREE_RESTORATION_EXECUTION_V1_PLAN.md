# MarketFlow Repository Integration Branch Detached Worktree Restoration Execution v1 Plan

## Purpose

Create exactly one registered detached worktree at the existing approved
integration commit so a later, separately authorized results review can verify
the restored prerequisite.

## Source Restoration Approval

The source approval digest is
`6ca8b958949667264419a1b5f59e08c7ae335c5e1b836e93541f87519a2b055d`.
It selects
`PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD`
and authorizes only this restoration execution.

## Blocked Remediation Execution Observation

The earlier remediation execution was blocked because the integration
worktree was missing or mismatched. That failed gate remains authoritative;
this plan does not reinterpret it as a successful remediation or integration
execution.

## Execution Scope

The scope is
`REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_ONLY_NOT_REMEDIATION_NOT_RETRY_NOT_RESULTS_REVIEW`.
Only local registered detached-worktree creation and verification are in scope.

## Worktree Restoration Path

Use only
`C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1`.
Fail closed if it exists or is registered unexpectedly; never delete,
overwrite, reset, or substitute another path.

## Registered Worktree Creation

After verifying all preconditions, run only:

`git worktree add --detach <approved-path> 220fbc220365fce9cae13ab4853cddff118c0187`

The completed execution created the registered entry without checking out the
integration branch itself.

## Worktree Head Verification

Require the registered worktree HEAD to equal
`220fbc220365fce9cae13ab4853cddff118c0187`, require detached HEAD, and require
a clean new worktree. The execution satisfied each requirement.

## Origin/Main Protection

Require `origin/main` to remain
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2` before and after. Do not push,
merge, rebase, cherry-pick, reset, or otherwise modify main.

## Remote Integration Branch Check

Require the remote integration branch to be absent before and after. Do not
push or delete any remote integration ref.

## Authority Boundaries

Do not stage or copy evidence, commit `.marketflow`, execute remediation or an
integration retry, create a results review, call providers, acquire or
regenerate data, recompute metrics, perform model work, generate
recommendations, accept predictive usefulness or profitability, or authorize
runtime, strategy, paper trading, broker access, or execution.

## Next Chain

1. Worktree Restoration Results Review v1.
2. Remediation Execution v1 retry only after the restoration review passes.
3. Remediation Results Review v1.
4. Integration Branch Retry Candidate v1.
5. Integration Branch Retry Approval v1.
6. Integration Branch Retry Execution v1.
7. Integration Branch Retry Results Review v1.
8. Main Merge Approval only if the retry results review passes.

## Next Gates

- `worktree_restoration_results_review`
- `remediation_execution_after_worktree_restoration_review`
- `remediation_results_review`
- `integration_branch_retry_candidate_after_remediation`
- `integration_branch_retry_approval_if_selected`
- `integration_branch_retry_execution_if_approved`
- `integration_branch_retry_results_review`
- `main_merge_approval_if_retry_passes`

## Risk Controls

Use the exact approved commit and deterministic path; preserve the integration
branch and failed gate; keep evidence ignored and untracked; prohibit branch,
worktree, tag, and protected-ref deletion or reset; prohibit remote pushes
other than the final execution feature-branch push; keep provider, data, model,
acceptance, runtime, and broker boundaries closed.

## Guardrails

The restoration result is ready only for a separate results review. It is not
remediation or retry evidence and creates no claim of integration success.

Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_RESULTS_REVIEW_V1`.
