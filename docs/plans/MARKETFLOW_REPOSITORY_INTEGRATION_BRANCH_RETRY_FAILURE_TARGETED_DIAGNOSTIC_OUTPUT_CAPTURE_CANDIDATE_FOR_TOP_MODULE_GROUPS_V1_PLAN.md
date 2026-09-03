# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Candidate for Top Module Groups v1 Plan

## Purpose

Define controlled, candidate-only options for future targeted diagnostic-output capture against the reviewed Priority 1 module groups. No package is selected and no diagnostic or retry action is performed.

## Source Remediation or Method Results Review

The ready source review is bound by results-review digest `d6588bfbfca55cec499d1960ab260b703dd754653473ee434b7f6ac100294956`, prioritized planning-review digest `2dec0b1aa1b7dfc8d3db2323ea0c48986a2f883ff8de5f9405eb480841d8bd91`, and manifest digest `02d83a02ccdd0e67ccd13e36575b8a654617cce3190b98ec977fd829d8bc295d`.

## Source Planning Reentry with Complete Detail

The candidate binds planning execution digest `846c926ed10172c45207adb982fdb93346dac9ac550dd3a6509178746529059b`, prioritized planning digest `ef372ac66b165456241a53fdbe551c51fd4c9bfb65d2b6cdbc366cc464370c60`, manifest digest `cb0db6d23e2c206473f154e0ab91e7f098e37fcb524669f7c9a89af0b070ccac`, and selected planning package `PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING`.

## Source Detail Binding Results Review

The reviewed detail chain binds results-review digest `9124d03f9c540873a1bb3253800b1574f1266e67708034e64c95eb1ff3254a74`, binding-review digest `93469cab365790b9c06db106a7df1366cfedbfff09d6a46cd63924a58419ce93`, and complete 29-row binding digest `36d292e80b06e0f43760d2a1763c0a4af6c327930553a13d9eb64f88efb781b7`.

## Source Materialization Results Review

The materialization chain binds results-review digest `09742be04ff9014323b6e845f3aa3e105ed9bfcfcfad42f0f55bf4930d63361a` and materialized payload digest `1df469267152ecae89f7f9abcc005af127dd13bbc24f5f467951947d2711bee7` without rerunning materialization.

## Retry Failure Context

The authoritative detached retry at commit `ab178b65c69f0274b0abbf9c20df102d35e78d34` recorded 24,877 passed, 1,292 failed, 112 errors, and 7 skipped. It failed. Root regression results remain separate and do not override it.

## Candidate Scope

`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_FOR_TOP_MODULE_GROUPS_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_DIAGNOSTIC_NOT_RETRY_NOT_MAIN`

## Reviewed Priority Planning Facts

The committed planning source contains 29 module groups and 1,404 failed-or-errored node IDs. Priority 1 contains 612 (43.58974359%), Priority 2 contains 457, and Priority 3 contains 335. The top ten contain 1,069 (76.13960114%). These are concentration facts, not root-cause findings.

## Priority 1 Top Module Groups

1. `tests/test_marketflow_signal_or_feature_generation_results_review_service.py`: 136
2. `tests/test_post_identity_freeze_registry_inventory_approval_service.py`: 131
3. `tests/test_corporate_action_authority_plan_candidate_service.py`: 122
4. `tests/test_feature_generation_results_review_redesigned_labels_service.py`: 112
5. `tests/test_marketflow_objective_label_or_target_generation_results_review_service.py`: 111

## Planning Buckets

The five buckets are targeted diagnostic-output capture, evidence-root requirement review, path/CWD assumption review, digest-constant drift review, and test-fixture isolation review. Every bucket remains `PLANNING_ONLY_NOT_EXECUTED`.

## Candidate Philosophy

The reviewed after-v2 planning reentry identified Priority 1 top module groups as the highest-concentration diagnostic planning target. The next safe step is to define a controlled diagnostic-output capture method for those modules only, preserving the failed retry as authoritative while collecting bounded diagnostic information for later review. The candidate must not execute diagnostics, run pytest, infer root cause, recommend remediation, or create retry readiness.

Candidate-only; no diagnostic command, diagnostic capture, remediation, classification, retry, results review, main merge, runtime, or trading authority is created.

## Proposed Diagnostic Capture Packages

Available for operator review are targeted Priority 1 capture, Priority 1 capture with cache disabled, bounded first-N output per module, expanded Priority 1 plus Priority 2 capture, binding an existing operator-provided bounded log, and command-manifest-only creation. The expanded Priority 1 plus Priority 2 package is not recommended for the first pass.

Blocked packages are pytest-lastfailed cache as output, full pytest as diagnostic capture, root regression as diagnostic output, direct remediation from module concentration, retry without diagnostic results review, and main merge despite the failed retry.

All twelve packages have `selected`, `approved`, and `executed` set to false.

## Recommended Package

`PACKAGE_CAPTURE_TARGETED_DIAGNOSTIC_OUTPUT_FOR_PRIORITY_1_TOP_MODULE_GROUPS` is recommended for operator review, not selected. It gives the smallest high-concentration target: five modules and 612 node IDs.

## Future Diagnostic Capture Requirements

A future capture must bind all source and retry facts; target only reviewed paths unless separately expanded; avoid full pytest and retry claims; record command, CWD, executable, targets, exit code, stdout, stderr, and duration; bound output volume; avoid secrets and `.env`; prevent protected cache/output commits; preserve main, integration, and staged evidence; and require separate results review, remediation/method governance, retry governance, and a passing retry review before main merge.

## Future Diagnostic Capture Plan

Bind candidate and source evidence, select one package, verify its target scope, approve an explicit command template, use the detached worktree and repository virtual environment if approved, control cache writes, capture bounded command evidence, preserve the failed retry, and require a diagnostic results review before any remediation/method candidate. New retry, main merge, runtime, and trading stay closed.

Plan status: `PLANNED_NOT_EXECUTED`.

## Future Diagnostic Command Template

Planning-only template:

```text
C:\Users\Aspire5 15 i7 4G2050\marketflow\env\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=short -rA tests/test_marketflow_signal_or_feature_generation_results_review_service.py tests/test_post_identity_freeze_registry_inventory_approval_service.py tests/test_corporate_action_authority_plan_candidate_service.py tests/test_feature_generation_results_review_redesigned_labels_service.py tests/test_marketflow_objective_label_or_target_generation_results_review_service.py
```

Working directory: `C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1`. This template is not a retry, is not full pytest, and is not executed.

## Planned Outputs

Fourteen future reports/manifests define target selection, command and output boundaries, integrity, volume, cache and secret controls, later results-review enablement, retry-gate preservation, unsupported claims, recommendation, and digests. All are `PLANNED_NOT_GENERATED`.

## Non-Goals

Do not select, approve, or execute diagnostics; run pytest or retry; read or modify cache; rerun evidence-producing workflows; remediate or classify; infer first failures, errors, traceback causes, or code fixes; create downstream reviews or retries; change branches, tags, or evidence; call providers or inspect `.env`; or grant predictive, profitability, runtime, or trading authority.

## Next Chain

Operator review comes first, followed—only when separately selected and approved—by diagnostic capture approval, execution, and results review. Remediation/method governance may then follow if needed. A new retry requires its own candidate, approval, execution, and results review. Main merge approval exists only after a passing new retry results review.

## Next Gates

Every transition is independently gated: candidate operator review, conditional approval, conditional execution, results review, conditional remediation/method work and review, new retry candidate/approval/execution/review, then conditional main-merge approval.

## Risk Controls

The artifact is planning-only. It preserves source-review validity, the authoritative failed retry, origin/main, the local integration branch and detached worktree, frozen evidence, terminal archives, published governance tags, and the META limitation. It does not execute commands or create downstream authority.

## Guardrails

MarketFlow remains research and decision-support software. Predictive usefulness and profitability are not accepted. Runtime, strategy use, paper trading, and broker execution are `NOT_AUTHORIZED`.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_CANDIDATE_OPERATOR_REVIEW_V1`
