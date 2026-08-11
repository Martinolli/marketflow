# MarketFlow Split Provider Evidence Execution Status

## Branch And Commit
- Branch: `feature/split-provider-evidence-execution-live-run-v1`
- Base commit: `58e3b560f4cc2ef8f06c15464911787e3c091588`
- Implementation commit: the commit containing this document.

## Execution Artifact
- Artifact kind: `SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED`
- Execution status: `SPLIT_EVENT_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY`
- Execution digest: `823bfb52b1623b8b9eb88b197da9b9943dfc1e14cb1d280160ba2cbe26eec4c4`
- Evidence scope: `READ_ONLY_SPLIT_EVENT_EVIDENCE_REQUESTS_ONLY`
- Output label: `RESEARCH_ONLY_NON_ACTIONABLE`
- Created offline: `False`

## Source Evidence
- Split provider evidence request approval digest: `7c7e93149fe118985fc218852d79e86b31c9ee5bbd75ebacd1890a3862d573db`
- Split event authority candidate review package digest: `5f59edb21ab0e800aa714cfca41f3fe2b155f012ea7cc6c4c4c382146303c95a`
- Split event authority candidate digest: `7faaaaf19f0630f200c7decaafc2555ea23dab3bcfdffd17713487f33d5d8e0b`
- Dividend event authority candidate review package digest: `cf120d55beaa22f1fbd4f27d9a7a6539583e5cd67f3d0ffe5a186f318f27a104`
- Corporate-action authority plan approval digest: `bd02155f618bee231e4472049963343d57b7585920653b31aa5518e96ded0d2f`

## Endpoint And Mode
- Selected provider: `Massive.com`
- Selected endpoint: `/stocks/v1/splits`
- Selected endpoint stability: `CURRENT_STOCKS_V1_SPLITS`
- Selected endpoint mode: `LIVE_HTTP_TRANSPORT_READ_ONLY`

## Target Universe
- Target universe count: `12`
- Target universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Execution Summary
- Provider request count: `12`
- Successful provider response count: `12`
- Failed provider response count: `0`
- Split evidence collected count: `7`
- No-split events returned count: `5`
- Not-evaluated count: `12`
- Generated output root: `.marketflow/split_event_provider_evidence/expanded_universe_v1`
- Generated output count: `6`
- Failure count: `0`
- Warning count: `12`

## Per-Ticker Sanitized Split Evidence Summary
- `MSFT`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `1`, provider response digest `51a58a2997bc74d4034b9f5699ee57d6a793deea9c5fe87a1e2a54112a99ee3a`, sanitized evidence digest `04f20386080dc7403750ad188bec919c78c59ba6a0ed65aba1521955f91c66bb`
- `NVDA`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `4`, provider response digest `2c5fe06493288240d7eca3ab425d69712107fad4d7e46ae798c290726171df22`, sanitized evidence digest `e7b051463e2351aec77767d87b8d98076eeb0dddb3935b5740b25bf294ef39ca`
- `AMZN`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `1`, provider response digest `6775556b9e18ffd8bf758d9e2bd4287fe8cd474e55f801f872b41a038e1e897f`, sanitized evidence digest `1560ddd3bafc214f13162c8f76cac9a6d6e03762da6664d32d6d1a32a59a741b`
- `GOOGL`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `1`, provider response digest `3c980b62dae570de0cea73257e086e9b981af8c64bcec3507b6597c1c2f66d57`, sanitized evidence digest `fc5ef5d46011c208c867371382467c34159dcbe2a23653f70fecaf569dbb064a`
- `META`: `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`, events `0`, provider response digest `4489bef1e1b9360cc47e9f23eea7f44898643873b4d804f9a471f704e15ebe1e`, sanitized evidence digest `0ae6d3c54d33a4ceeaed46fa72fdf30e41839c31b6b56f99df9c5ed50bfcf23b`
- `TSLA`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `2`, provider response digest `17105772cb859ff365923760a73174072d19c4d6b2f372d84369386fa93379fc`, sanitized evidence digest `5ce04473295185c79de1445dd3ce4d49330b2ade47f7cb1510a672a86b442b58`
- `JPM`: `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`, events `0`, provider response digest `ac4c0dab47b04d8ef07e9d613fba9d1cad113bf7a6c6ef15042c6d48eb56e351`, sanitized evidence digest `a5db65b83ed0aa125829edb1760955a4b179a8ba2fc15572af6c0d67cab9eb1e`
- `XOM`: `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`, events `0`, provider response digest `88294c97bda6cfdc54ff5a20baaa94b79822ecfb403d7f16c8da73374c2b508b`, sanitized evidence digest `648f2aad85b79abeb8f7884569c9e7668c5e9ee83eba77711ec6b36ebaab5ea2`
- `JNJ`: `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`, events `0`, provider response digest `6dcb911d308bdc0a61fa3a3038589eb9a4c3760bf7e681e23ebf82bd3333b3cb`, sanitized evidence digest `d40e4214404dc8e8dd28215119e4187c4be6b22b9e0637e2894b145903860066`
- `WMT`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `1`, provider response digest `a697ba9ae5e4c458bf1c16d3d68de95ced67e63a59b8f5931711ea44f5b26d61`, sanitized evidence digest `cf1030920ba2c02ae620a477b57e28792620cb275a439b2e42f0de63fe3bfe33`
- `CAT`: `SPLIT_EVIDENCE_COLLECTED_READ_ONLY`, events `1`, provider response digest `913080d01b03652ad947b5bc1e52f6ef71a5ce7adafe2d5b64ec93743dc7a6a9`, sanitized evidence digest `e62dedc26991f1d0aa6892e7c0bf1dd9e58a01b40481a9684185609a65ea4936`
- `LMT`: `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`, events `0`, provider response digest `b40bbf15e5883b88fc0f101c321ebeb73f83e2bd7b5988e17640cc6e2566faf8`, sanitized evidence digest `4852cd96099c768d4b58a743aebb46e18b1653b11e9f9f7712c2e464b3b9b5e6`

## Output Digest Manifest Summary
- `operator_review_summary.json`: `f89f53463cb7e9c9ff71e1de04322226d018cbb6a66bcc3c3c4cf401327f0683`
- `split_event_absence_inventory.json`: `e318894295993ffda91f7d5af394c3a0566f9ce12567b8da007ea7b43a74e88f`
- `split_event_failure_reason_inventory.json`: `00f3d48bb60134a983f00ac54ac4086fe240bf010f79afb8a25b4005efdb4f8d`
- `split_event_results_sanitized.json`: `af6de085ee34347b1c8188041dbc92d32183cc5af3c760df064f6c93d2470569`
- `split_provider_evidence_run_manifest.json`: `3593c5aa1d0dd8d08a2f7f709de3d810610623b521684af536fca35c7cdb0847`
- `split_provider_request_receipts_sanitized.json`: `a03e63633075a8d72fdd1cf9b7cffa5ddf13c2ba996a0b2c8e31b8c0c8cbb0e6`

## No-Split Event Policy Summary
- No-split provider responses were recorded for `META`, `JPM`, `XOM`, `JNJ`, and `LMT`.
- A provider response with zero split rows is recorded as `NO_SPLIT_EVENTS_RETURNED_BY_PROVIDER`.
- A no-split response is read-only evidence for review; it is not split authority.
- Unsupported endpoint fields are recorded as `NOT_EVALUATED_BY_SELECTED_ENDPOINT`.

## API Key And Raw Payload Boundary
- raw_provider_payloads_committed: `False`
- api_keys_stored_or_printed: `False`
- API key values were not printed, stored, or written to generated artifacts.
- Raw provider payloads were not committed.
- Generated outputs are ignored runtime evidence under `.marketflow/...` and are not source files.

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
1. `SPLIT_EVENT_EVIDENCE_RESULTS_REVIEW_PACKAGE`
