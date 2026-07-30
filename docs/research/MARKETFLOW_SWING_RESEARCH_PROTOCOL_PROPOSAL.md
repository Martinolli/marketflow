# MarketFlow Swing Research Protocol Proposal

Status: PROTOCOL_PROPOSED_WITH_BLOCKERS

This proposal is not frozen. Human approval is required before any future
performance campaign, holdout access, or claim of applicability.

## Research Question

Can MarketFlow's canonical point-in-time candidate builder support defensible
swing decision-support research for positions held for several days or weeks?

This protocol evaluates future applicability only after dataset identity,
coverage, horizons, splits, baselines, costs, metrics, and trial governance are
approved. It does not claim profitability or predictive usefulness.

## Profiles

### PROFILE A: SWING

- Decision timeframe: `4h`.
- Intended holding concept: several trading days.
- Primary proposed horizon: `10` bars.
- Secondary sensitivity horizons: `5` and `15` bars.
- Approximate interpretation: about 2.5 to 7.5 trading days depending on bar
  construction and market hours.
- Minimum proposed dataset floor: `360` rows.
- Proposed structural split-depth floor: `390` valid OHLCV rows, calculated as
  three 120-row chronological split segments plus two purge/embargo boundaries
  at the 15-bar maximum proposed horizon.

### PROFILE B: POSITION_SWING

- Decision timeframe: `1d`.
- Intended holding concept: several days to several weeks.
- Primary proposed horizon: `20` bars.
- Secondary sensitivity horizons: `10` and `40` bars.
- Approximate interpretation: about 2 to 8 trading weeks.
- Minimum proposed dataset floor: `500` rows.
- Proposed structural split-depth floor: `560` valid OHLCV rows, calculated as
  three 160-row chronological split segments plus two purge/embargo boundaries
  at the 40-bar maximum proposed horizon.

The horizon set is intentionally small and was not selected from outcome
performance. Any later horizon addition is a separate research trial.

## Architecture Finding

The accepted candidate builder is single-timeframe. The existence of `1d` or
`1w` local files does not mean higher-timeframe context is consumed by
production candidate construction.

Higher-timeframe context should remain a separately reviewed future extension.

## Universe Policy

Use deterministic ticker partitioning before performance inspection:

- sort canonical tickers alphabetically;
- assign index modulo 3:
  - 0: development universe;
  - 1: validation universe;
  - 2: locked holdout universe.

If the available universe is too small for meaningful ticker-level holdout,
use temporal holdout plus future external-universe validation. Do not fabricate
statistical independence.

User-interest tickers may be tracked as a declared use-case cohort, but they
must not be the sole evidence base.

## Temporal Split

Use a chronological split per ticker/timeframe:

- 60 percent development/calibration;
- 20 percent validation;
- 20 percent final locked holdout.

No random row shuffling is allowed. Candidate horizons are purged at split
boundaries, and an embargo of the maximum approved horizon is applied where
overlapping horizon dependence can contaminate adjacent splits.

No holdout result may feed a parameter revision without a new declared research
generation.

## Walk-Forward Protocol

Future campaign design must be chosen before performance is inspected.

Proposed options for human approval:

- expanding-window design with fixed validation windows;
- rolling-window design with fixed lookback and fixed validation windows.

Each option is a separate potential trial. The selected design must record:

- training/development window;
- validation window;
- step size;
- purge/embargo rule;
- minimum data per fold;
- minimum candidate-count rule;
- zero-candidate fold treatment;
- incomplete-evidence treatment;
- uncalibrated score-profile treatment;
- campaign run identity;
- deterministic configuration digest.

Zero-candidate folds are recorded, not deleted.

## Outcome Contract

Existing outcome evaluator supports:

- `TP_FIRST`;
- `SL_FIRST`;
- same-bar ambiguity with conservative, optimistic, open-proximity, or unknown
  tie-break policy;
- `NEITHER`;
- invalid inputs;
- horizon diagnostics;
- hit timestamp and row index;
- planned RR;
- mark-to-market R for neither outcomes.

Gaps before economic claims:

- no bid/ask spread model;
- no commission model;
- no executable open/close fill model;
- gap-through-stop and gap-through-target semantics are limited by OHLC bars;
- MFE/MAE fields are not explicit in the accepted outcome schema.

## Baselines

Freeze baselines before results:

- time-matched unconditional long baseline;
- matched random-entry baseline using same ticker and horizon with fixed seeds;
- simple declared trend baseline only if the existing deterministic trend
  contract is used.

No benchmark may be selected after seeing MarketFlow performance.

## Costs

Current local data appears to be OHLCV bars. It does not prove bid/ask spreads,
commissions, executable slippage, or market-open fill quality.

Therefore:

- gross price-path research may be run as structural research;
- fixed-cost sensitivity requires human-approved assumptions;
- spread/slippage sensitivity requires human-approved assumptions;
- no net profitability claim is allowed until cost assumptions are approved.

## Metrics

Candidate-generation metrics may include:

- total decisions evaluated;
- total candidate cores;
- complete-evidence candidates;
- rank-eligible candidates;
- ineligible reason counts;
- evidence-profile coverage;
- candidates by predeclared score band;
- candidates by ticker and fold.

Future outcome metrics may include:

- outcome counts;
- expectancy in R;
- median R;
- loss-tail quantiles;
- MFE and MAE distributions after schema support exists;
- target/stop hit timing;
- performance by predeclared score band;
- consistency across folds and tickers.

Statistical controls should include dependence-aware resampling, confidence
intervals, multiple-testing trial count, and PBO or a documented applicability
assessment. Deflated Sharpe Ratio is only appropriate if a valid return series
and repeated-trial context exist.

No isolated headline win rate is sufficient evidence.

## Acceptance Criteria

These require human approval before execution:

- minimum dataset quality: HUMAN_APPROVAL_REQUIRED;
- minimum fold coverage: HUMAN_APPROVAL_REQUIRED;
- minimum candidate count: HUMAN_APPROVAL_REQUIRED;
- maximum concentration in one ticker/fold: HUMAN_APPROVAL_REQUIRED;
- score-band ordering expectation: HUMAN_APPROVAL_REQUIRED;
- baseline comparison rules: HUMAN_APPROVAL_REQUIRED;
- economic significance rules: HUMAN_APPROVAL_REQUIRED.

Statistically inconclusive or economically insignificant results must be
reported as inconclusive or insufficient, not reframed as accepted.

## Final Statements

- No performance result was inspected.
- No horizon or profile was selected from returns.
- Predictive usefulness is not accepted.
- Profitability is not accepted.
- Protocol requires human approval before campaign execution.
