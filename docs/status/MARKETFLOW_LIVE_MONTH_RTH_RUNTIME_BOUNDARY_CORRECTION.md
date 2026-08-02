# MarketFlow Live-Month RTH Runtime Boundary Correction

UTC correction date: `2026-08-02T12:41:56Z`.

Status: `LIVE_MONTH_RTH_RUNTIME_AND_AUTHORIZATION_DISPLAY_CORRECTED`.

## Review Finding

Final offline acceptance found that the production-facing
`run_local_diagnostic()` function still accepted caller-supplied runtime
location and run-identity controls:

```text
run_root
run_id_factory
```

Those parameters were unacceptable because the confirmation-gated diagnostic
is a production local-run entrypoint. Allowing a caller to choose the output
root or run ID could write outside the fixed ignored diagnostic runtime
boundary after valid confirmation and could create non-opaque operator-chosen
runtime identities.

## Correction

The public entrypoint is now sealed:

```text
run_local_diagnostic(confirmation: str)
```

It resolves the source-defined repository runtime root internally:

```text
.marketflow/rth_derivation_smoke/runs/
```

It also generates an internal opaque run ID, validates it before directory
creation, and uses no-replace run-directory creation. The production root is
derived from the source/repository path, not from the current working
directory, CLI arguments, environment variables, configuration, user-home
defaults, modification time, or latest-folder discovery.

## Authorization Display Correction

A follow-up offline authorization-display review found that the public live
command printed only:

```text
Type confirmation phrase:
```

It did not first display the exact digest-bound phrase the operator must enter.
That made the confirmation ceremony incomplete unless the operator guessed or
inspected source code.

The live command now prints, in order:

1. the complete sanitized fixed diagnostic plan;
2. the noncanonical classification and warning;
3. the diagnostic specification digest;
4. the digest prefix;
5. the exact required operator confirmation phrase;
6. the interactive input prompt.

The plan command and live command use the same authoritative confirmation
details derived from the immutable diagnostic specification digest:

```text
diagnostic_specification_digest = d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257
diagnostic_specification_digest_prefix = d5bcaedb8414
required_confirmation_phrase = RUN MARKETFLOW LIVE MONTH RTH d5bcaedb8414
```

The phrase is not secret. It contains no runtime path, API key, credential,
market value, provider body, or account data.

## Private Test Seam

A leading-private implementation seam remains available for deterministic
tests only:

```text
_run_local_diagnostic_core(..., smoke_root, run_root, run_id_factory)
```

The seam is not exported through `marketflow.historical_data.__init__`, is not
referenced by the CLI, and still validates runtime roots and run IDs. It cannot
alter the fixed diagnostic specification or the fixed source smoke evidence.
The synthetic self-check continues to use only temporary automatically removed
artifacts and writes no persistent diagnostic output.

## Non-Regression Boundary

This correction does not change analytical semantics:

- diagnostic schema and specification digest remain unchanged;
- source smoke run, receipt hash, artifact IDs, and semantic digests remain
  unchanged;
- Massive.com business identity remains the provider identity in evidence;
- XNAS diagnostic identity and XNYS calendar resolution remain unchanged;
- RTH slot validation and SWING/POSITION_SWING aggregation remain delegated to
  the accepted bar engine;
- canonical, registry, Strategy, performance, acquisition, and runtime
  migration flags remain false.

## Evidence

Checks completed before this document was written:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
35 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
38 passed after the authorization-display correction

env\Scripts\python.exe -m pytest --collect-only -q
912 tests collected after the authorization-display correction

env\Scripts\python.exe -m pytest -q
912 passed after the authorization-display correction

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass after the authorization-display correction

git diff --check
pass after the authorization-display correction with LF-to-CRLF working-copy normalization warnings on modified text files

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
270 passed

env\Scripts\python.exe -m pytest --collect-only -q
909 tests collected

env\Scripts\python.exe -m pytest -q
909 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with LF-to-CRLF working-copy normalization warnings on modified text files
```

Test-count change from the prior accepted baseline is `+5`, from the added
runtime-boundary regressions in `tests/test_live_month_rth_diagnostic.py`.
The authorization-display correction adds `+3` focused tests, bringing the
focused diagnostic file to `38` tests and the full collected suite to `912`
tests.

Post-correction production-source hashes:

```text
marketflow/historical_data/__init__.py
837a82ac59e15b7614dc69725c92e89d4dc53f8ef1e5ca895690ce7716ea3d45

marketflow/historical_data/__main__.py
96c41694cf9a28ed27c6b213711045a8f745b10b6e9c7ebb290a3157b462a41c

marketflow/historical_data/live_month_rth_diagnostic.py
42d5aa9bdd6552e02847a7cc99d1791522368796274283cdf125ecd6cf1fc824
```

Post-display-correction production-source hashes:

```text
marketflow/historical_data/__init__.py
837a82ac59e15b7614dc69725c92e89d4dc53f8ef1e5ca895690ce7716ea3d45

marketflow/historical_data/__main__.py
d5d9d97e33f91cd43d87cf254ebc676ed7c5c6b98455de5b6d62a42c428dc718

marketflow/historical_data/live_month_rth_diagnostic.py
08e4e56af2aa707c6c6440d1ec4f78266ce40c181b520fab7c4518b18db19e35
```

## Remaining Limitation

The previous confirmation-gated local derivation receipt was produced before
these production-source corrections. The command was cancelled before
confirmation during the authorization-display review, so no local derivation
was performed during that correction. The local derivation was later repeated
after all bounded corrections from the fixed accepted smoke evidence already
on disk.

No provider was contacted. No API key, provider account, billing data, provider
portal, raw provider body, raw request URL, request ID, OHLCV value, audit
value, candidate score, account data, trade data, outcome, or performance
result was inspected. No commit or tag was created.

## Follow-Up Acceptance Attempt

UTC follow-up date: `2026-08-02T13:46:17Z`.

The corrected confirmation-gated local derivation receipt was later validated
by hash and sanitized metadata during final acceptance. That acceptance
remained blocked because source-smoke evidence lookup was current-working-
directory relative in production source. A later source-root correction derived
the fixed input evidence root from the validated repository root. The
confirmation-gated local derivation was then repeated successfully from an
unrelated current working directory, producing receipt SHA-256
`d2e97da8dda76d835e04a4b24eb683c8ba262bcde7491bb6f1746d4f605fad97`.

## Final Acceptance

The confirmation-gated local derivation was later repeated after the bounded
corrections through raw-page ancestry reconciliation. The corrected receipt was
validated against run `rthdiag-6236cb56914b466eb8d62585a3c9dada` and
receipt SHA-256
`af20626756a0873656b7c59c932f937ef7fdd8c36ab931271375600873d12936`.
Final acceptance is separately blocked until the post-payload-path-containment
local derivation is repeated.
