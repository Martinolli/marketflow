# MarketFlow Repository State Branch Inventory Operator Review v1 Plan

## Purpose

Create an offline, deterministic, digest-bound operator review of the frozen repository inventory and integration plan. This artifact records review findings and a planning-only next candidate; it creates no approval or Git execution authority.

## Source Inventory Plan

The source is `MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_V1`, status `MARKETFLOW_REPOSITORY_STATE_BRANCH_INVENTORY_AND_INTEGRATION_PLAN_READY`, digest `e58cc279c1ec62fd2c24426ad71d35fc0edac41610769794bc71e5561add9896`. The implementation uses committed constants when no source plan is supplied and never reruns the branch inventory.

## Repository State and Inventory Count Review

Bind the source snapshot at `0be55dc8a65a586368c192d6bc13302b9830a0b4`, the source planning commit at `e49a4a3b14d2bb4fc721857cc1dfb42747e7b79e`, and `origin/main` at `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`. Review 290 local plus 261 remote refs in the frozen snapshot, and acknowledge the expected post-push count of 290 local plus 262 remote refs.

## Category Review

Protect main refs, retain terminal evidence, keep completed research chains for traceability, and leave signal/feature/target, other-feature, and remote-only dispositions for future operator decisions. Unknown categories fail closed.

## Terminal and Other Chain Reviews

Keep the expectancy-lab path terminal and archived-not-ready with no current next action. Review the VPA/Wyckoff, feature-label matrix, signal/feature generation, target generation, expectancy-objective design, strategy-charter, prior improved-evidence archive, IBKR/broker, and miscellaneous feature chains as planning-only. Do not evaluate merge readiness or authorize deletion.

## Integration Phase Review

- Phase 0: source inventory and freeze reviewed complete.
- Phase 1: operator inventory review completed by this artifact.
- Phase 2: tagging/release strategy candidate is ready as the next planning task but is not created here.
- Phases 3-5: merge planning, cleanup planning, and any separately approved cleanup execution remain future and not started.

## Policy Review and Recommended Next Task

Accept `INVENTORY_FIRST_NO_MERGE_NO_DELETE_NO_TAG` for planning. Recommend only `MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1`, with a separate operator review and any later approval kept as distinct gates.

## Protected Branches

Protect local `main`, `origin/main`, and the terminal expectancy-lab archive refs. No rename, squash, rebase, merge, delete, tag, prune, main push, or force-push is allowed by this review.

## Branches Requiring Operator Review

Signal/feature/target refs require a future disposition decision. Other-feature and remote-tracking-only refs require operator review before any cleanup. Any future cleanup also requires a separate candidate, approval, and backup or bundle confirmation.

## Risk Controls

Preserve all 29 review controls: no Git integration or destructive action, no `origin/main` or `.marketflow` modification, no provider/data/evidence/metric/model/scoring/recommendation action, closed predictive/profitability/runtime/broker authority, recommendation-only dispositions, explicit operator gates, terminal archive preservation, and preservation of the META limitation.

## Non-Goals and Guardrails

This task is not tagging/release planning itself, approval, merge planning, cleanup planning, cleanup execution, or main release work. It does not inspect `.env`, call providers, acquire data, rerun evidence, regenerate datasets, recompute metrics, train models, score strategies, create recommendations, accept predictive usefulness or profitability, or authorize runtime, paper trading, or broker execution.

## Next Task

`MARKETFLOW_REPOSITORY_TAGGING_RELEASE_STRATEGY_CANDIDATE_V1`.
