# MarketFlow Massive Response Schema Compatibility Correction

## Status

`CORRECTIVE_TASK_ACCEPTED_OFFLINE_LOCAL_COMMIT_PENDING`

## Scope

- Correct HTTP-200 Massive.com Custom Bars response-schema compatibility without
  weakening strict allowlisting.
- Preserve the fixed Massive smoke target and Contract digests.
- Keep acquisition disabled.
- Do not inspect API keys, credentials, provider account state, billing state,
  or provider portal state.
- Do not make a real provider request.
- Do not change endpoint construction, retry policy, pagination algorithms,
  Decimal semantics, normalized OHLCV schema, Strategy, Monte Carlo, outcomes,
  registry, or execution behavior.

## Root Defect

Authentication succeeded and the provider returned HTTP 200 with a complete
response body, but the strict parser rejected the page before acceptance. The
leading compatibility defect was that the exact top-level schema did not allow
the observed optional Massive.com compatibility field `count`, even when it was
redundant with `resultsCount` and the parsed result count.

## Accepted Top-Level Fields

- `ticker`
- `adjusted`
- `queryCount`
- `request_id`
- `resultsCount`
- `status`
- `results`
- `next_url`
- optional compatibility metadata: `count`

Unknown top-level fields remain rejected.

## Count Compatibility

- `count` is optional.
- `count` must be an exact nonnegative integer; bool, string, and float are
  rejected.
- When present, `count` must equal `resultsCount` and `len(results)`.
- `count` is validated as compatibility metadata only.
- `count` is excluded from normalized OHLCV, Strategy, and the canonical
  semantic market-data projection after consistency validation.

## Aggregate Row Fields

Required:

- `t`
- `o`
- `h`
- `l`
- `c`
- `v`

Optional:

- `vw`
- `n`
- `otc`

`otc` must be an exact boolean when present. String and integer values are
rejected. `otc` is validated as provider compatibility evidence only and does
not enter the current analytical OHLCV artifact or Strategy semantics.

Unknown aggregate-row fields remain rejected.

## Sanitized Diagnostics

Schema failures persist bounded structural diagnostics on the rejected attempt
record only:

- sorted top-level field names;
- sorted aggregate-row field-name sets;
- missing required field names;
- unexpected field names;
- fixed JSON type-mismatch categories;
- row index for aggregate-row schema failures.

Diagnostics do not persist response values, OHLCV values, `request_id` values,
`next_url` values, cursor values, API keys, authorization headers, raw response
bodies, raw URLs, or raw exception text. Diagnostic field names are passed
through a strict bounded ASCII identifier policy.

## Status Mapping

- First-page HTTP-200 schema rejection:
  `MONTH_ACQUISITION_RESPONSE_SCHEMA_FAILED`.
- Zero accepted pages before pagination:
  `PAGINATION_NOT_STARTED`.
- Smoke-level provider schema rejection:
  `SMOKE_PROVIDER_RESPONSE_REJECTED`.
- Fixed finding:
  `RESPONSE_SCHEMA_INVALID`.

`SMOKE_INVALID` remains reserved for malformed internal state or contract
failure. Schema rejection is not classified as credential rejection, transport
timeout, or pagination-chain failure.

## Artifact Behavior

Invalid responses are not accepted raw pages. The correction preserves:

- no raw provider page for rejected schema responses;
- no completeness manifest;
- no normalized artifact;
- no canonical eligibility;
- no registry eligibility.

No second live request occurred during this correction. No live provider request
was made during this correction.
