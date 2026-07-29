# MarketFlow Source Identity Plan

## Observed Risk

The Strategy Ranking source resolver can select a Wyckoff annotated CSV by timeframe when no exact ticker/timeframe canonical CSV exists. A requested candidate such as `AAA` / `4h` can therefore be analyzed from `BBB_4h_wyckoff_annotated.csv` and reported under the requested ticker.

## Current Source-Selection Path

- `marketflow.marketflow_strategy.rank_long_candidates` locates report folders for requested tickers, calls `_select_strategy_source_csv`, loads the selected CSV with `pandas.read_csv`, computes strategy values, and labels each result with the request ticker and timeframe.
- `marketflow.marketflow_strategy._select_strategy_source_csv` lists CSV files in the selected report folder, prefers exact canonical Wyckoff annotated CSVs, currently falls back to timeframe-only canonical CSVs, and then falls back to exact non-generated raw CSVs.
- `marketflow.services.strategy_service.rank_latest_candidates` normalizes UI ticker/timeframe input and delegates ranking to `rank_long_candidates`.
- `marketflow.services.strategy_service.inspect_strategy_inputs` reports pre-ranking CSV availability using a separate timeframe-token matcher.
- Historical walk-forward helpers in `marketflow.services.walk_forward_validation_service` operate from explicit CSV paths and infer ticker/timeframe from that path when not supplied; they do not currently discover another ticker's CSV by requested ticker/timeframe.

## Requested Dataset Identity

Every selected strategy dataset must have a validated immutable identity:

- canonical ticker;
- canonical timeframe;
- resolved regular-file source path;
- source-selection status.

The selected source must match both canonical request values exactly. Resolver failure must be explicit and must not produce a scored candidate.

## Canonical Normalization Rules

Ticker:

- empty input fails;
- surrounding whitespace fails instead of being silently repaired;
- path separators fail;
- control characters fail;
- characters outside `A-Z`, `0-9`, `.`, `_`, `-`, and `:` fail;
- case is normalized to uppercase because existing batch and strategy services treat ticker symbols case-insensitively;
- different valid ticker tokens such as `A`, `AA`, `AAA`, `AI`, and `AT` remain distinct.

Timeframe:

- empty input fails;
- surrounding whitespace fails instead of being silently repaired;
- only source-defined tokens are accepted: `1mo`, `1w`, `1d`, `4h`, `2h`, `1h`, `30m`, `15m`, `5m`, `1m`;
- case is normalized to lowercase;
- substring matching is prohibited, so `1h` does not match `4h` and `1d` does not match `1w`.

## Exact-Match Behavior

Exactly one CSV identity matching the canonical request is selected. If both canonical Wyckoff annotated and raw CSV files exist for the same exact identity, the identity is ambiguous and no source is selected. Generated derivative CSVs remain excluded from source selection.

## Missing-Source Behavior

Zero exact matches returns a safe skipped state with reason `DATASET_NOT_FOUND`. The candidate is not loaded, scored, or given entry, stop, target, RR, or composite score values.

## Ambiguous-Source Behavior

More than one source for the same identity returns `DATASET_IDENTITY_AMBIGUOUS`. The candidate is skipped and no arbitrary latest-file or glob-order selection is allowed.

## Candidate-Label Integrity

Successful candidate result labels must come from the validated source identity, not the original request. Failed source resolution must not retain a requested ticker as a ranked success and must not expose absolute private source paths in normal skipped output.

## Source-Path Safety

The resolver must only select regular `.csv` files located inside the approved report folder. It rejects directories, missing files, non-CSV files, deceptive extensions, path traversal, and symlink or junction escapes where detectable.

## Tests

Focused deterministic tests will cover exact ticker/timeframe selection, zero match, wrong-ticker same-timeframe rejection, matching ticker wrong-timeframe rejection, similar ticker names, exact timeframe tokens, ambiguous duplicate identity, candidate skip without scoring values, truthful candidate labels, batch independence, regular-file/root enforcement, supported punctuation, no tracked-file modification, and no network.

## Exclusions

No changes are allowed to candidate scoring, weights, ranking mathematics, trend calculation, Wyckoff phase/event detection, event recency, ATR/volatility, stop/target/RR, Monte Carlo, Point-and-Figure, Eigen/PCA, walk-forward outcome definitions, outcome horizons, recommendation thresholds, eligibility, broker integration, or execution.

## Stop Conditions

Stop blocked if the starting branch or commit is wrong, the tree is dirty, a dependency changes, a network call completes, wrong-ticker fallback remains, ambiguous identity selects arbitrarily, missing source creates a scored candidate, labels can differ from validated source identity, absolute private paths leak, tests modify tracked files, full tests or compileall fail, strategy semantics outside source identity change, or a critical/high independent-review finding remains.
