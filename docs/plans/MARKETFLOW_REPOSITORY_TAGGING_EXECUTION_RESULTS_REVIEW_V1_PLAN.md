# MarketFlow Repository Tagging Execution Results Review v1 Plan

## Purpose

Create a deterministic, offline, digest-bound results review for the four local annotated tags created by Repository Tagging Execution v1. Verify local tag integrity and remote absence without creating, changing, deleting, approving publication of, or pushing tags.

## Source Tagging Execution

Bind the committed execution at `738941a3a8906f29528686fa35c76f76e1fa90ee`, execution digest `71a6853960c2d30ab53f5894fc2dd912dde8e75452cb942252d123e0bd5d5c40`, and tag-manifest digest `55674e0acd44977f2c700783cc6805f067fd96e1e200f001db075818b1729759`. Preserve the full upstream approval and research evidence chain without rerunning any builder.

## Repository Context and Review Scope

Preserve `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`, the source post-push branch inventory of 295/267/562, and the execution tag transition from 28/0 to 32/4.

Use `REPOSITORY_TAGGING_EXECUTION_RESULTS_REVIEW_ONLY_NOT_TAG_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN`. The review may inspect refs, tag objects, peeled targets, messages, tracked `.marketflow` paths, `origin/main`, and remote tag refs using read-only commands only.

## Local Tag Review Method

Support deterministic `git_snapshot` input for default tests. When no snapshot is supplied, use only read-only argument-list subprocess calls: `rev-parse`, `for-each-ref`, `cat-file`, `ls-files`, and `ls-remote`. Reject missing, extra, lightweight, target-mismatched, object-SHA-mismatched, message-mismatched, or remotely published approved tags. Do not repair any mismatch.

## Reviewed Local Annotated Tags

Review exactly final-archive-not-ready, archive-record-not-ready, operator-selection-option-a, and readiness-not-ready. Bind each expected target and tag object SHA from the source execution. Require all four to be annotated, present locally, message-verified, and absent remotely.

## Tag Count, Message, and Remote Publication Review

Record source and observed total/namespace counts, verified count, extra namespace count, and remote approved count. Explain unrelated total-tag drift if it occurs, while requiring exactly four namespace tags and no extra namespace entry.

Require every message to state the MarketFlow research governance milestone, `NOT_ACCEPTED` predictive usefulness and profitability, `NOT_AUTHORIZED` runtime and trading/broker use, and no trade recommendation. Remote publication remains unapproved; zero approved remote tags is required for review readiness.

## Next Chain and Gates

The next task is `MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_CANDIDATE_V1_IF_REMOTE_PUBLICATION_SELECTED`. Any push requires separate candidate, approval, and execution gates. Merge planning follows the tag-push or explicit local-only decision. Cleanup planning, approval, execution, and protected main push remain later independent gates.

## Risk Controls

Enforce all 35 controls: no tag creation/modification/deletion/push; no merge/rebase/delete/main/force/prune; no `origin/main` or `.marketflow` mutation; no provider/data/source rerun/metric/model/scoring/recommendation action; no predictive/profitability/runtime/broker authority; all reviewed tags local-only; separate push strategy; preserve terminal evidence and META limitation.

## Non-goals and Guardrails

Do not create a tag-push strategy candidate automatically. Do not approve or execute tag publication, merging, cleanup, main changes, provider access, data generation, metric recomputation, training, scoring, recommendations, or runtime/trading authority. Do not inspect `.env` or modify broker code.

Default tests remain deterministic and offline, write only under pytest temporary directories, and never mutate real tags or tracked files. Generated `.marketflow` and packaging artifacts remain untracked. MarketFlow remains research and decision-support software.
