# MarketFlow Ticker Events Live Evidence Acceptance

Status: PASS

UTC acceptance date: `2026-08-03T19:38:15Z`

## Branch And Parent

- repository: `marketflow`
- branch: `fix/swing-ticker-event-response-identity-fields`
- parent commit: `2a6ac42 feat: add ticker event supporting audit v1`

## Production Source Freeze

Production source hashes recorded before this offline acceptance work:

- `marketflow/source_authority/ticker_event_audit.py`:
  `BD6B54404839A3A3F4293EDA194698887390BCACF5E6E0A671F041CA7CB3431B`
- `marketflow/source_authority/__init__.py`:
  `3A3E63C5220C9F7DD2A4D04E2B08EA894224E9643B3E6EF88140DD04CD0CAAF7`
- `marketflow/source_authority/__main__.py`:
  `2837BB9B7156E6B9F032A84AF3243757726DD5DC82F00BEDD2D2478E15295F20`

These files were frozen during acceptance. Any production-source hash change
would require a blocked result and a repeated controlled live audit.

## Specification

- schema: `marketflow.ticker_event_audit_specification.v1`
- specification digest:
  `352710cea4dc09d11023404c8438d62f5df4d303bbc48083a091f6799d680769`
- endpoint stability: `EXPERIMENTAL`
- identifier type: `COMPOSITE_FIGI`
- identifier: `BBG000B9XRY4`
- event type: `ticker_change`
- inclusive contract range: `2022-01-01` through `2025-12-31`

## Source Identity

- identity run ID: `ident-509de6e2eb5e4a1db785e034bcfaf045`
- continuity artifact ID: `ident-art-8607986a2341423182614a41c6236ed9`
- continuity semantic digest:
  `50168a9e2fff208d0ba72df5657f21ee30d001f720f2cf44926f3b665bed4718`
- source continuity status: `IDENTITY_CONTINUITY_SUPPORTED`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- ticker context: `AAPL`

The accepted source identity chain remains the fixed six-manifest source. It is
referenced, not copied or rewritten.

## Live Run Inventory

- audit run ID: `tkev-959a591271874fe49bc8cb34bb29be36`
- provider request count: `1`
- `TICKER_EVENTS_RAW_RESPONSE`: `1`
- `TICKER_EVENT_TIMELINE`: `1`
- `TICKER_EVENT_AUDIT_CANDIDATE`: `1`
- `TICKER_EVENT_AUDIT_RECEIPT`: `1`
- total manifests: `4`

Artifact IDs and digests:

- raw response artifact: `tkev-art-5d8ed7c1aa0e451ab1c7b297230dca33`
- raw response digest:
  `07082085e9e41c467e020774954c045e83613d9581976ca26e87b74e3bbf15dc`
- timeline artifact: `tkev-art-54a14c247fb2459a9c588dd4695b4358`
- timeline semantic digest:
  `36ccff35908df36a7fadb124d6cb846e4ac0cace578830e7591f7edf92bde820`
- audit artifact: `tkev-art-df20d0c474464b74a28a6f4ed451fef6`
- receipt artifact: `tkev-art-2168e3f7caec46d59436ab0e4280d49d`

The four manifests validate with the expected run ID, schema, type, stage, safe
relative payload refs, exact byte sizes, SHA-256 values, semantic digests,
regular-file payloads, role-bound inputs, and external source artifact
reference.

## Lineage

Accepted lineage:

`accepted identity continuity artifact -> TICKER_EVENTS_RAW_RESPONSE -> TICKER_EVENT_TIMELINE -> TICKER_EVENT_AUDIT_CANDIDATE -> TICKER_EVENT_AUDIT_RECEIPT`

The raw-to-timeline, timeline-to-audit, and audit-to-receipt bindings validate.
There is no latest, first, or directory-neighbor source selection.

## Response Identity Fields

- accepted `results` fields: `events`, `name`, `cik`, `composite_figi`
- unknown result fields: rejected
- response Composite FIGI status:
  `RESPONSE_COMPOSITE_FIGI_PRESENT_MATCHED`
- response CIK status:
  `RESPONSE_CIK_PRESENT_MATCHED`

`name` is excluded from authority and public evidence. The CIK value is not
included in this acceptance document.

## Event Result

Accepted event:

- date: `2003-09-10`
- type: `ticker_change`
- reported ticker: `AAPL`
- range classification: `BEFORE_CONTRACT_RANGE`

Counts:

- event count: `1`
- pre-range event count: `1`
- in-range event count: `0`
- post-range event count: `0`

The event is retained as historical context. No effective ticker interval is
inferred and no automatic stitching occurs.

## Supporting Audit Result

- receipt status: `TICKER_EVENT_AUDIT_READY_NONCANONICAL`
- audit status:
  `TICKER_EVENT_AUDIT_SUPPORTS_NO_REPORTED_IN_RANGE_CHANGE`
- combined identity candidate:
  `IDENTITY_CONTINUITY_SUPPORTED_WITH_TICKER_EVENT_AUDIT_CANDIDATE`
- automatic stitching: `false`
- canonical eligibility: `false`
- registry eligibility: `false`
- identity-freeze eligibility: `false`
- Strategy enabled: `false`

This supports the existing point-in-time identity candidate. It does not prove
that the experimental endpoint provides complete universal identity history.

## Failure Observability

Future complete-response parser failures after raw-response persistence write a
sanitized `TICKER_EVENT_AUDIT_RECEIPT` failure artifact. The earlier failed run
`tkev-69ff705e692945bab7ac45c5332648a0` was not rewritten.

Failure receipts exclude raw body, URL, request ID, key, Authorization header,
provider asset name, CIK value, absolute path, and raw exception text.

## Receipt Sanitization

The successful receipt includes only bounded evidence: standardized Composite
FIGI, ticker context, event date/type/ticker, range classification, artifact
IDs and digests, count/status fields, source identity IDs/digests, endpoint
stability, and false authority flags.

It excludes API key, Authorization header, raw URL, request ID value, raw
provider body, provider asset name, CIK value, account data, absolute paths,
raw exceptions, prices, candidate values, and performance values.

## Acceptance Checks

Final checks use `env\Scripts\python.exe` and are offline:

- `python -m pip check`
- focused Ticker Events tests
- focused instrument identity tests
- related source-assurance and prior-integrity tests
- full collection
- full pytest
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`
- `git diff --check`
- staged diff checks before commit

The full collection count is expected to be `1064`. The focused Ticker Events
count is expected to be `39`.

## Reviewer Findings

Reviewer A covered FIGI/CIK compatibility, source-identity matching, saved
four-manifest lineage, raw/timeline/audit/receipt integrity, failure
observability, and sanitization. Finding: no findings.

Reviewer B covered event/range classification, supporting audit status, no
automatic stitching, experimental authority limits, public API/CLI boundaries,
tests, and documentation. Finding: no findings.

No critical, high, medium, or low reviewer finding remains. Any valid
production-source finding would have blocked this acceptance and required the
controlled live audit to be repeated after source correction.

## Limitations

- Endpoint stability remains `EXPERIMENTAL`.
- Evidence remains noncanonical supporting evidence.
- No frozen identity segment is created.
- Calendar authority remains pending.
- Split and dividend completeness remain pending.
- Canonical registry authority remains pending.
- Strategy, Monte Carlo, outcome, performance, broker, and execution authority
  remain out of scope.
