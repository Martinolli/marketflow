# MarketFlow Repository Integration Branch Detached Worktree Restoration Approval v1 Plan

## Purpose

Create an offline, attestation-bound approval selecting registered detached-
worktree restoration for a separately invoked future execution. Approval is not
worktree creation, remediation, evidence staging, retry, or results review.

## Source Operator Review

Bind operator-review digest
`e43dd78c5861e1bb0e8c8fe42c9dfeaf54c81f80943c521310ee20c6547cd0c1`,
candidate digest `a782d45a62b9d589381c1c50d0312312ca059b389aa60d8a7bdd3f8902ab39d6`,
remediation approval digest
`681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`,
and the remaining reviewed source-chain digests.

## Operator Attestation

Require the exact non-secret phrase:

`APPROVE INTEGRATION BRANCH DETACHED WORKTREE RESTORATION PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD MARKETFLOW REGISTERED DETACHED WORKTREE EXACT INTEGRATION HEAD NO BRANCH RESET NO WORKTREE DELETE NO REMEDIATION NO RETRY REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`

Require exact source digests, blocked status, integration branch/head,
`origin/main`, selected package, evidence and manifest confirmations, approval-
only scope, and every closed-boundary confirmation. Partial or altered
attestations fail closed and no secrets are required.

## Blocked Remediation Execution Observation

Preserve the missing-or-mismatched-worktree block, local integration branch at
`220fbc220365fce9cae13ab4853cddff118c0187`, absent remote integration branch,
unchanged `origin/main`, absent secondary worktree registration, and ignored
seven-file acquisition evidence root with its required manifest.

## Approval Scope

`REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_ONLY_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`

## Selected Restoration Package

Approve `PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD`
for future restoration execution only. Selection, approval, authorization, and
readiness become true; execution remains false.

## Approved Future Restoration Requirements

Approve all seventeen controls, including exact refs, deterministic non-
overwritten path, registered detached Git state, exact HEAD, no branch reset or
remote push, and separation from evidence staging, remediation, and retry.

## Approved Future Restoration Plan

Approve the ten-step source plan for future execution only: verify refs and path
preconditions, create the registered detached worktree at the exact integration
commit, verify registration and HEAD, and preserve the absent remote integration
branch. Do not copy `.marketflow`, run pytest, or retry integration. Status
remains `NOT_EXECUTED`.

## Supporting and Blocked Packages

Attached-worktree creation and later operator-restored-path parameterization
remain `AVAILABLE_NOT_SELECTED`. Integration-branch recreation, delete/recreate,
and feature-worktree substitution remain `BLOCKED_NOT_APPROVED`.

## Next Chain and Gates

A separately invoked restoration execution and results review come first. Only
after restoration review may remediation execute. Remediation review and the
complete integration retry chain must pass before any main-merge approval. All
nine matching gates remain separately controlled.

## Risk Controls and Guardrails

The approval preserves `origin/main`, the existing integration branch,
authoritative failed gate, published governance tags, ignored evidence boundary,
and META limitation. It prohibits current worktree mutation, evidence staging,
provider/data/model actions, recommendations, acceptance, runtime, and broker
authority.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_EXECUTION_V1`
