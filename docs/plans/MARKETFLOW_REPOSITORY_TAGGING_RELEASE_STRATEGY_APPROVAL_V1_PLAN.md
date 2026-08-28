# MarketFlow Repository Tagging / Release Strategy Approval v1 Plan

## Purpose

Create a deterministic, offline, operator-attested approval for future creation of the terminal expectancy-lab archive tags. Keep selection and approval distinct from tag creation or any other repository mutation.

## Source Operator Review

Bind the committed operator-review artifact and digest `8fbb5367af9cc114e9d4de40781cad351b73aa2cfb7581bb2e1b33d9b736922b` without rerunning it or any earlier candidate, inventory, evidence, review, readiness, archive, or metric task.

## Operator Attestation

Require the exact non-secret approval phrase, exact operator decision, selected package, ordered terminal tag names and count, upstream digests, frozen `origin/main` commit, approval-only scope, and every closed-boundary confirmation. Refuse missing, changed, extra, or false attestation fields. Do not collect secrets, API keys, personal financial data, broker data, or raw provider payloads.

## Repository Context

Preserve the frozen 290/261/551 inventory and later 290/262/552, 291/263/554, 292/264/556, and 293/265/558 observations. Bind `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`, source candidate commit `2fa1f512be659546d88a9c9604cac8c41f255941`, source operator-review commit `deb8ad3e84c73e94880816e646bd2ee28f5b3769`, 28 existing tags, and zero candidate-namespace tags.

## Approval Scope

Use `REPOSITORY_TAGGING_RELEASE_STRATEGY_APPROVAL_ONLY_NOT_TAGGING_NOT_MERGE_NOT_DELETE_NOT_MAIN`. Approval may authorize a future task but must not create or push tags or perform other Git mutations.

## Selected Tagging Package

Select `PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS` as `APPROVED_FOR_FUTURE_TAGGING_EXECUTION_ONLY`.

## Approved Terminal Tags

Approve exactly four annotated tags targeting the already-bound terminal commits:

- final archive not ready;
- archive record not ready;
- operator selection option A;
- readiness not ready.

Every approved tag remains `APPROVED_NOT_CREATED`, not pushed, and subject to a separate execution task.

## Supporting Packages and Unapproved Tags

Keep the governance-milestone, source-protection, and no-tagging archive-only packages available but not selected. Keep all seven governance tags and three source-protection tags unapproved and uncreated.

## Future Tag Message Template

Approve the existing future annotated-tag message template only. It must retain the not-accepted predictive-usefulness and profitability boundary, not-authorized runtime and trading boundary, and no-trade-recommendation statement. Concrete execution values remain to be bound later.

## Next Chain and Gates

The next task is `MARKETFLOW_REPOSITORY_TAGGING_EXECUTION_V1`, only if separately invoked. Merge-strategy planning follows execution or an explicit skip decision; branch-cleanup planning follows resolution of tag and merge strategy. Cleanup execution and any main push each require their own approval and protections.

## Risk Controls

Enforce the 31 declared controls covering no tag creation or push, no merge/rebase/delete/main/force/prune mutation, no provider/data/dataset/source rerun, no metric/model/scoring/recommendation action, and no predictive, profitability, runtime, or broker authority. Preserve terminal archive evidence and the recorded META limitation.

## Non-goals and Guardrails

Do not call providers, inspect `.env`, access credentials, acquire market data, regenerate datasets, recompute metrics, train models, score strategies, generate recommendations, alter broker code, or modify tracked/generated `.marketflow` data. Do not create tags, releases, merges, rebases, deletions, cleanup candidates, main pushes, force pushes, or remote prunes. MarketFlow remains research and decision-support software.

Default tests remain deterministic and offline, write only to pytest temporary directories, assert outcomes, and leave the working tree clean. Generated packaging and `.marketflow` artifacts stay untracked.
