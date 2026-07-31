# MarketFlow Dataset Decision Policy

Status: POLICY DRAFT FOR MANUAL DATA GOVERNANCE

## Objective

Dataset decisions must preserve evidence traceability and fail closed. Duplicate
files are classified deterministically, but no file becomes canonical until an
operator records an explicit decision.

## Decision Register

The local decision register is append-oriented and intended for ignored local
storage unless a sanitized version is deliberately reviewed for source control.

Each decision records exactly:

- `decision_id`;
- `identity`;
- `examined_source_digests`;
- `duplicate_classification`;
- `decision_status`;
- `selected_canonical_source`;
- `rationale_category`;
- `operator_approval_status`;
- `evidence_timestamp`;
- `code_commit`;
- `remediation_action_status`.

Pending decisions remain visible. Rejected sources are not silently deleted.
Changed decisions create new records; earlier records remain unchanged.

## Allowed Decision States

- `PENDING`;
- `APPROVED`;
- `REJECTED`.

## Duplicate Classifications

Decision evidence must use fixed classifications:

- `EXACT_BYTE_DUPLICATES`;
- `SEMANTICALLY_IDENTICAL`;
- `SAME_OHLCV_DIFFERENT_ANNOTATIONS`;
- `STRICT_SUPERSET_COMPATIBLE`;
- `STRICT_SUBSET_COMPATIBLE`;
- `OVERLAPPING_COMPATIBLE`;
- `OVERLAPPING_CONFLICTING`;
- `DISJOINT_HISTORY_SAME_IDENTITY`;
- `SCHEMA_DIVERGENT`;
- `TIMESTAMP_NORMALIZATION_CONFLICT`;
- `PROVENANCE_CONFLICT`;
- `IDENTITY_INVALID`;
- `UNCLASSIFIED_REVIEW_REQUIRED`.

## Recommendation States

The tooling may recommend a review category:

- `SAFE_REDUNDANCY_REVIEW`;
- `MANUAL_CANONICAL_SELECTION_REQUIRED`;
- `MANUAL_MERGE_REVIEW_REQUIRED`;
- `REANNOTATION_RECOMMENDED`;
- `SOURCE_REACQUISITION_RECOMMENDED`;
- `PROVENANCE_CONFIRMATION_REQUIRED`;
- `NO_SAFE_REMEDIATION_IDENTIFIED`.

It must not emit `APPROVED_CANONICAL_SOURCE` without an explicit human decision
record.

## Prohibited Rationale

No decision may use performance rationale, including profitability, win rate,
expectancy, Sharpe/Sortino, drawdown, R multiple, MFE/MAE, outcome labels,
candidate score, best ticker, best timeframe, best period, or optimization
results.

## Acquisition Policy

Additional history requirements are row-gated. Fixed acquisition cutoff dates
remain `HUMAN_APPROVAL_REQUIRED` until an operator approves them. The research
contract must not revert to mutable period strings such as `100d`, `365d`, or
`2y`.

## Reannotation Policy

If a longer OHLCV source is later approved, annotation compatibility must be
reviewed against the accepted current code. Stale or unknown annotations may
require deterministic reannotation in a separate phase. This policy does not
authorize reannotation now.
