# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Results Review Status

## Result

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_ONLY_NOT_CACHE_READ_NOT_SOURCE_RECOVERY_NOT_DETAIL_BINDING_REATTEMPT_NOT_REENTRY_NOT_RETRY_NOT_MAIN`.
- Results-review digest: `09742be04ff9014323b6e845f3aa3e105ed9bfcfcfad42f0f55bf4930d63361a`.
- Payload-review digest: `e40aa95d531a9f198038664368be7cdb9d457ac140f805eac6d720c8f67382a0`.
- Results-review manifest digest: `56d9a3c629a34f662f4841a596c68316a13bdc310d51e7ba929fe8a32cea1aed`.
- Checklist: `119/119` checks passed with zero blockers.

## Source Materialization Execution

The review binds source execution digest
`3c1b7e6cddf2aedaec4e91dcaf742eaceb37d974b01387a8ba7f0da70cb0ac3b`,
payload digest
`1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7`,
and materialization digest-manifest digest
`198e28d641e08fbba9b49fb33a942d4ffcbd77c1ad1329048e25028234a6261c`.
The selected package remains
`PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY`.

## Source Approval and Operator Review

The review binds approval digest
`f8126d0d38793c9c562fca0217823ffdb919301596ec44b9bc33ff807fa77059`,
operator-review digest
`72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90`,
and candidate digest
`4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061`.

## Source Detail Exposure or Binding Failure Diagnosis

The diagnosis digest is
`8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41`
with primary class `COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE`.
The prior detail-binding execution remains historically blocked under digest
`9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca`
and reason
`COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE`.

## Source Recovery Results Review

- Results-review digest: `1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266`.
- Recovery-detail digest: `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`.
- Module-grouping digest: `34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.

## Retry Failure Context

The authoritative first retry result remains 24,877 passed, 1,292 failed,
112 errors, and 7 skipped at commit
`ab178b65c69f0274b0abbf9c20df102d35e78d34`. The prior root regression of
29,323 passed and 7 skipped remains non-retry evidence.

## Reviewed Cache Verification from Source Execution

This review did not read the detached cache. It reviewed the committed source
execution record showing verified `lastfailed` and `nodeids` hashes, 1,404 and
26,288 entry counts, successful subset verification, and no source-execution
cache modification.

## Complete 29-row Materialized Source Review

The committed payload contains exactly 29 ordered rows totaling exactly 1,404
failed-or-errored node IDs. Every row contains all required fields, a valid
source/basis/confidence binding, and one to five sorted sample node IDs. The
digest calculated over the committed rows equals the bound source payload
digest.

## Top Module Concentration and Priority Tiers

The top-five counts remain `136, 131, 122, 112, 111`, totaling 612
(`43.58974359%`). The top ten total 1,069 (`76.13960114%`). Priority tiers
remain 612, 457, and 335. These tiers are planning priorities only.

## Unsupported Claims Boundary

The review preserves no failure/error separation, first-order, traceback root
cause, direct-remediation, retry-success, or main-merge-readiness claim.

## Review Findings and Outputs

All 12 required findings passed. All 12 required review outputs are represented
as `GENERATED_RESEARCH_ONLY`, including payload-digest, integrity, cache-record,
29-row source, concentration, tier, sample, unsupported-claim, readiness, and
digest-manifest reviews.

## Recommendation and Next Gates

The reviewed source is ready only for a separately invoked
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_REATTEMPT_WITH_COMPLETE_SOURCE_V1`.
That reattempt has not been created or executed. After-v2 planning reentry
remains closed until the reattempt and its separate results review pass; all
diagnostic, remediation, new-retry, retry-review, and main-merge gates remain
separately governed.

## Authority Boundaries and Risk Controls

The review used only committed structures. It performed no cache read or
modification, materialization or recovery rerun, pytest or retry run, detail
binding, planning reentry, diagnostics, remediation, classification, provider
or data work, runtime action, or trading action. It did not modify evidence,
branches, worktrees, tags, main, or the integration branch, and did not commit
`.marketflow` or `.pytest_cache`. Predictive usefulness and profitability remain
not accepted; runtime and broker execution remain `NOT_AUTHORIZED`.
