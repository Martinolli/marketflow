# MarketFlow Repository Integration Branch Retry Failure Classification Method Candidate v2 Operator Review v1 Plan

## Purpose

Create an offline, digest-bound operator review of the candidate-v2 package
catalog. Review every proposed package and future planning component without
selecting, approving, authorizing, or executing a package.

## Source Candidate v2, Reentry, and Classification-Source Review

Bind candidate digest
`0681e9f06cc45a18683055695d3a45750af87ba04cfad3afb21a07c818deccf4`,
reentry digest
`318c0d1b3f6977a79cd77e8de466286f4057f13d7c7f2bd218c5a561c17e91a6`,
results-review digest
`a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9`,
and cache-manifest digest
`cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee`.
Use committed constants only; do not read or modify cache.

## Retry Failure Context

Preserve the authoritative `24877 passed, 1292 failed, 112 errors, 7 skipped`
result. The prior root regression is not retry evidence and does not override
the failed detached retry.

## Review Scope and Candidate Philosophy

Review cache-supported module grouping and node-ID planning only. Preserve the
exclusion of failure/error separation, first-order results, traceback root
cause, remediation certainty, and retry-success claims. Status remains
`REVIEWED_PLANNING_ONLY`.

## Reviewed v2 Packages

Review all nine packages. Keep the recommended module-level node-ID package
unselected. Preserve the four blocked packages and the four other available
alternatives without selection, approval, authorization, or execution.

## Reviewed Requirements, Plan, Outputs, and Non-Goals

Mark all 16 future requirements reviewed and not executed; all ten execution
steps reviewed and planned but not executed; all nine outputs reviewed but not
generated; and all 25 non-goals reviewed and active.

## Recommendation

Require optional explicit package selection and a separate approval before any
v2 execution. Keep `ready_for_classification_method_v2_approval` false and the
possible approval task at `FUTURE_APPROVAL_NOT_CREATED`.

## Next Chain and Gates

Proceed only through separately gated v2 approval, execution, and results
review. A retry candidate may follow only after classification or remediation,
with separate retry approval, execution, and results review. Main-merge approval
requires a passing retry results review.

## Risk Controls and Guardrails

Do not select or approve packages; read cache; classify modules or node IDs;
run diagnostics, pytest, or a retry; create retry or integration results; push
protected branches; mutate evidence or tags; call providers; acquire or
regenerate data; or create predictive, profitability, runtime, or trading
authority. Preserve origin/main, the integration branch, detached worktree,
frozen evidence, terminal archive, governance tags, and META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_APPROVAL_V2_IF_SELECTED`
may be invoked only after an explicit package selection.
