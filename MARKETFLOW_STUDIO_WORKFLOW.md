# MarketFlow Studio Workflow

MarketFlow Studio is a local cockpit for reviewing MarketFlow reports, ranking setups, validating selected candidates, and building Analyst Packets. It does not replace trade judgment or issue automatic recommendations.

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
10. Use packet for Wyckoff Volume Analyst review.

## Recommended Batch Flow

1. Open Batch Analysis.
2. Enter ticker basket.
3. Run batch.
4. Use batch tickers in Strategy Ranking.
5. Rank by timeframe.
6. Validate finalists with Monte Carlo.
7. Build Analyst Packets for finalists.

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
- profile/risk rules

It does not call an LLM yet.

## Recommended Conservative Default

For daily use:

1. Run analysis.
2. Check chart.
3. Rank strategy without Monte Carlo.
4. Run Monte Carlo only on candidate.
5. Build Analyst Packet.
6. Do not act on candidates with weak score, failed POP gate, or failed P&F gate.
