# MarketFlow Repository Integration Branch Retry Failure Classification Method Reentry v1 Plan

## Purpose

Create an offline, digest-bound decision that selects the safe classification
reentry path after review of a valid but limited pytest-cache source. Do not
read cache or execute classification, diagnostics, remediation, or retry work.

## Source Classification-Source Results Review

Bind the ready results-review digest
`a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9`
and cache-manifest review digest
`cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee`.
Use committed source constants only; do not reread or mutate cache.

## Retry Failure Context

Preserve the authoritative result of `24877 passed, 1292 failed, 112 errors, 7
skipped`. The prior root regression is not retry evidence and does not override
the failed detached retry.

## Cache Source Capability

Accept the reviewed source for module-level grouping, node-ID inventory,
bounded module-name root-cause-family candidate hints, and planning a v2 method
candidate.

## Cache Source Limitations

Do not use the source for failure/error separation, first-failure or first-error
ordering, traceback-based root cause, remediation execution, retry-success
evidence, or main-merge approval. The source cannot replace the failed retry.

## Reentry Decision and Options

Select `NEW_CLASSIFICATION_METHOD_CANDIDATE_V2_REQUIRED`. Do not select direct
original-method reentry, a retry without classification, or main merge despite
failure. Keep diagnostic output capture available but unselected because the
cache is sufficient for bounded v2 planning.

## Future Classification Method v2 Requirements

Keep the source reviewed and digest-bound; limit v2 claims to cache-supported
facts; prohibit failure/error, first-order, traceback, and retry-success claims;
preserve failed-retry authority; produce a module-grouping candidate only; and
require separate approval before v2 execution or any future retry.

## Future Classification Method v2 Candidate Plan

Bind source digests, define supported and prohibited outputs, define
module-grouping and evidence-root/path/cwd/digest-drift candidate packages,
retain fallback diagnostic-output capture, and require operator review and
approval. Status remains `PLANNED_NOT_EXECUTED`.

## Authority Boundaries

This task creates the reentry decision only. It creates no v2 candidate,
classification execution, retry candidate, retry execution/results review,
integration success, main-merge approval, predictive/profitability acceptance,
runtime authority, or broker authority.

## Next Chain and Gates

Proceed only through separately gated v2 candidate, operator review, approval,
execution, and results review tasks. A new retry candidate may follow only after
classification or remediation; retry approval, execution, and results review
remain separate. Main-merge approval requires a passing retry results review.

## Risk Controls and Guardrails

Do not read or modify cache, parse operator logs, run diagnostics or pytest,
capture output, stage or regenerate evidence, call providers, acquire data,
commit generated roots, push main or integration, delete/reset/force-push,
prune remotes, modify tags, or create runtime/trading authority. Preserve
origin/main, the local integration ref, detached worktree, frozen evidence,
terminal archive, governance tags, and the META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2`
may be invoked separately.
