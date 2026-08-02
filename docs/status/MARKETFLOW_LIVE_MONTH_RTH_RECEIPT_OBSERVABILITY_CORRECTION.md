# MarketFlow Live-Month RTH Receipt Observability Correction

UTC correction date: `2026-08-02T15:03:08Z`.

Status: `LIVE_MONTH_RTH_RECEIPT_OBSERVABILITY_CORRECTED`.

## Finding

The successful noncanonical live-month RTH derivation receipt reported source
row count, extended-hours exclusions, complete ordinary sessions, and derived
SWING/POSITION_SWING bar counts, but did not directly report the validated RTH
source-row count.

The accepted January 2025 evidence had already reconciled:

```text
1277 - 757 = 520
20 * 26 = 520
```

The receipt now exposes that RTH-row reconciliation directly without exposing
OHLCV values.

## Correction

The sanitized diagnostic receipt now includes:

```text
expected_rth_source_row_count
validated_rth_source_row_count
rth_source_row_reconciliation_status
```

For the accepted January 2025 evidence:

```text
expected_rth_source_row_count = 520
validated_rth_source_row_count = 520
rth_source_row_reconciliation_status = RTH_SOURCE_ROWS_RECONCILED
```

## Semantics

`expected_rth_source_row_count` is derived from the January calendar view:
ordinary full sessions multiplied by the 26 required exact RTH source slots per
session.

`validated_rth_source_row_count` is derived from session/slot validation, using
unique source starts that exactly match expected RTH slots for each ordinary
full session. It is not calculated solely as total source rows minus
extended-hours exclusions.

Fixed reconciliation statuses are:

```text
RTH_SOURCE_ROWS_RECONCILED
RTH_SOURCE_ROWS_INCOMPLETE
RTH_SOURCE_ROWS_INVALID
```

Complete diagnostic status requires reconciled RTH source rows, zero incomplete
ordinary sessions, and no duplicate, extra, or invalid RTH-slot finding.

## Sanitization

The receipt still contains counts, statuses, identities, and digests only. It
does not expose OHLCV values, raw provider bodies, API keys, authorization
headers, raw URLs, request IDs, absolute runtime paths, candidate values, or
performance values.

## Non-Regression Boundary

This correction does not change:

- diagnostic schema or specification digest;
- fixed source smoke evidence;
- normalized artifact IDs or semantic digests;
- repository-derived source and output roots;
- run-ID generation;
- confirmation ceremony;
- requested `XNAS` identity or resolved `XNYS` schedule;
- calendar status or authority;
- RTH slot validation logic;
- SWING aggregation;
- POSITION_SWING aggregation;
- derived dataset semantic digests;
- authority flags.

The diagnostic remains noncanonical local evidence only. Calendar freeze,
canonical eligibility, registry eligibility, Strategy use, performance use,
acquisition, and runtime migration remain disabled.

## Evidence

Checks completed before this document was written:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
52 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
287 passed

env\Scripts\python.exe -m pytest --collect-only -q
926 tests collected

env\Scripts\python.exe -m pytest -q
926 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with LF-to-CRLF working-copy normalization warnings on modified Python files
```

Focused diagnostic coverage increased from `46` to `52` tests. The increase
covers complete 520/520 receipt reporting, accepted January evidence
non-regression, one missing exact RTH slot, extended-hours non-inflation,
duplicate-slot non-inflation, and extra-slot non-inflation.

The full collected suite increased from `920` to `926` tests.

## Repeat-Derivation Disposition

This task changed production source, so the previous confirmation-gated local
derivation receipt was pre-correction evidence. The local derivation was later
repeated after the bounded corrections through raw-page ancestry reconciliation
from the fixed accepted smoke evidence already on disk.

No provider was contacted. No API key, credential, provider account, billing
data, provider portal, raw provider body, raw request URL, request ID, OHLCV
value, audit value, candidate score, account data, trade data, outcome, or
performance result was inspected. No commit or tag was created.

The corrected receipt was validated against run
`rthdiag-6236cb56914b466eb8d62585a3c9dada` and receipt SHA-256
`af20626756a0873656b7c59c932f937ef7fdd8c36ab931271375600873d12936`.
Final acceptance is separately blocked until the post-payload-path-containment
local derivation is repeated.
