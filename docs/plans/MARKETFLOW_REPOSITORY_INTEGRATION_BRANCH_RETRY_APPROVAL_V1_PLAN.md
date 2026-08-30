# MarketFlow Repository Integration Branch Retry Approval v1 Plan

## Purpose

Create an offline, attestation-bound approval that selects the authoritative
full-pytest retry package for future execution from the remediated detached
integration worktree. This plan creates approval authority only.

## Source Retry Candidate Operator Review

Bind the ready operator-review artifact and digest
`8adea54bd72bc3d1c0ea284930ea836101594e8ed12a971863c2032e9fb3a2ce`,
along with the retry candidate, remediation results-review, remediation
execution, and frozen source/staged inventory digests.

## Operator Attestation

Require the exact non-secret approval phrase, decision, selected package,
source digests, branch/head/path confirmations, first-failure classification,
and all closed-boundary confirmations. Refuse missing or altered values.

## Failure and Remediation Context

Preserve the first integration pytest failure as authoritative. Preserve the
later wrong-worktree pass as diagnostic-only. Bind the diagnosis that the
detached integration worktree lacked the ignored acquisition evidence root and
bind the remediated seven-file inventory without modifying it.

## Approval Scope and Selected Package

Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_ONLY_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN`.
Select only
`PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE`
and authorize it for future retry execution only.

## Approved Future Retry Requirements

Approve all 18 reviewed requirements: exact remediation evidence, detached and
clean worktree at `220fbc220365fce9cae13ab4853cddff118c0187`, unchanged
`origin/main`, absent remote integration branch, present and untracked frozen
evidence, exact inventory digest, full pytest from the detached integration
worktree, fail-closed wrong-worktree handling, first-retry authority, separate
results review, and separate main-merge approval.

## Approved Future Retry Plan

Approve the reviewed 12-step plan without executing it: reverify bound digests,
worktree/ref/evidence state, run the full suite only in a separately invoked
execution task, record its first result, fail closed on failure, create only an
execution artifact on success, and push neither integration nor main.

## Supporting and Blocked Packages

The precheck, targeted-test, and cache/environment-guard packages remain
available and unselected. Accepting remediation without retry and retrying from
the feature/root worktree remain blocked and unapproved.

## Next Chain and Gates

1. Integration Branch Retry Execution v1, if separately invoked.
2. Integration Branch Retry Results Review v1.
3. Main Merge Approval v1, only if retry results review passes.
4. Main Merge Execution v1, only if separately approved.
5. Branch Cleanup Candidate v1, only after merge strategy is settled.

The matching gates remain separate and sequential; this approval opens only the
future retry-execution gate.

## Risk Controls and Guardrails

Do not run retry pytest, create execution/results artifacts, mark success,
generate success digests, mutate or regenerate evidence, call providers,
commit `.marketflow`, push protected refs, delete/reset branches or worktrees,
force-push, prune, mutate tags, perform data/model actions, accept predictive
usefulness or profitability, or authorize runtime, broker, or trading use.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_EXECUTION_V1`
