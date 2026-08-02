# MarketFlow Live-Month RTH Run-ID Determinism Correction

UTC correction date: `2026-08-02T14:39:38Z`.

Status: `LIVE_MONTH_RTH_RUN_ID_DETERMINISM_CORRECTED`.

## Finding

Final acceptance found that production diagnostic run-ID generation could
self-reject nondeterministically. The generator created one random UUID-based
candidate and immediately validated it against source-defined forbidden
fragments, including:

```text
2025
```

A random 32-character UUID hexadecimal token can rarely contain that fragment.
The candidate is still random and opaque, but the single-candidate algorithm
could terminate a confirmed local run and make the focused one-sample run-ID
test flaky.

The defect was reproduced before correction by forcing the first generated
candidate to contain `2025`; generation terminated with a sanitized opaque-ID
validation error instead of trying another candidate.

## Correction

Run-ID generation now uses bounded rejection sampling:

```text
MAX_DIAGNOSTIC_RUN_ID_GENERATION_ATTEMPTS = 32
```

Each candidate must match the production format:

```text
rthdiag-[0-9a-f]{32}
```

The existing case-insensitive forbidden-fragment policy remains in force. A
candidate that is malformed or contains a forbidden fragment is rejected and
the generator tries another UUID-based candidate, up to the fixed bound.

If every bounded candidate is rejected, generation fails closed with:

```text
DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED
```

No invalid candidate is returned. No unbounded loop, timestamp fallback,
context-derived ID, current-working-directory dependency, environment
override, CLI override, or caller-selected public run ID was added.

## Public Boundary

The public entrypoint remains:

```text
run_local_diagnostic(confirmation: str)
```

It accepts no run ID, run-ID factory, UUID factory, candidate factory, runtime
root, output root, source-smoke root, repository root, ticker, month, MIC, or
calendar override.

Deterministic candidate sequences are available only through a leading-private
generator seam used by focused tests. The private seam is not exported by
`marketflow.historical_data.__init__` and is not CLI-accessible.

Run-directory collision behavior is unchanged: directory creation remains
atomic/no-replace and existing run directories are not overwritten.

## Non-Regression Boundary

This correction does not change:

- diagnostic schema or specification digest;
- fixed source smoke run ID or receipt SHA-256;
- normalized artifact IDs or semantic digests;
- repository-derived source and output roots;
- requested `XNAS` identity or resolved `XNYS` schedule;
- calendar status or authority;
- source import and timestamp validation;
- RTH slot validation;
- SWING aggregation;
- POSITION_SWING aggregation;
- receipt sanitization or authority flags.

The diagnostic remains noncanonical local evidence only. Calendar freeze,
canonical eligibility, registry eligibility, Strategy use, performance use,
acquisition, and runtime migration remain disabled.

## Evidence

Checks completed before this document was written:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
46 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
281 passed

env\Scripts\python.exe -m pytest --collect-only -q
920 tests collected

env\Scripts\python.exe -m pytest -q
920 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with LF-to-CRLF working-copy normalization warnings on modified Python files
```

Focused diagnostic coverage increased from `40` to `46` tests. The increase is
from deterministic run-ID generation coverage for forbidden-fragment retry,
multiple rejected candidates, malformed candidate retry, safe first candidate,
bounded exhaustion without runtime output, and sanitized private factory
failure without runtime output.

The full collected suite increased from `914` to `920` tests.

## Reviewer Findings

Read-only reviewer A found that private candidate-factory failure could leak a
raw exception from the deterministic seam. Disposition: fixed. Candidate
factory failure now fails closed as `DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED`
before runtime directory creation.

Read-only reviewer B reported no findings and no critical/high blocker.

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
