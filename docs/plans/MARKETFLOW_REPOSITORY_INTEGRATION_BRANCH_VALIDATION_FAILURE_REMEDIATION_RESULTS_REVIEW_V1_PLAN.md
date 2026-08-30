# MarketFlow Repository Integration Branch Validation Failure Remediation Results Review v1 Plan

## Purpose

Create a deterministic, digest-bound, read-only governance review of the
completed remediation execution and its staged frozen ignored evidence root.

## Source Remediation Execution

Bind the executed remediation artifact, execution digest, evidence-manifest
digest, selected frozen-evidence package, attempted execution context, and all
closed authority boundaries without rerunning or modifying the execution.

## Source Worktree Restoration Review

Bind the restoration results-review digest and manifest digest that established
the required registered detached worktree at the integration head.

## Failure Context

Preserve the first failed integration pytest as authoritative, the later
wrong-worktree pass as diagnostic only, and the diagnosed missing ignored
evidence root as the remediation cause.

## Review Scope

The review may inspect Git state and hash local frozen evidence. It must not
copy, modify, delete, stage, retry, regenerate, push, merge, or create runtime
authority.

## Detached Worktree Review

Verify the exact approved worktree path, expected HEAD, detached state, clean
status, unchanged local integration branch, absent remote integration branch,
and unchanged `origin/main`.

## Staged Evidence Review

Verify the source and staged roots, required manifest, exact seven-file and
2,458,181-byte inventories, per-file hashes, ignored state, and zero tracked
`.marketflow` files.

## Digest Verification

Bind source governance digests, calculate deterministic source and staged
inventory digests, require exact equality, then issue deterministic review and
review-evidence-manifest digests.

## Tracking and Commit Boundary

Only the service, tests, exports, status, and plan are tracked. Generated or
staged `.marketflow` evidence remains ignored, local, unmodified, and
uncommitted.

## Authority Boundaries

The review creates readiness only for a later retry candidate. It creates no
candidate, approval, retry, integration success, predictive/profitability
acceptance, runtime use, paper trading, or broker execution authority.

## Next Chain

1. Integration Branch Retry Candidate v1.
2. Integration Branch Retry Approval v1, if selected.
3. Integration Branch Retry Execution v1, if approved.
4. Integration Branch Retry Results Review v1.
5. Main Merge Approval only if retry results review passes.

## Next Gates

- `integration_branch_retry_candidate_after_remediation`
- `integration_branch_retry_approval_if_selected`
- `integration_branch_retry_execution_if_approved`
- `integration_branch_retry_results_review`
- `main_merge_approval_if_retry_passes`

## Risk Controls

Fail closed on any path, ref, detached-state, cleanliness, inventory, digest,
tracking, or manifest mismatch. Preserve all protected refs, ignored evidence,
terminal archive evidence, published governance tags, the first failed pytest,
and the META limitation. Require separate candidate and approval tasks before a
retry.

## Guardrails

No provider or `.env` inspection, data acquisition, evidence regeneration,
dataset generation, metric recomputation, model training, scoring,
recommendations, retry, branch deletion/reset, remote pruning, force push, tag
mutation, integration-branch push, or main push is permitted.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1`.
