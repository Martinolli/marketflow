# MarketFlow Read-Only Registry Discovery v1 Plan

## Purpose
- Create a read-only discovery candidate for approved research registry datasets.
- Bind discovery to the completed runtime migration plan and operator review package evidence.
- Preserve current runtime defaults and Strategy inputs.
- Keep runtime migration, paper trading, broker execution, predictive usefulness, and profitability outside this artifact.

## Prerequisite Research Registry Approvals
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- SWING registry scope: `RESEARCH_DATASET`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- POSITION_SWING registry scope: `RESEARCH_DATASET`
- Runtime migration plan digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Runtime migration review package digest: `1d856db1e388e48948155739810baa5f140e2bec5318c80c3f4381d4d759d2e4`

## Read-Only Discovery Only
- Artifact kind: `READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE`
- Candidate status: `READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW`
- Schema version: `read_only_registry_discovery_candidate_v1`
- Candidate digest: `b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1`
- Registry entry count: `2`
- Discovery does not expose registry datasets as runtime defaults.

## Local Dataset And Manifest Availability
- SWING dataset path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- SWING dataset file status: `AVAILABLE_DIGEST_VERIFIED`
- SWING manifest path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json`
- SWING manifest file status: `AVAILABLE_DIGEST_VERIFIED`
- POSITION_SWING dataset path: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- POSITION_SWING dataset file status: `AVAILABLE_DIGEST_VERIFIED`
- POSITION_SWING manifest path: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json`
- POSITION_SWING manifest file status: `AVAILABLE_DIGEST_VERIFIED`
- Available dataset file count: `2`
- Available manifest file count: `2`
- Verified dataset digest count: `2`
- Verified manifest digest count: `2`
- Missing file count: `0`

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
1. Read-only registry discovery operator review package.
2. Dataset file availability verification.
3. Research-only applicability campaign plan.
