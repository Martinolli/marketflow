# MarketFlow Operational Workflows

Status: PASS

## Entry Points

`scripts/marketflow_batch_analysis.py`

- CLI: positional `tickers`, one or more.
- Defaults: no timeframe or period argument.
- Imports: `run_analysis`, `embed_fn`, `TransientVectorMemory`,
  `create_app_config`, `get_logger`, `sanitize_filename`,
  `write_batch_summary_csv`.
- Reads: configured data/provider paths through `run_analysis`; generated LLM
  JSON for batch summary if present.
- Writes: dated per-ticker reports via `run_analysis`; batch TVM under
  `REPORT_DIR/batch_<run_id>`; summary CSV under `REPORT_DIR/batch_csv_<run_id>`.
- Artifact identity: batch folder and TVM namespace are timestamped but not a
  strict parent identity for ticker reports.
- Provider behavior: `run_analysis` can invoke the normal analysis facade and
  LLM narrative path; not considered offline unless dependencies are mocked or
  local data providers are configured.

`marketflow/marketflow_strategy.py`

- CLI: `--report-root`, mutually exclusive `--date-glob` or `--batch latest`,
  `--tf`, `--tfs`, `--tickers`, `--use-mc`, `--use-pnf`, `--min-rr`,
  `--max-sl-atr`, `--prefer-phases`.
- Defaults: `--date-glob *`, `--tf 1h`, `--min-rr 1.5`,
  `--max-sl-atr 2.0`, preferred phases `C,D,E`, MC/PnF disabled.
- Reads: exact ticker/timeframe CSV source from the selected report folder;
  optional unique timeframe MC summary.
- Writes: timestamped Strategy JSON files under
  `.marketflow/reports/strategy_data`.
- Hardened selection: no recursive ticker-folder fallback; multiple ticker
  folders are ambiguous; MC evidence is used only on one exact-timeframe match.
- Candidate geometry: entry, stop, target, RR, source identity, and evidence
  diagnostics are produced by the canonical candidate builder.

`marketflow/marketflow_monte_carlo_trade.py`

- CLI: positional `csv`; single-run `--tp`, `--sl`, optional `--entry`, `--tf`,
  `--horizon`, `--model`, `--paths`, `--block`, `--seed`, `--nrows`,
  `--no-plots`, `--ml-model`, `--mu-shift`; backtest flags
  `--simulate-backtest`, `--bt-tp-pips`, `--bt-sl-pips`, `--bt-horizon`,
  `--bt-step`, `--bt-windows`, `--bt-paths`, `--bt-model`, `--bt-no-json`.
- Defaults: `entry` falls back to the latest close if omitted; `tf` is inferred
  from filename or defaults to `4h`; horizon `20`; model `garch`; paths
  `20000`; block `8`; seed `42`; nrows `4000`.
- Reads: OHLCV CSV; optional ML model file.
- Writes: timestamped MC summary JSON and optional HTML plots beside the CSV;
  ML model can be written for `ml_gbm`.
- Intended role: `CONDITIONAL PATH DIAGNOSTIC`. It must not create or replace
  Strategy target, stop, score, rank eligibility, or candidate validity.

`scripts/plot_annotated_features.py`

- CLI: positional `csv`; `--features`, `--nrows`, `--box-size`, `--reversal`,
  `--pnf-scale`, `--pnf-scale-value`, `--mc-summary`.
- Defaults: nrows `4000`, reversal `3`, auto PnF scale, no MC overlay unless
  `--mc-summary` is explicit.
- Reads: annotated CSV; optional explicit MC summary whose `csv` identity must
  match the plotted CSV.
- Writes: timestamped HTML plots and PnF sidecar JSON in the CSV directory.
- Hardened selection: no newest MC directory scan; mismatched MC summary fails
  before overlay.

## Artifact Lineage

Current report root inventory, schema/key inspection only:

- Total files: 925.
- Extensions: 426 CSV, 186 HTML, 154 Markdown, 131 JSON, 24 TXT, plus small
  TVM/faiss metadata.
- Report types include raw/annotated CSV, MC summary/HTML, PnF sidecar/HTML,
  backtest candidates/results, walk-forward cases/results/summary/registry,
  LLM analysis JSON, report HTML/JSON, summary TXT, and status Markdown.
- MC summaries have keys such as `csv`, `tf`, `params`, `metrics_from_now`,
  `actual_outcome`, `calibration`, and sometimes `join_metadata`,
  `source_csv`, `source_csv_path`, `source_report_dir`, `ticker`, `timeframe`.
- Existing reports do not consistently carry immutable `artifact_id`,
  `parent_artifact_id`, `workflow_type`, source digest, StrategyConfig digest,
  candidate core digest, or code commit.

## Proposed Identity Contract

Use the `marketflow.operational_artifacts` contract:

- `schema_version`
- `artifact_id`
- `run_id`
- `stage`
- `workflow_type`
- `ticker`
- `analysis_profile`
- `timeframe`
- `source_dataset_identity`
- `source_dataset_digest`
- `code_commit`
- `strategy_config_digest`
- `candidate_core_digest`
- `parent_artifact_id`
- `generated_at`
- safe relative `artifact_ref`

Do not include account identifiers, credentials, absolute home paths, live trade
values, or performance values in identity metadata.

## Future Fixed Profiles

Normal user input should be ticker only.

- `SWING`: timeframe `4h`, minimum valid rows `390`.
- `POSITION_SWING`: timeframe `1d`, minimum valid rows `560`.

The future normal interface must not expose timeframe, period/history window,
primary timeframe, StrategyConfig values, or evidence component toggles. Current
Studio Strategy Ranking remains an advanced/legacy operator surface because it
still exposes timeframe, StrategyConfig values, and evidence toggles. Results
remain separate. Higher-timeframe context is not currently consumed.

## Component Authority

- VPA/Wyckoff core: `AUTHORITATIVE ANALYTICAL ENGINE`.
- Canonical Strategy builder: `AUTHORITATIVE CANDIDATE ENGINE`.
- Monte Carlo, Eigen, PnF: `SUPPORTING DIAGNOSTICS`.
- CLI, reports, plotting: `INTERFACE AND PRESENTATION`.
- Streamlit: `OPTIONAL VIEWER, NOT REQUIRED BY ENGINE`.
- LLM: `NON-AUTHORITATIVE NARRATIVE ONLY OR LEGACY/EXPERIMENTAL`.

Source assurance confirms core Strategy, Monte Carlo, and operational contract
modules do not import Streamlit, OpenAI, or the MarketFlow LLM interface. LLM
output is not an input to candidate score, event, target, stop, RR, or rank
eligibility.
