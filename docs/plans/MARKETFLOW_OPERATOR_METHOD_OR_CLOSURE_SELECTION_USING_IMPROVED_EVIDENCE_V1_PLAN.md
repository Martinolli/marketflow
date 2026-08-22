# MarketFlow Operator Method or Closure Selection Using Improved Evidence v1 Plan

## Purpose

Record a single offline, guarded, digest-bound operator selection over the completed not-ready closure and method-planning tree. This plan selects Option A and closes or pauses the current predictive-usefulness acceptance path for the current dataset/evidence set. It creates only the selection artifact.

## Source Closure Artifact

- Artifact: `PREDICTIVE_USEFULNESS_NOT_READY_CLOSURE_AND_METHOD_PLANNING_TREE_USING_IMPROVED_EVIDENCE`.
- Status: `PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_CLOSED_NOT_READY_CURRENT_IMPROVED_EVIDENCE`.
- Decision: `CLOSE_CURRENT_ACCEPTANCE_PATH_AND_REQUIRE_OPERATOR_METHOD_SELECTION`.
- Digest: `ca179fdfe2fcc3c1572339d7e35f8f201177d59d3b7fa5dc245b58620987cbda`.
- The source closure and its complete bound evidence chain remain immutable and are not rerun.

## Dataset and Universe

Use `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, from `2022-01-01` through `2025-12-31`. Preserve the exact order `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`, the `11946` total records, META's `913` records, and `1003` records for each other ticker.

## Selection Basis

The source readiness decision is `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_IMPROVED_EVIDENCE`. The local model equals the majority baseline at `0.58626033`; cross-sectional accuracy is `0.58935950`, only `0.00309917` above the majority baseline; optional tree and ensemble coverage is unavailable; and majority-structure risk requires operator review. Eight leakage controls pass, but tooling integrity does not establish predictive usefulness or profitability.

## Operator Attestation

Require the exact non-secret attestation phrase and confirmations defined by the service. The attestation must bind the closure, readiness, and records digests; ordered universe/counts; Option A; selection-only scope; archive readiness; and every closed authority. Missing or changed bindings fail closed. Tests may use `TEST_OPERATOR`; real operator use must supply its own exact attestation. No credential, API key, broker detail, tax detail, or personal financial information is required.

## Selected Option

- Scope: `OPERATOR_METHOD_OR_CLOSURE_SELECTION_ONLY`.
- Option: `OPTION_A_STOP_ACCEPTANCE_PATH_CURRENT_DATASET`.
- Decision: `SELECT_STOP_ACCEPTANCE_PATH_CURRENT_DATASET`.
- Rationale: `CURRENT_IMPROVED_EVIDENCE_NOT_READY_SMALL_EDGE_LOCAL_MODEL_MATCHES_MAJORITY_OPTIONAL_MODEL_COVERAGE_INCOMPLETE`.

## Selection Options Review

- Select Option A, matching the source recommendation.
- Keep Options B through F unselected future research options.
- Keep Option G an unselected future governance option.
- Keep Option H `NOT_ALLOWED_CURRENTLY`.

## Next Artifact

Set `PREDICTIVE_USEFULNESS_ACCEPTANCE_PATH_ARCHIVE_RECORD_USING_IMPROVED_EVIDENCE` as the separately gated next artifact and set readiness for that artifact true. Do not create the archive record in this task.

## Future Chain

1. Create the separate predictive-usefulness acceptance-path archive record using improved evidence.
2. Require a separate operator decision before optional future method/evidence work.
3. Require separate selection, review, and approval before any future evidence candidate.
4. Permit reassessment only after new evidence exists.
5. Permit acceptance-readiness rerun only after new reassessment.
6. Permit an acceptance candidate only if future readiness passes.
7. Permit profitability review only after a separate predictive-usefulness acceptance chain.
8. Permit runtime migration only if separately authorized.

## Future Gates

Maintain the nine service-defined gates for the archive record; future operator method selection; optional method/evidence candidate; future evidence review/approval/execution; reassessment; readiness; acceptance candidacy; profitability; and runtime migration.

## Risk Controls

Maintain all 30 service-defined controls. They prohibit this selection from creating downstream artifacts or authority, preserve all frozen and reviewed source outputs and META's reduced record count, and retain research-only scope.

## Non-Goals

This task does not create an archive record, future method/evidence candidate, evidence execution candidate or execution, reassessment, readiness rerun, acceptance candidate, predictive-usefulness acceptance, profitability acceptance, runtime migration, strategy activation, paper trading, broker execution, or trade recommendation. It does not acquire or regenerate data, labels, targets, features, or matrices and does not recompute metrics or train models.

## Guardrails

Run entirely offline. Do not call providers, inspect `.env`, enable live transport, modify `.marketflow`, mutate source artifacts, store or print API keys, commit raw provider payloads, or touch broker/IBKR code. Default tests remain deterministic and credential-free.

## Next Task

`Predictive Usefulness Acceptance Path Archive Record Using Improved Evidence v1` is the next separately authorized task.
