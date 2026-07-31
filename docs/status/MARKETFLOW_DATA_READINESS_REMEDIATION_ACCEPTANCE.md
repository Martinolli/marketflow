# MarketFlow Data Readiness Remediation Acceptance

## Decisions

- Data-remediation tooling: PASS.
- Canonical data readiness: BLOCKED.
- UTC acceptance date: `2026-07-31T18:23:10Z`.
- Branch: `feature/swing-data-readiness-remediation`.
- Base commit: `07492d8496d0d897abbbc20d1e333b90ee0eca78`.
- Baseline tag at base: `v0.1.0-alpha.11-fixed-profile-orchestrator`.
- Commit intent: local commit only.
- Tag: not created.
- Push: not performed.

## Scope And Exclusions

Accepted scope:

- read-only canonical annotated CSV inventory;
- deterministic duplicate count semantics;
- deterministic duplicate group classification;
- OHLCV/annotation/provenance comparison without public OHLCV values;
- fixed-profile history-depth estimates;
- strict canonical-dataset registry design;
- append-only decision-register model;
- fixed-date acquisition requirement model;
- reannotation requirement model;
- ignored local deterministic report generation;
- focused tests and documentation.

Excluded scope:

- no source dataset deletion, rename, move, merge, truncate, overwrite,
  reannotation, download, or provider request;
- no approved canonical source selection;
- no normal-orchestrator registry integration;
- no Strategy Ranking, candidate builder, Monte Carlo, PnF outcome analysis,
  outcome evaluator, campaign aggregation, optimization, broker, execution, or
  performance analysis;
- no predictive usefulness, economic significance, or profitability acceptance.

## No-Peek Proof

The remediation module imports no provider, Strategy Ranking, candidate
builder, Monte Carlo, outcome evaluator, Streamlit, LLM, or broker module. It
does not call win-rate, expectancy, MFE/MAE, Sharpe/Sortino, drawdown,
optimization, best-result selection, or candidate-score logic.

The tool inspects OHLCV values only for deterministic data-consistency
comparison. Public report output does not include OHLCV row values.

## Inventory-Scope Reconciliation

The previous accepted readiness scan reported:

- total canonical annotated CSV files: 54;
- unique ticker/timeframe identities: 16;
- duplicate identities: 12;
- excess duplicate files: 38.

The current remediation scan reports:

- total canonical annotated CSV files: 60;
- unique ticker/timeframe identities: 20;
- duplicate identities: 14;
- files inside duplicate groups: 54;
- excess duplicate files: 40.

The old applicability scanner and the new remediation scanner agree on the
current 60-file source set. The count difference is due to six canonical
annotated files added under `.marketflow/reports` outside this remediation task
after the earlier readiness acceptance:

- `.marketflow/reports/2026-07-30/LOAR/LOAR_1d_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/LOAR/LOAR_1h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/LOAR/LOAR_4h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_1d_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_1h_wyckoff_annotated.csv`;
- `.marketflow/reports/2026-07-30/RKLB/RKLB_4h_wyckoff_annotated.csv`.

The delta adds four identities and two excess duplicate files. It is not caused
by expanded approved roots, changed filename parsing, corrected annotated-file
classification, or forced inclusion. A synthetic regression test confirms the
new scanner matches the accepted applicability canonical-dataset scope.

## Count Definitions

- Total file count: accepted annotated CSV source files scanned.
- Unique identity count: distinct canonical ticker/timeframe identities.
- Duplicate identity count: identities represented by more than one source
  file.
- Files in duplicate groups: source files belonging to duplicate identities.
- Excess duplicate files: `sum(group_size - 1)` across duplicate groups.

Final values:

- total file count: 60;
- unique identity count: 20;
- duplicate identity count: 14;
- files in duplicate groups: 54;
- excess duplicate files: 40.

## Duplicate Classifications

Current group classification summary:

- `OVERLAPPING_CONFLICTING`: 11;
- `DISJOINT_HISTORY_SAME_IDENTITY`: 3.

Current scan found:

- exact-byte duplicate groups: 0;
- semantic-identical groups: 0;
- same-OHLCV/different-annotation groups: 0;
- strict subset/superset-compatible groups: 0;
- compatible-overlap groups: 0.

Group classification is conservative. Precedence is:

1. `IDENTITY_INVALID`;
2. `SCHEMA_DIVERGENT`;
3. `TIMESTAMP_NORMALIZATION_CONFLICT`;
4. `PROVENANCE_CONFLICT`;
5. `OVERLAPPING_CONFLICTING`;
6. `EXACT_BYTE_DUPLICATES`;
7. same-coverage semantic classes, including
   `SAME_OHLCV_DIFFERENT_ANNOTATIONS` and `SEMANTICALLY_IDENTICAL`;
8. `DISJOINT_HISTORY_SAME_IDENTITY`;
9. strict subset/superset compatibility;
10. `OVERLAPPING_COMPATIBLE`;
11. `UNCLASSIFIED_REVIEW_REQUIRED`.

One conflicting shared OHLCV row prevents compatible classification. No
majority vote, newest-file selection, longest-history selection, row-count
preference, or best-file preference is used.

## Source Comparison

Exact-byte duplicates require identical SHA-256 over file bytes.

Semantic OHLCV comparison uses exact normalized timestamps and deterministic
`Decimal` numeric normalization. It rejects NaN and Infinity, records shared
timestamp count, exclusive timestamp counts, conflict count, first/last
conflict timestamps, common date range, and coverage relationship. Annotation
comparison is separate from OHLCV comparison.

Timezone conventions are compared. Duplicate and non-monotonic timestamps fail
closed; source rows are not sorted to create safety. Provenance conflicts
prevent automatic compatibility. Corporate-action adjustment status is accepted
only from explicit metadata; absent metadata remains
`CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN`.

## History Depth

Terminology:

- `BEST_VALID_SINGLE_SOURCE_ROWS`: greatest structurally valid row count
  observed in one source file, without approving that source.
- `APPROVED_CANONICAL_SAFE_ROWS`: rows in a registry-approved source whose
  digest has validated.
- `ESTIMATED_SHORTFALL_FROM_BEST_SINGLE_SOURCE`: row shortfall estimated from
  an unapproved single source.

For every current fixed-profile identity,
`APPROVED_CANONICAL_SAFE_ROWS = NOT_ESTABLISHED`.

`SWING` / `4h` requires 390 rows.

| Ticker | Best valid single-source rows | Approved canonical safe rows | Estimated shortfall | Duplicate/provenance blocker |
| --- | ---: | --- | ---: | --- |
| `AAAU` | 279 | `NOT_ESTABLISHED` | 111 | `OVERLAPPING_CONFLICTING` |
| `AAPL` | 324 | `NOT_ESTABLISHED` | 66 | `DISJOINT_HISTORY_SAME_IDENTITY` |
| `AI` | 283 | `NOT_ESTABLISHED` | 107 | `OVERLAPPING_CONFLICTING` |
| `IONQ` | 293 | `NOT_ESTABLISHED` | 97 | `DISJOINT_HISTORY_SAME_IDENTITY` |
| `LOAR` | 223 | `NOT_ESTABLISHED` | 167 | `SINGLE_SOURCE` |
| `RKLB` | 231 | `NOT_ESTABLISHED` | 159 | `SINGLE_SOURCE` |

`POSITION_SWING` / `1d` requires 560 rows.

| Ticker | Best valid single-source rows | Approved canonical safe rows | Estimated shortfall | Duplicate/provenance blocker |
| --- | ---: | --- | ---: | --- |
| `AAAU` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `AAPL` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `AI` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `IONQ` | 252 | `NOT_ESTABLISHED` | 308 | `SINGLE_SOURCE` |
| `LOAR` | 252 | `NOT_ESTABLISHED` | 308 | `OVERLAPPING_CONFLICTING` |
| `RKLB` | 252 | `NOT_ESTABLISHED` | 308 | `SINGLE_SOURCE` |

Potential compatible union rows are `REVIEW_REQUIRED` for conflicting and
disjoint duplicate groups and `NOT_APPLICABLE` for single-source identities. No
unapproved union is counted as approved canonical safe history.

## Registry And Decision Register

The registry schema version is `marketflow.canonical_dataset_registry.v1`.
Allowed statuses are:

- `UNRESOLVED`;
- `APPROVED`;
- `SUSPENDED`;
- `CONFLICT_REVIEW_REQUIRED`;
- `REACQUISITION_REQUIRED`.

Unknown fields, missing fields, unsafe refs, unsafe superseded refs, missing
files, file SHA-256 mismatch, semantic OHLCV digest mismatch, and multiple
approved records for one identity fail closed. The source-controlled example is
fictional only.

The decision register schema version is
`marketflow.dataset_decision_register.v1`. Changed decisions create new
records; deletion and retroactive mutation fail. Approval requires a selected
safe source and operator approval. Performance, candidate score,
profitability, or outcome rationale fails. The example is fictional only.

## Acquisition And Reannotation

Acquisition requirements are row-gated by ticker, timeframe, required rows,
best valid single-source rows, approved canonical safe rows, estimated
shortfall, provenance requirement, adjustment requirement, fixed start-date
status, fixed end-date status, and acquisition status.

Actual start/end dates remain `HUMAN_APPROVAL_REQUIRED`. Mutable period strings
such as `100d`, `365d`, `2y`, or `5y` are not accepted as the scientific
research contract.

No reannotation was performed. Longer or newly acquired OHLCV may later require
deterministic current-code annotation in a separate phase. Original raw sources
must not be modified by that later process.

## Deterministic Report

Generated ignored report:

```text
.marketflow/data_readiness/data_readiness_remediation_report.json
```

Report semantic SHA-256:

```text
814270b29e874edfe7493091edd1205248d18c7a6b957595fc713d69ef6252da
```

The semantic digest excludes scan timestamp. A synthetic unchanged-root
regression proves repeated scans have the same semantic digest. Report output
uses safe relative refs only and contains no absolute paths, credentials,
OHLCV row values, candidate results, outcome results, or performance values.
The generated report is ignored and was not staged.

## Warning Behavior

The final full suite emitted no warning summary. No broad global warning
suppression was introduced by this task. Existing provider/client warning
filters are test-local and pre-existing. The absence of the prior
Polygon/websockets deprecation warnings is not a strategy change and does not
hide a project-owned warning.

## Source Immutability

Read-only `.marketflow/reports` inventory before and after tests/scans:

- file count: 925;
- relative filename/size/mtime/SHA-256 inventory digest:
  `97fff3b4e44053381d47536d2f5fc9579ffad884ebac9d874df58baf20203599`.

Git status for `.marketflow/reports` was clean before and after. No automatic
cleanup or restoration was used to hide mutation.

## Verification

Required checks used `env\Scripts\python.exe`.

```text
pip check: No broken requirements found.
focused remediation tests: 18 passed.
related remediation/prior-integrity suite: 250 passed.
pytest --collect-only -q: 618 tests collected.
pytest -q: 618 passed.
compileall -W error: passed.
git diff --check: passed.
```

Test count explanation: accepted fixed-profile baseline collected `600` tests.
This task adds `18` deterministic data-readiness remediation tests.

No network, provider, broker, execution, dependency change, source-file
remediation, historical-report rewrite, candidate generation, Monte Carlo,
outcome evaluation, optimization, or performance analysis was added or
exercised.

## Previous Integrity Non-Regression

Focused and full suites preserve:

- baseline packaging/no-network controls;
- strict source identity;
- target/RR integrity;
- True Range;
- Wyckoff event recency;
- evidence availability;
- candidate-builder alignment;
- swing applicability readiness;
- operational artifact controls;
- Artifact Lineage v1;
- fixed-profile orchestrator.

No Strategy semantic change was added.

## Reviewer Findings

Reviewer A:

- High: invalid duplicate/non-monotonic timestamp chronology could still be
  classified as compatible and counted as approved canonical safe history.
  Fixed.
- Medium: `STRICT_SUPERSET_COMPATIBLE` was defined but not emitted. Fixed.
- Medium: direct `inspect_source()` could read unsafe paths. Fixed.
- Follow-up: no high or critical blocker remains.

Reviewer B:

- High: registry safe refs were checked only for approved records. Fixed.
- High: decision approval could lack selected source/operator approval. Fixed.
- Medium: performance-rationale rejection missed compound and candidate-score
  cases. Fixed.
- Medium: semantic OHLCV digest was not validated. Fixed.
- Follow-up: no high or critical blocker remains.

## Blockers

Canonical data readiness remains blocked:

- no source is approved canonical;
- no merge is approved;
- no deletion is approved;
- approved canonical safe history is not established;
- 14 duplicate identities require human decisions;
- 11 groups are overlapping conflicting;
- 3 groups are disjoint same-identity histories;
- every fixed-profile identity is below row requirements by the best
  single-source estimate;
- provenance and adjustment review remains required;
- fixed-date acquisition remains pending;
- research protocol remains blocked;
- no performance campaign is authorized.

## Final Acceptance Statement

Data-remediation tooling is accepted for local commit.

Canonical data readiness remains blocked.

No source is approved canonical.

No merge or deletion is approved.

Predictive usefulness and profitability remain unaccepted.
