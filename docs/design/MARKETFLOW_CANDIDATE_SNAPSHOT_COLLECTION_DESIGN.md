# MARKETFLOW_CANDIDATE_SNAPSHOT_COLLECTION_DESIGN

## 1. Purpose

Candidate Snapshot Collection will convert Strategy Ranking candidates into frozen records suitable for deterministic outcome evaluation.

The goal is research and Monte Carlo calibration. It is not a trade signal engine, not financial advice, and not a change to Strategy Ranking logic. Snapshot collection should preserve the candidate fields available at decision time so the backtest outcome engine can later evaluate what happened after the signal bar.

## 2. Current Baseline

The current backtest foundation includes:

- a deterministic outcome engine in `marketflow/backtesting/outcome_engine.py`
- a JSON-safe service wrapper in `marketflow/services/backtest_service.py`
- `CandidateSnapshot` and `OutcomeResult` dataclasses in `marketflow/backtesting/schemas.py`
- synthetic tests for the outcome engine and service wrapper

There is no Studio wiring, no snapshot artifact generation, no Monte Carlo forecast join, and no calibration summary yet.

## 3. Source Candidate Locations

Code inspection found the following current candidate sources.

| Source | Reliability | Available fields | Phase 2 suitability |
| --- | --- | --- | --- |
| Strategy Ranking dataframe from `rank_latest_candidates(...)` | High for selected setup fields, but it does not currently guarantee a signal row location. | `ticker`, `tf`, `close`, `sl`, `tp`, `rr`, `phase`, `event`, `trend`, `score`, `csv`, MC match metadata. | Best first source when combined with selected-candidate UI state and explicit row/timestamp evidence. |
| Studio selected Strategy Ranking candidate state | High for workflow alignment because it is the user-selected candidate used to prefill Monte Carlo and Analyst Packet. | Same as the Strategy Ranking row, plus any normalized fields added by Studio. | Recommended Phase 2 source. It matches the current user workflow and selected trade-plan handoff. |
| Monte Carlo selected candidate prefill | High for entry/SL/TP alignment after a selected candidate is sent to Monte Carlo. | `ticker`, `csv`, `tf`, `entry`, `stop_loss`, `take_profit`, `source`, and `source_candidate`. | Useful fallback or cross-check, but should not be the primary source because it may represent a manually edited scenario. |
| Analyst Packet normalized strategy candidate | High for evidence-layer consistency after packet build. | Normalized strategy candidate, selected CSV/timeframe, P&F and Eigen context, MC alignment metadata. | Useful later for enrichment and audit cross-checks, but Phase 2 should avoid depending on packet build. |
| Annotated CSV rows | Medium. They are closest to source OHLC/Wyckoff data, but the selected entry/SL/TP mapping is not always present. | OHLC, timestamps, Wyckoff labels, features, possible row positions. | Useful for locating signal row/timestamp and validating source data, not sufficient alone for selected candidate levels. |
| Report JSON / summary artifacts | Variable by artifact and report version. | Report metadata, generated files, summaries, possibly ranking outputs depending on the report. | Later fallback for batch collection. Not recommended for first implementation unless the schema is already stable for a report type. |

## 4. Recommended Phase 2 Source

The first implementation should use the selected Strategy Ranking candidate / normalized candidate object already used to prefill Monte Carlo and Analyst Packet.

This source is recommended because:

- it is already aligned with entry, stop loss, and take profit
- it represents the user-selected candidate in the current workflow
- it carries CSV and timeframe context
- it avoids scanning future rows to discover candidate fields
- it matches the current Monte Carlo and Analyst Packet handoff path

Annotated CSV data should be used to confirm the signal row or timestamp, not to recompute the selected candidate levels.

## 5. CandidateSnapshot Field Mapping

Optional enrichment fields are grouping variables only. They must not affect outcome logic.

| CandidateSnapshot field | Preferred source field | Alias/fallback fields | Required? | Notes |
| --- | --- | --- | --- | --- |
| `ticker` | `ticker` | inferred from `csv` filename | Preferred | Useful for grouping and artifact names. |
| `timeframe` | `timeframe` | `tf`, inferred from filename | Preferred | Needed for grouped analysis and matching. |
| `source_csv` | `source_csv` | `csv`, selected CSV path | Yes | Outcome evaluation requires the same CSV data used when the candidate was created. |
| `signal_timestamp` | `signal_timestamp` | `timestamp`, `date`, `datetime`, annotated row timestamp | Yes if no row index | Preserve the original string when possible. |
| `signal_row_index` | `signal_row_index` | source row index from Strategy Ranking or annotated CSV lookup | Yes if no timestamp | Preferred when available because it is deterministic. |
| `entry` | `entry` | `close` from selected Strategy Ranking row | Yes | Do not recompute during snapshot extraction. |
| `stop_loss` | `stop_loss` | `sl` | Yes | Do not silently repair invalid values. |
| `take_profit` | `take_profit` | `tp` | Yes | Do not silently repair invalid values. |
| `risk_reward` | `risk_reward` | `rr`, computed from levels | Preferred | Preserve source value when available. |
| `strategy_score` | `strategy_score` | `score` | Preferred | Grouping and later calibration analysis. |
| `wyckoff_phase` | `wyckoff_phase` | `phase` | Optional | Grouping context only. |
| `wyckoff_event` | `wyckoff_event` | `event` | Optional | Grouping context only. |
| `trend` | `trend` | none | Optional | Grouping context only. |
| `candidate_source` | `candidate_source` | `source`, default `strategy_ranking` | Preferred | Records how the snapshot was created. |
| `report_date` | `report_date` | report folder date | Optional | Useful for report lineage. |
| `pnf_gate` | Analyst Packet P&F context | packet summary | Future optional | Grouping variable only. |
| `pnf_objective_quality` | Analyst Packet P&F context | packet summary | Future optional | Grouping variable only. |
| `mc_model` | Monte Carlo result | `model` | Future optional | Forecast-join grouping variable only. |
| `mc_paths` | Monte Carlo result | `paths` | Future optional | Forecast-join grouping variable only. |
| `mc_horizon_bars` | Monte Carlo result | `horizon_bars` | Future optional | Forecast-join grouping variable only. |
| `eigen_available` | Analyst Packet Eigen context | packet summary | Future optional | Grouping variable only. |
| `eigen_recent_divergence_count` | Analyst Packet Eigen context | packet summary | Future optional | Grouping variable only. |

## 6. Signal Row Policy

Signal row location is critical for avoiding wrong-row evaluation.

Preferred policy:

1. Use explicit `signal_row_index` if available.
2. Else use exact timestamp match if the candidate has a timestamp and the CSV has `timestamp`, `date`, or `datetime`.
3. Else infer from the candidate row only if Strategy Ranking preserves a source row index.
4. Else mark the snapshot incomplete for backtest outcome evaluation.

For collected real candidates, do not default to row `0` unless the user explicitly creates a manual or synthetic snapshot. Defaulting to row `0` can accidentally evaluate a different setup and can introduce misleading results.

Outcome evaluation starts after the signal row. Rows before or at the signal row are not future outcomes.

## 7. Timestamp Policy

Candidate timestamp extraction should use these fields in order:

1. `signal_timestamp`
2. `timestamp`
3. `datetime`
4. `date`
5. annotated CSV row timestamp found from source row evidence

Rules:

- preserve the original string where possible
- avoid timezone transformation unless explicitly required later
- store `signal_timestamp_source`
- if timestamp matching is used, prefer exact string match before datetime parsing

## 8. CSV Path Policy

`source_csv` should preserve the selected CSV path that produced the Strategy Ranking candidate.

Rules:

- prefer absolute/resolved paths for internal evaluation
- store a display path or filename in future artifact rows
- preserve the original selected CSV path for traceability
- support report-folder-relative paths in a later artifact phase

Backtest outcome evaluation requires the same CSV data used when the candidate was created. If the CSV has changed or the row order differs, the snapshot should be marked incomplete or stale rather than silently evaluated.

## 9. Entry/SL/TP Policy

Entry, stop loss, and take profit must come from the selected Strategy Ranking candidate or the manually aligned Monte Carlo prefill derived from that selected candidate.

Rules:

- do not recompute entry during snapshot extraction
- do not recompute stop loss during snapshot extraction
- do not recompute take profit during snapshot extraction
- invalid or missing levels should produce an invalid snapshot status, not a silent repair
- manual edits should be marked as manual scenario data if they are supported later

## 10. Risk/Reward Policy

If the candidate has `risk_reward`, preserve it. If not, compute:

```text
(take_profit - entry) / (entry - stop_loss)
```

Phase 2 should remain long-only initially. Short strategy support is a future phase and should have separate validation rules.

## 11. Snapshot Validation

Planned validation statuses:

```text
valid
missing_levels
missing_source_csv
missing_signal_location
invalid_levels
unsupported_direction
```

Required fields for a Phase 2 valid snapshot:

- `source_csv`
- `entry`
- `stop_loss`
- `take_profit`
- `signal_row_index` or `signal_timestamp`
- `timeframe` if available
- `ticker` if available

Validation should return errors and warnings. It should not raise for normal incomplete-candidate cases.

## 12. Proposed Snapshot Extraction Service

Future file:

```text
marketflow/services/backtest_candidate_service.py
```

Planned functions:

```python
normalize_candidate_snapshot(candidate: dict[str, Any]) -> dict[str, Any]

build_candidate_snapshot_from_strategy_candidate(
    candidate: dict[str, Any],
    *,
    report_dir: str | Path | None = None,
) -> dict[str, Any]

validate_candidate_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]
```

Return shape:

```python
{
    "success": bool,
    "snapshot": {...},
    "validation": {
        "status": "...",
        "errors": [...],
        "warnings": [...],
    },
}
```

The first service implementation should normalize and validate only. It should not write artifacts and should not add Studio UI.

## 13. Proposed Snapshot CSV Artifact

Future artifact:

```text
*_backtest_candidates.csv
```

Planned fields:

- all `CandidateSnapshot` fields
- `validation_status`
- `validation_errors`
- `validation_warnings`
- `created_at`
- `source_report_dir`
- `source_strategy_rank`

Planned artifact kind:

```text
backtest_candidates_csv
```

A dedicated CSV artifact contract exists at `docs/reference/MARKETFLOW_BACKTEST_CANDIDATE_ARTIFACT_CONTRACT.md`.

Artifact classification should be added in a later implementation step, not in this design checkpoint.

## 14. Integration Points

Future integration points:

- Strategy Ranking selected candidate
- Monte Carlo alignment metadata
- Analyst Packet selected candidate
- future Backtest Lab

Phase 2 should start service-first, not UI-first. Studio integration should come after normalization and validation tests prove the snapshot shape is stable.

## 15. Look-Ahead Bias Guardrails

Guardrails:

- never use future rows to create snapshot fields
- outcome evaluation starts after the signal row
- candidate snapshot must freeze levels available at decision time
- do not recalculate entry, stop loss, or take profit from later data
- store source CSV and row/timestamp evidence
- mark snapshots incomplete when signal location cannot be proven

## 16. Testing Plan

Future tests should cover:

- selected candidate with explicit row index
- selected candidate with timestamp
- candidate missing timestamp and row index
- candidate missing source CSV
- candidate with alias fields `tf`, `csv`, `sl`, `tp`, `rr`, `score`, `phase`, `event`
- invalid levels
- valid snapshot written to CSV later
- no future rows accessed during snapshot construction

## 17. Non-Goals

- no backtest batch generation yet
- no calibration metrics yet
- no Monte Carlo forecast join yet
- no Studio UI yet
- no artifact generation yet
- no short strategy support yet
- no optimization or parameter fitting

## 18. Recommended Next Implementation Task

Phase 2.1 status: implemented `marketflow/services/backtest_candidate_service.py` for normalization and validation only. No Studio UI or artifact generation yet.

Next recommended task:
Plan the next service-first Phase 2 step for snapshot CSV artifact creation, then implement it separately with tests. No Studio UI until the snapshot artifact contract is stable.

Status: Phase 2.1 implementation checkpoint recorded; Studio UI and artifact generation remain future work.
