# MarketFlow Live-Month RTH Derivation Status

## Status

Implementation status: `LIVE_MONTH_RTH_DERIVATION_ACCEPTED_FOR_LOCAL_COMMIT`.

The noncanonical live-month RTH derivation diagnostic has been implemented
locally. It validates the accepted Massive.com AAPL January 2025 smoke evidence
from disk, builds a noncanonical XNAS diagnostic calendar candidate, derives
SWING and POSITION_SWING RTH bars through the accepted bar engine, and emits
sanitized receipts only.

The public local-run output boundary has now been corrected so
`run_local_diagnostic(confirmation: str)` no longer accepts caller-supplied
runtime roots or run IDs.

The live-run CLI authorization display has also been corrected. The command now
prints the complete sanitized plan, noncanonical warning, full diagnostic
digest, digest prefix, and exact required confirmation phrase before prompting
for interactive input. The displayed phrase and validated phrase come from the
same diagnostic confirmation helper.

No provider acquisition was enabled. No API key, provider account, billing
record, provider portal, credential value, or raw provider body was inspected.
No tag has been created for this implementation pass.

Final acceptance on 2026-08-02 validated the corrected confirmation-gated
local derivation receipt by hash and sanitized metadata. Earlier acceptance
attempts found bounded source-root, run-ID, receipt-observability, and raw-page
ancestry issues. Those issues have all been corrected, and the
confirmation-gated local derivation was repeated after the final raw-page
ancestry correction.

The source-smoke evidence root derives from the same validated repository root
as the diagnostic output root. Public source validation, public diagnostic
execution, and confirmation-gated local runs no longer depend on the process
current working directory.

The run-ID generator uses bounded rejection sampling, retains forbidden-
fragment validation, and fails closed with
`DIAGNOSTIC_RUN_ID_GENERATION_EXHAUSTED` after `32` rejected candidates.

The sanitized diagnostic receipt now also includes direct RTH source-row
reconciliation fields:

- `expected_rth_source_row_count`;
- `validated_rth_source_row_count`;
- `rth_source_row_reconciliation_status`.

The accepted January 2025 evidence reports `520`, `520`, and
`RTH_SOURCE_ROWS_RECONCILED`. The count is derived from session/slot
validation, not solely from subtracting extended-hours rows.

Final acceptance later found one medium source-evidence ancestry blocker: the
diagnostic did not compare completeness `accepted_pages[*].raw_page_artifact_id`
and `accepted_pages[*].raw_page_sha256` to the exact declared
`RAW_PROVIDER_PAGE` manifests. That blocker is now corrected with ordered
declared-input reconciliation and fixed sanitized failure categories. The
confirmation-gated local derivation was repeated after that correction, and
the corrected receipt validated by hash.

Final bounded Reviewer A then found a new medium source-boundary blocker:
source evidence payload references were lexically checked, then used without
rejecting symlink payload files or proving the resolved payload file remained
under the source root. That blocker is now corrected with one authoritative
source-evidence file helper, strict physical containment, symlink/junction/
reparse rejection, regular-file validation, and pre/post read identity checks.
The confirmation-gated local derivation was repeated after that correction.
Final acceptance validated the saved corrected receipt by hash and reports
`PASS`.

## Starting Evidence

- Branch: `feature/swing-live-month-rth-derivation-diagnostic`.
- Starting commit:
  `94d299c5608125b31266dd2d4fce5b9edc6664bb`.
- Baseline tag: `v0.1.0-alpha.22-live-monthly-smoke-noncanonical`.
- Python interpreter for acceptance commands: `env\Scripts\python.exe`.
- `exchange_calendars`: `4.13.2`.
- `pip check`: pass.
- Baseline collect-only: `874 tests collected`.
- Baseline full pytest: `874 passed`.

## Fixed Source Evidence

- Source run: `smoke-c3388f68530c4131a090a895953e3d89`.
- Source receipt SHA-256:
  `70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f`.
- Provider identity: `MASSIVE.COM`.
- Ticker/month: `AAPL` / `2025-01`.
- Normalized row count: `1277`.
- First/last source windows:
  `2025-01-02T09:00:00Z` / `2025-02-01T00:45:00Z`.
- Normalized OHLCV artifact:
  `month-art-0005-month-normalized-15m-ohlcv`.
- Normalized OHLCV semantic digest:
  `24e83b9eea95c9e7ba662123f6edac220de9fb64e9cbb4225ee76d60bcb1230e`.
- Normalized audit artifact:
  `month-art-0006-month-normalized-aggregate-audit-fields`.
- Normalized audit semantic digest:
  `3099ffab37579b20cb3dfdcb5c1e2741ce00cbf7f05fb8a4e135e9dcb421f9cd`.

## Diagnostic Result

Offline diagnostic read-only run result:

- Diagnostic status: `LIVE_MONTH_RTH_DERIVATION_COMPLETE`.
- Source evidence status: `LIVE_MONTH_SOURCE_EVIDENCE_VALID`.
- Diagnostic specification digest:
  `d5bcaedb84148d9c69a18852a4d6e2b8984d16d6e8d25f3901426c10f3574257`.
- Requested MIC/token: `XNAS` / `XNAS`.
- Resolved calendar: `XNYS`.
- Calendar alias: `XNAS_USES_XNYS_SCHEDULE`.
- Calendar status: `CALENDAR_GENERATED_PENDING_OFFICIAL_EVIDENCE`.
- Calendar authority: `NOT_OPERATOR_FROZEN`.
- Parent calendar candidate digest:
  `6cf9f2b15b398b1dd9877ee12a769d2f92f8555a84abf4f61bd528d296d40734`.
- January session-view digest:
  `2ef9b599399ddb5b00d689a1267f4e702523ac1513cbfbddabe7e9254e995325`.
- January full ordinary sessions: `20`.
- Early-close exclusions: `0`.
- Closed or absent sessions: `11`.
- Extended-hours rows excluded: `757`.
- Incomplete ordinary sessions: `0`.
- SWING derivation status: `DERIVATION_COMPLETE`.
- SWING produced bars: `40`.
- POSITION_SWING derivation status: `DERIVATION_COMPLETE`.
- POSITION_SWING produced bars: `20`.

## Current Local Checks

- `env\Scripts\python.exe -m pip check`: pass.
- `env\Scripts\python.exe -m pytest -q tests\test_live_month_rth_diagnostic.py`:
  `38 passed`.
- `env\Scripts\python.exe -m marketflow.historical_data --live-month-rth-derivation-plan`:
  pass.
- `env\Scripts\python.exe -m marketflow.historical_data --live-month-rth-derivation-self-check`:
  pass.

Additional acceptance checks:

- `env\Scripts\python.exe -m pytest -q tests\test_live_month_rth_diagnostic.py tests\test_historical_data_engine.py tests\test_historical_data_artifacts.py tests\test_fake_transport_monthly_acquisition.py tests\test_massive_one_month_smoke.py tests\test_massive_date_diagnostic.py tests\test_acquisition_contract_v2.py tests\test_acquisition_contract_v2_1.py tests\test_fixed_date_acquisition_contract.py tests\test_source_assurance.py tests\test_artifact_lineage_v1.py tests\test_packaging_integrity.py tests\test_network_guard.py`:
  `270 passed`.
- Confirmation-gated local run:
  `LIVE_MONTH_RTH_DERIVATION_COMPLETE`.
- Confirmation-gated run receipt SHA-256:
  `d2e97da8dda76d835e04a4b24eb683c8ba262bcde7491bb6f1746d4f605fad97`.
- `env\Scripts\python.exe -m pytest --collect-only -q`:
  `912 tests collected`.
- Test-count change before full rerun: `+38` from the original 874-test
  baseline, `+8` from the prior 904-test accepted baseline, and `+3` from the
  runtime-boundary-corrected 909-test baseline, from
  `tests/test_live_month_rth_diagnostic.py`.
- `env\Scripts\python.exe -m pytest -q`: `912 passed`.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: pass.
- `git diff --check`: pass with LF-to-CRLF working-copy normalization warnings.
- Source-root correction focused test:
  `40 passed`.
- Source-root correction related historical/source-assurance regression:
  `275 passed`.
- Source-root correction collect-only:
  `914 tests collected`.
- Source-root correction full default suite:
  `914 passed`.
- Run-ID determinism correction focused test:
  `46 passed`.
- Run-ID determinism correction related historical/source-assurance
  regression:
  `281 passed`.
- Run-ID determinism correction collect-only:
  `920 tests collected`.
- Run-ID determinism correction full default suite:
  `920 passed`.
- Receipt observability correction focused test:
  `52 passed`.
- Receipt observability correction related historical/source-assurance
  regression:
  `287 passed`.
- Receipt observability correction collect-only:
  `926 tests collected`.
- Receipt observability correction full default suite:
  `926 passed`.
- Raw-page ancestry correction reproduction:
  `2 failed: DID NOT RAISE` before the production fix.
- Raw-page ancestry correction focused diagnostic tests:
  `65 passed`.
- Raw-page ancestry correction related historical/source-assurance regression:
  `300 passed`.
- Raw-page ancestry correction collect-only:
  `939 tests collected`.
- Raw-page ancestry correction full default suite:
  `939 passed`.
- Payload-path containment correction focused diagnostic tests:
  `84 passed`.
- Payload-path containment correction related historical/source-assurance
  regression:
  `319 passed`.
- Payload-path containment correction collect-only:
  `958 tests collected`.
- Payload-path containment correction full default suite:
  `958 passed`.

Final accepted corrected local derivation:

- Diagnostic run:
  `rthdiag-aa3b306b21f040a3832ff8bf20aaad6b`.
- Diagnostic receipt SHA-256:
  `a0c7c1216d769910362952c2de799dfadd2272d80a01499c12a17ff453c28b87`.
- Status: `LIVE_MONTH_RTH_DERIVATION_COMPLETE`.
- Expected RTH source rows: `520`.
- Validated RTH source rows: `520`.
- RTH source-row reconciliation:
  `RTH_SOURCE_ROWS_RECONCILED`.
- Final acceptance: `PASS`.

Two bounded read-only reviews were run. Their earlier high/medium findings
were remediated by removing public diagnostic spec/source overrides,
separating private synthetic fixture helpers, requiring fixed raw-page ancestry
count validation, converting malformed source evidence to sanitized blocked
receipts, and marking synthetic self-check provider execution disabled. A final
runtime-boundary review then found caller-controlled local-run `run_root` and
`run_id_factory` parameters; those have now been removed from the public
entrypoint and retained only behind a leading-private validated test seam.
The follow-up authorization-display review found that the live command did not
show the operator confirmation phrase before prompting; that display defect is
now corrected without changing diagnostic semantics.

## Guardrails

- `calendar_freeze_eligible`: `false`.
- `canonical_eligibility`: `false`.
- `registry_eligibility`: `false`.
- `strategy_enabled`: `false`.
- `performance_enabled`: `false`.
- `acquisition_enabled`: `false`.
- `runtime_migration_enabled`: `false`.

The output remains noncanonical diagnostic evidence only.
