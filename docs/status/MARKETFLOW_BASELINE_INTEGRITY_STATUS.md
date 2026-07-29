# MarketFlow Baseline Integrity Status

## Status

PASS.

The malformed MarketFlow dependency metadata was repaired, default pytest is deterministic/offline, compileall passes under `-W error`, and `pip check` is clean after the external environment fix for `streamlit==1.45.1`.

```text
No broken requirements found.
```

No dependency was installed, upgraded, downgraded, removed, or hidden by Codex in this task.

## Starting Point

- Branch: `feature/swing-consistency-audit`
- Commit: `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`
- Initial working tree: clean
- Original `pip check`: malformed MarketFlow dependency metadata
- Original pytest baseline from task request: 373 passed, 24 warnings
- Original compileall baseline from task request: passed with two invalid escape `SyntaxWarning` messages
- Original tracked-artifact issue from task request: full suite modified three tracked NVDA report artifacts

## Fixes Applied

- Added `AGENTS.md` repository rules.
- Added `docs/plans/MARKETFLOW_BASELINE_INTEGRITY_PLAN.md`.
- Removed generated `marketflow.egg-info` files from Git tracking and ignored generated packaging directories.
- Corrected `setup.py` metadata hygiene:
  - `requirements.txt` remains authoritative.
  - missing requirements files now fail instead of silently generating fallback dependency metadata.
  - package setup no longer executes on import.
  - MIT license is declared without the deprecated license classifier warning.
- Added packaging integrity tests for requirements parsing, generated metadata parsing, ignored generated metadata, and untracked generated directories.
- Regenerated local ignored `marketflow.egg-info` and refreshed editable metadata with:

```powershell
& $python -m pip install --no-index --no-deps --no-build-isolation --disable-pip-version-check -e .
```

- Moved manual/provider/LLM observational scripts under `scripts/manual_checks/`.
- Added `docs/testing/MANUAL_NETWORK_CHECKS.md`.
- Updated README testing guidance for offline default pytest and manual network checks.
- Added a default pytest socket guard for `socket.create_connection`, `socket.socket.connect`, and `connect_ex`.
- Added network-guard regression tests.
- Reworked `tests/test_integration_core_pipeline.py` to generate reports only under `tmp_path` with deterministic facade-shaped data.
- Added source-assurance tests for pytest return values, import-time test output creation, tracked report writes, manual-check exclusion, real-provider boundaries, generated metadata, strategy-file drift, and the narrow Wyckoff dtype change.
- Fixed the Wyckoff pandas `FutureWarning` by creating `phase_series` with `dtype="string"` while preserving `UNKNOWN` fallback.
- Fixed invalid escape `SyntaxWarning` instances by converting affected docstrings to raw strings.
- Made the Wyckoff fixture deterministic and added missing-phase fallback coverage.
- Added deterministic query-engine tests for input validation, ticker extraction, and intent parsing without runtime provider calls.

## Test Count

- Original default pytest count: 373.
- Final default pytest count: 372.
- Count explanation:
  - 22 collected script-style/manual tests were removed from default collection.
  - 21 deterministic tests were added for packaging, no-network, source assurance, and query-engine pure behavior.

## Verification Results

- Focused integrity tests:

```text
29 passed, 3 warnings
```

- Full default pytest:

```text
372 passed, 3 warnings
```

- Collection:

```text
372 tests collected
```

- Compileall:

```text
& $python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
```

Result: passed.

- Final `pip check`:

```text
No broken requirements found.
```

The original malformed dependency parser warning is gone, and the later missing-`streamlit` environment issue is resolved.

## Warning Count

- Project-owned pytest warnings fixed:
  - pandas `FutureWarning`
  - invalid escape `SyntaxWarning`
  - pytest return-value warnings
- Remaining pytest warnings observed: 3 third-party `DeprecationWarning` warnings from installed `polygon` / `websockets` packages.
- No broad project warning suppression was added.

## No-Network Evidence

- Default pytest includes an autouse socket guard.
- Focused network guard tests prove external `create_connection`, `connect`, and `connect_ex` attempts are blocked.
- An early focused run exposed a blocked Polygon socket attempt from `tests/test_integration_core_pipeline.py`; that test was then converted to deterministic fixture data.
- No external connection was allowed to complete.
- No market-data provider, OpenAI, Polygon, Yahoo Finance, broker, or external service check was deliberately run.

## Working-Tree Behavior

- `test_outputs` stayed unchanged after the focused and full pytest runs.
- `compileall` did not modify tracked files.
- `pip check` did not modify tracked files.
- Generated local `marketflow.egg-info/` exists only as ignored generated metadata.
- Final working tree contains intentional implementation, documentation, test, manual-check reclassification, and staged generated-metadata removal changes only.

## Independent Reviews

Reviewer A:

- High: `pip check` is not clean because `streamlit` is not installed. Disposition: unresolved blocker; dependency changes are out of scope.
- Medium: `setup.py` silently fell back when `requirements.txt` was unreadable. Disposition: fixed.
- Medium: tracked report-path assurance covered only NVDA files. Disposition: fixed by deriving tracked report paths from `git ls-files test_outputs`.

Reviewer B:

- High: final status document missing. Disposition: fixed by this document.
- Medium: pure query-engine checks were moved to manual scripts without deterministic replacements. Disposition: fixed with `tests/test_query_engine_unit.py`.
- Medium: manual provider script could exit zero after provider failures. Disposition: fixed for `data_provider_simple_check.py`.
- Medium: Wyckoff warning-fix assurance did not protect the approved change boundary. Disposition: fixed with a narrow diff assertion.
- Low: stale manual script run instruction. Disposition: fixed.

## Strategy Scope

No changes were made to `marketflow/marketflow_strategy.py`, Strategy Ranking formulas, candidate scoring, risk/reward calculations, target or stop calculations, ATR or volatility semantics, Wyckoff event-detection semantics, event recency rules, Monte Carlo semantics, Point-and-Figure semantics, Eigen/PCA calculations, walk-forward candidate-generation semantics, outcome labels, ranking thresholds, trading recommendations, trade execution, or broker integration.

The only Wyckoff source change is the approved annotation dtype fix for warning cleanup.

## Deferred Strategy Issues

The following strategy concerns were recorded as deferred and were not fixed or validated in this task:

- cross-ticker/timeframe CSV fallback
- circular risk/reward target construction
- high-low volatility instead of true range
- stale Wyckoff event reuse
- missing evidence treated as neutral evidence
- live ranking versus historical walk-forward alignment

Swing-strategy consistency has not been validated in this phase.

## Commit And Tag

No commit or tag was created.
