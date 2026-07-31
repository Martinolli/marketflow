# MarketFlow Data Readiness Remediation Plan

## Scope

Build offline, read-only governance tooling for canonical annotated dataset
inventory, duplicate classification, history-depth analysis, registry design,
decision-register validation, and deterministic local reporting.

The tooling may inspect local dataset bytes, schema, timestamps, OHLCV values,
annotation columns, and explicit provenance metadata. It must not inspect
candidate results, outcomes, performance, account data, credentials, browser
state, providers, or unrelated repositories.

## Current Starting Evidence

Starting branch: `feature/swing-data-readiness-remediation`.

Starting commit: `07492d8496d0d897abbbc20d1e333b90ee0eca78`.

Starting tree: clean.

Baseline tag at HEAD: `v0.1.0-alpha.11-fixed-profile-orchestrator`.

Python: `env\Scripts\python.exe`, version `3.12.10`.

`pip check`: passed with `No broken requirements found.`

Read-only `.marketflow/reports` metadata inventory: 925 files.

Existing applicability scanner current result differs from the older inventory
quoted in the request:

- canonical annotated CSV files: 60;
- distinct tickers: 7;
- unique ticker/timeframe identities: to be recalculated by the new framework;
- duplicate identities: 14 under the existing scanner summary;
- timeframe file counts: `1d=17`, `1h=24`, `1w=3`, `4h=16`;
- zero split-depth-eligible `SWING` / `4h` datasets;
- zero split-depth-eligible `POSITION_SWING` / `1d` datasets.

The implementation must report the current deterministic scan, not force stale
counts.

## Non-Authority Boundary

This task does not remediate source files. It must not delete, rename, move,
overwrite, merge, truncate, reannotate, download, request, or select a
canonical source automatically.

It must not run Strategy candidates, ranking, Monte Carlo, Point-and-Figure
outcome analysis, outcome evaluation, future labels, return/R calculations,
win rate, expectancy, Sharpe/Sortino, drawdown, MFE/MAE, optimization, or
best-source selection.

## Implementation

Add `marketflow/research/data_readiness_remediation.py`.

The module will:

- discover canonical annotated CSV sources under approved local roots;
- emit safe relative references only;
- calculate exact byte digests and source metadata;
- validate OHLCV rows, timestamps, chronology, volume, schema, interval shape,
  annotation columns, explicit provenance, and explicit adjustment metadata;
- group sources by canonical ticker/timeframe identity;
- classify duplicate groups using fixed source-defined classification values;
- calculate best valid single-source rows, approved canonical safe row status,
  compatible-union potential, and profile shortfalls for fixed `SWING` and
  `POSITION_SWING` row floors;
- validate strict canonical-dataset registry examples and local decision
  registers;
- generate deterministic ignored local reports under
  `.marketflow/data_readiness/`.

The module will not be imported by the normal orchestrator. Registry
integration remains deferred until human dataset decisions are approved.

## Registry And Decision Policy

Create a strict source-controlled registry schema design document and fictional
example TOML. One identity may have at most one `APPROVED` record. Approved
records must use a safe relative source reference and must match exact file
SHA-256 before any future normal-mode use.

Create an append-oriented decision-register policy and fictional JSON example.
Changed decisions create new records; old records remain visible. Performance
rationale is prohibited.

## Reporting

The ignored report will include:

- schema version;
- code commit;
- file and identity counts;
- duplicate classifications;
- source refs and digests;
- sanitized coverage metadata;
- history shortfalls;
- unresolved decisions;
- blockers;
- semantic report SHA-256.

The semantic digest excludes the scan timestamp and uses deterministic ordering.
No absolute paths, OHLCV values, performance fields, candidate results, outcome
results, account values, or credentials appear in the report.

## Tests

Add synthetic temporary-dataset tests for:

- inventory identity parsing, safe refs, deterministic ordering, and duplicate
  count semantics;
- exact byte duplicates and same-size byte differences;
- semantically identical OHLCV with different formatting;
- same OHLCV with different annotations;
- subset, superset, compatible overlap, conflicting overlap, disjoint history,
  schema divergence, timezone conflict, and provenance conflict;
- missing columns, duplicate timestamps, non-monotonic timestamps, NaN/Infinity,
  invalid high/low geometry, invalid volume, and root escape;
- fixed row gates, best-single-source estimates, approved canonical safe row
  status, and potential-union shortfalls;
- registry duplicate approval, digest mismatch, missing file, unknown field,
  absolute/traversal rejection;
- decision-register append-only behavior, changed decision records, no deletion,
  pending/approved/rejected states, and no performance rationale;
- no-peek/source assurance: no provider, candidate-builder, Monte Carlo,
  outcome/performance imports or calls, no source dataset write/delete/move, no
  automatic canonical approval, and no normal-orchestrator integration.

## Stop Conditions

Stop blocked if branch/base/tree checks fail, dependencies change, network
access occurs, a source dataset changes, a duplicate is selected
automatically, an unapproved union is counted as approved canonical safe
history,
an unapproved source is labelled approved canonical safe history,
conflicting OHLCV is classified as compatible, row requirements are weakened,
performance is inspected, tests fail, or a critical/high reviewer finding
remains.
