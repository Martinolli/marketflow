# MarketFlow Data Readiness Remediation Status

Status: PASS FOR TOOLING, DATA READINESS BLOCKED

Branch: `feature/swing-data-readiness-remediation`

Base commit: `07492d8496d0d897abbbc20d1e333b90ee0eca78`

Baseline tag: `v0.1.0-alpha.11-fixed-profile-orchestrator`

## Boundary

Data-remediation tooling may be accepted as offline governance support. Data
readiness remains blocked pending human decisions, canonical registry approval,
provenance/adjustment resolution, and additional history.

No source is automatically canonical. No dataset has been deleted, renamed,
moved, merged, truncated, overwritten, reannotated, downloaded, or selected.
Predictive usefulness and profitability remain unaccepted.

## Implemented Artifacts

- `marketflow/research/data_readiness_remediation.py`;
- `docs/plans/MARKETFLOW_DATA_READINESS_REMEDIATION_PLAN.md`;
- `docs/architecture/MARKETFLOW_CANONICAL_DATASET_REGISTRY.md`;
- `docs/research/MARKETFLOW_DATASET_DECISION_POLICY.md`;
- `config/canonical_dataset_registry.example.toml`;
- `config/dataset_decision_register.example.json`;
- `tests/test_data_readiness_remediation.py`.

Generated local report:

- `.marketflow/data_readiness/data_readiness_remediation_report.json`;
- report semantic SHA-256:
  `814270b29e874edfe7493091edd1205248d18c7a6b957595fc713d69ef6252da`.

The generated report is ignored local runtime evidence and is not committed.

## Current Inventory

Current deterministic scan:

- total canonical annotated dataset file count: 60;
- unique ticker/timeframe identity count: 20;
- duplicate identities: 14;
- total files inside duplicate groups: 54;
- excess duplicate files: 40.

The older accepted readiness scan reported 54 files, 16 identities, 12
duplicate identities, and 38 excess files. The old applicability scanner and
the new remediation scanner now agree on the current 60-file source set. The
delta is due to six canonical annotated files added under `.marketflow/reports`
outside this remediation task after the earlier readiness acceptance:

- `.marketflow/reports/2026-07-30/LOAR/LOAR_1d_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/LOAR/LOAR_1h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/LOAR/LOAR_4h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_1d_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_1h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_4h_wyckoff_annotated.csv`.

The increase adds four identities and two excess duplicates. It is not caused
by expanded approved roots, changed filename parsing, corrected annotated-file
classification, or forced inclusion.

## Duplicate Classification Summary

Current duplicate groups:

- `OVERLAPPING_CONFLICTING`: 11;
- `DISJOINT_HISTORY_SAME_IDENTITY`: 3.

Current scan found no exact-byte duplicate group, semantic-identical group,
same-OHLCV/different-annotation group, subset/superset-compatible group, or
compatible-overlap group among the current duplicate identities.

Conflicting overlaps require manual conflict review or source reacquisition.
Disjoint histories require manual provenance, timezone, adjustment, interval,
and continuity review before any future merge decision.

## History Depth

`BEST_VALID_SINGLE_SOURCE_ROWS` is the greatest structurally valid row count
observed in one source file. It does not approve that source.

`APPROVED_CANONICAL_SAFE_ROWS` is `NOT_ESTABLISHED` for every current identity
because no registry-approved source exists.

`ESTIMATED_SHORTFALL_FROM_BEST_SINGLE_SOURCE` is a row-depth estimate from an
unapproved source, not an approved canonical shortfall.

`SWING` / `4h` requires 390 valid OHLCV rows.

| Ticker | Best valid single-source rows | Approved canonical safe rows | Estimated shortfall | Duplicate classification |
| --- | ---: | --- | ---: | --- |
| `AAAU` | 279 | `NOT_ESTABLISHED` | 111 | `OVERLAPPING_CONFLICTING` |
| `AAPL` | 324 | `NOT_ESTABLISHED` | 66 | `DISJOINT_HISTORY_SAME_IDENTITY` |
| `AI` | 283 | `NOT_ESTABLISHED` | 107 | `OVERLAPPING_CONFLICTING` |
| `IONQ` | 293 | `NOT_ESTABLISHED` | 97 | `DISJOINT_HISTORY_SAME_IDENTITY` |
| `LOAR` | 223 | `NOT_ESTABLISHED` | 167 | `SINGLE_SOURCE` |
| `RKLB` | 231 | `NOT_ESTABLISHED` | 159 | `SINGLE_SOURCE` |

`POSITION_SWING` / `1d` requires 560 valid OHLCV rows.

| Ticker | Best valid single-source rows | Approved canonical safe rows | Estimated shortfall | Duplicate classification |
| --- | ---: | --- | ---: | --- |
| `AAAU` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `AAPL` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `AI` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `IONQ` | 252 | `NOT_ESTABLISHED` | 308 | `SINGLE_SOURCE` |
| `LOAR` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `RKLB` | 252 | `NOT_ESTABLISHED` | 308 | `SINGLE_SOURCE` |

Potential compatible union rows are `REVIEW_REQUIRED` for conflicting and
disjoint duplicate identities, and `NOT_APPLICABLE` for single-source
identities. No unapproved union is counted as approved canonical safe history.

## Registry And Decision Register

The canonical registry design is strict and source-controlled. It rejects
unknown fields, missing fields, absolute or traversal source references,
unsafe superseded references, missing files, file-byte digest mismatches,
semantic OHLCV digest mismatches, and multiple approved records for one
identity. Registry integration with normal orchestration remains deferred.

The decision-register model is append-oriented. It rejects deletion,
retroactive edits, unsafe selected-source references, invalid duplicate
classifications, invalid states, incomplete approved decisions, missing
operator approval for approved decisions, and performance rationale including
candidate-score rationale.

## Acquisition And Reannotation

Every fixed-profile identity remains short of the accepted row floor. Fixed
start and end dates remain `HUMAN_APPROVAL_REQUIRED`; the acquisition contract
is row-gated rather than period-string-gated.

Annotation compatibility remains review-required. Deterministic reannotation
may be feasible later, but no file is reannotated in this task.

## Verification Evidence

Current completed checks:

- branch/start commit/clean tree verified;
- `env\Scripts\python.exe --version`: `Python 3.12.10`;
- `env\Scripts\python.exe -m pip check`: passed;
- read-only `.marketflow/reports` metadata inventory before implementation:
  925 files;
- `.marketflow/reports` Git status before implementation: clean;
- focused data-readiness remediation tests:
  `18 passed`;
- focused data-remediation, registry, decision-register, no-peek,
  source-assurance, fixed-profile, Artifact Lineage v1, applicability,
  operational, source-identity, evidence, candidate-alignment, risk/reward,
  True Range, event-recency, and data-parameter suite:
  `250 passed`;
- `env\Scripts\python.exe -m pytest --collect-only -q`:
  `618 tests collected`;
- `env\Scripts\python.exe -m pytest -q`:
  `618 passed`;
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed;
- `git diff --check`: passed;
- final `env\Scripts\python.exe -m pip check`: passed;
- post-test `.marketflow/reports` metadata inventory:
  925 files with relative filename/size/mtime/content-SHA-256 digest
  `97fff3b4e44053381d47536d2f5fc9579ffad884ebac9d874df58baf20203599`,
  matching the pre-test inventory;
- `.marketflow/reports` Git status after testing: clean.

Warnings: no warning summary was emitted by the final full suite. No broad
global warning suppression was introduced by this task. The prior three
third-party Polygon/websockets deprecation warnings were tied to imported
provider/client paths in earlier suites; the current full run emitted no
unsuppressed warnings and no project-owned warning was hidden.

Test count explanation: the accepted fixed-profile baseline collected `600`
tests. This task adds `18` deterministic data-readiness remediation tests,
bringing final collection to `618`.

## No-Peek Evidence

The remediation module imports no provider, candidate builder, Monte Carlo,
outcome evaluator, Streamlit, or LLM module. It does not call performance
metrics or automatic canonical approval. Source-assurance tests cover those
boundaries.

## Blockers

Data readiness remains blocked:

- 14 duplicate ticker/timeframe identities require human decisions;
- 11 duplicate groups are overlapping conflicting;
- 3 duplicate groups are disjoint same-identity histories;
- every fixed-profile identity remains below the accepted row floor;
- provenance and adjustment status require explicit review;
- no canonical registry approval exists.

## Reviewer Findings

Reviewer A:

- High: invalid duplicate/non-monotonic timestamp chronology could still be
  classified as compatible and counted as approved canonical safe history. Fixed by
  fail-closing chronology errors before byte/semantic compatibility and by
  excluding errored sources from best-valid single-source row counts.
- Medium: `STRICT_SUPERSET_COMPATIBLE` was defined but not emitted. Fixed with
  an explicit code path and regression coverage.
- Medium: direct `inspect_source()` could read an unsafe path after safe-ref
  failure. Fixed by returning before file-byte or CSV reads.
- Follow-up: no high/critical blocker remains.

Reviewer B:

- High: registry validation checked safe refs only for `APPROVED` records.
  Fixed by validating nonempty approved and superseded references for all
  statuses.
- High: decision-register approval semantics allowed approved decisions without
  selected source or operator approval. Fixed.
- Medium: performance-rationale rejection missed compound and candidate-score
  rationale. Fixed.
- Medium: approved semantic OHLCV digest was not validated. Fixed with digest
  validation and mismatch coverage.
- Follow-up: no high/critical blocker remains.

No critical or high reviewer finding remains open.
