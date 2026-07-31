# MarketFlow Operational Pipeline Audit Acceptance

## Decision

PASS.

UTC acceptance date: `2026-07-31T15:17:14Z`.

Branch: `feature/swing-operational-pipeline-audit`.

Base commit: `da6cb3564ed77135852741b216075f421a0d128e`.

## Acceptance Boundary

OPERATIONAL WORKFLOW AUDIT / READ-SIDE LINEAGE CONTROLS: ACCEPTED.

COMPLETE END-TO-END IMMUTABLE ARTIFACT WRITING: NOT YET ACCEPTED.

Read-side artifact selection, manual/canonical workflow classification, exact
Monte Carlo candidate geometry checks, explicit plot artifact selection, and
collision safeguards are accepted for local commit.

The raw Monte Carlo CLI still requires first-class immutable artifact identity
writing in a later phase. Historical/raw summaries without immutable
`artifact_id` and `parent_artifact_id` cannot provide complete immutable
lineage.

Research protocol freeze remains blocked. Predictive usefulness,
profitability, execution readiness, provider readiness, and broker integration
remain unaccepted.

## Scope And Exclusions

Accepted scope:

- operational workflow classification;
- artifact identity and parent-selection contracts;
- exact Monte Carlo/candidate geometry verification;
- explicit plotting artifact selection;
- collision safeguards;
- workflow/report documentation;
- focused deterministic tests;
- final acceptance evidence.

Explicit exclusions:

- no source identity semantic change;
- no canonical candidate-builder semantic change;
- no phase, event, recency, True Range, entry, stop, target, RR, score,
  threshold, Monte Carlo, Point-and-Figure, Eigen/PCA, outcome, provider,
  broker, or execution semantic change;
- no performance analysis, optimization, profitability analysis, provider call,
  broker check, dependency change, generated report deletion, tag, push, or
  remote change.

## Workflow A

Exact chain:

```text
scripts/marketflow_batch_analysis.py
  -> marketflow/marketflow_monte_carlo_trade.py
  -> scripts/plot_annotated_features.py
  -> .marketflow/reports
```

Classification:

```text
workflow_type = MANUAL_SCENARIO_ANALYSIS
scenario_origin = MANUAL_SCENARIO
```

Acceptance findings:

- geometry may be explicitly supplied by the operator;
- no candidate-core digest is fabricated;
- no Strategy rank eligibility is claimed;
- Monte Carlo remains a conditional path diagnostic;
- Workflow A output must not be labelled as canonical Strategy generation;
- plotting preserves explicit artifact linkage and does not scan for a latest
  MC summary.

## Workflow B

Exact chain:

```text
scripts/marketflow_batch_analysis.py
  -> marketflow/marketflow_strategy.py
  -> marketflow/marketflow_monte_carlo_trade.py
  -> scripts/plot_annotated_features.py
  -> .marketflow/reports
```

Classification:

```text
workflow_type = CANONICAL_STRATEGY_DECISION_SUPPORT
```

Acceptance findings:

- Strategy uses the canonical point-in-time candidate builder;
- candidates must be complete and rank/action eligible before canonical MC
  handoff;
- MC requests copy exact ticker, timeframe, entry, stop, target, candidate-core
  digest, and StrategyConfig identity where available;
- MC does not recompute entry, stop, or structural target;
- MC cannot convert an incomplete candidate into an actionable setup;
- Workflow B rejects Workflow A summaries when workflow metadata is available.

## Command Interface

Supported command forms:

```powershell
env\Scripts\python.exe scripts\marketflow_batch_analysis.py TICKER1 TICKER2
env\Scripts\python.exe marketflow\marketflow_strategy.py --report-root ".marketflow\reports" --date-glob "<exact-run-or-date>" --tf <tf> --tickers TICKER1 TICKER2
env\Scripts\python.exe marketflow\marketflow_monte_carlo_trade.py "<source_csv>" --entry <entry> --sl <stop> --tp <target> --tf <tf> --horizon <bars>
env\Scripts\python.exe scripts\plot_annotated_features.py "<source_csv>" --mc-summary "<exact_mc_summary>"
```

Command-interface findings:

- `--mc-summary` is an explicit plot input, not a directory-scan hint;
- `--batch latest` remains an opt-in legacy convenience and is not an
  immutable-lineage selection method;
- canonical Workflow B does not use latest, first, modification time, ticker
  only, timeframe only, or filename similarity as automatic artifact fallback.

## Artifact Identity Model

`marketflow/operational_artifacts.py` defines the strict model:

- `schema_version`
- `artifact_id`
- `run_id`
- `stage`
- `workflow_type`
- `ticker`
- `analysis_profile`
- `timeframe`
- `source_dataset_identity`
- `source_dataset_digest`
- `code_commit`
- `strategy_config_digest`
- `candidate_core_digest`
- `parent_artifact_id`
- `generated_at`
- safe relative `artifact_ref`

Validation findings:

- fixed workflow identifiers and fixed stage identifiers are enforced;
- `artifact_id`, `run_id`, ticker, timeframe, and source identity are nonempty;
- safe relative references are required;
- path traversal and paths outside an artifact root fail closed;
- arbitrary free-form workflow/stage values fail closed;
- self-parent artifacts fail closed;
- detectable parent cycles fail closed;
- identity metadata excludes account identifiers, credentials, absolute private
  paths, and live trade values.

## Parent Selection

Downstream artifact selection is accepted only through exact metadata:

- exact artifact ID;
- exact parent artifact ID when required;
- exact ticker/timeframe/run/workflow/stage metadata when required.

Results:

- zero matches fail closed;
- one exact match continues;
- more than one match fails closed as ambiguous.

Prohibited selection methods:

- newest-file selection;
- first-file selection;
- first glob match;
- ticker-only match;
- timeframe-only match;
- modification-time match;
- filename similarity;
- cross-run selection.

## Monte Carlo Summary Selection

Strategy MC evidence is accepted only when one requested-timeframe summary
matches the selected source through explicit metadata:

- ticker;
- timeframe;
- source CSV identity;
- workflow type.

Zero matches leave MC evidence unavailable. Multiple matches leave MC evidence
ambiguous and unavailable. Missing identity metadata, wrong ticker, wrong
workflow, wrong timeframe, and contradictory source metadata are rejected. No
newest, first, or filename-only fallback remains.

Limitation: historical/raw summaries without first-class IDs cannot provide
complete immutable lineage.

## Geometry Equality

Workflow B MC geometry is verified against canonical candidate fields:

- ticker;
- timeframe;
- entry;
- stop;
- target;
- candidate-core digest where present.

Any changed entry, stop, target, ticker, timeframe, or candidate digest fails
closed. Equality is exact over the canonical serialized values; no approximate
rounding contract was introduced.

## Plot Input

`scripts/plot_annotated_features.py` findings:

- MC overlay is used only when `--mc-summary` is supplied;
- the supplied path must be a regular `*_mc_summary.json` file;
- the MC summary `csv` identity must match the plotted CSV;
- the MC summary must be in the same report directory as the plotted CSV;
- zero explicit MC input means no MC overlay;
- no report-directory scan occurs;
- plotting does not reconstruct candidate semantics and does not recalculate
  entry, stop, target, RR, score, or event status.

## Report Root Inventory

The audit inspected `.marketflow/reports` only by safe metadata:

- filenames;
- extensions;
- directory structure;
- schema keys.

Sanitized counts:

- total files: 925;
- CSV: 426;
- HTML: 186;
- Markdown: 154;
- JSON: 131;
- TXT: 24;
- MC summaries: 34;
- PnF sidecars: 19;
- annotated CSVs: 82;
- LLM analysis JSONs: 24;
- walk-forward cases/results/summaries: 56 each.

No profit, loss, win rate, expectancy, best ticker, best timeframe, trade
amount, or account value was inspected or recorded. No generated inventory file
is committed.

## Stale And Collision Findings

Findings:

- local reports often encode ticker/timeframe in filenames but do not
  consistently encode immutable run identity;
- second-resolution timestamp filenames can collide;
- historical reports lack complete identity metadata;
- no historical report should be deleted, rewritten, or auto-selected among.

Accepted safeguards:

- read-side selection rejects stale/latest/first fallback;
- `run_specific_output_path(...)` refuses overwrites;
- manual and canonical workflows have distinct fixed identifiers.

Deferred:

- run-specific immutable names and complete identity writing must be threaded
  through the raw CLI writers in a later phase.

## Candidate And Config Digests

Candidate-core digest findings:

- deterministic canonical projection;
- includes ticker, timeframe, entry, stop, target, source CSV, source status,
  and candidate-build status;
- excludes future outcome fields, wrapper metadata, timestamps, random values,
  and absolute paths;
- changes when candidate geometry or selected semantic inputs change;
- does not change merely because report formatting changes.

StrategyConfig digest findings:

- deterministic helper support is present;
- Workflow B request accepts `strategy_config_digest`;
- raw CLI identity writing does not yet thread it end to end and remains
  deferred.

## Fixed Profile Design

Future normal user input:

```text
ticker only
```

Future profiles:

- `SWING`: candidate timeframe `4h`, minimum valid rows `390`;
- `POSITION_SWING`: candidate timeframe `1d`, minimum valid rows `560`.

The future normal mode must not expose timeframe, period/history window,
primary timeframe, ATR length, stop multiplier, minimum RR, PnF/MC toggles,
component weights, or evidence toggles.

Current Studio Strategy Ranking remains an advanced/legacy operator surface and
still exposes timeframe, StrategyConfig values, and evidence toggles. This task
documents the fixed-profile contract only. It does not acquire history, freeze
start/end dates, resolve duplicate data sources, combine profile scores, or
implement multi-timeframe context.

## Streamlit And LLM

Streamlit findings:

- Studio is optional;
- analytical modules do not require Streamlit;
- Strategy, Monte Carlo, and operational artifact contracts do not import
  Streamlit;
- Studio wording does not overstate itself as the engine;
- Studio does not reconstruct candidate semantics.

LLM findings:

- LLM paths are non-authoritative narrative or legacy/experimental;
- LLM output does not enter phase, event, volatility, entry, stop, target, RR,
  PnF, POP, evidence availability, composite score, or rank eligibility.

## Manual Live Observation Policy

Prior small live trades and observations are classified as:

```text
EXPLORATORY_MANUAL_LIVE_OBSERVATIONS
```

They must not be used for retrospective threshold changes, parameter
optimization, ticker selection, horizon selection, predictive-validation
claims, or profitability claims. No trade amount, account data, profit, or loss
appears in the policy document.

## Verification

Required final checks used `env\Scripts\python.exe`.

```text
pip check: passed
focused operational pipeline tests: 17 passed, 3 warnings
related integrity tests: 129 passed, 3 warnings
pytest --collect-only -q: 556 tests collected
pytest -q: 556 passed, 3 warnings
compileall -W error: passed
git diff --check: passed
git diff --cached --check: passed
```

Warnings are limited to the accepted third-party `polygon` / `websockets`
deprecation warnings.

The full suite did not modify tracked files. Pre-test and post-test Git status
matched except for the intentional task changes.

No network, provider, broker, execution, dependency, manual live, or
performance check was run.

## Test Count

Accepted prior applicability-readiness count: `539` tests.

Final collection: `556` tests.

Count explanation: the operational audit adds `17` deterministic tests over the
prior 539-test baseline. Coverage includes exact parent selection, missing and
ambiguous parent selection, fixed workflow/stage validation, safe relative
artifact references, parent-cycle rejection, Workflow A/B labelling, complete
and rank-eligible canonical MC handoff, exact MC geometry and digest equality,
metadata-missing and contradictory MC summary rejection, no newest/first
fallback, explicit plot MC input, cross-run plot summary rejection, collision
refusal, digest determinism, Streamlit isolation, and LLM non-authority.

## Reviewer Findings And Dispositions

Reviewer A findings:

- High: Strategy MC summaries with missing identity metadata could attach stale
  POP evidence. Disposition: fixed; ticker/source/workflow/timeframe metadata
  is required for canonical MC evidence.
- High: plot overlay validation was basename-only and could accept same-name
  summaries from other runs. Disposition: fixed; explicit summaries must be in
  the same report directory as the plotted CSV.
- Medium: operational contract was not wired into every active writer while the
  status text implied pre-execution production enforcement. Disposition: docs
  now classify the work as accepted read-side controls and defer complete
  writer integration.
- Low: status evidence test count was stale. Disposition: refreshed.

Reviewer B findings:

- High: required identity fields could be `None` and stringified. Disposition:
  fixed; required fields now fail closed before serialization.
- Medium: fixed-profile text conflicted with current Studio advanced controls.
  Disposition: docs classify fixed-profile as future normal mode and current
  Studio Strategy Ranking as advanced/legacy.
- Low/Medium: legacy strategy document still described latest/fallback
  behavior. Disposition: corrected.

No critical or high reviewer finding remains unresolved.

## Source-Semantic Non-Regression

No accepted strategy semantic was changed:

- source identity;
- canonical candidate builder;
- phase/event logic;
- event recency;
- True Range;
- entry;
- stop;
- target;
- RR;
- evidence statuses;
- score formula;
- weights;
- thresholds;
- outcome evaluator;
- Monte Carlo mathematics;
- Point-and-Figure;
- Eigen/PCA.

Previous baseline, source identity, risk/reward, True Range, event recency,
evidence availability, candidate-builder alignment, and applicability-readiness
integrity milestones remain accepted.

## Remaining Limitations

- raw MC CLI summaries still need first-class immutable identity writing;
- timestamp-oriented legacy writers still need run-specific identity threading;
- historical reports lack complete identity metadata;
- `--batch latest` remains an explicit legacy convenience, not a reproducible
  lineage method;
- fixed-profile UI implementation and data remediation are deferred;
- duplicate dataset identities and insufficient history still block research
  protocol freeze;
- predictive usefulness, economic significance, and profitability remain
  unaccepted.

## Next Phase

Thread first-class immutable artifact writing through raw MC, plot, batch, and
strategy writers without changing Strategy semantics. That phase should emit
validated artifact IDs, parent IDs, source digests, StrategyConfig digests,
candidate-core digests, safe relative artifact references, and collision-proof
run-specific output names.

## Final Acceptance Statement

Operational workflow classification is accepted.

Automatic stale/latest/first artifact selection is prohibited.

Read-side artifact selection controls are accepted.

Full first-class artifact identity writing is not yet accepted.

Research protocol remains blocked.

Predictive usefulness and profitability remain unaccepted.
