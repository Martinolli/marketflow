# MarketFlow Historical Data Artifact Lineage Status

## Decision

Status: PASS FOR OFFLINE SYNTHETIC ARTIFACT-LINEAGE MECHANICS.

Branch: `feature/swing-historical-data-artifact-lineage`.

Base commit: `d86846a37ef1ab582719ec539429af9b4a1f46d6`.

No commit or tag is authorized for this task.

## Scope

Implemented:

- historical artifact manifest schema
  `marketflow.historical_data_artifact_manifest.v1`;
- runtime root `.marketflow/historical_data/runs/`;
- canonical JSON payload serialization;
- safe relative manifest and payload references;
- no-overwrite atomic writes;
- saved lineage validation through explicit manifest refs;
- calendar candidate artifacts;
- normalized synthetic 15-minute OHLCV artifacts;
- dividend-event set artifacts;
- derived SWING and POSITION_SWING profile artifacts;
- analytical segment-map artifacts;
- sanitized pipeline receipt artifacts;
- optional dry CLI synthetic pipeline self-check;
- focused tests and source-assurance checks.

Excluded:

- provider executor;
- Massive/Polygon calls;
- actual calendar freeze;
- real data normalization;
- canonical dataset creation;
- registry approval;
- normal runtime migration;
- annotation, candidate generation, Monte Carlo, outcomes, performance,
  broker integration, or execution.

## Artifact Schema And Runtime Root

Schema:

```text
marketflow.historical_data_artifact_manifest.v1
```

Runtime root:

```text
.marketflow/historical_data/runs/
```

Tests use pytest temporary directories. Manifests store relative refs only.

## Atomic-Write Contract

The writer creates payload temp files and manifest temp files in the target
filesystem, flushes and closes them, installs payloads without replacement,
then installs manifests last. Saved validation reloads manifests and payloads
from disk before returning receipts.

Confirmed failure states:

- payload without manifest: incomplete;
- manifest without payload: invalid;
- digest mismatch: invalid;
- size mismatch: invalid;
- collision: rejected;
- temporary files: ignored.

## Artifact Results

Calendar candidate:

- writes `CALENDAR_SCHEDULE_CANDIDATE`;
- retains requested MIC, requested calendar token, resolved calendar, alias,
  `exchange_calendars` version, tzdata version, fixed range, official evidence
  identity/digest, session schedule digest, and calendar status;
- does not claim frozen or authoritative status.

Normalized source:

- writes `NORMALIZED_15M_OHLCV`;
- serializes start-stamped 15-minute source windows in chronological order;
- stores Decimal values as strings;
- requires explicit `SYNTHETIC_OFFLINE_FIXTURE` provenance in this phase.

Dividend-event set:

- writes `DIVIDEND_EVENT_SET`;
- stores deterministic event IDs and ex-dividend dates;
- uses explicit synthetic offline evidence only.

Derived profile artifacts:

- write `DERIVED_SWING_RTH_HALF_SESSION_195M` and
  `DERIVED_POSITION_SWING_RTH_FULL_SESSION_1D`;
- call the accepted RTH bar engine;
- keep calendar candidate and normalized source as exact multi-input lineage;
- retain early-close and extended-hours findings;
- block complete-success status on incomplete ordinary sessions.

Segment maps:

- write `ANALYTICAL_SEGMENT_MAP`;
- call the accepted segmentation engine;
- bind one derived profile artifact and one dividend-event set;
- retain deterministic segment IDs, fixed start reasons, deferred early-close
  boundaries, and prefix-safety behavior.

Pipeline receipt:

- writes `HISTORICAL_PIPELINE_RECEIPT`;
- reports sanitized statuses and artifact receipts;
- excludes OHLCV values and absolute paths.

## Dry CLI

Command:

```text
env\Scripts\python.exe -m marketflow.historical_data --pipeline-self-check
```

The command uses an embedded deterministic synthetic fixture and an
automatically removed temporary run root. It accepts no ticker and writes no
canonical runtime dataset or report.

## No-Network Evidence

Source assurance verifies no provider import, credential/environment read,
candidate/MC/outcome import, Streamlit, LLM, real market-data root scan,
latest/first artifact selection, duplicate aggregation formula outside the
accepted engine, score blending, registry authority, or runtime migration path
was added.

## Tests

Focused historical artifact suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_artifacts.py -q
```

Current result: 19 passed.

Focused historical artifact, calendar/bar-engine regression, Contract
regression, source-assurance, packaging, operational Artifact Lineage v1, and
prior-integrity suite:

```text
env\Scripts\python.exe -m pytest tests\test_historical_data_artifacts.py tests\test_historical_data_engine.py tests\test_acquisition_contract_v2_1.py tests\test_acquisition_contract_v2.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py tests\test_artifact_lineage_v1.py -q
```

Current result: 131 passed.

Full collection:

```text
env\Scripts\python.exe -m pytest --collect-only -q
```

Current result: 715 collected.

Full default suite:

```text
env\Scripts\python.exe -m pytest -q
```

Current result: 715 passed.

The test count increased from 696 to 715 because this task adds 19 focused
historical-data artifact-lineage tests.

## Pip, Compile, And Diff Checks

`pip check`: pass.

Compileall with warnings as errors:

```text
env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: pass.

`git diff --check`: pass.

Warnings:

- Git reported LF-to-CRLF working-copy normalization warnings for
  `marketflow/historical_data/__init__.py` and
  `marketflow/historical_data/__main__.py`.
- No pytest or compile warning summary was emitted.

## Git Status Evidence

Pre-full-suite Git status:

```text
## feature/swing-historical-data-artifact-lineage
 M marketflow/historical_data/__init__.py
 M marketflow/historical_data/__main__.py
?? docs/architecture/MARKETFLOW_HISTORICAL_DATA_ARTIFACTS.md
?? docs/plans/MARKETFLOW_HISTORICAL_DATA_ARTIFACT_LINEAGE_PLAN.md
?? docs/status/MARKETFLOW_HISTORICAL_DATA_ARTIFACT_LINEAGE_STATUS.md
?? marketflow/historical_data/artifacts.py
?? marketflow/historical_data/pipeline.py
?? tests/test_historical_data_artifacts.py
```

Post-full-suite Git status matched the same intended source, docs, and test
changes. No generated data, reports, registry state, cache, credentials, or
runtime artifacts were added.

## Reviewer Findings

Reviewer A:

```text
MEDIUM - segment-map creation accepted a calendar context manifest without
proving it was the same calendar candidate bound into the derived profile
artifact.
```

Disposition: fixed. Segment-map creation now rejects calendar-artifact and
calendar-digest mismatches, with focused regression coverage.

Reviewer B:

```text
MEDIUM - pipeline receipts could include raw HistoricalArtifactError text in
fixed_findings on blocked or partial paths.
```

Disposition: fixed. Pipeline findings now use fixed status codes only, with
focused coverage proving raw exception text is not emitted.

## Blockers

No implementation blocker is currently known.

## Remaining Limitations

- All exercised data is synthetic.
- No actual calendar is operator-frozen.
- No provider executor exists.
- No canonical dataset exists.
- No registry approval exists.
- Normal runtime migration remains pending.
- Research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.
