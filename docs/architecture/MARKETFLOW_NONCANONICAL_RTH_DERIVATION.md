# MarketFlow Noncanonical RTH Derivation

## Boundary

The live-month RTH diagnostic is an offline, evidence-bound derivation over an
already accepted Massive.com smoke run. It is not an acquisition path, calendar
freeze, canonical dataset promotion, strategy path, or performance evaluation.

The provider business identity is Massive.com. Legacy Polygon names may remain
only where they accurately identify existing adapter or package code.

## Source Evidence

The diagnostic consumes the fixed smoke source identified by:

- run ID: `smoke-c3388f68530c4131a090a895953e3d89`;
- receipt hash:
  `70b48e1c859d01cae7c0555f934fdaf3807863bbb1addffdc05b6f1c3197369f`;
- provider identity: `MASSIVE.COM`;
- ticker: `AAPL`;
- month: `2025-01`;
- normalized rows: `1277`;
- first source window: `2025-01-02T09:00:00Z`;
- last source window: `2025-02-01T00:45:00Z`.

The diagnostic validates the normalized OHLCV and aggregate-audit artifacts by
artifact ID, semantic digest, payload hash, payload size, run ID, row count, and
timestamp equality. The audit artifact proves one audit row per OHLCV row, but
audit fields are not used analytically.

Raw-page ancestry is checked only through artifact manifests and payload
existence plus payload byte size. Raw provider payload bytes are not read by the
diagnostic.

The month completeness payload's ordered `accepted_pages` entries are
reconciled to the exact declared raw-page input manifests. Accepted-page raw
artifact IDs must equal the corresponding `RAW_PROVIDER_PAGE` manifest
`artifact_id`, and accepted-page raw SHA-256 values must equal the
corresponding manifest `payload_sha256`. The diagnostic uses only declared
input refs and artifact IDs; directory-neighbor raw pages, filename order,
modification time, first, latest, or other fallback discovery cannot substitute
for a declared raw page.

The source-smoke evidence root is repository-derived from the source module
structure and resolves beneath `.marketflow/provider_smoke/runs/` in the
repository. It does not depend on process current working directory, CLI
options, environment variables, configuration, latest-folder discovery, or a
shadow `.marketflow` tree.

## Calendar Identity

The diagnostic uses an operator-declared assumption for XNAS only:

- requested primary listing MIC: `XNAS`;
- requested calendar token: `XNAS`;
- identity evidence classification:
  `OPERATOR_DECLARED_DIAGNOSTIC_IDENTITY`;
- calendar authority: `NOT_OPERATOR_FROZEN`.

The accepted frozen-calendar module resolves the package calendar and alias
relationship. For the current dependency set this resolves to `XNYS` with
`XNAS_USES_XNYS_SCHEDULE`, while preserving requested MIC/token separately in
the receipt.

No official-exchange evidence is introduced. No calendar freeze eligibility is
granted.

## Session View

The diagnostic builds a January 2025 session view from the generated calendar.
The session view keeps:

- normal full sessions;
- early-close sessions;
- closed or absent sessions;
- UTC open and close timestamps;
- parent calendar candidate digest;
- month-view semantic digest.

The view does not infer exchange closures from missing provider bars. Missing
or extra source rows are treated as data/session findings against the calendar
candidate.

## RTH Derivation

All RTH validation and aggregation is delegated to
`marketflow.historical_data.rth_bar_engine`.

The diagnostic imports source rows as `SourceBar` objects using exact Decimal
strings and UTC start-of-window timestamps. It rejects unsorted or duplicate
source rows before derivation.

For full ordinary sessions:

- exactly 26 15-minute RTH source slots are required;
- extended-hours rows are excluded and counted;
- missing first, middle, or final slots block the affected session;
- duplicate slots block the affected session;
- off-schedule RTH slots block the affected session.

Early-close sessions are excluded entirely. SWING produces two 195-minute
half-session bars per complete ordinary session. POSITION_SWING produces one
full-session RTH bar per complete ordinary session.

Receipts report both expected and validated RTH source-row counts. Expected RTH
rows are full ordinary sessions multiplied by 26 required source slots.
Validated RTH rows are unique exact expected slots matched during
session/slot validation; extended-hours, duplicate, and extra RTH rows cannot
inflate this count. The January 2025 diagnostic result is `520` expected and
`520` validated with `RTH_SOURCE_ROWS_RECONCILED`.

## Runtime Artifacts

The confirmation-gated local run writes sanitized receipts only under:

`.marketflow/rth_derivation_smoke/runs/`

The output root is derived from the same validated repository root as the
source-smoke evidence root. Run IDs are opaque and must not include ticker or
month. Runtime evidence under `.marketflow/` is ignored and is not a source
artifact for commit.

## Sanitization

Receipts contain digests, counts, statuses, and identity metadata. They do not
contain OHLCV values, raw provider bodies, API keys, authorization headers, raw
URLs, request IDs, absolute paths, strategy outputs, outcomes, or performance
metrics.
