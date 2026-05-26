# MarketFlow

**MarketFlow** is a modular, extensible Python framework for advanced Volume-Price Analysis (VPA) and Wyckoff Method analytics.
It integrates robust data collection, processing, and AI-driven narrative synthesis for modern stock market analysis. MarketFlow
is designed for clarity, testability, and ease of extension.

## 🚀 Key Features

- Multi-timeframe VPA and Wyckoff analysis for any ticker
- **All candle/volume features are preserved and available in exports:**
  - `spread`, `body_percent`, `upper_wick`, `lower_wick`
  - `avg_volume`, `volume_ratio`, `volume_class`, `candle_class`
  - `price_direction`, `volume_direction`
- HTML, CSV, JSON, and TXT reports with all calculated features
- Provider-agnostic: Use Polygon.io or local data
- LLM/RAG-ready: Rich outputs for AI, ML, and dashboards
- Modern, modular codebase—easy to extend, maintain, and debug

---

## ⚡ Quickstart

1. **Clone the repo and set up a virtual environment:**

    ```bash
    git clone https://github.com/Martinolli/marketflow.git
    cd marketflow
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. **Set up your `.env` file with API keys:**

    ```bash
    # Create a .env file and add (examples):
    POLYGON_API_KEY=your_polygon_api_key
    OPENAI_API_KEY=your_openai_api_key
    OLLAMA_BASE_URL=http://localhost:11434
    ```

3. **Run an analysis:**

    ```bash
    # Analyze a single ticker (default timeframes)
    python scripts/marketflow_analysis.py AAPL

    # Optional: specify timeframes
    python scripts/marketflow_analysis.py AAPL --timeframes 1d 4h 1h
    ```

    Notes:

    - Recent changes and new scripts are summarized in `CHANGELOG.md`.
    - Reports are saved under `.marketflow/reports/<YYYY-MM-DD>/<TICKER>/` by default.

4. **Use the CLI (module form):**

    ```bash
    python -m marketflow analyze AAPL
    python -m marketflow analyze AAPL --timeframes 1d 4h 1h
    ```

5. **Install as a CLI (optional):**

    ```bash
    # from the repo root
    pip install -e .
    marketflow analyze AAPL
    marketflow analyze AAPL --timeframes 1d 4h 1h
    ```

## MarketFlow Studio

A personal local Streamlit interface is available on `main`:

```bash
streamlit run apps/marketflow_studio.py
```

The app can:

- run analysis
- load generated reports
- preview annotated CSV files
- show a basic Wyckoff candlestick chart
- rank strategy candidates
- run simple Monte Carlo simulations
- build Analyst Packets

See `MARKETFLOW_STUDIO_WORKFLOW.md` for the recommended cockpit flow across analysis, Strategy Ranking, Monte Carlo, Analyst Packet, and batch analysis.

The Monte Carlo/backtest calibration refactor is planned in `MARKETFLOW_MONTE_CARLO_BACKTEST_REFACTOR_PLAN.md`.

### Design Review Checkpoint

A current Studio design checkpoint is available at:

- `MARKETFLOW_STUDIO_DESIGN_REVIEW_CHECKPOINT_2026-05-23.md`

It summarizes implemented capabilities, usage checklists, known limitations, and planned future features.

By default, MarketFlow Studio reduces console log noise. To enable verbose logs:

```powershell
$env:MARKETFLOW_CONSOLE_LOG_LEVEL="INFO"
streamlit run apps/marketflow_studio.py
```

## Overview: Main Data Flow in MarketFlow

The MarketFlow system is organized around the facade pattern (via MarketflowFacade), which orchestrates a modular pipeline for multi-timeframe financial analysis. The main pathway is:

External Input (ticker, timeframes) → Data Acquisition → Preprocessing → Multi-Timeframe Analysis → Signal Generation → Risk Assessment (+Wyckoff/Pattern analysis)

### Module-by-Module Data Pathway

Below is a breakdown of the data flow and dependencies, referencing your modules:

#### 1. Entry Point: MarketflowFacade

Input: ticker, timeframes
Delegates to:
MultiTimeframeProvider → Data acquisition (price/volume for all timeframes)
MultiTimeframeAnalyzer → Feature extraction & Analysis per timeframe

#### 2. Data Acquisition

Module: marketflow_data_provider.py
PolygonIOProvider.get_data() fetches raw OHLCV data as (price_df, volume_series)
MultiTimeframeProvider.get_multi_timeframe_data() fetches for all configured timeframes, returns timeframe_data dict.

#### 3. Preprocessing

Module: marketflow_processor.py
DataProcessor.preprocess_data()
Aligns price and volume
Calculates candle properties, volume metrics, trend/volume direction
Outputs: processed_data (dict of derived features, e.g. price, volume, candle_class, etc.)

#### 4. Multi-Timeframe Analysis

Module: multi_timeframe_analyzer.py
For each timeframe:
CandleAnalyzer.analyze_candle()
TrendAnalyzer.analyze_trend()
PatternRecognizer.identify_patterns()
SupportResistanceAnalyzer.analyze_support_resistance()
Outputs: timeframe_analyses (per-tf dict of candle_analysis, trend_analysis, etc.)

#### 5. Signal Generation & Risk Assessment

Module: marketflow_signals.py
SignalGenerator.generate_signals()
Consumes timeframe_analyses and confirmation dict.
Returns a unified signal dict.
RiskAssessor.assess_trade_risk()
Consumes signal, current_price, and S/R levels.
Returns position sizing and risk metrics.

#### 6. Wyckoff/Pattern Analysis (Advanced)

Module: marketflow_wyckoff.py
Consumes processed_data
Returns detected Wyckoff phases, events, trading ranges, added to the analysis output.

#### 7. Text-Based Data Flow Diagram

```bash
User Request (ticker, timeframes)
    |
    v
MarketflowFacade.analyze_ticker()
    |
    v
+--------------------+
| MultiTimeframeProvider.get_multi_timeframe_data()         |  ---> [Per timeframe: raw price/volume]
+--------------------+
    |
    v
+--------------------+
| DataProcessor.preprocess_data()         |  ---> [processed_data: price, volume, candle_class, etc.]
+--------------------+
    |
    v
+--------------------+
| MultiTimeframeAnalyzer.analyze_multiple_timeframes()      |
|   ├─ CandleAnalyzer.analyze_candle()                     |
|   ├─ TrendAnalyzer.analyze_trend()                       |
|   ├─ PatternRecognizer.identify_patterns()               |
|   └─ SupportResistanceAnalyzer.analyze_support_resistance() |
+--------------------+
    |
    v
+--------------------+
| SignalGenerator.generate_signals()      |  ---> [signal dict]
| RiskAssessor.assess_trade_risk()        |  ---> [risk assessment]
+--------------------+
    |
    v
+--------------------+
| WyckoffAnalyzer.run_analysis()           |  ---> [phases, events, trading_ranges]
+--------------------+
    |
    v
Final Output (analysis dict with all above results)
```

##### **Key Data Structures at Each Step**

- Raw Data:

    price_df: OHLC DataFrame
    volume_series: Pandas Series

- Processed Data:

    Dict with keys: price, volume, spread, candle_class, volume_class, etc.

- Timeframe Analysis Result:

    Dict with keys: candle_analysis, trend_analysis, pattern_analysis, support_resistance, processed_data

- Signal:

    Dict: type, strength, details, evidence

- Risk Assessment:

    Dict: stop_loss, take_profit, risk_reward_ratio, position_size, etc.

- Wyckoff Output:

    Lists of detected phases, events, trading_ranges

### UML Diagram: MarketFlow Core Classes (Conceptual)

This UML class diagram shows the primary classes, their key methods, and relationships. The focus is on data flow and module dependencies, not every method or field.

```bash
+---------------------------------------------------------------+
|                        MarketflowFacade                       |
+---------------------------------------------------------------+
| - parameters: MarketFlowDataParameters                        |
| - data_provider: PolygonIOProvider                            |
| - multi_tf_provider: MultiTimeframeProvider                   |
| - multi_tf_analyzer: MultiTimeframeAnalyzer                   |
| - signal_generator: SignalGenerator                           |
| - risk_assessor: RiskAssessor                                 |
| - processor: DataProcessor                                    |
| - analyzer: PointInTimeAnalyzer                               |
+---------------------------------------------------------------+
| + analyze_ticker(ticker, timeframes) : dict                   |
| + analyze_ticker_at_point(ticker, data_by_tf): dict           |
| + get_signals(ticker, timeframes): dict                       |
| + explain_signal(ticker, timeframes): str                     |
+---------------------------------------------------------------+
                |         (uses)
                v
+-------------------------------+
| MultiTimeframeProvider        |-----------+
+-------------------------------+           |
| + get_multi_timeframe_data()  |           |
| + get_multi_timeframe_data_async()        |
+-------------------------------+           |
    |        (uses)                         |
    v                                       |
+-------------------------------+           |
| PolygonIOProvider             |           |
+-------------------------------+           |
| + get_data()                  |           |
| + get_data_async()            |           |
+-------------------------------+           |
                                            |
+-------------------------------+           |
| MultiTimeframeAnalyzer        |<----------+
+-------------------------------+
| + analyze_multiple_timeframes()|
| + identify_timeframe_confirmations()|
+-------------------------------+
    |        (uses)      
    v
+----------------+     +-------------------+    +----------------+
| CandleAnalyzer |     | TrendAnalyzer     |    | PatternRecognizer |
+----------------+     +-------------------+    +----------------+
| + analyze_candle()|  | + analyze_trend() |    | + identify_patterns() |
+----------------+     +-------------------+    +----------------+
    |                                       
    v                                       
+-----------------------------+             
| SupportResistanceAnalyzer   |             
+-----------------------------+             
| + analyze_support_resistance()|
+-----------------------------+

+-----------------------+      +------------------+
| SignalGenerator       |      | RiskAssessor     |
+-----------------------+      +------------------+
| + generate_signals()  |      | + assess_trade_risk() |
+-----------------------+      +------------------+

+---------------------+
| WyckoffAnalyzer     |
+---------------------+
| + run_analysis()    |
| + detect_events()   |
| + detect_phases()   |
+---------------------+

(Arrows: solid for composition/aggregation, dashed for use/call)
```

Notes:
    - Most modules depend on a shared MarketFlowDataParameters for configuration.
    - Data flows linearly through the pipeline, but results are bundled per timeframe.
    - The facade orchestrates the entire pipeline, calling each module in sequence.
    - The WyckoffAnalyzer operates on processed data per timeframe, after the main analysis.

How to Read This Diagram
Produced fields: Each module’s main output fields are listed under "produces" in the data flow diagram.
Consumed fields: Each module’s main input fields are listed under "consumes".
UML: Shows class relationships (not full attributes/methods for brevity) and how data flows via method calls.

## 🚀 Modules Description

| Module                    | Role                                                        |
| ------------------------- | ----------------------------------------------------------- |
| MarketflowFacade          | Orchestrates the entire analysis pipeline                   |
| PolygonIOProvider         | Fetches market data from external APIs                      |
| MultiTimeframeProvider    | Supports multi-timeframe data acquisition                   |
| DataProcessor             | Preprocesses and feature-engineers data                     |
| CandleAnalyzer            | Detects candlestick signals                                 |
| TrendAnalyzer             | Analyzes trend direction/strength                           |
| PatternRecognizer         | Finds market structure patterns (accumulation, tests, etc.) |
| SupportResistanceAnalyzer | Identifies support/resistance levels                        |
| WyckoffAnalyzer           | Detects Wyckoff phases, events, trading ranges              |
| MultiTimeframeAnalyzer    | Aggregates multi-timeframe results                          |
| SignalGenerator           | Synthesizes actionable signals                              |
| RiskAssessor              | Computes stops, targets, position size                      |
| MarketflowResultExtractor | Structures results for reporting                            |
| MarketflowReport          | Generates TXT, HTML, JSON reports                           |

### MarketflowFacade

### PolygonIOProvider

### MultiTimeFrameProvider

### DataProcessor

### CandleAnalyzer

### TrendAnalyzer

### PatternRecognizer

### SupportResistanceAnalyzer

### WyckoffAnalyzer

### MultiTimeFrameAnalyzer

### SignalGenerator

### RiskAssessor

### MarketflowResultExtractor

### MarketflowReport

## 🏗️ Project Structure

Development Notes

- Some folders/files are intentionally present as placeholders for future work (for example, `trading_dashboard/*` and `scripts/marketflow_app.py`). These may be empty until those features are implemented.
- Several files under `tests/` are demonstration or real-data exercises with `main()` entry points and may require valid API keys (Polygon) and network access to run.
- For a minimal, network-free check, run the mocked provider test: `pytest tests/test_data_provider.py -q`.

```bash
marketflow/
│
├── __pycache__ 
│
├── .marketflow/
│   ├── batch_reports_data                              # Output from `marketflow_batch_report.py` a CSV file with the data from llm_interface
│   ├── config                                          # Config Files
│   ├── logs                                            # Central config/env loader
│   ├── memory                                          # Abstract + provider-specific data fetchers
│   ├── reports                                         # Save Reports
│   └── snapshot_reports                                # Save Reports from `marketflow_analysis_snapshot.py save data from report for future use by LLM
|
├── .pytest_cache
|
|
├── .vscode/
|
├── data/
│   └── timeframe_data                                  # Tickers fetched data saved CSV files for future use, data saved by Tickers and Date to retrieve
│
├── deprecated_backup/
│   ├── backup_info.txt (✓ created)
│   └── modules/
│       ├── app.py (✓ backup)
│       ├── enhanced_ai_studio_code.py (✓ backup)
│       ├── enhanced_app.py (✓ backup)
│       ├── enhanced_appv1.py (✓ backup)
│       ├── marketflow_analysis.py (✓ backup)
│       ├── marketflow_analyzer.py (✓ backup)
│       ├── marketflow_config_manager_original.py (✓ backup)
│       ├── marketflow_ibkr_demo.py (✓ backup)
│       ├── marketflow_llm_query_engine_original.py (✓ backup)
│       ├── marketflow_logger_original.py (✓ backup)
│       ├── marketflow_risk_placement.py (✓ backup)
│       ├── minimal_rag.py  (✓ backup)
│       ├── quick_connect_test.py  (✓ backup)
│       ├── README.md  (✓ backup)
│       ├── repair_tvm_namespace.py  (✓ backup)
│       ├── retriever_original.py  (✓ backup)
│       └── web_interface.py (✓ backup)                 
│
├── env                                                 # (Not committed) Environment
|
├── knowledgebase/                                      # KNowledge Datase      
│   ├── chunked/ (✓ created)                            # Chunked Files
│   ├── embeddings (✓ created)                          # Embeddings Files
│   ├── sources (✓ created)                             # Sources Files
│   └── vectordb (✓ created)                            # Embeddings DB file
│
│       
├── markdown_files/
│   ├── marketflow_files_compatibility_analysis.md (✓ created)
│   ├── marketflow_replacement_backup_guide.md (✓ created)
│   ├── post_replacement_verification_checklist.md (✓ created)
│   └── marketflow_analyzer_changes.md (✓ created)
│
│       
│
├── marketflow/                                                 # Core Python package
│   ├── __pycache__
│   ├── concepts/
│   │    ├── vpa_concepts.yaml (✓ new)                         # Concepts file to integrate to marketflow_llm_interface.py
│   │    └── wyckoff_concepts.yaml (✓ new)                     # Concepts file to integrate to marketflow_llm_interface.py
│   ├── examples/
│   │    └── integration_example.py (✓ new)                    # Integration example script
│   ├── __init__.py
│   ├── batch_utils.py (✓ new)                                 # This script generates a CSV file containing summary data from a JSON analysis file.
│   ├── candle_analyzer.py  (✓ new)                            # Analyze Candles Script
│   ├── enums.py                                                # Enum definitions
│   ├── marketflow_analysis.py (✓ new)                         # This script runs a market analysis for a given ticker symbol using the MarketflowFacade.
│   ├── marketflow_config_manager.py (✓ replaced)              # Central config/env loader
│   ├── marketflow_data_parameters.py (✓ new)                  # This module contains the data parameters to be used by processor
│   ├── marketflow_data_provider.py (✓ replaced)               # Abstract + provider-specific data fetchers
│   ├── marketflow_facade.py  (✓ new)                          # Orchestrator: unified API for analytics, charting, reporting
│   ├── marketflow_llm_interface.py  (✓ new)                   # Human-friendly narrative/report generator for LLM
│   ├── marketflow_llm_narrative.py  (✓ new)                   # Refactor llm_interface to reduce the code size, the narrative for llm_interface
│   ├── marketflow_llm_query_engine.py  (✓ new)                # Handles all LLM-driven query processing for MarketFlow with robust architecture.
│   ├── marketflow_logger.py (✓ replaced)                      # Centralized logging
│   ├── marketflow_memory_manager.py ✓ new)                    # Conversation/session memory for LLMs
│   ├── marketflow_polygon_tools.py (new)                       # Polygon Tools Requesting Code
│   ├── marketflow_processor.py  (✓ new)                       # Data processing/cleaning
│   ├── marketflow_report.py  (✓ new)                          # Report generation
│   ├── marketflow_results_extractor.py  (✓ new)               # Extractor Data from Facade
│   ├── marketflow_signals.py   (✓ new)                        # Signal detection algorithms
│   ├── marketflow_snapshot.py   (✓ new)                       # This module provides advanced functionality for capturing, storing, and retrieving MarketFlow
│   ├── marketflow_utils.py (✓ new)                            # This module contains common, reusable functions that are shared across different
│   ├── marketflow_wyckoff_confirmation_adapter.py (✓ new)     # Adds conservative confirmation and scoring to events.
│   ├── marketflow_wyckoff.py (✓ new)                          # Wyckoff method analytics
│   ├── multi_timeframe_analyzer.py (✓ new)                    # Multi timeframe analytics
│   ├── pattern_recognizer.py (✓ new)                          # Pattern recognition algorithms
│   ├── point_in_time_analyzer.py (✓ new)                      # Point in time analytics
│   ├── support_resistance_analyzer.py (✓ new)                 # Support and Resistance algorithms
│   ├── transient_vector_memory.py (✓ new)                     # This script implements a transient vector memory (TVM) system using FAISS for efficient similarity search.
│   ├── trend_analyzer.py (✓ new)                              # Trend Analyzer algorithms
│   ├── marketflow_llm_providers.py (TBD)                       # LLM abstraction layer
│   ├──
│   └── ...                                             # (Other modules as needed)
│
├── rag/                                                # RAG scripts
│   ├── __init__.py
│   ├── chunker.py  (✓ new)                            # Chunker script
│   ├── embedder_vector_db.py  (✓ new)                 # Embedder DB script                                      
│   ├── embedder.py (✓ new)                            # Embedder script
│   ├── query_vectordb.py (✓ new)                      # Query Vector DB script
│   └── retriever.py (✓ new)                           # Retriever scrip
│
├── scripts/                                            # CLI, app entrypoints, notebooks, demos
│   ├── __pycache__
│   ├── ai_studio_code.py  (✓ new)                      # Script to interact with LLM and the Embedded files
│   ├── ai_studio.py  (✓ new)                           # This script provides the main entry point for the Marketflow application, interact with llm_query_engine
│   ├── marketflow_analysis_llm_interface.py  (✓ new)   # Script to collect data and pass through llm_interface
│   ├── marketflow_analysis_snapshot.py  (✓ new)        # Analysis script and Snapshot Interface generation
│   ├── marketflow_analysis.py  (✓ new)                 # Analysis script
│   ├── marketflow_batch_analysis.py  (✓ new)           # Marketflow Batch Analysis Orchestrator
│   ├── marketflow_batch_report.py  (✓ new)             # Analysis script for a list of tickers
│   ├── marketflow_fair_price_calculation.py  (✓ new)   # Calculate the fair price of a stock using DCF and Venture-DCF methods
│   ├── marketflow_integration_example.py               # Integration Example
│   ├── marketflow_macp.py                              # MACP calculation for a given portfolio
│   ├── plot_annotated_features.py  (✓ new)             # Plot script
│   └── marketflow_app.py (TBD)                         # Empty to be developed
│
├── tests_outputs/                                      # Outputs Tests Files
│   └── tests_files                                     # HTML, JSON, TXT files
│
├── tests/                                              # Unit and integration tests
│   ├── __pycache__                                     
│   ├── demo_marketflow_modules.py (✓ new)
│   ├── test_candle_analyzer_real_data.py (✓ new)
│   ├── test_data_provider_async.py (✓ new)
│   ├── test_data_provider_simple.py (✓ new)
│   ├── test_data_provider.py
│   ├── test_test_integration_core_pipeline.py (✓ new)
│   ├── test_marketflow_data_parameters.py (✓ new)
│   ├── test_marketflow_facade_real_data.py (✓ new)
│   ├── test_marketflow_modules.py (✓ new)
│   ├── test_marketflow_processor_integration.py (✓ new)
│   ├── test_multi_timeframe_analyzer_real_data.py (✓ new)
│   ├── test_pattern_recognizer_real_data.py (✓ new)
│   ├── test_point_in_time_analyzer_real_data.py (✓ new)
│   ├── test_signals.py (✓ new)
│   ├── test_support_and_resistance_real_data.py (✓ new)
│   ├── test_trend_analyzer_real_data.py (✓ new)
│   ├── test_wyckoff_phases.py (✓ new)
│   ├── test_wyckoff_real_data.py
│   ├── test_wyckoff.py (✓ new)
│   └── ...
│
├── trading_dashboard/                                  # To be developed
│
├── .env                                                # (Not committed) Your API keys and secrets
├── .gitattributes                                      # Define long files to be ignored
├── .gitignore                                          # Standard ignore file
├── LICENSE                                             # MIT license
├── requirements.txt                                    # Python dependencies
├── README.md                                           # This file
├── CHANGELOG.md                                        # Document the Changes
├── backup_and_replace.bat (✓ created)
├── setup.py (✓ created)
│  
│
│
└── marketflow_finetuning/                              # NEW: The home for all training activities
    │
    ├── 1_data_generation/
    │   ├── get_ticker_list.py                          # Script to fetch a diverse list of tickers
    │   └── generate_dataset.py                         # Main script to run your VPA and Wyckoff data engine and create raw data
    │
    ├── 2_datasets/
    │   ├── raw/                                        # Raw JSON outputs from your engine
    │   │   ├── aapl_2023-01-15.json
    │   │   └── ...
    │   ├── formatted/                                  # Data formatted for fine-tuning
    │   │   ├── training_data.jsonl
    │   │   └── validation_data.jsonl
    │   └── golden_test_set.jsonl                       # A hold-out set for final model evaluation
    │
    ├── 3_training/
    │   ├── configs/                                    # Training configuration files (e.g., for Axolotl)
    │   │   └── llama3_marketflow_tune.yml
    │   ├── train.py                                    # Script to launch the fine-tuning job (e.g., using OpenAI SDK or Hugging Face)
    │   └── notebooks/                                  # Jupyter notebooks for experimentation
    │       └── 01_explore_data.ipynb
    │
    ├── 4_evaluation/
    │   ├── evaluate_model.py                           # Script to compare model outputs against the golden_test_set
    │   └── results/                                    # Stored evaluation results
    │       └── llama3_marketflow_v1_results.json
    │
    ├── 5_models/                                       # Directory to store model checkpoints (for open-source models)
    │   └── llama3-8b-marketflow-v1/
    │
    └── management_ui.py                                # NEW: A Streamlit/Gradio app for managing the whole process

```

## 🧩 Modular Architecture

Easily extend with new:

Data providers (e.g., Yahoo Finance, custom API)

Features or analytics modules

LLM or RAG integrations

## 🛡️ Configuration & Security

All config via .env or marketflow_config_manager.py

Never commit your API keys!

See the code for advanced configuration and logging options

## 📝 License

MIT License

## 🤝 Contributing

Contributions and suggestions are welcome!
Open an issue or pull request to get started.
