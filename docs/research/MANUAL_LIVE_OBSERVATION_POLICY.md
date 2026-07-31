# Manual Live Observation Policy

Status: PASS

Historical live trades and operator observations are classified as:

`EXPLORATORY_MANUAL_LIVE_OBSERVATIONS`

They are operational notes only. They must not be used for parameter selection,
retrospective Strategy calibration, preferred ticker selection, horizon
selection, threshold tuning, evidence weighting, score validation, or
profitability claims.

Permitted use:

- annotate what the operator manually observed;
- identify workflow usability questions;
- propose future blinded protocol requirements;
- compare whether future artifacts contain the required identity fields.

Prohibited use:

- fitting StrategyConfig values;
- selecting SWING or POSITION_SWING horizons;
- choosing tickers because they looked best in historical live observations;
- backfilling candidate labels after outcomes are known;
- promoting Monte Carlo diagnostics into Strategy signal generation;
- citing profits, losses, win rate, expectancy, or trade values as evidence.

Any future research trial must use a separately approved no-peek protocol,
manifest digest, code commit, StrategyConfig digest, fixed universe/split,
approved horizon, explicit costs policy, and append-only trial ledger.
