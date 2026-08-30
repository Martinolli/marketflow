# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate v1 Plan

## Purpose and Source Diagnosis

Create a deterministic, offline, digest-bound candidate describing safe future
methods for classifying the residual authoritative retry failures. Source
diagnosis digest:
`f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1`.

## Failure Context and Retry Environment

The detached-worktree retry used the root virtualenv Python and returned exit
code `1`: `24877 passed, 1292 failed, 112 errors, 7 skipped`. The original run
was `24481 passed, 1300 failed, 500 errors, 7 skipped`; the delta is `+396`
passed, `-8` failed, `-388` errors, and no skipped-count change.

The integration branch and detached worktree remain at
`220fbc220365fce9cae13ab4853cddff118c0187`. Staged evidence remains bound to
`06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`.

## Candidate Scope and Philosophy

Residual failures are a failure-domain and method-selection problem. Classify
them before choosing a repair or attempting another retry. This artifact is
candidate-only: no diagnostic execution, remediation, retry, results review,
integration success, main merge, runtime authority, or trading authority is
created.

## Proposed Method Packages

The eight packages cover authoritative-output classification, additional
ignored evidence roots, path/CWD assumptions, digest and historical-artifact
drift, test isolation/cache/environment diagnostics, integration-stack
rebuild, root-regression substitution, and main merge despite failure. The
last three are blocked; all eight remain unselected, unapproved, and
unexecuted.

## Recommended Method Package

`PACKAGE_CLASSIFY_RETRY_FAILURE_DOMAINS_FROM_AUTHORITATIVE_OUTPUT` is
`RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED`. Classification is safer than
guessing a remediation path given the remaining `1,292` failures and `112`
errors.

## Future Method Requirements and Plan

Future work must bind the source diagnosis and retry counts, preserve the root
regression boundary and staged evidence, avoid a full-pytest rerun, record
failure/error modules and first traces, classify likely root-cause families,
and keep all downstream authority closed. The ten-step plan is
`PLANNED_NOT_EXECUTED` and uses persisted authoritative records only.

## Planned Outputs

Eleven future outputs cover domain and module manifests, first traces,
evidence-root/path/digest/branch/isolation reports, a recommended-method
summary, and digest manifest. Every output is `PLANNED_NOT_GENERATED`.

## Non-Goals, Next Chain, and Gates

No retry, full pytest as retry evidence, remediation, results review, evidence
mutation, provider call, `.marketflow` commit, protected-branch push, deletion,
tag mutation, main-merge approval, usefulness/profitability acceptance,
runtime authority, or trading authority is in scope.

The next gated chain is operator review, approval if selected, execution if
approved, results review, then a separately reviewed and approved new retry.
Main-merge approval remains blocked until a future retry results review passes.

## Risk Controls and Guardrails

Preserve `origin/main`, the integration branch, detached worktree, staged
frozen evidence, terminal archive evidence, published governance tags, and the
META limitation. Separate review and approval are required before any method
execution.

Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_OPERATOR_REVIEW_V1`.
