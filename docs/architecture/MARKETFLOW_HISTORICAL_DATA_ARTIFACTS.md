# MarketFlow Historical Data Artifacts

## Status

Architecture status: IMPLEMENTED FOR OFFLINE SYNTHETIC ARTIFACT LINEAGE.

The implementation is isolated under:

```text
marketflow/historical_data/
```

It does not implement provider execution, operator calendar freeze, canonical
dataset approval, registry authority, Strategy candidate generation,
annotation, Monte Carlo, outcome evaluation, performance analysis, broker
integration, execution, or normal runtime migration.

## Manifest Schema

Historical-data artifacts use a separate manifest schema:

```text
marketflow.historical_data_artifact_manifest.v1
```

The existing operational Artifact Lineage v1 schema is not extended or
reinterpreted.

Required manifest fields include identity, Contract digests, processing-engine
version, market/profile context, explicit parent and input manifest references,
payload reference, byte digest, byte size, media type, and semantic payload
digest.

## Runtime Root

The source-defined historical runtime root is:

```text
.marketflow/historical_data/runs/
```

Tests use pytest temporary directories. Manifests store safe relative
references only. Absolute paths, traversal, UNC/device names, ADS-style refs,
backslashes, symlink escapes, non-regular files, and overwrite attempts fail
closed.

## Atomic Writes

The writer commits immutable artifacts by:

1. writing payload bytes to a temporary file in the target filesystem;
2. flushing and closing the payload;
3. computing SHA-256 and byte size;
4. writing a temporary manifest;
5. installing the final payload without replacement;
6. installing the final manifest last;
7. reloading and validating the saved manifest chain from disk.

Payload-only files are incomplete. Manifest-only files are invalid. Digest or
size mismatches are invalid. Temporary files are not selectable artifacts.

## Artifact Types

Fixed historical artifact types:

- `CALENDAR_SCHEDULE_CANDIDATE`;
- `NORMALIZED_15M_OHLCV`;
- `DIVIDEND_EVENT_SET`;
- `DERIVED_SWING_RTH_HALF_SESSION_195M`;
- `DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D`;
- `ANALYTICAL_SEGMENT_MAP`;
- `HISTORICAL_PIPELINE_RECEIPT`.

Calendar artifacts are candidates only. They do not claim frozen or
authoritative status.

## Payload Format

Payloads are deterministic UTF-8 canonical JSON:

- recursively sorted object keys;
- stable separators;
- no NaN or Infinity;
- no binary floats;
- Decimal values as canonical strings;
- timestamps as UTC ISO strings;
- deterministic list ordering.

Semantic payload digests exclude generated timestamps. Exact payload bytes also
receive a separate SHA-256.

## Lineage

Derived profile artifacts declare:

- primary parent: `NORMALIZED_15M_OHLCV`;
- additional input: `CALENDAR_SCHEDULE_CANDIDATE`.

Segment maps declare:

- primary parent: one derived profile artifact;
- additional input: `DIVIDEND_EVENT_SET`.

Saved validation loads the exact declared manifest refs from disk. It does not
infer parentage by filename, folder scan, timestamp, first match, or latest
match. Wrong run, wrong Contract digest, duplicate inputs, self-parent,
wrong type, wrong profile, wrong calendar/source relationship, and
cross-profile segment maps fail closed.

## Pipeline

The offline pipeline creates one opaque run, writes a calendar candidate,
normalized synthetic 15-minute source, dividend-event set, separate SWING and
POSITION_SWING derived artifacts, segment maps, and a sanitized pipeline
receipt.

The pipeline calls the accepted RTH bar engine and segmentation engine. It does
not duplicate aggregation formulas, borrow fields across profiles, blend
scores, build candidates, run Monte Carlo, call providers, or migrate the
normal runtime.

## Receipt Boundary

Pipeline receipts include run ID, Contract digest, sanitized artifact receipts,
calendar/source/profile/segment statuses, and findings.

Receipts exclude OHLCV values, absolute paths, account/trade information,
candidate scores, performance results, and outcomes.

## Acceptance Boundary

This architecture may be accepted only for offline deterministic artifact
mechanics. All exercised data is synthetic. No actual calendar is
operator-frozen. No provider executor exists. No canonical dataset exists. No
registry approval exists. Normal runtime migration remains pending. The
research protocol remains blocked. Predictive usefulness and profitability
remain unaccepted.
