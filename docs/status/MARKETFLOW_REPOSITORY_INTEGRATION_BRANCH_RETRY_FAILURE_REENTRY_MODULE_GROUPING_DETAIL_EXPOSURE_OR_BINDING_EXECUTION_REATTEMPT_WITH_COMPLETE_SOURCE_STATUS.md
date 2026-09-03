# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Execution Reattempt with Complete Source Status

## Status

The bounded reattempt is implemented. Its default offline execution binds the
reviewed, committed, complete 29-row materialized source and creates
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_V1`
with status
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_EXECUTED_COMPLETE_29_ROW_DETAIL_BOUND_FOR_REENTRY`.

The execution scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_ONLY_DETAIL_BINDING_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_RETRY_NOT_MAIN`.

## Source Evidence

The reattempt binds the materialization results-review digest
`09742be04ff9014323b6e845f3aa3e105ed9bfcfcfad42f0f55bf4930d63361a`,
payload-review digest
`e40aa95d531a9f198038664368be7cdb9d457ac140f805eac6d720c8f67382a0`,
and results-review manifest digest
`56d9a3c629a34f662f4841a596c68316a13bdc310d51e7ba929fe8a32cea1aed`.
It also binds the committed materialization execution digest
`3c1b7e6cddf2aedaec4e91dcaf742eaceb37d974b01387a8ba7f0da70cb0ac3b`,
payload digest
`1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7`,
and manifest digest
`198e28d641e08fbba9b49fb33a942d4ffcbd77c1ad1329048e25028234a6261c`.

The selected package remains
`PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY`.
The prior execution remains historically blocked under digest
`9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca`
and reason
`COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE`.

## Bound Detail

The binding contains exactly 29 deterministically ordered module rows totaling
1,404 failed-or-errored node IDs. The top-five counts remain 136, 131, 122,
112, and 111, totaling 612; the top-ten total remains 1,069. Priority tier
sums remain 612, 457, and 335. Samples remain sorted and bounded to no more
than five node IDs per module.

The binding source is
`REVIEWED_MATERIALIZED_COMPLETE_29_ROW_MODULE_GROUPING_SOURCE`, its basis is
`MATERIALIZATION_RESULTS_REVIEW_PAYLOAD_DIGEST_AND_SOURCE_BINDING`, and its
confidence is `HIGH_FOR_MODULE_GROUPING_ONLY`.

## Result and Next Gate

The detail is ready only for
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_RESULTS_REVIEW_V1`.
After-v2 planning reentry remains closed until that separate review passes.

## Boundaries

The reattempt does not read or modify cache, rerun materialization or source
recovery, rerun pytest or the integration retry, execute planning reentry,
diagnostics, remediation, or classification, or create a diagnostic or retry
candidate. It does not infer failure/error separation, first-result order,
traceback root cause, direct remediation, retry success, or main-merge
readiness.

No provider, market-data, dataset, metric, model, scoring, recommendation,
runtime, broker, evidence-regeneration, branch deletion, worktree deletion,
tag, integration-push, or main-push action is authorized. `.marketflow` and
`.pytest_cache` remain untracked. Predictive usefulness and profitability
remain not accepted; runtime and broker execution remain `NOT_AUTHORIZED`.

## Follow-on Results Review

The follow-on Detail Exposure or Binding Execution Reattempt with Complete
Source Results Review v1 is implemented. The successful reattempt remains its
committed source evidence. The review verifies only the complete 29-row binding
and does not read cache; rerun the reattempt, materialization, source recovery,
pytest, or the failed retry; execute planning reentry, diagnostics,
remediation, or classification; create a retry candidate; push protected
branches; commit `.marketflow` or `.pytest_cache`; accept usefulness or
profitability; or authorize runtime or broker execution.
