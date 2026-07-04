# MARKETFLOW_TESTING_BASELINE_CHECKPOINT

## 1. Purpose

This checkpoint records the current MarketFlow test-health baseline after cleanup stabilization.

This is documentation only. No code changes, test changes, pytest configuration changes, or dependency changes are made here. Use this baseline for future regression comparison before returning to feature work.

## 2. Current Commit

```text
a75524d - Reconcile remaining active pytest failures
```

## 3. Testing Baseline Summary

```text
pytest collection: passes
full pytest: passes
active failures: none
known skips: 2
known warnings: 26
```

## 4. Verified Commands

| Command | Result |
| --- | --- |
| `python -m pytest tests\test_data_provider.py -q` | `2 passed` |
| `python -m pytest tests\test_wyckoff_phases.py -q` | `2 passed` |
| `python -m pytest tests\test_llm_interface.py -q` | `16 passed` |
| focused backtest tests | `41 passed` |
| `python -m pytest --collect-only -q` | `131 tests collected` |
| `python -m pytest -q` | `129 passed, 2 skipped, 26 warnings` |
| `git diff --check` | passed, CRLF warnings only |

Focused backtest command:

```powershell
python -m pytest tests\test_backtest_candidate_artifact_service.py tests\test_backtest_candidate_service.py tests\test_backtest_service.py tests\test_backtesting_outcome_engine.py -q
```

## 5. What Was Stabilized

- Deprecated backup test collection blockers were renamed to manual scripts.
- `scripts/__init__.py` was added for repo-local script imports.
- LLM interface tests were reconciled with current behavior.
- Data provider test now matches current async-client fetch path.
- Wyckoff phase tests now use deterministic OHLCV synthetic data.
- Production code was not changed during C2.3.

## 6. Remaining Warnings And Skips

Known warning/skip areas:

- deprecated websocket APIs
- pytest return-value warnings
- skipped async tests without async plugin
- pandas future warning
- CRLF working-copy warnings on Windows

These are not blocking failures and may be handled in later cleanup passes.

## 7. Current Cleanup Status

```text
C2.1 completed - deprecated backup collection blockers quarantined
C2.2 completed - LLM interface tests reconciled
C2.3 completed - remaining active pytest failures reconciled
```

## 8. Active Test Health

```text
Full pytest now passes.
No active test failures remain at this checkpoint.
```

## 9. Guardrails For Future Work

- run focused tests after feature work
- run full pytest before major milestones
- do not reintroduce pytest collection blockers
- avoid random/non-deterministic test fixtures unless seeded
- optional broker/API tests should remain opt-in
- deprecated/prototype scripts should not be collected by default

## 10. Recommended Next Work

```text
Return to MarketFlow feature work: implement the Backtest Outcome Result CSV writer/service from `docs/reference/MARKETFLOW_BACKTEST_OUTCOME_RESULT_ARTIFACT_CONTRACT.md`.
```

```text
Later cleanup: review warnings/skips and continue repository cleanup phases.
```

## 11. Final Status

```text
Status: testing baseline checkpoint recorded.
```
