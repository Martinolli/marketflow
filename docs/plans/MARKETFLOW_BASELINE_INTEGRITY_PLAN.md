# MarketFlow Baseline Integrity Plan

## Observed Baseline

- Starting branch expected: `feature/swing-consistency-audit`.
- Starting commit expected: `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.
- Starting working tree expected: clean.
- Initial observed baseline from task request:
  - `pip check` reports malformed MarketFlow dependency metadata.
  - `pytest` reports 373 passed with 24 warnings.
  - `compileall` passes with two `SyntaxWarning` messages.
  - The full suite modifies three tracked NVDA report artifacts.

## Scope

- Correct Python packaging metadata source and generated-artifact tracking.
- Make default tests deterministic, hermetic, and offline.
- Isolate generated test outputs from tracked files.
- Remove false-positive pytest behavior.
- Clean project-owned warnings.
- Add offline/no-network assurance and baseline documentation.

## Exclusions

- No Strategy Ranking formula changes.
- No candidate scoring changes.
- No risk/reward, target, stop, ATR, volatility, Wyckoff event, event recency, Monte Carlo, Point-and-Figure, Eigen/PCA, walk-forward generation, outcome label, ranking threshold, recommendation, broker, provider, or execution behavior changes.
- No dependency installation, upgrade, downgrade, or removal.
- No network or market-provider calls.
- No commit or tag.

## Packaging Remediation Approach

- Inspect `setup.py`, `requirements.txt`, tracked `marketflow.egg-info`, and installed editable metadata.
- Treat `setup.py` and `requirements.txt` as authoritative unless a minimal source correction is required.
- Remove generated package metadata from tracking if confirmed generated and malformed.
- Add ignore patterns for generated packaging artifacts.
- Validate requirements with the installed packaging parser.
- Generate metadata into a temporary directory for validation only.
- Refresh the local editable install offline only if malformed installed metadata remains after the source fix.

## Test Isolation Approach

- Remove repository-relative test-output side effects.
- Use pytest-managed temporary directories for integration report output.
- Preserve report-generation assertions while ensuring tracked `test_outputs` artifacts are not modified.
- Add regression coverage for import/run behavior around tracked report paths.

## Manual/Network Test Classification

- Reclassify real-provider checks as explicit manual scripts outside default pytest collection.
- Preserve deliberate manual exit behavior.
- Document credentials, provider, and network expectations for manual checks.
- Add deterministic tests around pure validation or routing logic where useful.

## Warning-Remediation Approach

- Fix project-owned pandas `FutureWarning` with stable dtype handling while preserving phase labels and `UNKNOWN` fallback.
- Fix invalid escape `SyntaxWarning` instances with raw strings or escaped backslashes.
- Remove pytest return-value warnings by ensuring collected tests assert and return `None`.
- Do not add broad global warning suppressions for project-owned issues.

## Verification Commands

Use:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m pip check
& $python -m pytest -q
& $python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
& $python -m pytest --collect-only -q
```

Focused checks will cover packaging integrity, network denial, temporary report output, manual-check exclusion, and Wyckoff annotation warnings.

## Expected Test-Count Changes

- The baseline default suite is expected to start at 373 passing tests with warnings.
- Reclassifying real-market provider checks may reduce collected tests.
- New deterministic packaging, no-network, report-isolation, and source-assurance tests may offset that reduction.
- Any final count change will be documented explicitly with cause.

## Stop Conditions

Stop blocked without committing if branch or starting commit is wrong, the initial tree is dirty, a network call occurs, dependencies are installed or changed, metadata remains malformed, generated metadata remains tracked, pytest return values remain, default tests modify tracked files, manual network checks remain collected, project-owned warnings remain, full tests fail, `compileall -W error` fails, test-generated tracked modifications occur, strategy semantics change, or critical/high reviewer findings remain unresolved.
