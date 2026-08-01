# MarketFlow Massive One-Month Smoke Runner Plan

## Authority Boundary

This plan authorizes an operator-controlled runner for a future one-month
Massive.com provider smoke test. Acceptance of the runner implementation is
offline only. This task does not authorize a real provider request, actual
API-key inspection, data acquisition, canonical dataset creation, calendar
freeze, registry action, Strategy run, performance analysis, broker activity,
execution capability, or normal runtime migration.

## Fixed Smoke Target

- Provider: `MASSIVE.COM`
- Classification: `NONCANONICAL_PROVIDER_SMOKE`
- Endpoint: `STOCKS_CUSTOM_BARS_V2`
- Ticker: `AAPL`
- Month: `2025-01`
- Effective start: `2025-01-01`
- Effective end: `2025-01-31`
- Multiplier: `15`
- Timespan: `minute`
- Adjusted: `true`
- Sort: `asc`
- Limit: `50000`

No caller override is accepted for ticker, month, date, provider, host, limit,
or semantics.

## Implementation Plan

1. Add an immutable smoke specification model and deterministic canonical JSON
   digest in `marketflow/historical_data/massive_smoke.py`.
2. Add an offline plan command that validates the smoke specification and
   Contracts, prints sanitized evidence, requests no credential, opens no
   socket, and writes no runtime artifact.
3. Add an interactive live command boundary requiring a digest-bound typed
   confirmation phrase before a hidden `getpass.getpass` credential prompt.
4. Reject noninteractive live execution and do not accept credentials through
   CLI arguments, environment variables, config files, visible input, or URLs.
5. Reuse the accepted `MassiveRestTransport` and monthly executor through
   dependency injection, keeping executor ownership of retry, pagination,
   completeness, and normalization.
6. Use an ignored source-defined smoke root,
   `.marketflow/provider_smoke/runs/`, with opaque run IDs and no ticker or
   month in directory names.
7. Persist only noncanonical smoke artifacts and a sanitized smoke receipt for
   live execution. Tests use temporary roots and mock HTTP only.
8. Add `--massive-smoke-plan`, `--massive-smoke-run`, and
   `--massive-smoke-self-check` to the historical-data CLI without semantic
   override flags.
9. Add focused offline tests covering fixed spec/digest, plan, authorization,
   credential boundary, interactivity, execution outcomes, artifacts, receipt
   sanitization, CLI behavior, source assurance, and prior-integrity
   boundaries.

## Non-Goals

- No real smoke execution in this task.
- No actual API-key read.
- No provider account or billing query.
- No provider SDK use.
- No calendar or bar derivation.
- No Strategy, Wyckoff annotation, Monte Carlo, outcome, optimization, broker,
  execution, registry, report, or normal runtime path.
