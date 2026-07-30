# MarketFlow Risk/Reward Integrity Status

Date: 2026-07-29
Branch: feature/swing-risk-reward-integrity
Starting commit: 2ccaa223d4a193d655713285291d04267637f79a
Starting tag: v0.1.0-alpha.2-source-identity

## Result

PASS.

The circular long-target construction was reproduced before correction and removed from the Strategy and walk-forward candidate paths. Long targets now resolve from the existing Wyckoff trading-range high (`tr_high`) as a structural resistance source. Minimum RR is now only a gate against the realized ratio computed from entry, stop, and target.

## Baseline Reproduction

Before production edits, the baseline `_derive_sl_tp_long` behavior was reproduced with deterministic prefix data:

- entry: 100.0
- stop: 95.0
- min_rr 2.0 produced target 110.0 and RR 2.0
- min_rr 3.0 produced target 115.0 and RR 3.0

This confirmed the target was derived from the threshold instead of an independent market structure level.

## Correction Summary

- `marketflow/marketflow_strategy.py`
  - Added target and RR status constants.
  - Added target and trade-level resolution result structures.
  - Replaced circular `tp = close + cfg.min_rr * (close - sl)` behavior with structural `tr_high` target resolution.
  - Preserved long entry and stop semantics.
  - Changed RR calculation to fail closed for non-finite, non-positive, or invalid long geometry instead of silently repairing values.
  - Kept score, phase, event, P&F, POP, and trend scoring semantics unchanged.

- `marketflow/services/walk_forward_validation_service.py`
  - Replaced `entry + risk_reward * risk` target construction with the same structural target resolution.
  - Passed a decision-row prefix frame to target resolution.
  - Stored truthful target and RR status fields in candidate rows.

- `marketflow/marketflow_wyckoff_confirmation_adapter.py`
  - Emitted `tr_low` and `tr_high` as point-in-time row values instead of assigning one full-frame trading range to every row.

- Reporting and snapshot propagation
  - Added optional target/RR status fields to Strategy, walk-forward case artifacts, and backtest candidate snapshots/CSVs.

## Source Assurance

Independent review subagents were used.

Findings addressed:

- Walk-forward `rr_status` now carries the target failure status when target resolution fails.
- Behavioral coverage now explicitly reproduces the old circular formula.
- Walk-forward and backtest propagation tests now assert target/RR metadata preservation.
- Wyckoff TR column output now has point-in-time coverage.

Known boundary:

- `CandidateSnapshot` dataclass fields remain unchanged. The target/RR metadata is preserved in dict and CSV artifact surfaces only.

## Validation

Final validation completed after implementation:

- `python -m pip check`: pass.
- `python -m pytest --collect-only -q`: 423 tests collected.
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: pass.
- Focused risk/reward, propagation, leakage, source-identity, network-guard, and source-assurance tests: 195 passed.
- Full default pytest suite: 423 passed.

The pytest runs reported three third-party deprecation warnings from Polygon/websockets imports.

No commit, tag, push, dependency install, or network data retrieval was performed.
