# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Results Review v1 Plan

## Purpose

Create a read-only, digest-bound review of the successful detached pytest-cache
classification-source capture. Verify cache identity, module summary,
limitations, protected state, and authority boundaries without executing
classification reentry or another retry.

## Source Execution

Bind execution digest
`b7c987e76b02a026bc118ae05801e4ba02c92bdadb81df9562e28a646b4f80bb`
and classification-source manifest
`9218bad7b0b176bd3b4398293304159f22c1772fad0fa91b6e1d275a770ebcca`.
The execution remains source evidence and is not repeated or replaced.

## Retry Failure Context

Preserve the authoritative retry at `24877 passed, 1292 failed, 112 errors, 7
skipped`. Root regression and cache contents are not retry evidence and do not
override that failure.

## Cache Review

Read `lastfailed` and `nodeids` only for verification. Require their exact
SHA-256 digests, valid JSON structures, and counts of 1,404 and 26,288. Fail
closed on absence, corruption, drift, or tracking-boundary violations. Never
modify, delete, populate, or commit cache files.

## Classification-Source Review and Limitations

Verify that the classification source contains node IDs, the module summary
contains 29 untruncated module rows, and the largest counts are `136, 131, 122,
112, 111`. Preserve the inability to distinguish failures from errors and the
lack of authoritative first-failure order. Do not infer either property.

## Authority Boundaries

The review may mark the source ready for future classification-method reentry,
but it does not create reentry, a new classification candidate, retry
candidate, retry execution/results review, integration success, or main-merge
approval.

## Next Chain and Gates

The separate chain is classification-method reentry, an optional new method
candidate, a new retry candidate after classification/remediation, retry
approval, retry execution, retry results review, and only then main-merge
approval if that retry passes. Each transition remains separately gated.

## Risk Controls and Guardrails

Do not run pytest or diagnostics, capture output, parse logs, mutate staged
evidence, call providers, commit `.marketflow` or `.pytest_cache`, push main or
integration, delete/reset/force-push, prune remotes, mutate tags, or create
predictive, profitability, runtime, or broker authority. Preserve
`origin/main`, the integration ref, detached worktree, frozen evidence,
terminal archive, published governance tags, and META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1`
may be invoked separately after this review.
