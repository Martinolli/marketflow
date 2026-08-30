# MarketFlow Repository Integration Branch Retry Execution v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_ONLY_NOT_RESULTS_REVIEW_NOT_MAIN`.
- The first retry result is authoritative and will not be overridden by a later rerun.
- No successful execution or validation digest was created.

## Source Retry Approval

- Approval digest: `5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1`.
- Selected package: `PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE`.
- Operator-review digest: `8adea54bd72bc3d1c0ea284930ea836101594e8ed12a971863c2032e9fb3a2ce`.
- Retry-candidate digest: `35598851bf4bfec55385cd6e2559ebb933161d846302a3032861e72ed07985eb`.

## Authoritative Retry Command and Result

- Command: `C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q`.
- Working directory: `C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1`.
- Exit code: `1`.
- Result: `24877 passed, 1292 failed, 112 errors, 7 skipped`.
- Measured service duration: `1547.848456` seconds.
- Pytest-reported duration: `1538.84` seconds (`0:25:38`).

## Repository, Worktree, and Evidence Boundaries

Before and after the retry, `origin/main` remained
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`; the local integration branch and
detached worktree remained at `220fbc220365fce9cae13ab4853cddff118c0187`;
the remote integration branch remained absent; and the worktree remained
detached and clean. The seven-file, 2,458,181-byte staged evidence inventory
remained unchanged at
`06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`
and remained ignored and untracked.

## Blocked Disposition and Authority Boundary

The retry was executed, but retry execution success is false and readiness for
retry results review is false. No retry results review or integration results
review was created. No integration/main push, deletion, reset, evidence
mutation, `.marketflow` commit, provider/data/model action, predictive or
profitability acceptance, runtime authority, or trading authority occurred.

All `67/67` execution-boundary checks pass with zero checklist failures and
zero blockers. These checks confirm faithful fail-closed recording; they do not
mean pytest passed. The next task is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSIS_V1`.
