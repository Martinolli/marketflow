# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution After Diagnostic Capture v1 Plan

## Purpose

Execute the approved, deterministic method-analysis package over committed bounded diagnostic evidence. The result is evidence for a separate method results review, not remediation or retry evidence.

## Source Approval

- approval commit: `486024f32efb50d9620ba26b950892295c5a660e`
- approval digest: `7c4096364f1d1d5feb048bdbb7987c46e082947d75664f15976460590745b6e6`
- approval remains source evidence; it is not re-created by this execution

## Source Operator Review and Candidate

- operator-review digest: `63a717f6149f2deb9de303381235c2d0d80ec5273a332faf36708cfe79852845`
- candidate digest: `405fa30e32f2e71f77cd502cbd8ad0644f2f07d684de9a24b0d90ac0b3bab95d`

## Source Diagnostic Results Review

The execution binds results-review digest `427d2a76afcec7c8b9647a0f0c19b6037e5a451b0f70fad1a5025afc266946ba`, payload-review digest `bdba29bcb8835cb3b06caa0b4028b5480af04b6ecc28bd01392784e549556ee3`, durable-receipt-review digest `2cd966d75bd70fc3bcb6d3f7b9ed33dacc47fde0d2697dfc24d0f7e0b1e4bdcd`, and review-manifest digest `c3394bb56e7c20ed46274dc270992011417f52c3174cf3094c50cea3be823ce4`.

## Source Controlled Recapture Execution

The committed source execution is `51175f3d24232773ae3982a97b05877e18ff699e` with execution digest `25a70331c48eedeb62c6f8532dba0e1b782904ff4b753934c2fd12ccbec47e46`. It is historical diagnostic evidence and is not rerun.

## Source Durable Receipt

Read only `docs/status/MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_RECEIPT_V1.json`, bound by receipt digest `dfd7f50c4065e759ccfee0f160c97177f4d9a1cfe977fb6db1ce240f8ad3345b`. No alternate source is permitted.

## Source Receipt Loss History

The prior blocked execution remains historically blocked for `POST_CAPTURE_ARTIFACT_REPORTING_BOUNDARY_FAILED`; the reviewed durable receipt recovery does not rewrite that history.

## Source Planning and Detail Binding Evidence

Bind planning execution digest `846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b`, detail-binding results-review digest `9124d03f9c540873a1bb3253800b1574f1266e67708034e64c95eb1ff3254a74`, complete 29-row binding digest `36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7`, recovery-detail digest `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`, and module-grouping digest `34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.

## Retry Failure Context

The first retry result remains authoritative: `24877` passed, `1292` failed, `112` errors, and `7` skipped. The latest prior root regression is not retry evidence.

## Execution Scope

`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_ONLY_METHOD_ANALYSIS_NOT_REMEDIATION_NOT_RETRY_NOT_MAIN`

## Selected Remediation or Method Package

`PACKAGE_CLASSIFY_REVIEWED_DURABLE_DIAGNOSTIC_RECEIPT_FAILURE_FAMILIES_FOR_REMEDIATION_METHOD_PLANNING`

## Priority 1 Target Modules

1. `tests/test_marketflow_signal_or_feature_generation_results_review_service.py` — 136 node IDs
2. `tests/test_post_identity_freeze_registry_inventory_approval_service.py` — 131 node IDs
3. `tests/test_corporate_action_authority_plan_candidate_service.py` — 122 node IDs
4. `tests/test_feature_generation_results_review_redesigned_labels_service.py` — 112 node IDs
5. `tests/test_marketflow_objective_label_or_target_generation_results_review_service.py` — 111 node IDs

Priority 1 totals `612` of `1404` failed-or-errored node IDs (`43.58974359%`); the top 10 total is `1069` across a reviewed 29-module summary.

## Diagnostic Capture Evidence Summary

The source records exit code `1`, duration `21.584361` seconds, stdout `1231380` bytes, stderr `0` bytes, a truncated bounded stdout excerpt, an untruncated empty stderr excerpt, and completed redaction review. These facts are diagnostic evidence only.

## Method Input Source

Use only approval constants, reviewed source constants, and the committed receipt fields `bounded_stdout_excerpt` and `bounded_stderr_excerpt`. Do not use full streams, caches, histories, logs, environment files, providers, or commands.

## Durable Receipt Integrity

Require the expected path, finalized status, execution binding, embedded receipt digest, original stream metadata, bounded excerpt fields, and redaction status. Any mismatch produces the blocked artifact.

## Bounded Excerpt Integrity

Compute integrity hashes only for the committed receipt file and bounded excerpt strings. These hashes must not be described as reconstructed full-stream hashes.

## Failure-Family Classification Method

Apply deterministic conservative regex rules to non-empty bounded lines, redact before storage, retain at most five snippets of at most 500 characters for each family, and order families by descending evidence count then ascending `family_id`.

## Observable Failure Families

Create only text-supported families from the approved inventory. If no specific family matches, create `insufficient_visible_pattern_detail` with low confidence and an explicit additional-capture limitation.

## Family Confidence and Limitations

Confidence derives only from bounded visible match counts. Every record states that it is not a root-cause conclusion, direct remediation recommendation, full retry classification, or retry-success claim.

## Success Path

When approval, receipt, digest, excerpt, and boundary checks pass, create the executed artifact, the fourteen `GENERATED_METHOD_ANALYSIS_ONLY` outputs, four deterministic success digests, and readiness only for a separately invoked method results review.

## Blocked Path

If a required input or boundary fails, create the blocked artifact and deterministic blocked-manifest digest. Do not seek alternate evidence, recapture, rerun, or infer missing values.

## Unsupported Claims Boundary

Root cause, authoritative first failure or error, full retry classification, direct remediation, retry success, and main-merge readiness remain false.

## Authority Boundaries

This execution grants no remediation, retry, integration-results-review, main-merge, provider, data, predictive, profitability, runtime, strategy, paper-trading, or broker authority.

## Next Chain

Success proceeds only to method results review, then separately governed remediation candidate/review/approval/execution/results review, then separately governed retry candidate/approval/execution/results review, and only then possible main-merge approval. A blocked result proceeds only to execution failure diagnosis or an alternate separately governed method/source candidate.

## Next Gates

Keep all method-review, remediation, new-retry, and main-merge gates explicit. Remediation stays blocked until method results review passes; retry stays blocked until remediation or method review passes; main merge stays blocked until a new retry results review passes.

## Risk Controls

Preserve the approved package and bounded receipt-only input; no stream reconstruction, diagnostic or retry command, pytest diagnostic work, cache/log/environment access, source behavior change, evidence regeneration, protected-branch mutation, provider/data/model action, recommendation generation, predictive/profitability acceptance, or runtime/broker authorization.

## Guardrails

Default tests remain offline and deterministic. Generated `.marketflow`, `.pytest_cache`, and packaging artifacts remain untracked. MarketFlow remains research and decision-support software, not execution software.

## Next Task

- success: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_AFTER_DIAGNOSTIC_CAPTURE_V1`
- blocked: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_AFTER_DIAGNOSTIC_CAPTURE_FAILURE_DIAGNOSIS_V1`
