# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Execution v1 Plan

## Purpose

Execute the approved package that turns reviewed detached-cache grouping
evidence into a bounded, non-secret, committed 29-row planning source. This is
materialization only, not a retry, diagnosis, remediation, or classification.

## Source Approval

Bind approval digest
`f8126d0d38793c9c562fca0217823ffdb919301596ec44b9bc33ff807fa77059`
and package
`PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY`.

## Source Operator Review and Candidate

Bind operator-review digest
`72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90`
and candidate digest
`4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061`.

## Source Detail Exposure or Binding Failure Diagnosis

Bind diagnosis digest
`8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41`,
class `COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE`, and its prior
blocked execution evidence. Materialization closes only the source-availability
gap; it does not revise the historical blocked result.

## Source Recovery Results Review

Bind results-review digest
`1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266`,
recovery-detail digest
`a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`,
and module-grouping digest
`34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.

## Retry Failure Context

Preserve the authoritative first retry result of 24,877 passed, 1,292 failed,
112 errors, and 7 skipped. The prior 29,323-passed root regression is not retry
evidence.

## Execution Scope

The scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_ONLY_COMPLETE_DETAIL_SOURCE_CREATION_NOT_RETRY_NOT_MAIN`.

## Reviewed Cache Verification

Read only the reviewed `lastfailed` and `nodeids` files. Before result use,
verify their exact SHA-256 digests, 1,404 and 26,288 entry counts, and that
`lastfailed` is a subset of `nodeids`. Do not modify or commit cache data.

## Complete 29-row Materialization Success Path

Group `lastfailed` node IDs by their module-path prefix, sort by descending
count then ascending path, assign orders 1 through 29, assign tiers 1-5,
6-10, and 11-29, retain at most five sorted samples per module, and bind the
result into tracked service source. Require all specified totals and compare
the live materialization with the committed source before success.

## Blocked Source-unavailable Path

Fail closed if either file is absent or unparseable, a hash/count/subset check
fails, a row/path/count/concentration/tier/sample invariant fails, or the live
rows differ from the committed source. Record the actual reason and recommend
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_FAILURE_DIAGNOSIS_V1`.

## Materialized Row Format

Each row binds module path, failed-or-errored node-ID count, deterministic
percentage, priority order and tier, one to five sorted sample node IDs and
their count, reviewed-cache source, verification basis, grouping-only
confidence, and all unsupported claims.

## Top Module Concentration Preservation

Require top-five counts `136, 131, 122, 112, 111`, top-five sum 612 and
percentage `43.58974359`, and top-ten sum 1,069 and percentage `76.13960114`.

## Priority Tier Enablement

Require tier totals 612, 457, and 335 with respective percentages
`43.58974359`, `32.54985755`, and `23.86039886`. Tiers prioritize future
review only.

## Unsupported Claims Boundary

Do not claim failure/error separation, first failure or error, first-result
order, traceback root cause, direct remediation, retry success, or main-merge
readiness.

## Authority Boundaries

Do not run pytest, retry, recovery, diagnostics, remediation, classification,
binding reattempt, planning reentry, provider or data work, training, scoring,
runtime, or trading. Do not push main or the integration branch, mutate tags,
delete branches/worktrees, regenerate evidence, or commit ignored outputs.

## Next Chain

On success, proceed to the materialization results review, then separately
govern detail binding, after-v2 planning reentry, remediation/method review,
diagnostic capture, a new retry, retry results review, and main-merge approval.
On failure, proceed only to materialization execution failure diagnosis and an
alternate candidate if warranted.

## Next Gates

Success opens only
`complete_29_row_module_grouping_detail_source_materialization_results_review`.
Detail binding remains gated by that review; every planning, diagnostic, retry,
results-review, and merge gate remains closed. A blocked execution opens only
the failure-diagnosis and possible alternate-materialization gates.

## Risk Controls

Use deterministic offline tests, fixed hashes and counts, strict payload
invariants, bounded samples, digest/payload separation, immutable source-chain
bindings, fail-closed validation, and explicit false downstream authorities.
Preserve origin main, integration state, staged frozen evidence, terminal
archive evidence, governance tags, and the META limitation.

## Guardrails

The committed rows are grouping evidence only and are not a root-cause report.
The historical failed retry remains authoritative. A separate results review
is mandatory before any detail-binding reattempt, and a separate approval is
mandatory before any new retry.

## Next Task if Successful

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1`

## Next Task if Blocked

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_FAILURE_DIAGNOSIS_V1`
