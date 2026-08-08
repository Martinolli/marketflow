# MarketFlow Read-Only Registry Discovery Status

## Purpose
- Branch: `feature/read-only-registry-discovery-candidate-v1`
- Base commit: `93d0cdece58b0fe08807d86979158e6aa9c9d5a9`
- Implementation commit: the commit containing this document.
- Purpose: create an offline read-only discovery candidate for approved research registry datasets.
- This status document does not approve or activate runtime migration.

## Discovery Candidate
- Artifact kind: `READ_ONLY_REGISTRY_DISCOVERY_CANDIDATE`
- Candidate status: `READ_ONLY_REGISTRY_DISCOVERY_READY_FOR_OPERATOR_REVIEW`
- Schema version: `read_only_registry_discovery_candidate_v1`
- Candidate digest: `b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1`
- Created offline: `True`
- Provider requests made: `False`
- Read-only discovery: `True`
- Operator review required: `True`

## Runtime Review Evidence
- Runtime migration plan digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Runtime migration review package digest: `1d856db1e388e48948155739810baa5f140e2bec5318c80c3f4381d4d759d2e4`

## Registry Entries Discovered
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry scope: `RESEARCH_DATASET`
- SWING runtime use: `NOT_AUTHORIZED`
- SWING Strategy use: `NOT_AUTHORIZED`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry scope: `RESEARCH_DATASET`
- POSITION_SWING runtime use: `NOT_AUTHORIZED`
- POSITION_SWING Strategy use: `NOT_AUTHORIZED`
- Registry entry count: `2`

## Dataset File Availability Summary
- SWING dataset file status: `AVAILABLE_DIGEST_VERIFIED`
- SWING manifest file status: `AVAILABLE_DIGEST_VERIFIED`
- SWING dataset digest verified: `True`
- SWING manifest digest verified: `True`
- POSITION_SWING dataset file status: `AVAILABLE_DIGEST_VERIFIED`
- POSITION_SWING manifest file status: `AVAILABLE_DIGEST_VERIFIED`
- POSITION_SWING dataset digest verified: `True`
- POSITION_SWING manifest digest verified: `True`
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

## Checklist Summary
- Total checks: `21`
- Passed checks: `21`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Runtime migration authorized: `False`
- Software runtime activation authorized: `False`

## Authority Boundary
- No `RUNTIME_MIGRATION_APPROVED` artifact or status is created.
- No `RUNTIME_MIGRATION_ACTIVE` artifact or status is created.
- No `STRATEGY_RUNTIME_MIGRATION` artifact or status is created.
- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.
- This discovery candidate is evidence for operator assessment only.

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence was refreshed.
- No Strategy runtime behavior was modified.
- No runtime, Strategy, paper trading, or broker execution use was authorized.
- No predictive-usefulness or profitability acceptance occurred.

## Next Task Recommendation
- Read-only registry discovery operator review package.
