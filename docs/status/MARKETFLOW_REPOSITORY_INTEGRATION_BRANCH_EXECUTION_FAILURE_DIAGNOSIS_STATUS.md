# MarketFlow Repository Integration Branch Execution Failure Diagnosis v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_ONLY_NOT_RETRY_NOT_REMEDIATION_NOT_RESULTS_REVIEW`.
- The diagnosis is offline, governance-only, and does not retry or accept the integration execution.

## Source Merge-Strategy Approval

The diagnosis binds approval digest
`34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`
and attempted execution commit
`9d3dbc488747a0e17921bd4dcab7be2fadefc5ba`.

## Preserved Integration State

The local-only integration branch is
`integration/marketflow-terminal-evidence-stack-validation-v1` at merge commit
`220fbc220365fce9cae13ab4853cddff118c0187`. Its exact parents remain
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2` and
`71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`. Neither the integration branch
nor `origin/main` is pushed or modified by diagnosis.

## Authoritative Failure Gate

The first integration pytest result remains authoritative:
`24481 passed, 1300 failed, 500 errors, 7 skipped`. Execution remains blocked
as `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_BLOCKED_INTEGRATION_PYTEST_FAILED`.
No successful execution or validation digest exists, and Integration Branch
Results Review is not ready.

## Root-Cause Trace

The representative approval failure requires frozen acquisition evidence review
digest `57c0a06e...`, but an integration worktree without the ignored acquisition
evidence root deterministically builds blocked review digest `783e0013...` with
`acquisition_provider_evidence_run_manifest.json missing`.

The later `26842 passed, 7 skipped` command created a detached worktree but ran
pytest from the feature worktree. It is diagnostic feature-branch evidence, not
an isolated integration rerun and not acceptance evidence. This explains the
apparent contradiction without reopening the failed gate.

## Recommendation and Authority Boundary

The next task is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1`.
It must separately propose deterministic ignored-evidence availability or test
fixture isolation. No retry may occur before remediation review and approval.

No provider, market-data, dataset, metric, model, scoring, recommendation,
runtime, broker, or trading action is performed or authorized. Predictive
usefulness and profitability remain not accepted.
