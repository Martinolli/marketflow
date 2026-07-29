# Manual Network Checks

MarketFlow's default pytest suite is deterministic and offline. It must not require provider credentials, call external services, or modify tracked repository files.

Manual checks that may require credentials or external services live under:

```text
scripts/manual_checks/
```

These scripts are not part of the deterministic release gate and are not collected by default pytest. Run them only when deliberately validating provider-backed or LLM-backed behavior in an environment configured for that purpose.

Examples:

```powershell
$python = (Resolve-Path ".\env\Scripts\python.exe").Path
& $python scripts\manual_checks\real_market_data_check.py
& $python scripts\manual_checks\data_provider_simple_check.py
& $python scripts\manual_checks\complete_integration_check.py
& $python scripts\manual_checks\enhanced_query_engine_check.py
& $python scripts\manual_checks\enhanced_rag_check.py
& $python scripts\manual_checks\marketflow_facade_real_data_check.py
& $python scripts\manual_checks\multi_timeframe_analyzer_real_data_check.py
```

Manual-check results are observational evidence only. They are not a substitute for the default offline test suite, and they do not validate swing-strategy consistency or trading recommendations.
