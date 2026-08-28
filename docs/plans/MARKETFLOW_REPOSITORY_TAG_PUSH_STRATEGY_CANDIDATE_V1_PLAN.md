# MarketFlow Repository Tag Push Strategy Candidate v1 Plan

## Purpose

Create a deterministic, offline, digest-bound candidate for deciding whether four verified local annotated governance tags should later be published to `origin`. The candidate proposes options only; it does not select, approve, authorize, or execute publication.

## Source Tagging Results Review

Bind the committed results review at `5daeecb556e4964eda623e5db89142f0e2e0db90`, review digest `d63ce543d95b936cee8ec5fb8f85c17fc20a3cf66a73d7774e8f55d23f7fad4a`, and tag-manifest review digest `cfcc8411902b65aa28e02d2987b4b180dbbb5e344228d31833243657a0c281e3`. Preserve its complete upstream digest chain without rerunning source builders or inspecting Git tags.

## Repository Context

Preserve `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`, the source branch inventory of 296/268/564, and its tag counts of 32 total, four approved namespace tags, zero extra namespace tags, and zero approved remote tags.

## Candidate Scope

Use `REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN`. Build entirely from committed constants by default. If a source review is supplied, validate its exact review and manifest digests before binding its evidence.

## Tag Push Philosophy

Publish only verified local annotated governance tags after separate operator review and approval. Publication is for remote governance traceability and creates no predictive, profitability, runtime, or trading authority.

## Recommended Push Package

Recommend `PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN` for operator review without selecting it. It contains only the four terminal expectancy-lab archive tag refs.

## Candidate Push Packages

Provide four unselected choices: publish the four terminal tags, keep them local, delay until merge-strategy review, or require a backup/bundle before publication. Every package remains unapproved, unexecuted, and not pushed.

## Candidate Push Records

For each tag bind its name, annotated tag-object SHA, peeled target commit, source artifact and digest, candidate remote ref, source-review verification, and remote absence. Keep selection, approval, push, predictive acceptance, profitability acceptance, runtime authority, and recommendation generation false.

## Remote Publication Plan

Store a planned command template that names all four `refs/tags/...` refspecs explicitly. Do not execute it. Mark it `PLANNED_NOT_EXECUTED` and `NOT_PUSHED`; require a separate approval and execution task.

## Tag Push Prerequisites

Require operator review and approval, a clean tree, protected `origin/main`, local tag reverification, absent-or-matching remote refs, mismatch blocking, explicit refspecs, and a separate post-push results review. Forbid all-tags, main, branch, and force pushes.

## Tag Push Non-Goals

Do not push/create/modify/delete tags, push main or branches, force-push, delete remote tags, merge, delete branches, clean up, or imply predictive/profitability/runtime/trading authority.

## Next Chain and Gates

Proceed through operator review, conditional approval, conditional execution, and results review. Merge-strategy planning follows only a tag-push or explicit local-only decision. Cleanup planning and any protected main action remain separate later gates.

## Risk Controls

Validate the full evidence chain and 63 candidate checks. Fail closed on changed source digests or main commit; missing packages, records, template, controls, or digest; any execution/publication/mutation flag; provider/data/model activity; or opened predictive, profitability, runtime, or broker authority.

## Non-goals and Guardrails

Do not inspect `.env`, call providers, acquire market data, regenerate datasets, rerun source workflows, recompute metrics, train models, score strategy, generate recommendations, modify broker code, or track `.marketflow` output. Default tests remain deterministic, offline, and isolated.

## Next Task

`MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_OPERATOR_REVIEW_V1`.
