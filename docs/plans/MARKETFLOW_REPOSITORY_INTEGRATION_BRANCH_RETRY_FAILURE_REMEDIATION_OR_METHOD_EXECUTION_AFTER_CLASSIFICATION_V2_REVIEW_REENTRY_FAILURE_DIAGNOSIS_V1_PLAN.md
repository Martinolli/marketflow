# MarketFlow Repository Integration Branch Retry Failure Reentry Execution Failure Diagnosis v1 Plan

## Purpose

Create an offline, deterministic, digest-bound diagnosis of why the approved
after-v2 planning reentry blocked, without executing or repairing anything.

## Source Blocked Reentry Execution

Bind the blocked artifact, status, scope, execution digest, blocked-manifest
digest, and exact blocked reason from committed source constants.

## Source Planning Reentry

Preserve the accepted planning-reentry digest and its limited future-execution
authority. Acceptance did not itself transport the full recovery rows into the
downstream execution interface.

## Source Recovery Results Review

Preserve the recovery execution, recovery-detail, digest-manifest, and
results-review digests. Treat the review as valid historical evidence; do not
rerun recovery or read the detached cache.

## Retry Failure Context

Preserve the authoritative result of 24,877 passed, 1,292 failed, 112 errors,
and 7 skipped. The latest root regression is not retry evidence.

## Recovered Module Grouping Source Summary

Preserve 1,404 failed-or-errored node IDs across 29 modules, the largest counts
`136, 131, 122, 112, 111`, top-five sum 612, top-ten sum 1,069, and the five
committed module records. Do not expose or infer the remaining 24 records.

## Available and Missing Committed Detail

Available details are counts, module total, largest counts, top-five paths and
counts, concentration facts, source digests, and the recovery-detail digest.
Missing details are all 29 paths, path-bound counts, bounded samples, complete
grouping rows, and a committed source snapshot sufficient for deterministic
priority-tier planning.

## Diagnosis Questions and Findings

Answer the twelve prescribed questions from committed evidence. Record that
recovery and its review succeeded, reentry authority was valid, complete detail
was not carried forward, and fail-closed behavior correctly prevented invented
module identities.

## Root Cause Classification

Classify only `COMMITTED_REENTRY_SOURCE_DETAIL_GAP`. Do not classify the
original retry failures or make traceback, failure/error-separation, first-order,
or direct-remediation claims.

## Not Root Causes

Exclude origin/main, the integration branch, detached worktree state, staged
evidence, source-recovery cache verification, a retry/full-pytest rerun,
providers, market data, runtime, and broker execution.

## Recommended Next Package

Recommend
`PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY`
for a separate candidate. Reduced top-five planning changes the contract;
inference, direct diagnostics, a new retry, and main merge remain blocked.

## Next Chain

Proceed through detail-exposure/binding candidate, operator review, approval,
execution, and results review before reentering planning. Only a successful
planning and remediation/method review can lead to diagnostic capture. A new
retry requires its own candidate, approval, execution, and results review;
main-merge approval remains last.

## Next Gates

Every candidate, approval, execution, and results-review gate remains separate.
No package created by this diagnosis authorizes its successor.

## Risk Controls and Guardrails

Use committed constants only. Do not expose detail, read cache, parse logs, run
diagnostics, execute remediation/classification, rerun tests, mutate evidence,
push protected branches, call providers, or authorize research acceptance,
runtime, trading, or broker execution. Keep `.marketflow` and `.pytest_cache`
ignored and untracked.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_CANDIDATE_V1`
