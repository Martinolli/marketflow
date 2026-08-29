# MarketFlow Repository Merge Strategy Candidate v1 Plan

## Purpose

Prepare a conservative, non-authorizing choice set for possible future
integration of the terminal evidence stack after remote governance tags were
verified.

## Source Tag Push Results Review

Source commit: `71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`.
Review digest:
`83ef5805ead9310494bbe3cb2122ffb8946861d36b3b20bcb81f2376ee9af0b4`.
Remote-manifest review digest:
`cf406bc974ebd88ffdfd1567b7e175fe17128e4e2adf770efbbf240df3819d5c`.

## Repository Context

The source review recorded 301 local branches, 273 remote refs, 574 total refs,
32 local tags, four verified remote terminal tags, and zero extra namespace
tags. `origin/main` remains protected at
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.

## Candidate Scope

`REPOSITORY_MERGE_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_MERGE_NOT_DELETE_NOT_MAIN`

## Merge Strategy Philosophy

Protect main, preserve terminal evidence traceability, avoid destructive
cleanup, and keep planning separate from execution. The goal is to decide
later whether to preserve branch/tag-only traceability, validate on a temporary
integration branch, or consider a separately approved main integration.

## Recommended Merge Strategy

Recommend `PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION` for
operator review without selecting it. A future temporary branch based on
protected main provides a non-main validation surface for this large stacked
governance chain.

## Proposed Merge Packages

Six packages cover branch/tag-only preservation, temporary integration-branch
validation, future squash merge, future merge commit, selective docs/status
integration, and deferral until cleanup planning. Every package remains
unselected, unapproved, and unexecuted.

## Merge Prerequisites

Operator review and approval are required before an integration branch or main
merge. Require clean state, protected main, verified tags, full integration
tests, diff review, separate main-push approval, no force push, and no branch
deletion before cleanup approval.

## Candidate Integration Branch Plan

`integration/marketflow-terminal-evidence-stack-validation-v1` is planned from
`origin/main`, using the results-review branch/commit as source. Its status is
`PLANNED_NOT_CREATED`; no branch, merge, test run, main merge, or main push is
performed here.

## Merge Non-Goals

Do not merge, create the integration branch, push main, rebase, squash,
cherry-pick, delete branches, clean up, mutate tags, publish more tags, or imply
usefulness, profitability, runtime, or trading authority.

## Chain Merge Impact Summary

The candidate records ten evidence/governance chains. Each is preserved for
future integration-branch validation, requires operator review, requires no
merge now, and requires no main push now.

## Next Chain

Operator review precedes any selection or approval. Integration-branch
execution and review, any main-merge approval/execution, and branch cleanup all
remain separately gated future tasks.

## Next Gates

Merge-strategy review, optional approval, integration execution/review,
optional main approval/execution, and cleanup candidate/approval/execution are
distinct gates.

## Risk Controls

No merge, integration branch, rebase, squash, cherry-pick, main/force push,
deletion, prune, tag mutation, provider, data, metric, model, recommendation,
runtime, broker, or trading action is allowed. Preserve published tags,
terminal archive evidence, and the META limitation.

## Non-Goals

This candidate does not select a package, approve integration, create cleanup
authority, or change predictive/profitability acceptance.

## Guardrails

Default tests are deterministic and offline. `.marketflow` remains ignored and
untracked. Next task:
`MARKETFLOW_REPOSITORY_MERGE_STRATEGY_OPERATOR_REVIEW_V1`.
