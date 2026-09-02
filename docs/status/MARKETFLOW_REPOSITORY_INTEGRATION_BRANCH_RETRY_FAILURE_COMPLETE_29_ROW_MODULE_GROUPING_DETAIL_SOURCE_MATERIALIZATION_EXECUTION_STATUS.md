# MarketFlow Repository Integration Branch Retry Failure Complete 29-row Module Grouping Detail Source Materialization Execution Status

## Result

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTED_COMPLETE_29_ROW_SOURCE_CREATED`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_EXECUTION_ONLY_COMPLETE_DETAIL_SOURCE_CREATION_NOT_RETRY_NOT_MAIN`.
- Selected package: `PACKAGE_MATERIALIZE_OR_BIND_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_FOR_REENTRY`.
- Execution digest: `3c1b7e6cddf2aedaec4e91dcaf742eaceb37d974b01387a8ba7f0da70cb0ac3b`.
- Materialized payload digest: `1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7`.
- Digest-manifest digest: `198e28d641e08fbba9b49fb33a942d4ffcbd77c1ad1329048e25028234a6261c`.
- Checklist: `107/107` checks passed with zero blockers.

## Source Approval

The execution binds approval digest
`f8126d0d38793c9c562fca0217823ffdb919301596ec44b9bc33ff807fa77059`.
The approval remains source evidence; execution does not alter its historical
approval-only status or scope.

## Source Operator Review and Candidate

- Operator-review digest: `72c8e88d3939ecda52acf8b0193a9df340dba832d3947daaf2449d04b0678d90`.
- Candidate digest: `4273313747b049264718bd162875b9fdea29f8f7cbb9cb4740f3b1c900fcc061`.

## Source Detail Exposure or Binding Failure Diagnosis

- Diagnosis digest: `8975126234bb36db48aab6d853879f922a65b2e86b1738212697f793c736dc41`.
- Primary failure class: `COMMITTED_COMPLETE_29_ROW_DETAIL_SOURCE_UNAVAILABLE`.
- Prior blocked execution digest: `9c1e25da799a5cafec8521cf820a39dc39e319397d978bc04695cfe2460b93ca`.
- Prior blocked-manifest digest: `c732eac857725728bb856f2d145eb86101ce1f839ddca740b66db4d48ae3aa4c`.
- Prior blocked reason: `COMMITTED_COMPLETE_29_ROW_RECOVERED_MODULE_GROUPING_DETAIL_SOURCE_UNAVAILABLE`.

## Source Recovery Results Review

- Results-review digest: `1328c7a0e8fd30052c1092b4088ee43ca0ede88659ec9ac2d79a296504aa2266`.
- Recovery-detail digest: `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`.
- Module-grouping digest: `34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.

## Retry Failure Context

The authoritative first retry result remains 24,877 passed, 1,292 failed,
112 errors, and 7 skipped at retry commit
`ab178b65c69f0274b0abbf9c20df102d35e78d34`. The latest prior root result of
29,323 passed and 7 skipped is not retry evidence.

## Reviewed Cache Verification

The approved read-only cache materialization verified:

- `lastfailed` SHA-256 `24fb8cf5ce237ae6c952c29c37acaea7d22205ca885659a196f0bc27c4b1f1b1` and 1,404 entries;
- `nodeids` SHA-256 `9d69140fd12f57de3c14060139bc4d50a3096c29b0262c5e482af5b78ea0206d` and 26,288 entries;
- every `lastfailed` node ID exists in `nodeids`; and
- the live materialized rows exactly match the committed bounded source.

The cache was read only, was not modified, and is not committed.

## Complete 29-row Materialized Source

The tracked service contains all 29 ordered module rows and their bounded
samples. This compact inventory identifies the full committed source:

| Order | Module | Count | Tier |
|---:|---|---:|---|
| 1 | `tests/test_marketflow_signal_or_feature_generation_results_review_service.py` | 136 | 1 |
| 2 | `tests/test_post_identity_freeze_registry_inventory_approval_service.py` | 131 | 1 |
| 3 | `tests/test_corporate_action_authority_plan_candidate_service.py` | 122 | 1 |
| 4 | `tests/test_feature_generation_results_review_redesigned_labels_service.py` | 112 | 1 |
| 5 | `tests/test_marketflow_objective_label_or_target_generation_results_review_service.py` | 111 | 1 |
| 6 | `tests/test_corporate_action_authority_plan_candidate_operator_review_service.py` | 109 | 2 |
| 7 | `tests/test_expanded_universe_per_ticker_identity_authority_freeze_service.py` | 97 | 2 |
| 8 | `tests/test_post_identity_freeze_registry_inventory_candidate_operator_review_service.py` | 86 | 2 |
| 9 | `tests/test_post_identity_freeze_registry_inventory_candidate_service.py` | 84 | 2 |
| 10 | `tests/test_position_swing_canonical_dataset_operator_freeze_service.py` | 81 | 2 |
| 11 | `tests/test_swing_canonical_dataset_operator_freeze_service.py` | 75 | 3 |
| 12 | `tests/test_corporate_action_authority_plan_approval_service.py` | 73 | 3 |
| 13 | `tests/test_marketflow_signal_or_feature_generation_execution_service.py` | 72 | 3 |
| 14 | `tests/test_marketflow_objective_label_or_target_generation_execution_service.py` | 48 | 3 |
| 15 | `tests/test_feature_generation_execution_redesigned_labels_service.py` | 28 | 3 |
| 16 | `tests/test_additional_predictive_evidence_results_review_redesigned_labels_service.py` | 17 | 3 |
| 17 | `tests/test_live_month_rth_diagnostic.py` | 4 | 3 |
| 18 | `tests/test_fixed_profile_orchestrator.py` | 3 | 3 |
| 19 | `tests/test_ticker_event_audit.py` | 3 | 3 |
| 20 | `tests/test_dataset_file_availability_verification_service.py` | 2 | 3 |
| 21 | `tests/test_position_swing_canonical_dataset_operator_review_service.py` | 2 | 3 |
| 22 | `tests/test_artifact_lineage_v1.py` | 1 | 3 |
| 23 | `tests/test_expanded_universe_per_ticker_identity_authority_candidate_operator_review_service.py` | 1 | 3 |
| 24 | `tests/test_packaging_integrity.py` | 1 | 3 |
| 25 | `tests/test_position_swing_registry_approval_service.py` | 1 | 3 |
| 26 | `tests/test_read_only_registry_discovery_operator_review_service.py` | 1 | 3 |
| 27 | `tests/test_source_assurance.py` | 1 | 3 |
| 28 | `tests/test_swing_canonical_dataset_operator_review_service.py` | 1 | 3 |
| 29 | `tests/test_swing_registry_approval_service.py` | 1 | 3 |

Every full row also records its deterministic percentage, priority order,
priority tier, one to five sorted sample node IDs, source, basis, confidence,
and unsupported-claims boundary.

## Top Module Concentration Preservation

The top-five counts are `136, 131, 122, 112, 111`, totaling 612
(`43.58974359%`). The top ten total 1,069 (`76.13960114%`).

## Priority Tier Enablement

Tier 1 totals 612 (`43.58974359%`), tier 2 totals 457 (`32.54985755%`),
and tier 3 totals 335 (`23.86039886%`). These are grouping priorities only,
not failure or error classifications.

## Unsupported Claims Boundary

This materialization does not separate failures from errors, identify a first
failure or first error, preserve first-result order, establish traceback root
cause, recommend direct code remediation, establish retry success, or establish
main-merge readiness.

## Outputs

All 14 required outputs are represented as `GENERATED_RESEARCH_ONLY`, including
the manifest, committed 29-row detail, source-selection and integrity reports,
module/count/sample reports, concentration and tier reports, limitations,
reattempt-enablement report, and digest manifest.

## Authority Boundaries and Guardrails

No pytest or retry was run. No source-recovery rerun, diagnostic, remediation,
classification, detail-binding reattempt, after-v2 planning reentry, targeted
diagnostic candidate, new retry candidate, results review, main push,
integration-branch push, branch/worktree deletion, tag mutation, evidence
regeneration, provider request, data acquisition, dataset generation, metric
recomputation, training, scoring, recommendation, runtime action, or trading
action occurred. Predictive usefulness and profitability remain not accepted;
runtime and broker execution remain `NOT_AUTHORIZED`.

## Next Chain and Gates

The immediate next task is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_COMPLETE_29_ROW_MODULE_GROUPING_DETAIL_SOURCE_MATERIALIZATION_RESULTS_REVIEW_V1`.
Only a passing review may open the separate detail exposure/binding reattempt
gate. After-v2 planning reentry, diagnostic capture, a new retry, its results
review, and main-merge approval remain later separately governed gates.

## Risk Controls

The execution required exact cache hashes, entry counts, subset membership,
29 rows, 1,404 grouped node IDs, exact top-five paths/counts, concentration
sums, tier sums, sorted maximum-five samples, and equality with the tracked
committed source. It preserved the integration branch, origin main, staged
evidence, terminal archive evidence, published governance tags, and the META
limitation.

## Follow-on Results Review

Complete 29-row Module Grouping Detail Source Materialization Results Review v1
is implemented and ready. This execution status remains its immutable source
evidence. The follow-on review verifies only the committed 29-row payload and
its bound execution, payload, and manifest digests.

The review does not read cache, rerun materialization or source recovery, run
pytest or the retry, execute detail binding or planning reentry, perform
diagnostics, remediation, or classification, create a new retry candidate,
push branches, commit `.marketflow` or `.pytest_cache`, accept predictive
usefulness or profitability, or authorize runtime or trading.
