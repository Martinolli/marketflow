# MarketFlow Baseline Integrity Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-29T17:30:36Z`
- Branch: `feature/swing-consistency-audit`
- Base commit: `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`
- Commit intent: local commit only
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope

Accepted scope:

- `AGENTS.md` safety rules
- baseline-integrity plan, status, acceptance, and testing documentation
- generated `marketflow.egg-info` removal and ignore rules
- minimal packaging source corrections
- manual/network test reclassification
- deterministic replacement tests
- default socket-denial guard
- temporary report-output isolation
- source-assurance tests
- project-owned warning cleanup
- README/testing documentation updates

Exclusions:

- no Strategy Ranking formula changes
- no candidate scoring changes
- no risk/reward calculation changes
- no target or stop calculation changes
- no ATR or volatility semantic changes
- no Wyckoff event semantic changes
- no event recency changes
- no Monte Carlo semantic changes
- no Point-and-Figure semantic changes
- no Eigen/PCA semantic changes
- no walk-forward semantic changes
- no outcome-label changes
- no recommendation-threshold changes
- no broker integration, trade execution, provider call, or live-network check

## Original Baseline Observations

- `pip check` reported malformed MarketFlow dependency metadata.
- Default pytest baseline was recorded as `373 passed, 24 warnings`.
- `compileall` passed but emitted two invalid escape `SyntaxWarning` messages.
- Full pytest modified tracked NVDA report artifacts under `test_outputs`.

## Packaging Root Cause

Tracked generated `marketflow.egg-info` metadata was incorrectly treated as source-controlled content. Its `PKG-INFO` contained quoted/list-style dependency metadata, causing pip to interpret the `Requires-Dist` block as an invalid requirement rather than parse normal line-oriented requirements.

## Packaging Disposition

- `marketflow.egg-info` files were removed from Git tracking.
- Local regenerated `marketflow.egg-info/` remains ignored generated metadata.
- `*.egg-info/`, `*.dist-info/`, `build/`, and `dist/` are ignored.
- `setup.py` and `requirements.txt` remain authoritative.
- `setup.py` no longer silently falls back if `requirements.txt` is missing.
- Requirement lines are strictly parseable.
- Generated metadata is validated into temporary/ignored locations only.
- No dependency version was changed by Codex to make checks pass.
- `git ls-files marketflow.egg-info build dist "*.dist-info"` returned no tracked generated packaging files.

Package metadata evidence:

- `pip show marketflow`: version `0.1.0`, editable package, requires `streamlit`.
- `pip show streamlit`: version `1.45.1`, required by `marketflow`.
- `pip check`: `No broken requirements found.`

Absolute install paths are intentionally omitted from this document.

## Environment Metadata Refresh History

The local editable MarketFlow metadata was refreshed offline after the source metadata fix with:

```powershell
& $python -m pip install --no-index --no-deps --no-build-isolation --disable-pip-version-check -e .
```

Codex did not install, upgrade, downgrade, or remove dependencies. The later `streamlit==1.45.1` environment fix was performed outside Codex before this acceptance pass.

## Manual-Test Reclassification

Provider/manual/observational scripts were moved out of default pytest collection and retained under:

```text
scripts/manual_checks/
```

They are documented in `docs/testing/MANUAL_NETWORK_CHECKS.md` as manual checks requiring explicit invocation and possible credentials/network access. They were not run during acceptance and are not deterministic release evidence.

Removed default-collection tests were unsuitable for the deterministic release gate because they were provider/manual/network-oriented observational checks, script-style boolean-return checks, dependent on uncontrolled external state, or otherwise not reliable unit tests.

Deterministic replacement coverage was added for:

- packaging metadata integrity
- offline socket denial
- source assurance
- temporary report output
- manual-check collection exclusion
- pure query-engine input validation, ticker extraction, and intent parsing
- Wyckoff phase annotation warning regression

## Test Count

- Original default count: `373`
- Tests removed from default collection: `22`
- Deterministic tests added: `21`
- Final default count: `372`

Collection command result:

```text
372 tests collected
```

The removed checks are not described as passing unit tests; they were manual or false-positive default-suite checks.

## No-Network Controls

- Default pytest patches `socket.create_connection`, `socket.socket.connect`, and `socket.socket.connect_ex`.
- Focused network tests assert external socket attempts are blocked before connection.
- No ordinary default-test opt-out weakens the guard.
- Manual network scripts live outside default pytest collection.
- No real provider/API/manual check was run.
- No network/provider call was allowed to complete during acceptance.

## Test-Output Isolation

- `tests/test_integration_core_pipeline.py` writes report output under pytest `tmp_path`.
- Importing the integration test does not create repository-relative output directories.
- Report generation remains tested with deterministic facade-shaped data.
- Production report paths were not changed.
- `test_outputs/NVDA_report.html`, `test_outputs/NVDA_report.json`, and `test_outputs/NVDA_summary_report.txt` were not modified by the full suite.
- `git status --short test_outputs` was empty after full pytest.

## Warning Findings

Project-owned warnings resolved:

- pandas `FutureWarning` in Wyckoff phase annotation fixed through stable `dtype="string"` handling.
- `UNKNOWN` fallback remains unchanged.
- Wyckoff phase labels remain covered by existing regression fixtures.
- invalid escape warnings in `scripts/monte_carlo_trade.py` and `rag/chunker.py` fixed by raw docstring handling only.
- command examples remain unchanged.
- pytest return-value warnings removed by moving boolean-return manual checks out of default collection and adding source-assurance coverage.

Remaining pytest warnings:

- count: `3`
- source: installed `polygon` and `websockets` deprecation warnings

No broad warning suppression was added.

## Verification Results

Required final checks:

```text
pip check: No broken requirements found.
pytest --collect-only -q: 372 tests collected
pytest -q: 372 passed, 3 warnings
compileall -W error: passed
focused integrity suite: 29 passed, 3 warnings
git diff --check: passed
```

The `git diff --check` output only contained line-ending normalization notices from Git for edited text files; it returned success and reported no whitespace errors.

## Pre/Post-Test Git Status

Pre-full-suite and post-full-suite `git status --short` matched. The status contained only intentional baseline-integrity changes:

- documentation and repository rules
- packaging source and ignore-rule changes
- tracked generated `marketflow.egg-info` removal
- manual-check relocation
- deterministic tests and pytest socket guard
- report-output isolation and warning cleanup

No tracked file changes were produced by the test run.

## Source-Semantic Boundary

- `marketflow/marketflow_strategy.py` is byte-identical to the base commit.
- The `marketflow/marketflow_wyckoff.py` diff is limited to stable dtype handling for `phase_series` plus final newline normalization.
- `UNKNOWN` fallback remains present.
- Source-assurance tests protect strategy-file diff boundaries and the Wyckoff annotation dtype contract.

No change was made to:

- strategy scoring
- risk/reward
- target or stop
- ATR/volatility
- event recency
- walk-forward generation
- Monte Carlo
- Point-and-Figure
- Eigen/PCA
- recommendations

## Independent Reviews

Reviewer A:

- Critical/high/medium findings: none.
- Confirmed packaging correctness, generated-artifact disposition, test-output isolation, no-network guard, and pre/post-test cleanliness.

Reviewer B:

- High: dirty-tree-dependent Wyckoff source-assurance test would fail after commit. Disposition: fixed by replacing diff-expectation logic with committed-source contract assertions.
- High: final acceptance document missing. Disposition: fixed by this document.
- Medium: protected strategy-file assurance checked only unstaged changes. Disposition: fixed by checking `git diff HEAD --name-only`.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- Remaining pytest warnings are third-party deprecations from installed `polygon` and `websockets`.
- Manual provider and LLM checks remain observational and outside the deterministic release gate.
- Swing-strategy consistency and predictive applicability have not yet been accepted.

## Deferred Strategy Issues

- cross-ticker/timeframe CSV fallback;
- circular risk/reward target construction;
- high-low volatility instead of true range;
- stale Wyckoff event reuse;
- missing evidence treated as neutral evidence;
- live ranking versus historical walk-forward alignment.

## Final Acceptance Statement

The baseline-integrity remediation is accepted for local commit. This acceptance does not validate swing-strategy consistency, predictive applicability, trading recommendations, broker integration, or execution behavior.
