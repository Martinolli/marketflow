# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Classification v2 Review Reentry v1 Plan

## Purpose

Execute planning-only module prioritization from reviewed, complete recovered
module-grouping rows. Fail closed when committed source evidence lacks the rows
needed for deterministic prioritization.

## Source Planning Reentry

Bind ready reentry digest
`8ddc6c2b288ae44f9a17132885d03586f0ba0a17ebfbb78d95d1653b01125927`
and preserve its planning-only and separate-results-review boundaries.

## Source Recovery Results Review

Bind results-review digest
`1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266`,
manifest digest `4a154d08b7e0a2c66cfe4247f7f10c4c539d96b617b64846e30561d1c94436b9`,
recovery execution digest `250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a`,
and detail digest `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`.

## Previous Blocked After-v2 Execution

Preserve the historical block
`MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS` and its
digests. The blocker was resolved for reentry authority, but the old execution
never became successful.

## Retry Failure Context

Preserve 24,877 passed, 1,292 failed, 112 errors, and 7 skipped as the first and
authoritative retry result. Root regression remains separate and non-authoritative
for retry evidence.

## Recovered Module Grouping Source

Use only reviewed rows containing module path, positive count, and bounded
samples. Require exactly 29 unique modules totaling 1,404 node IDs, expected
largest counts and top-five paths, top-five sum 612, and top-ten sum 1,069.

## Execution Scope

Generate research-only prioritization evidence. Do not execute diagnostics,
remediation, classification, retry, integration, runtime, or trading activity.

## Prioritized Module Planning Success Path

With complete reviewed rows, sort count descending and path ascending. Emit rank,
tier, deterministic percentage, sorted samples bounded to five, five candidate
planning buckets, low-to-medium confidence, module-level basis, and explicit
unsupported claims for each row.

## Blocked Recovered-Source-Unavailable Path

When complete committed rows are absent or inconsistent, create a blocked
artifact with the actual reason. Do not read cache, infer missing paths, repair
rows, or substitute aggregates for module-level detail. The current actual
execution follows this path.

## Priority Tier Policy

Ranks 1–5 are `PRIORITY_1_TOP_5_MODULE_GROUPS`; ranks 6–10 are
`PRIORITY_2_NEXT_5_MODULE_GROUPS`; ranks 11–29 are
`PRIORITY_3_REMAINING_MODULE_GROUPS`. Expected tier sums are 612, 457, and 335.

## Top Module Concentration

Preserve top-five concentration `43.58974359%` and top-ten concentration
`76.13960114%`. Concentration supports planning priority only and is not root
cause or remediation evidence.

## Diagnostic and Remediation Planning Buckets

The success path may generate research-only candidate reports for targeted
diagnostic capture, evidence-root review, path/cwd assumptions, digest drift,
and fixture isolation. It does not create or approve those candidates.

## Recommended Follow-on Candidate

Only after a successful execution results review may the process recommend
`PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS`. The current
blocked result does not make that recommendation actionable.

## Unsupported Claims Boundary

Keep failure/error classification, first-failure and first-error identification,
first-order inference, traceback root cause, direct remediation, retry success,
and main-merge readiness false.

## Authority Boundaries

No cache access, recovery, diagnostics, remediation, classification, retry,
integration, merge, provider/data, predictive, profitability, runtime, strategy,
paper-trading, or broker authority is granted.

## Next Chain

Success proceeds to a separate execution results review and only then optional
diagnostic capture ceremonies, a separately approved retry, retry results review,
and conditional main merge. Blocked execution proceeds to failure diagnosis and
possible source/reentry remediation; diagnostic capture, retry, and merge remain
closed.

## Next Gates

Success gates cover execution results review, optional diagnostic capture,
new-retry candidate/approval/execution/results review, and conditional merge.
Blocked gates cover failure diagnosis, possible source/reentry remediation, and
continued diagnostic and merge blocks.

## Risk Controls

Use recovered reviewed source only. Preserve cache, Git, evidence, provider,
data, model, predictive, runtime, and trading boundaries. Preserve origin/main,
the local integration branch and detached worktree, staged frozen evidence,
terminal archive evidence, published governance tags, and the META limitation.

## Guardrails

Default validation is deterministic and offline. Test-only snapshots are
explicitly injected. `.marketflow` and `.pytest_cache` remain ignored and
untracked. Run only focused execution and authorized source regressions; do not
run full pytest.

## Next Task If Successful

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_V1`

## Next Task If Blocked

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_CLASSIFICATION_V2_REVIEW_REENTRY_FAILURE_DIAGNOSIS_V1`
