# MarketFlow Canonical Dataset Registry

Status: DESIGN ACCEPTED FOR TOOLING, NOT ACTIVATED

## Purpose

The canonical dataset registry is a strict source-controlled approval contract
for future normal-mode dataset selection. It records human decisions after
duplicate/history review. It does not move, merge, rewrite, delete, or
reannotate source files.

Normal orchestrator integration is deferred until the registry contains
approved human decisions and digest validation is accepted in a later phase.

## Registry Record

Each record contains exactly:

- `registry_schema_version`;
- `canonical_ticker`;
- `canonical_timeframe`;
- `status`;
- `approved_safe_relative_source_reference`;
- `approved_file_sha256`;
- `approved_semantic_ohlcv_digest`;
- `provenance_status`;
- `adjustment_status`;
- `approval_evidence_category`;
- `decision_id`;
- `decision_timestamp`;
- `superseded_source_references`;
- `notes_category`.

Unknown fields fail. Missing fields fail.

## Statuses

Allowed statuses:

- `UNRESOLVED`;
- `APPROVED`;
- `SUSPENDED`;
- `CONFLICT_REVIEW_REQUIRED`;
- `REACQUISITION_REQUIRED`.

Only one `APPROVED` record may exist for a ticker/timeframe identity. An
approved record must point to one safe relative source reference whose current
file bytes match `approved_file_sha256` and whose normalized OHLCV content
matches `approved_semantic_ohlcv_digest`.

## Path And Digest Rules

Registry source references must be relative POSIX-style paths. Absolute paths,
drive-qualified paths, traversal, backslashes, colon-containing references,
missing files, directories, file-byte digest mismatches, and semantic OHLCV
digest mismatches fail.

The registry never approves approximate matches. Filename similarity, newest
timestamp, largest file, longest history, row count, modification time, and
first glob match are not selection rules.

## Provenance And Adjustment

Explicit provenance and corporate-action adjustment status are required before
normal-mode readiness can be accepted. Unknown adjustment metadata remains
`CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN`; the tooling must not infer split
or adjustment state from price movement.

## Non-Performance Boundary

The registry contains no candidate score, outcome, return, R multiple, win
rate, expectancy, Sharpe/Sortino, drawdown, MFE/MAE, account, broker, or
profitability field.

Approval rationale must be data-governance evidence, not observed trading or
research performance.
