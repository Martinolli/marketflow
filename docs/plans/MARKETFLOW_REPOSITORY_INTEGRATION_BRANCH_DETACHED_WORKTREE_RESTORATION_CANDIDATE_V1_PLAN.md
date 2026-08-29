# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate v1 Plan

## Purpose

Define an offline, digest-bound candidate path for restoring the missing
detached integration worktree. This plan is not approval, worktree creation,
remediation, evidence staging, integration retry, or results review.

## Source Remediation Approval

Bind remediation approval digest
`681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`
and its operator-review, candidate, diagnosis, and merge-strategy approval
digests. The approved evidence-staging remediation remains blocked because the
required detached integration worktree is absent.

## Blocked Remediation Execution Observation

Record the blocked artifact and missing-or-mismatched-worktree status. Preserve
the local integration branch at
`220fbc220365fce9cae13ab4853cddff118c0187`, absent remote integration branch,
unchanged `origin/main`, absent secondary worktree registration, and ignored
seven-file acquisition evidence root with its required manifest.

## Candidate Scope

`REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`

## Worktree Restoration Philosophy

A future execution must create or restore a registered local Git worktree at
the exact approved integration head before evidence staging can proceed. It
must preserve the existing branch and failed gate and must not treat restoration
as successful integration validation.

## Proposed Restoration Packages

Define six packages: registered detached worktree creation, attached worktree
creation, later parameterization with an operator-restored path, integration
branch recreation, branch/worktree deletion and recreation, and feature-
worktree substitution. All remain unselected and unexecuted.

## Recommended Restoration Package

Recommend
`PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD`
for operator review. A detached checkout avoids branch-reset and branch-checkout
conflicts while providing the exact future remediation location.

## Future Restoration Requirements

Require unchanged `origin/main`, the existing local integration branch at the
bound commit, an absent remote integration branch, a deterministic non-
overwritten path, registered detached Git state, the exact HEAD, no branch
reset/deletion or remote push, no evidence copy/staging during restoration, and
separate later remediation and retry stages.

## Future Restoration Plan

Verify all bound refs and path preconditions, then—only after separate approval—
create a registered detached worktree with `git worktree add --detach`, verify
registration and exact HEAD, and verify remote refs remain unchanged. The
restoration execution must not copy `.marketflow`, run pytest, or retry
integration.

## Restoration Non-Goals

Do not create, restore, delete, or use a worktree in this candidate. Do not
reset or recreate the integration branch, stage evidence, commit `.marketflow`,
retry pytest, create a results review, push protected/integration refs, alter
tags, or create data/model/runtime/trading authority.

## Next Chain

Operator review, approval if selected, restoration execution if approved, and
restoration results review precede a remediation execution retry. Remediation
review and a separate integration retry candidate/approval/execution/review
chain must pass before any main-merge approval.

## Next Gates

All restoration, remediation, retry, results-review, and main-merge gates remain
separate and closed by this candidate.

## Risk Controls and Guardrails

The candidate preserves the existing integration branch, authoritative failed
gate, published governance tags, `origin/main`, ignored evidence boundary, and
META limitation. It prohibits worktree mutation, evidence staging, provider and
data actions, model or recommendation actions, acceptance, runtime, and broker
authority.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1`
