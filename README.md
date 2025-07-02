# MarketFlow

**MarketFlow** is a modular, extensible Python framework for advanced Volume-Price Analysis (VPA) and Wyckoff Method analytics. It integrates robust data collection, processing, and AI-driven narrative synthesis for modern stock market analysis. MarketFlow is designed for clarity, testability, and ease of extension.

---

## 🚀 Features

- **Modular architecture:** Clean separation of data fetching, processing, signal analysis, and LLM-driven reporting.
- **Provider-agnostic data layer:** Easily add new data providers (e.g., Polygon.io, Yahoo Finance).
- **LLM integration:** Swappable support for OpenAI, Ollama, and other LLMs for natural language reporting, tool-calling, and concept explanations.
- **Robust error handling:** Retries, logging, and detailed diagnostics for every module.
- **Configurable and secure:** Environment-based config, `.env` secrets, and a central `config_manager.py`.
- **Extensible:** Add new strategies, signals, or analytics with minimal friction.

---

## 📁 Folder Structure

```bash
marketflow/
│
├── marketflow/                  # Core Python package
│   ├── __init__.py
│   ├── marketflow_config_manager.py        # Central config/env loader
│   ├── marketflow_data_provider.py         # Abstract + provider-specific data fetchers
│   ├── marketflow_processor.py         # Data processing/cleaning
│   ├── marketflow_analyzer.py          # Core VPA and Wyckoff analytics
│   ├── marketflow_signals.py           # Signal detection algorithms
│   ├── marketflow_wyc_module.py            # Wyckoff method analytics
│   ├── marketflow_facade.py            # Orchestrator: unified API for analytics, charting, reporting
│   ├── marketflow_logger.py            # Centralized logging
│   ├── market_flow_llm_providers.py         # LLM abstraction layer
│   ├── marketflow_memory_manager.py        # Conversation/session memory for LLMs
│   ├── marketflow_llm_interface.py     # Human-friendly narrative/report generator for LLM
│   ├── marketflow_llm_query_engine.py  # Orchestrates user query through LLM and backend
│   └── ...                      # (Other modules as needed)
│
├── scripts/                     # CLI, app entrypoints, notebooks, demos
│   └── vpa_app.py
│
├── tests/                       # Unit and integration tests
│   ├── test_data_provider.py
│   └── ...
│
├── .env                         # (Not committed) Your API keys and secrets
├── .gitignore                   # Standard ignore file
├── LICENSE                      # MIT license
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

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
    cp .env.example .env  # or create .env manually
    # Edit .env and add your API keys, e.g.:
    # POLYGON_API_KEY=your_polygon_api_key
    # OPENAI_API_KEY=your_openai_api_key
    # OLLAMA_BASE_URL=http://localhost:11434
    ```

3. **Run the CLI app:**

    ```bash
    python scripts/vpa_app.py --query "Analyze AAPL"
    ```

---

## 🛠️ Configuration

All configuration is managed by `config_manager.py` and environment variables.

- Do **not** commit your `.env` file.
- Use the `ConfigManager` class to access API keys and config in code.

---

## 📊 Extending MarketFlow

- **New data provider?**  
  Subclass `BaseDataProvider` in `data_provider.py`, and register it in the factory.
- **New signal or analytics?**  
  Add logic to `vpa_signals.py` or `vpa_analyzer.py`.
- **Custom reporting/LLM tools?**  
  Update `vpa_llm_interface.py` and `llm_providers.py`.
- **Testing:**  
  Add new tests to the `tests/` folder using mocks for API calls.

---

## 📝 License

MIT License

---

## 🤝 Contributing

Contributions welcome!  
Please open issues or pull requests to suggest improvements.

---

## 📚 Documentation

- Each module is documented with clear docstrings.
- See the code comments and CLI help for usage examples.

---

*MarketFlow: Modular, modern analytics for the modern market.*
