# MarketFlow Fake-Transport Monthly Acquisition Acceptance

## Decision

FAKE-TRANSPORT MONTHLY ACQUISITION MECHANICS: PASS FOR DETERMINISTIC OFFLINE
SIMULATION ONLY.

PROVIDER EXECUTOR: NOT IMPLEMENTED.

PROVIDER ACQUISITION: DISABLED.

CANONICAL DATASET: NOT AVAILABLE.

UTC acceptance date: `2026-08-01T18:42:42Z`.

Branch: `feature/swing-fake-transport-monthly-acquisition`.

Base commit: `0386e20941c899a7c2f4922101c3d433f105399e`.

Baseline tag: `v0.1.0-alpha.17-historical-data-artifact-lineage`.

No Git tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- deterministic scripted fake transport;
- strict one-month request contract for fictional tickers;
- immutable request attempts;
- exact raw fake response byte artifacts;
- strict Decimal provider-response parser;
- sanitized continuation identity;
- semantic retry equivalence and variance blocking;
- pagination and range-coverage completeness gates;
- paired normalized OHLCV and aggregate-audit artifacts;
- saved monthly manifest validation;
- sanitized dry CLI self-check;
- focused and full offline tests.

Excluded scope:

- Massive.com or Polygon provider call;
- API-key, credential, account, billing, portal, browser, trade, or performance
  review;
- socket, DNS, network, or real sleep path;
- real provider response or real market-data download;
- operator-frozen calendar;
- production provider executor;
- canonical dataset;
- Strategy candidate generation;
- Monte Carlo;
- outcome or performance evaluation;
- broker or execution capability;
- report rewrite;
- registry authority;
- normal runtime migration.

## Artifact Schema

Monthly acquisition artifact schema:

```text
marketflow.monthly_acquisition_artifact_manifest.v1
```

Implemented artifact types:

- `MONTH_CHUNK_REQUEST_CONTRACT`;
- `REQUEST_ATTEMPT_RECORD`;
- `RAW_PROVIDER_PAGE`;
- `MONTH_CHUNK_COMPLETENESS_MANIFEST`;
- `MONTH_NORMALIZED_15M_OHLCV`;
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`;
- `MONTH_ACQUISITION_RECEIPT`.

Artifacts are written payload first and manifest last with no overwrite. Saved
monthly manifests are reloaded and validated before returned use. Validation
checks schema, run, type, stage, safe relative payload references, exact payload
SHA-256, byte size, parent refs, and input refs.

## Fake Transport

The fake transport is deterministic and script-driven. It accepts exact logical
request objects, rejects unexpected requests, identifies unconsumed scripted
outcomes, imports no provider client, opens no socket, performs no DNS, uses no
randomness, and cannot silently become a real transport.

Injected fake clock and fake sleeper are used. No real sleep is performed.

## Month Request

The immutable request binds:

- schema/version;
- Contract v2.1 digest;
- base v2 digest;
- fictional acquisition-generation identity;
- fictional identity-segment identity;
- fictional canonical ticker;
- month key;
- effective start/end;
- multiplier 15;
- timespan `minute`;
- adjusted `true`;
- ascending sort;
- limit 50000;
- source timestamp contract version;
- deterministic request digest.

Ordinary and clipped months validate. Effective dates must remain inside one
logical month and inside `2022-01-01` through `2025-12-31`. There is no
current-date, rolling, arbitrary provider URL, or real-ticker behavior.

## Retry Policy

Fixed retry behavior:

- maximum attempts: 3;
- backoffs: `[2, 5]`;
- jitter: `false`.

Retryable classes are exactly:

- `TRANSPORT_TIMEOUT`;
- `CONNECTION_RESET`;
- `HTTP_408`;
- `HTTP_429`;
- `HTTP_500`;
- `HTTP_502`;
- `HTTP_503`;
- `HTTP_504`.

Retry-After is considered only for HTTP 429 and 503, must be an integer from 0
through 60, and uses max(configured backoff, Retry-After). Malformed, negative,
noninteger, and greater-than-60 values block retry. No delay is recorded after a
final attempt.

## Attempts And Raw Pages

Every attempt is immutable and retains logical page request ID, attempt ID,
ordinal, fixed status, fixed failure category, fake timestamps, intended delay,
HTTP category, response-body availability/completeness, raw artifact ID where
available, and semantic projection digest where valid.

Failed attempts are retained. Raw exception strings are not persisted. A valid
response is not accepted merely because it exists.

Raw fake response bytes are stored exactly, with exact byte size, exact SHA-256,
and fixed raw media type. Reformatted JSON is not used as raw evidence.

## Parser And Projection

Provider response parsing uses JSON `Decimal` parsing. It rejects NaN, Infinity,
numeric-string coercion, boolean-as-integer coercion, duplicate keys, invalid
status, empty accepted responses, incoherent counts, timestamp misalignment,
high/low conflicts, negative volume, negative transaction counts, duplicate or
nonascending timestamps, and rows outside the effective month.

The projection version is:

```text
OHLCV_PLUS_CONTRACTED_AUDIT_FIELDS_V1
```

The projection includes ticker, adjusted, status, counts, continuation
presence, sanitized continuation identity, ordered timestamp/OHLCV rows, VWAP
presence/value, and transaction-count presence/value. It excludes request ID,
attempt ID, retrieval timestamps, JSON formatting, JSON key order, credentials,
raw cursor text, and raw continuation URLs.

Decimal equality is exact and canonical: `100`, `100.0`, and `1e2` are
equivalent; `100.0000001` differs; negative zero is canonicalized; no epsilon or
display rounding exists.

## Pagination And Completeness

Pagination requires contiguous page ordinals from one, exact predecessor
accepted-page identity, exact sanitized continuation chain, no repeated
continuation, no duplicate timestamp across pages, no page from another request,
and explicit exhaustion.

Month completeness requires a validated completeness manifest. Raw pages without
that manifest are incomplete and not normalizable. Completeness binds month
request identity/digest, month key, effective range, accepted page IDs, accepted
attempt IDs, page ordinals, raw payload digests, semantic projection digests,
page-chain digest, row count, first/last source-window start, pagination
exhaustion, duplicate/conflict status, and completion status.

Range coverage must be complete for the effective date range. Incomplete chains
block with `RANGE_COVERAGE_INCOMPLETE`.

## Normalized Pair

The normalized pair is immutable and parented to the exact completeness
manifest:

- `MONTH_NORMALIZED_15M_OHLCV`;
- `MONTH_NORMALIZED_AGGREGATE_AUDIT_FIELDS`.

Both artifacts preserve exact row count and timestamp order. No provider row is
omitted, no sorting repair is performed, no synthetic values are fabricated, no
RTH filtering is applied, and extended-hours rows remain available for later
policy-controlled exclusion.

Provenance remains:

```text
SCRIPTED_FAKE_TRANSPORT_FIXTURE
```

It does not claim Massive.com or Polygon acquisition.

## Receipt And CLI

The receipt is sanitized and includes fixed status, fake execution ID, month
request digest, month key, attempt count, accepted-page count,
failed/rejected-attempt count, intended retry delays, completeness status, safe
artifact receipts, and fixed findings.

It excludes OHLCV values, raw response body, raw continuation URL, credentials,
absolute paths, account/trade data, candidate/performance values, and raw
exceptions.

CLI:

```text
env\Scripts\python.exe -m marketflow.historical_data --monthly-acquisition-self-check
```

The CLI self-check uses a deterministic fictional two-page month in an
automatically removed temporary directory. It performs no real sleep, opens no
socket, accepts no ticker/source-root option, prints sanitized output, imports
no provider client, performs no bar-engine derivation, runs no
Strategy/MC/outcome path, and performs no runtime migration.

## Contract Non-Regression

Reproduced digests:

```text
v1:   29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
v2:   59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
v2.1: 538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

No contract file was edited to make the executor pass.

## Verification

Focused fake-transport suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_fake_transport_monthly_acquisition.py
```

Result: 18 passed.

Focused fake-transport, historical-artifact, Contract regression,
source-assurance, packaging, and prior-integrity suite:

```text
env\Scripts\python.exe -m pytest -q tests/test_fake_transport_monthly_acquisition.py tests/test_historical_data_artifacts.py tests/test_historical_data_engine.py tests/test_acquisition_contract_v2_1.py tests/test_acquisition_contract_v2.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py
```

Result: 149 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result: 733 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result: 733 passed.

Test count explanation: accepted starting collection was 715 historical-data
artifact-lineage tests; final collection is 733 because this task adds 18
focused fake-transport monthly acquisition tests.

`pip check`: pass, `No broken requirements found.`

Compileall:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

Ruff focused source check: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization warnings
only.

## Git Status Evidence

Pre-final-suite status:

```text
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
?? docs/architecture/MARKETFLOW_MONTHLY_ACQUISITION_ARTIFACTS.md
?? docs/plans/MARKETFLOW_FAKE_TRANSPORT_MONTHLY_ACQUISITION_PLAN.md
?? docs/status/MARKETFLOW_FAKE_TRANSPORT_MONTHLY_ACQUISITION_STATUS.md
?? marketflow/historical_data/fake_transport.py
?? marketflow/historical_data/monthly_acquisition.py
?? marketflow/historical_data/provider_response.py
?? tests/test_fake_transport_monthly_acquisition.py
```

The final acceptance evidence file is added by this acceptance task.

No generated monthly run, provider payload, generated dataset, report, cache,
credential, API key, absolute user-home path, registry/sentinel/authority
artifact, or unrelated refactor is part of the intended changes.

## Reviewer Findings

Reviewer A:

- Critical: sanitized continuation identity missing from semantic projection.
  Disposition: fixed with focused coverage.
- High: continuation range not checked against request. Disposition: fixed with
  focused coverage.
- High: non-OK and empty responses accepted. Disposition: fixed with focused
  coverage.
- Medium: receipt semantic retry status overstated. Disposition: fixed.
- Medium: fixed 2022-2025 range not enforced. Disposition: fixed.

Reviewer B:

- High: monthly lineage not saved-validated before downstream use. Disposition:
  fixed with saved manifest reload/validation and focused coverage.
- High: completeness could be marked complete for empty/incomplete chains.
  Disposition: fixed with nonempty parser gate and range-coverage gate.
- Medium: returned and persisted receipts diverged. Disposition: fixed by
  excluding the post-commit self-reference from both.
- Medium: receipt semantic retry status overstated. Disposition: fixed.
- Medium: CLI self-check did not exercise multi-page pagination. Disposition:
  fixed with deterministic two-page self-check.

No critical or high reviewer finding remains.

## Remaining Limitations

- Fake-transport monthly mechanics are accepted only for deterministic offline
  simulation.
- No real provider was contacted.
- No actual provider response was used.
- No calendar was operator-frozen.
- No production provider executor exists.
- No canonical dataset exists.
- Normal runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Next Phase

Future work may propose a real provider acquisition executor only through a
separate design and acceptance task. That phase must preserve this fake-only
evidence boundary and must separately prove provider credentials, entitlement,
pagination, completeness, adjustment/corporate-action provenance, and runtime
integration policy before any canonical dataset or research protocol approval.
