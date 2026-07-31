# MarketFlow Artifact Lineage v1 Acceptance

## Decision

PASS.

UTC acceptance date: `2026-07-31T16:24:59Z`.

Branch: `feature/swing-artifact-lineage-v1`.

Base commit: `e005d216245bf5d6f42e31ae878de46a418db984`.

Commit intent: local commit only.

Tag: not created.

Push: not performed.

## Acceptance Boundary

Artifact Lineage v1 writing is accepted for newly generated canonical
operational artifacts under `.marketflow/reports/runs`.

Historical `.marketflow/reports` files remain `LEGACY_UNVERSIONED_ARTIFACTS`.
They were not migrated, rewritten, deleted, renamed, merged, moved, backfilled,
or assigned fabricated lineage.

This acceptance does not establish predictive usefulness, profitability,
provider readiness, broker integration, execution capability, or research
protocol freeze.

## Scope And Exclusions

Accepted scope:

- opaque run and artifact identities;
- strict versioned manifests;
- payload, source, StrategyConfig, candidate-core, and manual-scenario digests;
- collision-safe atomic writer;
- saved manifest and ancestry validation;
- Workflow A and Workflow B canonical handoff helpers;
- canonical CLI handoff modes;
- plot ancestry validation;
- focused deterministic tests and documentation.

Explicit exclusions:

- no source-identity semantic change;
- no candidate-builder formula or output change;
- no phase/event, event-recency, True Range, entry, stop, target, RR,
  evidence, score, threshold, Monte Carlo, PnF, Eigen/PCA, outcome, provider,
  broker, execution, or research-protocol semantic change;
- no real operational workflow, market-data provider call, broker call,
  performance campaign, outcome aggregation, optimization, dependency change,
  tag, push, or remote change.

## Writer Inventory

Annotated dataset writer:

- stage: `BATCH_ANALYSIS`;
- artifact type: `ANNOTATED_DATASET`;
- workflows: manual scenario analysis or canonical Strategy decision support;
- input: exact newly produced CSV path;
- output: copied CSV payload and `.manifest.json`;
- collision/atomicity: run-wide artifact ID and final path collisions fail,
  payload installs first, manifest installs last, no replace;
- receipt: safe run/artifact IDs and safe relative payload/manifest refs;
- failure: fixed `ArtifactContractError`.

Candidate core writer:

- stage: `STRATEGY_CANDIDATE`;
- artifact type: `CANDIDATE_CORE`;
- workflow: `CANONICAL_STRATEGY_DECISION_SUPPORT`;
- input: exact saved `ANNOTATED_DATASET` manifest and rank/action-eligible
  Strategy candidate;
- output: strict candidate-core JSON plus eligibility/config metadata;
- failure: rejects non-canonical input, non-actionable candidate, geometry
  mismatch, unsafe path, collision, and saved-chain failure.

Manual scenario writer:

- stage: `MANUAL_SCENARIO`;
- artifact type: `MANUAL_SCENARIO_DEFINITION`;
- workflow: `MANUAL_SCENARIO_ANALYSIS`;
- input: exact saved manual-workflow `ANNOTATED_DATASET` manifest plus explicit
  entry, stop, target, and horizon;
- output: deterministic scenario JSON and manual-scenario digest;
- failure: rejects canonical input, non-finite geometry, bad horizon, unsafe
  paths, collisions, and saved-chain failure.

Monte Carlo summary writer:

- stage: `MONTE_CARLO`;
- artifact type: `MONTE_CARLO_SUMMARY`;
- workflows: manual scenario or canonical Strategy;
- input: exact saved manual-scenario or candidate-core parent;
- output: deterministic MC summary JSON bound to parent digest and geometry;
- failure: rejects wrong parent type, changed geometry, changed digest,
  changed timeframe, unsafe paths, collisions, and saved-chain failure.

Annotated plot writer:

- stage: `PLOT`;
- artifact type: `ANNOTATED_PLOT`;
- workflows: manual scenario or canonical Strategy;
- inputs: exact saved annotated dataset and exact saved MC summary;
- output: exact HTML bytes and manifest with fixed ordered inputs;
- failure: rejects wrong run, workflow, ticker, timeframe, profile, source
  digest, missing ancestry, duplicate inputs, unsafe paths, and forged lineage.

## Identity Contracts

Run IDs are opaque, collision-resistant by default, path-safe, not timestamp,
ticker, account, operator, or path derived, and injectable only for
deterministic tests. Duplicate run directories fail. Downstream stages reuse
the run ID from saved parents; they do not silently start a second run.
`created_at` is timezone-aware UTC, and malformed or naive timestamps fail.

Artifact IDs are opaque, path-safe, collision-resistant by default, not
timestamp/ticker/account/path derived, injectable only for tests, and unique
inside the run. Same-ID, payload, and manifest collisions fail without
overwrite. Self-parenting and duplicate inputs fail.

## Manifest Schema

Schema version: `marketflow.artifact_manifest.v1`.

The v1 manifest has an exact fixed field set covering identity, market/profile,
source, software/configuration, lineage, payload, and time. Unknown fields,
missing fields, unknown schema versions, unknown workflow/stage/type/profile or
payload values, invalid timestamps, non-list input/lineage fields, unsafe IDs,
unsafe refs, and stage/type mismatches fail closed.

Stage/type mapping:

- `BATCH_ANALYSIS` -> `ANNOTATED_DATASET`;
- `STRATEGY_CANDIDATE` -> `CANDIDATE_CORE`;
- `MANUAL_SCENARIO` -> `MANUAL_SCENARIO_DEFINITION`;
- `MONTE_CARLO` -> `MONTE_CARLO_SUMMARY`;
- `PLOT` -> `ANNOTATED_PLOT`.

## Path And Runtime Root

Canonical references are safe relative POSIX-style refs under the lineage run
root. Absolute paths, drive-qualified paths, UNC/device-style paths, alternate
data streams, colon-containing refs, backslash refs, traversal, dot segments,
Windows device names, paths with trailing spaces/dots, root-prefix lookalikes,
directories, missing payloads, nonregular files, and wrong run/stage
directories fail. Saved manifest files must be located at the manifest path
implied by their own safe `payload_ref`.

Symlink/junction escapes are checked where resolved filesystem targets are
available. Privileged junction-specific creation was not required or performed
in the acceptance run.

## Payload And Digests

Payload digest is SHA-256 over exact committed bytes; byte size is exact.
Changing any payload byte, deleting a payload, changing size, changing schema,
or moving the manifest to the wrong path fails validation. JSON payloads use
deterministic UTF-8 serialization with stable key ordering and no NaN/Infinity.
CSV and HTML payload digests cover exact written bytes; lineage metadata lives
in manifests rather than modifying analytical payload format.

Candidate-core, StrategyConfig, and manual-scenario digests reuse deterministic
JSON-compatible projections. Candidate-core stores the strict semantic core
only. Manual-scenario digest is distinct from candidate-core digest and covers
scenario geometry, horizon, workflow/profile identity, parent artifact, and
source digest.

## Atomic Write And Crash States

Commit sequence:

1. create destination run/stage directories without replacing an existing run;
2. write payload temp file in the target directory;
3. flush/fsync and close payload temp;
4. calculate payload SHA-256 and byte size;
5. write manifest temp file;
6. flush/fsync and close manifest temp;
7. install final payload without replacing an existing path;
8. install final manifest last without replacing an existing path;
9. reload the saved manifest from disk;
10. validate saved manifest and saved ancestry before returning receipt.

No `os.replace` is used. Final paths are not opened in truncate mode before
collision validation. Cleanup is limited to the current attempted payload if a
manifest install fails.

Crash-state findings:

- payload without manifest: incomplete and not selectable;
- manifest without payload: invalid;
- temp files: ignored/incomplete;
- digest or size mismatch: invalid;
- unknown manifest schema: invalid;
- valid manifest committed before a lost receipt remains recoverable only by
  exact saved-manifest validation; retry does not silently overwrite.

## Saved Evidence And Transition Graph

Readers load manifests from disk, verify the manifest path, validate payload
existence, size, digest, run/stage path, source refs, parent/input manifests,
parent/input payloads, same-run constraints, workflow/ticker/timeframe/profile
consistency, source digests, and allowed transitions.

Allowed manual graph:

```text
ANNOTATED_DATASET -> MANUAL_SCENARIO_DEFINITION -> MONTE_CARLO_SUMMARY -> ANNOTATED_PLOT
```

Allowed canonical Strategy graph:

```text
ANNOTATED_DATASET -> CANDIDATE_CORE -> MONTE_CARLO_SUMMARY -> ANNOTATED_PLOT
```

Cross-workflow, cross-run, wrong ticker/timeframe/profile, stage skipping,
reversed transition, self-parent, cycle, orphan child, Workflow A as Workflow B,
and Workflow B as Workflow A fail.

## Workflow Findings

Workflow A is accepted as manual-scenario lineage. It carries explicit
operator geometry and horizon, manual-scenario origin, exact parent annotated
dataset, and manual-scenario digest. It has no candidate-core digest, no rank
eligibility, no Strategy recommendation, no account, no position size, and no
P/L field.

Workflow B is accepted as canonical Strategy lineage. It carries the strict
candidate core, deterministic candidate digest, deterministic StrategyConfig
digest, canonical MC summary, and full plot ancestry. Canonical MC requires a
candidate artifact and rejects geometry overrides.

Geometry equality is exact over canonical serialized numeric values. No display
rounding or tolerance is used. Changed entry, stop, target, horizon where
applicable, ticker, timeframe, profile, candidate digest, or scenario digest
fails.

## CLI And Legacy Isolation

Canonical CLI forms are explicit:

- batch: `--lineage-mode canonical`, optional exact run ID, explicit timeframes;
- strategy: exact annotated-dataset manifest to candidate-core artifact;
- Monte Carlo manual: exact analysis manifest plus explicit geometry;
- Monte Carlo canonical: exact candidate manifest, no geometry override;
- plot: exact analysis and exact MC manifests.

Canonical mode does not scan newest/first/latest, does not use `--batch latest`,
does not fall back to legacy, and does not fabricate lineage from historical
files. Legacy commands remain available and explicitly legacy.

## Streamlit, LLM, And Private Data

Core artifact writers import no Streamlit and require no Streamlit runtime.
LLM output cannot create candidate artifacts or canonical MC inputs, and no
narrative field enters candidate/config/scenario digests.

No accepted manifest or receipt contains account identifiers, live position
size, trade amount, credentials, API tokens, browser/session values, absolute
home paths, or historical performance aggregates. Monte Carlo retains ordinary
diagnostic simulation payload structure; this acceptance did not run or inspect
real simulation results.

## Verification

Required final checks used `env\Scripts\python.exe`.

```text
pip check: No broken requirements found.
focused Artifact Lineage v1 tests: 13 passed, 3 warnings.
related integrity suite: 142 passed, 3 warnings.
pytest --collect-only -q: 569 tests collected.
pytest -q: 569 passed, 3 warnings.
compileall -W error: passed.
git diff --check: passed with Git LF-to-CRLF notices only.
git diff --cached --check: passed with Git LF-to-CRLF notices only.
```

Warnings are the accepted third-party `polygon` / `websockets` deprecation
warnings. No project-owned warnings were introduced.

Test count explanation: prior operational-audit baseline collected `556`
tests. Artifact Lineage v1 adds `13` deterministic tests over immutable run and
artifact identity, atomic commit/collisions, incomplete and misplaced manifests,
strict schema, unsafe Windows refs, non-finite geometry, Workflow A/B lineage,
forged ancestry rejection, plot input validation, canonical CLI receipts, and
source assurance.

Pre-full-suite and post-full-suite `git status --short` matched. The full
suite did not modify tracked files. `.marketflow/reports` safe metadata
inventory and `git status --short -- .marketflow\reports` matched before and
after. No generated lineage run, generated report, generated MC output,
generated plot, market-data file, cache, credential, or local environment file
is committed.

## Reviewer Findings And Dispositions

Initial reviewers:

- High: MC summary writer did not enforce geometry. Fixed.
- High: canonical plot CLI had runtime JSON import defect. Fixed.
- High: canonical plot claimed but did not consume MC payload. Fixed.
- Medium: stage/type pairs were not enforced. Fixed.
- Medium: naive timestamps passed. Fixed.
- High: plot ancestry could be forged through claimed lineage IDs. Fixed.
- High: unsafe `source_ref` passed. Fixed.
- High: canonical batch swallowed lineage failures. Fixed.
- Medium: candidate payload stored full mutable candidate. Fixed.

Final acceptance reviewers:

- High: focused test fixture failed after the stricter saved-chain write
  behavior. Fixed; focused suite now passes.
- High: copied manifest under the wrong stage was accepted. Fixed by binding
  loaded manifest file location to its own `payload_ref`, with regression
  coverage.

No critical or high reviewer finding remains unresolved.

## Previous Integrity Non-Regression

Baseline integrity, source identity, risk/reward integrity, True Range
volatility, Wyckoff event recency, evidence availability, candidate-builder
alignment, swing applicability readiness, and operational read-side lineage
acceptance remain covered by the passing focused and full suites.

No Strategy or Monte Carlo mathematical change was added.

## Remaining Limitations

- Historical reports remain unversioned legacy artifacts.
- Studio has not been converted into the canonical lineage driver.
- Canonical batch mode records annotated dataset artifacts after `run_analysis`
  returns exact output paths; deeper provider/report interception is deferred.
- Research protocol remains blocked by duplicate identity and history-depth
  readiness issues.
- Predictive usefulness, economic significance, profitability, broker
  readiness, and execution capability remain unaccepted.

## Next Phase

Convert selected operator surfaces, including Studio, into explicit canonical
lineage drivers where appropriate, without changing Strategy semantics or
promoting historical reports. Data-remediation and research protocol work must
remain separate from artifact-lineage acceptance.

## Final Acceptance Statement

Artifact Lineage v1 writing is accepted for new canonical runs.

Legacy reports are not migrated.

No predictive validity is established.

No profitability is established.

No broker or execution functionality exists.

The research protocol remains blocked.
