# MarketFlow Historical Data Artifact Lineage Plan

## Status

Plan status: IMPLEMENTATION IN PROGRESS.

Branch: `feature/swing-historical-data-artifact-lineage`.

Starting commit: `d86846a37ef1ab582719ec539429af9b4a1f46d6`.

## Scope

This phase binds the accepted frozen-calendar and deterministic RTH bar engine
to immutable, digest-bound historical-data artifacts. It remains offline and
synthetic-only.

In scope:

- separate historical-data manifest schema;
- canonical JSON payloads;
- safe relative payload and manifest references;
- no-overwrite atomic writes;
- saved lineage validation from disk;
- calendar candidate, normalized 15-minute source, dividend-event set, derived
  profile, segment-map, and pipeline-receipt artifacts;
- a narrow offline pipeline orchestrator;
- a dry synthetic self-check;
- focused pytest coverage and source assurance.

Out of scope:

- provider execution;
- Massive/Polygon calls;
- operator calendar freeze;
- canonical dataset approval;
- registry authority;
- normal ticker-only runtime migration;
- Strategy candidates, annotation, Monte Carlo, outcomes, performance analysis,
  broker integration, or execution.

## Schema Boundary

Historical artifacts use:

```text
marketflow.historical_data_artifact_manifest.v1
```

The existing operational Artifact Lineage v1 schema remains unchanged. The
historical schema records explicit safe manifest references for declared
parents and inputs so saved validation does not infer parentage by filename,
directory, timestamp, first match, or latest match.

## Runtime Root

The source-defined runtime root is:

```text
.marketflow/historical_data/runs/
```

Tests use pytest temporary directories. Manifests store safe relative
references only.

## Implementation Steps

1. Add historical artifact constants, canonical serialization, run creation,
   safe path validation, atomic writers, manifest loading, and saved chain
   validation.
2. Add writers for calendar candidates, normalized 15-minute OHLCV, dividend
   event sets, derived profile datasets, analytical segment maps, and pipeline
   receipts.
3. Add a narrow pipeline module that writes one offline run and derives `SWING`
   and `POSITION_SWING` independently through the accepted engine.
4. Extend the dry CLI with a sanitized synthetic pipeline self-check that uses
   an automatically removed temporary run root.
5. Add focused tests covering manifest/path safety, atomic writes, artifact
   types, multi-input lineage, segmentation, pipeline receipts, dry CLI, and
   source-assurance boundaries.
6. Run focused and full offline validation with no commit or tag.

## Acceptance Boundary

Acceptance in this phase means deterministic artifact-lineage mechanics are
implemented and tested with synthetic data. It does not mean provider data was
used, a calendar was operator-frozen, a canonical dataset exists, registry
approval exists, normal runtime migration occurred, or predictive usefulness or
profitability was accepted.
