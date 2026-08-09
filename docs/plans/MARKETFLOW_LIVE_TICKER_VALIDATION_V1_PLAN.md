# MarketFlow Live Ticker Validation v1 Plan

## Purpose
- Define an offline, digest-bound candidate/request package for future live ticker validation of the approved expanded ticker universe.
- Preserve the approval boundary: ticker universe selection is approved only for future validation and authority-chain planning.
- This plan does not authorize provider requests, perform live ticker validation, create ticker authority, authorize acquisition, generate datasets, execute predictive evidence, or activate runtime behavior.

## Source Ticker Universe Approval
- Source approval artifact kind: `TICKER_UNIVERSE_SELECTION_APPROVED`
- Source approval status: `TICKER_UNIVERSE_SELECTION_APPROVED`
- Source approval digest: `e0b56da411ada20f40fbefdcf74c1cce75ca86d13931471f518ef970db23188c`
- Source approval scope: `TICKER_UNIVERSE_APPROVED_FOR_FUTURE_VALIDATION_AND_AUTHORITY_CHAIN_PLANNING_ONLY`
- Source ticker universe selection candidate digest: `6baeb13550814f8c0d3d0a815a797e2f7b46552fa2fa5aa3aa950a7f6d5fce01`
- Source ticker universe selection candidate review package digest: `df63f64a3b145740a650ecf7db703356f3ee24e0dbdfdc4ac27a1812b75dcf4a`

## Validation Target Universe
- Candidate artifact kind: `LIVE_TICKER_VALIDATION_CANDIDATE`
- Candidate status: `LIVE_TICKER_VALIDATION_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `7d4bd0b944cce2fd6be6e242683befba3ea432ddfec079eeac129722942587e7`
- Candidate operator review package artifact kind: `LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE`
- Candidate operator review package status: `LIVE_TICKER_VALIDATION_CANDIDATE_REVIEW_PACKAGE_READY`
- Candidate operator review package digest: `c38b723df9a66e94ff82696cf8c88aa5008e915e7fc42b2a8a760ea61623b3fc`
- Candidate operator review package decision: `None`
- Candidate operator review package remains ready for operator assessment only.
- Approved expanded ticker count: `12`
- Validation target count: `12`
- Validation targets: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`
- Target status: `APPROVED_FOR_FUTURE_VALIDATION_ONLY`
- Provider request status: `NOT_REQUESTED`
- Live validation status: `NOT_PERFORMED`
- Listing, security type, exchange, active, delisting, tradability, corporate-action data availability, and historical aggregate data availability statuses remain `NOT_VERIFIED`.

## Planned Validation Checks
- `ticker_symbol_recognized_by_provider`
- `security_type_check`
- `primary_exchange_check`
- `listing_active_status_check`
- `delisting_or_inactive_status_check`
- `historical_data_availability_check`
- `corporate_action_endpoint_availability_check`
- `split_data_availability_check`
- `dividend_data_availability_check`
- `data_range_coverage_feasibility_check`
- `provider_symbol_mapping_consistency_check`
- Each check requires future provider interaction, was not performed in this task, and requires operator approval before execution.

## Provider Request Policy
- future_provider_request_policy_status: `PLANNED_REQUIRES_SEPARATE_APPROVAL`
- allowed_future_request_type: `READ_ONLY_VALIDATION_REQUESTS_ONLY`
- sanitized_status_doc_required: `True`
- rate_limit_policy: `RESPECT_PROVIDER_LIMITS_AND_FAIL_CLOSED`
- provider_result_authority: `VALIDATION_RESULTS_ONLY_NOT_ACQUISITION_AUTHORITY`

## No API Key Storage Policy
- api_key_handling: `DO_NOT_STORE_KEYS_OR_PRINT_KEYS`
- The candidate records no secrets, API keys, tokens, request headers, or environment values.
- Future validation approval must confirm key handling before any live provider transport is enabled.

## Raw Payload Non-Commit Policy
- raw_payload_policy: `DO_NOT_COMMIT_RAW_PROVIDER_PAYLOADS`
- Future live validation results must use sanitized status artifacts.
- Raw provider payloads must not become tracked source files.

## Non-Goals
- No provider request authorization.
- No provider requests made during candidate operator review.
- No live provider transport.
- No live ticker validation execution.
- No live ticker validation approval artifact.
- No live validation results artifact.
- No current listing status, security type, exchange, active, delisting, tradability, corporate-action, or aggregate availability verification.
- No new ticker authority.
- No acquisition authorization.
- No dataset generation authorization.
- No additional predictive evidence execution.
- No predictive usefulness acceptance.
- No profitability acceptance.
- No runtime migration, runtime activation, paper trading, broker execution, or trade recommendations.

## Guardrails
- Default tests remain deterministic and offline.
- Provider requests remain `False`.
- Provider request authorization remains `False`.
- Live provider transport remains disabled.
- Approved tickers remain validation targets only until a separate operator approval ceremony authorizes validation execution.
- Validation results, when later authorized, must not imply acquisition authority, canonical dataset authority, registry authority, predictive usefulness acceptance, profitability acceptance, or runtime activation.
- Runtime, strategy, paper trading, broker execution, and automatic stitching remain unauthorized.

## Next Tasks
1. Operator assessment of the live ticker validation candidate review package.
2. Live ticker validation approval ceremony.
3. Live ticker validation execution only after separate approval.
4. Sanitized live ticker validation results review.
5. Per-ticker identity/corporate-action/acquisition authority chain only after validation.
