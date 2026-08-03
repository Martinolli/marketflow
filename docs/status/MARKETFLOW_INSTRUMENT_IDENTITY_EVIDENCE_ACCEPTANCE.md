# MarketFlow Instrument Identity Evidence Acceptance

Status: PASS

UTC acceptance date: 2026-08-03T01:05:39Z

## Branch And Base

- Repository: `marketflow`
- Branch: `feature/swing-instrument-identity-evidence-v1`
- Base commit: `a6f067872082a0b509bcaf912f0e040ca3db2a4a`
- Baseline tag at base: `v0.1.0-alpha.23-live-month-rth-diagnostic`

## Scope

This acceptance covers offline source-authority tooling for MarketFlow
Instrument Identity Evidence v1. It accepts only noncanonical candidate evidence
tooling for two point-in-time Massive.com Ticker Overview snapshots.

Accepted classification:

`PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL`

No live Massive.com request occurred. No actual API key or credential was
requested, inspected, read from the environment, printed, or committed.

## Specification

- schema version: `marketflow.instrument_identity_specification.v1`
- specification digest:
  `a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`
- provider: `MASSIVE.COM`
- endpoint family: `TICKER_OVERVIEW_V3`
- ticker: `AAPL`
- start snapshot date: `2022-01-01`
- end snapshot date: `2025-12-31`
- expected market: `stocks`
- expected locale: `us`
- expected currency: `usd`

Canonical eligibility, registry eligibility, generation-freeze eligibility, and
Strategy enablement remain false.

The specification has no caller override, CLI ticker/date/provider/host
override, environment override, or current-date dependency.

## Transport And Credential Boundary

The prepared request is fixed to:

`GET https://api.massive.com/v3/reference/tickers/AAPL`

Each snapshot uses exactly one `date` query parameter:

- `date=2022-01-01`
- `date=2025-12-31`

The transport uses bearer-header authentication only, no key in URL, fixed
HTTPS and Massive.com host, exact ticker endpoint, TLS verification, redirects
disabled, `trust_env=False`, no cookies, `Accept: application/json`,
`Accept-Encoding: identity`, one request per snapshot, and no internal retry.

The package imports no Polygon/Massive SDK and does not call Custom Bars,
Ticker Events, All Tickers, splits, dividends, provider account, or entitlement
endpoints.

## Parser And Projection

Accepted top-level fields are strictly:

- `request_id`
- `status`
- `results`
- `count`

`request_id` values are excluded from receipts and semantic authority.
`status` is fixed and validated. `results` must be one object. `count` is
optional, but when present must be an exact nonnegative integer equal to one.
Unknown top-level and result fields fail closed.

The bounded identity projection includes the fixed critical fields: ticker,
active status, market, locale, currency, primary exchange, Composite FIGI, Share
Class FIGI, and security type. Supporting CIK, list date, and delisting evidence
use explicit presence statuses.

Missing critical fields produce `IDENTITY_SNAPSHOT_INCOMPLETE`. Present
identity values are still validated before an incomplete projection is emitted.
No boolean/string/integer coercion or fabricated optional value is accepted.

Address, phone number, homepage, branding, description, market capitalization,
employee counts, and share counts do not enter identity projection or public
receipts.

## Artifacts

Identity artifacts use schema:

`marketflow.instrument_identity_artifact_manifest.v1`

Accepted public evidence artifact types:

- `TICKER_OVERVIEW_SNAPSHOT`
- `IDENTITY_CONTINUITY_CANDIDATE`
- `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT`

The implementation also persists a bounded raw parent artifact,
`TICKER_OVERVIEW_RAW_RESPONSE`, so future live response bytes are committed and
validated on disk before identity projection.

Artifact controls include repository-derived ignored runtime root, opaque run
IDs, safe relative refs, lexical and physical path containment,
symlink/junction/reparse rejection, regular-file requirements, no overwrite,
payload committed before manifest, manifest committed last, exact byte size and
SHA-256, semantic digest validation, and saved-disk validation before receipt.

No latest/first file selection exists.

## Continuity

Continuity compares start and end snapshots exactly on:

- ticker
- market
- locale
- currency
- primary exchange
- Composite FIGI
- Share Class FIGI
- security type

Supporting comparisons include CIK when present on both sides, active status,
list date, and delisting evidence.

Statuses remain:

- `IDENTITY_CONTINUITY_SUPPORTED`
- `IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW`
- `IDENTITY_EVIDENCE_INCOMPLETE`
- `IDENTITY_EVIDENCE_CONFLICT`

Automatic stitching is prohibited. Critical identity changes produce
`IDENTITY_CHANGE_REQUIRES_SEGMENT_REVIEW`. The tooling does not prefer the end
snapshot, prefer the newest response, infer continuity only from ticker, create
a frozen identity segment, or mark a candidate canonical.

## Ticker Events Deferral

Ticker Events remains:

`TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`

Matching start/end snapshots create only `IDENTITY_CONTINUITY_CANDIDATE`; they
do not create final identity authority.

## Receipt Sanitization

Public receipts retain only the standardized identity evidence under review,
artifact IDs, semantic digests, continuity status, fixed findings, and false
authority flags.

Public receipts exclude API key, Authorization header, raw URL, raw response
body, request ID value, address, phone, homepage, branding, description, market
capitalization, employee/share counts, account data, absolute paths, raw
exceptions, Strategy fields other than disabled flags, and performance values.

## Commands

Plan command:

`python -m marketflow.source_authority --instrument-identity-plan`

Accepted as offline, no credential, no write, exact fixed ticker/dates, digest,
Ticker Events pending, and canonical/registry flags false.

Self-check command:

`python -m marketflow.source_authority --instrument-identity-self-check`

Accepted as fictional-key, `httpx.MockTransport` only, matching and
changed-identity cases, temporary root, no persistent output, and no socket.

Live command:

`python -m marketflow.source_authority --instrument-identity-run`

Implemented but not executed in this acceptance. It requires interactive TTY,
shows the digest-bound confirmation phrase before credential prompt, uses
`getpass` only after confirmation, performs exactly two Overview requests, has
no automatic retry, accepts no CLI/env/config key, accepts no caller
ticker/date/root override, and writes noncanonical isolated artifacts only.

## Verification

Pre-test Git status: intentionally dirty only with the identity source package,
focused tests, and requested documentation.

Checks run with `env\Scripts\python.exe`:

- `python -m pip check`: passed
- focused identity tests: `51 passed`
- related Massive transport, artifact, source-assurance, and prior-integrity
  bundle: `351 passed`
- full collection: `1009 tests collected`
- full suite: `1009 passed`
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed
- `git diff --check`: passed

No warnings were reported by the final test or compile checks.

Contract digests reproduced unchanged:

- v1: `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`
- v2: `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`
- v2.1: `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

The full collection increased from the accepted 958-test baseline to 1009
tests because this phase adds 51 focused identity evidence tests.

## Repository-Root Correction Addendum

A subsequent controlled local live attempt exposed a live-runner defect after
the original offline acceptance. The operator accepted the exact digest-bound
confirmation phrase and the command then prompted for the API key through
`getpass` before completing nonsecret local preflight. The command failed
locally with repository-root resolution and surfaced an uncaught traceback with
an absolute local path.

Root cause:

`_repository_root()` required a `pyproject.toml` marker that is absent from this
valid source checkout.

Corrected behavior:

- repository root derives from
  `marketflow/source_authority/instrument_identity.py` via
  `Path(__file__).resolve().parents[2]`;
- fixed repository evidence is regular-file checked;
- production runtime output resolves only beneath
  `.marketflow/source_authority/identity/runs/` under the validated repository;
- unrelated current working directories and shadow `.marketflow` trees are not
  output authority;
- local preflight runs before `getpass`, `ProviderApiKey`, transport
  construction, runtime-directory creation, or provider request;
- expected repository/runtime failures emit
  `INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED` with fixed failure categories and
  no traceback or absolute path.

No provider request was completed by the failed local attempt, and no identity
snapshot or artifact from that attempt was accepted.

The identity specification digest remains:

`a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`

Final live identity tooling acceptance is blocked until the controlled live
identity run is repeated after this correction. That future evidence remains
noncanonical candidate evidence unless separately accepted with the required
Ticker Events and authority evidence.

Repository-root correction final checks:

- `python -m pip check`: passed
- focused identity tests: `67 passed`
- related Massive transport, artifact, source-assurance, and prior-integrity
  bundle: `438 passed`
- full collection: `1025 tests collected`
- full suite: `1025 passed`
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed
- `git diff --check`: passed with Git LF-to-CRLF working-copy normalization
  warnings on modified text files

Repository-root correction reviewers:

- Reviewer A initially found evidence-parent symlink/reparse coverage and
  private-seam documentation wording gaps; both were corrected and covered by
  focused regressions.
- Reviewer B initially found a Python 3.12-only local preflight gate that was
  stricter than package metadata; it was removed and covered by focused
  regression.

No critical, high, or unresolved medium reviewer finding remains.

## Reviews

Reviewer A covered request/parser/identity-field contract, credential boundary,
raw-response and snapshot artifact/path/atomic-write controls, and receipt
sanitization. Result: no issues found after the raw-response correction.

Reviewer B covered continuity logic, no automatic stitching, Ticker Events
deferral, CLI/runtime isolation, tests/docs coverage, and prior-integrity
boundaries. Result: no issues found.

## Remaining Limitations

Start and end snapshots are not yet provider-verified. Ticker Events audit is
pending. Identity continuity is not frozen. Calendar, corporate-action, and
registry authority remain pending. Canonical, registry, generation-freeze, and
Strategy eligibility remain false.

No Strategy, Monte Carlo, outcome, performance, broker, execution, registry
authority, report rewrite, runtime migration, split/dividend audit, or calendar
freeze occurred.

## Next Manual Live Procedure

After separate human authorization, run the controlled live command in an
interactive terminal:

`python -m marketflow.source_authority --instrument-identity-run`

Verify the printed plan, type the exact digest-bound confirmation phrase, enter
the Massive.com key through `getpass`, and review the sanitized receipt. That
future run will still be noncanonical candidate evidence until Ticker Events and
remaining authority evidence are accepted.
