# MarketFlow Split Provider Evidence Execution Status

## Branch And Commit
- Branch: `feature/split-provider-evidence-execution-v1`
- Base commit: `8469a842c47bd2ab89dd7e217b1f14082ec19b97`
- Implementation commit: the commit containing this document.

## Execution Artifact
- Artifact kind: `SPLIT_EVENT_PROVIDER_EVIDENCE_BLOCKED`
- Execution status: `SPLIT_EVENT_PROVIDER_EVIDENCE_BLOCKED_LIVE_GATE_OR_API_KEY_MISSING`
- Execution digest: `NOT_CREATED`
- Evidence scope: `READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY`
- Output label: `RESEARCH_ONLY_NON_ACTIONABLE`

## Source Evidence
- Split provider evidence request approval digest: `7c7e93149fe118985fc218852d79e86b31c9ee5bbd75ebacd1890a3862d573db`

## Endpoint And Mode
- Selected provider: `Massive.com`
- Selected endpoint: `/stocks/v1/splits`
- Selected endpoint stability: `CURRENT_STOCKS_V1_SPLITS`
- Selected endpoint mode: `BLOCKED_NOT_ENABLED`

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Execution Summary
- Provider request count: `0`
- Successful provider response count: `0`
- Failed provider response count: `0`
- Split evidence collected count: `0`
- No-split events returned count: `0`
- Not-evaluated count: `0`
- Generated output root: `.marketflow/split_event_provider_evidence/expanded_universe_v1`
- Generated output count: `0`
- Failure count: `1`
- Warning count: `0`

## Per-Ticker Sanitized Split Evidence Summary
- No provider requests were made; no per-ticker provider evidence exists.

## Output Digest Manifest Summary
- No generated outputs were created because the live gate/API key requirement was not satisfied.

## No-Split Event Policy Summary
- A provider response with zero split rows is recorded as `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`.
- A no-split response is read-only evidence for review; it is not split authority.
- Unsupported endpoint fields are recorded as `NOT_EVALUATED_BY_SELECTED_ENDPOINT`.

## API Key And Raw Payload Boundary
- raw_provider_payloads_committed: `False`
- api_keys_stored_or_printed: `False`
- API key values are never printed, stored, or written to generated artifacts.
- Raw provider payloads are not committed.

## Authority Boundaries
- split_event_authority_created: `False`
- split_event_authority_frozen: `False`
- dividend_provider_evidence_request_authorized: `False`
- dividend_provider_evidence_executed: `False`
- dividend_event_authority_created: `False`
- dividend_event_authority_frozen: `False`
- corporate_action_authority_created: `False`
- new_ticker_acquisition_authorized: `False`
- dataset_generation_authorized: `False`
- acquisition_generation_authorized: `False`
- canonical_dataset_authorized: `False`
- registry_approval_created: `False`
- additional_predictive_evidence_execution_authorized: `False`
- additional_predictive_evidence_executed: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`

## Non-Goals
- No split authority approval or freeze is created.
- No dividend provider request or dividend authority is created.
- No corporate-action authority is created.
- No acquisition or dataset generation authorization is created.
- No predictive experiment rerun, strategy scoring, runtime activation, paper trading, broker execution, or trade recommendation is performed.

## Next Task
1. `ENVIRONMENT_OR_API_KEY_CORRECTION`
