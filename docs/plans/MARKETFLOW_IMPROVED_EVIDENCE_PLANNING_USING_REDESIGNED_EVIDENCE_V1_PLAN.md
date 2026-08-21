# MarketFlow Improved Evidence Planning Using Redesigned Evidence v1 Plan

## Purpose

Define a deterministic, offline, candidate-only plan for possible future improved evidence around the selected no-trade/abstain label-objective redesign. This document creates no approval or execution authority.

## Source Label Objective Redesign Results Review

- Source artifact/status: `LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE` / `LABEL_OBJECTIVE_REDESIGN_RESULTS_REVIEW_PACKAGE_USING_REDESIGNED_EVIDENCE_READY`.
- Source digest: `6bbf7af2ae72e33dbc0a86da2b8ba8faa05edeea982baea89c6b511b3cd7d1f4`.
- Selected direction: `REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS`.
- Decision boundary: `NO_LABEL_REGENERATION_OR_NEW_TARGETS_AUTHORIZED`.

## Dataset And Universe

- Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, `1d`, `2022-01-01` through `2025-12-31`, and records digest `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Preserve exact order: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- Preserve 11,946 total rows, META at 913, and every other ticker at 1003. Do not repair, infer, normalize, or fabricate META rows.

## Candidate Basis

- The source review and redesign are `COMPLETED_RESEARCH_ONLY`.
- The no-trade/abstain, material-move, horizon, ticker/regime, risk-adjusted, label-family, and acceptance-prerequisite paths still require operator selection.
- FLAT majority structure requires operator review; the small cross-sectional edge is not acceptance evidence.
- This candidate prepares planning structure only. It does not select a design or convert source findings into authority.

## Improved Evidence Themes

Plan future operator consideration of the 11 frozen themes declared by `IMPROVED_EVIDENCE_THEME_IDS`: no-trade/abstain label design, material-move target design, class balance and coverage, horizon validation, ticker/regime validation, risk adjustment, feature-label alignment, baseline outperformance policy, calibration/confidence, META limitation handling, and acceptance-readiness prerequisites. Every theme remains `PLANNED_NOT_EXECUTED`.

## Planned Evidence Components

Plan the 13 components declared by `PLANNED_EVIDENCE_COMPONENT_IDS`, including schema and coverage analysis, threshold and horizon plans, ticker/regime evaluation, feature-label alignment, chronological split/embargo, baseline and cross-sectional comparison, calibration/Brier review, leakage/no-peek controls, per-ticker/META reporting, and an operator results-review template. No component is authorized or executed.

## Planned Data Products

The 13 declared templates and manifest remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`. They describe future structure only; the candidate does not materialize label, feature, matrix, metric, model, or predictive-evidence outputs.

## Planned Future Outputs

The 12 declared future outputs remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`, including future execution, schema, matrix, walk-forward, OOS, baseline, metric, calibration, leakage-control, per-ticker/META, operator-review, and digest-manifest outputs.

## Future Chain

1. Candidate operator review using redesigned evidence.
2. Planning approval, if selected in a separate task.
3. Planning execution, if separately approved.
4. Planning results review.
5. Additional predictive-evidence execution candidate, if supported.
6. Additional predictive-evidence approval and execution, if separately approved.
7. Predictive-usefulness reassessment and acceptance-readiness reruns only after new evidence exists.
8. Predictive-usefulness acceptance candidate only if readiness passes.
9. Profitability and runtime chains only if separately governed.

## Future Gates

The service records the explicit `NEXT_GATES` sequence. Every gate after candidate creation remains closed. Operator review is the only immediate next gate and creates no approval or execution by itself.

## Risk Controls

- Preserve all `RISK_CONTROLS` in the candidate artifact.
- Do not call providers, inspect `.env`, enable transport, acquire data, mutate frozen outputs, regenerate labels/features, create targets or matrices, rerun evidence, recompute metrics, train models, or score strategies.
- Do not accept predictive usefulness or profitability and do not authorize runtime, strategy, paper trading, broker execution, recommendations, or trading.
- Preserve research-only, non-actionable labels and META's 913-row limitation.

## Non-Goals

This plan is not a planning review, selection, approval, execution, results review, predictive-evidence candidate, predictive execution, usefulness acceptance, profitability review, runtime migration, or trading feature.

## Guardrails

Default validation remains deterministic and offline. Candidate and per-ticker digests must be canonical and stable. Tests write only to pytest temporary directories, and `.marketflow` files must remain untracked.

## Next Task

`Optional Improved Evidence Planning Candidate Operator Review Using Redesigned Evidence v1`.
