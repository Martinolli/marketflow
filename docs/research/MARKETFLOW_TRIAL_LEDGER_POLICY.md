# MarketFlow Trial Ledger Policy

Status: proposed, requires human approval before use.

The trial ledger is append-oriented research governance. It records every
future applicability trial before performance is inspected and keeps failed,
unfavourable, inconclusive, and abandoned trials visible.

## Required Fields

Each trial must record:

- trial ID;
- protocol generation;
- code commit;
- data-manifest digest;
- candidate-builder version;
- `StrategyConfig` digest;
- profile;
- universe split;
- temporal split;
- horizon;
- baseline definitions;
- cost assumptions;
- random seeds;
- metrics requested;
- status;
- whether holdout was touched;
- reason for any follow-up trial.

## Immutability Rules

- No trial deletion.
- No retroactive parameter edits.
- Any changed horizon, threshold, split, universe, cost assumption, or metric
  set creates a new trial.
- Final holdout access is recorded irreversibly.
- Failed and unfavourable trials remain in the ledger.
- The ledger contains no credentials, no absolute local paths, and no provider
  account data.

## Performance Boundary

This policy defines what future trials must record. It does not record or
calculate performance values in this design phase.
