# MarketFlow

MarketFlow is a local research cockpit for multi-timeframe market analysis. It combines Volume Price Analysis and Wyckoff annotations with strategy review, historical validation, calibration services, and inspectable report artifacts.

## Current Capabilities

- Multi-timeframe OHLCV analysis with VPA and Wyckoff annotations
- HTML, JSON, text, and annotated CSV report generation
- Strategy Ranking for reviewing generated analysis candidates
- Historical Walk-Forward Validation with deterministic outcome evaluation
- Walk-Forward Run Registry with source fingerprints, run parameters, and stale/active state
- Walk-Forward Campaign Aggregation across registered or discovered runs
- Backtest and Monte Carlo forecast-versus-actual calibration summaries
- Parameter Profiles and data sufficiency diagnostics
- Point-and-Figure and price-volume Eigen diagnostics
- Streamlit-based MarketFlow Studio for running and reviewing the workflow locally

MarketFlow is research infrastructure. It does not automatically optimize strategies, execute trades, or guarantee profitable outcomes.

## Quickstart

```powershell
git clone https://github.com/Martinolli/marketflow.git
cd marketflow
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file and provide the API credentials required by the data providers you use. Do not commit `.env` or generated report data.

Run a ticker analysis:

```powershell
python scripts\marketflow_analysis.py AAPL --timeframes 1d 4h 1h
```

Reports are written under `.marketflow/reports/<YYYY-MM-DD>/<TICKER>/` by default.

## Run MarketFlow Studio

```powershell
streamlit run apps\marketflow_studio.py
```

Studio can run or load analysis, preview artifacts, rank candidates, perform historical walk-forward validation, maintain run registries, aggregate campaigns, and review calibration outputs.

## Typical Workflow

1. Run ticker analysis.
2. Inspect generated reports and annotated CSVs.
3. Run Strategy Ranking.
4. Run Historical Walk-Forward Validation for the required timeframe, profile, and event-filter combinations.
5. Review the Walk-Forward Run Registry for coverage, stale inputs, and duplicate/superseded runs.
6. Run the Walk-Forward Campaign Aggregator.
7. Review campaign coverage, outcome distribution, and grouped historical statistics.

## Reports and Artifacts

Ticker artifacts normally live in:

```text
.marketflow/reports/<YYYY-MM-DD>/<TICKER>/
```

Depending on the workflow, a report folder can contain annotated market data, HTML/JSON/text reports, backtest or Monte Carlo outputs, walk-forward cases/results/summaries, run registry JSON/CSV manifests, and campaign CSV/Markdown reports. Runtime reports are ignored by Git; only explicit test fixtures should be versioned.

## Documentation Map

- [Documentation index](docs/README.md)
- [MarketFlow Studio workflow](docs/workflow/MARKETFLOW_STUDIO_WORKFLOW.md)
- [Historical Walk-Forward Validation plan](docs/plans/MARKETFLOW_HISTORICAL_WALK_FORWARD_VALIDATION_PLAN.md)
- [Walk-Forward Validation milestone status](docs/status/MARKETFLOW_WALK_FORWARD_VALIDATION_MILESTONE_STATUS.md)
- [Studio design review](docs/design/MARKETFLOW_STUDIO_DESIGN_REVIEW_CHECKPOINT_2026-05-23.md)
- [Personal/UI planning archive](markdown_files/marketflow_personal_ui_plan.md)
- [Legacy detailed README](docs/archive/MARKETFLOW_LEGACY_README.md)

## Guardrails

- MarketFlow is a research and analysis tool, not financial advice.
- Historical results do not guarantee future performance.
- Candidate ranking and workflow validity are separate from investment suitability.
- Walk-forward and calibration services report saved evidence; they do not automatically select or optimize a strategy.
- Users remain responsible for data quality, parameter choices, interpretation, and risk decisions.

## Development

Run the full test suite:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python -m pytest -q
```

The default pytest suite is deterministic and offline. It must not require credentials, make external network calls, or write tracked report artifacts. Pytest-generated temporary files should use pytest temporary directories or ignored runtime paths.

Manual provider or LLM checks are separate from the default suite. See [Manual network checks](docs/testing/MANUAL_NETWORK_CHECKS.md) before running scripts under `scripts/manual_checks/`.

Packaging metadata is generated from `setup.py` and `requirements.txt`; generated `*.egg-info/`, `*.dist-info/`, `build/`, and `dist/` directories are ignored and should not be committed.

Run Studio locally:

```powershell
streamlit run apps\marketflow_studio.py
```

See [CHANGELOG.md](CHANGELOG.md) for historical changes and [docs/README.md](docs/README.md) for planning, status, workflow, design, and reference documents.
