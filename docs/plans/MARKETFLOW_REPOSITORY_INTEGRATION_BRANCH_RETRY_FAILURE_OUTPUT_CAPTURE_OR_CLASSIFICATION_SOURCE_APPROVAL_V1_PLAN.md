# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Approval v1 Plan

## Purpose

Create an offline, deterministic, attestation-bound approval selecting one
reviewed classification-source acquisition package for future execution only.
This plan does not acquire a source, execute diagnostics, or retry integration.

## Source Operator Review

Bind operator-review digest
`f73a94b36e7884d778c980d4989c999c383a04310f45e58b6ffae9da6172aa8c`.
The operator review remains source evidence and is not rewritten as an
execution or results-review record.

## Operator Attestation

Require the exact non-secret phrase and decision, source-review and candidate
digests, method-execution and blocked-manifest digests, retry execution commit
and counts, classification blocker, detached worktree path and HEAD, staged
evidence digest, selected package, approval-only scope, and every closed
authority confirmation. Reject any missing or changed binding.

## Source Output-Capture Candidate

Bind candidate digest
`fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518`.
The candidate supplies the reviewed packages, requirements, plan, planned
outputs, and evidence-preservation boundary.

## Source Method Execution

Bind method-execution digest
`522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562`
and blocked-manifest digest
`3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f`.
That execution remains blocked because authoritative retry detail was not
persisted or locatable.

## Retry Failure Context and Approval Scope

Preserve the authoritative detached retry at `24877 passed, 1292 failed, 112
errors, 7 skipped`. Root-worktree regression output is not retry evidence.
Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.

## Selected Output-Capture Package

Approve
`PACKAGE_READ_EXISTING_DETACHED_PYTEST_CACHE_LASTFAILED_AS_CLASSIFICATION_SOURCE`
as `APPROVED_FOR_FUTURE_OUTPUT_CAPTURE_EXECUTION_ONLY`. It is selected,
approved, and authorized for a future separate execution task, but remains
unexecuted. This approval does not read cache artifacts.

## Approved Future Output-Capture Requirements

Approve all eighteen reviewed requirements. The future execution must bind the
failed retry, treat root regression and diagnostics as non-retry evidence,
read a detached-worktree cache only read-only, fail closed if absent, use only
an explicitly provided non-secret log path if applicable, and leave retries,
results review, integration success, main merge, runtime, and trading closed.

## Approved Future Output-Capture Plan

Approve the ten-step plan to verify source and worktree evidence, inventory
classification sources, hash and parse a selected source read-only, report
availability, fail closed when unavailable, and preserve downstream gates.
Every step remains `NOT_EXECUTED`.

## Planned Outputs

Carry the classification-source inventory, pytest-cache reports, optional log
source report, availability and missing-source reports, diagnostic recommendation,
authority-boundary report, and digest manifest as
`AUTHORIZED_NOT_GENERATED`.

## Supporting and Blocked Packages

Keep the operator-provided log, diagnostic capture, and targeted diagnostic
inventory packages available but unselected. Keep committed-status-only,
root-regression substitution, authoritative-retry replacement, and
main-merge-despite-missing-output packages blocked and unapproved.

## Next Chain and Gates

The gated chain is source execution, source results review, classification
method reentry, a new retry candidate, retry approval, retry execution, retry
results review, and only then main-merge approval if that new retry passes.
Every transition remains separately gated.

## Risk Controls and Guardrails

Do not read `.pytest_cache`, parse logs, run diagnostics, capture output, rerun
pytest, replace the failed retry, create a results review, mutate staged
evidence, call providers, commit `.marketflow`, push main or integration,
delete/reset/force-push, prune remotes, mutate tags, or create predictive,
profitability, runtime, or broker authority. Preserve `origin/main`, the local
integration branch, detached worktree, frozen evidence, terminal archive,
published governance tags, and the META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_V1`
may be invoked separately after this approval.
