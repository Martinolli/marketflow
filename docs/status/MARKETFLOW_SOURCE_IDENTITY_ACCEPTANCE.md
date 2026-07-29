# MarketFlow Source Identity Acceptance

## Decision

PASS.

## Acceptance Metadata

- UTC acceptance date: `2026-07-29T18:42:59Z`
- Branch: `feature/swing-source-identity`
- Base commit: `f3c2ca8f841030c46657332371b155ad6bd81e68`
- Commit intent: local commit only
- Tag: not created
- Push: not performed
- Remote configuration: not changed

## Scope

Accepted scope:

- strict Strategy Ranking ticker/timeframe source identity;
- source-resolution failure handling before CSV loading and scoring;
- truthful candidate ticker/timeframe labels from validated source identity;
- source path confinement for Strategy Ranking, Studio, and Strategy candidate reopen flows;
- explicit walk-forward CSV filename identity validation;
- focused deterministic tests and source-assurance coverage;
- documentation of the accepted source-identity boundary.

Exclusions:

- no candidate score formula changes;
- no score weight changes;
- no score normalization changes;
- no trend calculation changes;
- no Wyckoff phase or event detection changes;
- no Wyckoff event recency changes;
- no volatility or ATR calculation changes;
- no stop, target, or risk/reward calculation changes;
- no Monte Carlo, Point-and-Figure, or Eigen/PCA semantic changes;
- no walk-forward decision-row slicing or future-outcome logic changes;
- no candidate threshold, outcome label, recommendation, or long/short eligibility changes;
- no broker integration or execution functionality.

## Exact Pre-Fix Defect

The reproduced defect used a request for ticker `AAA` and timeframe `4h` while the exact `AAA` / `4h` dataset was absent. The available dataset was:

```text
BBB_4h_wyckoff_annotated.csv
```

Previous behavior allowed the `BBB` dataset to be selected through a timeframe-only fallback and then reported under the `AAA` request. The correction removes the fallback at source resolution. In the final behavior, `BBB` data is never opened for the `AAA` request, no score is calculated, no entry is calculated, no stop is calculated, no target is calculated, no risk/reward value is calculated, and the candidate cannot enter ranked output as a valid candidate.

## Affected Production Paths

- `marketflow/marketflow_strategy.py`
- `marketflow/services/strategy_service.py`
- `marketflow/services/backtest_candidate_service.py`
- `marketflow/services/backtest_result_service.py`
- `marketflow/services/walk_forward_validation_service.py`
- `apps/marketflow_studio.py`

## Identity Model

The authoritative Strategy Ranking source identity is represented by immutable dataclasses:

- `StrategyDatasetIdentity`
- `StrategySourceResolution`

The identity contains canonical ticker, canonical timeframe, validated source path, source kind, and fixed resolution status. It does not contain candidate score, recommendation, entry, stop, target, risk/reward, provider credentials, market-data results, or an absolute private path in normal public output.

CSV files in the reviewed paths do not carry reliable embedded ticker/timeframe metadata. For this release, identity is established by strict source filename resolution and report-root path validation. The implementation does not insert requested labels into a DataFrame and then treat them as identity evidence.

## Normalization Rules

Ticker normalization:

- empty ticker fails;
- surrounding whitespace fails;
- path separators fail;
- control characters fail;
- unsupported characters fail;
- allowed characters are `A-Z`, `0-9`, `.`, `_`, `-`, and `:`;
- case is canonicalized to uppercase;
- `A`, `AA`, `AAA`, `AI`, and `AT` remain distinct;
- substring matching is absent.

Timeframe normalization:

- empty timeframe fails;
- surrounding whitespace fails;
- accepted tokens are `1mo`, `1w`, `1d`, `4h`, `2h`, `1h`, `30m`, `15m`, `5m`, and `1m`;
- case is canonicalized to lowercase;
- `1h` cannot match `4h`, `1d` cannot match `1w`, and `30m` cannot match another minute interval;
- substring matching is absent;
- displayed candidate timeframe comes from validated source identity.

## Resolution Rules

Exactly one matching identity selects only that regular `.csv` source.

Zero matches return fixed safe failure `DATASET_NOT_FOUND`. The candidate is skipped before CSV loading and before all strategy calculations.

More than one exact matching identity returns `DATASET_IDENTITY_AMBIGUOUS`. The resolver does not choose by file order, modification time, canonical/raw preference, first match, latest match, or shortest name.

The resolver does not fall back to timeframe-only, ticker-only, first CSV, latest CSV, similar ticker, substring, or best-effort alternatives.

## Path And Reopen Safety

Selected Strategy Ranking sources must be regular `.csv` files inside the approved report folder. Source resolution rejects directories, missing files, non-CSV files, traversal, and symlink or junction escapes where testable.

Candidate output uses relative source references and source filenames. Studio and backtest candidate flows resolve Strategy candidate source context under the configured report root before reopening. A candidate-provided validated `source_report_dir` is preserved, with UI report directory used only as a fallback when source context is missing.

## Candidate Labels And Batch Findings

Successful Strategy Ranking candidates derive ticker and timeframe from validated source identity. Requested labels cannot override validated labels. Source-resolution failures do not produce score, close, stop, target, risk/reward, POP, phase, event, or trend fields and do not appear as successful ranked candidates.

Focused tests cover a batch with one exact valid identity, one missing identity, one wrong-ticker same-timeframe source, one wrong-timeframe same-ticker source, and one ambiguous duplicate identity. Invalid candidates are skipped independently, do not change the valid candidate score or ordering, and cannot borrow another candidate's source.

## Backtest And Walk-Forward Findings

Backtest candidate source-context reopen now resolves inside the configured report root when Strategy source context exists, rejects root escape, and preserves the candidate source report directory when a separate UI report directory is supplied as fallback. Backtest outcome evaluation now also resolves relative Strategy snapshot source context inside the configured report root before reopening a source CSV.

Walk-forward validation receives explicit CSV paths. It now validates caller ticker/timeframe labels against filename identity and fails closed with `DATASET_IDENTITY_MISMATCH` or `DATASET_IDENTITY_UNKNOWN`. It does not discover an alternate CSV on mismatch. Decision-row slicing, future-window outcome logic, and no-future-leakage behavior remain unchanged.

## Studio Findings

Studio source prefill now uses the Strategy candidate source context when present, resolves the reopened CSV under the configured report root, rejects escaped or missing paths, and returns no unvalidated path for source-context candidates. It does not select the first same-timeframe file and does not hide source identity as a successful candidate.

## Verification Results

Required final checks:

```text
pip check: No broken requirements found.
focused source-identity suite: 100 passed, 3 warnings
pytest --collect-only -q: 403 tests collected
pytest -q: 403 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
```

The test count increased from the prior 395-test verification to 403 because reviewer-driven regressions were added for generated artifact exclusion, escaping date-glob rejection, valid batch-folder filtering, preserving and reopening validated Strategy candidate `source_report_dir` context, and walk-forward unknown identity failure. The focused source-identity count increased to 100 because the focused set now includes backtest outcome source-context coverage.

Warnings remain the accepted third-party `polygon` / `websockets` deprecations. No project-owned warnings were introduced.

## No-Network Evidence

The default pytest socket guard remained active. No manual provider checks were run, no network/provider call was allowed to complete, and no dependency was installed, upgraded, downgraded, or removed by this acceptance pass.

## Pre/Post-Test Git Status

Pre-full-suite and post-full-suite `git status --short` matched. The full suite did not modify tracked files.

## Strategy-Semantic Non-Regression

All `marketflow/marketflow_strategy.py` hunks were classified as source discovery, identity validation, source-resolution failure handling, truthful labeling, or sanitized source reference. No hunk changed candidate score components, score weights, ranking calculation, target or stop calculation, risk/reward calculation, high-low volatility behavior, Monte Carlo, Point-and-Figure, trend placeholder, event extraction, or recommendation thresholds.

Source-assurance tests protect the unchanged Strategy Ranking and walk-forward semantic functions against unintended diff.

## Reviewer Findings And Dispositions

Prior Reviewer A findings:

- High: canonical/raw duplicate identity could select one file. Disposition: fixed with `DATASET_IDENTITY_AMBIGUOUS`.
- High: Strategy candidate CSV reopen paths were not scoped to report root. Disposition: fixed in Studio and backtest candidate resolution.
- High: walk-forward caller labels could override source identity. Disposition: fixed with explicit filename identity validation.
- Medium: ranking directory lookup used raw requested ticker before canonical validation. Disposition: fixed.
- Medium: diagnostics still reported timeframe-only matches. Disposition: fixed.

Prior Reviewer B findings:

- High: service-level whitespace normalization could bypass fail-closed rules. Disposition: fixed.
- High: canonical/raw duplicate identity could select one file. Disposition: fixed.
- High: source-identity status documentation was missing. Disposition: fixed.
- Medium: diagnostics used timeframe-only matching and stale fallback wording. Disposition: fixed.
- Final-review High: Studio Strategy candidate reopen path needed explicit root confinement for `source_report_dir`. Disposition: fixed.
- Final-review Medium: walk-forward caller labels could still be used when filename identity was incomplete. Disposition: fixed with `DATASET_IDENTITY_UNKNOWN`.
- Final-review Medium: plan text still described canonical preference over raw for the same identity. Disposition: fixed.

Current acceptance review finding:

- Medium: backtest snapshot construction overwrote a candidate-provided `source_report_dir` when a UI report directory fallback was supplied. Disposition: fixed; candidate source context now wins, with focused regression coverage.
- High: escaping `date_glob` and batch-like summary folders could become Strategy source roots. Disposition: fixed with safe date-glob validation, report-root-constrained directories, valid batch-run filtering, and focused regression coverage.
- High: backtest outcome evaluation could reopen a Strategy snapshot source without relative source context. Disposition: fixed with report-root source-context resolution and focused regression coverage.
- High: generated walk-forward CSV artifacts could be parsed as Strategy source identities. Disposition: fixed by excluding walk-forward cases, results, and summary artifacts with focused regression coverage.
- High: Studio Monte Carlo prefill could fall back to an unvalidated raw CSV when source-context resolution failed. Disposition: fixed with fail-closed source-context logic and source-assurance coverage.
- Medium: Studio diagnostics still read the removed timeframe-only diagnostic key. Disposition: fixed with strict source status/reason/name reporting.
- Medium: semantic-baseline tests compared protected functions to moving `HEAD`. Disposition: fixed by comparing to the fixed source-identity base commit.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- CSV files in reviewed flows do not provide reliable embedded ticker/timeframe metadata; identity is accepted through strict filename and path-resolution contracts.
- Legacy direct CSV workflows without Strategy source context remain supported and were not converted into report-root-only workflows.
- Remaining warnings are third-party deprecations from installed `polygon` and `websockets`.
- This acceptance does not validate swing-strategy profitability, trading suitability, risk/reward correctness, ATR correctness, or event-recency correctness.

## Deferred Issues

- circular risk/reward target construction;
- high-low volatility instead of true range;
- stale Wyckoff event reuse;
- missing evidence treated as neutral evidence;
- live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks.

## Final Acceptance Statement

Source identity is accepted. Swing-strategy consistency as a whole is not yet accepted. Predictive applicability is not yet accepted.
