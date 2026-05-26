# MarketFlow Personal UI Plan

## Purpose

This plan describes how to add a simple, friendly, local-only user interface to MarketFlow.

The goal is not to build a commercial product, multi-user platform, cloud service, or complex dashboard. The goal is to make the existing personal workflow easier:

1. Select one or more tickers.
2. Run MarketFlow analysis.
3. Review generated results.
4. View Wyckoff/VPA charts.
5. Run strategy ranking.
6. Optionally run Monte Carlo analysis.
7. Ask the local “Wyckoff Volume Analyst” about the latest results.

The interface should act as a cockpit for the existing project, not as a replacement for the current analytical engine.

---

## Current Workflow

The current manual flow is approximately:

```text
scripts/marketflow_batch_analysis.py
        ↓
marketflow/marketflow_strategy.py
        ↓
scripts/plot_annotated_features.py
        ↓
optional:
marketflow/marketflow_monte_carlo_trade.py
        ↓
manual handoff to Wyckoff Volume Analyst
````

The main analytical orchestration is currently handled by:

```text
marketflow/marketflow_facade.py
```

The project already has strong backend functionality. The main problem is usability: many steps are script-driven, path-driven, and manual.

---

## Target Workflow

The new workflow should be:

```text
Open MarketFlow Studio
        ↓
Enter ticker or tickers
        ↓
Choose timeframes
        ↓
Run analysis
        ↓
Review reports, charts, signals, Wyckoff events
        ↓
Run strategy ranking
        ↓
Optionally run Monte Carlo
        ↓
Ask the Wyckoff Volume Analyst questions
```

---

## Recommended Interface

Use **Streamlit** for the first personal-use interface.

Reasons:

* Fast to build.
* Works well locally.
* Good for forms, tables, charts, and tabs.
* No need for frontend/backend separation.
* No need for authentication.
* No need for deployment.
* Good enough for personal use.

The app should run with:

```bash
streamlit run apps/marketflow_studio.py
```

---

## Implementation Progress

* Milestone 1: Initial Streamlit UI — implemented
* Timeframe normalization fix — implemented
* Milestone 2: Report Browser and CSV Preview — implemented
* Milestone 3: Basic Chart Tab — implemented
* Milestone 4: Strategy Ranking tab — implemented
* Strategy Ranking diagnostics — implemented
* Strategy latest-batch diagnostics refinement — implemented
* Monte Carlo tab, simple single-run mode — implemented
* Streamlit logging control — implemented
* Candidate-to-Monte Carlo handoff — implemented
* Monte Carlo output file listing — implemented
* Batch Analysis tab — implemented
* Analyst Packet Builder — implemented
* Analyst Packet end-to-end validation — implemented
* Studio readability polish — implemented
* P&F sidecar integration into Analyst Packet — implemented
* MarketFlow Studio workflow documentation — implemented
* Strategy Ranking timeframe-aware Monte Carlo matching — implemented
* Monte Carlo HTML plot preview/download — implemented
* P&F sidecar chart rendering — implemented
* Analyst Packet Wyckoff extraction and save clarity — implemented
* Manual P&F sidecar generation in Studio — implemented
* Full report artifact browser and legacy plot generation — implemented
* P&F sidecar traceability and Analyst Packet matching — implemented
* P&F objective quality refinement — implemented
* P&F extended objective wording refinement — implemented
* Price-Volume Eigen Analyzer standalone feature generator — implemented
* Price-Volume Eigen chart preview — implemented
* Price-Volume Eigen window comparison — implemented
* Eigen-Wyckoff proximity review — implemented
* Eigen Review Summary artifact — implemented
* Strategy-to-Monte-Carlo trade-plan alignment — implemented
* Candidate Decision Card — implemented
* Candidate Decision Summary artifact — implemented
* Wyckoff Analyst prompt preview — implemented
* Wyckoff Analyst prompt artifact and UI robustness pass — implemented
* Studio performance pass with active-page navigation and lazy artifact previews — implemented
* Studio design review checkpoint — implemented
* Analyst Chat skeleton — implemented
* Analyst Chat dry-run response polish — implemented
* Analyst Review Notes artifact — implemented
* Next planned milestone: PR review / merge to main

---

## Non-Goals

Do not build these in the first version:

* Multi-user login.
* Cloud deployment.
* Complex database.
* Real-time streaming market data.
* Broker integration.
* Order execution.
* User account management.
* Advanced permissions.
* Public web hosting.
* Mobile app.
* Heavy frontend framework such as React.

Keep it local, practical, and simple.

---

## Proposed File Structure

Add the following:

```text
apps/
    marketflow_studio.py

marketflow/services/
    __init__.py
    analysis_service.py
    report_index.py
    strategy_service.py
    monte_carlo_service.py
    analyst_packet_service.py

marketflow/charts/
    __init__.py
    wyckoff_chart.py
    volume_profile_chart.py
    point_and_figure_chart.py
```

Optional later:

```text
markdown_files/
    marketflow_personal_ui_plan.md
```

---

## Design Principle

The UI should not contain heavy business logic.

The UI should call small service classes or functions.

Preferred pattern:

```text
Streamlit page
    ↓
Service layer
    ↓
Existing MarketFlow modules
    ↓
Reports / CSV / JSON / HTML outputs
```

Avoid this:

```text
Streamlit page
    ↓
Huge direct calls to many internal modules
    ↓
Duplicated logic
```

---

## Phase 1 — Minimal Personal UI

### Objective_1

Create the first usable local page.

### Add -1

```text
apps/marketflow_studio.py
marketflow/services/analysis_service.py
marketflow/services/report_index.py
```

### Features

The first version should allow:

* Enter one ticker.
* Select timeframes.
* Run analysis.
* Load latest report folder.
* Display:

  * ticker
  * current price
  * signal type
  * signal strength
  * stop loss
  * take profit
  * risk/reward ratio
  * generated output path

### UI Layout

Use Streamlit sidebar for inputs:

```text
Sidebar:
    Ticker
    Timeframes
    Run Analysis button
    Load Latest Results button
```

Main page:

```text
Main:
    Summary cards
    Report location
    JSON preview
```

### Acceptance Criteria_1

Phase 1 is complete when:

* The app opens locally.
* A ticker can be analyzed from the UI.
* Reports are generated using the existing backend.
* The latest report can be loaded without manually searching folders.
* No existing CLI/script workflow is broken.

---

## Phase 2 — Report Browser

### Objective_2

Make generated reports easier to inspect.

### Add to UI - 1

A report browser section with:

* latest report folder
* available tickers
* available timeframes
* generated files
* JSON report preview
* summary text preview
* annotated CSV preview

### Service Functions

In `report_index.py`, add helpers like:

```python
find_latest_report_root()
find_latest_ticker_report(ticker)
list_available_tickers()
list_available_timeframes(ticker)
load_report_json(ticker)
load_summary_text(ticker)
load_annotated_csv(ticker, timeframe)
```

### Acceptance Criteria_2

Phase 2 is complete when:

* The user can inspect previous analysis results without rerunning analysis.
* The UI can load the latest report for a ticker.
* Annotated CSV files can be previewed in a table.

---

## Phase 3 — Charts Inside the UI

### Objective_3

Show the most useful visual outputs directly in the app.

### Refactor Existing Plotting Code

Current plotting functionality exists in:

```text
scripts/plot_annotated_features.py
```

Refactor chart-building logic into reusable modules:

```text
marketflow/charts/wyckoff_chart.py
marketflow/charts/volume_profile_chart.py
marketflow/charts/point_and_figure_chart.py
```

Each chart module should expose functions that return Plotly figures.

Example:

```python
def build_wyckoff_candlestick_chart(df, title=None):
    return fig
```

The old script should still work, but it should call the new chart functions.

### UI Chart Tabs

Add tabs:

```text
Charts:
    Wyckoff Candlestick
    Volume Profile
    Point & Figure
    Feature Plot
```

### Acceptance Criteria_3

Phase 3 is complete when:

* The user can select a ticker and timeframe.
* The app displays the Wyckoff candlestick chart.
* The app displays the volume profile chart.
* The app displays the Point & Figure chart.
* Existing HTML chart export behavior is not broken.

---

## Phase 4 — Batch Analysis

### Objective_4

Support the normal personal workflow for multiple tickers.

### Add to UI - 2

Input:

```text
Tickers:
AAPL MSFT NVDA
```

Button:

```text
Run Batch Analysis
```

Output:

```text
Batch run ID
Ticker status table
Output folders
Batch summary CSV path
```

### Service

Create:

```text
marketflow/services/analysis_service.py
```

With functions:

```python
run_single_ticker(ticker, timeframes=None)
run_batch(tickers, timeframes=None)
```

This service can internally call existing code from:

```text
marketflow/marketflow_analysis.py
scripts/marketflow_batch_analysis.py
```

However, avoid duplicating batch logic directly inside the Streamlit app.

### Acceptance Criteria_4

Phase 4 is complete when:

* Multiple tickers can be analyzed from the UI.
* The batch output folder is created.
* The batch summary CSV is generated.
* Errors for individual tickers do not stop the entire batch.

---

## Phase 5 — Strategy Ranking

### Objective_5

Expose the existing strategy ranking in the UI.

### Existing Logic - 1

Use:

```text
marketflow/marketflow_strategy.py
```

Especially:

```python
rank_long_candidates()
```

### Add Service - 1

```text
marketflow/services/strategy_service.py
```

The service should hide report path complexity from the UI.

Example function:

```python
rank_latest_batch(
    tickers,
    timeframe,
    min_rr=1.5,
    prefer_phases=("C", "D", "E"),
    use_mc=False
)
```

### UI

Add a tab:

```text
Strategy Ranking
```

Inputs:

* batch folder: latest
* ticker list
* timeframe
* minimum risk/reward
* preferred Wyckoff phases
* use Monte Carlo: yes/no

Output table:

```text
ticker | tf | close | sl | tp | rr | phase | event | trend | score
```

### Acceptance Criteria_5

Phase 5 is complete when:

* The user can rank candidates from the latest batch.
* Results are displayed in a sortable table.
* The selected candidate can be used later by the Monte Carlo tab.

---

## Phase 6 — Monte Carlo Tab

### Objective_6

Allow optional Monte Carlo analysis from the UI.

### Existing Logic -2

Use:

```text
marketflow/marketflow_monte_carlo_trade.py
```

Main class:

```python
MonteCarloTradeSimulator
```

### Add Service -2

```text
marketflow/services/monte_carlo_service.py
```

Example function:

```python
run_monte_carlo_for_csv(
    csv_path,
    entry,
    stop_loss,
    take_profit,
    timeframe,
    model="bootstrap",
    paths=10000,
    horizon=20
)
```

### UI Inputs

* ticker
* timeframe
* CSV path selected automatically
* entry price
* stop loss
* take profit
* model
* paths
* horizon

### UI Outputs

* probability of TP-first
* probability of SL-first
* median bars to TP
* median bars to SL
* fan chart
* hit histogram
* generated JSON path

### Acceptance Criteria_6

Phase 6 is complete when:

* The user can run Monte Carlo from a selected annotated CSV.
* The result summary is displayed in the UI.
* Generated JSON/HTML outputs are saved beside the CSV.
* Monte Carlo remains optional.

---

## Phase 7 — Wyckoff Volume Analyst Packet

### Objective_7

Improve the quality of information passed to the Wyckoff Volume Analyst.

Instead of passing large raw reports or scattered files, create a compact structured packet.

### Add

```text
marketflow/services/analyst_packet_service.py
```

Or:

```text
marketflow/marketflow_analyst_packet.py
```

### Packet Example

```json
{
  "ticker": "AAPL",
  "current_price": 213.42,
  "overall_signal": {
    "type": "BUY",
    "strength": "MODERATE",
    "details": "..."
  },
  "risk": {
    "stop_loss": 205.10,
    "take_profit": 229.00,
    "risk_reward": 2.1
  },
  "timeframes": {
    "1d": {
      "trend": "up",
      "wyckoff_phase": "D",
      "confirmed_events": ["SOS", "LPS"],
      "support": [205.10],
      "resistance": [229.00],
      "volume_context": "high volume on up bars"
    },
    "4h": {
      "trend": "sideways",
      "wyckoff_phase": "C",
      "confirmed_events": ["SPRING_TEST"]
    }
  },
  "contradictions": [
    "Daily timeframe is bullish, but 1h shows supply near resistance."
  ],
  "decision_support": {
    "strategy_score": 72.5,
    "monte_carlo_pop": 0.61
  }
}
```

### Purpose - 1

The packet should help the LLM answer better by separating:

* observations
* interpretation
* trade plan
* uncertainty
* contradictions

### Acceptance Criteria_7

Phase 7 is complete when:

* The UI can generate an analyst packet for a ticker.
* The packet can be displayed as JSON.
* The packet can be copied to clipboard or saved as a file.
* The packet is shorter and clearer than the full raw report.

---

## Phase 8 — Analyst Chat Page

### Objective_8

Create a simple local chat interface for asking questions about the latest analysis.

### Existing Logic - 3

Use existing LLM/RAG modules where possible:

```text
marketflow/marketflow_llm_interface.py
marketflow/marketflow_llm_query_engine.py
scripts/ai_studio.py
```

### UI -1

Add tab:

```text
Wyckoff Volume Analyst
```

Inputs:

* selected ticker
* selected batch/latest report
* user question

The app should pass:

* analyst packet
* selected ticker context
* optional recent report narrative
* user question

### Example Questions

```text
Is this a valid Wyckoff long setup?
What is the strongest evidence for accumulation?
What contradicts the bullish case?
Where is the most logical invalidation level?
Which timeframe should I trust more?
Is this more likely accumulation or redistribution?
```

### Acceptance Criteria_8

Phase 8 is complete when:

* The user can ask questions about the selected ticker.
* The answer references only available analysis data.
* The answer separates observation, interpretation, and risk.
* The answer avoids inventing Wyckoff events not present in the packet.

---

## Phase 9 — Optional CLI Cleanup

### Objective_9

Expose the common workflows through the existing CLI.

Current CLI already supports:

```bash
python -m marketflow analyze AAPL
```

Optional new commands:

```bash
marketflow studio
marketflow batch AAPL MSFT NVDA
marketflow strategy --batch latest --tf 1d
marketflow mc --ticker AAPL --tf 1h
```

This is optional because the main goal is the personal UI.

---

## Streamlit Page Layout

Suggested first layout:

```text
MarketFlow Studio

Sidebar:
    Mode:
        Single ticker
        Batch
        Load previous result

    Ticker input
    Timeframe selection
    Run button

Main Tabs:
    1. Overview
    2. Reports
    3. Charts
    4. Strategy Ranking
    5. Monte Carlo
    6. Wyckoff Volume Analyst
```

---

## First Version Scope

The first useful version should only include:

```text
1. Single ticker analysis
2. Load latest report
3. Show summary
4. Show annotated CSV
5. Show one Wyckoff chart
```

Do not try to implement all phases at once.

Recommended first milestone:

```text
MVP-1:
    apps/marketflow_studio.py
    analysis_service.py
    report_index.py
```

---

## Development Rules

1. Keep existing scripts working.
2. Do not remove current CLI behavior.
3. Do not rewrite the analysis engine during the UI MVP.
4. Use services as wrappers around existing code.
5. Keep personal-use assumptions:

   * local machine
   * one user
   * no authentication
   * no deployment
6. Prefer small, testable functions.
7. Avoid hiding errors; show useful messages in the UI.
8. Save all generated outputs in the existing `.marketflow/reports` structure.
9. Do not add broker execution or live trading.
10. Keep financial output as analysis support, not trading advice.

---

## Suggested Implementation Order

### Milestone 1

```text
Create Streamlit shell
Create AnalysisService
Create ReportIndex
Run one ticker from UI
Load latest report
Display basic summary
```

### Milestone 2

```text
Add annotated CSV preview
Add timeframe selector
Add basic Wyckoff chart
```

### Milestone 3

```text
Add batch analysis
Add batch status table
Add latest batch report loading
```

### Milestone 4

```text
Add strategy ranking
Display candidate table
Allow candidate selection
```

### Milestone 5

```text
Add Monte Carlo tab
Run simulation from selected candidate
Show POP and generated plots
```

### Milestone 6

```text
Add analyst packet
Add Wyckoff Volume Analyst chat
```

---

## Final Target

The final personal-use app should feel like this:

```text
1. Open app.
2. Enter tickers.
3. Click Run.
4. Review ranked opportunities.
5. Open a ticker.
6. Inspect Wyckoff chart.
7. Run Monte Carlo if needed.
8. Ask the analyst:
   “Is this setup valid, and what would invalidate it?”
9. Save/export the result.
```

The app should make MarketFlow easier to use without making the project unnecessarily complex.

```bash

When you’re ready, the next step is a **CODEX implementation prompt** that tells it exactly what to build first, with guardrails so it doesn’t over-engineer the UI.
```
