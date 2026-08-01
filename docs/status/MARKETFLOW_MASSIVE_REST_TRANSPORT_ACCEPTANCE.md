# MarketFlow Massive REST Transport Acceptance

## Decision

MASSIVE REST TRANSPORT ADAPTER: PASS.

Accepted classification:

```text
MASSIVE_REST_TRANSPORT_ACCEPTED_OFFLINE_MOCK_ONLY
```

UTC acceptance date: `2026-08-01T19:28:55Z`.

Branch: `feature/swing-massive-rest-transport-adapter`.

Base commit: `bdcac256ea217e37785a5f8f7754d04e1aefc2aa`.

Baseline tag: `v0.1.0-alpha.18-fake-transport-monthly-acquisition`.

No Git tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- production-capable Massive.com REST transport module;
- fixed Custom Bars request construction;
- explicit bearer-header credential injection boundary;
- strict continuation URL validation and safe reconstruction;
- exact raw application byte return from mock HTTP responses;
- fixed HTTP status and transport exception mapping;
- monthly executor dependency-injection compatibility;
- mock-only CLI self-check;
- focused tests and source assurance;
- transport plan, status, architecture, security, and acceptance evidence.

Excluded scope:

- real Massive.com request;
- actual API-key inspection or use;
- provider account, billing, portal, browser, account, trade, or credential
  review;
- external network, DNS, socket, or provider SDK execution;
- data acquisition, canonical dataset creation, calendar freeze, registry
  authority, report rewrite, or runtime migration;
- Strategy candidate generation, Monte Carlo, outcome evaluation, performance
  analysis, broker integration, or execution capability.

## Dependency Result

`httpx==0.28.1` is source-declared in `requirements.txt` and consumed by
`setup.py` through `load_requirements()`.

The current environment satisfies the declaration. No dependency was installed,
upgraded, downgraded, renamed, or removed. The Massive module imports `httpx`
only and imports no Polygon or Massive SDK. No second HTTP dependency was
introduced.

## Provider And Endpoint

Provider business identity: `MASSIVE.COM`.

Fixed endpoint:

```text
https://api.massive.com/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}
```

The transport accepts only the Custom Bars endpoint family with multiplier
`15`, timespan `minute`, adjusted `true`, sort `asc`, and limit `50000`.
Arbitrary hosts, arbitrary base URLs, HTTP fallback, `api.polygon.io` fallback,
provider switching, and endpoint switching are rejected.

## Credential Boundary

Authentication uses only:

```text
Authorization: Bearer <secret>
```

Credentials are accepted only by explicit constructor injection through the
secret wrapper. The wrapper rejects empty keys, surrounding whitespace, control
characters, CR/LF, and header-injection characters. `repr` and `str` are
redacted, and focused tests use fictional credentials only.

The API key is not placed in URLs, query strings, continuation identities,
request digests, artifacts, receipts, public prepared-request headers, `repr`,
`str`, logs, exception output, assertion output, or saved raw request headers.

No environment variable value, config-file key, credential store, provider
portal, provider account, or billing data was inspected.

## Request Construction

Initial requests use:

- GET;
- HTTPS;
- host `api.massive.com`;
- strict ticker path validation;
- exact month request range;
- multiplier `15`;
- timespan `minute`;
- adjusted `true`;
- sort `asc`;
- limit `50000`;
- no extra query parameters.

Headers include:

- bearer `Authorization`;
- `Accept: application/json`;
- `Accept-Encoding: identity`;
- bounded non-private User-Agent.

Requests include no cookies, user/account identifier, or API-key query
parameter. Unsupported ticker/path characters and fixed-contract overrides fail
closed before an HTTP call.

## Continuation Validation

Raw `next_url` is treated as provider evidence, never as direct authority.

Validation requires HTTPS, exact Massive host, no userinfo, no unsupported port,
no fragment, exact endpoint family, ticker match, multiplier/timespan match,
month/range consistency, adjusted/sort/limit consistency, no credential-bearing
query, no user/account query, no unsupported query keys, and no duplicate query
keys.

The raw continuation URL is absent from public receipts and manifests. Opaque
cursor evidence is represented publicly through a nonreversible digest and
sanitized continuation identity. Reconstructed continuation requests use bearer
authentication again. Invalid continuation state fails before an HTTP call.

## HTTP Security

Fixed settings:

- connect timeout: 10 seconds;
- read timeout: 30 seconds;
- write timeout: 10 seconds;
- pool timeout: 10 seconds;
- TLS verification enabled;
- redirects disabled;
- `trust_env=false`;
- no cookie persistence;
- `Accept-Encoding: identity`;
- body limit: 67108864 bytes.

There is no CLI or environment override for host, timeout, TLS verification,
redirects, or body limit.

## Response Boundary

The transport returns exact application-level body bytes. It does not parse JSON
inside the transport, decode and re-encode, normalize newlines, reorder keys,
mutate body bytes, retry, sleep, traverse pagination, normalize aggregates, or
write acquisition artifacts.

Selected headers only are retained: `Content-Type`, `Content-Length`,
`Content-Encoding`, `Retry-After`, `X-Request-ID`, and `X-Correlation-ID`.

Response bytes are later committed and parsed by the accepted monthly executor
boundary.

## Content Type, Encoding, And Redirects

Successful responses require deterministic JSON media types. Missing
`Content-Type`, HTML, text/plain, XML, multipart, ambiguous duplicate
`Content-Type`, and unsupported nonidentity `Content-Encoding` fail closed.

Body at the exact limit succeeds. Body over the limit fails closed, including a
`Content-Length` pre-check before streaming.

Redirects are not followed. All 3xx responses are rejected and `Location`
targets are never followed.

## Status And Exception Mapping

Fixed sanitized mapping is covered for transport timeouts, connection reset, TLS
validation failure, malformed request, body-limit violation, unsupported content
type/encoding, HTTP 408, 429, 500, 502, 503, 504, authentication,
authorization, and redirect.

Raw exception strings are not persisted or printed. Retry-After text may be
exposed to the monthly executor, but the transport does not decide retry timing.

## Transport Responsibility

Each transport invocation performs exactly one HTTP round trip when request
validation succeeds.

The transport does not retry, sleep, follow pagination automatically, select
attempts, compare semantic responses, normalize aggregates, or write
acquisition artifacts.

The monthly executor remains the sole owner of retries, attempt evidence,
semantic equivalence, accepted-page selection, pagination chain, month
completeness, and normalization.

## Monthly Executor Integration

The same executor accepts `ScriptedFakeTransport` and `MassiveRestTransport`
through explicit dependency injection.

There is no mode inference from optional values, fake fallback, old Polygon
adapter fallback, Massive transport default in normal runtime, duplicate
monthly executor, or changed retry constants.

## Self-Check CLI

Command:

```text
python -m marketflow.historical_data --massive-transport-self-check
```

The self-check uses `httpx.MockTransport`, a fictional key, no real socket, no
provider request, exact bearer-header verification, no key in URL, exact
scripted body bytes, continuation reconstruction, sanitized receipt output, and
no persistent artifacts. It accepts no ticker, key, host, URL, timeout, or
provider mode.

## Contract Non-Regression

Reproduced digests:

```text
v1:   29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
v2:   59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
v2.1: 538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

No contract source was modified to make the adapter pass.

## Verification

Focused Massive transport suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py
```

Result: 65 passed.

Focused Massive transport and source-assurance suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py tests/test_source_assurance.py
```

Result: 86 passed.

Expanded historical-data, monthly executor, Contract regression,
source-assurance, packaging, and prior-integrity suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py tests/test_fake_transport_monthly_acquisition.py tests/test_historical_data_artifacts.py tests/test_historical_data_engine.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py
```

Result: 214 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 798 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 798 passed.

Final staged-source rerun:

- `env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py`:
  65 passed.
- `env\Scripts\python.exe -m pytest -q`: 798 passed.

Test count explanation: accepted starting collection was 733 tests from the
fake-transport monthly acquisition baseline. Final collection is 798 because
this task adds 65 focused Massive REST transport tests.

## Pip, Compile, Ruff, And Diff

`pip check`: pass, `No broken requirements found.`

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings only.

Ruff was not available as `python -m ruff` or as an `env\Scripts\ruff*` entry
point. Ruff was not installed, and Ruff absence is not represented as a passed
Ruff check. `AGENTS.md` does not make Ruff a mandatory release gate.

## Warnings

Git reports LF-to-CRLF working-copy normalization warnings on modified text
files. No project-owned warning was suppressed to make tests pass.

## Git Status Evidence

Pre-final-suite status:

```text
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/monthly_acquisition.py
 M marketflow/historical_data/provider_response.py
?? docs/architecture/MARKETFLOW_MASSIVE_REST_TRANSPORT.md
?? docs/plans/MARKETFLOW_MASSIVE_REST_TRANSPORT_PLAN.md
?? docs/security/
?? docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_STATUS.md
?? marketflow/historical_data/massive_transport.py
?? tests/test_massive_rest_transport.py
```

The final acceptance evidence file is added by this acceptance task.

Post-final-suite status before staging:

```text
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
 M marketflow/historical_data/monthly_acquisition.py
 M marketflow/historical_data/provider_response.py
?? docs/architecture/MARKETFLOW_MASSIVE_REST_TRANSPORT.md
?? docs/plans/MARKETFLOW_MASSIVE_REST_TRANSPORT_PLAN.md
?? docs/security/
?? docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_ACCEPTANCE.md
?? docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_STATUS.md
?? marketflow/historical_data/massive_transport.py
?? tests/test_massive_rest_transport.py
```

Pre-staged-source-rerun status:

```text
A  docs/architecture/MARKETFLOW_MASSIVE_REST_TRANSPORT.md
A  docs/plans/MARKETFLOW_MASSIVE_REST_TRANSPORT_PLAN.md
A  docs/security/MARKETFLOW_PROVIDER_CREDENTIAL_BOUNDARY.md
A  docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_ACCEPTANCE.md
A  docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_STATUS.md
M  marketflow/historical_data/__init__.py
M  marketflow/historical_data/__main__.py
A  marketflow/historical_data/massive_transport.py
M  marketflow/historical_data/monthly_acquisition.py
M  marketflow/historical_data/provider_response.py
A  tests/test_massive_rest_transport.py
```

## Staged Diff Checks

Staged files:

```text
A docs/architecture/MARKETFLOW_MASSIVE_REST_TRANSPORT.md
A docs/plans/MARKETFLOW_MASSIVE_REST_TRANSPORT_PLAN.md
A docs/security/MARKETFLOW_PROVIDER_CREDENTIAL_BOUNDARY.md
A docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_ACCEPTANCE.md
A docs/status/MARKETFLOW_MASSIVE_REST_TRANSPORT_STATUS.md
M marketflow/historical_data/__init__.py
M marketflow/historical_data/__main__.py
A marketflow/historical_data/massive_transport.py
M marketflow/historical_data/monthly_acquisition.py
M marketflow/historical_data/provider_response.py
A tests/test_massive_rest_transport.py
```

Staged diff stat:

```text
11 files changed, 1885 insertions(+), 3 deletions(-)
```

`git diff --cached --check`: pass.

No API key, provider credential, real provider response, downloaded market
data, generated persistent monthly acquisition, report, registry event,
sentinel, account/trade value, absolute user-home path, cache, environment
file, or unrelated refactor is part of the intended staged changes.

## Reviewer Findings

Reviewer A:

- Medium: forged page/continuation protocol state could be accepted by direct
  transport callers. Disposition: fixed with focused coverage.
- Low: 401 and 403 carried HTTP status but mapped to `NO_RESPONSE`.
  Disposition: fixed with focused coverage.
- Low: public prepared-request representation could expose raw continuation
  cursor. Disposition: fixed with focused coverage.

Reviewer B:

- Medium: public prepared-request representation could expose raw continuation
  cursor. Disposition: fixed with focused coverage.

Local audit:

- Medium: injected month request could alter multiplier, timespan, adjusted,
  sort, or limit. Disposition: fixed with focused coverage.

No critical or high reviewer finding remains.

## No-Network Evidence

Module import opened no socket during tests. Self-check used injected mock HTTP
only. Focused tests use `httpx.MockTransport`. Source assurance confirms no
provider SDK, environment credential read, fallback provider, candidate, Monte
Carlo, outcome, or runtime migration path was introduced. No real DNS,
external network, provider request, actual API key, provider account, or billing
path was exercised.

## Remaining Limitations

- Acceptance is offline mock-only.
- No real Massive.com request was made.
- No actual API key was inspected.
- No provider account or billing system was accessed.
- Acquisition remains disabled.
- No canonical dataset exists.
- No one-month smoke test occurred.
- Calendar freeze remains pending.
- Normal runtime migration remains pending.
- Predictive usefulness and profitability remain unaccepted.

## Next Controlled Phase

A future phase may propose controlled runtime integration or a separately
authorized provider smoke test. That future phase must preserve credential
safety, fixed endpoint construction, no-public-cursor evidence, monthly
executor ownership of retry/pagination/completeness, and separate approval for
any acquisition, canonical data, calendar freeze, or runtime migration.
