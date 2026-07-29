# MarketFlow Source Identity Status

## Decision

PASS.

## Metadata

- UTC status date: `2026-07-29T18:05:08Z`
- Branch: `feature/swing-source-identity`
- Base commit: `f3c2ca8f841030c46657332371b155ad6bd81e68`
- Commit: not created
- Tag: not created
- Push: not performed

## Exact Reproduced Defect

Before the correction, a temporary deterministic reproduction created only:

```text
BBB_4h_wyckoff_annotated.csv
```

Then it requested:

```text
ticker = AAA
timeframe = 4h
```

`marketflow.marketflow_strategy._select_strategy_source_csv(...)` returned `BBB_4h_wyckoff_annotated.csv` because it fell back from exact ticker/timeframe matching to canonical CSV matching by timeframe only. That would allow a `BBB` dataset to be analyzed and reported under an `AAA` request.

## Affected Call Paths

- `marketflow.marketflow_strategy.rank_long_candidates`:
  - locates report folders for requested tickers;
  - resolves the Strategy Ranking CSV source;
  - reads the selected CSV;
  - computes ranking fields;
  - emits candidate ticker, timeframe, CSV, and score fields.
- `marketflow.marketflow_strategy._select_strategy_source_csv`:
  - legacy compatibility wrapper now delegates to strict identity resolution.
- `marketflow.marketflow_strategy.resolve_strategy_source_identity`:
  - new strict source-identity resolver for Strategy Ranking.
- `marketflow.services.strategy_service.rank_latest_candidates`:
  - UI/service wrapper that validates public ticker/timeframe requests and delegates ranking.
- `marketflow.services.strategy_service.inspect_strategy_inputs`:
  - diagnostics now report strict source status/reason instead of timeframe-only matches.
- `apps.marketflow_studio._candidate_csv_path`:
  - resolves Strategy candidate CSV references inside the configured report root when source context is present.
- `marketflow.services.backtest_candidate_service._candidate_source_path`:
  - resolves Strategy candidate source CSV references inside the configured report root when source context is present.
- `marketflow.services.backtest_result_service.evaluate_candidate_snapshot_row`:
  - reopens Strategy candidate snapshot sources through relative report-root source context when present.
- `marketflow.services.walk_forward_validation_service.build_walk_forward_cases_from_csv`:
  - validates caller-provided ticker/timeframe labels against explicit CSV filename identity.

## Correction

Added a narrow immutable source-identity model in `marketflow.marketflow_strategy`:

- `StrategyDatasetIdentity`
- `StrategySourceResolution`

The Strategy Ranking resolver now accepts only one exact source identity. It never falls back to timeframe-only, ticker-only, first CSV, latest CSV, or substring matching.

## Canonical Rules

Ticker:

- empty ticker fails;
- surrounding whitespace fails;
- path separators fail;
- control characters fail;
- unsupported characters fail;
- `A-Z`, `0-9`, `.`, `_`, `-`, and `:` are supported;
- ticker identity is uppercase canonicalized;
- similar tickers remain distinct.

Timeframe:

- empty timeframe fails;
- surrounding whitespace fails;
- accepted tokens are `1mo`, `1w`, `1d`, `4h`, `2h`, `1h`, `30m`, `15m`, `5m`, and `1m`;
- timeframe identity is lowercase canonicalized;
- substring matching is prohibited.

## Missing And Ambiguous Behavior

- Zero exact matches returns `DATASET_NOT_FOUND` and skips before reading CSV data.
- More than one exact source identity returns `DATASET_IDENTITY_AMBIGUOUS` and skips before reading CSV data.
- Invalid request values return `INVALID_DATASET_REQUEST`.
- Invalid source roots return `INVALID_DATASET_SOURCE_ROOT`.

## Candidate-Label Integrity

Successful Strategy Ranking candidates now report ticker/timeframe from the validated source identity. Skipped source-resolution failures do not appear as ranked successes and cannot receive `score`, `close`, `sl`, `tp`, `rr`, `pop`, phase, event, or trend fields. Normal Strategy candidate output uses relative source references and source filenames rather than absolute private paths.

## Batch Behavior

Focused tests cover a batch containing:

- one exact valid candidate;
- one missing candidate;
- one wrong-ticker same-timeframe source;
- one ambiguous duplicate identity.

Only the exact valid candidate is ranked. Missing, wrong-ticker, and ambiguous candidates are skipped independently and do not alter the valid candidate's score.

## Historical And Walk-Forward Finding

Historical walk-forward validation does not discover CSVs by requested ticker/timeframe. It receives an explicit CSV path. The reviewed risk was caller relabeling: passing a ticker/timeframe that differs from the CSV filename, or passing labels for a CSV with incomplete filename identity, could label historical cases as another identity. `build_walk_forward_cases_from_csv` now validates caller labels against inferred CSV filename identity and fails before building cases with `DATASET_IDENTITY_MISMATCH` or `DATASET_IDENTITY_UNKNOWN`.

No change was made to row slicing, future outcome windows, leakage controls, candidate-generation math, or outcome definitions.

## Tests

Focused source-identity set:

```text
100 passed, 3 warnings
```

Coverage includes exact match, zero match, wrong ticker with matching timeframe, matching ticker with wrong timeframe, similar ticker names, exact timeframe tokens, canonical/raw ambiguity, generated walk-forward artifact exclusion, deterministic skip, no scoring after source failure, truthful labels, batch independence, source-root enforcement, escaping date-glob rejection, valid batch-folder filtering, symlink escape where supported, punctuation, service-level whitespace validation, diagnostics accuracy, Studio source-context fail-closed assurance, backtest source-context path confinement, backtest outcome source-context reopening, walk-forward label mismatch, walk-forward unknown identity failure, durable semantic-baseline assurance, no tracked-file modification assurance, and no-network assurance.

Full default suite:

```text
403 passed, 3 warnings
```

Warnings remain the accepted third-party `polygon` / `websockets` deprecations.

Collection:

```text
403 tests collected
```

## No-Network Evidence

The default pytest socket guard remained active. No manual provider checks were run, no network/provider call was allowed to complete, and no dependency was installed, upgraded, downgraded, or removed.

## Verification Results

Latest required checks:

```text
pip check: No broken requirements found.
focused source-identity suite: 100 passed, 3 warnings
pytest --collect-only -q: 403 tests collected
pytest -q: 403 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
```

The test count increased from 395 to 403 because reviewer-driven regressions were added for generated artifact exclusion, escaping date-glob rejection, valid batch-folder filtering, preserving and reopening validated Strategy candidate `source_report_dir` context, and walk-forward unknown identity failure.

Pre/post full-suite Git status matched. The full suite did not modify tracked files.

## Strategy-Semantic Non-Regression

Source-assurance tests compare the following Strategy Ranking formula functions against `HEAD`:

- `_atr`
- `_rr`
- `_phase_score`
- `_event_score`
- `_pnf_score_neutral`
- `_derive_sl_tp_long`
- `_extract_context`

Source-assurance tests also compare walk-forward semantic functions against `HEAD`:

- `_minimum_lookback_rows_from_profile`
- `_profile_horizon`
- `_row_matches_event_filters`
- `build_walk_forward_candidate_from_row`
- `evaluate_walk_forward_cases`
- `summarize_walk_forward_validation`

No candidate scoring formula, scoring weight, trend formula, Wyckoff phase/event detection, ATR/volatility calculation, stop/target/RR formula, Monte Carlo, Point-and-Figure, Eigen/PCA, outcome window, outcome definition, broker integration, or execution capability was changed.

## Independent Reviews

Reviewer A findings and dispositions:

- High: canonical/raw duplicate identity could still select one file. Disposition: fixed; any multiple exact identity matches now return `DATASET_IDENTITY_AMBIGUOUS`.
- High: Strategy candidate CSV reopen paths were not scoped to report root. Disposition: fixed for Strategy source context in Studio and backtest snapshot resolution.
- High: walk-forward caller labels could override source identity. Disposition: fixed with explicit CSV filename identity validation.
- Medium: ranking directory lookup used raw requested ticker before canonical validation. Disposition: fixed by validating/canonicalizing before folder globbing.
- Medium: diagnostics still reported timeframe-only matches. Disposition: fixed by removing timeframe-only match diagnostics and reporting strict source status/reason.

Reviewer B findings and dispositions:

- High: service-level ticker/timeframe normalization could bypass whitespace fail-closed rules. Disposition: fixed with public request whitespace validation before ranking.
- High: canonical/raw duplicate identity could still select one file. Disposition: fixed.
- High: required status documentation was missing. Disposition: fixed by this document.
- Medium: diagnostics used timeframe-only matching and stale fallback wording. Disposition: fixed.
- Final-review High: Studio Strategy candidate reopen path still needed explicit root confinement for `source_report_dir`. Disposition: fixed with resolved path confinement under the configured report root.
- Final-review Medium: walk-forward caller labels could still be used when filename identity was incomplete. Disposition: fixed with `DATASET_IDENTITY_UNKNOWN` fail-closed behavior.
- Final-review Medium: plan text still described canonical preference over raw for the same identity. Disposition: fixed; plan now states duplicate exact identities are ambiguous.
- Acceptance-review High: escaping `date_glob` and batch-like summary folders could become Strategy source roots. Disposition: fixed with safe date-glob validation, report-root-constrained directories, and valid `batch_YYYYMMDD_HHMMSS` filtering.
- Acceptance-review High: backtest outcome evaluation could reopen a Strategy snapshot source without relative source context. Disposition: fixed by resolving relative `source_report_dir` inside the configured report root before outcome evaluation.
- Acceptance-review High: generated walk-forward CSV artifacts could be parsed as Strategy source identities. Disposition: fixed by excluding walk-forward cases, results, and summary CSV artifacts from Strategy source resolution.
- Acceptance-review High: Studio Monte Carlo prefill could fall back to an unvalidated raw CSV when source-context resolution failed. Disposition: fixed; source-context candidates now fail closed.
- Acceptance-review Medium: Studio diagnostics still read the removed `matching_timeframe_csvs` key. Disposition: fixed with strict source status/reason/name fields.
- Acceptance-review Medium: semantic-baseline tests compared to moving `HEAD`. Disposition: fixed by comparing to the fixed source-identity base commit.

No critical or high reviewer finding remains unresolved.

## Remaining Limitations

- CSV files do not contain reliable embedded ticker/timeframe metadata in the reviewed paths; identity is therefore validated from strict source filename resolution and documented as such.
- Legacy direct absolute CSV workflows without Strategy source context remain supported and were not converted into report-root-only workflows.
- Remaining warnings are third-party deprecations from installed `polygon` and `websockets`.
- This task does not validate swing-strategy profitability, predictive applicability, or trading suitability.

## Deferred Issues

- circular risk/reward target construction;
- high-low volatility instead of true range;
- stale Wyckoff event reuse;
- missing evidence treated as neutral evidence;
- live ranking versus historical walk-forward alignment;
- predictive applicability for days/weeks.

## Final Status

The source-identity correction is accepted locally as PASS. No commit, tag, push, provider call, broker integration, execution capability, or unrelated strategy-semantic change was added or exercised.
