# MarketFlow Live-Month RTH Derivation Acceptance

UTC acceptance date: `2026-08-02T18:41:13Z`.

Status: `PASS`.

## Decision

PASS for local acceptance and local commit authorization of the noncanonical
live-month RTH derivation diagnostic.

The accepted production source is the exact source that produced the latest
confirmation-gated local derivation after all bounded corrections, including
runtime-root sealing, repository-derived source/output roots, CWD independence,
shadow-runtime rejection, visible digest-bound confirmation, bounded run-ID
generation, direct RTH source-row reconciliation, raw-page ID/SHA ancestry
reconciliation, and physical payload-path containment.

This final acceptance did not execute the diagnostic again. It validated the
saved sanitized receipt by SHA-256 and metadata, reviewed source/test/docs,
ran the required offline suites, and recomputed frozen production hashes. The
subsequent staging and commit steps must include only the accepted
source/test/documentation files and must not stage `.marketflow` evidence.

No provider was contacted. No API key, credential, provider account, billing
data, provider portal, raw provider-page body, raw request URL, request ID
value, OHLCV value, audit-field value, candidate value, performance result,
account data, or trade data was inspected.

No tag was created. No push was performed. The remote was not altered.

## Repository State

- Repository: `marketflow`.
- Branch: `feature/swing-live-month-rth-derivation-diagnostic`.
- Base commit: `94d299c5608125b31266dd2d4fce5b9edc6664bb`.
- Python: `env\Scripts\python.exe`, `Python 3.12.10`.
- Diagnostic schema: `marketflow.live_month_rth_diagnostic.v1`.
- Diagnostic specification digest:
  `d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257`.

## Production-Source Freeze

Production-source hashes were recorded before acceptance work and must remain
byte-identical after documentation, tests, staging, and commit:

```text
marketflow/historical_data/__init__.py
837a82ac59e15b7614dc69725c92e89d4dc53f8ef1e5ca895690ce7716ea3d45

marketflow/historical_data/__main__.py
d5d9d97e33f91cd43d87cf254ebc676ed7c5c6b98455de5b6d62a42c428dc718

marketflow/historical_data/live_month_rth_diagnostic.py
8976e470a72934058bb2b08e5238b9c699b6ee5c35d89b2c4f0e8f2c9208f018
```

## Latest Corrected Receipt

Latest corrected local derivation evidence:

```text
diagnostic_run_id = rthdiag-aa3b306b21f040a3832ff8bf20aaad6b
diagnostic_receipt_sha256 = a0c7c1216d769910362952c2de799dfadd2272d80a01499c12a17ff453c28b87
diagnostic_status = LIVE_MONTH_RTH_DERIVATION_COMPLETE
source_evidence_status = LIVE_MONTH_SOURCE_EVIDENCE_VALID
```

The sanitized receipt reports:

```text
source_row_count = 1277
source_rows_inspected = 1277
extended_hours_rows_excluded = 757
expected_rth_source_row_count = 520
validated_rth_source_row_count = 520
rth_source_row_reconciliation_status = RTH_SOURCE_ROWS_RECONCILED
complete_ordinary_session_count = 20
incomplete_ordinary_session_count = 0
early_close_exclusion_count = 0
closed_or_session_absent_count = 11
swing_produced_bar_count = 40
position_swing_produced_bar_count = 20
```

Derived digests:

```text
january_session_view_digest = 2ef9b599399ddb5b00d689a1267f4e702523ac1513cbfbddabe7e9254e995325
parent_calendar_candidate_digest = 6cf9f2b15b398b1dd9877ee12a769d2f92f8555a84abf4f61bd528d296d40734
swing_dataset_semantic_digest = 48b97d83b737e2a591d2145e3b9a0395d08578cad57ec98f1b7f35d007bb72f0
position_swing_dataset_semantic_digest = 1f43aa14824892a13d45c6c124e78a997d8c4cd3e24933ba6c16922bc41324c7
```

## Source Smoke Evidence

Accepted source smoke evidence:

```text
smoke_run_id = smoke-c3388f68530c4131a090a895953e3d89
smoke_receipt_sha256 = 70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f
classification = NONCANONICAL_PROVIDER_SMOKE
provenance = LIVE_PROVIDER_SMOKE_NONCANONICAL
provider_identity = MASSIVE.COM
ticker = AAPL
month = 2025-01
pagination_status = PAGINATION_EXHAUSTED
retrieval_completeness = PROVIDER_RETRIEVAL_COMPLETE
total_normalized_row_count = 1277
```

Normalized artifacts:

```text
month_completeness_artifact_id = month-art-0004-month-chunk-completeness-manifest
ohlcv_artifact_id = month-art-0005-month-normalized-15m-ohlcv
ohlcv_semantic_digest = 24e83b9eea95c9e7ba662123f6edac220de9fb64e9cbb4225ee76d60bcb1230e
audit_artifact_id = month-art-0006-month-normalized-aggregate-audit-fields
audit_semantic_digest = 3099ffab37579b20cb3dfdcb5c1e2741ce00cbf7f05fb8a4e135e9dcb421f9cd
```

Validation confirms manifest schema, payload hashes, payload byte sizes,
semantic digests, run identity, exact parent ancestry, row-count equality,
timestamp-order equality, and one audit row per normalized row. Raw provider
page bodies are not read. Audit values are not used analytically. Source rows
are not sorted, filled, repaired, or synthesized.

## Payload-Path Containment

The trusted source root is repository-derived:

```text
<repo>/.marketflow/provider_smoke/runs/
```

Every manifest-referenced source-evidence file goes through one authoritative
private validator. The validator preserves lexical safe-relative-reference
rules, rejects absolute/traversal/UNC/device/ADS/URL/control-character forms,
uses no string-prefix containment shortcut, inspects path components with
`lstat`, rejects symbolic links, junctions and reparse points, requires strict
resolved containment under the trusted source root, and requires the final
object to be a regular file.

For source files that are read, validation completes before open, the opened
handle identity is compared before read, the path is rechecked for indirection
before read, and identity is checked again after read. Raw-page payload paths
are validated for path and size metadata only; raw provider bodies remain
unread.

All source-evidence path failures map to sanitized public source-evidence
failures without physical paths, link targets, raw exceptions, URLs, request
IDs, credentials, or market values.

## Raw-Page Ancestry

The month-completeness payload's ordered `accepted_pages` evidence reconciles
exactly to the declared `RAW_PROVIDER_PAGE` manifests:

```text
accepted_page.raw_page_artifact_id == raw_page_manifest.artifact_id
accepted_page.raw_page_sha256 == raw_page_manifest.payload_sha256
accepted_page_count == declared_raw_page_manifest_count
input_artifact_id == raw_page_manifest.artifact_id
```

The accepted-page count, declared manifest-ref count, declared artifact-ID
count, page ordinal, manifest order, raw-page type, fixed smoke run ID, and
request/month identity all reconcile. Accepted raw-page IDs are unique. Every
accepted page has one declared raw-page manifest and every declared raw-page
manifest has one accepted page.

Cross-run and cross-request references fail closed through fixed sanitized
source-evidence categories. Validation occurs before normalized source import,
audit alignment, calendar generation, RTH derivation, SWING/POSITION outputs,
and diagnostic runtime artifact writing. No directory scan, filename inference,
latest/first fallback, modification-time choice, or neighbor substitution is
used.

## Public And Runtime Boundaries

The public local-run entrypoint remains:

```text
run_local_diagnostic(confirmation: str) -> dict[str, Any]
```

It accepts no repository root, source-smoke root, output root, run root, run ID,
UUID/candidate factory, manifest/payload path, artifact ID/digest, ticker,
month, MIC, or calendar override. Source-smoke and output roots are
repository-derived, current-working-directory independent, and cannot be
replaced by a shadow `.marketflow` tree. Private test seams remain
leading-private, path-validated, unexported, and CLI-inaccessible.

Run IDs are internally generated opaque `rthdiag-[0-9a-f]{32}` values with
bounded 32-attempt rejection sampling, forbidden-fragment validation, fixed
sanitized exhaustion failure, no unbounded loop, no caller factory, and
no-overwrite run-directory creation.

The plan and run commands display the complete diagnostic digest, digest
prefix, and exact confirmation phrase before the input prompt:

```text
RUN MARKETFLOW LIVE MONTH RTH d5bcaedb8414
```

Display and validation use the same authoritative builder. No runtime
directory or artifact is created before successful confirmation.

## Calendar And RTH Result

Calendar boundary:

```text
requested_primary_listing_mic = XNAS
requested_calendar_token = XNAS
resolved_calendar = XNYS
calendar_alias_relationship = XNAS_USES_XNYS_SCHEDULE
calendar_status = CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE
calendar_authority = NOT_OPERATOR_FROZEN
```

Explicit row reconciliation:

```text
20 full ordinary sessions * 26 expected RTH slots = 520 expected RTH rows
unique exact validator matches = 520 validated RTH rows
1277 total rows - 757 extended-hours exclusions = 520 RTH rows
```

No extended-hours replacement, slot repair, synthetic bar, or profile borrowing
is permitted. The accepted RTH engine is reused and SWING/POSITION_SWING
outputs remain independent.

Profile results:

```text
SWING: 20 * 2 = 40 bars
POSITION_SWING: 20 * 1 = 20 bars
```

## Noncanonical Limitations

This result does not establish provider-verified instrument identity, an
operator-frozen calendar, canonical dataset approval, predictive usefulness,
profitability, Strategy source approval, registry authority, broker capability,
execution capability, or runtime migration.

All authority flags remain false:

```text
acquisition_enabled = false
calendar_freeze_eligible = false
canonical_eligibility = false
registry_eligibility = false
strategy_enabled = false
performance_enabled = false
runtime_migration_enabled = false
```

## Test Evidence

Final required checks:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py
84 passed

env\Scripts\python.exe -m pytest -q tests/test_live_month_rth_diagnostic.py tests/test_historical_data_engine.py tests/test_historical_data_artifacts.py tests/test_fake_transport_monthly_acquisition.py tests/test_massive_one_month_smoke.py tests/test_massive_date_diagnostic.py tests/test_acquisition_contract_v2.py tests/test_acquisition_contract_v2_1.py tests/test_fixed_date_acquisition_contract.py tests/test_source_assurance.py tests/test_artifact_lineage_v1.py tests/test_packaging_integrity.py tests/test_network_guard.py
319 passed

env\Scripts\python.exe -m pytest --collect-only -q
958 tests collected

env\Scripts\python.exe -m pytest -q
958 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with LF-to-CRLF working-copy normalization warnings on modified Python files
```

The focused diagnostic file increased from `38` to `84` tests across bounded
runtime/source-root/run-ID/receipt-observability/raw-page-ancestry and
payload-path-containment corrections. The full collected suite increased from
`912` to `958` tests after those corrections.

## Reviewer Findings

Final bounded read-only Reviewer A found no remaining blocker after the
payload-path containment safe-open and taxonomy fixes. Reviewer A confirmed
post-open path indirection is rejected before read and disappearing-path
taxonomy maps to `SOURCE_EVIDENCE_PATH_INVALID`.

Final bounded read-only Reviewer B found no unresolved critical, high, or
medium issue in public/root/run-ID boundaries, confirmation ceremony,
calendar/RTH reuse, 520/520 receipt evidence, sanitization, CLI/no-network
boundaries, tests, or docs.

Earlier medium findings were corrected by sealing public local-run controls,
deriving source roots from the repository, adding bounded run-ID rejection
sampling, adding direct RTH row-count receipt observability, reconciling raw
accepted-page ID/SHA metadata to declared raw-page manifests, mapping public
raw-page ancestry failures to fixed sanitized categories, and rejecting
source-evidence payload paths that are symlinks, reparse points, nonregular
files, physically outside the trusted root, or changed during read.

## Final State

Runtime `.marketflow` output remains ignored evidence and is not source
authority. No `.marketflow` file was staged.

No provider request, credential access, download, Strategy, Monte Carlo,
outcome, performance, broker, execution, registry authority, report rewrite,
runtime migration, tag, push, or remote alteration occurred.
