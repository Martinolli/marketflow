# Changelog

All notable changes to this project are documented in this file.

    **Version Date = 2025 August 03**

| Date       | Revision |
|------------|----------|
| 2025-08-03 | v1.17    |
| 2025-07-28 | v1.16    |
| 2025-07-20 | v1.15    |
| 2025-07-17 | v1.14    |
| 2025-07-15 | v1.13    |
| 2025-07-15 | v1.12    |
| 2025-07-12 | v1.11    |
| 2025-07-12 | v1.11    |
| 2025-07-12 | v1.10    |
| 2025-07-12 | v1.9     |
| 2025-07-11 | v1.8     |
| 2025-07-10 | v1.7     |
| 2025-07-10 | v1.7     |
| 2025-07-10 | v1.7     |
| 2025-07-10 | v1.7     |
| 2025-07-10 | v1.7     |
| 2025-07-10 | v1.7     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-09 | v1.6     |
| 2025-07-06 | v1.5     |
| 2025-07-06 | v1.4     |
| 2025-07-05 | v1.3     |
| 2025-07-05 | v1.3     |
| 2025-07-05 | v1.3     |
| 2025-07-05 | v1.3     |
| 2025-07-04 | v1.2     |
| 2025-07-03 | v1.1     |
| 2025-07-03 | v1.1     |
| 2025-07-03 | v1.1     |
| 2025-07-01 | v1.0     |

---

## [1.17.0]

### Added 17 - 2025-08-03

- Development of `marketflow_batch_report.py`
    Script to run analysis for different tickers from a LIST

- Refactor `marketflow_llm_interface.py`
    Split the narrative to a different module to reduce the size of the code.
    Create YAML files to store the concepts: VPA and Wyckoff Methods

- First Version for `marketflow_llm_query_engine.py`
    Provider-agnostic LLM interface with OpenAI as default
    Advanced intent recognition with confidence scoring
    RAG integration for knowledge retrieval
    Multi-turn conversation support
    Comprehensive error handling and logging
    Input validation and sanitization

- Refactor the `chunker.py`
    To be able to chunk "DOCX" files
    Update the knowledgebase with a new file: Wyckoff Method Original Book from Mr. Wyckoff
    Update the Embeddings and vectors with the new chunks
    Update the DB with the new embeddings vectors.

---

## [1.16.0]

### Added 16 - 2025-07-28

- Development of `marketflow_llm_interface`
    LLM interface This module provides an intelligent, narrative-driven interface for LLMs
    to interact with the advanced VPA and Wyckoff analysis engine.

- Development of `marketflow_snapshot`
    his module provides advanced functionality for capturing, storing, and retrieving MarketFlow
    analysis results with comprehensive support for historical data storage, chart plotting,
    information display, and LLM interface/training data preparation.

- Development of `marketflow_analysis`
    Three (3) different scripts to run analysis using complete analysis plus Snapshot and LLM Interface script,
    and pure analysis and results.

---

## [1.15.0] - 2025-07-20

### Added 15

- Initial development of `marketflow_snapshot`
    Multi-layared data architecture with semantic modeling
    First version - not working so good - need to be refactored

---

## [1.14.0] - 2025-07-17

### Added 14

- Streamlined README.md focusing on key features and onboarding.
- Project roadmap/next steps plan template.
- Initial CHANGELOG.md for transparent version tracking.
- Initial Script to plot data from CSV files from generated reports with annotated information
- Initial Script to analyze integrated script/logic using complete pipeline from:
     `data_provider` -> `facade` -> `extractor` -> `report`.

---

## [1.13.0] - 2025-07-15

### Added 13

- Full feature propagation: all computed fields (`spread`, `body_percent`, `upper_wick`, `lower_wick`, `avg_volume`, `volume_ratio`, `volume_class`, `candle_class`, `price_direction`, `volume_direction`) are now preserved from data processing through export (CSV, HTML, JSON).
- Sample output table in README.md showing all preserved features.

### Changed

- Refactored data pipeline to ensure no feature loss between modules (`marketflow_processor.py`, `marketflow_facade.py`, etc.).
- README.md restructured and cleaned for clarity and easier onboarding.

### Fixed

- Issue where advanced candle/volume features were not appearing in reports or exports.
- Source field now appears correctly in RAG/ChromaDB retrieval (no more `Source: ?`).

---

## [1.12.0] - 2025-07-15

### Added 12

- `embedder_vector_db.py` for ChromaDB/SQLite-based persistent vector DB.
- ChromaDB retrieval option in `retriever.py` (faster, scalable RAG queries).

---

## [1.11.0] - 2025-07-12

### Added 11

- `chunker.py`, `embedder.py`, and `retriever.py` modules for chunked doc embeddings and retrieval.
- `marketflow_report.py` for automated multi-format report generation.
- `marketflow_result_extractor.py` for output structuring and access.

---

## [1.10.0] - 2025-07-12

### Added 10

- `marketflow_result_extractor.py` module for unified results extraction.

---

## [1.9.0] - 2025-07-12

### Deprecated

- `marketflow_analyzer.py` (split into new modular components).

---

## [1.8.0] - 2025-07-11

### Added 8

- `marketflow_facade.py` pipeline orchestrator (facade pattern for analysis flow).

---

## [1.7.0] - 2025-07-10

### Added 7

- New modular analytics components: `candle_analyzer.py`, `trend_analyzer.py`, `pattern_recognizer.py`, `support_resistance_analyzer.py`, `multi_timeframe_analyzer.py`, `point_in_time_analyzer.py`.

---

## [1.6.0] - 2025-07-09

### Changed 6

- Major refactor: Split `marketflow_analyzer.py` into modular files for maintainability.

---

## [1.5.0] - 2025-07-06

### Added 5

- `marketflow_analyzer.py` initial analytics engine module.

---

## [1.4.0] - 2025-07-06

### Added 4

- `enums.py` (enum definitions for consistent classification).

---

## [1.3.0] - 2025-07-05

### Added 3

- `marketflow_wyckoff.py`, `marketflow_signals.py`, `marketflow_processor.py`, `marketflow_data_parameters.py` for advanced analytics and parameterization.

---

## [1.2.0] - 2025-07-04

### Added 2

- `marketflow_polygon_tools.py` for Polygon.io data integration.

---

## [1.1.0] - 2025-07-03

### Added 1

- `marketflow_config_manager.py` and `marketflow_logger.py` refactor for robust logging and configuration.
- `marketflow_utils.py` for shared helpers.
- `marketflow_data_provider.py` for async data access.

---

## [1.0.0] - 2025-07-01

### Added 0

- **Initial release:** All core modules, multi-timeframe analysis, report generation, configuration, and logging.

---
