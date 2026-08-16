# MarketFlow Additional Predictive Evidence Execution for Refined Evidence Status

## Branch And Scope

- Branch: `feature/additional-predictive-evidence-execution-refined-evidence-v1`.
- Base commit: `96a4b83720fad948fa9664f33f66fcf18d1b85a8`.
- Commit: recorded by this document's implementing commit after validation.
- Scope: offline, research-only binding and reassessment of already reviewed refined evidence. No provider, acquisition, canonical generation, source refinement rerun, acceptance, profitability, runtime, strategy, paper, broker, or recommendation authority is created.

## Execution Artifact

- Artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE` / `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY`.
- Schema: `additional_predictive_evidence_executed_for_refined_evidence_v1`.
- Execution digest: `9cf962933620f066dfb105845428a262743f9f36dbc2850838321f23de10b5fd`.
- Run timestamp: `2026-08-16T16:00:00Z`.
- Failures/warnings: `0 / 1`; the warning preserves META's reduced record count.

## Bound Source Evidence

- Execution approval digest: `5ad7b3b8df3156ab6b35b9490dcd4ae05bda3d1a7786212481b78d549103a8dd`.
- Candidate review/candidate digests: `5cee77990a1f40689ee45ab2f65e2adda070e79970e12d52169f7e88236f6e04` / `dce3a92d05eaba5c2b9307c08799c27bbadb69e804c27c157c7290eec705c340`.
- Feature/label refinement results-review/execution digests: `00604008d3c647f45896cd8b6707de519ed6eda4e32566b3c99910441ec6cc79` / `377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36`.
- Feature/label refinement execution approval digest: `1b98237ae9156875ca703396b6e1fabf2acf31ab607789247f8af2391d8b5c20`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical freeze/records digests: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset And Universe

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Profile/timeframe/range: `RTH_FULL_SESSION_1D` / `1d` / `2022-01-01` through `2025-12-31`.
- Exact universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Total records: `11946`; META remains exactly `913`, and every other ticker remains exactly `1003`.
- Data quality: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.

## Refined Evidence Source Profile

- Source root: `.marketflow/feature_label_refinement/expanded_universe_v1/`.
- Required source outputs: `12`; all were present.
- All eleven non-self source hashes matched the reviewed digest manifest.
- Self-reference policy: `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.
- Frozen canonical records were read only for hash/count verification and were not mutated.

## Refined Evidence Facts And Input Binding

- Binding status: `BOUND_REVIEWED_REFINED_EVIDENCE`; label/feature status: `BOUND_NOT_REGENERATED`.
- Labels: 7 families, 84 coverage entries, 82,698 available and 924 unavailable values; digest `04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8`.
- Features: 9 groups, 11 categories, 19 fields, 11,946 rows, and 1,128 null/unavailable values; digest `35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00`.
- Features use current/historical information only; future labels are not used as features.

## Refined Walk-Forward Reassessment

- Status: `ASSESSED_FROM_REVIEWED_SOURCE_NOT_RERUN`.
- Four folds and 3,024 evaluation rows were bound from existing evidence.
- Q1/Q2/Q3/Q4 rows: `732 / 756 / 768 / 768`; every fold keeps one embargo session and shuffle disabled.
- Fold accuracy ranges: `0.133880–0.501366`, `0.146825–0.460317`, `0.125000–0.492188`, and `0.140625–0.427083`.

## Refined OOS And Model Reassessment

- OOS status: `ASSESSED_FROM_REVIEWED_SOURCE_NOT_RERUN`; window `2025-01-01` through `2025-12-31`.
- Seven deterministic comparisons each bind 2,988 OOS rows; observed accuracy range `0.119813 to 0.480924`.
- Five model-comparison groups are preserved. Three unavailable family requests remain `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`; no value was fabricated.
- Model comparison remains explicitly not acceptance evidence.

## Calibration, Stability, Leakage, And Quality

- Calibration/stability status: `REVIEWED_FROM_EXISTING_REFINED_METRICS`; the source conclusion remains `NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED`.
- Leakage/quality status: `REVIEWED_FROM_EXISTING_REFINED_EVIDENCE`.
- Protocol: 6 groups, chronological splits, one-session embargo, no shuffle, and no lookahead.
- Leakage: `PASS`, with `0` failed controls.
- Data quality: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`, `0` failures, and the single META limitation warning.

## Generated Outputs And Digest Manifest

- Ignored output root: `.marketflow/additional_predictive_evidence_refined/expanded_universe_v1/`.
- Generated output count: `10`.
- Outputs: execution manifest, input manifest, label/feature binding manifest, walk-forward report, OOS report, baseline/model report, calibration/stability report, leakage/quality report, digest manifest, and operator summary.
- All nine non-self output SHA-256 values match the generated digest manifest; its own entry uses `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.
- Every output is `RESEARCH_ONLY_NON_ACTIONABLE`, `NOT_ACCEPTANCE_EVIDENCE`, `NOT_PROFITABILITY_EVIDENCE`, and `NOT_RUNTIME_AUTHORITY`.

## Execution And Authority Boundaries

- Approval/authorization/ready/executed/results created: `True / True / True / True / True` for this refined-evidence research execution only.
- Refined input binding, walk-forward, OOS, baseline/model, calibration/stability, and leakage/quality assessment states are `True`.
- Provider requests, live transport, acquisition, dataset generation/regeneration, feature/label rerun, refined label/feature rerun, source validation rerun, source metric recomputation, and source model-comparison rerun: all `False`.
- Predictive usefulness: `not accepted`; readiness/recommendation/candidate: `False / False / False`.
- Profitability: `not accepted`; readiness/recommendation: `False / False`.
- Runtime migration approved/active: `False / False`.
- Runtime/strategy/paper/broker: all `NOT_AUTHORIZED`; stitching, strategy scoring, and trade recommendations are `False`.
- No API key or raw provider payload was accessed, stored, printed, or committed.

## Non-Goals And Next Task

- This execution is not predictive-usefulness acceptance, profitability acceptance, runtime migration, strategy activation, paper trading, broker execution, or trade recommendation generation.
- Next task recommendation: `Additional Predictive Evidence Results Review for Refined Evidence v1`.
