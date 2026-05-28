# MARKETFLOW_CANDIDATE_SIGNAL_LOCATION_ENRICHMENT_PLAN

## 1. Purpose

This plan defines how to enrich saved Backtest Candidate Snapshots with signal location evidence so deterministic outcome evaluation can produce meaningful `TP_FIRST`, `SL_FIRST`, `NEITHER`, or `AMBIGUOUS` outcomes instead of `INVALID`.

This checkpoint is planning only. It does not change Python code, Studio UI, tests, Strategy Ranking, backtest evaluation, outcome engine logic, artifact formats, or dependencies.

This enrichment must not generate trading signals, introduce future-data leakage, recompute Strategy Ranking, join Monte Carlo results, or optimize candidate selection.

Implementation status: conservative signal-location enrichment is implemented in `marketflow/services/backtest_candidate_service.py`. It uses explicit row/timestamp evidence first and can use latest-row fallback with a validation warning when Strategy Ranking candidates are confirmed as latest-row derived.

## 2. Current Baseline

The current implemented flow is:

```text
Strategy Ranking candidate
-> Save Backtest Candidate Snapshot
-> Backtest Outcome Evaluation
-> *_backtest_results.csv
```

Snapshots may lack `signal_row_index` and `signal_timestamp`. When both are missing, deterministic evaluation cannot locate the signal bar and returns `INVALID`.

Current validation marks this as `missing_signal_location`. That behavior is expected and correct when no signal location evidence exists.

## 3. Why Signal Location Matters

Outcome evaluation must start from future bars only. The outcome engine needs a known decision bar or signal bar before it can scan later OHLC rows for TP/SL hits.

Without `signal_row_index` or `signal_timestamp`, the evaluator cannot know where the future window starts. The service must preserve invalid rows rather than guessing a signal location.

## 4. Candidate Source Reality

Likely current Strategy Ranking candidate fields include:

- `ticker`
- `tf`
- `close`
- `sl`
- `tp`
- `rr`
- `phase`
- `event`
- `trend`
- `score`
- `csv`

The selected Strategy Ranking candidate carries a source CSV path and trade levels, but may not carry row index or timestamp evidence.

## 5. Recommended Enrichment Strategy

Use a conservative enrichment strategy:

1. Prefer explicit candidate location if already present:
   - `signal_row_index`
   - `row_index`
   - `source_row_index`
   - `index`
   - `signal_timestamp`
   - `timestamp`
   - `datetime`
   - `date`
2. If explicit location is missing, inspect `source_csv`.
3. Match the candidate to a source CSV row using deterministic evidence.
4. Only enrich when match confidence is high.
5. If no high-confidence match exists, leave signal location missing and preserve `missing_signal_location`.

## 6. Candidate-to-CSV Matching Methods

Matching methods should run in priority order.

### Method A - exact explicit row index

If the candidate has a row index and it is within CSV bounds:

- use it
- derive timestamp from that row if a timestamp column exists

### Method B - exact timestamp match

If the candidate has timestamp/date/datetime:

- find an exact timestamp match in the source CSV timestamp column
- use the matching row index
- preserve the timestamp source column

### Method C - latest row fallback when candidate is latest-row derived

If Strategy Ranking candidates are known to be derived from the latest row of the source CSV:

- use the last row index
- derive timestamp from the last row
- mark match method as `latest_row_assumption`

This method must be explicitly documented and should add a warning because it depends on Strategy Ranking implementation.

### Method D - close/phase/event/trend match near end of CSV

If no explicit location exists:

- search recent rows only, for example the last 20 rows
- compare close/entry/phase/event/trend if columns exist
- require strong match:
  - close approximately equals candidate entry/close
  - phase matches if available
  - event matches if available
  - trend matches if available
- if multiple matches exist, choose latest only if unambiguous
- otherwise do not enrich

### Method E - no match

Leave signal location missing.

## 7. Timestamp Column Detection

Candidate timestamp columns:

```text
timestamp
datetime
date
Date
Datetime
Timestamp
time
```

Use the first existing column from a preferred list.

Preserve:

```text
signal_timestamp
signal_timestamp_source
```

## 8. Source CSV Row Index Policy

The row index should be the zero-based DataFrame row position used by pandas after reading the CSV.

It should not depend on a CSV index column unless that column is explicitly preserved, clearly named, and validated.

If a CSV has an explicit index-like column, do not use it unless it is clearly named and validated.

Outcome evaluation should start at `signal_row_index + 1`.

## 9. Match Metadata

Future implementations may add optional metadata fields:

```text
signal_match_method
signal_match_confidence
signal_match_warning
```

Do not change the artifact contract in this planning task unless those fields are already supported.

For a first implementation, if artifact columns should not change, place match warnings in validation warnings only.

If changing columns later is acceptable, plan a separate contract update.

## 10. Future Service Design

Plan changes to:

```text
marketflow/services/backtest_candidate_service.py
```

Potential new helper functions:

```python
def enrich_candidate_snapshot_signal_location(
    snapshot: dict[str, Any],
    *,
    max_recent_rows: int = 20,
    latest_row_fallback: bool = True,
) -> dict[str, Any]:
    ...

def locate_candidate_in_source_csv(
    snapshot: dict[str, Any],
    *,
    max_recent_rows: int = 20,
    latest_row_fallback: bool = True,
) -> dict[str, Any]:
    ...
```

Return shape:

```python
{
    "success": bool,
    "snapshot": dict,
    "match": {
        "matched": bool,
        "method": str | None,
        "row_index": int | None,
        "timestamp": Any | None,
        "timestamp_source": str | None,
        "confidence": str,
        "warnings": [...],
        "errors": [...],
    },
}
```

## 11. Integration Point

Recommended integration point:

```text
build_candidate_snapshot_from_strategy_candidate(...)
```

Run enrichment after normalization and before validation.

Reasons:

- snapshot already has `source_csv` and trade levels
- validation can then consider enriched signal location
- Studio save control does not need major changes

Alternative:
Add a separate explicit enrichment toggle in Studio later.

Recommended first implementation:
Automatic conservative enrichment in the service, with warnings when using assumptions.

## 12. Latest Row Fallback Decision

Key design question:

```text
Should we assume Strategy Ranking candidates come from the latest row of the source CSV?
```

Recommended answer:
Yes, but only if current Strategy Ranking implementation confirms it ranks latest candidate state from the latest report row.

Plan:

- inspect `marketflow/services/strategy_service.py`
- inspect source of candidates
- if candidates are latest-row derived, use latest row fallback
- add warning: `signal location inferred from latest source row assumption`

If not confirmed:

- do not use latest row fallback

## 13. Validation Behavior After Enrichment

Expected behavior:

- snapshots with successful enrichment become `valid` if levels, source, and direction are valid
- snapshots without enrichment remain `missing_signal_location`
- validation warnings may include match method and assumption warning

## 14. Safety / Leakage Guardrails

Guardrails:

- never search future rows because the whole source CSV is historical; the signal is the decision row
- if using latest row fallback, the signal row is the last row in the source CSV at candidate-generation time
- never use rows after the selected signal row to choose entry, stop loss, or take profit
- do not infer signal row from TP/SL outcome
- do not optimize row selection to produce a favorable result
- ambiguous matches must not enrich

## 15. Testing Plan For Future Implementation

Future tests should cover:

1. Explicit row index enriches timestamp.
2. Explicit timestamp finds row index.
3. Latest row fallback enriches row index/timestamp when enabled.
4. Latest row fallback disabled leaves missing.
5. Recent close/phase/event match enriches only when unambiguous.
6. Ambiguous duplicate matches do not enrich.
7. Missing source CSV leaves missing.
8. Missing timestamp columns still enriches row index only.
9. Validation changes from `missing_signal_location` to `valid` after enrichment.
10. Invalid levels remain invalid even if location enriches.
11. No mutation of input candidate.
12. Warning produced for latest-row assumption.

## 16. Studio Verification Plan For Future Implementation

Manual flow:

1. Run/load ticker report, e.g. AI or LOAR.
2. Rank candidates.
3. Select a candidate.
4. Inspect Backtest Candidate Snapshot preview.
5. Confirm `signal_row_index` and/or `signal_timestamp` are populated when source CSV allows.
6. Save candidate snapshot.
7. Run Backtest Outcome Evaluation.
8. Confirm outcome is not `INVALID` due only to missing signal location.
9. Confirm `*_backtest_results.csv` is created.
10. Confirm Generated Artifacts shows `backtest_results_csv`.

## 17. Non-Goals

- no Studio UI change in this planning checkpoint
- no Strategy Ranking logic change
- no backtest evaluation logic change
- no Monte Carlo join
- no calibration metrics
- no short setup support
- no trade recommendations
- no artifact column changes unless planned separately

## 18. Recommended Next Implementation Task

Next recommended task:
Implement conservative signal-location enrichment in `marketflow/services/backtest_candidate_service.py`, with tests, using explicit row/timestamp first and latest-row fallback only if Strategy Ranking candidates are confirmed to be latest-row derived.

Status: candidate snapshot signal-location enrichment implemented in the candidate snapshot service.
