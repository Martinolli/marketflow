# MarketFlow Live-Month RTH Derivation Diagnostic Plan

## Purpose

Implement a deterministic offline diagnostic that derives noncanonical RTH SWING
and POSITION_SWING bars from the already accepted Massive.com live-month smoke
artifact for AAPL January 2025.

This plan does not authorize provider acquisition, credential inspection,
provider-account inspection, registry promotion, canonical calendar freeze,
strategy execution, or performance evaluation.

## Fixed Source Evidence

- Provider business identity: Massive.com.
- Legacy adapter/package naming may remain Polygon where it describes installed
  code.
- Source run: `smoke-c3388f68530c4131a090a895953e3d89`.
- Source receipt SHA-256:
  `70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f`.
- Source ticker: `AAPL`.
- Source month: `2025-01`.
- Normalized row count: `1277`.
- First normalized source window: `2025-01-02T09:00:00Z`.
- Last normalized source window: `2025-02-01T00:45:00Z`.
- Normalized OHLCV artifact:
  `month-art-0005-month-normalized-15m-ohlcv`.
- Normalized OHLCV semantic digest:
  `24e83b9eea95c9e7ba662123f6edac220de9fb64e9cbb4225ee76d60bcb1230e`.
- Normalized audit artifact:
  `month-art-0006-month-normalized-aggregate-audit-fields`.
- Normalized audit semantic digest:
  `3099ffab37579b20cb3dfdcb5c1e2741ce00cbf7f05fb8a4e135e9dcb421f9cd`.

## Diagnostic Contract

- Schema: `marketflow.live_month_rth_diagnostic.v1`.
- Classification: `NONCANONICAL_LIVE_MONTH_RTH_DERIVATION`.
- Requested primary listing MIC: `XNAS`.
- Requested calendar token: `XNAS`.
- Identity evidence classification:
  `OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY`.
- Calendar authority: `NOT_OPERATOR_FROZEN`.
- Calendar freeze eligibility: `false`.
- Canonical eligibility: `false`.
- Registry eligibility: `false`.
- Strategy enabled: `false`.
- Performance enabled: `false`.

## Implementation Steps

1. Add `marketflow/historical_data/live_month_rth_diagnostic.py`.
2. Validate the fixed smoke receipt hash and sanitized smoke metadata from disk.
3. Validate normalized OHLCV and audit artifact IDs, semantic digests,
   payload hashes, payload sizes, row counts, timestamp equality, and common
   completeness parentage.
4. Validate raw-page ancestry only through manifests plus payload existence and
   payload byte size. Do not read raw provider payload bodies.
5. Import normalized OHLCV rows into accepted `rth_bar_engine.SourceBar`
   instances using exact Decimal strings and UTC source-window starts.
6. Generate a noncanonical XNAS diagnostic calendar candidate through the
   accepted frozen-calendar module. Keep requested MIC/token distinct from the
   resolved package calendar.
7. Build a January 2025 session view that retains full, early-close, and closed
   sessions, with a digest bound to the parent calendar digest.
8. Reuse accepted `rth_bar_engine` validation and derivation functions for
   SWING and POSITION_SWING. Do not duplicate bar-construction formulas.
9. Emit sanitized receipts with digests and counts only. Do not emit OHLCV
   values, raw provider bodies, keys, authorization headers, raw URLs, request
   IDs, absolute paths, strategy fields, outcome metrics, or performance
   measures.
10. Add CLI plan, synthetic self-check, and confirmation-gated local run
    commands.

## CLI Commands

```powershell
env\Scripts\python.exe -m marketflow.historical_data --live-month-rth-derivation-plan
env\Scripts\python.exe -m marketflow.historical_data --live-month-rth-derivation-self-check
env\Scripts\python.exe -m marketflow.historical_data --live-month-rth-derivation-run
```

The run command writes only to the ignored runtime root
`.marketflow/rth_derivation_smoke/runs/` after the operator types the
diagnostic confirmation phrase printed by the plan command.

## Acceptance Gates

- Default tests must remain deterministic and offline.
- The source-assurance tests must prove there is no provider client import,
  network import, credential access, raw provider payload access, registry
  promotion, strategy import, outcome engine import, performance evaluation, or
  runtime migration.
- Focused diagnostic tests must cover fixed spec, smoke hash validation,
  artifact digest validation, exact Decimal source import, calendar identity
  separation, complete/partial session handling, RTH slot completeness,
  extended-hours exclusion, profile independence, CLI plan, CLI self-check, and
  receipt sanitization.
- Full pytest, collect-only, compileall, pip check, and diff whitespace checks
  must pass before acceptance.
