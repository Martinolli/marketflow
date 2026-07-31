# MarketFlow Artifact Lineage v1

Status: PASS

## Boundary

Artifact Lineage v1 is the writer-side companion to the accepted operational
read-side controls. It applies only to newly produced canonical operational
artifacts under `.marketflow/reports/runs/`. Historical files under
`.marketflow/reports` remain `LEGACY_UNVERSIONED_ARTIFACTS`.

## Runtime Root

Canonical artifacts are written below:

```text
.marketflow/reports/runs/<run_id>/<stage>/<artifact_id>.<ext>
.marketflow/reports/runs/<run_id>/<stage>/<artifact_id>.<ext>.manifest.json
```

`run_id` and `artifact_id` are opaque path-safe IDs. Ticker, timeframe,
timestamp, account, operator, and filename are not authoritative identity.

## Manifest Schema

Schema version: `marketflow.artifact_manifest.v1`.

Required manifest fields:

- `schema_version`
- `artifact_id`
- `run_id`
- `stage`
- `artifact_type`
- `workflow_type`
- `ticker`
- `analysis_profile`
- `timeframe`
- `source_dataset_identity`
- `source_dataset_digest`
- `source_ref`
- `code_commit`
- `strategy_config_digest`
- `candidate_core_digest`
- `manual_scenario_digest`
- `parent_artifact_id`
- `input_artifact_ids`
- `lineage_artifact_ids`
- `payload_ref`
- `payload_sha256`
- `payload_byte_size`
- `payload_type`
- `created_at`

Fixed values are used for workflow, stage, artifact type, analysis profile, and
payload type. Unknown schema versions fail closed.

## Atomic Commit

The canonical writer writes a payload temp file, closes and fsyncs it, computes
payload SHA-256 and byte size, writes a manifest temp file, closes and fsyncs
it, installs the final payload without replacing an existing file, and installs
the final manifest last. Manifest presence is the commit marker.

Failure states:

- payload without manifest: incomplete;
- manifest without payload: invalid;
- digest mismatch: invalid;
- size mismatch: invalid;
- temp file present: ignored;
- unknown manifest schema: invalid.

No recovery path scans for plausible parents.

## Writer Inventory

`scripts/marketflow_batch_analysis.py`

- Legacy writes: timestamp batch directory, TVM namespace, batch CSV summary.
- Canonical v1 writes: `ANNOTATED_DATASET` artifacts for exact requested
  `--lineage-timeframes` after batch analysis completes.
- Overwrite behavior: canonical run directory and artifact destinations fail on
  collision.
- Structured identity: canonical mode prints sanitized receipts.

`marketflow/marketflow_strategy.py`

- Legacy reads: report-root/date-glob or explicit legacy `--batch latest`.
- Legacy writes: timestamped Strategy candidate JSON under
  `.marketflow/reports/strategy_data`.
- Canonical v1 reads: exact `ANNOTATED_DATASET` manifest only.
- Canonical v1 writes: `CANDIDATE_CORE` artifact with candidate-core digest and
  StrategyConfig digest.
- No report-folder scan occurs in canonical mode.

`marketflow/marketflow_monte_carlo_trade.py`

- Legacy reads: positional CSV and explicit geometry.
- Legacy writes: timestamped MC summary JSON and optional HTML plots beside the
  CSV.
- Manual canonical mode reads: exact `ANNOTATED_DATASET` manifest plus explicit
  entry/stop/target/horizon; writes `MANUAL_SCENARIO_DEFINITION` then
  `MONTE_CARLO_SUMMARY`.
- Strategy canonical mode reads: exact `CANDIDATE_CORE` manifest; accepts no
  geometry overrides; writes `MONTE_CARLO_SUMMARY`.
- Canonical mode disables legacy MC plot/json writers and commits the summary
  through the manifest writer.

`scripts/plot_annotated_features.py`

- Legacy reads: positional CSV and optional explicit `--mc-summary`.
- Legacy writes: timestamped plot HTML and PnF sidecar JSON.
- Canonical v1 reads: exact `ANNOTATED_DATASET` and exact MC manifests.
- Canonical v1 writes: `ANNOTATED_PLOT` artifact and validates same run,
  workflow, ticker, timeframe, profile, source digest, and MC ancestry.

`marketflow/marketflow_analysis.py`, `marketflow/marketflow_utils.py`,
`marketflow/batch_utils.py`, and Studio/service report helpers remain legacy
unless they invoke the explicit canonical helpers added above.

## Workflow A

Canonical manual scenario chain:

```text
ANNOTATED_DATASET
  -> MANUAL_SCENARIO_DEFINITION
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

The manual scenario digest covers workflow type, scenario origin, ticker,
timeframe, profile, entry, stop, target, horizon, parent artifact ID, and
source dataset digest. It is not a candidate-core digest and carries no rank
eligibility claim.

## Workflow B

Canonical strategy chain:

```text
ANNOTATED_DATASET
  -> CANDIDATE_CORE
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

The candidate-core artifact contains the accepted canonical candidate core,
candidate-core digest, StrategyConfig digest, eligibility metadata, and parent
annotated-dataset artifact. It does not store the full mutable Strategy result
as the candidate-core payload. Canonical MC reads geometry from the candidate
only and rejects operator overrides.

## Validation

Manifest validation checks schema, IDs, fixed enum values, safe refs, payload
existence, regular-file status, payload size, payload SHA-256, run/stage
directory consistency, self-parent, duplicate inputs, and self-input. Child
lineage checks enforce allowed workflow stage transitions, same run, same
workflow, ticker/timeframe/profile consistency, and source digest consistency.
Saved manifest-chain validation reconstructs declared parents and inputs from
the run directory; `lineage_artifact_ids` alone is never accepted as proof of
ancestry.

## Legacy Isolation

Legacy commands remain available and labelled by mode. Canonical modes require
manifest inputs and do not fall back to legacy scans or historical reports.
Historical reports are not rewritten, migrated, deleted, or made canonical
parents by timestamp or filename.

## Non-Authority Boundaries

Streamlit remains an optional viewer. LLM paths remain narrative or
legacy/experimental and cannot satisfy canonical candidate or MC inputs.
Provider, broker, execution, outcome, and profitability paths are unchanged.
