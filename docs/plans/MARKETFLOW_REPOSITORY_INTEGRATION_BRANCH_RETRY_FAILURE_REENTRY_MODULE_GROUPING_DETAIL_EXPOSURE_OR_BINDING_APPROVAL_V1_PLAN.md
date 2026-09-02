# MarketFlow Repository Integration Branch Retry Failure Reentry Module Grouping Detail Exposure or Binding Approval v1 Plan

## Purpose

Create a deterministic, offline, attestation-bound approval for one future
detail exposure or binding execution. No recovered row is exposed or bound by
this approval.

## Operator Attestation

Require the exact non-secret approval phrase, operator decision, selected
package, source digests, retry facts, recovered summary confirmations, and all
closed-boundary confirmations. Reject missing or changed inputs.

## Source Operator Review and Candidate

Bind the ready operator review at digest
`8ea86457a92bccbcb9712b208140300964fbcf3c361f21819aa008cd7ebec17b`
and its candidate at digest
`e25825ebcbccef1186655ba300e505b4b992959ba3bbc725178af9882a730f23`.
The review remains historical source evidence; the explicit attestation makes
the separate selection and approval.

## Source Reentry Failure Diagnosis and Blocked Execution

Bind the `COMMITTED_REENTRY_SOURCE_DETAIL_GAP` diagnosis and the blocked
reentry reason
`RECOVERED_MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_REENTRY_ARTIFACT`.
The prior blocked execution remains historically blocked.

## Source Recovery Results Review

Bind the reviewed recovery execution, results-review, detail, and manifest
digests. Do not read detached cache or rerun recovery in this task.

## Retry Failure Context

Preserve the authoritative first retry result: 24,877 passed, 1,292 failed,
112 errors, and 7 skipped. The latest root regression is not retry evidence.

## Recovered Module Grouping Source Summary

Preserve the reviewed summary of 1,404 failed-or-errored node IDs across 29
modules, largest counts `[136, 131, 122, 112, 111]`, top-five sum 612, top-ten
sum 1,069, and the five known top module paths. Do not infer the other paths.

## Available and Missing Committed Detail

Preserve the committed aggregates, known top-five paths, concentrations, and
digests. Preserve as missing all 29 paths, all per-path counts, all bounded
samples, the full 29-row detail, and a committed snapshot sufficient for
deterministic priority-tier planning.

## Approval Scope and Selected Package

Select
`PACKAGE_EXPOSE_OR_BIND_COMPLETE_RECOVERED_MODULE_GROUPING_DETAIL_FOR_REENTRY`
for future Detail Exposure or Binding Execution v1 only. Approval is not
execution, detail exposure, binding, source recovery, planning reentry, retry,
or main-merge authority.

## Approved Future Requirements and Plan

Approve all 31 reviewed requirements. The ten-step plan must bind source
evidence, use a controlled complete source, verify all 29 rows and preserved
concentrations, produce a bounded planning source, retain unsupported-claim
limits, require results review, and leave downstream actions gated. Every plan
step remains `NOT_EXECUTED`.

## Planned Outputs

Authorize the 12 specified approval, source-identification, binding,
concentration, limitations, reentry-enablement, recommendation, and digest
outputs as `AUTHORIZED_NOT_GENERATED`.

## Supporting and Blocked Packages

Keep five supporting alternatives available but unselected. Keep inference,
pytest rerun, direct diagnostic capture, premature retry, and premature main
merge blocked and unapproved.

## Next Chain and Gates

Proceed next to separate detail exposure/binding execution and results review.
Only then may after-v2 planning reentry be considered. Diagnostics,
remediation/method review, a new retry, and main merge retain their own review,
approval, execution, and results gates.

## Risk Controls and Guardrails

Preserve origin/main, the local integration branch, detached worktree, staged
frozen evidence, terminal archives, published governance tags, and the META
limitation. Do not access providers, market data, credentials, cache, runtime,
or broker systems. Do not claim failure/error separation, first-order failure,
traceback root cause, direct remediation, retry success, or merge readiness.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REENTRY_MODULE_GROUPING_DETAIL_EXPOSURE_OR_BINDING_EXECUTION_V1`
