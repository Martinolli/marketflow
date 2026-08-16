# MarketFlow Additional Predictive Evidence Results Review for Refined Evidence Status

## Branch And Scope

- Branch: `feature/additional-predictive-evidence-results-review-refined-evidence-v1`.
- Base commit: `5f4ba0aa775a487295c611cdc69fe812db92cf54`.
- Commit: recorded by this document's implementing commit after validation.
- Scope: offline, digest-bound inspection of the ten existing refined-evidence execution outputs. This review creates no source execution, predictive-usefulness reassessment review, acceptance, profitability, runtime, strategy, paper, broker, scoring, or recommendation authority.

## Review Artifact And Status

- Artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE` / `ADDITIONAL_PREDICTIVE_EVIDENCE_RESULTS_REVIEW_FOR_REFINED_EVIDENCE_PACKAGE_READY`.
- Schema: `additional_predictive_evidence_results_review_for_refined_evidence_v1`.
- Review digest: `539d06be9b20edee5ff883030e4fd1091fdaefb468fa595001178bf7ec0740da`.
- Checklist: `86 / 86` checks passed, `0` failed, and `0` blockers.
- Result state: review created/ready and ready for the separate Predictive Usefulness Reassessment Review Rerun Using Refined Evidence v1.

## Bound Source Evidence

- Refined-evidence execution artifact/status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE` / `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_FOR_REFINED_EVIDENCE_RESEARCH_ONLY`.
- Refined-evidence execution digest: `9cf962933620f066dfb105845428a262743f9f36dbc2850838321f23de10b5fd`.
- Refined-evidence execution approval digest: `5ad7b3b8df3156ab6b35b9490dcd4ae05bda3d1a7786212481b78d549103a8dd`.
- Refined-evidence candidate review/candidate digests: `5cee77990a1f40689ee45ab2f65e2adda070e79970e12d52169f7e88236f6e04` / `dce3a92d05eaba5c2b9307c08799c27bbadb69e804c27c157c7290eec705c340`.
- Feature/label refinement results-review/execution digests: `00604008d3c647f45896cd8b6707de519ed6eda4e32566b3c99910441ec6cc79` / `377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical freeze/records digests: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Source profile/timeframe/range: `RTH_FULL_SESSION_1D` / `1d` / `2022-01-01` through `2025-12-31`.
- Registry label/data quality: `RESEARCH_ONLY_NON_ACTIONABLE` / `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Total canonical records: `11946`; records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Target Universe And Per-Ticker Records

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- `MSFT 1003`; `NVDA 1003`; `AMZN 1003`; `GOOGL 1003`; `META 913`; `TSLA 1003`.
- `JPM 1003`; `XOM 1003`; `JNJ 1003`; `WMT 1003`; `CAT 1003`; `LMT 1003`.
- META's exact `913` records are preserved as a source limitation; no record was repaired, inferred, backfilled, normalized, or fabricated.

## Refined Evidence Input Binding Review

- The reviewed input binding is available and bound to the saved execution outputs.
- Labels: `7` families, `84` coverage entries, `82698` available values, `924` unavailable values; digest `04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8`.
- Features: `9` groups, `11` categories, `19` fields, `11946` rows, `1128` null/unavailable values; digest `35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00`.

## Refined Walk-Forward And OOS Reassessment Review

- Protocol: `6` groups with chronological splits, one-session embargo, no shuffle, and no lookahead.
- Walk-forward: `4` folds and `3024` evaluation rows, inspected from existing outputs without rerun.
- OOS: `2988` evaluation rows and observed accuracy range `0.119813 to 0.480924`.
- Interpretation: `WEAK_OR_MIXED_REQUIRES_REASSESSMENT_REVIEW` and `LOW_TO_MIXED_NOT_ACCEPTANCE_EVIDENCE`.

## Refined Baseline, Model, Calibration, Stability, Leakage, And Quality Review

- Model comparison: `5` groups, `7` deterministic comparisons, and `3` unavailable model-family requests.
- Unavailable status: `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`; no unavailable result was fabricated.
- Model interpretation: `RESEARCH_ONLY_REQUIRES_OPERATOR_REVIEW`.
- Calibration/stability interpretation: `NOT_ACCEPTANCE_EVIDENCE_UNTIL_REVIEWED`.
- Leakage: `PASS` with `0` failed controls.
- Data quality: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.

## Generated Output Inspection And Digest Manifest

- Ignored output root: `.marketflow/additional_predictive_evidence_refined/expanded_universe_v1/`.
- All `10` expected JSON outputs were present, parsed, and locally SHA-256 hashed.
- All `9` non-self hashes matched the declared digest manifest; mismatch count: `0`.
- The digest manifest's own entry is explicitly `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`.
- Every output is `RESEARCH_ONLY_NON_ACTIONABLE`, `NOT_ACCEPTANCE_EVIDENCE`, `NOT_PROFITABILITY_EVIDENCE`, and `NOT_RUNTIME_AUTHORITY` in scope `ADDITIONAL_PREDICTIVE_EVIDENCE_REFINED_EVIDENCE_RESEARCH_ONLY`.
- No raw provider payload or API key is present in the reviewed outputs.

## Predictive Usefulness, Profitability, And Runtime Boundaries

- Predictive-usefulness reassessment review rerun created: `False`.
- Predictive usefulness: `not accepted`; acceptance readiness/recommendation/candidate: `False / False / False`.
- Profitability: `not accepted`; acceptance readiness/recommendation: `False / False`.
- Runtime migration approved/active: `False / False`.
- Runtime/strategy/paper/broker: all `NOT_AUTHORIZED`; automatic stitching: `False`.
- New strategy scoring and trade recommendations: `False / False`.
- This package supports only a future, separate reassessment-review rerun; it creates no reassessment review, acceptance, profitability, or runtime artifact.

## Offline Review Guardrails

- Provider requests, live transport, market-data acquisition, dataset generation, and canonical-dataset regeneration: all `False`.
- Feature/label refinement execution, refined label generation, refined feature generation, walk-forward/OOS reassessment, metrics, model comparison, and refined predictive-evidence execution were not rerun.
- No `.env` or API key was inspected, stored, or printed.
- No source output, canonical dataset, feature/label refinement output, Strategy behavior, broker code, or tracked runtime artifact was modified.

## Limitations And Next Gates

- The low-to-mixed OOS range, unavailable model families, calibration/stability interpretation, and preserved META limitation require operator review.
- The review result is research-only and is not predictive-usefulness or profitability acceptance evidence.
- Next task recommendation: `Predictive Usefulness Reassessment Review Rerun Using Refined Evidence v1`.
- Later acceptance-readiness, acceptance-candidate, profitability, and runtime chains remain separate and closed.
