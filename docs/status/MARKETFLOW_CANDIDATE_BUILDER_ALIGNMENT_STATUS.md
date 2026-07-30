# MarketFlow Candidate Builder Alignment Status

Status: PASS, final acceptance gates complete after reviewer fixes.

Date: 2026-07-30

Branch: feature/swing-candidate-builder-alignment

Starting baseline observed locally:

- Commit: 00098822c7d782c7f135614df9f4e8fac5e3e1d4
- Tag at baseline HEAD: v0.1.0-alpha.6-evidence-availability
- Initial working tree: intentionally dirty with candidate-builder alignment files only
- Python: env\Scripts\python.exe, Python 3.12.10

Baseline parity audit before production edits:

- Current ranking and backtest snapshot normalization matched for the audited complete candidate because backtest normalized the ranking candidate.
- Walk-forward candidate generation diverged from ranking/backtest for the same source prefix and evidence inputs.
- Observed walk-forward differences included stop loss, risk/reward, volatility diagnostics, POP/PnF evidence status, score status, composite score, rank eligibility, and active evidence profile.
- Root cause: walk-forward row construction independently computed candidate core fields instead of delegating to the Strategy Ranking point-in-time candidate logic.

Implemented alignment:

- Added immutable `CandidateBuildRequest` and `CandidateEvidenceInputs` plus canonical `build_candidate_from_prefix` in `marketflow/marketflow_strategy.py`.
- Moved long candidate core assembly behind the canonical prefix builder: source identity, signal row/timestamp, entry, stop, target, RR, True Range volatility, Wyckoff phase/event/trend diagnostics, evidence component statuses/scores, composite score, and rank eligibility.
- Refactored `rank_long_candidates` to resolve source files and optional Monte Carlo evidence, then delegate candidate construction to `build_candidate_from_prefix`.
- Refactored exact-source backtest candidate snapshot building to rebuild from the exact source prefix; invalid, unavailable, or rejected canonical prefixes fail closed and cannot validate from stale legacy levels.
- Refactored walk-forward candidate generation to slice rows through the signal row, normalize accepted aliases, call the canonical builder, and attach only wrapper/future-window metadata afterward.
- Added strict signal-row validation: missing, boolean, negative, float, string, and out-of-range indices fail closed. Timestamp/index mismatch fails closed.
- Added alias conflict handling: accepted OHLC, phase, confirmed-event, and timestamp aliases are copied only when unambiguous; conflicting aliases fail closed.
- Preserved outcome separation: rows after the decision point are used only by outcome evaluation.

Verification added/updated:

- Added `tests/test_candidate_builder_alignment.py`.
- Added parity coverage proving direct canonical build, current ranking, backtest rebuild, and walk-forward generation produce the same candidate core for identical source identity, prefix, `StrategyConfig`, and explicit evidence inputs.
- Added future-row invariance coverage, including direct walk-forward calls with a future-containing decision frame.
- Added invalid signal-row, timestamp mismatch, alias normalization, alias conflict, exact-source fail-closed, malformed-prefix fail-closed, and canonical-rejection non-actionability coverage.
- Updated source-assurance tests to verify wrappers delegate to the canonical builder and walk-forward no longer calls target/RR helpers directly.
- Updated legacy walk-forward tests to reflect that raw event filters may select cases but raw-only events are not claimed as confirmed event evidence.

Independent read-only review:

- Reviewer A found two high blockers: exact-source backtest ignored canonical rejection, and malformed prefixes without `close` could raise instead of failing closed.
- Reviewer B found one critical blocker and two high issues: invalid canonical builds could remain actionable in wrappers, the status documentation was stale, and tests lacked rejection propagation coverage.
- Disposition: all blocker findings were fixed. Canonical invalid builds now clear `rank_eligible`; exact-source backtest returns a failed snapshot for rejected canonical builds; malformed prefixes without `close` fail closed; docs and tests were refreshed.

Out of scope and unchanged:

- No strategy formulas, thresholds, RR formulas, True Range volatility formulas, event recency rules, score weights, provider behavior, broker/execution behavior, dependency installation, tag, push, or remote changes were made.
- Walk-forward future-window and outcome evaluation remain outside the candidate core builder.
- Predictive usefulness, profitability, timeframe calibration, and complete swing-strategy acceptance are not claimed.

Final acceptance gates:

- `env\Scripts\python.exe -m pip check`: passed.
- Focused matrix: 295 passed.
- `env\Scripts\python.exe -m pytest --collect-only -q`: passed, 520 tests collected.
- `env\Scripts\python.exe -m pytest -q`: passed, 520 tests passed.
- Warnings: only the three accepted third-party polygon/websockets deprecation warnings.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed.
- `git diff --check`: passed.
- Git status before and after the full suite matched; tests did not modify tracked files.

Test count explanation:

- Accepted baseline collected 505 tests.
- Current collection is 520 tests.
- Increase of 15 tests comes from new candidate-builder alignment/regression coverage in `tests/test_candidate_builder_alignment.py`, including parity, future invariance, invalid signal rows, timestamp mismatch, alias conflict, canonical rejection propagation, malformed-prefix fail-closed behavior, exact-source fail-closed behavior, and delegation source assurance.
