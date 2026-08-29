# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate Operator Review v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_OPERATOR_REVIEW_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`.
- The review is offline, governance-only, and reviews restoration options without selecting or approving one.

## Source Candidate and Blocked Observation

- Source candidate digest: `a782d45a62b9d589381c1c50d0312312ca059b389aa60d8a7bdd3f8902ab39d6`.
- Source remediation approval digest: `681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`.
- Blocked remediation status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_BLOCKED_INTEGRATION_WORKTREE_MISSING_OR_MISMATCHED`.
- Integration branch/head: `integration/marketflow-terminal-evidence-stack-validation-v1` / `220fbc220365fce9cae13ab4853cddff118c0187`.
- No detached integration worktree or registered secondary worktree exists.
- The ignored seven-file evidence root and required manifest remain observed; no `.marketflow` file is tracked.

## Reviewed Restoration Packages

All six packages were reviewed. The registered detached-worktree package remains
recommended for operator assessment but is not selected. The attached-worktree
and operator-restored-path packages remain available but unselected. Branch
recreation, delete/recreate, and feature-worktree substitution remain blocked.

All seventeen future requirements, ten future plan steps, and twenty-one
non-goals are reviewed. Every future step remains `NOT_EXECUTED` and every
non-goal remains active.

## Recommendation

`OPTIONAL_OPERATOR_SELECTION_AND_APPROVAL_REQUIRED_BEFORE_ANY_WORKTREE_RESTORATION`

The review is not ready for restoration approval because it does not select a
package. A separate optional selection and approval task is required before any
worktree restoration.

## Authority Boundary

No package is selected or approved. No worktree is created, restored, deleted,
or reset. No evidence is staged or copied; no remediation, retry, results review,
branch push, branch deletion, tag mutation, provider/data/model action,
acceptance, runtime activation, broker action, or trading action occurs.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1_IF_SELECTED`
