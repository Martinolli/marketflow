# MarketFlow Runtime Migration v1 Plan

## Purpose
- Create an offline, digest-bound planning candidate for future runtime migration work.
- Preserve the read-only first principle: registry discovery and dataset availability checks must come before any runtime approval ceremony.
- Keep runtime use, Strategy use, paper trading, broker execution, predictive usefulness, and profitability outside this planning artifact.

## Prerequisite Research Registry Approvals
- SWING registry approved: `True`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- SWING registry scope: `RESEARCH_DATASET`
- POSITION_SWING registry approved: `True`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- POSITION_SWING registry scope: `RESEARCH_DATASET`

## Plan Candidate
- Artifact kind: `RUNTIME_MIGRATION_PLAN_CANDIDATE`
- Plan status: `RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW`
- Schema version: `runtime_migration_plan_candidate_v1`
- Plan digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Checklist result: `24` passed / `0` failed / `0` blockers.
- Runtime touchpoint inventory complete: `False`
- Runtime readiness established: `False`

## Read-Only First Principle
- migration_scope: `READ_ONLY_RESEARCH_DATASET_DISCOVERY`
- runtime_activation_scope: `NONE`
- strategy_input_replacement: `NOT_AUTHORIZED`
- default_dataset_switch: `NOT_AUTHORIZED`
- paper_trading_scope: `NOT_AUTHORIZED`
- broker_execution_scope: `NOT_AUTHORIZED`

## Planned Phases
1. Read-only registry discovery service.
2. Dataset manifest locator.
3. Dataset file availability verification.
4. Strategy/Studio read-only display integration.
5. Research-only applicability campaign runner.
6. Operator review of research campaign results.
7. Separate runtime migration approval ceremony, if ever authorized.

## Future Gates
- `read_only_registry_discovery_review`
- `dataset_file_availability_review`
- `research_campaign_plan_review`
- `applicability_campaign_completion`
- `predictive_usefulness_review`
- `profitability_review`
- `runtime_migration_operator_approval`

## Runtime Touchpoints
- `marketflow/__main__.py`: CLI entry point; high risk; do not change commands before read-only discovery review.
- `apps/marketflow_studio.py`: Studio UI; high risk; future integration must be display-only until runtime approval exists.
- `marketflow/services/strategy_service.py`: Strategy Ranking source discovery; high risk; do not silently replace current Strategy inputs.
- `marketflow/services/artifact_service.py`: generated artifact classification; medium risk; future display classification only after review.
- `marketflow/services/walk_forward_validation_service.py`: deterministic walk-forward cases; medium risk; research-only campaign candidate.
- `marketflow/services/walk_forward_campaign_service.py`: campaign aggregation; medium risk; can summarize applicability evidence later.
- `marketflow/services/walk_forward_run_registry_service.py`: saved run metadata; medium risk; not a dataset registry.
- `marketflow/marketflow_data_provider.py`: live provider access; high risk; no provider calls in migration planning.
- `marketflow/services/acquisition_provider_adapter_service.py`: live provider adapter; high risk; keep separated behind existing gates.
- `marketflow/operational_artifacts.py`: artifact lineage helpers; medium risk; may inform future migration evidence packaging.

## Hard Guardrails
- no runtime default change
- no automatic strategy input replacement
- no paper trading
- no broker execution
- no predictive claim
- no profitability claim
- no automatic stitching
- no silent fallback to non-authorized datasets

## Runtime Boundary
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not regenerate SWING or POSITION_SWING bars.
- Do not alter current operational behavior.
- Do not approve runtime migration.
- Do not activate runtime migration.
- Do not enable paper trading or broker execution.
- Do not claim predictive usefulness or profitability.

## Next Tasks
1. Runtime migration operator review package.
2. Read-only registry discovery candidate.
3. Dataset availability verification.
4. Research-only applicability campaign plan.
