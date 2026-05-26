# MarketFlow Studio Workflow

MarketFlow Studio is a local cockpit for reviewing MarketFlow reports, ranking setups, validating selected candidates, and building Analyst Packets. It does not replace trade judgment or issue automatic recommendations.

Studio uses the sidebar Workspace selector to render one page at a time. This keeps heavy pages such as Charts, Generated Artifacts, Monte Carlo plots, and Analyst Packet views from rendering when they are hidden.

## Design Review Checkpoint

For the current Studio milestone review, see:

- `MARKETFLOW_STUDIO_DESIGN_REVIEW_CHECKPOINT_2026-05-23.md`

## Recommended Single Ticker Flow

1. Enter ticker and timeframes in the sidebar.
2. Run Analysis or Load Latest Report.
3. Review Overview.
4. Review Charts by timeframe.
5. Run Strategy Ranking without Monte Carlo first.
6. Select a candidate.
7. Send candidate to Monte Carlo.
8. Run Monte Carlo, usually bootstrap first.
9. Build Analyst Packet.
10. Build a Wyckoff Analyst prompt preview.
11. Use packet and prompt for Wyckoff Volume Analyst review.

## Recommended Batch Flow

1. Open Batch Analysis.
2. Enter ticker basket.
3. Run batch.
4. Use batch tickers in Strategy Ranking.
5. Rank by timeframe.
6. Validate finalists with Monte Carlo.
7. Build Analyst Packets for finalists.

## Charts Tab

- Charts tab shows annotated candlestick charts by timeframe.
- If P&F sidecars exist, it can also render a basic P&F sidecar chart.
- If only metadata is available, the P&F chart shows last price, breakout, and objective levels.
- The reconstructed P&F chart is built from sidecar JSON and may not include every visual feature from the saved HTML plot. Use Generated Artifacts to preview the original saved P&F HTML.

P&F sidecars are not generated automatically by Run Analysis. Use Charts tab > Generate P&F Sidecars to create:

- `*_point_and_figure_plot.html`
- `*_pnf_meta.json`

After generation:

- the P&F chart appears in the Charts tab
- the Analyst Packet can use the P&F sidecar
- the P&F gate can move from pending to pass/fail/unknown
- Studio-generated P&F sidecars include source CSV, inferred timeframe, box settings, row limit, and generation metadata.

Bulk P&F generation processes only `*_wyckoff_annotated.csv` files. The selected CSV generator can still be used for a single selected CSV.

P&F sidecars now display source hygiene indicators. Sidecars generated from `*_wyckoff_annotated.csv` are preferred for candidate traceability. Raw CSV sidecars may still be useful for visual review but are flagged as raw source.

Use Charts tab > Generate Legacy Feature Plots to run the legacy plotting workflow from an annotated CSV without opening browser windows. The generated files are saved beside the CSV and can include P&F HTML/meta JSON, Wyckoff annotated charts, price-volume, volume profile, volume distribution, and spread/features HTML.

## Generated Artifacts

Reports tab includes a Generated Artifacts browser for saved HTML, JSON, TXT, and CSV outputs in the loaded report folder.
Artifact previews are lazy for performance: select an artifact, then click Preview selected artifact to render it. Large Plotly HTML artifacts may take time to render, and very large files may need to be downloaded or opened externally.

It can list, filter, preview, and download:

- report HTML, report JSON, and summary text
- P&F HTML and P&F sidecar JSON
- Monte Carlo hits/paths HTML and summary JSON
- legacy feature plot HTML outputs
- annotated and raw CSV files

## Price-Volume Eigen Analyzer

The Price-Volume Eigen Analyzer is a standalone feature generator.
It measures price-volume harmony and abnormal effort-result behavior using rolling eigen/PCA-style analysis.

It does not create buy/sell signals.
It does not change Strategy Ranking or Analyst Packet decisions yet.
Generated files are saved as `*_pv_eigen.csv` artifacts.
Studio can preview an Eigen chart showing price context, residual, coupling, and divergence markers. The chart is exploratory and does not create trading signals.
Studio can compare Eigen windows such as 20/40/60 to help distinguish local, structural, and broader effort-result abnormalities. This comparison is diagnostic only and does not create trading signals.
Studio can review whether Eigen residual/divergence attention rows occur near Wyckoff-labelled events or appear independently. This is a diagnostic review only and does not create trading signals.
Eigen Window Comparison and Eigen-Wyckoff Proximity Review can be saved as a markdown Eigen Review Summary artifact. This creates an audit snapshot of diagnostic Eigen evidence only; it does not create trading signals.

## Strategy Ranking Monte Carlo Checkbox

Monte Carlo is optional in Strategy Ranking.

If unchecked, ranking uses CSV/Wyckoff/ATR logic.

If checked, the strategy tries to use available Monte Carlo summary files.

If no matching Monte Carlo data is available, ranking should still work with neutral or missing POP.

For now, the safer workflow is:

1. Rank first without Monte Carlo.
2. Select the strongest candidates.
3. Run Monte Carlo for selected candidates.
4. Build Analyst Packet for final validation.

Strategy Ranking now prefers MC summaries matching the selected timeframe. If no matching summary is found, it may fall back to the latest available summary and mark the match mode in the results.

## Monte Carlo Tab

- Select CSV or use a selected Strategy Ranking candidate.
- Entry, stop loss, and take profit are editable.
- Bootstrap is the recommended default.
- Save plots writes HTML/JSON files beside the CSV.
- Generated files are listed in the UI.
- HTML plots can be previewed inside Studio after a run.
- They can also be downloaded and opened in a browser.
- Monte Carlo hits, paths, and summary files also appear in the Generated Artifacts browser.

When a Strategy Ranking candidate is sent to Monte Carlo, Studio now treats that candidate trade plan as the authoritative prefill. Analyst Packet validates that the Monte Carlo result matches the selected candidate before including it. Mismatched Monte Carlo runs can be included only as explicit manual scenarios.

## Monte Carlo Backtest Refactor Plan

A planning checkpoint exists at `MARKETFLOW_MONTE_CARLO_BACKTEST_REFACTOR_PLAN.md`. The planned refactor will compare Monte Carlo forecast probabilities with actual historical TP/SL/neither outcomes. This is research/calibration only and does not create trade signals.

Phase 1 outcome engine is implemented as a standalone tested utility. It is not wired into Studio yet.

## GARCH

GARCH requires optional package `arch`.

If `arch` is not installed, GARCH will fail with an optional dependency error.

Use bootstrap unless GARCH support is intentionally installed.

## Analyst Packet

Analyst Packet combines:

- report context
- strategy candidate
- Monte Carlo metrics
- P&F sidecars if available
- Eigen diagnostic context if available
- profile/risk rules

Analyst Packet can extract Wyckoff context from report JSON and the selected annotated CSV.

Analyst Packet uses discovered P&F sidecars and prefers the sidecar matching the selected strategy candidate CSV/timeframe. If multiple P&F sidecars exist, verify the selected sidecar and match reason before relying on the P&F gate.

P&F objectives are interpreted relative to the selected strategy candidate. For long candidates, downside objectives are treated as risk/contradiction rather than support. Extreme objectives are flagged for review.
Very distant P&F objectives are labelled as supportive_extended when they support the setup but require realism/timeframe review.

The Analyst Packet page includes a Candidate Decision Card summarizing Strategy, Monte Carlo, P&F, and packet readiness. It is a visual workflow check, not a new scoring model.

The Candidate Decision Card can be saved as a markdown Decision Summary artifact. This creates a lightweight snapshot of the selected setup, Monte Carlo alignment, P&F context, and packet readiness.

The packet can be downloaded or saved to the loaded report folder.

It does not call an LLM yet.

## Analyst Packet Eigen Context

Analyst Packet can include read-only Eigen diagnostic context when matching `*_pv_eigen.csv` artifacts are available. Eigen context summarizes residual, coupling, divergence counts, and recent divergence state. It is diagnostic only and does not change Strategy Ranking, Monte Carlo, P&F gates, risk rank, or analyst readiness.

## Wyckoff Analyst Prompt Preview

The Wyckoff Analyst tab converts the Analyst Packet into a markdown prompt.
It does not call any AI model.
Use it to inspect, edit, download, or save the prompt before future Analyst Chat integration.
Saved prompt files are markdown artifacts. Studio includes the prompt style and a timestamp in saved filenames so balanced, strict, and educational prompts do not overwrite each other.
Saved prompt markdown files appear in Reports > Generated Artifacts and can be previewed or downloaded from there.

Recommended flow:

Analysis -> Strategy Ranking -> Monte Carlo -> P&F -> Analyst Packet -> Wyckoff Analyst Prompt

## Analyst Chat Skeleton

The Analyst Chat section is experimental.
It does not run automatically.
The user must review the prompt and click Run Analyst.
If no API/provider is configured, Studio shows setup guidance or dry-run output.
Responses can be saved as markdown artifacts and reviewed in Generated Artifacts.
Analyst Chat dry-run responses are saved as `analyst_response_md` artifacts. They are placeholders only and do not represent model output.

## Analyst Review Notes

Studio can save manual Analyst Review Notes as a markdown artifact. This records the reviewer posture, conviction, notes, follow-up actions, and evidence snapshot. It is a human review artifact only and does not create trading signals or change Strategy Ranking, Monte Carlo, P&F, Eigen, or Analyst Packet results.

## Recommended Conservative Default

For daily use:

1. Run analysis.
2. Check chart.
3. Rank strategy without Monte Carlo.
4. Run Monte Carlo only on candidate.
5. Build Analyst Packet.
6. Build and inspect the Wyckoff Analyst prompt.
7. Do not act on candidates with weak score, failed POP gate, or failed P&F gate.
