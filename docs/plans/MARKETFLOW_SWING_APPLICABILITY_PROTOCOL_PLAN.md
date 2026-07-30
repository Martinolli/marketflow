# MarketFlow Swing Applicability Protocol Plan

## Mission

Design a no-peek scientific applicability protocol for MarketFlow swing
decision support after the canonical point-in-time candidate-builder alignment.

This phase determines whether local datasets and current research
infrastructure are sufficient to support a future campaign for positions held
for several days or weeks. It does not evaluate performance.

## Starting Controls

- Repository: `marketflow`
- Branch: `feature/swing-applicability-protocol`
- Starting commit: `3f93671d9d8abc0d7c48515680b37bc6b8980415`
- Interpreter: `env\Scripts\python.exe`
- Starting tree: clean
- Dependency check: `pip check` passed

## No-Peek Boundary

Allowed in this phase:

- dataset identity;
- row counts;
- timestamp ranges;
- chronology and interval quality;
- OHLCV validity;
- annotation/schema availability;
- timeframe availability;
- explicit provenance metadata;
- whether enough history exists for a proposed design.

Forbidden in this phase:

- outcome evaluator execution;
- TP/SL result proportions;
- win rate, expectancy, R multiples, Sharpe, Sortino, drawdown, or returns;
- candidate score versus outcome;
- best ticker, profile, horizon, parameter, or regime selection;
- provider/network checks;
- strategy tuning.

## Implementation Plan

1. Inventory existing accepted integrity docs, walk-forward plans/status,
   parameter-profile docs, calibration docs, candidate-builder code, outcome
   schema/code, and existing tests.
2. Add a deterministic offline research readiness module and CLI that
   inventories local canonical OHLCV/annotated datasets without invoking
   candidate generation or outcome evaluation.
3. Add source-controlled examples for a proposed protocol and trial ledger.
4. Add docs for protocol proposal, trial-ledger policy, and readiness status.
5. Add deterministic pytest coverage using synthetic data and temporary
   directories.
6. Run independent read-only reviews and address only concrete blocker
   findings.
7. Run required offline checks and leave the working tree uncommitted.

## Proposed Source Additions

- `marketflow/research/applicability_readiness.py`
- `config/swing_applicability_protocol.example.toml`
- `config/swing_trial_ledger.example.json`
- `docs/research/MARKETFLOW_SWING_RESEARCH_PROTOCOL_PROPOSAL.md`
- `docs/research/MARKETFLOW_TRIAL_LEDGER_POLICY.md`
- `docs/status/MARKETFLOW_SWING_APPLICABILITY_READINESS_STATUS.md`
- focused tests under `tests/`

## Dataset Inventory Contract

The manifest must contain safe relative paths only and include:

- ticker and timeframe identity;
- row count and valid OHLCV row count;
- timestamp range and timezone limitation;
- duplicate and non-monotonic timestamp counts;
- missing OHLCV and invalid high/low counts;
- median interval and irregular interval count;
- volume, Wyckoff, TR level, and confirmed-event marker availability;
- explicit provenance/version/adjustment status when available;
- deterministic status: `valid`, `limited`, or `ineligible`.

Duplicate or ambiguous ticker/timeframe identities fail closed.

## Profile Feasibility

Profile A, `SWING`:

- candidate decision timeframe: `4h`;
- intended holding concept: several trading days;
- higher-timeframe context: `1d` only as a future extension unless production
  candidate construction consumes it.

Profile B, `POSITION_SWING`:

- candidate decision timeframe: `1d`;
- intended holding concept: several days to several weeks;
- higher-timeframe context: `1w` only as a future extension unless production
  candidate construction consumes it.

The current canonical candidate builder is single-timeframe. This phase must
not add multi-timeframe features.

## Protocol Freeze Design

The proposed protocol is represented as deterministic JSON-serializable data
with a stable SHA-256 digest. It remains
`PROTOCOL_PROPOSED_WITH_BLOCKERS` until human approval. Any later change to
horizon, split, universe, threshold, cost assumption, metric set, or holdout
access creates a new declared research trial.

## Stop Conditions

Stop blocked if branch/commit/tree checks fail, dependency state changes,
network/provider code runs, outcome/performance is inspected, protocol choices
are tuned from outcomes, local absolute paths enter source-controlled output,
tests fail, previous integrity milestones regress, or a critical/high reviewer
finding remains unresolved.
