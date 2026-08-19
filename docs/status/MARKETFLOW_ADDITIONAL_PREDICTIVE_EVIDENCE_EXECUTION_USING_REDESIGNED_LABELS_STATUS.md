# MarketFlow Additional Predictive Evidence Execution Using Redesigned Labels Status

## Branch And Execution

- Branch/base: `feature/additional-predictive-evidence-execution-redesigned-labels-v1` / `7241c861f42eb1accd9c4380c50871ca76555368`.
- Artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS` / `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_REDESIGNED_LABELS_RESEARCH_ONLY`.
- Fixed run timestamp: `2026-08-19T16:30:00Z`.
- Execution digest: `8d70be25979c7e7d8ffeedd5a6ee8f0e69c5f1015d186f39196a23ded6cf081b`.
- Feature/label matrix digest: `275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad`.
- Checklist: `36 / 36` passed, `0` failed, `0` blockers.

## Source Approval And Evidence

- Execution approval digest: `cc45d6692f1f249cc76554f7019f148c8510efedeade22adb3ccb3fcbc54fe96`.
- Candidate review/candidate digests: `dc4ae33cd0f40d84de33ce7e195d35696443fa5cd5dcb52dee4ce0c649ac06ec` / `f11550ab63f21f2f08b896296324e0f0b1cb99a27ae186cfc347028e5ddf9cd5`.
- Feature results review/execution/values digests: `e46bbd76b895a9513d338b415cef364baf778fe5ade67128a069631ae2bbbda3` / `d44e11b32dc8ba82ec0cdbf431397762dec56f9fd9323bf66f0571c39d82ca7f` / `63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1`.
- Redesigned-label values and canonical-record digests: `2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Post-execution hashing confirmed that canonical, redesigned-label, and feature source files remained byte-for-byte unchanged.

## Dataset And Matrix

- Dataset/profile/timeframe/range: `expanded_universe_canonical_dataset_v1` / `RTH_FULL_SESSION_1D` / `1d` / `2022-01-01` through `2025-12-31`.
- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Canonical records: `11946`; META remains `913`, every other ticker remains `1003`.
- Redesigned labels: `143352` rows, `142200` available, `1152` unavailable.
- Features: `203082` rows, `190848` available, `12234` unavailable, covering the 17 reviewed feature groups.
- Matrix: `143352` rows; `142200` evaluable; `1152` unavailable targets retained as null and excluded from training and metrics.
- Target values, forward returns, and threshold values are kept outside feature inputs.

## Chronological Protocol And Leakage Controls

- Training window: `2022-01-01` through `2023-12-31`.
- Validation: expanding-window quarterly folds `2024-Q1` through `2024-Q4`.
- OOS holdout: `2025-01-01` through `2025-12-31`.
- Shuffling is prohibited. A horizon-aware training embargo excludes any label whose forward outcome was unresolved at the applicable fold/OOS cutoff.
- Leakage status: `PASS`; failed controls: `0`.
- No future labels, `forward_return`, `label_value`, or `threshold_value_used` entered any feature vector.

## Walk-Forward Results

| Fold | Training | Evaluation | Majority | Previous known direction | Ticker cross-sectional | Regularized local model |
|---|---:|---:|---:|---:|---:|---:|
| 2024-Q1 | 69912 | 8784 | 0.66507286 | 0.58515483 | 0.69945355 | 0.66507286 |
| 2024-Q2 | 78696 | 9072 | 0.67482363 | 0.54982363 | 0.67250882 | 0.67482363 |
| 2024-Q3 | 87768 | 9216 | 0.57063802 | 0.46896701 | 0.58572049 | 0.57063802 |
| 2024-Q4 | 96984 | 9216 | 0.61881510 | 0.49728733 | 0.61555990 | 0.61881510 |

All values are aggregated research-only accuracies across heterogeneous label families; they are not acceptance or profitability evidence.

## OOS Holdout Results

| Method | Accuracy | Macro F1 | Brier score |
|---|---:|---:|---:|
| Majority class | 0.58626033 | 0.21557412 | 0.04867526 |
| Previous known direction | 0.47319789 | 0.30751393 | 0.06197672 |
| Buy/hold reference only | 0.28437787 | 0.11974993 | 0.08419084 |
| Ticker cross-sectional | 0.58935950 | 0.28155252 | 0.04831065 |
| Regularized local model | 0.58626033 | 0.21557412 | 0.04867526 |

- OOS training/evaluation rows: `106200` / `34848`.
- The deterministic dependency-free regularized model did not outperform the majority or ticker-cross-sectional baselines in aggregate OOS accuracy.
- These results do not accept or establish predictive usefulness.

## Models, Metrics, And Outputs

- Four required baselines were evaluated.
- `MODEL_FAMILY_REGULARIZED_LINEAR` used a deterministic shrunk nearest-centroid linear score and was evaluated research-only.
- Per-ticker and global comparison reports were evaluated.
- Optional tree and ensemble families are `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`; no dependency was installed. These produce two non-blocking warnings.
- All ten required metric families were computed and labeled `RESEARCH_ONLY_NON_ACTIONABLE`, `NOT_PREDICTIVE_USEFULNESS_ACCEPTANCE`, `NOT_PROFITABILITY_EVIDENCE`, and `NOT_RUNTIME_AUTHORITY`.
- Thirteen ignored outputs were created under `.marketflow/additional_predictive_evidence_using_redesigned_labels/expanded_universe_v1/`.
- The digest manifest contains 13 entries; all 12 non-self file hashes were verified, with an explicit self-reference exception for the digest manifest.

## Authority Boundary

- Predictive evidence execution, research-only metric computation, and deterministic local model evaluation are complete.
- Predictive usefulness remains `not accepted`; acceptance readiness/recommendation/candidate creation remain false.
- Profitability remains `not accepted`.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- New strategy scoring and trade recommendations remain false.
- No provider request, `.env` inspection, live transport, market-data acquisition, dataset generation, canonical regeneration, label regeneration, feature regeneration, runtime activation, broker action, or trading action occurred.

## Next Gate

- Follow-on `Additional Predictive Evidence Results Review Using Redesigned Labels v1` is implemented as a separate offline, digest-bound review package.
- This execution remains source evidence; the results review does not accept predictive usefulness, approve profitability, or authorize runtime.
- Predictive-usefulness reassessment remains future and separately gated after results review.
