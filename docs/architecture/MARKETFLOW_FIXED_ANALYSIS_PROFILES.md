# MarketFlow Fixed Analysis Profiles

Status: NORMAL MODE CONTRACT

## Profiles

| Field | SWING | POSITION_SWING |
| --- | --- | --- |
| Profile ID | `SWING` | `POSITION_SWING` |
| Candidate timeframe | `4h` | `1d` |
| Minimum valid OHLCV rows | `390` | `560` |
| Intended holding concept | `SEVERAL_TRADING_DAYS` | `SEVERAL_DAYS_TO_WEEKS` |
| Higher-timeframe context | `NOT_IMPLEMENTED` | `NOT_IMPLEMENTED` |
| Automatic Monte Carlo | `false` | `false` |
| Automatic outcome evaluation | `false` | `false` |

## Contract Version And Digest

The fixed profile contract has a deterministic versioned digest over:

- profile version;
- profile ID;
- candidate timeframe;
- minimum valid rows;
- intended holding concept;
- higher-timeframe context status;
- automatic Monte Carlo status;
- automatic outcome-evaluation status.

The digest excludes ticker, local paths, current date, run ID, artifact ID,
report formatting, credentials, account data, and outcomes.

## Normal Orchestration

The normal orchestrator accepts exactly one ticker and resolves one local
canonical annotated source per profile under the repository-controlled
`.marketflow/reports` root. A profile with exactly one valid source and
sufficient valid rows creates its own Artifact Lineage v1 run, commits an
`ANNOTATED_DATASET` artifact, and commits a `CANDIDATE_CORE` artifact only when
the canonical candidate builder returns a valid rank/action-eligible core.

Each profile is independent. Runs, candidates, scores, event context, target,
stop, RR, evidence state, MC summaries, and plots are not shared across
profiles.

## Data Resolution

Resolution is exact by ticker plus candidate timeframe under the approved
local report root. Raw CSVs and generated derivative CSVs are not normal-mode
sources. Duplicate canonical annotated identities fail closed as
`DATASET_IDENTITY_AMBIGUOUS`. Missing identities fail as
`DATASET_NOT_FOUND`. Invalid sources fail as `DATASET_INVALID`.
Insufficient valid OHLCV rows fail as `INSUFFICIENT_HISTORY`.

No provider download, timestamp/latest selection, first glob match,
modification-time choice, ticker-only fallback, timeframe-only fallback,
automatic duplicate remediation, or source outside the approved root is
allowed.

## Non-Authority Boundaries

Normal mode does not expose timeframe, period/history, primary timeframe,
ATR length, stop multiplier, minimum RR, event-age limit, PnF enablement,
Monte Carlo enablement, component weights, thresholds, profile selection,
optimization, or execution.

Monte Carlo is not automatic because SWING and POSITION_SWING horizons have not
been approved through the research protocol. Outcome evaluation is not
automatic. Candidate-only plotting is deferred.

Existing parameterized scripts and Studio controls are advanced/research or
legacy surfaces and do not define the normal fixed-profile contract.
