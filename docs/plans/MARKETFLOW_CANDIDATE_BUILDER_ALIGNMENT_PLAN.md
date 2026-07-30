# MarketFlow Candidate Builder Alignment Plan

## Mission

Unify current Strategy Ranking, backtest candidate generation, and
walk-forward candidate generation behind one canonical point-in-time
candidate-building contract.

MarketFlow remains research and decision-support software, not execution
software.

## Observed Duplication

Current candidate construction is split across several production paths:

- `marketflow.marketflow_strategy.rank_long_candidates` loads a validated
  Strategy source CSV, uses the latest row as the decision row, computes
  Wyckoff context, event recency, True Range volatility, entry, stop,
  structural target, RR, evidence components, composite score, and rank
  eligibility.
- `marketflow.services.backtest_candidate_service` normalizes selected Strategy
  candidate dictionaries, locates or enriches signal rows, re-resolves event
  diagnostics from source context, validates levels, and serializes snapshot
  fields.
- `marketflow.services.backtest_service` and
  `marketflow.backtesting.outcome_engine` convert dict/dataclass snapshots and
  evaluate outcomes from future rows.
- `marketflow.services.walk_forward_validation_service` slices a historical row
  range, independently resolves target/RR/event diagnostics from the decision
  prefix, copies score diagnostics from row fields, and attaches future-window
  metadata for later outcome evaluation.
- `marketflow.services.strategy_service`, artifact services, Studio, and report
  surfaces flatten or display candidate dictionaries and snapshots.

The architectural risk is not only field mismatch in one fixture. The risk is
that live, backtest, and walk-forward paths can independently decide candidate
semantics.

## Current Live Path

Live/current ranking:

- validates ticker/timeframe source identity with Strategy source resolution;
- reads the selected source frame;
- uses the full available frame and treats the final row as the decision row;
- reads explicit optional POP evidence from a Monte Carlo summary when present;
- reads explicit optional PnF score evidence from source columns when present;
- calculates all core candidate semantics in `rank_long_candidates`;
- sorts complete/rank-eligible candidates without recomputing core fields.

## Current Backtest Path

Backtest candidate generation:

- starts from a Strategy-style candidate dict or legacy snapshot artifact;
- normalizes aliases and legacy score diagnostics;
- may enrich signal location and event diagnostics from the candidate source;
- validates entry/stop/target/risk-reward shape;
- serializes a snapshot consumed by outcome evaluation;
- outcome evaluation uses future rows only after candidate snapshot creation.

The pre-refactor gap is that backtest can reconstruct or preserve candidate
fields without invoking the same candidate builder used by current ranking.

## Current Walk-Forward Path

Walk-forward candidate generation:

- receives an explicit CSV path and validates filename identity;
- selects a decision row and constructs a prefix through that row for some
  calculations;
- independently resolves event, target, RR, and wrapper metadata;
- copies score/evidence diagnostics from row fields when present;
- attaches future-window metadata and evaluates outcomes separately.

The pre-refactor gap is that walk-forward can independently calculate candidate
semantics instead of delegating to the current ranking builder.

## Field Parity Contract

Given identical validated source identity, data prefix, `StrategyConfig`, and
explicit evidence inputs, wrappers must produce identical candidate-core values
for:

- ticker, timeframe, source status, source reference;
- decision timestamp and row position;
- Wyckoff phase, event, event status, provenance, age, policy, and scoring
  eligibility;
- volatility status, value, provenance, and window;
- entry, stop, target, target status/provenance/kind, RR, and RR status;
- component evidence statuses, scores, weights, provenance, reasons, active
  profile, evidence coverage, score status, composite score, and rank
  eligibility.

Wrapper metadata excluded from equality:

- batch date;
- report paths;
- snapshot/run/case/campaign IDs;
- artifact filenames;
- future-window and outcome fields;
- UI formatting metadata.

No strategy semantic may be excluded solely to make parity pass.

## Point-In-Time Prefix Contract

The canonical builder receives a chronological data prefix ending at the
decision row. It does not receive future rows.

Rules:

- empty prefix fails closed;
- duplicate or non-monotonic timestamp chronology fails where accepted
  volatility/event contracts require it;
- the decision row is the final row in the supplied prefix;
- source identity is already validated by the wrapper;
- ticker/timeframe come from validated identity;
- optional evidence inputs are explicit;
- no provider, broker, network, or dependency behavior occurs.

Current ranking may pass all currently available rows because the final row is
the current decision row. Historical wrappers must slice rows `<= T` before
calling the builder.

## Configuration Contract

Wrappers must pass one explicit `StrategyConfig` into the canonical builder.
Candidate-affecting fields include:

- `atr_len`;
- `max_sl_atr`;
- `min_rr`;
- `max_event_age_bars`;
- `use_mc`;
- `use_pnf`;
- `min_pop`;
- `min_pop_backup`;
- component `weights`;
- existing score and recommendation thresholds when part of current candidate
  output.

No wrapper may silently change or infer configuration from artifacts,
environment values, provider state, or missing fields.

## Evidence Input Contract

Optional evidence is passed explicitly:

- POP/Monte Carlo evidence value and provenance when available;
- PnF evidence value and provenance when available from point-in-time source
  rows;
- enable/disable state remains controlled by `StrategyConfig`.

Rules:

- no missing POP or PnF becomes neutral;
- no failed component is silently disabled;
- genuine neutral `0.5` remains valid only with fixed available evidence;
- future rows cannot supply evidence for a historical decision;
- the builder opens no provider connection.

## Candidate Core Model

The canonical candidate core may remain a strict dict projection or become an
immutable dataclass. It must carry every current semantic field needed by
Strategy, backtest, walk-forward, Studio, and reporting:

- identity and decision-row metadata;
- source status and safe source reference;
- phase/event diagnostics;
- volatility/geometry/target/RR diagnostics;
- evidence components and score diagnostics;
- rank eligibility and fixed reasons.

Future outcome data is excluded from the candidate core.

## Wrapper Metadata

Wrappers may attach metadata after core construction:

- Strategy batch/report metadata;
- backtest validation and snapshot metadata;
- walk-forward case/run/future-window metadata;
- artifact filenames;
- outcome model fields.

Wrappers must not recompute core semantics while attaching metadata.

## Future Outcome Separation

Outcome evaluation may use future rows for TP/SL ordering, horizon, bars to hit,
mark-to-market, and realized diagnostics. Outcome evaluation must not mutate
entry, stop, target, RR, phase, event, volatility, score, or rank eligibility.

## Failure Parity

Equivalent invalid prefixes/configuration/evidence should produce equivalent
fixed failure statuses rather than wrapper-specific raw exceptions, fabricated
defaults, silent skips, or low-score candidates.

Wrapper-level source-identity failures may occur before the builder, but must
remain fail-closed and non-actionable.

## Test Plan

Add deterministic synthetic tests for:

- baseline pre-refactor parity audit evidence;
- complete candidate core parity;
- RR below minimum;
- missing target;
- invalid volatility;
- old event without recency policy;
- current event;
- missing active Monte Carlo evidence;
- valid neutral Monte Carlo `0.5`;
- missing active PnF evidence;
- explicitly disabled PnF profile;
- invalid chronology;
- source mismatch at wrapper boundary;
- future-row, future-event, future-volatility, future-target, and
  future-evidence invariance;
- outcome separation;
- rank sorting and batch independence;
- legacy artifact fail-closed behavior;
- Studio/report source-assurance;
- prior source identity, target/RR, True Range, event recency, and evidence
  availability non-regression.

## Exclusions

Do not change source identity, entry, stop, True Range, volatility aggregation,
structural target, target provenance, RR, minimum-RR gate, phase/event values,
event recency, Monte Carlo formulas, PnF calculations, trend formula, component
weights, composite math, thresholds, outcomes, future horizons, providers,
brokers, or execution behavior.

Do not tune the strategy.

## Stop Conditions

Stop blocked if branch/base/cleanliness checks fail, dependency or network
behavior changes, wrappers still independently construct candidate semantics,
identical prefix/config/evidence yields divergent cores, future rows can change
candidate core, legacy artifacts bypass the current core contract, formulas or
thresholds change, previous integrity milestones regress, tests mutate tracked
files, full tests fail, compileall fails, or a critical/high reviewer finding
remains unresolved.
