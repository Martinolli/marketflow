# MarketFlow Research Applicability Campaign v1 Plan

## Purpose
- Create an offline, digest-bound plan for a future research-only applicability campaign.
- Use only the research-registry-approved SWING and POSITION_SWING datasets for AAPL.
- Keep the campaign unexecuted until a later operator approval gate.
- Preserve runtime, Strategy, paper trading, broker execution, predictive-usefulness, and profitability boundaries.

## Prerequisite Research Dataset Approvals
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- SWING dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- SWING dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- POSITION_SWING dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- POSITION_SWING dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`

## Prerequisite File Availability Verification Review
- Dataset file availability verification package digest: `8ba7db3aa50eb858f7eebb10eb6ee1a554a97b43a789c93460ff276cadc96751`
- Dataset file availability verification review package digest: `1002c6f19bc57a6537dc71b8a830517de90fbfd89774797a3dd1e9232531ecff`
- Read-only discovery candidate digest: `b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1`
- Read-only discovery review package digest: `299eb78d52e598e690db501b10ea88390ff6848a217640022e56251c41584021`
- Runtime migration plan digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Runtime migration review package digest: `1d856db1e388e48948155739810baa5f140e2bec5318c80c3f4381d4d759d2e4`

## Plan Candidate
- Artifact kind: `RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE`
- Plan status: `RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_READY_FOR_OPERATOR_REVIEW`
- Schema version: `research_applicability_campaign_plan_candidate_v1`
- Plan digest: `b376bce431248be913dfe5c534535104a1663a5491a16560c9989681c323b97e`
- Created offline: `True`
- Campaign execution performed: `False`
- Campaign execution authorized: `False`
- Campaign plan completed: `True`

## Operator Review Package
- Artifact kind: `RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE`
- Review status: `RESEARCH_APPLICABILITY_CAMPAIGN_PLAN_CANDIDATE_REVIEW_PACKAGE_READY`
- Schema version: `research_applicability_campaign_plan_candidate_review_v1`
- Review package digest: `e908ef36dc38879ff59a72c2b7260497dfd2e75b1582806ece0b8852416ed01d`
- Operator review package implemented: `True`
- Campaign plan remains source evidence for review: `True`
- Campaign execution remains future work: `True`
- Runtime activation remains future work: `True`

## Campaign Scope
- Campaign name: `AAPL_SWING_POSITION_SWING_RESEARCH_APPLICABILITY_V1`
- Ticker universe: `AAPL`
- Dataset profiles: `SWING`, `POSITION_SWING`
- Date range: `2022-01-01` through `2025-12-31`
- Registry scope: `RESEARCH_DATASET`
- Runtime use: `NOT_AUTHORIZED`
- Strategy use: `NOT_AUTHORIZED`

## Campaign Questions
1. Can existing MarketFlow research modules load the research-registry datasets read-only?
2. Can SWING and POSITION_SWING datasets pass schema and continuity checks?
3. Can existing analysis modules compute non-trading descriptive indicators without runtime migration?
4. Can campaign outputs remain clearly marked research-only and non-actionable?
5. Which code paths require adaptation before any future runtime migration?

## Planned Metrics
- `dataset_load_success`
- `schema_validation_success`
- `bar_count_consistency`
- `date_range_coverage`
- `null_field_summary`
- `OHLC consistency checks`
- `volume consistency checks`
- `indicator_calculation_success`: `RESEARCH_ONLY_NOT_PERFORMANCE_ACCEPTANCE`
- `module_compatibility_matrix`
- `failure_reason_inventory`

## Planned Outputs
- `research_campaign_run_manifest`: planned only, not created.
- `dataset_load_report`: planned only, not created.
- `schema_validation_report`: planned only, not created.
- `compatibility_matrix`: planned only, not created.
- `failure_inventory`: planned only, not created.
- `operator_review_summary`: planned only, not created.

## Future Gates
- `research_campaign_plan_operator_review`
- `research_campaign_execution_approval`
- `read_only_execution_environment_confirmation`
- `no_broker_execution_confirmation`
- `no_paper_trading_confirmation`
- `no_runtime_default_change_confirmation`
- `output_labeling_research_only_confirmation`

## Risk Controls
- No provider refresh.
- No broker execution.
- No paper trading.
- No runtime source switch.
- No automatic stitching.
- No trade recommendations.
- No predictive/profitability acceptance.
- All outputs labeled research-only.
- Operator approval required before campaign execution.

## Non-Goals
- No campaign execution.
- No walk-forward validation run.
- No strategy scoring run.
- No provider request.
- No generated research campaign outputs.
- No runtime migration approval or activation.
- No predictive-usefulness or profitability acceptance.

## Next Tasks
1. Research-only applicability campaign execution candidate.
2. Research-only applicability campaign execution operator review.
3. Research-only applicability campaign execution, if approved.
4. Predictive usefulness review.
5. Profitability review.
6. Runtime migration approval ceremony, if ever authorized.
