# MarketFlow Live-Month RTH Source Root Correction

UTC correction date: `2026-08-02T13:57:58Z`.

Status: `LIVE_MONTH_RTH_SOURCE_SMOKE_ROOT_CORRECTED`.

## Finding

Final acceptance found that the diagnostic output root was repository-derived,
but fixed source-smoke evidence lookup still used a current-working-directory
relative root:

```text
.marketflow/provider_smoke/runs/
```

That meant a non-CLI caller could change the process current working directory
and cause public source validation or a confirmed local run to look for the
accepted smoke evidence outside the repository.

## Correction

Production source-evidence lookup now derives the source-smoke root from the
same validated repository root used for diagnostic output:

```text
repository_root = Path(__file__).resolve().parents[2]
source_smoke_root = <repository_root>/.marketflow/provider_smoke/runs/
diagnostic_output_root = <repository_root>/.marketflow/rth_derivation_smoke/runs/
```

The repository root is derived from the source module path, not from
`Path.cwd()`, CLI arguments, environment variables, configuration, timestamps,
or latest-folder discovery. It is validated against fixed repository evidence
before either production root is returned. Failure to establish the root fails
closed with `REPOSITORY_ROOT_UNRESOLVED`.

The source-smoke root must remain beneath the validated repository root. The
private test seam may still accept explicit temporary source and output roots
for deterministic pytest fixtures, but that seam is leading-private, validates
paths, is not package-exported, is not CLI-accessible, and cannot alter the
fixed diagnostic specification.

## Non-Regression Boundary

This correction does not change:

- diagnostic schema or specification digest;
- fixed source smoke run ID or receipt SHA-256;
- normalized artifact IDs or semantic digests;
- requested `XNAS` identity or resolved `XNYS` schedule;
- calendar status or authority;
- source import and timestamp validation;
- RTH slot validation;
- SWING aggregation;
- POSITION_SWING aggregation;
- receipt sanitization or authority flags.

The diagnostic remains noncanonical evidence only. Calendar freeze,
canonical eligibility, registry eligibility, Strategy use, performance use,
acquisition, and runtime migration remain disabled.

## CWD Independence

Focused tests now change the process current working directory to an unrelated
temporary directory and prove that:

- plan generation remains identical;
- production source-smoke root resolves to the repository smoke root;
- production output root resolves to the repository diagnostic root;
- accepted source evidence is located from the repository;
- a shadow temporary `.marketflow` source tree is not read;
- no diagnostic output tree is created beneath the unrelated current working
  directory;
- diagnostic digest remains unchanged.

## Evidence

Checks completed before this document was written:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
40 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
275 passed

env\Scripts\python.exe -m pytest --collect-only -q
914 tests collected

env\Scripts\python.exe -m pytest -q
914 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with LF-to-CRLF working-copy normalization warnings on modified Python files
```

Focused diagnostic coverage increased from `38` to `40` tests, and the full
collected suite increased from `912` to `914` tests. The increase is from the
new CWD-independence and shadow `.marketflow` source-root regressions.

## Repeat Derivation

The confirmation-gated local derivation was repeated after this correction
from an unrelated current working directory:

```text
diagnostic_run_id = rthdiag-7a792f9043004f7598a7f478ac64c4c6
diagnostic_receipt_sha256 = d2e97da8dda76d835e04a4b24eb683c8ba262bcde7491bb6f1746d4f605fad97
diagnostic_status = LIVE_MONTH_RTH_DERIVATION_COMPLETE
```

The repeated run validated that source evidence was read from the repository
source-smoke root, output was written only beneath the repository diagnostic
runtime root, and no shadow `.marketflow` tree was created beneath the
unrelated current working directory.

## Remaining Limitation

This correction remains noncanonical local evidence only. It does not freeze a
calendar, approve a canonical dataset, grant registry authority, or establish
predictive usefulness or profitability.

No provider was contacted. No API key, credential, provider account, billing
data, provider portal, raw provider body, raw request URL, request ID, OHLCV
value, audit value, candidate score, account data, trade data, outcome, or
performance result was inspected. No commit or tag was created.

## Final Acceptance

The confirmation-gated local derivation was later repeated after the bounded
corrections through raw-page ancestry reconciliation. The corrected receipt was
validated against run `rthdiag-6236cb56914b466eb8d62585a3c9dada` and
receipt SHA-256
`af20626756a0873656b7c59c932f937ef7fdd8c36ab931271375600873d12936`.
Final acceptance is separately blocked until the post-payload-path-containment
local derivation is repeated.
