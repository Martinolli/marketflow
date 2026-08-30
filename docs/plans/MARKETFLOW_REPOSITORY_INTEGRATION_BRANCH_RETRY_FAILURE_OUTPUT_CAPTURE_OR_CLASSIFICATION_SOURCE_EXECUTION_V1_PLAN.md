# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Execution v1 Plan

## Purpose

Execute the approved package by reading an existing detached-worktree pytest
cache only. Produce a classification-source capture when `lastfailed` is
usable, otherwise fail closed. Do not run pytest or diagnostics.

## Source Approval

Bind approval digest
`41052b8621f57721383bc7d8fc416c95e9fef4d5af49b94278ede43209304d33`
and the approved package
`PACKAGE_READ_EXISTING_DETACHED_PYTEST_CACHE_LASTFAILED_AS_CLASSIFICATION_SOURCE`.
The approval remains source evidence and creates no execution result itself.

## Retry Failure Context

Preserve the authoritative detached retry at `24877 passed, 1292 failed, 112
errors, 7 skipped`. Root regression is not retry evidence. The cache capture
must neither replace the failed result nor infer failure/error classes that the
cache does not encode.

## Execution Scope

Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.
The task is classification-source capture only.

## Read-Only Cache Inputs

After all source, ref, worktree, frozen-evidence, and tracking prechecks pass,
read `.pytest_cache/v/cache/lastfailed` as JSON. Read
`.pytest_cache/v/cache/nodeids` only when it exists. Hash both files, never
write them, and never invoke pytest or `pytest --cache-show`.

## Cache Capture Success Path

When `lastfailed` is a non-empty JSON object with usable node IDs, create the
success artifact, hash the full sorted node-ID set, retain a bounded sample,
summarize module paths, record ordering and failure/error limitations, and
route to a separate results review.

## Cache-Unavailable Blocked Path

When `lastfailed` is missing, empty, corrupt, non-JSON, or insufficient, create
the blocked artifact and blocked-manifest digest. If any protected-state
precheck fails, do not read cache and use the precheck-failed blocked status.
The blocked next task is a diagnostic-output-capture candidate, not a retry.

## Authority Boundaries

No retry, full pytest, diagnostic command, new diagnostic output, operator-log
parse, remediation, results review, integration success, main merge, provider
request, data/model action, runtime authority, or trading authority is created.

## Next Chain and Gates

Success routes to output-capture results review, classification reentry, a new
retry candidate, retry approval, retry execution, retry results review, and
only then main-merge approval if the retry passes. Blocked execution routes
through diagnostic-output candidate, review, approval, execution, results
review, and classification reentry. Every transition is separately gated.

## Risk Controls and Guardrails

Read existing cache only; do not modify it or treat it as new retry evidence.
Do not run pytest, mutate staged evidence, call providers, commit `.marketflow`
or `.pytest_cache`, push main or integration, delete/reset/force-push, prune
remotes, mutate tags, or create predictive, profitability, runtime, or broker
authority. Preserve `origin/main`, the integration ref, detached worktree,
frozen evidence, terminal archive, published governance tags, and META
limitation.

## Next Tasks

Success:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_RESULTS_REVIEW_V1`.

Blocked:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_V1`.
