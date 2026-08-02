# MarketFlow Massive Smoke Auth Failure Propagation Correction

## Status

`CORRECTIVE_TASK_IMPLEMENTED_PENDING_LOCAL_ACCEPTANCE`

## Scope

- Correct truthful propagation of first-page HTTP 401 authentication failure
  from monthly acquisition to the controlled Massive.com one-month smoke receipt.
- Preserve Massive.com as the provider business identity.
- Preserve explicit legacy Polygon adapter/package naming where it describes
  installed code.
- Do not inspect credentials, account state, billing state, provider portal, or
  API-key values.
- Do not enable acquisition.
- Do not make a real provider request.
- Do not change or install the existing Polygon SDK.

## Root Defect

The low-level request attempt could correctly record a nonretryable
`AUTHENTICATION_FAILURE` with `http_status = 401`, but the monthly acquisition
status collapsed that first-page terminal condition into
`MONTH_ACQUISITION_INVALID`. The receipt builder also marked every incomplete
run as `PAGINATION_CHAIN_INVALID`, even when no provider page had been accepted
and pagination had not started.

## Corrected Mapping

- `failure_category = AUTHENTICATION_FAILURE` and `http_status = 401`:
  `MONTH_ACQUISITION_AUTHENTICATION_FAILED`.
- `MONTH_ACQUISITION_AUTHENTICATION_FAILED` plus `AUTHENTICATION_FAILURE`:
  `SMOKE_CREDENTIAL_REJECTED`.
- Zero accepted pages before a non-pagination terminal condition:
  `PAGINATION_NOT_STARTED`.
- Actual accepted-page pagination defects remain `PAGINATION_CHAIN_INVALID`.

## Expected First-Page 401 Receipt Semantics

- `smoke_status = SMOKE_CREDENTIAL_REJECTED`
- `request_status = MONTH_ACQUISITION_AUTHENTICATION_FAILED`
- `pagination_status = PAGINATION_NOT_STARTED`
- `completeness_status = INCOMPLETE`
- `fixed_findings = [AUTHENTICATION_FAILURE]`
- `attempt_count = 1`
- `accepted_page_count = 0`
- `raw_page_count = 0`
- `normalized_artifact_receipts = []`
- no retry delay
- no second request
- no raw provider page
- no normalized artifacts
- no raw body, raw URL, authorization header, bearer token, API key, or key-like
  query parameter in public receipts

## Regression Coverage

- Synthetic monthly first-page 401 authentication rejection.
- Synthetic smoke first-page 401 mapping and sanitization.
- Synthetic 429 and 503 retry behavior remains retryable.
- Existing one-page and multipage success assertions remain complete and
  pagination-valid.
- Existing accepted-page pagination failures remain invalid.
- All coverage is deterministic and offline.

## Blockers Preserved

- Fixed start date.
- Fixed end date.
- 4h bar-construction policy.
- Session policy.
- Adjustment/corporate-action provenance.
- Pagination and completeness acceptance.

## Provider Execution

No real Massive.com provider call was made for this corrective task. No
credential value was requested, inspected, stored, printed, or asserted.
