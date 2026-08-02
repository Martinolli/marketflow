# MarketFlow Live-Month RTH Raw-Page Ancestry Correction

UTC correction date: `2026-08-02T16:47:29Z`.

Status: `LIVE_MONTH_RTH_RAW_PAGE_ANCESTRY_CORRECTED`.

## Finding

Final acceptance Reviewer A found that source-evidence validation checked raw
input-manifest count, raw manifest schema/type/run metadata, raw payload
existence, and raw payload byte size, but did not reconcile the month
completeness payload's ordered `accepted_pages` entries to the exact declared
`RAW_PROVIDER_PAGE` manifests.

The missing checks were:

```text
accepted_pages[*].raw_page_artifact_id == raw_page_manifest.artifact_id
accepted_pages[*].raw_page_sha256 == raw_page_manifest.payload_sha256
```

Before the correction, deterministic synthetic evidence proved that altering
either accepted-page metadata field did not make source-evidence validation
fail.

## Correction

Raw-page ancestry validation now walks only the completeness manifest's ordered
declared input refs and input artifact IDs. It reconciles each entry with the
same-position accepted page and requires:

- exact raw-page artifact ID equality;
- exact raw-page payload SHA-256 equality;
- accepted-page count equals declared raw input count;
- page ordinal order matches the declared input order;
- accepted raw-page artifact IDs are unique;
- declared raw input refs and artifact IDs are unique;
- raw-page artifact type is `RAW_PROVIDER_PAGE`;
- raw-page manifest run ID matches the fixed smoke run;
- contract and request identity fields match the completeness artifact.

No directory scan, filename order, modification time, first, latest, or neighbor
raw-page fallback is used.

## Failure Behavior

Raw-page ancestry defects raise fixed sanitized findings:

```text
SOURCE_RAW_PAGE_ANCESTRY_INVALID
RAW_PAGE_ARTIFACT_ID_MISMATCH
RAW_PAGE_PAYLOAD_DIGEST_MISMATCH
RAW_PAGE_ANCESTRY_COUNT_MISMATCH
RAW_PAGE_ANCESTRY_ORDER_MISMATCH
RAW_PAGE_ANCESTRY_DUPLICATE
RAW_PAGE_MANIFEST_MISSING
RAW_PAGE_INPUT_UNDECLARED
```

The public diagnostic maps detailed ancestry failures to
`SOURCE_RAW_PAGE_ANCESTRY_INVALID`. Ancestry failure stops before normalized
OHLCV import, calendar generation, RTH derivation, SWING/POSITION output, or
diagnostic runtime artifact creation.

## Raw-Body Boundary

The correction does not parse, display, or persist raw provider-body content.
It reconciles completeness payload metadata to already validated raw-page
manifest metadata and continues to avoid raw URLs, next URLs, request IDs, API
keys, Authorization headers, OHLCV values, absolute paths, and performance
values in diagnostic output.

## Non-Regression Boundary

This correction does not change diagnostic schema or specification digest,
source smoke run ID or receipt digest, month completeness artifact ID,
normalized artifact IDs or semantic digests, requested `XNAS` and resolved
`XNYS` behavior, calendar status or authority, source row import, RTH slot
validation, SWING/POSITION aggregation, explicit `520 / 520 /
RTH_SOURCE_ROWS_RECONCILED` row reconciliation, authority flags, public
signature, repository roots, run-ID generation, or confirmation ceremony.

## Evidence

Reproduction before production change:

```text
env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py::test_raw_page_accepted_page_artifact_id_mismatch_rejected_before_derivation tests/test_live_month_rth_diagnostic.py::test_raw_page_accepted_page_payload_sha_mismatch_rejected
2 failed: DID NOT RAISE
```

Post-correction focused evidence:

```text
env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py -k raw_page
13 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
65 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
300 passed

env\Scripts\python.exe -m pytest --collect-only -q
939 tests collected

env\Scripts\python.exe -m pytest -q
939 passed
```

Focused diagnostic coverage increased from `52` to `65` tests. The `13` added
tests cover matching accepted-page metadata, artifact-ID mismatch, payload-SHA
mismatch, missing manifest, directory-neighbor non-substitution, count
mismatch, duplicate accepted raw-page ID, order mismatch, cross-run rejection,
cross-month/request rejection, no diagnostic runtime artifact on ancestry
failure, local-run writer suppression for ancestry failure, and source
assurance for declared-input validation.

Reviewer B found that cross-run raw-page ancestry was rejected through a
generic run-mismatch message rather than the public raw-page ancestry failure
category. Disposition: fixed. Cross-run declared raw manifests now raise a
fixed raw-page ancestry category before generic manifest validation, and the
public diagnostic maps that failure to `SOURCE_RAW_PAGE_ANCESTRY_INVALID`.

## Repeat-Derivation Disposition

This task changed production source, so the confirmation-gated local
derivation was repeated after this correction before final acceptance and local
commit. The repeat consumed fixed accepted smoke evidence already on disk.

No provider was contacted. No API key, credential, provider account, billing
data, provider portal, raw provider body, raw request URL, request ID, OHLCV
value, audit value, candidate score, account data, trade data, outcome,
performance result, Strategy, Monte Carlo, broker, execution, registry
authority, report rewrite, runtime migration, commit, or tag was created.

The corrected receipt was validated against run
`rthdiag-6236cb56914b466eb8d62585a3c9dada` and receipt SHA-256
`af20626756a0873656b7c59c932f937ef7fdd8c36ab931271375600873d12936`.
Final acceptance is separately blocked until the post-payload-path-containment
local derivation is repeated.
