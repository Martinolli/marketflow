# MarketFlow Repository Tagging / Release Strategy Candidate v1 Plan

## Purpose

Create an offline, deterministic, digest-bound candidate for future repository tagging and release governance. The artifact proposes options only; it creates no approval, tag, release, merge, cleanup, or main authority.

## Source Inventory Operator Review

Bind `MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1`, digest `c50b37ceb06597014056a739848da76b2da2923824ba48f85edea71a1e8fceb5`, at commit `65cf8f129cfd49300a983401757e32f3fdc43570`. Use its committed constants and complete 57-field evidence chain without rerunning the review or inventory.

## Repository Context

Preserve the frozen 290/261/551 snapshot, 290/262/552 post-plan-push state, and 291/263/554 operator-review observation. Protect `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`, the terminal evidence branches, and the inventory-plan source commit.

## Tagging Philosophy and Recommended Package

Use human-readable, governance-only tags to preserve terminal evidence milestones after separate operator review and approval. Recommend `PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS` for review because it is the narrowest candidate aligned with the archived-not-ready terminal path. Do not select it here.

## Candidate Tag Packages

- `PACKAGE_TERMINAL_EXPECTANCY_LAB_ARCHIVE_TAGS`: four exact terminal milestone candidates.
- `PACKAGE_GOVERNANCE_MILESTONE_TAGS`: seven governance milestone candidates.
- `PACKAGE_SOURCE_PROTECTION_TAGS`: three protected-source candidates.
- `PACKAGE_NO_TAGGING_ARCHIVE_ONLY`: skip tags and preserve branches.

Every package remains unselected, unapproved, unexecuted, and creates no tags.

## Candidate Tag Definitions

Define all 14 candidate tags as annotated-tag recommendations. Bind the four required terminal tags to their specified branches and commits. Bind source-protection tags to known protected commits. Leave governance targets explicitly unbound for later operator selection because the source contract does not authorize choosing their tips.

## Tagging Prerequisites and Message Template

Require operator review and approval, clean-tree and origin/main protections, explicit not-ready/no-runtime/no-trading message boundaries, and separate tag-creation and tag-push tasks. The future message template identifies artifact, status, decision, scope, digest, and all closed authority boundaries.

## Tagging Non-Goals

Do not tag, push tags, merge, delete, clean up, push main, modify origin/main, create a release package, or imply acceptance or runtime/trading authority in this candidate.

## Per-Chain Tagging Summary

Record planning-only recommendations for the expectancy-lab, VPA/Wyckoff, feature-label matrix, signal/feature, target generation, expectancy-objective, strategy-charter, prior improved-evidence archive, and miscellaneous feature chains. No chain requires merge or main push, and every chain remains behind operator review and approval.

## Next Chain and Gates

Proceed first to `MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1`. Any approval and execution remain separate tasks. Merge-strategy planning follows only after review or an explicit skip decision. Cleanup remains behind merge/tag settlement, separate approval, backup or bundle, and protected-branch confirmation.

## Risk Controls

Preserve all 30 candidate controls: no Git tagging/integration/destructive action, no `origin/main` or `.marketflow` modification, no provider/data/inventory/evidence/metric/model/scoring/recommendation action, closed predictive/profitability/runtime/broker authority, candidate-only tags, explicit review and approval gates, origin/main protection, terminal evidence preservation, and the META limitation.

## Non-Goals and Guardrails

This is not a release, tagging approval, tagging execution, merge strategy, cleanup plan, cleanup execution, or main deployment. Do not inspect `.env`, call providers, acquire data, regenerate datasets, rerun evidence, recompute metrics, train models, score strategies, create recommendations, or activate runtime or trading.

## Next Task

`MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_OPERATOR_REVIEW_V1`.
