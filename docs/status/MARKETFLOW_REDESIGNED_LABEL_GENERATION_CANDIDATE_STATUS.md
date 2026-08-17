# MarketFlow Redesigned Label Generation Candidate Status

## Branch And Scope

- Branch: `feature/redesigned-label-generation-candidate-v1`.
- Base/source review commit: `bc7ac4cb24ad326dec5afbe9c37898fce552d5b3`.
- Scope: deterministic, offline construction of a candidate package for future redesigned-label generation from reviewed design artifacts.
- This candidate is planning-only. It does not approve or perform label generation.

## Candidate Artifact

- Artifact/status: `REDESIGNED_LABEL_GENERATION_CANDIDATE` / `REDESIGNED_LABEL_GENERATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Schema: `redesigned_label_generation_candidate_v1`.
- Candidate digest: `6ef5c93b660e2f2ad825a774299e3dae1adc3041a1f619f7b3df0001c18f5a08`.
- Candidate created/ready for operator review: `True / True`.
- Candidate review created: `False`.
- Ready for approval/execution: `False / False`.
- Checklist: `46 / 46` passed, `0` failed, `0` blockers.

## Bound Evidence

- Label-objective redesign results-review digest: `bda6012c74cffb8841a6b9568c0985e2b6d1c337c7b7fcf892da4b724fcb15f9`.
- Execution digest: `d43bb214850f8068b445d1620ae8f4f948162eda309f04acf6fdd7b73abd63a4`.
- Execution approval digest: `8ca1dee0aa2c175a1ab5bf7f9ba724b8dc0df6e2057e4f97721bad02f4adaff0`.
- Execution-candidate review/candidate digests: `88297ae3b63a14edf17a4b5c069c1360101999a003592f68e87bbd5af498d6f1` / `92171d443cb676425a73dbdf484040f55a19371c5c0713b70e5ea6f37742b63d`.
- Redesign approval digest: `71cd46568009929a37afb2936d32ca6d9fb097c6c51a1cccf84af1bfc8eb0185`.
- Operator method-selection digest: `2f771999ff5e31dbd959ea1a33b08852cda46913ff1b5dfc6fe17bc0853ee14a`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical-records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Dataset And Universe

- Dataset/source profile/timeframe: `expanded_universe_canonical_dataset_v1` / `RTH_FULL_SESSION_1D` / `1d`.
- Date range: `2022-01-01` through `2025-12-31`.
- Exact universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Records: `11946` total; META remains `913`; every non-META ticker remains `1003`.
- META's reduced count remains explicit and unmodified, with no backfill or synthetic labels.

## Candidate Objective And Source Profile

- Objective: `PREPARE_REDESIGNED_LABEL_GENERATION_CANDIDATE_FROM_REVIEWED_LABEL_OBJECTIVE_REDESIGN_OUTPUTS`.
- Scope/mode/authority: `CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION` / `PLANNED_NOT_GENERATED` / `NOT_AUTHORIZED`.
- All eight source design artifacts remain `SOURCE_REVIEWED_NOT_REGENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Source counts: 10 label families, seven threshold strategies, five horizon strategies, and 12 per-ticker plans.
- Interpretation remains `DESIGN_ARTIFACTS_READY_FOR_OPERATOR_REVIEW`, `NOT_GENERATED_NOT_AUTHORIZED`, and `NOT_ACCEPTANCE_EVIDENCE`.

## Planned Redesigned Label Families

- Ten planned families cover flat-zone direction, redesigned return buckets, multi-horizon targets, benchmark-relative and volatility-adjusted returns, drawdown avoidance, asymmetric risk/reward, regime-conditioned direction, per-ticker calibration, and a no-trade-zone class.
- Every family is `PLANNED_NOT_GENERATED`; authorization, generation, and actual label values remain false.

## Planned Threshold And Horizon Strategies

- Seven threshold strategies are `PLANNED_NOT_COMPUTED`; threshold computation is neither authorized nor performed.
- Five horizon strategies are `PLANNED_NOT_COMPUTED`; horizon selection is neither authorized nor performed.
- All strategies are research-only and non-actionable.

## Planned Availability Rules

- Eight candidate-only rules preserve training-window-only fitting, null forward tails, no-peek generation, late-window boundaries, META's record limitation, no synthetic rows, no backfill, and no calendar inference.
- Every rule is `PLANNED_FOR_OPERATOR_REVIEW` and `NOT_EXECUTED`.

## Per-Ticker Candidate Entries

- Twelve entries preserve the exact registry-approved order and frozen record counts.
- Each entry is `PLANNED_READY_FOR_OPERATOR_REVIEW` and binds the source results-review digest plus a deterministic per-ticker candidate digest.
- Redesigned label generation remains unauthorized and unperformed for every ticker.

## Planned Outputs

- Eight output definitions are recorded, including the future generation manifest, selection matrices/plans, per-ticker plan, META handling plan, and operator-summary template.
- Every output remains `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Future Chain And Gates

1. Redesigned Label Generation Candidate Operator Review Package v1.
2. Redesigned Label Generation Approval v1, if selected.
3. Redesigned Label Generation Execution v1.
4. Redesigned Label Generation Results Review v1.
5. Feature or predictive-evidence planning using redesigned labels, if results support it.
6. Separately selected and approved additional predictive-evidence execution and results review.
7. Predictive-usefulness reassessment/readiness only after new evidence.
8. A predictive-usefulness acceptance candidate only if readiness passes.
9. Separate profitability and runtime chains, if ever required and authorized.

All 13 requested gates are recorded and remain separate; none after candidate creation is opened here.

## Risk Controls And Authority Boundary

- All 16 requested controls are recorded, including no label generation, feature generation, predictive-evidence execution, acceptance, profitability approval, runtime, strategy use, paper trading, broker execution, recommendations, dataset mutation, META repair, or generation without operator approval.
- Predictive usefulness/profitability remain `not accepted / not accepted`.
- Runtime/strategy/paper/broker remain `NOT_AUTHORIZED`; trade recommendations remain false.
- No provider request, `.env` access, live transport, acquisition, dataset regeneration, execution rerun, label or feature generation, metric recomputation, model training, strategy scoring, runtime activation, or trading action occurred.

## Next Task

- `Redesigned Label Generation Candidate Operator Review Package v1` remains the next separate task.
- This candidate does not create its review package and does not imply approval or execution.
