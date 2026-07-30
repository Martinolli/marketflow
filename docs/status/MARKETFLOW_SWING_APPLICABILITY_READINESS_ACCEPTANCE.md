# MarketFlow Swing Applicability Readiness Acceptance

## Decisions

- Implementation decision: PASS.
- Research protocol freeze decision: BLOCKED.
- Acceptance timestamp: 2026-07-30T19:05:22Z.
- Branch: `feature/swing-applicability-protocol`.
- Base commit: `3f93671d9d8abc0d7c48515680b37bc6b8980415`.
- Baseline tag at base: `v0.1.0-alpha.7-candidate-builder-alignment`.
- Commit intent: local commit only.
- Tag: not created.
- Push: not performed.

The readiness framework is accepted as deterministic offline no-peek tooling.
The applicability research protocol is not frozen. Predictive usefulness,
profitability, and outcome-campaign authorization are not accepted.

## Scope and Exclusions

Accepted scope:

- offline dataset manifest and readiness CLI;
- deterministic protocol model and digest;
- safe protocol and trial-ledger examples;
- focused readiness/source-assurance tests;
- research protocol, ledger policy, plan, status, and acceptance documents.

Excluded scope:

- strategy formula, threshold, score, target, stop, RR, and outcome changes;
- candidate generation and outcome evaluation;
- return, win-rate, expectancy, Sharpe, Sortino, drawdown, R-multiple, MFE, or
  MAE aggregation;
- optimization, best-profile selection, best-horizon selection, provider calls,
  broker integration, and execution capability.

No market-data source file was modified, deleted, renamed, merged, selected, or
rewritten.

## No-Peek Rule

The accepted readiness command may inspect only identities, schemas,
timestamps, row counts, chronology, missing or invalid OHLCV, interval
regularity, annotations, explicit provenance, and split feasibility. It must
not inspect future performance. Source review found no runtime import or call
path to candidate generation, outcome evaluation, walk-forward campaign
aggregation, performance metrics, parameter sweeps, or best-result selection.

## Dataset Inventory

Generated local manifest:

- ignored local path: `.marketflow/research/swing_applicability_manifest.json`;
- manifest digest: `3edff02356e1a571c0fd84c3a785f27b076a1077d763da6600682689ff3efecd`;
- manifest status: `ineligible`;
- canonical annotated CSV file count: 54;
- distinct canonical tickers: 6;
- unique ticker/timeframe identity count: 16;
- duplicate ticker/timeframe identity count: 12 identities with more than one
  source file;
- excess duplicate files above one source per identity: 38.

Timeframe file counts:

- `1d`: 15 files, 5 unique identities;
- `1h`: 22 files, 6 unique identities;
- `1w`: 3 files, 1 unique identity;
- `4h`: 14 files, 4 unique identities.

Dataset quality status:

- `valid`: 48 files;
- `limited`: 6 files;
- missing explicit volume column: 0 files;
- missing or invalid volume rows: 0.

The file counts are not independent-instrument counts. For example, 15 daily
files collapse to 5 unique daily ticker/timeframe identities.

## Blockers

Duplicate-identity blocker:

- duplicate detection uses exact canonical ticker/timeframe identity;
- duplicates are not resolved by modification time, largest file, longest
  history, canonical-looking suffix, alphabetical order, first glob match, or
  latest timestamp;
- duplicate resolution requires a separate reviewed data-remediation phase.

Row-depth and split-feasibility blocker:

- `SWING` uses the `4h` decision timeframe and remains `BLOCKED`;
- `POSITION_SWING` uses the `1d` decision timeframe and remains `BLOCKED`;
- both blockers are based on valid OHLCV rows, proposed split floors, proposed
  horizons, and purge/embargo rows, not observed performance.

`SWING` split-depth requirement:

- primary horizon: 10 bars;
- secondary horizons: 5 and 15 bars;
- split floor: three chronological split segments with 120 rows each;
- purge/embargo budget: 30 rows;
- required valid OHLCV rows: 390;
- available 4h files after quality gates: 14;
- eligible 4h files after split-depth gate: 0.

`POSITION_SWING` split-depth requirement:

- primary horizon: 20 bars;
- secondary horizons: 10 and 40 bars;
- split floor: three chronological split segments with 160 rows each;
- purge/embargo budget: 80 rows;
- required valid OHLCV rows: 560;
- available 1d files after quality gates: 15;
- eligible 1d files after split-depth gate: 0.

The numerical row floors are proposed readiness gates, not approved scientific
acceptance thresholds. Minimum candidate counts remain
`HUMAN_APPROVAL_REQUIRED`.

## Protocol Findings

- Current candidate construction is single-timeframe.
- `1d`/`1w` higher-timeframe context remains a future extension, not active
  protocol behavior.
- Proposed horizons were selected before performance inspection and require
  human approval.
- Universe split is deterministic sorted modulo 3 with development,
  validation, and locked holdout buckets.
- Temporal split is chronological 60/20/20 with no row shuffle.
- Purge/embargo uses maximum approved horizon bars.
- Small-universe limitations are explicit; no cross-sectional independence is
  claimed.
- Favourite or user-interest tickers are not accepted as the sole evidence
  base.
- Protocol status remains `PROTOCOL_PROPOSED_WITH_BLOCKERS`.
- Protocol digest from the final readiness run:
  `bf07595e4f8f074f3e883e67e67f9c10f3ddf2e81be6cc0b677f445a7b0393c3`.
- Deterministic serialization is stable and one-field changes alter the digest.
- The protocol is not automatically activated or frozen.

## Outcome and Statistical Readiness

The proposal defines but does not calculate:

- benchmark baselines;
- fixed seeds for future random baselines;
- gross versus cost-sensitive research boundaries;
- OHLCV executable-price limitations;
- candidate-generation metrics;
- future outcome metrics;
- confidence intervals;
- dependence-aware resampling;
- multiple-testing controls;
- PBO and Deflated-Sharpe applicability conditions;
- proposed acceptance criteria and inconclusive-evidence handling.

Outcome-contract gaps remain:

- explicit MFE/MAE fields are not in the accepted outcome schema;
- bid/ask, commission, spread, slippage, and executable fill modelling are not
  available from OHLCV alone;
- same-bar and gap-through semantics remain OHLC-bar limited.

Arbitrary numerical acceptance criteria remain `HUMAN_APPROVAL_REQUIRED`.

## Trial Ledger

The trial-ledger policy and example are accepted as no-performance governance
artifacts. Future trials must record trial ID, protocol generation, code
commit, data-manifest digest, candidate-builder version, `StrategyConfig`
digest, profile, universe, temporal split, horizon, baseline, costs, seeds,
metrics, status, holdout access, and follow-up reason.

The validator enforces append-only behavior, no deletion, no retroactive edits,
unique trial IDs, required governance fields, and no absolute paths, including
nested ledger values. The example contains no performance values, credentials,
or absolute paths.

## Verification

Required checks used `env\Scripts\python.exe`.

- `python -m pip check`: passed.
- Focused readiness/source-assurance suite: 39 passed, 3 accepted third-party
  polygon/websockets warnings.
- `pytest --collect-only -q`: 539 tests collected.
- Full default suite: 539 passed, 3 accepted third-party polygon/websockets
  warnings.
- `python -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed.
- Tests added since accepted baseline: 19. The increase covers readiness
  manifest identity, duplicate and ambiguous identity failure, safe paths,
  deterministic digests, timestamp range accuracy, OHLCV checks, split-depth
  feasibility, universe and temporal splits, protocol digest behavior,
  recursive trial-ledger governance, CLI no-peek behavior, and source-assurance
  leakage controls.

Git status immediately before and after the full suite matched:

```text
 M tests/test_source_assurance.py
?? config/
?? docs/plans/MARKETFLOW_SWING_APPLICABILITY_PROTOCOL_PLAN.md
?? docs/research/
?? docs/status/MARKETFLOW_SWING_APPLICABILITY_READINESS_STATUS.md
?? marketflow/research/
?? tests/test_swing_applicability_readiness.py
```

The default suite did not modify tracked files.

## Reviewer Findings

Reviewer A findings and dispositions:

- High: feasibility overstated readiness by ignoring split floors,
  purge/embargo rows, and unique eligible identities. Fixed.
- Medium: timestamp coverage used physical first/last rows for non-monotonic
  data. Fixed.
- Medium: duplicate-count semantics were under-defined in docs. Fixed.
- Medium: `valid_ohlcv_row_count` did not validate volume. Fixed.
- Low: no-performance call checks missed attribute calls. Fixed.
- Low: nested trial-ledger paths were not checked. Fixed.

Reviewer B findings and dispositions:

- High: insufficient rows could produce `LIMITED_DATA` instead of `BLOCKED`.
  Fixed.
- High: split-depth feasibility was not tied to proposed split controls. Fixed.
- Medium: final evidence was pending. Fixed by this acceptance document and the
  refreshed status document.
- Low: no-performance call checks missed attribute calls. Fixed.

No critical or high reviewer finding remains open.

## Remaining Limitations

- Duplicate local dataset identities require a reviewed data-remediation phase.
- Current local 4h and 1d histories are insufficient for the proposed
  multi-split no-peek design.
- Adjustment provenance is unknown where explicit metadata is absent and no
  price-history inference or split correction is performed.
- Multi-timeframe context is not active.
- Explicit MFE/MAE, cost/slippage, and executable-fill modelling are not
  accepted.
- Predictive validity, economic significance, and profitability are not
  accepted.

Next required remediation phase: resolve duplicate ticker/timeframe identities
and obtain or approve sufficient history before any protocol freeze or outcome
campaign.
