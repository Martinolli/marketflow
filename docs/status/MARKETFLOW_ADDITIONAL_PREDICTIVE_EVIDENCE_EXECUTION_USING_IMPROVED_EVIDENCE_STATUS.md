# MarketFlow Additional Predictive Evidence Execution Using Improved Evidence Status

## Status

- Artifact: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE`.
- Status: `ADDITIONAL_PREDICTIVE_EVIDENCE_EXECUTED_USING_IMPROVED_EVIDENCE_RESEARCH_ONLY`.
- Classification: `COMPLETED_RESEARCH_ONLY`.
- Scope: `RESEARCH_EVIDENCE_EXECUTION_ONLY_NOT_ACCEPTANCE`.
- Execution digest: `b6e6429fefd2d8b0ed450845d104aab415e0142740d62bd49fc76678677aab17`.
- Output-manifest binding digest: `d6d272c9369430546c73f96d220c3e33183631de98a0a5cf9471c9179bf0710a`.
- Execution checklist: 47 passed, zero failed, zero blockers.

## Source Approval and Binding

The execution binds approval `c2ce4254de6c4fa3934a6c1fddb04f8bad334054ba914119c915f6b6071c558f`, candidate review `1db2b5a32e4cbd475330b3558706e8f7319bdf8d29a53c9e8c26bc32cc2b2442`, candidate `5705fd75afa0d614836f5b74d8a074054fd4f45b9395d5694f9f647a9322956f`, planning execution `1f2f04133a6b1d80dd30b5e8b4af08f1ae78aca8a164aa7a760a693192a894a4`, and planning output binding `23edda5191badabced31ff152a60f2428ffa08730ebaa0ba8b2facfd2d87269c`.

All 21 required source files were present and read-only. Records `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`, redesigned labels `2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f`, features `63ff963b7856607730911c567860aa8aa95274295cf3cedc99ada7339eabe8f1`, and matrix `275f23fc57c8b033224ccc7c8de6c3388bc9d1792ff3a208ee40ec018707e6ad` matched their frozen digests before and after execution.

## Dataset and Universe

- Dataset: `expanded_universe_canonical_dataset_v1`; 11,946 frozen daily records.
- Exact order: MSFT, NVDA, AMZN, GOOGL, META, TSLA, JPM, XOM, JNJ, WMT, CAT, LMT.
- META remains exactly 913 records; every other ticker remains 1003.
- The frozen matrix contains 143,352 rows: 142,200 evaluable and 1,152 with unavailable targets.

## Execution Policy

The selected direction `REDESIGN_OPTION_ADD_OR_FORMALIZE_NO_TRADE_ABSTAIN_CLASS` was used as research context only. The execution loaded the frozen matrix, repeated deterministic chronological walk-forward and 2025 OOS evaluation, and required the recomputed evidence to match the bound prior summaries exactly. It did not regenerate labels, create targets, generate features, create a canonical matrix, or mutate any source output.

## Research Results

- Walk-forward: four chronological 2024 folds, `COMPUTED_RESEARCH_ONLY`.
- OOS: 34,848 rows in the 2025 holdout, `COMPUTED_RESEARCH_ONLY`.
- Majority accuracy: `0.58626033`; local regularized accuracy: `0.58626033`.
- Ticker cross-sectional accuracy: `0.58935950`; delta versus majority: `0.00309917`.
- Nine approved model/baseline families are reported; the optional tree and ensemble families remain unavailable and no dependency was installed.
- Ten metric families are reported, including accuracy, macro precision/recall/F1, confusion matrices, Brier scores, calibration summary, class balance, stability, and baseline delta.
- Eight leakage/no-peek and frozen-source controls passed; zero failed.
- Twelve per-ticker entries are digest-bound. META's reduced-depth limitation is explicitly preserved.

These are research-only evidence results. They do not establish predictive usefulness or profitability.

## Generated Outputs

Thirteen sanitized outputs were written under the ignored execution root: the execution manifest, source-binding manifest, improved-label-schema binding report, improved feature-label matrix report, walk-forward results, OOS results, baseline/model comparison, metric-family results, calibration/stability report, leakage/quality-control report, per-ticker/META review, operator results-review summary, and digest manifest.

The digest manifest contains SHA-256 values for the 12 non-self outputs. Its own entry uses `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE` with a null file digest and an explicit binding digest.

## Authority Boundary

- Execution and results creation are true only for this research evidence package.
- Label regeneration, new-target creation, target-definition change, feature generation, and source mutation remain false.
- Predictive usefulness and profitability remain `not accepted`; a separate results review remains required.
- Runtime, strategy use, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, market-data acquisition, dataset regeneration, runtime scoring, recommendation, or trading action occurred.

## Next Gate

The separately governed `Optional Additional Predictive Evidence Results Review Using Improved Evidence v1` is now implemented and ready. This execution remains immutable source evidence; the review did not rerun it.

The results review does not regenerate labels, create targets, authorize target-definition changes, generate source features, create a canonical feature-label matrix, recompute metrics, train models, or mutate any source output. It does not create the predictive-usefulness reassessment or acceptance-readiness review, accept predictive usefulness, approve profitability, or authorize runtime, strategy, paper trading, broker execution, or recommendations.
