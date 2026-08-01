# MarketFlow Massive REST Transport Status

## Status

`MASSIVE_REST_TRANSPORT_ACCEPTED_OFFLINE_MOCK_ONLY`

## Current Acceptance Boundary

- Production transport code exists.
- Acceptance is offline through injected mock HTTP only.
- No real Massive.com request was made.
- No actual API key was inspected.
- No provider account or billing data was accessed.
- No canonical data exists.
- No one-month smoke test was performed.
- Normal runtime migration remains pending.
- Predictive usefulness and profitability remain unaccepted.

## Dependency Result

`httpx==0.28.1` is source-declared in `requirements.txt` and consumed through
`setup.py` requirements loading. No dependency install, upgrade, downgrade,
rename, or removal is part of this task.

## Implemented

- Fixed `https://api.massive.com` Custom Bars request construction.
- Bearer-header credential wrapper with redacted public representation.
- Strict continuation URL validation and safe reconstruction.
- Fixed timeout, redirect, TLS, `trust_env`, and body-limit settings.
- Exact response-byte capture under `Accept-Encoding: identity`.
- Strict content-type and content-encoding checks.
- Fixed HTTP status and transport-exception category mapping.
- Monthly executor protocol compatibility.
- Mock-only CLI self-check:
  `python -m marketflow.historical_data --massive-transport-self-check`.

## Acceptance Evidence

- Branch: `feature/swing-massive-rest-transport-adapter`.
- Baseline commit: `bdcac256ea217e37785a5f8f7754d04e1aefc2aa`.
- Baseline tag at commit:
  `v0.1.0-alpha.18-fake-transport-monthly-acquisition`.
- Contract v1 digest:
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.
- Contract v2 digest:
  `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`.
- Contract v2.1 digest:
  `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`.
- `env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py`:
  65 passed.
- `env\Scripts\python.exe -m pytest -q tests/test_massive_rest_transport.py tests/test_source_assurance.py`:
  86 passed.
- Expanded historical-data regression subset: 214 passed.
- `env\Scripts\python.exe -m pytest --collect-only -q`: 798 tests collected.
- `env\Scripts\python.exe -m pytest -q`: 798 passed.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed.
- `env\Scripts\python.exe -m pip check`: passed.
- `git diff --check`: passed with Git LF-to-CRLF working-copy warnings only.
- Ruff was not run because neither `env\Scripts\python.exe -m ruff` nor an
  `env\Scripts\ruff*` entrypoint exists in the task environment; no dependency
  was installed.

## Mock Self-Check Receipt

- Status: `MASSIVE_REST_TRANSPORT_SELF_CHECK`.
- Provider business identity: `MASSIVE.COM`.
- Fixed scheme: `https`.
- Fixed host: `api.massive.com`.
- Authorization header present: true.
- URL contains API key: false.
- Exact body bytes returned: true.
- Provider execution enabled: false.
- Real provider call performed: false.

## Security Boundary

- Credentials are accepted only by explicit constructor injection.
- Environment variables, credential files, keyrings, provider portals, account
  pages, and billing information are not inspected.
- Request logging and public receipts use sanitized request identity values.
- Authorization values are redacted from public request representations.
- Continuation URLs are validated and reconstructed under the fixed provider
  host before use.
- Transport acceptance is based on injected mock HTTP only.

## Test Count Change

Default collection is 798 tests after adding 65 focused Massive REST transport
tests. The added tests cover request construction, fixed 15-minute Custom Bars
constants, credential redaction, continuation validation, raw-cursor
sanitization in public prepared-request evidence, forged page-state rejection,
HTTP status mapping, transport exception mapping, body limits, cookie/header
boundaries, CLI self-check behavior, and monthly executor pagination
compatibility.

## Reviewer Dispositions

- Reviewer A: Medium forged page/continuation protocol state, Low auth HTTP
  response outcome category, and Low raw cursor exposure in sanitized prepared
  request representation. Disposition: fixed with focused regression coverage.
- Reviewer B: Medium raw cursor exposure in sanitized prepared request
  representation. Disposition: fixed with focused regression coverage.
- Additional local audit finding: injected month request values could alter
  multiplier, timespan, adjusted, sort, or limit. Disposition: fixed with
  focused regression coverage.

## Not Implemented

- Real provider execution.
- Environment credential loading.
- Provider SDK invocation.
- Transport-level retries.
- Pagination-chain traversal.
- Aggregate parsing or normalization inside the transport.
- Runtime provider mode.
- Calendar freeze, canonical dataset, or registry approval.

## Commit And Tag Status

No commit, tag, or push was created for this task.
