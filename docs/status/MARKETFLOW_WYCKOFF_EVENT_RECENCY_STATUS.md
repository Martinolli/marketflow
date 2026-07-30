# MarketFlow Wyckoff Event Recency Status

## Current Status

PASS. Baseline branch, commit, tag, Python executable, clean tree, and `pip check` were confirmed before production changes. Implementation, review remediation, focused tests, collection inspection, full default pytest, compileall, diff check, and before/after Git status comparison completed.

## Baseline Evidence

- Branch: `feature/swing-wyckoff-event-recency`
- Commit: `c14515edde64c47ca7934b17b6c3a7e8ddb62ce6`
- Tag at HEAD: `v0.1.0-alpha.4-true-range-volatility`
- Python: `env\Scripts\python.exe` (`Python 3.12.10`)
- Initial working tree: clean
- Dependency check: `No broken requirements found.`

## Defect Reproduction

Reproduced before production changes with synthetic data:

- One confirmed `SPRING_WEAK` at row 2.
- Rows 3 through 29 have no confirmed event (`pd.NA`).
- Decision row: 29.
- Current `_extract_context` reported `SPRING_WEAK`.
- Current `_event_score` returned `1.0`.
- No age, status, recency policy, or stale-event diagnostic was present.

## Implementation

Implemented:

- Added explicit Wyckoff confirmed-event recency resolution in Strategy Ranking.
- Added `max_event_age_bars` with no default persistence window.
- Added event age, status, provenance, occurrence row/timestamp, decision row, scoring eligibility, supersession count, reason, and resolution-source diagnostics.
- Added optional `wyckoff_confirmed_event_occurrence` provenance marker from the confirmation adapter.
- Preserved `_event_score` behavior for accepted current events and moved temporal gating into `_event_score_for_resolution`.
- Preserved candidate actionability when event credit is zero.
- Propagated diagnostics through Strategy service output ordering, backtest candidate snapshots, backtest candidate/result artifacts, walk-forward candidate construction, walk-forward artifacts, and Studio displays.
- Walk-forward temporal diagnostics resolve only confirmed-event columns; raw `wyckoff_event` fallback remains a label/filter fallback and does not claim `WYCKOFF_CONFIRMED_EVENT` provenance.
- Backtest candidate construction enriches missing event diagnostics from source CSV plus signal row when available.
- Sparse confirmed-event cells are treated as explicit occurrences unless consecutive identical markerless labels make explicitness ambiguous.
- Consecutive identical markerless confirmed labels fail closed as source-unsafe.
- Marker-backed forward-filled display copies do not refresh occurrence age.

Review remediation:

- Resolved reviewer high finding where walk-forward rows could show blank `wyckoff_event` with `EVENT_CURRENT`.
- Resolved reviewer high finding where normal walk-forward case building could not receive/pass `max_event_age_bars`.
- Resolved reviewer high finding where raw event fallback could claim confirmed-event provenance.
- Resolved reviewer medium finding where backtest construction only preserved but did not resolve missing diagnostics when source context was available.

## Verification

Verification passed:

- `env\Scripts\python.exe -m pytest -q tests/test_wyckoff_event_recency.py tests/test_backtest_candidate_service.py tests/test_walk_forward_validation_service.py tests/test_walk_forward_validation_artifact_service.py tests/test_source_assurance.py`
- Result: superseded by the final acceptance run.
- Warnings: the accepted third-party polygon/websockets deprecation warnings only.
- Final acceptance checks are recorded in `docs/status/MARKETFLOW_WYCKOFF_EVENT_RECENCY_ACCEPTANCE.md`.

## Commit And Tag

Final acceptance permits one local commit and still prohibits tag creation and push.
