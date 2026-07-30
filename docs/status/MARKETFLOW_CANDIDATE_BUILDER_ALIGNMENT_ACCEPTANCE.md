# MarketFlow Candidate Builder Alignment Acceptance

Status: PASS

UTC acceptance date: 2026-07-30T18:14:53Z

Branch: feature/swing-candidate-builder-alignment

Base commit: 00098822c7d782c7f135614df9f4e8fac5e3e1d4

Baseline tag at base: v0.1.0-alpha.6-evidence-availability

## Scope

Accepted scope:

- canonical point-in-time candidate-build architecture;
- immutable candidate input request and evidence bundle;
- current ranking, exact-source backtest, and walk-forward wrapper delegation;
- explicit `StrategyConfig` and explicit optional evidence propagation;
- alias normalization required before canonical construction;
- candidate-core parity projection;
- separation of candidate-time and outcome-time data;
- focused tests and status documentation.

Explicit exclusions:

- source-identity semantics;
- entry formula;
- stop formula and multiplier;
- True Range formula;
- volatility window or aggregation;
- structural target calculation or provenance;
- RR formula and minimum-RR gate;
- Wyckoff phase/event classification;
- event recency and supersession;
- phase/event score values;
- Monte Carlo formula or parameters;
- Point-and-Figure calculations;
- trend formula;
- component weights;
- composite-score mathematics;
- score or recommendation thresholds;
- outcome labels and horizons;
- provider, broker, execution, dependency, network, or remote behavior.

## Pre-Refactor Paths

Candidate-time semantics were previously split across these paths:

- `marketflow.marketflow_strategy.rank_long_candidates` resolved source identity, loaded the selected Strategy CSV, used the final row as the decision row, and computed phase, event recency, volatility, entry, stop, target, RR, evidence components, composite score, and rank eligibility.
- `marketflow.services.backtest_candidate_service` normalized selected Strategy candidate dictionaries, enriched signal rows and event diagnostics from source context, validated levels, and serialized snapshot fields.
- `marketflow.services.walk_forward_validation_service` selected historical rows, independently resolved event, target, RR, and score diagnostics, then attached future-window metadata for outcome evaluation.
- Backtest outcome services, walk-forward artifact services, Studio, and reports consumed or flattened candidate dictionaries and snapshots.

Reproduced divergences and duplication risks:

- Walk-forward diverged from ranking/backtest for the same prefix and evidence in stop loss, RR, volatility diagnostics, POP/PnF evidence status, score status, composite score, rank eligibility, and active evidence profile.
- Backtest could preserve or reconstruct candidate fields without being forced through the current ranking candidate builder.
- Independent wrapper calculations created a risk that future rows, legacy fields, or wrapper defaults could alter candidate-time semantics.

## Canonical Contract

Canonical input contract:

- `CandidateBuildRequest` is frozen and includes validated `StrategyDatasetIdentity`, chronological `data_prefix`, explicit `StrategyConfig`, explicit `CandidateEvidenceInputs`, safe source/report references, source status, and candidate source label.
- The prefix ends at the decision row. Future rows, outcome labels, MFE/MAE, TP/SL result, future exit timestamp, realized result, provider clients, and unrelated filesystem paths are excluded.
- Wrappers validate source identity and slice historical prefixes before calling the builder.

Canonical builder:

- `build_candidate_from_prefix` is the authoritative production candidate-time builder.
- It orchestrates decision-row context extraction, phase/event diagnostics, True Range volatility, entry, stop, structural target, RR, evidence availability, active evidence profile, composite score, rank eligibility, and fixed candidate reasons.
- It opens no provider connection, discovers no alternate dataset, reads no future outcome, and returns one candidate core or one fixed invalid result.

Canonical candidate core:

- Carries ticker, timeframe, source status, safe source references, signal row/timestamp, phase/event diagnostics, volatility, entry, stop, target, RR, evidence diagnostics, score diagnostics, rank eligibility, and reasons.
- Contains no future-outcome fields or wrapper run/campaign/case metadata.
- Invalid canonical builds clear `rank_eligible`.
- Malformed prefixes, including prefixes without canonical `close`, fail closed instead of raising raw exceptions.

Configuration and evidence:

- Candidate-affecting `StrategyConfig` fields are explicit, including ATR length, stop ATR multiplier, minimum RR, event age policy, MC/PnF enablement, POP thresholds, component weights, and score/recommendation fields used at candidate-build time.
- Explicitly different configs may produce different cores.
- Missing POP/PnF does not become neutral evidence. Valid neutral evidence remains valid only with an available evidence status.

Alias normalization:

- Walk-forward normalizes accepted OHLC, phase, confirmed-event, and timestamp aliases before canonical construction.
- Invalid signal-row indices fail rather than clamp.
- Timestamp/index mismatch fails closed.
- Conflicting aliases fail closed and do not overwrite canonical values.
- Raw event filters can select rows but do not upgrade raw events into confirmed event evidence.

## Wrapper Delegation

Current ranking:

- Resolves strict source identity, loads the exact source, passes the full current prefix, explicit config, and optional MC evidence to `build_candidate_from_prefix`, then filters/sorts returned candidate cores.
- It does not recompute target, stop, RR, event, evidence, score, or rank eligibility after the builder.

Backtest:

- Exact-source snapshots rebuild from the historical source prefix through the signal row and call `build_candidate_from_prefix`.
- Rejected, unavailable, invalid, or mismatched canonical prefixes fail closed.
- Legacy target, stop, RR, score, POP/PnF, event, and volatility values cannot override a rebuilt canonical core.
- Outcome evaluation remains separate.

Walk-forward:

- Identifies row T, validates the signal index, slices rows `<= T`, normalizes aliases, passes explicit config/evidence to the builder, freezes the candidate core, and passes rows `> T` only to outcome evaluation.
- Future rows cannot alter phase/event, event age, volatility, stop, target, RR, evidence status, score, or rank eligibility.

## Acceptance Results

Parity matrix:

- Direct canonical build, current ranking, exact-source backtest, and walk-forward produce identical semantic projections for the complete covered candidate when source identity, prefix, config, and explicit evidence match.
- Failure parity is covered for exact-source rebuild failures, canonical POP rejection propagation, invalid signal rows, timestamp mismatch, alias conflicts, malformed prefixes, target unavailable, invalid OHLC, event recency, evidence availability, and source-identity failures.

Future-row invariance:

- Candidate core remains identical when future rows contain altered closes, volatility-looking values, later PnF values, or later events, as long as the decision prefix is unchanged.
- Only separate outcome objects may use future rows.

Outcome separation:

- Candidate-time and outcome-time data remain structurally separate.
- TP/SL ordering, MFE, MAE, future horizon, time exit, and realized diagnostics do not mutate entry, stop, target, RR, phase, event, volatility, evidence, score, rank eligibility, or candidate reasons.

Legacy artifacts:

- Legacy numeric scores cannot create current candidate cores.
- Legacy target, stop, RR, POP/PnF, event, and volatility fields cannot bypass exact-source canonical rebuilds.
- Missing or unsafe source context fails closed or remains non-actionable.
- Old artifacts are not rewritten automatically.

Studio and reporting:

- Existing Studio/report surfaces consume flattened candidate/snapshot fields.
- They do not reconstruct score, event status, volatility, stop, target, RR, evidence completeness, or rank eligibility.
- Missing and incomplete values remain visible and non-actionable.

Formula and threshold non-regression:

- Source identity, entry, stop, True Range volatility, structural target, RR, minimum RR, event recency/supersession, MC/PnF calculations, trend, weights, composite score, recommendation thresholds, and outcome definitions were not tuned or semantically changed.

Previous integrity non-regression:

- Source identity, risk/reward integrity, True Range volatility, Wyckoff event recency, evidence availability, and baseline integrity tests remain part of the passing focused and full suites.
- No provider, broker, network, or execution path was added or exercised.

## Verification

Focused tests:

- Command: `env\Scripts\python.exe -m pytest tests/test_candidate_builder_alignment.py tests/test_backtest_candidate_service.py tests/test_backtest_candidate_artifact_service.py tests/test_backtest_service.py tests/test_backtesting_outcome_engine.py tests/test_backtest_result_service.py tests/test_walk_forward_validation_service.py tests/test_walk_forward_validation_artifact_service.py tests/test_walk_forward_run_registry_service.py tests/test_evidence_availability.py tests/test_risk_reward_integrity.py tests/test_true_range_volatility.py tests/test_wyckoff_event_recency.py tests/test_source_assurance.py tests/test_strategy_source_csv_selection.py tests/test_strategy_service_source_identity.py -q`
- Result: 295 passed, 3 warnings.

Full suite:

- Collection: 520 tests collected.
- Full default suite: 520 passed.
- Test count explanation: accepted baseline was 505 tests; current count is 520 tests; the 15-test increase is focused candidate-builder alignment and regression coverage.

Warnings:

- Only the three accepted third-party polygon/websockets deprecation warnings remain.
- No project-owned warnings were introduced.

Dependency and compile checks:

- `env\Scripts\python.exe -m pip check`: passed.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed.
- `git diff --check`: passed.

No-network and clean-test-output evidence:

- No manual provider check, broker check, real-market check, network check, dependency installation, or dependency modification was run.
- Git status before and after the full suite matched; default tests did not modify tracked files.

## Reviewer Findings

Reviewer A:

- High: exact-source backtest ignored canonical builder rejection.
- High: canonical builder could raise on malformed prefixes without `close`.
- Disposition: fixed by failing exact-source backtest snapshots when canonical build rejects and by making missing `close` fail closed.

Reviewer B:

- Critical: invalid canonical builds could remain actionable in wrappers.
- High: status documentation stale.
- High: tests lacked canonical rejection propagation coverage.
- Disposition: fixed by clearing rank eligibility for invalid canonical builds, adding rejection propagation tests, and refreshing status/acceptance docs.

No critical or high finding remains open.

## Remaining Limitations

- This acceptance proves candidate-builder consistency, not profitability.
- Historical outcome validity remains separate from candidate-builder acceptance.
- Predictive usefulness is not accepted.
- The complete swing strategy is not yet accepted.

Deferred issues:

- predictive applicability for days/weeks;
- timeframe/profile calibration;
- recommendation-threshold calibration for alternate profiles;
- minimum evidence-coverage calibration;
- volatility-window calibration;
- stop-multiplier calibration;
- event-age calibration;
- structural event invalidation;
- structural target-quality calibration.

Final acceptance statement:

- Candidate-builder consistency is accepted.
- Historical outcome validity remains separate.
- Predictive usefulness is not accepted.
- The complete swing strategy is not yet accepted.
