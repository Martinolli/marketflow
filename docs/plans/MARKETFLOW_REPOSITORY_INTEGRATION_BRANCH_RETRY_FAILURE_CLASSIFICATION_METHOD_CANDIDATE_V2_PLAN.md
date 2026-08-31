# MarketFlow Repository Integration Branch Retry Failure Classification Method Candidate v2 Plan

## Purpose

Create an offline, digest-bound candidate catalog for a cache-supported v2
classification method. Propose packages for operator review without selecting,
approving, authorizing, or executing any package.

## Source Reentry and Classification-Source Review

Bind reentry digest
`318c0d1b3f6977a79cd77e8de466286f4057f13d7c7f2bd218c5a561c17e91a6`,
results-review digest
`a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9`,
and cache-manifest review digest
`cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee`.
Use committed constants only; do not read or modify cache.

## Retry Failure Context

Preserve the authoritative `24877 passed, 1292 failed, 112 errors, 7 skipped`
result. The prior root regression is not retry evidence and does not override
the failed detached retry.

## Candidate Scope and Philosophy

Limit the candidate to module-level grouping, node-ID inventory, and bounded
planning evidence. Do not claim failure/error separation, first-order results,
traceback root cause, remediation certainty, or retry success.

## Proposed and Recommended v2 Packages

Define nine packages: five available for operator review and four blocked.
Recommend `PACKAGE_CACHE_SUPPORTED_MODULE_LEVEL_NODEID_CLASSIFICATION_V2` as the
safest cache-supported package, but keep it unselected, unapproved, unauthorized,
and unexecuted.

Available alternatives may add module-name-only evidence-root hints, path/cwd
and digest-drift hints, a limitation-first report, or separately approved
diagnostic enrichment. Block cache-only failure/error separation, cache-only
first-order trace analysis, retry without classification, and main merge despite
the failed retry.

## Future v2 Requirements and Execution Plan

Require ready source evidence, digest binding, module/node-only scope, explicit
unsupported-claim exclusions, failed-retry preservation, limitation reporting,
separate execution approval, and separate retry approval. The ten-step plan may
produce module grouping, bounded summaries, optional low-confidence module-name
hints, limitation reporting, and a recommendation for later evidence packages.
Its status remains `PLANNED_NOT_EXECUTED`.

## Planned Outputs

Keep the classification manifest, module grouping and summary reports, largest
module summary, limitation report, low-confidence hint report,
unsupported-claims report, next-method recommendation, and digest manifest at
`PLANNED_NOT_GENERATED`.

## Non-Goals and Authority Boundaries

Do not read cache; classify modules or node IDs; run diagnostics, pytest, or a
retry; create retry or integration results; push protected branches; mutate
evidence or tags; call providers; acquire or regenerate data; or create
predictive, profitability, runtime, or trading authority.

## Next Chain and Gates

Proceed only through separately gated operator review, v2 approval, execution,
and results review. A new retry candidate may follow only after classification
or remediation, with separate retry approval, execution, and results review.
Main-merge approval requires a passing retry results review.

## Risk Controls and Guardrails

Preserve origin/main, the local integration branch, detached worktree, staged
frozen evidence, terminal archive, governance tags, and META limitation. Do not
delete/reset/force-push branches or worktrees, prune remotes, or commit generated
roots.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2_OPERATOR_REVIEW`
may be invoked separately.
