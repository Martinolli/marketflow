# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Candidate Operator Review v1 Plan

## Purpose

Create a deterministic, offline, digest-bound review of the existing
module-grouping source-recovery candidate. The review evaluates planning
packages without selecting, approving, or executing any package.

## Source Module Grouping Source Recovery Candidate

The source candidate is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1`,
bound by digest
`4c0542256406f1db4d86f32958d738f6c86dc83ea2dd2132e2d54bcf5afb8bcb`.
It remains the source evidence and grants no recovery authority.

## Source Blocked After-v2 Execution

The review preserves blocked reason
`MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS`, execution
digest `7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755`,
and blocked-manifest digest
`c3d644957eb536ede1d725c912f0211a0d84aa72e56d5f8cbed2e0939a907cef`.

## Source Classification Results Review v2

The results-review-v2, execution-v2, and module-grouping digests remain bound.
Classification still reports 1,404 failed-or-errored node IDs across 29 modules,
with largest counts `136, 131, 122, 112, 111`. No module identities are inferred.

## Retry Failure Context

The first retry result remains authoritative: 24,877 passed, 1,292 failed, 112
errors, and 7 skipped at retry commit
`ab178b65c69f0274b0abbf9c20df102d35e78d34`. The latest root full regression is
not retry evidence.

## Known Available and Missing Detail

Available detail is limited to aggregate retry counts, total classified node-ID
count, module count, largest module counts, module-grouping digest, and source
execution/review digests. Missing detail remains module paths, per-path counts,
bounded samples, grouping-report content, and a committed prioritization source.

## Review Scope

The scope is review-only. It permits deterministic review of committed candidate
constants and prohibits cache access, log parsing, diagnostics, remediation,
classification, retry, full pytest, provider/data actions, and repository
integration or release mutations.

## Reviewed Candidate Philosophy

The candidate correctly fails closed on missing committed grouping detail and
offers controlled future ways to recover the source without inventing module
identities or rerunning the failed authoritative retry.

## Reviewed Module Grouping Source Recovery Packages

Ten packages are reviewed: five remain potentially reviewable and unselected;
five remain blocked as insufficient or prohibited. The recommended read-only
detached-cache package remains `REVIEWED_RECOMMENDED_PACKAGE_FOR_OPERATOR_ASSESSMENT_NOT_SELECTED`.

## Reviewed Future Source Recovery Requirements

All 23 candidate requirements are reviewed as required for a future recovery
execution. Each retains execution status `NOT_EXECUTED`.

## Reviewed Future Source Recovery Plan

All 10 candidate plan steps are reviewed as `REVIEWED_PLANNED_NOT_EXECUTED`.
No source location, cache content, module path, or node-ID sample is obtained.

## Reviewed Planned Outputs

All 10 proposed outputs are reviewed as `REVIEWED_PLANNED_NOT_GENERATED` and
remain ungenerated.

## Reviewed Non-Goals

All 33 non-goals remain `REVIEWED_ACTIVE`, including no recovery execution,
diagnostics, retry, main merge, provider/data work, runtime use, or trading.

## Recommendation

Keep
`PACKAGE_RECOVER_MODULE_GROUPING_DETAIL_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY`
as the reviewed recommendation. Operator selection and a separate digest-bound
approval are required before any execution.

## Next Chain

If selected, the chain is approval, execution, and results review for source
recovery; conditional after-v2 planning re-entry and remediation/method review;
conditional targeted diagnostic candidate, approval, execution, and review;
then a separately governed retry candidate, approval, execution, and results
review; finally main-merge approval only if that new retry passes.

## Next Gates

Fourteen gates preserve the chain from conditional source-recovery approval
through conditional main-merge approval. Each later gate remains closed until
the preceding result is separately reviewed.

## Risk Controls

Fifty-nine controls preserve review-only authority, including explicit controls
that this review does not select or approve a package. Existing candidate
controls continue to prohibit inference, cache mutation, retry substitution,
evidence regeneration, provider/data/model actions, and runtime/trading use.

## Guardrails

No detached cache is read or modified. No module detail is recovered or exposed.
No diagnostics, remediation, classification, retry, or full suite is run. No
integration/main branch or tag is mutated. `.marketflow` and `.pytest_cache`
remain ignored and untracked.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_APPROVAL_V1_IF_SELECTED`
