# MarketFlow Ticker Event Response Identity Fields Correction

Status: PASS, LIVE SUPPORTING EVIDENCE ACCEPTED

Date: `2026-08-03`

## Correction

The first Ticker Events Supporting Audit v1 implementation accepted only
`events` and `name` inside the provider `results` object. A controlled live
observation showed that Massive.com may also return `cik` and `composite_figi`
with the same result shape.

The correction accepts only those two additional observed fields. Arbitrary
unknown result fields still fail closed.

## Identity Semantics

`composite_figi` is optional. When returned, it must be exact text, pass strict
FIGI validation, and match the fixed query/source Composite FIGI
`BBG000B9XRY4`. A mismatch is an identity conflict.

`cik` is optional. When returned, it must be exact decimal text and match the
accepted start/end source identity CIK evidence when that evidence is present.
No integer, float, boolean, or malformed CIK coercion is accepted. Public
receipts retain only CIK status values and do not expose the CIK value.

`name` remains optional provider text. It is excluded from authority, receipts,
stitching, and digest-bearing identity decisions.

## Failure Observability

If a future live raw response is persisted and then rejected by parsing, the run
also writes a sanitized `TICKER_EVENT_AUDIT_RECEIPT` failure artifact. The
failure receipt contains fixed run/spec/request-count/stage/category/field-name
metadata, endpoint stability, raw-artifact-written status, and false authority
flags only.

Failure receipts exclude raw provider body, request ID value, URL,
Authorization header, API key, provider name text, CIK value, raw exception
text, absolute paths, account data, prices, and performance values.

## Current Evidence State

The correction is offline. It does not rewrite the saved failed runtime
evidence and does not contact a provider during acceptance.

The corrected parser was later accepted against the saved controlled live run.
The returned ticker-change event was classified as before-range historical
context, with zero in-range events.

No automatic stitching, canonical identity, registry eligibility,
identity-freeze eligibility, Strategy authority, Monte Carlo, outcome,
performance, broker, execution, or runtime migration authority is created.
