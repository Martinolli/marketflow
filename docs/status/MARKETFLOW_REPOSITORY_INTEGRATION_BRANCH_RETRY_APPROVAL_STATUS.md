# MarketFlow Repository Integration Branch Retry Approval v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVED`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN`.
- Approval digest: `5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1`.
- The approval is offline, governance-only, and bound to the exact non-secret operator attestation.

## Source Evidence

- Retry candidate operator-review digest: `8adea54bd72bc3d1c0ea284930ea836101594e8ed12a971863c2032e9fb3a2ce`.
- Retry candidate digest: `35598851bf4bfec55385cd6e2559ebb933161d846302a3032861e72ed07985eb`.
- Remediation results-review digest: `b3f86722e05d7692805e51ca86f125df79099a10e0f4bb4d39ea9c824472ec67`.
- Remediation execution digest: `4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346`.
- Source/staged evidence inventory digest: `06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`.

## Failure and Remediation Context

The first integration pytest remains authoritative: `24481 passed, 1300
failed, 500 errors, 7 skipped`. The later `26842 passed, 7 skipped`
wrong-worktree rerun remains diagnostic-only and cannot override that failure.
The remediated detached integration worktree contains seven matching ignored
evidence files totaling 2,458,181 bytes; those files remain untracked.

## Selected Retry Package

`PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE`
is selected, approved, and authorized for future retry execution only. It has
not been executed. All 18 future requirements and all 12 future execution steps
are approved only for a separately invoked execution task. Three supporting
packages remain available and unselected; two unsafe packages remain blocked.

## Authority Boundary

This approval sets retry selection, approval, authorization, and readiness for
future execution to true. It does not run pytest or a retry, create an execution
or results-review artifact, mark integration successful, generate success
digests, mutate evidence, call providers, commit `.marketflow`, push the
integration branch or main, delete branches or worktrees, change tags, accept
predictive usefulness or profitability, or authorize runtime or trading.

All `55/55` approval checks pass with zero failures and zero blockers. The next
task is `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1`, if
separately invoked.

## Follow-on Execution

Integration Branch Retry Execution v1 was separately invoked from this
approval. The authoritative full pytest ran only from the remediated detached
integration worktree and returned `24877 passed, 1292 failed, 112 errors, 7
skipped` with exit code `1`. The execution therefore failed closed as
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED`.
The approval remains source evidence; no retry results review, branch push,
`.marketflow` commit, usefulness/profitability acceptance, runtime authority,
or trading authority was created.
