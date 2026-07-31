# MarketFlow Artifact Lineage v1 Status

Status: PASS

Date: 2026-07-31

Branch: `feature/swing-artifact-lineage-v1`

Base commit: `e005d216245bf5d6f42e31ae878de46a418db984`

## Baseline

- Initial branch: confirmed.
- Initial commit: confirmed.
- Initial tree: clean.
- Python: `env\Scripts\python.exe`.
- `pip check`: passed.
- No commit or tag has been created.
- No network, provider, broker, execution, dependency, manual live, outcome
  campaign, or performance-analysis step has been run.

Artifact Lineage v1 writing is not accepted until this task passes all final
checks and read-only reviews.

## Implementation

Added canonical writer-side support:

- opaque run context creation under `.marketflow/reports/runs`;
- strict `marketflow.artifact_manifest.v1` manifest model;
- exact payload SHA-256 and byte-size recording;
- source dataset digest propagation;
- parent/input and lineage ID recording;
- atomic payload then manifest commit marker;
- manifest validation and sanitized receipts;
- Workflow A manual-scenario artifact creation;
- Workflow B candidate-core artifact creation;
- canonical MC summary artifact creation;
- canonical plot artifact creation.

## Writer Inventory

- Batch analysis: legacy timestamp outputs remain; canonical mode writes
  `ANNOTATED_DATASET` receipts for explicit lineage timeframes.
- Strategy: legacy report-root scan remains legacy; canonical mode consumes one
  exact `ANNOTATED_DATASET` manifest and writes `CANDIDATE_CORE`.
- Monte Carlo: legacy single-run/backtest commands remain legacy; manual
  lineage mode writes manual scenario then MC; canonical lineage mode consumes
  `CANDIDATE_CORE` and accepts no geometry override.
- Plotting: legacy plotting remains legacy; canonical mode consumes exact
  analysis and MC manifests and writes `ANNOTATED_PLOT`.
- Studio/services: remain optional/legacy unless they call the canonical
  helpers; analytical core does not depend on Streamlit.

## Workflows

Workflow A:

```text
ANNOTATED_DATASET
  -> MANUAL_SCENARIO_DEFINITION
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

Workflow B:

```text
ANNOTATED_DATASET
  -> CANDIDATE_CORE
  -> MONTE_CARLO_SUMMARY
  -> ANNOTATED_PLOT
```

## Atomic And Collision Behavior

Canonical writes fail on run, payload, or manifest collision. The manifest is
installed last and marks a committed artifact. Timestamp-only identity is not
used for canonical artifacts. Temporary and partial files are not selectable.

## Incomplete Artifact Behavior

- Payload without manifest: incomplete.
- Manifest without payload: invalid.
- Digest mismatch: invalid.
- Size mismatch: invalid.
- Temp file: ignored.
- Unknown schema: invalid.
- Legacy file without manifest: not canonical.

## Digest Contracts

- Annotated datasets use exact payload bytes for payload and source digest.
- Candidate-core digest uses the accepted candidate-core projection.
- StrategyConfig digest uses deterministic dataclass projection.
- Manual scenario digest is deterministic and distinct from candidate-core
  digest.

## CLI Handoff

Canonical modes require explicit `--lineage-mode` plus exact manifest inputs.
Receipts include run ID, artifact ID, stage, artifact type, workflow, ticker,
profile, timeframe, payload ref, and manifest ref. Receipts contain no absolute
home path.

## Legacy Treatment

Existing `.marketflow/reports` files remain `LEGACY_UNVERSIONED_ARTIFACTS`.
They were not rewritten, moved, deleted, migrated, or backfilled. Legacy modes
do not claim immutable lineage.

## Streamlit And LLM

Streamlit remains optional. LLM output remains non-authoritative narrative or
legacy/experimental and cannot satisfy canonical candidate, MC, or plot input
contracts.

## Verification To Date

- `env\Scripts\python.exe -m pip check`: passed before and after
  implementation.
- Focused Lineage v1 tests: 13 passed, 3 accepted third-party warnings.
- Focused Lineage v1 plus operational/read-side/prior integrity set: 142
  passed, 3 accepted third-party warnings.
- Full collection: 569 tests collected.
- Pre-suite `git status --short -- .marketflow\reports`: empty.
- Full suite: 569 passed, 3 accepted third-party warnings.
- Post-suite `git status --short -- .marketflow\reports`: empty.
- `env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps
  trading_dashboard utils rag tests`: passed.
- `git diff --check`: passed with Git LF-to-CRLF normalization warnings only.
- Intended-file secret/path scan found no secrets or absolute home paths; hits
  were expected domain terms and existing MC terminology.

## Reviewer Findings

Reviewer A returned BLOCKED with four findings:

- Canonical plot ancestry could be forged by crafting
  `lineage_artifact_ids`. Disposition: fixed. Plot commits now validate the
  saved manifest chain and reconstruct parent/input ancestry from saved
  manifests before accepting MC ancestry.
- `source_ref` accepted unsafe relative paths. Disposition: fixed. Manifest
  build and validation now reject unsafe `source_ref` values and require present
  regular files when a source ref is declared.
- Canonical batch could swallow lineage writer failures inside the ticker-level
  broad exception handler. Disposition: fixed. Canonical mode now re-raises
  lineage contract failures and does not complete as partial/no-receipt success.
- `CANDIDATE_CORE` payload stored the full mutable candidate while digesting
  only the core projection. Disposition: fixed. The payload now stores the
  strict candidate-core projection plus eligibility/config metadata.

Reviewer B returned BLOCKED with six findings:

- MC summary writer did not enforce summary geometry against parent payload.
  Disposition: fixed. Manual and canonical MC summaries now compare entry,
  stop, target, horizon where applicable, and digest against parent payloads.
- Plot CLI had a runtime `json` import defect. Disposition: fixed.
- Canonical plot did not consume MC payload despite claiming MC ancestry.
  Disposition: fixed. Canonical plot reads the MC payload and embeds MC input
  details in the HTML payload.
- Manifest validation did not enforce stage/artifact-type pairs. Disposition:
  fixed.
- `created_at` accepted naive timestamps. Disposition: fixed. Validation now
  requires timezone-aware UTC.
- Initial focused coverage was too narrow. Disposition: fixed. Focused coverage
  now includes CLI handoffs, forged ancestry, unsafe source refs, stage/type,
  UTC timestamp, digest, collision, incomplete artifact, and workflow mixing
  cases.

Final acceptance reviewers returned one additional high finding:

- Saved manifest-file location was not validated against the manifest's own
  run/stage/payload reference. Disposition: fixed. `load_manifest()` now
  requires the loaded manifest path to equal the manifest path implied by the
  safe `payload_ref`, and focused tests cover misplaced manifest copies under
  the wrong stage.

## Blockers

None known after focused, related, full-suite, compile, diff, status, and
artifact hygiene checks.

## Remaining Limitations

- Legacy commands and historical reports remain unversioned.
- Studio has not been converted into the canonical lineage driver.
- Canonical batch mode records annotated dataset artifacts after `run_analysis`
  returns exact output paths; deeper interception inside provider/report
  internals is deferred.
- Research protocol remains blocked by data readiness.
- Predictive usefulness and profitability remain unaccepted.
