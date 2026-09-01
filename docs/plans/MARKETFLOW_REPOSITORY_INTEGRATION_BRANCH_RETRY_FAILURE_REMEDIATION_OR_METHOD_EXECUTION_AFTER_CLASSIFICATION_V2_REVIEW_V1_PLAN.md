# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review v1 Plan

## Purpose

Execute the approved largest-module planning method offline. Generate bounded,
deterministic prioritization only when actual committed module paths and per-path
counts are available; otherwise fail closed without inventing detail.

## Source Approval

Bind approval digest
`676e01e2d15b2ae018facc73b966e35aa29c3411edda3c13e80e77f93ee11e97`
and the selected
`PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING`
package. Approval remains source evidence and grants only this planning
execution.

## Source Classification Results Review v2

Bind results-review digest
`0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86`,
execution-v2 digest
`054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017`,
and module-grouping digest
`34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.
Do not read the detached pytest cache or reconstruct grouping from logs.

## Retry Failure Context

Preserve the first retry as authoritative: `24,877 passed / 1,292 failed / 112
errors / 7 skipped`, commit
`ab178b65c69f0274b0abbf9c20df102d35e78d34`. The prior root regression is not
retry evidence.

## Classification Evidence Summary

Preserve 1,404 failed-or-errored node IDs across 29 modules and top aggregate
counts `136, 131, 122, 112, 111`. Preserve that failures and errors were not
separated and that no first failure, first error, first-order cause, traceback
root cause, retry success, or main-merge readiness was established.

## Execution Scope

Use only
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_ONLY_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN`.
The method may produce planning records, never diagnostic or remediation
evidence.

## Prioritized Module Planning Success Path

When a validated 29-module detail snapshot is supplied, sort rows by descending
node-ID count and ascending module path. Assign the first five modules to
`PRIORITY_1_TOP_5_MODULE_GROUPS`, the next five to
`PRIORITY_2_NEXT_5_MODULE_GROUPS`, and the remainder to
`PRIORITY_3_REMAINING_MODULE_GROUPS`. Include only already-available bounded
samples and label confidence `LOW_TO_MEDIUM` with a module-grouping-only basis.

The top-five aggregate is 612 of 1,404, deterministically represented as
`43.589744%`. A successful execution may recommend targeted diagnostic-output
capture only as a future candidate after a separate results review.

## Blocked Module-Detail-Unavailable Path

The current committed artifacts expose aggregates but no module paths or
per-path counts. The actual execution therefore records
`MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS`, leaves
all planning outputs ungenerated, and routes to source recovery. It does not
derive module identities from count positions.

## Diagnostic and Remediation Planning Buckets

Success-path rows may identify five planning candidates: targeted diagnostic
output capture, evidence-root requirement review, path/CWD assumption review,
digest-constant drift review, and test-fixture isolation review. These labels do
not execute those actions or select a follow-on package.

## Unsupported Claims Boundary

Exclude failure/error separation, first-order claims, traceback root cause,
direct code remediation, retry success, and main-merge readiness in both
dispositions.

## Next Chain and Gates

The success chain requires a method results review before any targeted
diagnostic-output candidate, operator review, approval, execution, results
review, or later retry chain. The blocked chain requires a module-grouping
source-recovery candidate, operator review, approval, execution, and results
review before re-entering this planning execution. Every transition is a
separate gate.

## Risk Controls

Preserve all execution controls: no diagnostics, remediation, classification,
cache access, log parsing, retry, full pytest, success claim, protected-state
mutation, runtime-output commit, evidence regeneration, provider/data/model
activity, predictive/profitability acceptance, runtime use, or broker execution.
Preserve origin/main, the integration branch/worktree, staged frozen evidence,
terminal archives, governance tags, and the META limitation.

## Guardrails

Default behavior remains deterministic and offline. A supplied test snapshot
must contain exactly 29 unique module paths, counts totaling 1,404, and top
counts `136, 131, 122, 112, 111`; malformed detail is rejected rather than
repaired. No runtime directory is written or tracked.

## Next Task if Successful

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_V1`

## Next Task if Blocked

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1`
