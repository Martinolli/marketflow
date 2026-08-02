# MarketFlow Live-Month RTH Payload-Path Containment Correction

UTC correction date: `2026-08-02T18:03:38Z`.

Status: `LIVE_MONTH_RTH_PAYLOAD_PATH_CONTAINMENT_CORRECTED_REPEAT_DERIVATION_REQUIRED`.

## Finding

Final acceptance Reviewer A found that source-evidence payload references were
lexically checked but then used without rejecting symbolic links, junctions,
Windows reparse points, or proving that the strictly resolved physical file
remained beneath the trusted source root.

The affected diagnostic paths were normalized monthly payload reads and
raw-page payload metadata checks. The concern was not the textual reference
format alone; a lexically safe reference such as `normalized/payload.json`
could still resolve through filesystem indirection to an untrusted file.

## Reproduction

Before the correction, a deterministic synthetic saved-artifact chain replaced
the normalized OHLCV payload file with a symlink to a byte-identical file
outside the trusted source root. The manifest still contained a lexically safe
relative `payload_ref`, and current validation accepted the source evidence:

```text
accepted_symlink_payload = true
rows = 520
payload_is_symlink = true
resolved_inside_source_root = false
```

After the correction, the same case fails closed:

```text
rejected_symlink_payload = true
finding = SOURCE_EVIDENCE_SYMLINK_REJECTED
payload_is_symlink = true
resolved_inside_source_root = false
```

## Correction

The diagnostic now uses one private authoritative helper for source-evidence
files:

```text
_validate_source_evidence_file(source_root, relative_ref, expected_kind=...)
```

The helper is used for the smoke receipt, normalized monthly manifests and
payloads, month-completeness manifests and payloads, declared raw-page
manifests, and raw-page payload files inspected only for bounded metadata.

It preserves the existing safe-relative lexical rules and adds physical
validation:

- source root must exist and be a directory;
- source root components must not be symlinks or reparse points;
- every component from the trusted source root through the final file is
  inspected with `lstat`;
- symlinks are rejected even when they resolve inside the source root;
- Windows reparse points are rejected by file attributes where available;
- strict resolution must stay beneath the trusted source root;
- final object must be a regular file;
- string-prefix containment checks are not used.

For files that are read, validation happens before open, and file identity
metadata is checked before and after the read. Any detectable identity change
fails closed as `SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED`.

Raw-page payload bodies remain unread. The diagnostic validates raw-page
payload path containment and byte-size metadata without opening or parsing raw
provider content.

## Failure Categories

The correction uses fixed sanitized path-failure categories:

```text
SOURCE_EVIDENCE_PATH_INVALID
SOURCE_EVIDENCE_PATH_OUTSIDE_ROOT
SOURCE_EVIDENCE_REPARSE_POINT_REJECTED
SOURCE_EVIDENCE_SYMLINK_REJECTED
SOURCE_EVIDENCE_NOT_REGULAR_FILE
SOURCE_EVIDENCE_FILE_IDENTITY_CHANGED
```

Public diagnostic receipts map these to the existing invalid source-evidence
status and do not include absolute paths, symlink targets, raw exceptions,
provider bodies, URLs, request IDs, API keys, OHLCV values, or performance
values.

## Non-Regression Boundary

This correction does not change:

- diagnostic schema or specification digest;
- fixed source smoke run ID or receipt digest;
- normalized artifact IDs or semantic digests;
- raw-page accepted ID/SHA ancestry reconciliation;
- requested `XNAS` and resolved `XNYS` behavior;
- calendar status or authority;
- source row import semantics;
- RTH slot validation;
- SWING/POSITION formulas;
- receipt sanitization;
- run-ID generation;
- confirmation ceremony;
- authority flags.

Expected analytical evidence remains:

```text
source rows = 1277
extended-hours excluded = 757
expected RTH rows = 520
validated RTH rows = 520
rth_source_row_reconciliation_status = RTH_SOURCE_ROWS_RECONCILED
full sessions = 20
incomplete sessions = 0
SWING bars = 40
POSITION_SWING bars = 20
```

## Evidence

Focused evidence after the correction:

```text
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

The focused diagnostic file increased from `65` to `84` tests. The added
coverage includes contained regular files, final symlink to outside root,
final symlink to inside root, intermediate-directory symlink, deterministic
reparse metadata, root-prefix confusion, directory payload rejection,
nonregular metadata rejection, source-root symlink rejection, manifest symlink
rejection, raw-page payload symlink rejection without reading raw body,
file-identity change rejection, opened-file identity mismatch rejection before
read, post-open path-indirection rejection before read, disappearing-path fixed
category mapping, fail-closed ordering before import/calendar/RTH, no runtime
artifact on path failure, and sanitized public path-failure receipts.

The full collected suite increased from `939` to `958` tests.

## Remaining Limitation

This task changes production source. The corrected confirmation-gated local
derivation must be repeated after this correction before final acceptance and
local commit can be reconsidered. No provider request is required for that
repeat because it consumes fixed accepted smoke evidence already on disk.

No provider was contacted. No API key, credential, provider account, billing
data, provider portal, raw provider body, raw request URL, request ID, OHLCV
value, audit value, candidate score, account data, trade data, outcome,
performance result, Strategy, Monte Carlo, broker, execution, registry
authority, report rewrite, runtime migration, commit, or tag was created.
