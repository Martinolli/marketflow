# MarketFlow Swing Applicability Readiness Status

Status: BLOCKED

Date: 2026-07-30

Branch: `feature/swing-applicability-protocol`

Base commit: `3f93671d9d8abc0d7c48515680b37bc6b8980415`

## Starting State

- Starting tree: clean.
- Python: `env\Scripts\python.exe`, Python 3.12.10.
- `pip check`: passed.
- No commit or tag created.
- No provider, broker, execution, dependency, or network check was run.

## Dataset Inventory Summary

A no-peek local manifest was generated into ignored local research output:

- `.marketflow/research/swing_applicability_manifest.json`

The generated manifest is not source-controlled.

Sanitized inventory summary:

- Manifest status: `ineligible`.
- Manifest digest: `3edff02356e1a571c0fd84c3a785f27b076a1077d763da6600682689ff3efecd`.
- In-scope canonical dataset files: 54.
- Canonical tickers: 6.
- Unique ticker/timeframe identities: 16.
- Timeframe counts:
  - `1d`: 15
  - `1h`: 22
  - `1w`: 3
  - `4h`: 14
- Dataset status counts:
  - `valid`: 48
  - `limited`: 6
- Files missing explicit volume column: 0.
- Missing or invalid volume rows: 0.
- Duplicate ticker/timeframe identities: 12 identities with more than one
  source file.
- Excess duplicate files above one source per identity: 38.
- Unique ticker/timeframe identity counts by timeframe:
  - `1d`: 5
  - `1h`: 6
  - `1w`: 1
  - `4h`: 4

Identity and coverage summary:

| Ticker | Timeframe | Files | Row Count Range | Timestamp Coverage | Status |
| --- | --- | ---: | ---: | --- | --- |
| AAAU | 1d | 7 | 250-252 | 2025-06-20 to 2026-07-30 | valid |
| AAAU | 1h | 9 | 361-381 | 2026-04-30 to 2026-07-30 | valid |
| AAAU | 1w | 3 | 105-105 | 2024-06-23 to 2026-06-21 | limited |
| AAAU | 4h | 7 | 266-279 | 2026-03-11 to 2026-07-30 | valid |
| AAPL | 1d | 3 | 251-252 | 2025-06-09 to 2026-07-30 | valid |
| AAPL | 1h | 3 | 432-443 | 2026-04-30 to 2026-07-30 | valid |
| AAPL | 4h | 3 | 239-324 | 2026-03-02 to 2026-07-16 | limited/valid |
| AI | 1d | 3 | 251-252 | 2025-06-09 to 2026-07-06 | valid |
| AI | 1h | 4 | 424-441 | 2026-04-30 to 2026-07-06 | valid |
| AI | 4h | 2 | 267-283 | 2026-03-09 to 2026-07-06 | valid |
| AVAV | 1h | 1 | 417 | 2026-04-30 to 2026-06-09 | valid |
| IONQ | 1d | 1 | 252 | 2025-06-09 to 2026-06-09 | valid |
| IONQ | 1h | 4 | 432-443 | 2026-04-27 to 2026-07-02 | valid |
| IONQ | 4h | 2 | 227-293 | 2026-03-09 to 2026-06-16 | limited/valid |
| LOAR | 1d | 1 | 252 | 2025-06-09 to 2026-06-09 | valid |
| LOAR | 1h | 1 | 227 | 2026-04-30 to 2026-06-09 | limited |

## Data Quality Findings

- The manifest uses strict ticker/timeframe identity inferred from canonical `*_wyckoff_annotated.csv` filenames.
- Source references are safe relative paths in the generated manifest.
- Duplicate identity is the main blocker. Multiple local canonical files exist for the same ticker/timeframe identity.
- Duplicate detection uses exact canonical ticker/timeframe identity and does
  not resolve duplicates by modification time, file size, row count, history
  length, suffix shape, alphabetical order, first match, or latest timestamp.
- The manifest is therefore `ineligible` until a deterministic dataset-selection rule is approved.
- Local 4h and 1d row counts are useful for protocol design but below the proposed multiple-split and purge/embargo floors.
- Adjustment provenance was not explicit in inspected datasets, so adjustment status is recorded as `CORPORATE_ACTION_ADJUSTMENT_STATUS_UNKNOWN`.
- No split/dividend adjustment status was inferred from price behavior.

## Profile Feasibility

`SWING`:

- Decision timeframe: `4h`.
- Proposed primary horizon: 10 bars.
- Secondary sensitivity horizons: 5 and 15 bars.
- Proposed split floor: 3 chronological split segments with at least 120 rows
  each.
- Proposed purge/embargo budget: 30 rows, derived from two boundaries times
  the 15-bar maximum proposed horizon.
- Required valid OHLCV rows for split-depth readiness: 390.
- Available 4h files: 14.
- Unique 4h ticker/timeframe identities: 4.
- Eligible 4h dataset files after quality gates: 14.
- Eligible 4h dataset files after split-depth gate: 0.
- Status: `BLOCKED`.
- Blockers:
  - duplicate dataset identity;
  - insufficient rows for multiple sequential splits under the proposed
    390-row structural floor.

`POSITION_SWING`:

- Decision timeframe: `1d`.
- Proposed primary horizon: 20 bars.
- Secondary sensitivity horizons: 10 and 40 bars.
- Proposed split floor: 3 chronological split segments with at least 160 rows
  each.
- Proposed purge/embargo budget: 80 rows, derived from two boundaries times
  the 40-bar maximum proposed horizon.
- Required valid OHLCV rows for split-depth readiness: 560.
- Available 1d files: 15.
- Unique 1d ticker/timeframe identities: 5.
- Eligible 1d dataset files after quality gates: 15.
- Eligible 1d dataset files after split-depth gate: 0.
- Status: `BLOCKED`.
- Blockers:
  - duplicate dataset identity;
  - insufficient rows for multiple sequential splits under the proposed
    560-row structural floor.

## Multi-Timeframe Capability Finding

The accepted canonical candidate builder is single-timeframe. Local `1d` and
`1w` files may support future context research, but production candidate
construction does not currently consume multi-timeframe context.

No higher-timeframe feature was added.

## Proposed Horizons

- `SWING`: primary 10 bars; secondary 5 and 15 bars.
- `POSITION_SWING`: primary 20 bars; secondary 10 and 40 bars.

Horizon choices are proposed for human approval only. They were not selected
from observed outcomes or returns. Any later horizon addition is a new trial.

## Universe and Split Proposal

Universe policy:

- sort ticker symbols deterministically;
- assign modulo 3 buckets:
  - development;
  - validation;
  - locked holdout.

The current local universe is small and concentrated. If ticker-level holdout
is not meaningful after duplicate resolution, use temporal holdout plus a
future external-universe validation requirement.

## Temporal and Walk-Forward Proposal

Temporal split:

- chronological 60/20/20 by timestamp range;
- no random row shuffling;
- purge candidate horizons at split boundaries;
- embargo by maximum approved horizon bars.

Walk-forward:

- expanding or rolling design must be approved before performance inspection;
- zero-candidate folds are recorded;
- incomplete-evidence candidates remain non-actionable and separately counted;
- uncalibrated score profiles are reported, not promoted;
- minimum candidate count is `HUMAN_APPROVAL_REQUIRED`.

## Outcome Contract Readiness

Existing outcome schema supports:

- `TP_FIRST`;
- `SL_FIRST`;
- `NEITHER`;
- `AMBIGUOUS`;
- `INVALID`;
- same-bar policies;
- horizon diagnostics;
- hit timestamp/index;
- planned RR;
- mark-to-market R for neither outcomes.

Gaps before campaign execution or economic claims:

- explicit MFE/MAE fields are not in the accepted outcome schema;
- bid/ask, commission, and slippage modelling are not available from OHLCV alone;
- gap-through-stop/target semantics remain OHLC-bar limited;
- executable market-open fill quality is not accepted.

No outcome evaluator was invoked during this task.

## Baselines, Costs, Metrics, and Acceptance Criteria

Proposed baselines:

- time-matched unconditional long baseline;
- matched random-entry baseline using fixed seeds;
- declared deterministic trend baseline only if existing trend contract is used.

Cost modelling:

- gross price-path research can be separated from economic claims;
- fixed cost sensitivity is `HUMAN_APPROVAL_REQUIRED`;
- spread/slippage sensitivity is `HUMAN_APPROVAL_REQUIRED`;
- no net profitability claim is allowed until cost assumptions are approved.

Metrics are defined in the protocol proposal but were not calculated.

Acceptance thresholds remain `HUMAN_APPROVAL_REQUIRED` where numeric values
would be arbitrary before results.

## Trial Ledger and Protocol Digest

- Trial ledger policy: append-only, no deletion, no retroactive edits.
- Example ledger: `config/swing_trial_ledger.example.json`.
- Example protocol: `config/swing_applicability_protocol.example.toml`.
- Protocol proposal digest from the local readiness run:
  `bf07595e4f8f074f3e883e67e67f9c10f3ddf2e81be6cc0b677f445a7b0393c3`.
- Digest changes when protocol fields change.
- Protocol status remains `PROTOCOL_PROPOSED_WITH_BLOCKERS`.

## Tests and Warnings

Focused readiness tests:

- `env\Scripts\python.exe -m pytest tests/test_swing_applicability_readiness.py tests/test_source_assurance.py -q`
- Result: 39 passed, 3 accepted third-party warnings.

Full suite:

- `env\Scripts\python.exe -m pytest --collect-only -q`: 539 tests collected.
- `env\Scripts\python.exe -m pytest -q`: 539 passed, 3 accepted third-party warnings.
- Test count explanation: accepted baseline was 520 tests; this task adds
  19 tests for readiness manifest identity, duplicate/ambiguous identity
  failure, safe paths, deterministic digests, timestamp range accuracy,
  OHLCV checks, split-depth profile feasibility, universe/temporal splits,
  protocol digest behavior, recursive trial-ledger governance, CLI no-peek
  behavior, and source-assurance leakage controls.

Compile and diff:

- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests`: passed.
- `git diff --check`: passed.

Pre/post full-suite Git status matched; tests did not modify tracked files.

## Reviewer Findings

Reviewer A:

- High: profile feasibility could use total rows instead of valid OHLCV rows.
- High: absolute scan roots outside the repository could be traversed.
- Disposition: fixed. Feasibility now uses valid OHLCV row counts, and scan roots fail closed before traversal when outside the repository.

Reviewer B:

- High: readiness CLI did not fully enforce repo-only and ignored-manifest-output boundaries.
- High: ambiguous timeframe identities were not failed closed.
- High: trial-ledger validation was too weak for required governance fields.
- Disposition: fixed. Manifest output is constrained to `.marketflow/research`, ambiguous dataset identities fail closed, and trial rows require fixed governance fields, unique IDs, append-only behavior, and no absolute paths.

No critical or high reviewer finding remains open.

Acceptance review correction:

- High: timestamp range metadata used physical first/last row values for
  non-monotonic datasets instead of the true minimum and maximum parsed
  timestamps. Disposition: fixed. The manifest now records min/max timestamp
  range while still failing non-monotonic datasets closed.
- High: row-depth feasibility did not consume split floors, purge/embargo
  requirements, or unique eligible identity availability. Disposition: fixed.
  The feasibility gate now reports required split count, split-floor rows,
  max horizon bars, purge/embargo rows, required valid OHLCV rows, eligible
  dataset count, and eligible identity count.
- High: insufficient row depth could produce `LIMITED_DATA` instead of a
  protocol-freeze blocker. Disposition: fixed. Any freeze blocker now leaves
  the profile `BLOCKED`.
- Medium: `valid_ohlcv_row_count` validated OHLC rows but not volume.
  Disposition: fixed. Volume is part of valid OHLCV row counting and missing
  or invalid volume remains visible.
- Low: static no-performance checks did not catch forbidden attribute-form
  calls. Disposition: fixed by checking both direct calls and attribute calls.
- Low: trial-ledger absolute-path validation did not inspect nested values.
  Disposition: fixed with recursive path validation.

## Blockers

- Duplicate canonical ticker/timeframe identities in local data.
- 4h and 1d row counts are below proposed multiple-split floors for most local identities.
- Adjustment provenance is unknown.
- Current candidate construction is single-timeframe.
- Outcome schema lacks explicit MFE/MAE fields.
- Cost/slippage modelling is not approved.
- Human approval is required before protocol freeze or campaign execution.

## Required Statements

- No performance result was inspected.
- No horizon or profile was selected from returns.
- Predictive usefulness is not accepted.
- Profitability is not accepted.
- Protocol requires human approval before campaign execution.
