# MarketFlow Repository State, Branch Inventory, and Integration Plan v1 Plan

## Purpose

Create a deterministic, offline, read-only repository snapshot and a conservative future integration strategy. This artifact inventories and classifies refs; it does not execute merge, cleanup, tagging, release, or main-branch work.

## Source Final Archive Summary

Bind `MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_EXPECTANCY_LAB_EVIDENCE`, its terminal archived-not-ready status and non-acceptance decision, digest `91320fd42e4dab0286c9250496278413ffd24a3f08669ea7a7344519942785ac`, and the complete 57-field upstream evidence chain without rerunning any source task.

## Repository State

Record the current branch and head, local `main`, `origin/main`, worktree cleanliness, and tracked `.marketflow` count. Bind the inventory base `0be55dc8a65a586368c192d6bc13302b9830a0b4` and protect `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.

## Branch Inventory

Collect local and remote refs with `git for-each-ref` and other explicitly allowed read-only commands. The point-in-time snapshot contains 290 local, 261 remote, and 551 total refs. Record identity, commit metadata, role flags, category, and a recommendation-only disposition for each ref.

## Branch Categories

Protect main and the terminal expectancy-lab archive branch. Keep named expectancy-lab, VPA/Wyckoff, matrix, signal/feature/target, strategy-charter, and prior improved-evidence archive chains for traceability. Treat other feature branches as possible future archive candidates only after operator confirmation. Treat remote-only and unknown branches conservatively and require review; unknown root-category branches must remain untouched.

## Terminal Chains

Summarize ten chains: the terminal expectancy-lab path; VPA/Wyckoff; feature-label matrix; signal/feature generation; objective label/target generation; expectancy-objective design; strategy charter; prior improved-evidence archive; IBKR/broker-related branches if present; and unknown/miscellaneous branches.

The current expectancy-lab path remains `TERMINAL_ARCHIVED_NOT_READY`, with no immediate next action. Merge readiness is not evaluated, deletion is not authorized, and archive readiness is planning-only.

## Integration Phases

1. Phase 0 — Inventory and Freeze: `COMPLETED_BY_THIS_ARTIFACT`.
2. Phase 1 — Operator Review of Inventory: `FUTURE_NOT_STARTED`.
3. Phase 2 — Tagging / Release Strategy Candidate: `FUTURE_NOT_STARTED`.
4. Phase 3 — Merge Strategy Candidate: `FUTURE_NOT_STARTED`.
5. Phase 4 — Branch Archive / Cleanup Candidate: `FUTURE_NOT_STARTED`.
6. Phase 5 — Execution of Approved Cleanup: `FUTURE_NOT_STARTED`.

## Recommended Policy

Use `INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG`. Keep main, deletion, and force-push protections enabled. The immediate next task is a separate operator review of this inventory.

## Protected Branches

Protect local `main`, `origin/main`, and both local and remote refs for `feature/marketflow-predictive-usefulness-final-archive-summary-expectancy-lab-evidence-v1`. Preserve every terminal evidence branch needed for traceability.

## Future Operator-Review Needs

The operator must review the 389 other-feature refs and six remote-tracking-only refs before any archive, merge, delete, or tag plan is proposed. No disposition in this artifact authorizes an action. IBKR/broker and unknown root-category branches, if later present, require explicit review and default to do-not-touch treatment.

## Non-Goals

Do not merge, squash, rebase, rename, delete, tag, prune, push main, force-push, modify `origin/main`, or execute a cleanup. Do not call providers, acquire data, rerun evidence, regenerate datasets, recompute metrics, train models, score strategies, generate recommendations, accept predictive usefulness or profitability, or authorize runtime or broker execution.

## Risk Controls

Maintain all 29 service-defined controls. They keep every integration disposition advisory, protect main and terminal evidence, require operator review before merge/delete/tagging, preserve META's 913-record limitation, and keep every data, predictive, profitability, runtime, and trading authority closed.

## Guardrails

Use subprocess only for the approved read-only Git command families. Default tests use deterministic snapshots or isolated mocked collection. Do not inspect `.env`, enable live transport, modify `.marketflow`, store or print credentials, or modify broker/IBKR code.

## Next Task

`MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_OPERATOR_REVIEW_V1`.
