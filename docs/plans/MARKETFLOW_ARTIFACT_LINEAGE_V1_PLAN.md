# MarketFlow Artifact Lineage v1 Plan

Status: PASS

Date: 2026-07-31

Branch: `feature/swing-artifact-lineage-v1`

Base commit: `e005d216245bf5d6f42e31ae878de46a418db984`

## Mission

Implement first-class immutable provenance for newly produced operational
artifacts in the accepted MarketFlow operational workflows. Preserve the
accepted read-side controls and Strategy semantic-integrity boundaries.

## Existing Read-Side Contract

Accepted read-side controls already prohibit lineage inference from filename,
modification time, newest file, first file, ticker-only match, timeframe-only
match, directory order, or report-folder scanning. Downstream selection must use
exact identity, parent, ticker, timeframe, run, workflow, and stage metadata and
fail closed on zero or multiple matches.

## Writer-Side Gap

Current operational writers still produce timestamped or legacy files without
complete immutable manifest metadata at creation time. Artifact Lineage v1 must
make the producing side write identity, payload digest, source digest, and exact
parent/input relationships before those artifacts can be treated as canonical.

## Run Identity

- Run IDs are opaque and collision resistant.
- Run IDs are not based solely on timestamps, ticker, account, operator, or
  file path.
- UTC creation time is stored separately.
- ID generation is injectable for deterministic tests.
- Run directory creation fails if it already exists.
- Downstream canonical stages reuse one run ID and never silently start another
  run.

## Artifact Identity

- Artifact IDs are opaque and collision resistant.
- Artifact IDs are unique within a run and stage.
- Artifact IDs are never ticker, timestamp, account, operator, or path values.
- Artifact ID generation is injectable for deterministic tests.
- Artifact identity is separate from payload filename.

## Manifest Schema

Version: `marketflow.artifact_manifest.v1`.

Required groups:

- identity: schema version, artifact ID, run ID, stage, artifact type, workflow
  type;
- market/profile: ticker, analysis profile, timeframe;
- source: source dataset identity, source dataset digest, safe source reference;
- software/configuration: code commit, StrategyConfig digest, candidate-core
  digest, manual-scenario digest as applicable;
- lineage: primary parent artifact ID and exact declared input artifact IDs;
- payload: safe payload reference, SHA-256, byte size, media/type;
- time: timezone-aware UTC creation timestamp.

Fixed enums are required for stage, artifact type, workflow type, analysis
profile, and payload type. Unknown schema versions fail closed.

## Payload Digest

Every committed payload records SHA-256 over the exact payload bytes and byte
size. JSON payloads use deterministic UTF-8 serialization where the writer owns
the payload. CSV and HTML payload digests cover the exact bytes written without
injecting metadata rows or modifying analytical content.

## Source Dataset Digest

Annotated dataset artifacts record the payload SHA-256 as both payload digest
and source dataset digest. Derived artifacts copy the exact upstream source
dataset digest. Legacy sources without an exact manifest are not silently
promoted to canonical lineage.

## Parent And Input Relationships

- Self-parent is rejected.
- Duplicate input IDs are rejected.
- Detectable parent cycles are rejected.
- Same-run, same-workflow, ticker/timeframe/profile, source-digest, and allowed
  stage transition checks are enforced.
- Multi-input plot artifacts declare both analysis data and MC evidence inputs.

## Workflow A Lineage

Canonical chain:

```text
ANNOTATED_DATASET
  -> MANUAL_SCENARIO_DEFINITION
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

Manual scenario artifacts contain explicit entry, stop, target, horizon,
ticker, timeframe, profile, scenario origin, parent annotated-dataset artifact,
and manual-scenario digest. They have no candidate-core digest and claim no
Strategy rank eligibility.

## Workflow B Lineage

Canonical chain:

```text
ANNOTATED_DATASET
  -> CANDIDATE_CORE
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

Candidate artifacts contain the accepted canonical candidate core,
candidate-core digest, StrategyConfig digest, parent annotated-dataset artifact,
and exact ticker/timeframe/profile. Only complete, calibrated, rank/action
eligible candidates can proceed to canonical MC.

## Atomic Write Contract

The writer commits payload then manifest with fail-closed recovery:

1. create final run/stage directory without overwrite;
2. write payload to an opaque temp file in the same directory;
3. flush and close payload;
4. digest payload bytes and size;
5. write manifest to an opaque temp file;
6. flush and close manifest;
7. install final payload only if no destination exists;
8. install final manifest last only if no destination exists;
9. manifest presence is the commit marker;
10. return a sanitized immutable artifact receipt.

No writer may replace an existing artifact destination.

## Collision Behavior

Run directory, payload destination, and manifest destination collisions fail
with fixed errors. Timestamp collision cannot overwrite another artifact.
Manual and canonical workflow artifacts use separate identity metadata and
cannot overwrite or satisfy each other.

## Incomplete-Artifact Recovery

- Payload without manifest: incomplete and not selectable.
- Manifest without payload: invalid.
- Digest mismatch: invalid.
- Size mismatch: invalid.
- Temp file present: incomplete and ignored.
- Unknown manifest version: invalid.
- Orphaned child: invalid or recovery-review only.

No automatic repair may scan for plausible parents.

## Legacy Report Treatment

Existing `.marketflow/reports` files remain `LEGACY_UNVERSIONED_ARTIFACTS`.
They are not rewritten, deleted, migrated, backfilled, or made canonical
parents by timestamp or filename. They may be viewed through explicit legacy
tools only.

## CLI Handoff

Add minimum explicit canonical lineage modes only:

- batch lineage mode starts or receives one run identity and writes annotated
  dataset artifacts;
- strategy lineage mode accepts exact annotated-dataset manifest input and
  writes candidate-core artifacts;
- manual MC lineage mode accepts exact annotated-dataset manifest input and
  explicit geometry, writes manual scenario, then MC summary;
- canonical MC lineage mode accepts exact candidate artifact and no geometry
  override;
- plot lineage mode accepts exact analysis and MC artifacts and writes plot
  artifact.

Legacy commands remain labelled and must not silently fall back from canonical
mode.

## Tests

Focused tests will cover identity generation, safe paths, atomic commit,
collision refusal, crash-state recovery, digest and size validation, Workflow A
and B lineage, manual/canonical mixing rejection, MC geometry preservation, plot
ancestry, sanitized CLI receipts, source assurance, and prior integrity
non-regression.

## Exclusions

Do not change source identity, candidate builder semantics, phase/event logic,
event recency, True Range, entry, stop, target, RR, evidence availability,
score, ranking thresholds, MC mathematics, PnF mathematics, Eigen/PCA, outcome
evaluation, provider behavior, broker/execution behavior, research protocol
values, timeframe calibration, or ticker-only UI.

## Stop Conditions

Stop blocked if branch/base/tree are wrong; a dependency changes; a network or
provider call completes; any canonical writer can overwrite an existing
artifact; timestamp-only identity remains; incomplete payload/manifest states
can be selected; Workflow A can masquerade as Workflow B; canonical MC accepts
geometry overrides; plot can mix unrelated artifacts; canonical mode falls back
to legacy; historical reports are rewritten; previous integrity milestones
regress; tests fail; or a critical/high reviewer finding remains unresolved.
