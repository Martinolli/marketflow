# MarketFlow Repository Merge Strategy Approval v1 Plan

## Purpose

Select and approve the reviewed temporary integration-branch validation
package for a separately invoked future execution task, without executing it.

## Source Merge-Strategy Operator Review

The committed source review at
`34fbc53a31eab0e9feec8df1814dfbd9b22c4f4b` remains the evidence authority.
Its digest is
`557c0960704c09c512fc4cdd64964742d67a11793d1750569e775a5868a45930`.
The approval binds its complete upstream chain without rerunning it.

## Operator Attestation

Require the exact non-secret decision, phrase, package, source digests,
protected-main commit, integration-branch plan, timestamp/reference, and all
closed-boundary confirmations. Missing or incorrect inputs fail closed. Never
request or store API keys, raw payloads, broker details, or personal secrets.

## Repository Context

Preserve 302 local branches, 274 remote refs, 576 total refs, 32 local tags,
four verified terminal tags, and `origin/main` at
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.

## Approval Scope

`REPOSITORY_MERGE_STRATEGY_APPROVAL_ONLY_NOT_INTEGRATION_BRANCH_NOT_MERGE_NOT_DELETE_NOT_MAIN`

## Selected Merge Strategy Package

Select `PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION` as
`APPROVED_FOR_FUTURE_INTEGRATION_BRANCH_EXECUTION_ONLY`. Selection and
authorization do not constitute execution.

## Approved Integration Branch Plan

Approve future creation of
`integration/marketflow-terminal-evidence-stack-validation-v1` from protected
`origin/main`, using
`feature/marketflow-repository-tag-push-results-review-v1` at
`71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`. A separate task is required for
branch creation, integration, and pytest; a separate results review follows.

## Supporting Packages

Branch/tag-only preservation, future squash merge, future merge commit,
selective documentation/status integration, and deferral until cleanup
planning remain `AVAILABLE_NOT_SELECTED`.

## Future Execution Boundary

Future execution may create the temporary integration branch, attempt the
stack integration only there, and run full pytest there. It may not push main,
delete branches, force-push, accept predictive usefulness, or authorize
runtime. Main merge requires a separate approval after results review.

## Next Chain

Integration-branch execution, integration results review, conditional main-
merge approval and execution, then cleanup candidate and separately approved
cleanup with backup and protected-branch confirmation.

## Next Gates

Integration execution, integration results review, main approval, main
execution, cleanup candidate, cleanup approval, and cleanup execution remain
distinct gates.

## Risk Controls

No integration branch or Git integration operation in this approval; no tag
mutation; no provider, data, metric, model, scoring, recommendation, runtime,
broker, or trading action. Protect `origin/main`, terminal archive evidence,
published governance tags, and the META limitation.

## Non-Goals

This approval does not execute the strategy, create the branch, merge, push
main, authorize cleanup, accept predictive usefulness or profitability, or
create runtime or trading authority.

## Guardrails

Default tests remain deterministic and offline. `.marketflow` remains ignored
and untracked. Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_V1`.
