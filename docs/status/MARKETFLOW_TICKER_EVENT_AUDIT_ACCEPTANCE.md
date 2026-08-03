# MarketFlow Ticker Events Supporting Audit v1 Acceptance

Status: PASS

UTC acceptance date: `2026-08-03T17:46:07Z`

## Branch And Base

- repository: `marketflow`
- branch: `feature/swing-ticker-event-audit-v1`
- base commit: `4401cb6db61a1bbb0e007e6dfce89b1549eb1c6d`
- baseline tag at base: `v0.1.0-alpha.26-instrument-identity-live-evidence-accepted`

## Scope And Exclusions

Accepted scope:

- offline MarketFlow Ticker Events Supporting Audit v1 tooling;
- fixed experimental Massive.com Ticker Events request construction;
- strict Ticker Events response parser;
- event timeline and supporting-audit status derivation;
- raw, timeline, audit, and receipt artifact lineage;
- source identity binding to the accepted instrument identity evidence;
- plan, self-check, and controlled live command boundaries;
- focused tests and bounded documentation.

Excluded scope:

- real Ticker Events request;
- actual API key, credential, provider account, portal, billing, browser,
  account, trade, or entitlement inspection;
- external network use;
- provider data download;
- Ticker Overview, Custom Bars, All Tickers, splits, dividends, or calendar
  endpoint call;
- calendar freeze, split/dividend audit, canonical identity, registry
  authority, Strategy, Monte Carlo, outcome, performance, broker, execution,
  report rewrite, or runtime migration.

Tooling is accepted offline only. No real Ticker Events request occurred.

## Specification

- schema version: `marketflow.ticker_event_audit_specification.v1`
- classification: `PROVIDER_TICKER_EVENT_AUDIT_CANDIDATE_NONCANONICAL`
- provider: `MASSIVE.COM`
- endpoint family: `TICKER_EVENTS_EXPERIMENTAL_VX`
- endpoint stability: `EXPERIMENTAL`
- query identifier type: `COMPOSITE_FIGI`
- query identifier: `BBG000B9XRY4`
- ticker context: `AAPL`
- Share Class FIGI context: `BBG001S5N8V8`
- date range: `2022-01-01` through `2025-12-31`
- event type: `ticker_change`
- source identity run ID: `ident-509de6e2eb5e4a1db785e034bcfaf045`
- source continuity artifact ID: `ident-art-8607986a2341423182614a41c6236ed9`
- source continuity status: `IDENTITY_CONTINUITY_SUPPORTED`
- specification digest:
  `352710cea4dc09d11023404c8438d62f5df4d303bbc48083a091f6799d680769`

Canonical eligibility, registry eligibility, identity-freeze eligibility, and
Strategy enablement remain false.

The specification has no caller override, CLI identifier/ticker/date/type/
provider/host/root override, environment override, or current-date dependency.

## Source Identity Binding

The audit validates the exact accepted source identity evidence before
credential prompting or HTTP construction.

Accepted source-authorized six-manifest inventory:

- `TICKER_OVERVIEW_RAW_RESPONSE`: 2
- `TICKER_OVERVIEW_SNAPSHOT`: 2
- `IDENTITY_CONTINUITY_CANDIDATE`: 1
- `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT`: 1

Validated source fields:

- continuity artifact: `ident-art-8607986a2341423182614a41c6236ed9`
- continuity semantic digest:
  `50168a9e2fff208d0ba72df5657f21ee30d001f720f2cf44926f3b665bed4718`
- start snapshot digest:
  `75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928`
- end snapshot digest:
  `5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- ticker: `AAPL`
- primary exchange: `XNAS`
- security type: `CS`

Validation checks exact fixed run ID, exact continuity artifact ID, safe payload
references, lexical and physical root containment, no symlink/junction/reparse
indirection, regular files only, exact byte size and SHA-256, raw-to-snapshot
lineage, snapshot-to-continuity lineage, receipt-to-continuity lineage,
critical identity fields, false authority flags, and continuity digest
self-consistency.

There is no latest, first, or directory-neighbor source selection.

## Request And Transport

The controlled request is fixed to:

`GET https://api.massive.com/vX/reference/tickers/BBG000B9XRY4/events?types=ticker_change`

Accepted controls:

- fixed HTTPS;
- fixed host `api.massive.com`;
- fixed experimental endpoint path;
- fixed Composite FIGI path identifier;
- no ticker or CUSIP fallback;
- no `api.polygon.io` fallback;
- bearer-header authentication only;
- API key absent from query;
- `Accept: application/json`;
- `Accept-Encoding: identity`;
- TLS verification enabled;
- redirects disabled;
- `trust_env=False`;
- cookies cleared;
- exactly one HTTP invocation;
- no retry;
- no pagination;
- no endpoint-version substitution.

The module does not call Ticker Overview, Custom Bars, All Tickers, splits,
dividends, account, entitlement, registry, Strategy, Monte Carlo, outcome, or
runtime migration paths.

## Parser And Timeline

Strict accepted top-level fields:

- `request_id`
- `results`
- `status`

`request_id` is excluded from semantic and public evidence. Provider status is
fixed to `OK`. Unknown top-level fields, malformed JSON, non-object payloads,
and rejected statuses fail closed.

Strict accepted `results` fields:

- `events`
- `name`

`events` is required for complete evidence and must be an exact array. An empty
array is valid and produces `NO_TICKER_CHANGE_EVENTS_RETURNED`. Missing events
produces `TICKER_EVENT_EVIDENCE_INCOMPLETE`. `name` is optional and excluded
from identity authority and public receipts.

Strict event fields:

- `date`
- `type`
- `ticker_change`

`type` must be `ticker_change`. The ticker-change object accepts only `ticker`.
Dates must be strict ISO dates, ticker text is bounded and case-sensitive, no
numeric or boolean ticker coercion is accepted, missing ticker fails, unknown
event fields fail, duplicate exact events fail, and conflicting same-date/type
events fail.

Canonical timeline sorting is deterministic by date, event type, and ticker.
Endpoint stability is persisted as `EXPERIMENTAL`.

Range classifications:

- `BEFORE_CONTRACT_RANGE`
- `WITHIN_CONTRACT_RANGE`
- `AFTER_CONTRACT_RANGE`

The inclusive dates `2022-01-01` and `2025-12-31` classify as
`WITHIN_CONTRACT_RANGE`. Pre-range and post-range context is retained. The
tooling does not infer effective ticker intervals beyond explicit provider
event records.

## Supporting Audit Statuses

Empty events array:

`TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE`

Only pre-range events:

`TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE`

Only post-range events:

`TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE`

Any in-range ticker-change event:

`TICKER_EVENT_CHANGE_REQUIRES_SEGMENT_REVIEW`

Missing events or incomplete schema:

`TICKER_EVENT_EVIDENCE_INCOMPLETE`

Endpoint unavailable:

`TICKER_EVENT_ENDPOINT_UNAVAILABLE`

Evidence absence never becomes no-event evidence.

The existing snapshot continuity status remains
`IDENTITY_CONTINUITY_SUPPORTED`. When no in-range event is reported, the
combined candidate status is
`IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE`. This remains
candidate evidence only. Any in-range change requires segment review.

No automatic stitching, frozen identity segment, canonical identity, registry
eligibility, generation-freeze eligibility, or Strategy authority is created.

## Artifact Schema And Lineage

Ticker Events artifacts use:

`marketflow.ticker_event_audit_artifact_manifest.v1`

Expected audit-run inventory:

- `TICKER_EVENTS_RAW_RESPONSE`: 1
- `TICKER_EVENT_TIMELINE`: 1
- `TICKER_EVENT_AUDIT_CANDIDATE`: 1
- `TICKER_EVENT_AUDIT_RECEIPT`: 1
- total: 4 manifests

Runtime root:

`.marketflow/source_authority/ticker_events/runs/`

Artifact controls include opaque run IDs, no FIGI/ticker/date in run-directory
name, no CWD/environment/caller root override in public paths, safe relative
refs, lexical and physical containment, no symlink/junction/reparse
indirection, regular files only, no overwrite, payload before manifest,
manifest committed last, exact byte size and SHA, saved-disk validation before
receipt, and no latest/first artifact selection.

Lineage chain:

`accepted identity continuity artifact -> TICKER_EVENTS_RAW_RESPONSE -> TICKER_EVENT_TIMELINE -> TICKER_EVENT_AUDIT_CANDIDATE -> TICKER_EVENT_AUDIT_RECEIPT`

Validation checks role-bound inputs, input ref-to-artifact-ID reconciliation,
transitive lineage recomputation, run identity, source identity run/artifact
reference, continuity semantic digest, and exact payload/semantic digests. The
accepted identity artifact is referenced and not copied or rewritten.

Future live raw responses are retained as exact bytes with exact SHA and size,
validated before parsing, and excluded from public receipts.

## Receipt Sanitization

Receipts may include audit run ID, specification digest, provider, Composite
FIGI, ticker context, range dates, source identity run/artifact IDs, source
continuity semantic digest, raw/timeline/audit artifact IDs and digests, event
counts, pre/in/post-range counts, standardized event dates and reported
symbols, audit status, combined identity candidate status, experimental status,
and false authority flags.

Receipts exclude API key, Authorization header, raw URL, request ID value, raw
body, provider asset text, account data, absolute paths, raw exceptions,
prices, candidate values, and performance values.

## Commands

Plan command:

`python -m marketflow.source_authority --ticker-event-audit-plan`

Accepted as offline, no credential, no write, fixed FIGI/range, digest,
experimental endpoint, no automatic stitching, and false authority flags.

Self-check command:

`python -m marketflow.source_authority --ticker-event-audit-self-check`

Accepted as fictional key, `httpx.MockTransport` only, temporary artifacts,
empty/pre/in/post/incomplete fixtures, no socket, and no persistent output.

Controlled live command:

`python -m marketflow.source_authority --ticker-event-audit-run`

Implemented but not executed in this acceptance. Required sequence is TTY check,
sanitized plan, exact phrase display, operator confirmation, nonsecret
source-identity/runtime preflight, `getpass`, one fixed HTTP request, artifact
persistence, and sanitized receipt.

Preflight runs before `getpass`, key construction, transport construction,
output-run creation, or provider request on source-evidence failure. Expected
failures return sanitized receipts without traceback, path, secret, URL, or raw
exception text.

## Public API

Public exports include only bounded plan, specification, digest, self-check,
error, and classification surfaces. Private run, transport, root, prompt, and
test seams remain leading-private, unexported, and CLI-inaccessible.

No ordinary caller can provide a transport, root, run ID, identifier, dates,
event type, host, or credential through the public API or CLI.

## Verification

Checks run with `env\Scripts\python.exe`:

- `python -m pip check`: passed
- focused ticker-event tests: `30 passed`
- focused identity tests: `67 passed`
- related transport/artifact/source-assurance/prior-integrity bundle:
  `294 passed`
- full collection: `1055 tests collected`
- full suite: `1055 passed`
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed
- `git diff --check`: passed with Git LF-to-CRLF working-copy normalization
  warnings on modified text files

Contract and identity digests reproduced unchanged:

- v1: `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`
- v2: `59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0`
- v2.1: `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`
- identity:
  `a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`

The full collection increased from 1025 tests at the accepted identity baseline
to 1055 because this phase adds 30 focused ticker-event audit tests.

## Git Status Evidence

Pre-test and post-test status were intentionally dirty only with the
ticker-event audit source, bounded source-authority package/CLI updates,
focused tests, and four required documents. This acceptance document is added
by the final acceptance task.

No `.marketflow` audit artifact, provider response, credential, environment
file, report, cache, canonical/registry artifact, absolute user-home path, or
unrelated refactor is part of the accepted change set.

## Reviewer Findings

Reviewer A covered source identity evidence binding, request/parser contract,
raw/timeline/audit/receipt lineage, and credential/path/no-network controls.
Findings:

- Medium: persisted source binding omitted the upstream continuity digest it
  validated. Disposition: fixed by carrying the source continuity semantic
  digest in the binding, manifests, audit payloads, and public receipts.
- Medium: manifest validation accepted corrupted `lineage_artifact_ids` when
  input refs remained valid. Disposition: fixed by recomputing transitive
  lineage from loaded input manifests.
- Medium: getpass/key-construction failures could bypass sanitized receipts.
  Disposition: fixed with sanitized failure receipts and focused regressions.

Reviewer B covered event range classifications, supporting-audit statuses, no
automatic stitching, experimental-authority limitation, CLI/tests/docs, and
prior-integrity preservation. Finding:

- Medium: the prior identity CLI override guard was weakened by substring
  checks. Disposition: fixed by parsing CLI `add_argument` calls with AST and
  checking exact option names.

No critical, high, or unresolved medium reviewer finding remains.

## Remaining Limitations

- Tooling accepted offline only.
- No real Ticker Events request occurred.
- No actual API key was inspected.
- Endpoint remains experimental.
- Audit is supporting evidence only.
- Identity freeze remains pending.
- Calendar, splits, dividends, registry, and Strategy remain pending.
- Canonical, registry, identity-freeze, generation, and Strategy authority
  remain false.

## Next Controlled Live Procedure

A future controlled live run requires separate human authorization, interactive
TTY, exact digest-bound confirmation phrase, nonsecret source preflight,
credential entry only through `getpass`, one fixed Ticker Events request, and
sanitized receipt review. A future live result will still be supporting
noncanonical candidate evidence unless separately accepted with remaining
identity, calendar, corporate-action, registry, and authority evidence.
