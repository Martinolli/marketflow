# MarketFlow Repository Integration Branch Execution v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED`.
- Successful status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTED_VALIDATION_COMPLETED`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_EXECUTION_ONLY_NOT_MAIN_MERGE_NOT_CLEANUP_NOT_RUNTIME`.
- Selected package: `PACKAGE_CREATE_INTEGRATION_BRANCH_FOR_FULL_STACK_VALIDATION`.

The execution service performs only the approved local integration-branch
validation. It uses an isolated temporary worktree so the execution feature
worktree is not switched or modified. The temporary worktree is removed after
validation while the exact local integration branch is preserved for results
review.

## Source Approval

The source merge-strategy approval digest is
`34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.
It selected and authorized only the temporary integration-branch validation
package. The operator-review, candidate, tag-push, archive, readiness,
reassessment, backtest, metric, and records digest chain remains bound without
rerunning any source workflow.

## Approved Integration

The execution prechecks protected `origin/main` at
`eda58d9a56656641d4e0c2a80a6e572b6e949fc2`, the approved source commit
`71ed7fa63b27e1572fe7ccfd9b05f38b73a23416`, clean state, branch absence, and
the four published terminal tags.

The local branch is
`integration/marketflow-terminal-evidence-stack-validation-v1`. It is created
from `origin/main` and uses a deterministic `NO_FF_MERGE_COMMIT` for the exact
approved source commit. The service runs the repository virtualenv's complete
pytest suite in the isolated integration worktree and records the actual
branch head, merge commit, merge bases, bounded diff, test totals, duration,
execution digest, and validation digest in the returned artifact.

The integration branch remains local and is not pushed. `origin/main` remains
unchanged. No merge to main, main push, rebase, squash, cherry-pick, branch
deletion, force push, remote prune, tag mutation, or additional tag push is
performed.

## Authority Boundary

No provider, market-data, dataset, metric, model, scoring, recommendation,
runtime, broker, or trading action is authorized or performed. Predictive
usefulness and profitability remain not accepted; runtime and trading remain
`NOT_AUTHORIZED`.

## Failed Execution Follow-On

Repository Integration Branch Execution Failure Diagnosis v1 is implemented as
a diagnosis-only follow-on. Execution remains blocked because the authoritative
first integration pytest run reported `24481 passed, 1300 failed, 500 errors,
7 skipped`.

The later `26842 passed, 7 skipped` feature-worktree diagnostic does not override
the failed gate and is not integration acceptance evidence. Results Review is
not ready. A separate remediation candidate is required before any approved
retry.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1`.
