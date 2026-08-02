# MarketFlow Massive Date Diagnostic 2025 Acceptance

## Decision

PASS.

Accepted classification:

```text
MASSIVE_DATE_DIAGNOSTIC_2025_ACCEPTED_OFFLINE_NOT_EXECUTED
```

UTC acceptance date: `2026-08-02T08:20:38Z`.

Branch: `diagnostic/swing-massive-2025-date-response`.

Base commit:

```text
db9446713f8fb3adb4160f7582a7a2163ff76074
```

Baseline tag:

```text
v0.1.0-alpha.21-massive-2026-date-diagnostic
```

No Git tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- fixed January-2025 Massive.com Custom Bars date-response diagnostic;
- exact same-code-path A/B comparison with the accepted January-2026
  diagnostic;
- offline 2025 plan command;
- mock-only 2025 self-check command;
- interactive-only 2025 live diagnostic command;
- digest-bound authorization ceremony;
- hidden `getpass` credential prompt after authorization;
- one-request live diagnostic boundary;
- strict provider-response parser reuse;
- sanitized structural diagnostic receipt;
- focused deterministic tests and final acceptance evidence.

Excluded scope:

- real provider request during acceptance;
- API-key inspection or credential-store access;
- provider account, portal, billing, browser, trade, or performance review;
- provider SDK change or dependency installation;
- canonical acquisition approval;
- `MonthChunkRequest` creation by the diagnostic;
- monthly executor invocation;
- month completeness manifest, normalized OHLCV, or registry artifact creation;
- Strategy, Monte Carlo, outcome, broker, execution, report rewrite, registry
  authority, or runtime migration.

## Fixed Diagnostic Specification

Schema:

```text
marketflow.massive_provider_date_diagnostic.v1
```

Fixed target:

- classification: `NONCANONICAL_PROVIDER_DATE_DIAGNOSTIC`;
- provider: `MASSIVE.COM`;
- endpoint: `STOCKS_CUSTOM_BARS_V2`;
- ticker: `AAPL`;
- month key: `2025-01`;
- effective start: `2025-01-01`;
- effective end: `2025-01-31`;
- multiplier: `15`;
- timespan: `minute`;
- adjusted: `true`;
- sort: `asc`;
- limit: `50000`;
- maximum provider pages: `1`;
- canonical eligibility: false;
- registry eligibility: false;
- acquisition-generation eligibility: false;
- Strategy enabled: false.

There is no caller, CLI, environment, config, provider, host, ticker, date,
month, limit, timeout, or semantic override for this diagnostic. There is no
current-date behavior and no range expansion.

Diagnostic digest:

```text
b90f5e8d681be1ca753f2fccd78ed778341aefb6d6c4fb89b1d657376a5e8e98
```

Required confirmation phrase:

```text
RUN MARKETFLOW MASSIVE DATE DIAGNOSTIC b90f5e8d681b
```

The digest is deterministic canonical JSON and excludes API key, current
timestamp, local path, run ID, provider response, raw URL, request ID, market
values, and console formatting.

## A/B Invariant

The January-2025 and January-2026 diagnostic specifications are identical
except for:

- `month_key`;
- `effective_start`;
- `effective_end`.

The accepted January-2026 diagnostic digest remains unchanged:

```text
588e61a824799f24feedfeaa9b4629ed2f623b5ff0490624089562ca0eb63376
```

Both diagnostics use the same plan builder, live runner, authorization
ceremony, interactive TTY check, `getpass` credential boundary, one-request
transport function, strict provider-response parser, structural sanitizer,
receipt model, and self-check machinery.

Constraint note: the diagnostic reuses the accepted Massive transport module's
provider identity, endpoint constants, credential wrapper, HTTP settings, and
failure taxonomy, plus the accepted strict `parse_provider_response` parser. It
does not instantiate `MassiveRestTransport` because that class is bound to
`MonthChunkRequest`, and this diagnostic is prohibited from creating a
`MonthChunkRequest`.

## Canonical And Monthly Boundary

Contract-v2 range remains:

```text
2022-01-01 through 2025-12-31
```

Contract-v2 digest:

```text
59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
```

Contract-v2.1 digest:

```text
538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

January 2025 lies inside the Contract-v2 calendar range, but this diagnostic
remains noncanonical. No Contract file changed. No `MonthChunkRequest` is
created, the monthly executor is not invoked, no completeness manifest is
written, no normalized artifact is produced, no calendar/bar derivation occurs,
no Strategy path is enabled, no registry eligibility is created, and no
acquisition-generation eligibility is created.

The existing controlled January-2025 smoke digest remains unchanged:

```text
2116c4dfa3e8ea759e5bca09cf0f4ccc329134f0cac1329ad871fb7746cdcfe4
```

## Plan And Self-Check

Plan command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-date-diagnostic-2025-plan
```

Result: `DATE_DIAGNOSTIC_PLAN_VALID`.

Confirmed: offline, no credential prompt, no network, no persistent write,
fixed January-2025 target, correct digest, noncanonical classification, and no
retry, pagination, normalization, monthly executor, registry, acquisition, or
Strategy behavior.

Self-check command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-date-diagnostic-2025-self-check
```

Result: `MASSIVE_DATE_DIAGNOSTIC_2025_SELF_CHECK`.

Confirmed: `httpx.MockTransport` only, fictional explicit key injection only,
shared execution path, valid schema status `DATE_DIAGNOSTIC_SCHEMA_ACCEPTED`,
rejected schema status `DATE_DIAGNOSTIC_SCHEMA_REJECTED`, request count `2`,
no external socket, no real provider call, no persistent artifact, and no key
leakage.

## Authorization And Credential Boundary

Live command:

```text
env\Scripts\python.exe -m marketflow.historical_data --massive-date-diagnostic-2025-run
```

Result in this noninteractive acceptance shell: rejected with
`DATE_DIAGNOSTIC_INVALID` and fixed finding
`DATE_DIAGNOSTIC_REQUIRES_INTERACTIVE_TTY`.

The live path requires an interactive TTY and the exact digest-bound
confirmation phrase before `getpass`. The API key has no CLI, environment,
config, URL, or ordinary visible-input path. Invalid keys fail before any HTTP
request. Keys are absent from receipts, diagnostics, errors, artifacts, URLs,
and public object representations.

This acceptance did not execute live mode and did not inspect an actual
credential.

## One-Request Boundary

The live diagnostic boundary performs at most one HTTP GET request after
interactive authorization and hidden credential entry. It does not retry,
sleep, follow pagination, normalize, persist a raw provider body, write
completeness manifests, invoke monthly acquisition, or call Strategy,
calendar/bar derivation, Monte Carlo, outcome, registry, broker, execution, or
runtime migration paths.

Continuation presence may be reported structurally as a boolean. Continuation
URLs, cursors, and follow-up requests are not followed or persisted.

## Sanitized Diagnostics

Receipts may contain only bounded structural data:

- schema/version;
- classification;
- diagnostic digest;
- ticker and fixed dates;
- HTTP status;
- response-body-complete status;
- parser status;
- whitelisted provider-status identifier;
- top-level and row field names;
- missing and unexpected field names;
- fixed JSON type categories;
- failing row index;
- query and result counts;
- results-present and continuation-present booleans;
- invocation and disabled-operation flags.

Receipts exclude API key, Authorization header, raw URL, raw `next_url`,
cursor, request ID value, raw response body, OHLCV/VWAP/transaction-count
values, raw exception text, absolute paths, provider account data, and account
state.

Unknown provider-status strings map to:

```text
PROVIDER_STATUS_UNACCEPTED
```

and are not echoed into public output.

## Verification

Python:

```text
Python 3.12.10
```

`pip check`: pass, `No broken requirements found.`

Focused diagnostic suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_date_diagnostic.py
```

Result: 28 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 860 tests collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 860 passed.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings only.

Test count explanation: accepted starting collection was 855 tests at the
January-2026 date-diagnostic baseline. Final collection is 860 because this
task adds 5 net focused diagnostic tests for the January-2025 fixed spec, A/B
invariance, digest preservation, sanitizer hardening, and 2025 CLI
plan/self-check/noninteractive-run behavior.

## Git Status Evidence

Pre-test status:

```text
## diagnostic/swing-massive-2025-date-response
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/massive_date_diagnostic.py
 M tests/test_massive_date_diagnostic.py
?? docs/status/MARKETFLOW_MASSIVE_DATE_DIAGNOSTIC_2025_STATUS.md
```

Post-test status before staging:

```text
## diagnostic/swing-massive-2025-date-response
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/massive_date_diagnostic.py
 M tests/test_massive_date_diagnostic.py
?? docs/status/MARKETFLOW_MASSIVE_DATE_DIAGNOSTIC_2025_STATUS.md
```

The acceptance evidence file is added by this acceptance task.

## Reviewer Findings

Reviewer A:

- No findings.
- Confirmed shared A/B implementation, fixed specifications, digest
  invariance, parser reuse, transport-module boundary reuse, and one-request,
  no-retry, no-pagination behavior.

Reviewer B:

- No findings.
- Confirmed TTY/getpass boundary, unknown provider-status sanitization to
  `PROVIDER_STATUS_UNACCEPTED`, canonical/monthly/runtime isolation, tests,
  docs, and prior-integrity preservation.

No critical, high, medium, or low finding remains.

## No-Network Evidence

No real DNS, external socket, provider request, API key, provider account,
billing, portal, browser, account, trade, credential-store path, or environment
credential value was used. Plan mode is receipt-only. Self-check uses
`httpx.MockTransport` with a fictional injected key. The live command was
tested only in a noninteractive shell and stopped before credential prompt or
request construction.

## Remaining Limitations

- Acceptance is offline and mock-only.
- No January-2025 live diagnostic has been executed.
- No actual API key was inspected.
- No market data was downloaded.
- January 2025 remains noncanonical.
- No acquisition is authorized.
- Runtime migration remains pending.
- Fixed start date, fixed end date, 4h bar-construction policy, session
  policy, adjustment/corporate-action provenance, and pagination/completeness
  acceptance remain blocking.
- Predictive usefulness and profitability remain unaccepted.
- No Strategy, Monte Carlo, outcome, performance, broker, execution, registry
  authority, report rewrite, or runtime migration is accepted.

## Next Manual Action

Run one January-2025 live diagnostic using the same accepted key in a separate
operator-authorized interactive terminal session, preserving the same
noncanonical, one-request, sanitized receipt, no-acquisition, no-normalization,
and no-runtime-migration boundaries.
