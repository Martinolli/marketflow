# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate Operator Review v1 Plan

## Purpose

Create an offline, digest-bound operator review of the detached-worktree
restoration candidate. The review assesses the restoration packages and controls
without selecting, approving, or executing restoration.

## Source Restoration Candidate

Bind source candidate digest
`a782d45a62b9d589381c1c50d0312312ca059b389aa60d8a7bdd3f8902ab39d6`
and its remediation approval, operator-review, remediation candidate, diagnosis,
and merge-strategy approval digests.

## Blocked Remediation Execution Observation

Preserve the missing-or-mismatched-worktree block, local integration branch at
`220fbc220365fce9cae13ab4853cddff118c0187`, absent remote integration branch,
unchanged `origin/main`, absent secondary worktree registration, and ignored
seven-file acquisition evidence root with its required manifest.

## Review Scope

`REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`

## Reviewed Worktree Restoration Philosophy

Review the candidate principle that future remediation requires a registered
local Git worktree at the exact integration head. Preserve the existing branch
and failed gate; do not treat restoration as integration-validation success.

## Reviewed Restoration Packages

Review all six source packages with their source status and a review status.
Keep every package unselected, unapproved, and unexecuted. Preserve the three
blocked package outcomes.

## Reviewed Restoration Requirements

Review all seventeen requirements as
`REVIEWED_REQUIRED_FOR_FUTURE_WORKTREE_RESTORATION` with execution status
`NOT_EXECUTED`.

## Reviewed Future Restoration Plan

Review all ten steps as `REVIEWED_PLANNED_NOT_EXECUTED`. Do not create a path or
worktree, copy evidence, run pytest, or retry integration.

## Reviewed Non-Goals

Keep all twenty-one non-goals `REVIEWED_ACTIVE`, including no worktree mutation,
branch reset/deletion, evidence staging, `.marketflow` commit, retry, results
review, protected-ref/tag changes, acceptance, runtime, or trading authority.

## Recommendation

Set the action to
`OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_WORKTREE_RESTORATION`.
The review does not select a package and therefore keeps readiness for approval
false.

## Next Chain and Gates

A separate optional approval, restoration execution, and restoration results
review precede remediation. Remediation review and the complete integration
retry candidate/approval/execution/review chain precede any main-merge approval.
All matching gates remain closed.

## Risk Controls and Guardrails

Preserve `origin/main`, the local integration branch, authoritative failed gate,
published governance tags, ignored evidence boundary, and META limitation. No
provider, data, model, recommendation, acceptance, runtime, broker, or trading
action is permitted.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1_IF_SELECTED`
