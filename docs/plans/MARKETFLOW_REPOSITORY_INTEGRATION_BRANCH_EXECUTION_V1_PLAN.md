# MarketFlow Repository Integration Branch Execution v1 Plan

## Purpose

Execute the approved temporary integration-branch validation without merging
or pushing main and without creating cleanup, runtime, or trading authority.

## Source Merge-Strategy Approval

Bind approval digest
`34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`
and its complete upstream evidence chain. Do not rerun approval, review,
tag-push, inventory, evidence, metric, model, or strategy workflows.

## Repository Context

Protect `origin/main` at
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`. Require a clean feature
worktree, an existing approved source commit, absence of the integration
branch locally and remotely, and all four published terminal tags.

## Execution Scope

`REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME`

## Integration Branch Creation Method

Use an isolated temporary Git worktree to create
`integration/marketflow-terminal-evidence-stack-validation-v1` from the exact
protected `origin/main` commit. Remove only that temporary worktree after
validation and retain the local branch for results review.

## Integration Source and Merge

Integrate exact commit `71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`
from `feature/marketflow-repository-tag-push-results-review-v1` with a
deterministic no-FF merge commit. Verify the two parents and both merge bases.

## Full Pytest Validation

Run `env\Scripts\python.exe -m pytest -q` against the integration worktree.
Fail closed on merge conflict or test failure. Record actual pass/skip totals,
duration, output summary, branch head, merge commit, and bounded diff evidence.

## Origin/Main Protection

Verify `origin/main` before and after. Never merge or push main, push the
integration branch, rebase, squash, cherry-pick, delete branches, force-push,
prune, or mutate tags.

## Next Chain

Integration-branch results review precedes any conditional main-merge
approval. Main execution and cleanup remain separately approved later gates.

## Next Gates

Results review, conditional main approval and execution, cleanup candidate,
cleanup approval, and cleanup execution remain distinct.

## Risk Controls

Create only the approved local branch, integrate only the approved source,
run the complete suite, and preserve main, tags, terminal evidence, and the
META limitation. No provider, data, metric, model, scoring, recommendation,
runtime, broker, or trading action is allowed.

## Non-Goals

No integration-branch push, main merge/push, cleanup, predictive or
profitability acceptance, or runtime/trading authorization.

## Guardrails

Default tests remain deterministic and offline. `.marketflow` remains ignored
and untracked. Next task:
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RESULTS_REVIEW_V1`.
