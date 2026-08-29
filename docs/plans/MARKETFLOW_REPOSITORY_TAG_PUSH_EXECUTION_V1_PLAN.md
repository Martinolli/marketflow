# MarketFlow Repository Tag Push Execution v1 Plan

## Purpose

Publish only the four terminal expectancy-lab governance tags approved for
remote publication, and produce deterministic evidence of the exact remote
objects and peeled targets.

## Source Tag-Push Approval

The source is `MARKETFLOW_REPOSITORY_TAG_PUSH_STRATEGY_APPROVED`, commit
`523a75676e42b4c16bc00ef13b67b04cc8bcfbde`, digest
`1758d75de5839fb2299873d183b68cdcd6772286642822654ab0efe4cfd726c7`.
It selects `PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN`.

## Repository Context

The execution branch is stacked directly on the approval commit. The protected
baseline is `origin/main` at
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`. The source context records 299
local branches, 271 remote refs, 570 total refs, and 32 local tags.

## Execution Scope

`REPOSITORY_TAG_PUSH_EXECUTION_ONLY_EXPLICIT_REMOTE_TAG_REFS_NOT_MERGE_NOT_DELETE_NOT_MAIN`

## Approved Remote Tag Refs

- `refs/tags/marketflow/expectancy-lab/final-archive-not-ready/v1`
- `refs/tags/marketflow/expectancy-lab/archive-record-not-ready/v1`
- `refs/tags/marketflow/expectancy-lab/operator-selection-option-a/v1`
- `refs/tags/marketflow/expectancy-lab/readiness-not-ready/v1`

## Pre-Push Verification

For every tag, verify annotated object type, exact object SHA, exact peeled
target, and exact governance message. Verify the bound `origin/main` SHA. The
remote namespace must contain only absent approved refs or existing refs whose
object and peeled target match exactly. A mismatch or extra namespace ref
blocks the entire push.

## Explicit Push Command

```text
git push origin refs/tags/marketflow/expectancy-lab/final-archive-not-ready/v1 refs/tags/marketflow/expectancy-lab/archive-record-not-ready/v1 refs/tags/marketflow/expectancy-lab/operator-selection-option-a/v1 refs/tags/marketflow/expectancy-lab/readiness-not-ready/v1
```

## Remote Publication Verification

Read the namespace again after publication. Require four approved annotated
objects, four exact peeled commits, no extra namespace ref, and unchanged
`origin/main`. Existing exact tags are idempotent and are never overwritten.

## Next Chain

1. Repository Tag Push Results Review v1.
2. Repository Merge Strategy Candidate v1 only after that review or an explicit local-only decision.
3. Repository Branch Cleanup Candidate v1 only after merge/tag strategy is settled.
4. Cleanup only after separate approval, backup/bundle, and protected-branch confirmation.
5. Main push only if separately approved and protected.

## Next Gates

Results review, merge-strategy candidate, branch-cleanup candidate, cleanup
approval, cleanup execution, and any protected main push remain separate gates.

## Risk Controls

Use exactly four explicit refs. Never use all-tags, force, overwrite, delete,
merge, rebase, prune, or main publication. Preserve terminal evidence and the
META limitation. Keep provider, data, model, metric, recommendation, runtime,
broker, and trading paths closed.

## Non-Goals

This execution does not create or change local tags, publish branches during
tag publication, alter `origin/main`, rerun source evidence, or make any
predictive-usefulness or profitability acceptance decision.

## Guardrails

Default tests are offline and cannot access the real remote. `.marketflow`
outputs remain ignored and untracked. The next task is
`MARKETFLOW_REPOSITORY_TAG_PUSH_RESULTS_REVIEW_V1`.
