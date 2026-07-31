# MarketFlow Operational Pipeline Audit Status

Status: PASS

Date: 2026-07-31

Branch: `feature/swing-operational-pipeline-audit`

Base commit: `da6cb3564ed77135852741b216075f421a0d128e`

## Baseline

- Initial branch: confirmed.
- Initial commit: confirmed.
- Initial tree: clean.
- Python: `env\Scripts\python.exe`.
- `pip check`: passed.
- No commit or tag was created.
- No network, provider, broker, execution, dependency, or performance-analysis
  step was run.

## Workflow A

Path:

`scripts/marketflow_batch_analysis.py -> marketflow/marketflow_monte_carlo_trade.py -> scripts/plot_annotated_features.py -> .marketflow/reports`

Classification: `MANUAL_SCENARIO_ANALYSIS`.

Monte Carlo may use manually supplied entry, stop, target, horizon, ticker,
timeframe, source dataset, and annotation artifact. If entry is omitted in the
raw CLI it falls back to latest close, so manual scenario usage must pass
`--entry` explicitly. Workflow A output is labelled with
`scenario_origin = MANUAL_SCENARIO` and must not claim canonical Strategy
generation.

## Workflow B

Path:

`scripts/marketflow_batch_analysis.py -> marketflow/marketflow_strategy.py -> marketflow/marketflow_monte_carlo_trade.py -> scripts/plot_annotated_features.py -> .marketflow/reports`

Classification: `CANONICAL_STRATEGY_DECISION_SUPPORT`.

Strategy uses `build_candidate_from_prefix`, the canonical candidate builder.
The added operational contract builds Workflow B Monte Carlo requests from
candidate `entry`, `stop_loss`, `take_profit`, ticker, timeframe, and source CSV
fields, and provides a tested equality guard for use before MC execution.
Monte Carlo remains a conditional diagnostic and does not recompute or replace
Strategy geometry. Complete production writer integration is deferred.

## Acceptance Boundary

OPERATIONAL WORKFLOW AUDIT / READ-SIDE LINEAGE CONTROLS: ACCEPTED.

COMPLETE END-TO-END IMMUTABLE ARTIFACT WRITING: NOT YET ACCEPTED.

The raw Monte Carlo CLI still requires first-class immutable artifact identity
writing in a later phase. Historical/raw summaries without immutable IDs can
only be used through the stricter read-side matching rules documented below.

Research protocol freeze remains blocked. Predictive usefulness and
profitability remain unaccepted.

## Handoffs

- Strategy source CSV selection requires exact ticker/timeframe identity.
- Strategy no longer recursively falls back to arbitrary ticker folders.
- Multiple matching ticker directories fail closed as ambiguous.
- Strategy MC evidence accepts exactly one same-ticker, same-timeframe,
  canonical-workflow summary with matching source CSV metadata.
- No requested MC summary or multiple requested-timeframe MC summaries produce
  missing/incomplete MC evidence instead of newest-file selection.
- Missing ticker/source/workflow metadata, wrong ticker, wrong workflow, and
  contradictory source CSV metadata are rejected.
- Plotting requires explicit `--mc-summary` and validates the summary `csv`
  identity and report directory against the plotted CSV.
- Output collision prevention is provided by
  `run_specific_output_path(...)` for the next implementation phase.

## Report Root

Safe inspection of `.marketflow/reports` recorded only counts, names, schema
keys, and metadata fields:

- Total files: 925.
- CSV: 426; HTML: 186; Markdown: 154; JSON: 131; TXT: 24.
- MC summaries: 34.
- PnF sidecars: 19.
- Annotated CSVs: 82.
- LLM analysis JSONs: 24.
- Walk-forward cases/results/summaries: 56 each.

Findings:

- Ticker/timeframe appears in many filenames, but immutable run identity is not
  consistently encoded.
- Second-resolution timestamp names can collide.
- Existing metadata is partial; immutable artifact identity and parent linkage
  are not consistently present.
- Existing reports should not be deleted or auto-selected among.
- Raw and historical MC summaries do not yet consistently provide first-class
  immutable `artifact_id` / `parent_artifact_id` metadata.

## Future Fixed Profile Design

Future normal interface:

- user input: ticker only;
- `SWING`: `4h`, minimum valid rows `390`;
- `POSITION_SWING`: `1d`, minimum valid rows `560`.

The future normal interface must hide timeframe, period/history window,
StrategyConfig values, primary timeframe, and evidence toggles. Current Studio
Strategy Ranking remains an advanced/legacy operator surface because it still
exposes timeframe, StrategyConfig values, and evidence toggles. Workflow A
remains an advanced manual mode.

## Streamlit And LLM

Streamlit participates as an optional viewer through Studio and is not imported
by Strategy, Monte Carlo, or operational artifact contracts. LLM paths are
legacy/narrative and do not feed canonical candidate score, event, target, stop,
RR, or rank eligibility.

## Reviews

Reviewer A found:

- batch lineage was not batch-bound;
- raw MC CLI had weak provenance;
- Strategy source selection was mostly strict but MC selection used newest
  fallback;
- MC summaries with missing identity metadata could attach stale POP evidence;
- plot MC overlay could be stale or cross-run with same basename;
- second-resolution output names could collide.

Reviewer B found:

- `None` required identity fields could be stringified instead of rejected;
- docs/UI needed updates after hardening;
- fixed-profile wording needed to be classified as future/legacy because
  current Studio still exposes advanced controls;
- explicit MC plot linkage needed tests;
- canonical/manual distinctions and dry-run LLM controls were preserved.

## Tests

Focused tests added:

- exact artifact parent selection;
- fixed stage/workflow validation;
- safe relative artifact references;
- parent cycle rejection;
- no newest/first MC fallback;
- wrong ticker/timeframe/run rejection;
- missing identity metadata rejection;
- ambiguous artifact rejection;
- Workflow A manual scenario labelling;
- Workflow B canonical candidate labelling;
- rank-ineligible candidate rejection before Workflow B MC handoff;
- MC geometry equality and mutation detection;
- candidate-core digest mismatch rejection;
- plot explicit artifact identity;
- plot directory rejection for `--mc-summary`;
- report collision prevention;
- candidate and StrategyConfig digest determinism;
- source assurance for Streamlit/LLM isolation.

Focused count: 17 operational tests.

Related integrity count run locally: 129 passed.

Full default suite result: 556 passed.

Warnings observed in focused runs: the three accepted third-party
polygon/websockets deprecation warnings.

Required checks:

- `env\Scripts\python.exe -m pip check`: passed.
- `env\Scripts\python.exe -m pytest --collect-only -q`: 556 tests collected.
- `env\Scripts\python.exe -m pytest -q`: 556 passed, 3 accepted
  third-party warnings.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`:
  passed.
- `git diff --check`: passed.
- Pre-test Git status: expected task modifications only.
- Post-test Git status: expected task modifications only.

## Blockers

None remaining for this audit phase after hardening and focused validation.

Remaining limitations:

- raw MC CLI summaries still need first-class immutable identity writing in the
  next implementation phase;
- second-resolution naming remains in legacy writers until run-specific naming
  is threaded through all call sites;
- historical reports lack complete identity metadata;
- `--batch latest` remains an explicit legacy UI/CLI convenience, not a normal
  fixed-profile interface.
