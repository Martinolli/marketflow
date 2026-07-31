# MarketFlow Operational Pipeline Audit Plan

Status: PASS

Date: 2026-07-31

Branch: `feature/swing-operational-pipeline-audit`

Base commit: `da6cb3564ed77135852741b216075f421a0d128e`

## Mission

Audit and harden the two operator-used operational workflows without running
performance analysis, modifying market-data files, invoking providers, adding
broker/execution capability, changing dependencies, or changing accepted
Strategy semantics.

## Workflows

Workflow A:

```powershell
env\Scripts\python.exe scripts\marketflow_batch_analysis.py TICKER1 TICKER2
env\Scripts\python.exe marketflow\marketflow_monte_carlo_trade.py ".marketflow\reports\<date>\<ticker>\<ticker>_<tf>_wyckoff_annotated.csv" --entry <entry> --sl <stop> --tp <target> --tf <tf> --horizon <bars>
env\Scripts\python.exe scripts\plot_annotated_features.py ".marketflow\reports\<date>\<ticker>\<ticker>_<tf>_wyckoff_annotated.csv" --mc-summary ".marketflow\reports\<date>\<ticker>\<timestamp>_mc_summary.json"
```

Classification: `MANUAL_SCENARIO_ANALYSIS`.

Workflow B:

```powershell
env\Scripts\python.exe scripts\marketflow_batch_analysis.py TICKER1 TICKER2
env\Scripts\python.exe marketflow\marketflow_strategy.py --report-root ".marketflow\reports" --date-glob "<exact-run-or-date>" --tf <tf> --tickers TICKER1 TICKER2
env\Scripts\python.exe marketflow\marketflow_monte_carlo_trade.py "<candidate source_csv>" --entry <candidate entry> --sl <candidate stop_loss> --tp <candidate take_profit> --tf <candidate timeframe> --horizon <bars>
env\Scripts\python.exe scripts\plot_annotated_features.py "<candidate source_csv>" --mc-summary "<exact MC summary>"
```

Classification: `CANONICAL_STRATEGY_DECISION_SUPPORT`.

## Audit Steps

- Confirm branch, base commit, clean tree, and `pip check`.
- Read required workflow entry points, imported services, acceptance/status
  documents, README/protocol documentation, and report/artifact services.
- Inventory CLI arguments, defaults, files read/written, artifact lookup, and
  provider/offline behavior.
- Inspect `.marketflow/reports` for filenames, directory structure, schemas,
  metadata fields, and artifact linkage only.
- Add fail-closed handoff contracts and tests using synthetic temporary data.
- Run focused tests, collect-only, full default tests, compileall, and
  `git diff --check`.

## Acceptance Criteria

- Exact ticker/timeframe/source identity is required for Strategy input.
- MC evidence for Strategy is accepted only when exactly one requested-timeframe
  summary exists; no newest-file fallback.
- Plot MC overlay requires an explicit matching `--mc-summary`; no directory
  scan for newest MC summary.
- Manual scenario and canonical Strategy workflows carry distinct workflow
  labels.
- Canonical MC request geometry is copied from candidate fields and verified for
  equality.
- Report output paths have a reusable collision-prevention contract.
- LLM and Streamlit remain outside authoritative Strategy/MC contracts.
