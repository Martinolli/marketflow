# MarketFlow Research Applicability Campaign Execution Status

## Branch And Commit
- Branch: `feature/research-applicability-campaign-execution-v1`
- Base commit: `77a31596ce862ecf25c06beb6586be41171374d9`
- Implementation commit: the commit containing this document.

## Execution Artifact
- Artifact kind: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED`
- Execution status: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTED_RESEARCH_ONLY`
- Execution digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- Execution request ID: `AAPL_RESEARCH_APPLICABILITY_EXECUTION_2022_2025_V1`
- Execution timestamp UTC: `2026-08-09T07:12:42.109219Z`

## Outputs Generated Summary
- Output root path: `.marketflow/research_applicability_campaigns/AAPL/2022_2025`
- Planned output count: `12`
- Generated output count: `12`
- Research output label: `RESEARCH_ONLY_NON_ACTIONABLE`

## Output Digest Manifest
- `bar_count_consistency_report`: `04bba27d83b6705a0a7e76319d6533f0003bdf5a19d901de00c743cd59e2df95`
- `dataset_load_report`: `cd6b9fd19b9bf52d545a7e8b1b9fadea4a15b657ed885a9050e8ca4510bdebb7`
- `date_range_coverage_report`: `bb93b21959ded943e5ccc7155ce513791931bc38ddbeaf8093d8ac042b7d6bc8`
- `failure_reason_inventory`: `071280e457244d1854026240bbc78f369eff1a11ce0574deb2f48eba7bcbcb02`
- `indicator_calculation_report`: `886af84a4b87a9af3df6f97629323791996bfe910296097853eaeb87cf63346b`
- `module_compatibility_matrix`: `310b0b7de6861d18016dc5cc2b2facf6902004bd7e54cb3f62bb9d37037f5fee`
- `null_field_summary_report`: `ed069480f4339a1846bdcf5439e312c726533b9018052e0909d7cfb62edcb862`
- `ohlc_consistency_report`: `466bef5b3e0d952a99c918cf92bda3494104b11bf449c59a007fbaedba297e1e`
- `operator_review_summary`: `741aab4deff66e0bb7b450dc0da5d6296ee9babf2cd20be41d35586082fc33bf`
- `research_campaign_run_manifest`: `22fb30fe786a8ce99b2bcb1ba662822d84dcb1ddcabdb3b1bf492662f4690a30`
- `schema_validation_report`: `7f86c9195b637bf6043986c4f4fe010f3dee895e249acfd9f718899a4d3f355e`
- `volume_consistency_report`: `640f4438b875a9efcb93705314afb59cee5502c9693ae91a6c63bb6bd4f80f4a`

## Dataset Load Summary
- Dataset count: `2`
- Datasets loaded count: `2`
- Dataset digests verified count: `2`
- SWING row count: `1988`
- POSITION_SWING row count: `994`

## Schema Bar Date Null OHLC Volume Indicator Module Summaries
- Schema validation status: `PASS`
- Bar count consistency status: `PASS`
- Date range coverage status: `PASS`
- Null field summary report: generated under the ignored output root.
- OHLC consistency status: `PASS`
- Volume consistency status: `PASS`
- Indicator calculation status: `PASS`
- Module compatibility status: `RESEARCH_ONLY_COMPATIBILITY_LISTED`

## Failure Warning Count
- Failure count: `0`
- Warning count: `0`

## Runtime Boundary
- provider_requests_made: `False`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`

## Predictive Profitability Boundary
- predictive_usefulness: `not accepted`
- profitability: `not accepted`
- No predictive-usefulness acceptance was created.
- No profitability acceptance was created.

## Follow-On Results Review
- Follow-on execution results review implemented: `True`
- Follow-on review artifact kind: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE`
- Follow-on review status: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY`
- Execution artifact remains source evidence for results review.
- The results review does not accept predictive usefulness, profitability, or runtime activation.

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.
- No default runtime dataset source was changed.
- No Strategy runtime behavior was modified.
- No broker or paper trading action was performed.
- No trade recommendations were produced.
- No runtime migration or runtime activation was approved.

## Next Task
- Predictive usefulness review candidate.
