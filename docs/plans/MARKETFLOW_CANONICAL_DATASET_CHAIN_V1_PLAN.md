# MarketFlow Canonical Dataset Chain v1 Plan

## Purpose
- Plan a deterministic canonical-dataset chain for the acquisition-generation-frozen 12-ticker expanded universe.
- Create only an offline operator-review candidate; do not authorize or generate a dataset.
- Preserve all registry, predictive, profitability, runtime, strategy, paper, and broker gates as closed.

## Source Acquisition Generation Freeze
- Source artifact/scope: `ACQUISITION_GENERATION_FROZEN` / `ACQUISITION_GENERATION_FREEZE_ONLY`.
- Freeze digest: `534d72f842a44162bf07d32bbd6c2defb4e0064deb148fb92e785a5514319bd5`.
- Acquisition generation is authorized, approved, and frozen only for future canonical-dataset-chain input; it remains unexecuted.

## Target Universe
- `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Preserve this exact order in every future candidate, manifest, dataset, and review.

## Source Profile
- Date range: `2022-01-01` through `2025-12-31`.
- Timeframe/profile: `1d` / `RTH_FULL_SESSION_1D`.
- Scope: `READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY`.
- Evidence covers 12 tickers and seven sanitized acquisition outputs.

## Canonical Dataset Planning Dimensions
- Bind acquisition freeze, corporate-action, identity, split, and dividend authority evidence.
- Define ordered ticker, daily OHLCV schema, timestamp/timezone, trading calendar, session filter, adjusted/unadjusted price, split/dividend adjustment, missing-gap, data-quality, deterministic sorting, column order, metadata, digest-manifest, sanitized-output, and raw-payload policies.
- Every dimension requires review before generation or authority can be considered.

## META Reduced Bar Count Preservation
- META remains exactly `913` historical bars while all other tickers remain exactly `1003`.
- No future chain step may repair, infer, smooth, normalize, backfill, or fabricate the difference.

## Future Canonical Dataset Chain
1. Canonical Dataset Chain Candidate Operator Review Package v1.
2. Canonical Dataset Approval Ceremony v1, if required.
3. Canonical Dataset Generation Execution v1.
4. Canonical Dataset Results Review Package v1.
5. Canonical Dataset Freeze Ceremony v1.
6. Research Registry Candidate v1.
7. Research Registry Operator Review and Approval Ceremony.
8. Additional predictive evidence and runtime migration only if separately authorized.

## Non-Goals
- No provider request, live transport, market-data acquisition, or acquisition rerun.
- No dataset generation authorization or execution.
- No canonical dataset candidate, generation, authorization, or freeze.
- No registry approval.
- No predictive experiment, feature regeneration, strategy scoring, recommendation, usefulness acceptance, or profitability acceptance.
- No runtime migration, source switch, automatic stitching, paper trading, or broker execution.

## Guardrails
- `no_dataset_generation_without_operator_approval`
- `no_canonical_dataset_freeze_without_results_review`
- `no_registry_approval_without_canonical_dataset_freeze`
- `no_raw_provider_payload_commit`
- `no_api_key_storage_or_printing`
- `preserve_meta_reduced_bar_count`
- `no_missing_bar_fabrication`
- `no_calendar_session_inference_without_review`
- `no_adjustment_policy_change_without_review`
- `no_predictive_label_use_without_registry_approval`
- `no_runtime_source_switch`
- `no_automatic_stitching`
- `no_broker_execution`
- `no_paper_trading`
- `no_trade_recommendations`
- `no_predictive_usefulness_acceptance`
- `no_profitability_acceptance`
- `all_outputs_labeled_research_only`

## Next Tasks
1. Canonical Dataset Approval Ceremony v1, if required by policy.
2. Canonical Dataset Generation Execution v1 under separate explicit authorization.
3. Canonical Dataset Results Review Package v1.
4. Canonical Dataset Freeze Ceremony v1.
5. Research Registry Candidate v1.

## Implementation Status
- Canonical Dataset Chain Candidate v1 is completed and remains source evidence.
- Canonical Dataset Chain Candidate Operator Review Package v1 is implemented and ready for operator assessment.
- Canonical dataset approval remains future work if required by policy.
- Canonical dataset generation, results review, freeze, and registry approval remain future work.
- Predictive usefulness and profitability remain not accepted.
- Runtime activation remains future and separate.
