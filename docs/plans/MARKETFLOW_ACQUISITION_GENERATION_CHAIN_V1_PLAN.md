# MarketFlow Acquisition Generation Chain v1 Plan

## Purpose
- Plan an offline, digest-bound acquisition-generation chain for the corporate-action-authority-approved 12-ticker expanded universe.
- Create only a candidate for operator review; do not authorize or execute acquisition.
- Keep dataset, canonical-dataset, registry, predictive, profitability, runtime, and trading gates closed.

## Source Corporate-Action Authority Approval
- Artifact/scope: `CORPORATE_ACTION_AUTHORITY_APPROVED` / `CORPORATE_ACTION_AUTHORITY_ONLY`.
- Approval digest: `93524b9bdc4641de4c6eb1cc8343b848ceff316241c92edab57a2062b8640644`.
- Combined readiness digest: `ee425cb1ee8b9e513d3ed4bc5ddc05ca7498a3003bc5820c5a2b5014f799d621`.
- Split/dividend freeze digests: `37a06dceac17761319f9d5eb716d64dced765997b8d1e9d8a79166162bfdb303` / `98b7e740b750701eb1e63e6e0ad88ffd4d665c44ece2e0e85e0a15e4a2a4d6ae`.

## Target Universe
- `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Identity is frozen, split/dividend authority is frozen in separate event-only scopes, and corporate-action authority is approved in corporate-action-only scope.

## Acquisition Planning Dimensions
- Bind ticker identity and corporate-action authority.
- Plan provider and endpoint selection, historical price/volume acquisition, adjusted/unadjusted price handling, split/dividend adjustment policies, calendar/session/timeframe policy, data-quality validation, sanitized outputs, raw-payload policy, and digest manifests.

## Future Provider Request Policy
- Status: `PLANNED_REQUIRES_SEPARATE_APPROVAL`.
- Only future read-only historical market-data acquisition requests may be considered.
- Never store or print API keys and never commit raw provider payloads.
- Require sanitized status documentation, respect provider limits, and fail closed.
- Provider results are acquisition evidence only and confer no dataset authority.

## Future Acquisition Chain
1. Acquisition Generation Chain Candidate Operator Review Package v1.
2. Acquisition Provider Request Approval Ceremony v1, if required.
3. Acquisition Provider Evidence Execution v1.
4. Acquisition Results Review Package v1.
5. Acquisition Generation Approval Ceremony v1, if required.
6. Acquisition Generation Freeze Ceremony v1.
7. Canonical Dataset Chain Candidate v1.
8. Canonical Dataset Candidate Operator Review v1.
9. Canonical Dataset Freeze Ceremony v1.
10. Research Registry Approval Chain v1.

## Non-Goals
- No provider request, live transport, market-data acquisition, or acquisition output.
- No acquisition authorization, approval, execution, results artifact, or freeze.
- No dataset generation or canonical dataset candidate, authorization, or freeze.
- No registry approval.
- No predictive experiment, feature regeneration, strategy scoring, or trade recommendation.
- No predictive-usefulness or profitability acceptance.
- No runtime migration, runtime/strategy use, paper trading, broker execution, or automatic stitching.

## Guardrails
- `no_provider_refresh_without_authority`
- `no_raw_provider_payload_commit`
- `no_api_key_storage_or_printing`
- `no_acquisition_execution_without_operator_approval`
- `no_acquisition_freeze_without_results_review`
- `no_dataset_generation_without_acquisition_freeze`
- `no_canonical_dataset_without_dataset_candidate_review`
- `no_registry_approval_without_canonical_dataset_freeze`
- `no_runtime_source_switch`
- `no_automatic_stitching`
- `no_broker_execution`
- `no_paper_trading`
- `no_trade_recommendations`
- `no_predictive_usefulness_acceptance`
- `no_profitability_acceptance`
- `all_outputs_labeled_research_only`
- `operator_approval_required_before_any_acquisition_provider_request`

## Implementation Status
- Candidate artifact/status: `ACQUISITION_GENERATION_CHAIN_CANDIDATE` / `ACQUISITION_GENERATION_CHAIN_READY_FOR_OPERATOR_REVIEW`.
- Candidate digest: `e0fb0b3f2ccd4bdac3d8f24a6888e8a97d5013bcc33f1dee1d49ccd59204b4ff`.
- Checklist: `57 / 57` passing with zero blockers.
- Acquisition generation chain candidate is completed and remains source evidence.
- Candidate operator review package implemented as `ACQUISITION_GENERATION_CHAIN_CANDIDATE_REVIEW_PACKAGE_READY`.
- Review package digest: `4df1f99cc3902219a658cb2459353e73b3be12cba22365cfec35c2170a75af3d`.
- Acquisition provider request approval was required and is now completed as a separate ceremony.
- Acquisition generation chain candidate review is completed.
- Acquisition provider evidence request approval ceremony implemented with scope `READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUEST_APPROVAL_ONLY`.
- Request approval digest: `a83acdf0c64fa8d430274350c59b547a23e7a58fb897cc33982ab0444ec0993c`.
- Acquisition provider evidence execution completed as `ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY`; execution digest `decc59a4a0ae91229ed527f9fcafd54e9d5af468d057d5200a67d2167939b02b` binds `12` successful sanitized responses and `7` ignored research-only outputs.
- Acquisition Evidence Results Review Package v1 is implemented as `ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY`; digest `57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415` binds the seven verified sanitized outputs.
- Acquisition execution and acquisition-generation approval/freeze remain future work.
- Canonical dataset and registry chains remain future work.
- Predictive usefulness and profitability remain not accepted.
- Runtime activation remains future and separate.
- Acquisition and every downstream gate remain closed.

## Next Tasks
1. Acquisition Evidence Results Operator Review and data-quality review if required.
2. Keep acquisition-generation authorization and freeze separate from evidence-results review.
3. Acquisition Generation Approval and Freeze ceremonies remain future, separate gates.
4. Canonical Dataset Chain Candidate v1.
5. Registry approval only after canonical dataset freeze.
6. Predictive usefulness/profitability acceptance and runtime activation remain future and separate.
