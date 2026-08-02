# MarketFlow Massive Response Schema Compatibility Acceptance

## Decision

PASS.

Accepted classification:

```text
MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_ACCEPTED_OFFLINE
```

UTC acceptance date: `2026-08-02T01:00:25Z`.

Branch: `fix/swing-massive-response-schema-compatibility`.

Base commit:

```text
0f136db5b6377111fe227ad7edae223ada8e38ca
```

Base commit subject:

```text
fix: propagate smoke authentication failures
```

No Git tag was created. No push was performed. The configured remote was not
altered.

## Sanitized Real Observation

The operator-provided smoke evidence was:

- HTTP status: `200`;
- response body: complete;
- first-page failure: `SCHEMA_FAILURE`;
- accepted pages: `0`;
- raw accepted pages: `0`.

No provider response body, request URL, `next_url`, request ID value, API key,
credential, authorization header, or market value is included in this evidence.

## Root Defect

Three defects were confirmed:

- the strict top-level Massive.com Custom Bars response schema did not accept
  the real compatibility field `count`;
- aggregate rows did not have a strict documented field allowlist including
  optional `otc`;
- provider schema rejection was collapsed into generic
  `MONTH_ACQUISITION_INVALID` and `SMOKE_INVALID`.

The correction remains strict and fail closed.

## Top-Level Schema

Accepted top-level fields are exactly:

- `ticker`
- `adjusted`
- `queryCount`
- `request_id`
- `resultsCount`
- `status`
- `results`
- `next_url`
- `count`

`resultsCount` remains authoritative. Unknown top-level fields are rejected.

## Count Contract

`count` is optional compatibility metadata. When present it must be an exact
nonnegative integer, must not be bool, float, or string, and must equal both
`resultsCount` and `len(results)`.

Validated `count` is excluded from normalized OHLCV, Strategy, and the
canonical semantic market-data projection. Valid redundant `count` presence
alone does not create semantic retry variance.

## Aggregate Row Schema

Required aggregate-row fields:

- `t`
- `o`
- `h`
- `l`
- `c`
- `v`

Optional aggregate-row fields:

- `vw`
- `n`
- `otc`

`otc` is optional and must be an exact boolean. Integer, float, and string
coercion are rejected. `otc` is excluded from the analytical OHLCV artifact and
current Strategy semantics.

Unknown aggregate-row fields are rejected.

## Sanitized Diagnostics

Schema-failure diagnostics retain only bounded structural evidence:

- sorted non-sensitive top-level field names;
- sorted aggregate-row field-name sets;
- missing required field names;
- unexpected field names;
- fixed JSON type categories;
- row index for aggregate-row failures.

Diagnostic field names pass a bounded ASCII identifier policy before
persistence. Sensitive accepted field names `next_url` and `request_id` are not
persisted in diagnostics.

Diagnostics do not retain response values, OHLCV values, VWAP values,
transaction-count values, request ID values, `next_url` values, raw URLs, cursor
values, API keys, authorization headers, raw response bodies, or raw exception
text.

## Status Mapping

First-page HTTP-200 schema failure maps to:

```text
MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED
```

Fixed finding:

```text
RESPONSE_SCHEMA_INVALID
```

When no first page is accepted, pagination maps to:

```text
PAGINATION_NOT_STARTED
```

Smoke maps provider response-schema rejection to:

```text
SMOKE_PROVIDER_RESPONSE_REJECTED
```

It does not map to `SMOKE_INVALID`, `SMOKE_CREDENTIAL_REJECTED`, or
`SMOKE_TRANSPORT_FAILED`.

## Raw And Normalized Artifacts

For schema-invalid HTTP-200 responses:

- attempt count remains `1`;
- accepted page count remains `0`;
- raw accepted page count remains `0`;
- no retry delay is scheduled;
- no automatic retry occurs;
- no accepted `RAW_PROVIDER_PAGE` is written;
- no completeness manifest is written;
- no normalized OHLCV artifact is written;
- no normalized supplemental aggregate-audit artifact is written;
- no canonical or registry eligibility is created.

Credential-bearing continuations still fail before raw-page persistence.
Authentication and authorization failures with response bodies do not persist
those bodies as raw pages.

## Non-Regression

Authentication mapping remains:

```text
HTTP 401 / AUTHENTICATION_FAILURE
MONTH_ACQUISITION_AUTHENTICATION_FAILED
SMOKE_CREDENTIAL_REJECTED
PAGINATION_NOT_STARTED
```

Authentication failure remains nonretryable and raw-page-free.

Retry and pagination behavior remains:

- 429 and 503 retry behavior unchanged;
- retry constants unchanged;
- successful one-page and multipage responses unchanged;
- actual accepted-page pagination defects retain `PAGINATION_CHAIN_INVALID`;
- repeated continuations and duplicate timestamps remain blocking;
- semantic response variance remains blocking;
- latest response never wins.

Previous source-assurance boundaries remain accepted: no default-test provider
network call, no environment credential read, no Strategy, Monte Carlo,
outcome, runtime migration, registry authority, report rewrite, broker, or
execution behavior was introduced.

## Verification

Python:

```text
Python 3.12.10
```

`pip check`: pass.

Focused Massive compatibility, transport, monthly acquisition, and smoke
regression group:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py
```

Result: 116 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 832 tests collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 832 passed.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings only.

Staged diff checks:

```text
git diff --cached --name-status
```

Result: seven intended files staged:

- `A docs/status/MARKETFLOW_MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_ACCEPTANCE.md`
- `A docs/status/MARKETFLOW_MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_CORRECTION.md`
- `M marketflow/historical_data/massive_smoke.py`
- `M marketflow/historical_data/monthly_acquisition.py`
- `M marketflow/historical_data/provider_response.py`
- `M tests/test_fake_transport_monthly_acquisition.py`
- `M tests/test_massive_one_month_smoke.py`

```text
git diff --cached --stat
```

Result before this evidence paragraph was added:
`7 files changed, 859 insertions(+), 20 deletions(-)`.

```text
git diff --cached --check
```

Result: pass.

Final staged-source rerun:

- focused Massive group: 116 passed;
- full default suite: 832 passed.

Test count explanation: accepted baseline at the committed authentication
propagation fix was 825 tests. This correction brings collection to 832 by
adding seven focused regressions covering `count`, `otc`, sanitized diagnostics,
schema-failure monthly/smoke propagation, and auth-body raw-page non-regression.

## Git Status Evidence

Pre-test status:

```text
## fix/swing-massive-response-schema-compatibility
 M marketflow/historical_data/massive_smoke.py
 M marketflow/historical_data/monthly_acquisition.py
 M marketflow/historical_data/provider_response.py
 M tests/test_fake_transport_monthly_acquisition.py
 M tests/test_massive_one_month_smoke.py
?? docs/status/MARKETFLOW_MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_CORRECTION.md
```

Post-test status before staging:

```text
## fix/swing-massive-response-schema-compatibility
 M marketflow/historical_data/massive_smoke.py
 M marketflow/historical_data/monthly_acquisition.py
 M marketflow/historical_data/provider_response.py
 M tests/test_fake_transport_monthly_acquisition.py
 M tests/test_massive_one_month_smoke.py
?? docs/status/MARKETFLOW_MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_CORRECTION.md
?? docs/status/MARKETFLOW_MASSIVE_RESPONSE_SCHEMA_COMPATIBILITY_ACCEPTANCE.md
```

## Reviewer Findings

Reviewer A:

- Medium: sanitized diagnostics could persist sensitive accepted field
  identifiers `next_url` and `request_id`. Disposition: fixed by omitting those
  identifiers from persisted structural diagnostics and adding regression
  coverage.
- Gap: schema-failure test did not explicitly assert absence of normalized
  artifacts. Disposition: fixed with explicit absence checks.

Reviewer B:

- Medium: scripted auth failures with response bodies could persist a raw page.
  Disposition: fixed by suppressing raw-page persistence for authentication and
  authorization response bodies, with focused regression coverage.
- Gap: schema-failure test did not explicitly assert no retry delay.
  Disposition: fixed with explicit retry-delay assertion.

No critical or high finding remains. No medium finding remains undisposed.

## No-Network Evidence

Default tests include socket-blocking coverage and source-assurance checks for
provider and Massive transport mock boundaries. Focused smoke tests use
`httpx.MockTransport`; monthly acquisition tests use deterministic scripted fake
transport.

No real DNS, external socket, provider request, API key, provider account,
billing, portal, browser, account, trade, or credential-store path was used.

## Remaining Limitations

- Acceptance is offline and mock/fake-transport only.
- No real Massive.com provider request was made.
- No actual API key was inspected.
- No provider account or billing state was accessed.
- No market data was downloaded.
- Acquisition remains disabled.
- Runtime migration remains pending.
- No Strategy, Monte Carlo, outcome, performance, broker, or execution
  capability is accepted by this correction.

## Future Live Smoke Procedure

A future live smoke remains a separate operator-authorized action:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m marketflow.historical_data --massive-smoke-plan
& $python -m marketflow.historical_data --massive-smoke-run
```

The operator must type the digest-bound phrase shown by the plan command. The
hidden API-key prompt appears only after that phrase is accepted. Any resulting
artifacts remain noncanonical smoke evidence and do not enable acquisition,
canonical registry approval, Strategy use, or runtime migration.
