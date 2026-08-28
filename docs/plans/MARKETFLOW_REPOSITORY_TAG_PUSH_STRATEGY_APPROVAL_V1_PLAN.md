# MarketFlow Repository Tag Push Strategy Approval v1 Plan

## Purpose

Create an offline, deterministic, attestation-bound approval selecting the reviewed terminal expectancy-lab tag package for future explicit-refspec publication. Approval authorizes only a separately invoked execution task and performs no tag push.

## Source Tag Push Operator Review

Bind the committed review at `1f543e7067744d351a67bbab034abb643fa4c508`, review digest `2e97941cf486272f9cb12889f929ff51a69fe515ee73b90f6f4d76cba7039788`, candidate digest `7153f9c97c651fe817046d27a527d30ca2b8280c3d1555ff292a2b83416ac227`, and the complete upstream evidence chain. Do not rerun source workflows or inspect tags.

## Operator Attestation

Require the exact decision, package, attestation phrase, source digests, `origin/main`, approved refs/object SHAs/targets/count, approval-only scope, and all no-execution/no-authority confirmations. Require a non-empty non-secret reference and timestamp. Reject every incomplete or mismatched attestation; never request or store API keys or personal/broker information.

## Repository Context and Approval Scope

Preserve `origin/main` and the bound/pre-review/post-review ref contexts of 564/566/568, with 32 local tags, four candidate-namespace tags, and zero approved remote tags.

Use `REPOSITORY_TAG_PUSH_STRATEGY_APPROVAL_ONLY_NOT_PUSH_NOT_MERGE_NOT_DELETE_NOT_MAIN`. Selection and future-execution authorization are allowed; execution and publication remain false.

## Selected Package and Approved Records

Select only `PACKAGE_PUSH_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS_TO_ORIGIN`. Approve the four reviewed annotated tag records, their exact object SHAs, targets, and remote refs for future execution only. Each record requires separate execution and an explicit refspec.

## Approved Future Push Command

Approve the four-explicit-refspec command template without running it. Mark it `APPROVED_FOR_FUTURE_EXECUTION_ONLY`, `command_executed: false`, and `APPROVED_NOT_PUSHED`.

## Supporting Packages

Carry the local-only, delayed-publication, and backup/bundle packages as `AVAILABLE_NOT_SELECTED` with no selection, approval, authorization, execution, or push.

## Next Chain and Gates

The next task is a separately invoked tag-push execution, followed by results review. Merge strategy follows only after publication results or an explicit local-only decision. Cleanup and protected main actions remain independent later gates.

## Risk Controls

Validate 62 exact attestation, evidence, selection, record, closed-execution, and authority checks. Approval must not push/create/modify/delete tags, push branches/main/all tags, merge/rebase/delete/prune, call providers, regenerate data, rerun evidence, recompute metrics, train/score, recommend trades, or authorize predictive/profitability/runtime/broker use.

## Non-goals and Guardrails

Do not inspect `.env`, use live transport, modify `.marketflow`, touch broker code, or infer any authority beyond the four future tag pushes. Default tests remain deterministic, offline, isolated, and non-mutating.

## Next Task

`MARKETFLOW_REPOSITORY_TAG_PUSH_EXECUTION_V1`.
