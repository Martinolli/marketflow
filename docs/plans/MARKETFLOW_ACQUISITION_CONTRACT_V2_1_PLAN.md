# MarketFlow Acquisition Contract v2.1 Plan

## Status

Plan status: COMPLETE.

Branch: `feature/swing-acquisition-contract-v2-1`.

Starting commit: `23b690f35d5e6bc8f4d439a6ded4c956f7f37005`.

## Mission

Implement a narrow offline corrective contract release that adds the missing
source 15-minute aggregate timestamp semantic required by the future frozen
calendar and deterministic RTH bar engine.

## Scope

Create Contract v2.1 as a separate source-controlled contract bound to the
accepted Contract v2 digest. Keep v1 and v2 semantic content unchanged.

Contract v2.1 must define:

- provider endpoint family `STOCKS_CUSTOM_BARS_V2`;
- provider timestamp field `t`;
- provider timestamp unit `UNIX_EPOCH_MILLISECONDS`;
- source timestamp semantic `START_OF_AGGREGATE_WINDOW`;
- 15-minute left-closed/right-open source intervals;
- normalized source identity fields `window_start_utc`, `window_end_utc`,
  `open`, `high`, `low`, `close`, `volume`;
- derived MarketFlow bars as close-stamped.

## Implementation Steps

1. Create `config/fixed_date_acquisition_contract_v2_1.toml`.
2. Create `marketflow/research/acquisition_contract_v2_1.py` with immutable
   policy models, strict loader, deterministic canonical JSON, SHA-256 digest,
   source interval helpers, and sanitized dry CLI receipt.
3. Add focused tests covering versioning, v1/v2 non-regression, endpoint
   binding, timestamp semantics, slot examples, DST conversion, strict loader,
   digest sensitivity, CLI behavior, source assurance, and prior integrity.
4. Add status, architecture, and research decision documentation.
5. Run focused tests, collect-only, full pytest, compileall with warnings as
   errors, `pip check`, and `git diff --check`.

## Verification Result

- Focused v2.1, v1/v2 regression, and source-assurance suite: 86 passed.
- Full collection: 683 tests collected.
- Full default suite: 683 passed.
- Compileall with warnings as errors: passed.
- `pip check`: passed.
- `git diff --check`: passed.

## Non-Goals

This task does not implement the frozen-calendar engine, RTH bar engine,
calendar generation, acquisition, normalization, registry approval, provider
execution, annotation, candidate generation, Monte Carlo, outcomes, broker
integration, runtime profile migration, or data generation.
