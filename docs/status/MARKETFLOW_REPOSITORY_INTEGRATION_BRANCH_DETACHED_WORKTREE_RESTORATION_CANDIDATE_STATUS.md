# MarketFlow Repository Integration Branch Detached Worktree Restoration Candidate v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_WORKTREE_CREATION_NOT_REMEDIATION_NOT_RETRY`.
- The artifact is offline, governance-only, candidate-only, and requires a separate operator review.

## Bound Source and Observation

- Remediation approval digest: `681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`.
- Blocked remediation status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_BLOCKED_INTEGRATION_WORKTREE_MISSING_OR_MISMATCHED`.
- Local integration branch/head: `integration/marketflow-terminal-evidence-stack-validation-v1` / `220fbc220365fce9cae13ab4853cddff118c0187`.
- `origin/main`: `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.
- No detached integration worktree or registered secondary worktree was observed.
- The ignored acquisition evidence root and required manifest were observed with seven files totaling 2,458,181 bytes; no `.marketflow` files are tracked.

## Recommended Restoration Package

`PACKAGE_CREATE_REGISTERED_DETACHED_WORKTREE_AT_REQUIRED_INTEGRATION_HEAD` is
recommended for operator review but is not selected, approved, authorized, or
executed. It proposes a future registered detached worktree at the exact
integration merge commit without resetting or checking out the integration
branch.

Five alternatives remain available or blocked for review. Recreating the
integration branch, deleting/resetting branch or worktree state, and using the
feature worktree as the integration worktree are blocked.

## Authority Boundary

This candidate does not create, restore, delete, or use a worktree. It does not
stage or copy evidence, commit `.marketflow`, execute remediation, retry
integration, create a results review, push main or the integration branch,
delete branches, or mutate tags.

No provider request, market-data acquisition, dataset generation, metric
recomputation, model training, strategy scoring, recommendation, predictive or
profitability acceptance, runtime activation, broker action, or trading action
is authorized or performed.

## Next Task

The follow-on Integration Branch Detached Worktree Restoration Candidate
Operator Review v1 is implemented. This candidate remains the source evidence;
the operator review assesses restoration packages only.

The review does not select or approve restoration, create or restore a worktree,
stage evidence, retry integration, create a results review, push branches,
commit `.marketflow`, accept predictive usefulness or profitability, or
authorize runtime or trading.

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_DETACHED_WORKTREE_RESTORATION_APPROVAL_V1_IF_SELECTED`
