# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Results Review v1 Plan

## Purpose

Create one deterministic, offline, digest-bound results-review artifact for the
successful Module Grouping Source Recovery Execution v1. Review committed source
facts only; do not read cache or execute recovery again.

## Source Recovery Execution

Bind execution digest `250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a`,
recovery-detail digest `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`,
and digest-manifest digest `940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc`.
The selected package remains
`PACKAGE_RECOVER_MODULE_GROUPING_DETAIL_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY`.

## Source Approval and Candidate Chain

Bind the approval, operator-review, candidate, blocked after-v2 execution,
blocked manifest, classification results-review v2, execution v2, module
grouping, review-manifest, approval-v2, source-manifest, and staged-inventory
digests. Preserve
`MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS` as the
reason that preceded recovery.

## Retry Failure Context

Preserve the first detached result as authoritative: 24,877 passed, 1,292
failed, 112 errors, and 7 skipped. The later root regression is not retry
evidence.

## Cache Verification Review

Review only the committed source artifact's hash, count, parseability, and
subset facts for `lastfailed` and `nodeids`. Do not open, parse, or modify either
cache file in this review.

## Recovered Module Grouping Detail Review

Verify 1,404 node IDs, 29 module paths, per-module counts, deterministic ordering,
and bounded samples of at most five node IDs per module.

## Top Module Source Detail Review

Verify largest counts `136, 131, 122, 112, 111`, the exact top-five module
paths, top-five sum 612 (`43.58974359%`), and top-ten sum 1,069
(`76.13960114%`).

## Unsupported Claims Boundary

Keep failure/error classification, first-failure and first-error identification,
first-order inference, traceback root-cause inference, direct remediation,
retry-success, and main-merge-readiness claims false. No diagnostic,
remediation, or classification execution occurs in this review.

## Source Recovery Limitations

The cache source does not distinguish failures from errors, preserve first
failure order, or provide tracebacks. Recovered grouping is planning source
only; it neither proves root cause nor authorizes retry or main merge.

## Success Review Path

Create the ready review only when every source digest, cache verification fact,
module detail, concentration, limitation, unsupported-claim boundary, and
authority boundary matches. A ready review opens only the separate planning
re-entry gate.

## Blocked Review Path

Fail closed with the blocked review artifact and an actual reason when source
detail is missing or inconsistent. Do not repair, read cache, rerun recovery,
invent paths, or run pytest.

## Authority Boundaries

The review grants no diagnostic, remediation, classification, retry,
integration, merge, predictive, profitability, runtime, strategy, paper-trading,
or broker authority. It makes no provider or data request and leaves staged
evidence and protected Git state unchanged.

## Next Chain

The success chain proceeds through a separately authorized after-v2 planning
re-entry, any selected remediation/method and its review, optional targeted
diagnostic capture ceremonies, a new retry candidate/approval/execution/results
review, and only then a possible main-merge approval. The blocked chain proceeds
to results-review failure diagnosis and, if needed, a recovery-remediation
candidate; planning re-entry, retry, and main merge remain closed.

## Next Gates

Success gates cover after-v2 planning re-entry, separately authorized method or
remediation execution and review, optional diagnostic capture candidate/review/
approval/execution/results review, new retry candidate/approval/execution/results
review, and conditional main-merge approval. Blocked gates cover review-failure
diagnosis, possible source-recovery review remediation, and continued planning
and main-merge blocks.

## Risk Controls

Do not recover grouping, read or modify cache, parse logs, run diagnostics,
execute remediation or classification, rerun retry or full pytest, create any
downstream ceremony, push protected branches, mutate tags or evidence, track
runtime outputs, call providers, process market data, train models, score a
strategy, generate recommendations, or change acceptance/authorization state.
Preserve origin/main, the integration branch and worktree, staged frozen and
terminal archive evidence, published governance tags, and the META limitation.

## Guardrails

Default validation is deterministic and offline. Generated artifacts use an
isolated temporary directory. `.marketflow` and `.pytest_cache` remain ignored
and untracked. Focused review, source-execution regression, and source-approval
regression tests are allowed; full pytest is not run by contract.

## Next Task If Successful

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1`

## Next Task If Blocked

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1`
