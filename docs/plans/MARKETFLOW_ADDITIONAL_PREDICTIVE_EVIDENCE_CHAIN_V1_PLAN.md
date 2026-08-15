# MarketFlow Additional Predictive Evidence Chain v1 Plan

## Purpose

Define an offline, deterministic, digest-bound plan for future additional predictive evidence over the registry-approved expanded universe. This plan creates only an operator-review candidate; it does not authorize or execute predictive work.

## Source Research Registry Approval

- Approval artifact/scope: `RESEARCH_REGISTRY_APPROVED` / `RESEARCH_REGISTRY_APPROVAL_ONLY`.
- Approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Candidate review/candidate digests: `5ec5c7a36787963e14e23494cee7fad54a4d072d613b06dccc1e43792d94b267` / `e62cbf4ccfbf6377f64c92ed39d1c300188f0b9923e7f8da74827db2149b7865`.
- Frozen dataset/generation/records digests: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc` / `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset: `expanded_universe_canonical_dataset_v1`.
- Scope/profile: `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `RTH_FULL_SESSION_1D`.
- Range/timeframe: `2022-01-01` through `2025-12-31` / `1d`.
- Universe/record count: `12 / 11946`.
- Quality/label/status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION` / `RESEARCH_ONLY_NON_ACTIONABLE` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.

## Target Universe

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- META remains exactly `913` records; every other ticker remains exactly `1003`.

## Planned Label Families

- `NEXT_BAR_DIRECTION`
- `NEXT_BAR_RETURN_BUCKET`
- `NEXT_SESSION_DIRECTION`
- `NEXT_SESSION_RETURN_BUCKET`
- `MULTI_HORIZON_RETURN_BUCKET`
- `VOLATILITY_REGIME_LABEL`
- `DRAWDOWN_RISK_LABEL`

All labels remain `PLANNED_NOT_GENERATED`, `NOT_AUTHORIZED_FOR_EXECUTION`, and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Planned Feature Families

- `ohlcv_return_features`
- `volume_price_features`
- `volatility_features`
- `trend_momentum_features`
- `wyckoff_vpa_features`
- `corporate_action_context_features`
- `cross_ticker_relative_strength_features`
- `calendar_session_features`
- `data_quality_flags`
- `meta_reduced_record_count_flag`

All features remain `PLANNED_NOT_GENERATED`, `NOT_AUTHORIZED_FOR_EXECUTION`, and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Planned Evaluation Protocol

- Chronological split and walk-forward policies.
- Out-of-sample holdout with no shuffling.
- Forward-only labels, leakage prevention, and baseline comparison.
- Stability review and operator review before execution.
- Every protocol item remains `PLANNED_NOT_EXECUTED`.

## Future Predictive Evidence Chain

1. Candidate operator review package.
2. Execution candidate.
3. Execution approval ceremony, if required.
4. Execution.
5. Results review package.
6. Predictive usefulness reassessment candidate and review package.
7. Predictive usefulness acceptance readiness review and a separate ceremony only if evidence is sufficient.
8. Separate profitability and runtime-migration chains only if later required and authorized.

## Future Gates

The twelve named gates in the candidate keep operator review, execution candidacy, execution approval, execution, results review, usefulness reassessment, usefulness acceptance, profitability review, and runtime migration distinct. Planning does not satisfy any gate.

## Risk Controls

- No predictive execution, labels, features, walk-forward validation, or OOS evaluation without separate approval.
- No usefulness acceptance without results review and no profitability acceptance without separate review.
- No runtime source switch, automatic stitching, trading, or trade recommendations.
- Preserve META's reduced count and never mutate the frozen canonical dataset.
- Label all outputs research-only; commit no raw provider payloads; store or print no API keys.

## Non-Goals

- Provider calls, market-data acquisition, dataset regeneration, label/feature generation, predictive execution, strategy scoring, trading recommendations, predictive/profitability acceptance, and runtime activation.
- Changes to default dataset selection, Strategy runtime, paper/broker execution, or IBKR code.

## Guardrails

- Default behavior and tests remain deterministic and offline.
- Candidate outputs are canonical, digest-bound, research-only, and no-overwrite.
- The frozen records and exact ticker order are inputs, never repaired or inferred facts.

## Implementation Progress

- Additional Predictive Evidence Chain Candidate v1 is complete.
- Additional Predictive Evidence Chain Candidate Operator Review Package v1 is implemented.
- The chain candidate is reviewed, and the review remains digest-bound source evidence.
- Additional Predictive Evidence Execution Candidate v1 is implemented and remains non-authorizing.
- Profitability remains `not accepted`; runtime activation remains future and separate.

## Next Tasks

1. Additional Predictive Evidence Execution Candidate Operator Review Package v1 remains future work.
2. Additional Predictive Evidence Execution Approval Ceremony v1 remains future work, if required.
3. Additional Predictive Evidence Execution v1 remains future work.
4. Additional Predictive Evidence Results Review Package v1 remains future work.
5. Predictive Usefulness Reassessment Candidate v1 remains future work.
