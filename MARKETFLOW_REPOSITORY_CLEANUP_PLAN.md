# MARKETFLOW_REPOSITORY_CLEANUP_PLAN

## 1. Purpose

This plan defines how to clean the MarketFlow repository safely without losing potentially useful prototype or historical code.

This is a planning checkpoint only. No files are deleted, moved, renamed, or behaviorally changed here. Cleanup should be staged, reversible, and documented so useful experiments can be preserved before any removal is considered.

## 2. Current Repository Health Snapshot

MarketFlow Studio is actively developed and now covers report loading, charts, Strategy Ranking, Monte Carlo, Analyst Packet, analyst prompt/chat artifacts, manual review notes, and early backtest calibration support.

The backtest refactor is in progress, with deterministic outcome evaluation, JSON-safe services, candidate snapshot normalization/validation, candidate CSV artifacts, artifact classification, and a Studio save control for candidate snapshots.

The repository also contains deprecated/prototype code, old tests, historical backup material, empty or partial skeletons, generated local files, and optional integration experiments. Focused backtest tests pass, while full pytest has known unrelated collection failures from deprecated or stale areas. Cleanup is needed to separate active code from historical/prototype material and improve test reliability.

Known full-pytest collection issues to preserve in the cleanup plan:

- missing CSV fixture in `deprecated_backup/modules/plot_ohlc_test.py`
- missing optional `ib_insync` in `deprecated_backup/modules/quick_connect_test.py`
- missing `scripts.marketflow_analysis_llm_interface` in `tests/test_llm_interface.py`

Note: the current tree contains `scripts/marketflow_analysis_llm_interface.py`, so the LLM-interface failure should be revalidated before changing the test. It may be stale, environment-dependent, or caused by an import inside that module.

## 3. Cleanup Principles

- preserve first, delete later
- classify before moving
- archive instead of delete when uncertain
- do not break imports
- do not hide active failures by accident
- keep cleanup commits small
- document every category
- avoid mixing cleanup with feature work

## 4. Inventory Categories

```text
active_core
active_studio
active_services
active_backtest
active_tests
prototype_keep
deprecated_archive
broken_tests_quarantine
optional_dependency_tests
missing_fixture_tests
empty_skeleton
delete_candidate_later
unknown_review_needed
```

Category meanings:

- `active_core`: Current package logic required by active workflows.
- `active_studio`: Current Streamlit Studio application and direct UI support code.
- `active_services`: Service modules used by Studio, scripts, or tests.
- `active_backtest`: Current backtest/refactor modules and tests.
- `active_tests`: Tests that should run in normal focused or full test workflows.
- `prototype_keep`: Prototype code that may be useful later but is not active.
- `deprecated_archive`: Historical code retained for reference or rollback.
- `broken_tests_quarantine`: Tests that fail collection or depend on removed/stale code.
- `optional_dependency_tests`: Tests requiring optional packages, broker/API access, or external services.
- `missing_fixture_tests`: Tests depending on local/private files that are absent from the repo.
- `empty_skeleton`: Empty or near-empty scaffold files/directories.
- `delete_candidate_later`: Files likely removable after confirmation and a dedicated cleanup commit.
- `unknown_review_needed`: Files that need owner review before classification.

## 5. Initial Candidate Inventory

### deprecated_backup/

`deprecated_backup/` appears historical/prototype. It contains `backup_info.txt`, a long README/revision history, old modules, old Streamlit/app experiments, original module backups, RAG prototypes, Monte Carlo prototypes, IBKR/broker experiments, and test-like files.

It also contains files that cause or have caused full-pytest collection issues:

- `deprecated_backup/modules/plot_ohlc_test.py`
- `deprecated_backup/modules/quick_connect_test.py`

Classification: `deprecated_archive`, with specific test-like files classified as `broken_tests_quarantine`, `missing_fixture_tests`, or `optional_dependency_tests`.

Recommended future action: do not delete immediately. First quarantine pytest-collected test-like files, then decide whether the folder should remain in place, move under an archive namespace, or be preserved by git history/tag.

### trading_dashboard/

`trading_dashboard/` contains several zero-byte skeleton files:

- `analysis.py`
- `app.py`
- `charts.py`
- `static/style.css`
- `templates/index.html`

It also contains large non-empty files:

- `base_client.py`
- `stocks.py`

The user identified this area as an old/empty dashboard skeleton, but the non-empty files mean it should not be deleted without review.

Classification: `empty_skeleton` for zero-byte scaffold files, `prototype_keep` or `unknown_review_needed` for non-empty files.

Recommended future action: inspect imports and purpose, then either archive under `archive/prototypes/trading_dashboard/` or remove the confirmed-empty skeleton in a dedicated cleanup commit.

### tests/test_llm_interface.py

`tests/test_llm_interface.py` references `scripts.marketflow_analysis_llm_interface`. Recent full-pytest runs reported a missing-module collection issue. The current tree appears to contain `scripts/marketflow_analysis_llm_interface.py`, so this needs revalidation before action.

Classification: `broken_tests_quarantine` or `unknown_review_needed`.

Recommended future action: run this test alone, inspect its import chain, then choose one path: restore missing dependency, update stale imports, add skip guards, or archive the stale interface test.

### deprecated_backup/modules/plot_ohlc_test.py

This file reads `1d_2025-08-17_10-45-17.csv` directly at import time. That local CSV fixture is not present, so pytest collection can fail before test execution.

Classification: `missing_fixture_tests`.

Recommended future action: quarantine, rewrite with a small synthetic fixture, or archive if it is only a manual plotting experiment.

### deprecated_backup/modules/quick_connect_test.py

This file imports `ib_insync` at module import time. It is a broker/connectivity experiment and should not run in normal unit-test collection without the optional dependency and explicit integration-test intent.

Classification: `optional_dependency_tests`.

Recommended future action: quarantine or mark as an integration test with skip guards for missing `ib_insync` and missing explicit environment opt-in.

### deprecated_backup/modules/marketflow_ibkr_demo.py and marketflow_risk_placement.py

These files also import `ib_insync` and appear tied to broker/IBKR workflows.

Classification: `optional_dependency_tests` or `prototype_keep`.

Recommended future action: preserve for review, but keep out of normal test/import paths unless integration prerequisites are explicit.

### deprecated_backup/modules/*_original.py and *_v1.py

Examples include:

- `marketflow_config_manager_original.py`
- `marketflow_logger_original.py`
- `marketflow_llm_query_engine_original.py`
- `plot_annotated_features_v1.py`
- `monte_carlo_trade_v1.py`

Classification: `deprecated_archive`.

Recommended future action: compare only if needed, then preserve in archive or rely on git history after a documented cleanup decision.

### Root-level local/generated candidates

Observed root-level candidates:

- `streamlit_marketflow_8502.err.log`
- `streamlit_marketflow_8502.out.log`
- `streamlit_marketflow_8503.err.log`
- `streamlit_marketflow_8503.out.log`
- `bfg-1.14.0.jar`
- `backup_and_replace.bat`
- `.pytest_cache/`
- `__pycache__/`
- `env/`
- `marketflow.egg-info/`
- `test_outputs/`

Classification: `delete_candidate_later` or `unknown_review_needed`, depending on whether each item is generated, local-only, or intentionally tracked.

Recommended future action: review git tracking status and `.gitignore` before removing or ignoring anything.

## 6. Test Cleanup Strategy

### Stage 1 - Inventory only

No changes except this plan.

### Stage 2 - Quarantine broken/deprecated tests

Options:

- move old tests under `archived_tests/`
- rename old tests so pytest does not collect them
- add pytest markers for optional dependencies
- add skip guards for missing optional packages
- add fixture availability checks

Do not implement these in this checkpoint.

### Stage 3 - Restore or remove missing fixtures

Options:

- add a small synthetic fixture if the test is useful
- rewrite the test to avoid local/private file dependency
- archive the test if it is not useful

### Stage 4 - Optional dependency policy

For optional broker/API tests involving `ib_insync`, connectivity, credentials, or external services:

- mark them as integration tests
- skip by default unless dependencies are installed
- require an explicit environment variable before live connectivity tests run
- never run broker/API tests as part of normal unit-test collection

## 7. Deprecated Code Strategy

Options:

- keep in place but document as deprecated
- move to `archive/deprecated_backup/`
- preserve via git tag before removal
- extract useful modules into the active package only after review

Recommended approach: do not delete in the first cleanup implementation. Archive or quarantine only after inventory and import checks.

## 8. Prototype Code Strategy

Prototype code should be reviewed by purpose:

- identify whether the prototype contains unique logic
- label the intended purpose if known
- move to `archive/prototypes/` only after import checks
- avoid active package namespace pollution
- extract useful pieces into active modules only in separate feature/refactor commits

## 9. Empty Skeleton Strategy

For `trading_dashboard/`:

- inspect contents before action
- classify zero-byte files as `empty_skeleton`
- classify non-empty `base_client.py` and `stocks.py` as `prototype_keep` or `unknown_review_needed`
- do not delete in this planning checkpoint

Recommended future action:

- either remove confirmed-empty skeleton files in a dedicated cleanup commit
- or move the dashboard skeleton to `archive/prototypes/trading_dashboard/`

## 10. Active Code Protection

Do not touch these areas during cleanup unless specifically planned:

```text
apps/marketflow_studio.py
marketflow/services/
marketflow/backtesting/
marketflow/analyzers/
marketflow/charts/
scripts/plot_annotated_features.py
current markdown checkpoint docs
```

## 11. Import Safety Checks

Before moving or removing anything in future cleanup:

- use `rg` to find references to candidate files/modules
- verify imports are not used by active Studio/service paths
- run `python -m py_compile` on active package files
- run focused pytest suites
- run full pytest after test-collection stabilization
- run a Streamlit smoke check if Studio imports may be affected

## 12. Proposed Future Cleanup Phases

### Phase C1 - Inventory report only

Create and commit this cleanup plan.

### Phase C2 - Test collection stabilization plan

Plan exact treatment for broken tests, optional dependency tests, missing fixtures, and stale interface tests.

### Phase C3 - Quarantine deprecated tests

Move or rename only clearly deprecated tests so full pytest collection stops failing for deprecated/prototype areas.

### Phase C4 - Optional dependency marker policy

Add skip/marker policy for broker, API, integration, and external-connectivity tests.

### Phase C5 - Archive deprecated_backup

Move or document deprecated backup code after import/reference checks.

### Phase C6 - Review trading_dashboard

Delete or archive the skeleton after confirmation and after non-empty files are classified.

### Phase C7 - Final cleanup audit

Run focused tests, full pytest, import checks, and Studio smoke check.

## 13. Recommended First Cleanup Implementation Task

Recommended next implementation task:

```text
Phase C2 - create a test collection stabilization plan for deprecated/broken tests.
```

If the team wants a direct implementation after that plan, the likely first code cleanup is:

```text
Phase C3 - quarantine deprecated_backup tests so full pytest no longer collects them.
```

No cleanup implementation is done in this checkpoint.

## 14. Risks

- deleting useful prototype logic
- breaking hidden imports
- masking real test failures
- losing historical context
- mixing cleanup with feature work
- removing broker/integration tests that may be useful later
- changing pytest behavior in a way that hides active regressions

## 15. Non-Goals

- no deletion in this checkpoint
- no file moves
- no pytest config changes
- no dependency changes
- no Studio changes
- no backtest feature work
- no refactoring active services

## 16. Final Status

Status: repository cleanup planning checkpoint only.
Next recommended task: stabilize test collection plan for deprecated/broken tests before moving or deleting files.
