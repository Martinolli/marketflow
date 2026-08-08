# MarketFlow Runtime Migration Plan Status

## Purpose
- Branch: `feature/runtime-migration-planning-v1`
- Base commit: `7736d486d0bee974f7fa478ac9e03c1b80bea0f2`
- Implementation commit: the commit containing this document.
- Purpose: create an offline, digest-bound runtime migration planning candidate for future operator review.
- This status document does not approve or activate runtime migration.

## Plan Candidate
- Artifact kind: `RUNTIME_MIGRATION_PLAN_CANDIDATE`
- Plan status: `RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW`
- Schema version: `runtime_migration_plan_candidate_v1`
- Runtime migration plan candidate digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Created offline: `True`
- Provider requests made: `False`
- Operator review required: `True`
- Operator approval required before runtime use: `True`

## Research Registry Inputs
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- SWING registry scope: `RESEARCH_DATASET`
- SWING runtime use: `NOT_AUTHORIZED`
- SWING Strategy use: `NOT_AUTHORIZED`
- SWING dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- SWING dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- SWING bar count: `1988`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- POSITION_SWING registry scope: `RESEARCH_DATASET`
- POSITION_SWING runtime use: `NOT_AUTHORIZED`
- POSITION_SWING Strategy use: `NOT_AUTHORIZED`
- POSITION_SWING dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- POSITION_SWING dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- POSITION_SWING bar count: `994`

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

## Touchpoint Inventory Summary
- Inventory count: `10`
- Inventory complete: `False`
- High-risk touchpoints: CLI entry point, Studio UI, Strategy Ranking source discovery, live provider paths.
- Medium-risk touchpoints: artifact classification, walk-forward validation/campaign aggregation, run registry, operational artifact lineage.
- Recommended posture: read-only discovery and display only until a separate runtime migration approval ceremony exists.

## Checklist Summary
- Total checks: `24`
- Passed checks: `24`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Runtime migration authorized: `False`
- Software runtime activation authorized: `False`

## Authority Boundary
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition generation frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence was refreshed.
- No Strategy runtime behavior was modified.
- No runtime, Strategy, paper trading, or broker execution use was authorized.
- No predictive-usefulness or profitability acceptance occurred.

## Next Task Recommendation
- Runtime migration operator review package.
