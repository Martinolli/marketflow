# MarketFlow Feature/Label Refinement Execution Status

## Branch And Scope

- Branch: `feature/feature-label-refinement-execution-v1`.
- Base commit: `8970fe73329490467a82d9a406c0b6c2afbc0736`.
- Commit: recorded by this document's implementing commit after validation.
- Scope: approved offline feature/label refinement execution and research-only results. No additional predictive-evidence candidate, predictive-usefulness acceptance, profitability acceptance, or runtime authority is created.

## Execution Artifact

- Artifact/status: `FEATURE_LABEL_REFINEMENT_EXECUTED` / `FEATURE_LABEL_REFINEMENT_EXECUTED_RESEARCH_ONLY`.
- Schema: `feature_label_refinement_executed_v1`.
- Execution digest: `377d6d232dcdf4b94f9f2d66414ff994edca2d3d9d95f4fb97d9dbfaf2359b36`.
- Execution timestamp: `2026-08-15T16:00:00Z`.
- Execution/results created: `True / True`.

## Bound Source Evidence

- Execution approval digest: `1b98237ae9156875ca703396b6e1fabf2acf31ab607789247f8af2391d8b5c20`.
- Execution-candidate review digest: `e6f72e45d85d58759d8f35518c1d5e6795b02923acb43f9170c5cc34a810d9ef`.
- Execution-candidate digest: `9977616fd85dbb07ff3f1192b067c77157f26935668f07135cd44eb93b5f5bc5`.
- Plan approval digest: `0dc0dc8a6a70b6549f453995ad639092da0e2b615fa059013592ae51a9609f2f`.
- Plan-candidate review digest: `782856ed6aa901762e0194e7d73d7bdd971f87034e67a6bbe142d2c494a212c1`.
- Readiness-review digest: `d4ea4dc23590d9746727d5028116e2d0711fbc55dc8853f0b455d6ee4344a3e3`.
- Results-review/original execution digests: `167a0399e99f46e895c9cdf6c70a3e650e20f60cb78641180de04e56f88caee8` / `61a90d0b863da3ddfc3ef8eb744a1ef64c476a975d83faa2be19d0f199776ed3`.
- Research-registry approval digest: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958`.
- Canonical freeze/records digests: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.

## Registry-Approved Dataset Metadata

- Dataset/scope/status: `expanded_universe_canonical_dataset_v1` / `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `APPROVED_FOR_RESEARCH_REGISTRY_ONLY`.
- Source profile/timeframe: `RTH_FULL_SESSION_1D` / `1d`.
- Date range: `2022-01-01` through `2025-12-31`.
- Total records: `11946`; data quality: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Source verification found all nine required files, verified the records digest and source-output digests, and accepted the explicit `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` policy for the canonical digest manifest.

## Target Universe And Per-Ticker Record Summary

- Exact order: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- META preserves exactly `913` records and its reduced-record-count limitation.
- Every other ticker preserves exactly `1003` records.
- All nine source-file hashes were unchanged before and after execution. No source record was repaired, inferred, normalized, backfilled, smoothed, fabricated, or mutated.

## Refined Label Generation Summary

- Seven families were generated: next-session direction and return bucket; 5-, 10-, and 20-session return buckets; forward volatility regime; and forward drawdown risk.
- All seven approved label-refinement groups were executed research-only.
- Coverage entries/available/unavailable: `84 / 82698 / 924`.
- Unavailable forward labels remain `null` with `label_unavailable_due_to_insufficient_future_bars`.
- Threshold source: `FIXED_APPROVED_RESEARCH_THRESHOLDS`; flat-return tolerance: `0.002000`.
- Refined-label generation digest: `04cf6925b956a0813c1b14e5009dc1fc4225179006589cc09d4f39721c749ee8`.

## Refined Feature Generation Summary

- All nine approved feature-refinement groups were executed across eleven documented feature categories and nineteen deterministic feature fields.
- Features use current and historical information only; future labels are not features.
- Matrix rows/coverage entries/null-or-unavailable values: `11946 / 132 / 1128`.
- META record-count handling is an explicit flag and does not repair or synthesize rows.
- Refined-feature generation digest: `35bf96942c57b851ee1fea7255002115fb871c9245cef849b1689411192b7f00`.

## Refined Protocol Execution Summary

- All six approved protocol groups were executed research-only.
- Training/validation/OOS windows remain `2022-01-01..2023-12-31` / `2024-01-01..2024-12-31` / `2025-01-01..2025-12-31`.
- Walk-forward uses expanding training with quarterly 2024 folds, a one-session label-availability embargo, and no shuffle.
- No strategy scoring, trade recommendation, runtime migration, paper trading, or broker execution occurred.

## Refined Walk-Forward Summary

- Four chronological 2024 folds were evaluated over `3024` evaluation rows.
- Each fold records its training and evaluation counts plus deterministic classification metrics for all seven comparison IDs.
- Walk-forward completion is research evidence only and is not predictive-usefulness acceptance.

## Refined Out-Of-Sample Summary

- The 2025 OOS evaluation contains `2988` rows.
- OOS accuracies: majority `0.480924`; previous direction `0.404953`; zero return `0.119813`; ticker cross-sectional `0.396252`; refined relative strength `0.396252`; refined VPA `0.233266`; refined combined simple signal `0.382195`.
- Results are preserved as observed, with no repair or acceptance inference.

## Refined Metric Summary

- Classification accuracy, macro precision, macro recall, macro F1, confusion matrices, and walk-forward stability were recomputed.
- Seven deterministic comparisons were evaluated.
- Metric conclusion: `NOT_ACCEPTANCE_EVIDENCE_UNTIL_RESULTS_REVIEWED`.

## Model Comparison Summary

- Five approved comparison groups were processed and seven dependency-light deterministic comparisons were evaluated.
- Simple-ensemble and per-ticker-versus-cross-sectional reviews are `EVALUATED_RESEARCH_ONLY`.
- Regularized-linear, tree-based, and global-versus-sector-like requests are `NOT_EVALUATED_MODEL_FAMILY_UNAVAILABLE`; no model result was fabricated and no sector authority was invented.
- Model comparison was performed but does not create acceptance evidence or recommendations.

## Refined Leakage-Control Summary

- Status/failed controls: `PASS / 0`.
- Controls cover forward-only labels, null unavailable labels, no future labels in features, current/historical-only features, chronological splits, one-session embargo, no shuffle, disabled provider transport, and closed runtime/trading paths.

## Data-Quality Summary

- Status/failures/warnings: `PASS_WITH_PRESERVED_SOURCE_LIMITATION / 0 / 1`.
- The sole warning is META's exact `913`-record limitation, preserved without repair or inference.

## Generated Outputs And Digest Manifest

- Output root: `.marketflow/feature_label_refinement/expanded_universe_v1/`.
- Generated output count: `12`.
- The digest manifest contains all twelve filenames, eleven verified file SHA-256 values, and one explicit self-reference entry for itself.
- All outputs are `RESEARCH_ONLY_NON_ACTIONABLE` with scope `FEATURE_LABEL_REFINEMENT_RESEARCH_ONLY`.
- Generated `.marketflow` outputs remain ignored and are not committed.

## Execution Boundary

- Refinement execution/results: `True / True`.
- Refined label/feature generation, walk-forward, OOS, metric recomputation, and model comparison authorized/performed: `True / True` for each.
- Provider requests, live transport, market-data acquisition, dataset generation, canonical regeneration, and prior predictive reruns: all `False`.
- Additional predictive-evidence candidate/authorization/execution/results: all `False`.
- New strategy scoring and trade recommendations: `False / False`.

## Predictive Usefulness, Profitability, And Runtime Boundaries

- Predictive usefulness: `not accepted`; readiness/recommendation/candidate: `False / False / False`.
- Profitability: `not accepted`; readiness/recommendation: `False / False`.
- Runtime migration approved/active: `False / False`.
- Runtime/strategy/paper/broker: `NOT_AUTHORIZED / NOT_AUTHORIZED / NOT_AUTHORIZED / NOT_AUTHORIZED`.
- Automatic stitching: `False`.

## Non-Goals

- No additional predictive-evidence execution candidate or execution.
- No predictive-usefulness or profitability acceptance.
- No runtime migration, strategy use, paper trading, broker execution, strategy scoring, or trade recommendations.
- No provider access, acquisition, dataset regeneration, canonical-source mutation, dependency installation, or fabricated model results.

## Next Task Recommendation

- `Feature/Label Refinement Results Review Package v1`, as a separate offline review of these exact ignored outputs and execution digest.
