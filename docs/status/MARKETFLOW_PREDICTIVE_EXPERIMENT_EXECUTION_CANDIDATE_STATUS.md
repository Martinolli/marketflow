# MarketFlow Predictive Experiment Execution Candidate Status

## Branch And Commit
- Branch: `feature/predictive-experiment-execution-candidate-v1`
- Base commit: `5b87c7495efb21414617243413a16296df9d88a8`
- Implementation commit: the commit containing this document.

## Execution Candidate Artifact
- Artifact kind: `PREDICTIVE_EXPERIMENT_EXECUTION_CANDIDATE`
- Candidate status: `PREDICTIVE_EXPERIMENT_EXECUTION_READY_FOR_OPERATOR_REVIEW`
- Schema version: `predictive_experiment_execution_candidate_v1`
- Execution candidate digest: `36d724706fe3ea43592eb4589ffae3370f15dd4393d3226fbf9c9155f02561da`
- Execution request ID: `AAPL_PREDICTIVE_EXPERIMENT_EXECUTION_2022_2025_V1`

## Bound Source Evidence
- Predictive experiment plan digest: `2d338822163dd25f262a32940153ff9842bb7e3213372ad09ce705bbfddede71`
- Predictive experiment plan review package digest: `e71197fb6838e2caa99d1cffa3c6bd8847d3170d6f842ea921e5345dac349180`
- Predictive usefulness review candidate digest: `e5724cc5eb106b2aa24c68e80bb24835b293fe50009a4eb01b21154553bc79b6`
- Predictive usefulness review candidate review package digest: `f124ee8e7e6b72f9d8f5f2a495bb0afa09ef02e4d8a6a03e795a04de4276efe2`
- Campaign execution results review package digest: `c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b`
- Campaign execution digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- Prior execution request ID: `AAPL_RESEARCH_APPLICABILITY_EXECUTION_2022_2025_V1`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- SWING dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- POSITION_SWING dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`

## Experiment Scope
- Scope: `RESEARCH_ONLY`
- Ticker universe: `AAPL`
- Dataset profiles: `SWING / RTH_HALF_SESSION_195M`, `POSITION_SWING / RTH_FULL_SESSION_1D`
- Date range: `2022-01-01` through `2025-12-31`
- Registry scope: `RESEARCH_DATASET`
- Execution mode: `OFFLINE_RESEARCH_EXPERIMENT`
- Runtime mode: `NOT_RUNTIME`
- Strategy mode: `NOT_STRATEGY_INPUT`
- Broker mode: `DISABLED`
- Paper trading mode: `DISABLED`

## Planned Inputs
- SWING: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- POSITION_SWING: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- Planned output root: `.marketflow/predictive_experiments/AAPL/2022_2025/`

## Labels And Features
- Labels: `SWING_NEXT_BAR_DIRECTION`, `SWING_NEXT_BAR_RETURN_BUCKET`, `POSITION_SWING_NEXT_SESSION_DIRECTION`, `POSITION_SWING_NEXT_SESSION_RETURN_BUCKET`
- Feature families: `price_return_features`, `range_volatility_features`, `volume_context_features`, `rolling_mean_features`, `rolling_zscore_features`, `bar_position_features`
- Label generation performed: `False`
- Feature matrix generation performed: `False`

## Walk-Forward And OOS
- Walk-forward method: `chronological_walk_forward`
- Training window: `planned`
- Validation window: `planned`
- Test window: `planned`
- No shuffle: `True`
- Time order preserved: `True`
- Final holdout period: `planned`
- No future leakage: `True`
- Walk-forward validation performed: `False`
- Out-of-sample evaluation performed: `False`

## Planned Outputs
- Output root: `.marketflow/predictive_experiments/AAPL/2022_2025/`
- All planned outputs remain `PLANNED_NOT_GENERATED`.
- All planned outputs are labeled `RESEARCH_ONLY_NON_ACTIONABLE`.
- Planned outputs include run manifest, label reports, feature reports, feature matrix manifest, walk-forward configuration, OOS split report, baseline comparison, signal-quality metrics, stability analysis, false-positive/false-negative report, leakage control report, and operator review summary.

## Execution Gates
- `predictive_experiment_execution_candidate_operator_review`
- `predictive_experiment_execution_approval`
- `dataset_digest_reverification`
- `label_definition_operator_acceptance`
- `leakage_control_review`
- `walk_forward_configuration_review`
- `no_broker_execution_confirmation`
- `no_paper_trading_confirmation`
- `no_runtime_default_change_confirmation`
- `output_labeling_research_only_confirmation`

## Risk Controls
- `no provider refresh`
- `no broker execution`
- `no paper trading`
- `no runtime source switch`
- `no automatic stitching`
- `no trade recommendations`
- `no predictive usefulness acceptance in experiment execution`
- `no profitability acceptance in experiment execution`
- `all outputs labeled research-only`
- `operator approval required before experiment execution`

## Predictive And Profitability Boundary
- predictive_usefulness: `not accepted`
- predictive_usefulness_acceptance_ready: `False`
- profitability: `not accepted`
- profitability_acceptance_ready: `False`

## Runtime Boundary
- runtime_migration_recommended: `False`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`

## Checklist Summary
- Total checks: `51`
- Passed checks: `51`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Experiment execution authorized: `False`
- Experiment execution performed: `False`
- Predictive usefulness accepted: `False`
- Profitability accepted: `False`
- Runtime migration authorized: `False`
- Software runtime activation authorized: `False`

## Next Task
- Predictive experiment execution candidate operator review package.
