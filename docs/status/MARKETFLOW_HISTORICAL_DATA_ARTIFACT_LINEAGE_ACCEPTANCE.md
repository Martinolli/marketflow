# MarketFlow Historical Data Artifact Lineage Acceptance

## Decision

HISTORICAL-DATA ARTIFACT LINEAGE PIPELINE: PASS FOR SYNTHETIC OFFLINE
PROCESSING MECHANICS.

UTC acceptance date: `2026-08-01T17:26:33Z`.

Branch: `feature/swing-historical-data-artifact-lineage`.

Base commit: `d86846a37ef1ab582719ec539429af9b4a1f46d6`.

No Git tag was created. No push was performed. The configured remote was not
altered.

## Scope And Exclusions

Accepted scope:

- separate historical-data artifact manifest schema;
- immutable canonical JSON historical-data artifacts;
- opaque offline processing run identity;
- safe relative payload and manifest references;
- no-overwrite atomic writers;
- saved-disk manifest and payload validation;
- exact multi-input parent validation;
- calendar candidate artifact;
- normalized synthetic 15-minute OHLCV artifact;
- dividend-event set artifact;
- `SWING` and `POSITION_SWING` derived profile artifacts;
- analytical segment-map artifacts;
- sanitized pipeline receipt artifact;
- dry synthetic pipeline self-check;
- focused deterministic tests and source assurance.

Excluded scope:

- provider calls or provider executor;
- Massive/Polygon acquisition;
- real market-data normalization;
- operator calendar freeze;
- canonical dataset approval;
- registry or quarantine authority;
- annotation;
- Strategy candidate generation;
- Monte Carlo;
- outcome evaluation;
- performance analysis;
- broker integration;
- execution capability;
- normal ticker-only runtime migration.

## Artifact Schema

Historical-data artifact schema:

```text
marketflow.historical_data_artifact_manifest.v1
```

This schema is separate from operational Artifact Lineage v1:

```text
marketflow.artifact_manifest.v1
```

The operational schema was not extended, weakened, or reinterpreted.

The historical schema validates exact required fields, fixed artifact types,
fixed stages, immutable run and artifact IDs, UTC creation timestamps, Contract
v2 and v2.1 digests, processing-engine version, safe relative payload
references, payload SHA-256, payload byte size, semantic payload digest,
primary parent IDs, ordered additional input IDs, explicit manifest refs, and
lineage IDs.

Unknown fields, unknown schema versions, duplicate inputs, self-parent,
self-input, cross-run inputs, wrong stages, wrong types, and wrong Contract
digests fail closed.

## Runtime Root And Path Security

Source-defined runtime root:

```text
.marketflow/historical_data/runs/
```

Tests inject pytest temporary roots only. Manifests store safe relative
references and no absolute paths.

Path validation rejects traversal, absolute references, UNC-style references,
Windows device names, ADS-style references, backslashes, NUL bytes, trailing
space/dot components, root-prefix confusion, symlink payloads, non-regular
payloads, run/stage mismatches, and cross-run lineage.

No generated pipeline run, generated calendar artifact, runtime dataset,
report, cache, credential, provider response, registry state, quarantine state,
or absolute user-home path is part of the source changes.

## Atomic Writer

The writer sequence is:

1. create payload temporary file in the target filesystem;
2. write, flush, and close payload bytes;
3. compute exact payload byte size and SHA-256;
4. create manifest temporary file in the target filesystem;
5. write, flush, and close manifest bytes;
6. install the final payload without replacing an existing file;
7. install the final manifest last;
8. reload saved manifest and payload from disk;
9. validate saved lineage before returning the receipt.

No silent overwrite or replace-existing fallback exists. Payload-only state is
incomplete. Manifest-only state is invalid. Digest and size mismatches fail.
Temporary files are not selectable artifacts. Writer failure removes only the
payload from that failed attempt when the manifest was not committed.

## Saved Lineage Validation

Readers validate saved evidence from disk. They do not trust in-memory parent
objects as proof of lineage.

Saved validation checks manifest schema, payload existence, regular-file
status, payload digest, payload size, run/stage/type, Contract digests,
parent/input manifest refs, parent/input payloads, lineage IDs, allowed
transitions, profile consistency, calendar consistency, and source consistency.

No filename-only relationship, first-match fallback, latest fallback, folder
scan, or manual filename selection is used.

## Payload And Digest Rules

Payloads are deterministic UTF-8 canonical JSON with recursively sorted keys,
stable separators, UTC ISO timestamps, exact Decimal strings, deterministic row
ordering, no NaN, no Infinity, no binary-float conversion, no credentials, and
no absolute paths.

The implementation distinguishes exact payload byte SHA-256 from semantic
payload digest. Generated timestamps are excluded from semantic payload
digests.

## Artifact Type Inventory

Implemented fixed artifact types:

- `CALENDAR_SCHEDULE_CANDIDATE`;
- `NORMALIZED_15M_OHLCV`;
- `DIVIDEND_EVENT_SET`;
- `DERIVED_SWING_RTH_HALF_SESSION_195M`;
- `DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D`;
- `ANALYTICAL_SEGMENT_MAP`;
- `HISTORICAL_PIPELINE_RECEIPT`.

The calendar artifact type is not labelled `FROZEN`, `APPROVED`,
`CANONICAL`, or `AUTHORITATIVE`.

## Calendar Candidate

`CALENDAR_SCHEDULE_CANDIDATE` records requested MIC, requested calendar token,
resolved calendar, Contract v2.1 digest, `exchange_calendars` version, tzdata
version, fixed date range, official evidence identity/digest, session schedule
digest, source timezone, canonical timezone, and non-authoritative calendar
status.

The calendar remains pending later official-evidence review and operator
freeze. No freeze ceremony is implemented or claimed.

## Normalized 15-Minute Source

`NORMALIZED_15M_OHLCV` accepts only validated `SourceBar` objects from the
accepted bar engine. It serializes exact start-stamped `window_start_utc`,
`window_end_utc`, open, high, low, close, and volume fields.

Rows are deterministic and chronological. Duplicate windows, floats,
non-finite values, and invalid source bars fail closed.

Synthetic test and self-check data is explicitly labelled:

```text
SYNTHETIC_OFFLINE_FIXTURE
```

It is not labelled provider-acquired or Massive/Polygon-acquired.

## Dividend Event Set

`DIVIDEND_EVENT_SET` stores explicit offline evidence only: deterministic
event IDs, ex-dividend dates, evidence classification, and event-set semantic
digest.

No provider call, return calculation, performance calculation, dividend-price
adjustment, or corporate-action acquisition path exists in this task.

## Derived Profile Artifacts

`DERIVED_SWING_RTH_HALF_SESSION_195M` and
`DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D` call the accepted RTH bar engine.
They do not duplicate aggregation formulas.

Both artifacts bind exact calendar and normalized-source artifacts in the same
run, preserve Contract v2.1, expose exact canonical profile and bar type,
preserve derived bar digests, retain early-close and extended-hours findings,
and keep incomplete ordinary sessions from becoming complete-success claims.

SWING and POSITION_SWING remain independent. They do not borrow bars, profile
identity, calendar relationships, derived digests, or segment state.

## Multi-Input Lineage

Derived profile artifacts require role-bound inputs:

- primary parent: `NORMALIZED_15M_OHLCV`;
- additional input: `CALENDAR_SCHEDULE_CANDIDATE`.

Analytical segment maps require:

- primary parent: exact derived profile artifact;
- additional input: exact `DIVIDEND_EVENT_SET`.

Duplicate input IDs, wrong run, wrong Contract digest, wrong artifact type,
wrong stage, wrong profile, wrong calendar artifact, wrong calendar digest,
and cross-profile segment input are rejected.

Reviewer correction retained:

```text
The segment map calendar context must match the derived artifact's exact bound
calendar artifact and calendar digest.
```

## Analytical Segment Maps

`ANALYTICAL_SEGMENT_MAP` invokes the accepted segmentation engine and writes
one map per profile.

It preserves deterministic segment IDs/digests, fixed start reasons
`DATASET_START` and `EX_DIVIDEND_CONTINUITY_RESET`, normal-session resets,
early-close/closed-date deferral to the next eligible canonical bar,
same-date event ID retention, immutable derived bars, no prior-segment leakage,
and no future-row leakage.

## Pipeline Behavior

The offline orchestrator performs:

1. opaque run creation;
2. calendar candidate write;
3. normalized 15-minute source write;
4. dividend-event set write;
5. independent SWING derivation;
6. independent POSITION_SWING derivation;
7. profile artifact writes;
8. profile segment-map writes;
9. sanitized pipeline receipt write.

One profile failure does not roll back a valid other profile. The pipeline
does not borrow across profiles, blend scores, build candidates, call a
provider, approve registry state, or migrate runtime behavior.

Fixed pipeline statuses:

- `PIPELINE_COMPLETED`;
- `PIPELINE_PARTIAL`;
- `PIPELINE_BLOCKED`;
- `PIPELINE_INVALID`.

Receipts include run ID, Contract v2.1 digest, safe artifact receipts,
calendar status, normalized-source status, profile derivation statuses,
segment-map statuses, and fixed findings. Receipts exclude OHLCV values,
absolute paths, account/trade data, candidate scores, performance results, and
raw exception strings.

## Dry CLI

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data --pipeline-self-check
```

The self-check uses a deterministic synthetic fixture and an automatically
removed temporary run root. It prints sanitized output, accepts no ticker,
accepts no source path, calls no provider, reads no credential, opens no
network path, writes no persistent generated dataset, modifies no report, runs
no Strategy/MC/outcome code, and performs no normal runtime migration.

## Contract And Runtime Non-Regression

Contract v1 digest:

```text
29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
```

Contract v2 digest:

```text
59958593a6667b74f90c55d0f40debb63a9c5ac10fe4f2aa7255345a5996c2c0
```

Contract v2.1 digest:

```text
538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6
```

The accepted frozen-calendar/RTH bar-engine formulas and timestamp semantics
remain unchanged.

Normal runtime remains:

```text
LEGACY_FIXED_PROFILE_RUNTIME_PENDING_V2_MIGRATION
```

`marketflow normal <ticker>` was not changed. No current runtime resolver
consumes the new historical-data artifacts.

## Tests

Focused artifact-lineage suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_artifacts.py -q
```

Result: 19 passed.

Focused artifact-lineage, pipeline, frozen-engine regression, Contract
regression, source-assurance, packaging, operational Artifact Lineage v1, and
prior-integrity suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_artifacts.py tests\test_historical_data_engine.py tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py tests\test_artifact_lineage_v1.py -q
```

Result before final staging: 131 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Result before final staging: 715 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Result before final staging: 715 passed.

The full test count increased from 696 to 715 because this task adds 19
focused historical-data artifact-lineage tests.

## Pip, Compile, And Diff Checks

`pip check`: pass.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result before final staging: pass.

`git diff --check`: pass with Git LF-to-CRLF working-copy normalization
warnings on modified text files.

## Warnings

No pytest warning summary was emitted.

No compile warning was emitted.

Git reported LF-to-CRLF working-copy normalization warnings for modified and
new text files.

## No-Network Evidence

Source assurance covers:

- no provider import;
- no credential or environment read;
- no candidate, Monte Carlo, or outcome import;
- no Streamlit or LLM import;
- no real market-data-root scan;
- no latest/first artifact selection;
- no duplicate aggregation formula outside the accepted engine;
- no score blending;
- no registry-authority implementation;
- no runtime migration.

Default tests remained deterministic and offline. No provider/network/manual
check was run.

## Git Status Evidence

Pre-test intended dirty set:

```text
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
?? docs/architecture/MARKETFLOW_HISTORICAL_DATA_ARTIFACTS.md
?? docs/plans/MARKETFLOW_HISTORICAL_DATA_ARTIFACT_LINEAGE_PLAN.md
?? docs/status/MARKETFLOW_HISTORICAL_DATA_ARTIFACT_LINEAGE_STATUS.md
?? marketflow/historical_data/artifacts.py
?? marketflow/historical_data/pipeline.py
?? tests/test_historical_data_artifacts.py
```

The final acceptance evidence file is added by this acceptance task.

No generated run, dataset, report, cache, credential, provider response,
registry state, or quarantine state is staged or committed.

## Reviewer Findings

Reviewer A:

```text
MEDIUM - segment-map creation accepted a calendar context manifest without
proving it was the same calendar candidate bound into the derived profile
artifact.
```

Disposition: fixed. Segment-map creation rejects calendar-artifact and
calendar-digest mismatches, with focused regression coverage.

Reviewer B:

```text
MEDIUM - pipeline receipts could include raw HistoricalArtifactError text in
fixed_findings on blocked or partial paths.
```

Disposition: fixed. Pipeline receipts now emit fixed finding codes only, with
focused regression coverage.

No critical or high reviewer finding remains.

## Remaining Limitations

- Historical-data artifact-lineage mechanics are accepted for synthetic
  offline processing only.
- No provider data was used.
- No calendar is operator-frozen.
- No acquisition executor exists.
- No canonical dataset exists.
- No registry approval exists.
- Normal runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Next Phase

Future work may introduce canonical v2.1 dataset generation, operator calendar
freeze, registry approval, and runtime integration only through separate
acceptance.
