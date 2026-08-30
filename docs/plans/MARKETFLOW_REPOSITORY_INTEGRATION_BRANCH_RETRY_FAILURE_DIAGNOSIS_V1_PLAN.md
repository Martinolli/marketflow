# MarketFlow Repository Integration Branch Retry Failure Diagnosis v1 Plan

## Purpose

Create a deterministic, offline, digest-bound diagnosis of the failed
authoritative integration retry. The artifact records evidence and open
root-cause questions only; it is not remediation, another retry, results
review, or main-merge authority.

## Source Retry Execution

- Artifact/status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED` / `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_BLOCKED_AUTHORITATIVE_FULL_PYTEST_FAILED`.
- Approval digest: `5197f10cfda574736ef2929c676774a9644840919d6bddcfdc5afe889de024d1`.
- Branch/commit: `feature/marketflow-repository-integration-branch-retry-execution-v1` / `ab178b65c69f0274b0abbf9c20df102d35e78d34`.

## Failure Summary and Retry Environment

The authoritative detached-worktree command used the root virtualenv Python and
returned exit code `1`: `24877 passed, 1292 failed, 112 errors, 7 skipped`.
The detached worktree remained at
`220fbc220365fce9cae13ab4853cddff118c0187`, clean and detached. The staged
evidence manifest remained unchanged at
`06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`.

## Original Failure Comparison

- Original: `24481 passed, 1300 failed, 500 errors, 7 skipped`.
- Retry: `24877 passed, 1292 failed, 112 errors, 7 skipped`.
- Delta: `+396 passed, -8 failed, -388 errors, 0 skipped`.

Evidence staging corrected or reduced some environment/evidence-root failures,
but substantial failures and errors remain. The retry remains blocked.

## Root Regression Boundary

The root-worktree result (`29066 passed, 7 skipped`) is a regression control,
not retry evidence. It cannot override the failed detached-worktree retry.

## Diagnosis Domains

The artifact covers retry-gate status, failure volume, original-failure
comparison, detached-worktree validity, staged-evidence validity,
wrong-worktree control, remaining failure classification, pytest error and
failure domains, authority boundaries, and the next remediation direction.

## Root-Cause Questions

- Which modules account for the `112` errors and `1,292` failures?
- Are ignored evidence roots, branch-content differences, paths/CWD, stale digest constants, or other generated-output assumptions involved?
- Which original failures disappeared and which persisted?
- What are the first failing module and first error trace in pytest order?
- Can a targeted diagnostic command classify the failures without becoming retry evidence?
- What remediation package is required before another retry?

## Recommendation

Create
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_V1`
as a future candidate. It must be based on failure-domain diagnosis and must not
be inferred to exist or be selected by this plan.

## Next Chain and Gates

The next chain is candidate, operator review, approval if selected, execution
if approved, results review, then a new retry candidate/review/approval/
execution/results-review chain. Main-merge approval is available only if that
future retry results review passes. Every step remains a separate gate.

## Risk Controls and Guardrails

No detached full-pytest retry, provider call, evidence change, data acquisition,
dataset generation, metric recomputation, model training, strategy scoring,
recommendation generation, `.marketflow` commit, integration/main push, branch
or worktree deletion, force-push, remote prune, or tag mutation is allowed.
Predictive usefulness and profitability remain not accepted; runtime, strategy,
paper-trading, and broker execution remain `NOT_AUTHORIZED`. Preserve the
terminal archive evidence, staged frozen evidence, published governance tags,
and the META limitation.
