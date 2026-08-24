# MarketFlow Feature-Label Matrix Candidate Status

## Candidate Artifact

- Artifact: `MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_V1`.
- Status: `MARKETFLOW_FEATURE_LABEL_MATRIX_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Schema: `marketflow_feature_label_matrix_candidate_v1`.
- Scope: `FEATURE_LABEL_MATRIX_CANDIDATE_ONLY_NOT_APPROVAL_NOT_CREATION`.
- Candidate digest: `ef3d42d39a5ae353044d29d645a7ca1ad01143e5557951b05b85f837413187b4`.
- Source feature-results-review/feature-values/target-results-review/target-values digests: `8de3cfa3d4543a05956c4d9e55940525417336ffcbe523c674b43924fd22ddb7` / `7512da78cb0d222bddb2e0e5c5cb8307064ad47ebc6817025f1eaea2bcd8815e` / `41afa9e7159f2788f8dce3c44343c2058414fb51efb95b5d6714246ab866e47c` / `61480462caa3cb1177b56b72276c439035a69a28294cc1154d272f02515a8119`.

## Candidate Basis and Recommendation

- The candidate binds 155,298 reviewed feature rows across thirteen feature groups and 179,190 reviewed target rows across fifteen target profiles.
- It asks how to align history-only feature bundles to expectancy target profiles while preserving target availability, no-peek controls, per-ticker counts, and META's limitation.
- `PACKAGE_EXPECTANCY_TARGET_PROFILE_WIDE_FEATURE_MATRIX` is recommended for operator review but is not selected, approved, authorized, or executed.
- The recommended layout plans one row per target profile with a wide feature bundle: 179,190 total, 177,090 target-available, and 2,100 target-unavailable rows.
- Alternative candidate layouts retain a 2,329,470-pair long audit view and an 11,946-record canonical feature-bundle view.

## Planned Contract

- Nine matrix alignment keys, eight feature-side join rules, seven target-side join rules, and thirteen quality checks are `PLANNED_NOT_EXECUTED`.
- Twelve future outputs remain `PLANNED_NOT_GENERATED`, research-only, and non-actionable.
- Every non-META ticker plans 15,045 matrix rows and 13,039 feature rows. META plans 13,695 matrix rows and 11,869 feature rows from exactly 913 canonical records.
- All 92 candidate checklist checks pass with zero failures and zero blockers.

## Authority Boundary and Next Gate

- Candidate creation and readiness for Feature-Label Matrix Candidate Operator Review v1 are true.
- Selection, approval, authorization, matrix creation, row creation, joining, and execution remain false.
- No backtest, model, metric, strategy score, recommendation, predictive-usefulness acceptance, or profitability acceptance was created.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.
- No provider request, data acquisition, dataset regeneration, source rerun, runtime activation, or trading action occurred.
- The next task is Feature-Label Matrix Candidate Operator Review v1.
