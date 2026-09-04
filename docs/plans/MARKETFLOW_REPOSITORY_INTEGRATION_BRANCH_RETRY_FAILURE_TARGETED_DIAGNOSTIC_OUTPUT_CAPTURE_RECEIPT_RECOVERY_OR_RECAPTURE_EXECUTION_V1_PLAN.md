# MarketFlow Repository Integration Branch Retry Failure Targeted Diagnostic Output Capture Receipt Recovery or Recapture Execution v1 Plan

## Purpose

Execute the approved controlled single recapture once, retain a durable bounded receipt, and enable a separately invoked results review without creating retry or integration-success evidence.

## Source Approval

The source approval digest is `e745e07163a3bc0535b039e94433da59fb4f405558f13d69aaacfce848cf3cf9`. It selects `PACKAGE_CONTROLLED_SINGLE_RECAPTURE_WITH_PREWRITE_RECEIPT_FILE_AND_NO_CACHEPROVIDER`.

## Source Candidate Operator Review and Candidate

The operator-review digest is `c9e9844aef0926585bc96d44d37c25577ac3a29246bc0a5bd57729db0149fd6c`; the candidate digest is `a3312f96a90cb8cefdd826ac14aa2ff9d4335a4e9ed9869e3589227fb3711041`.

## Source Failure Diagnosis

The failure-diagnosis digest is `20ca664e0d673808b8be152589b76ad6f92ef9cb5be55f6c76ce87646baa9935`. The prior execution lost its durable success receipt after a single transiently successful service return; unavailable fields remain unavailable and are not reconstructed.

## Source Targeted Diagnostic Output Capture Execution

The prior execution digest is `587a13409b9654639f2282eb0c0b55c4270ba7f1cc25ad97ad7adec6630ca21d`; its blocked-manifest digest is `cfd72e69861ebbdde2a290c2d9266fbc9dfd51fc8f0fcb4b8ebe5175adaeb236` and its blocked reason is `POST_CAPTURE_ARTIFACT_REPORTING_BOUNDARY_FAILED`.

## Source Planning and Detail Binding Evidence

The execution binds the approved planning, detail-binding, materialization, recovery, and module-grouping digest chain without rerunning or modifying any source evidence.

## Retry Failure Context

The authoritative first retry remains `24,877 passed, 1,292 failed, 112 errors, and 7 skipped`. This recapture is not a retry and cannot replace that result.

## Execution Scope

`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_ONLY_CONTROLLED_RECAPTURE_DIAGNOSTIC_OUTPUT_CAPTURE_NOT_RETRY_NOT_MAIN`

## Approved Priority 1 Target Modules

- `tests/test_marketflow_signal_or_feature_generation_results_review_service.py`
- `tests/test_post_identity_freeze_registry_inventory_approval_service.py`
- `tests/test_corporate_action_authority_plan_candidate_service.py`
- `tests/test_feature_generation_results_review_redesigned_labels_service.py`
- `tests/test_marketflow_objective_label_or_target_generation_results_review_service.py`

## Approved Controlled Recapture Command

Use the repository virtualenv Python with `-m pytest -q -p no:cacheprovider --tb=short -rA`, targeting exactly the five approved modules, with the detached integration worktree as `cwd`. Use list-form subprocess arguments and never `shell=True`.

## Durable Receipt Scaffold

Write and fsync the committed JSON receipt below `docs/status` before invoking the command. It binds source digests, retry counts, argv, cwd, Python, target modules, timestamp, and prechecks while marking the command unexecuted and the receipt unfinalized.

## Pre-Execution Checks

Require the exact detached clean worktree and HEAD, exact virtualenv Python, five present module files, exact argv and cacheprovider disabling, protected Git state, no tracked `.marketflow` or `.pytest_cache`, an absent remote integration branch, and a new prewritable receipt path.

## Controlled Recapture Success Path

Run once; capture stdout and stderr in memory; hash full streams; retain only bounded redacted excerpts; record exit code, duration, byte counts, truncation, redaction, and postchecks; then finalize and fsync the same receipt. A nonzero exit remains successful diagnostic capture if all persistence and boundary checks pass.

## Blocked Path

Fail closed on source, prewrite, command-start, output-capture, receipt-finalization, or post-execution boundary failure. Retain the best available receipt and do not rerun.

## Output Bounding and Redaction

Store no more than 20,000 characters from each stream. Hash the complete streams and redact bearer tokens, secret-like assignments, environment secret assignments, and account-like identifiers from excerpts without inspecting `.env`.

## Unsupported Claims Boundary

Do not classify failures/errors, name a first failure/error, claim root cause, recommend remediation, claim retry success, claim integration success, or claim merge readiness.

## Authority Boundaries

No provider, data acquisition, dataset generation, metric recomputation, model training, strategy scoring, recommendation, predictive/profitability acceptance, runtime authorization, paper trading, or broker execution is authorized.

## Next Chain

If successful, proceed only to a separately invoked recapture results review, then to remediation/method governance if supported, and only later to a separately approved new retry. If blocked, proceed only to execution-failure diagnosis.

## Next Gates

Results review gates any remediation/method candidate; remediation/method review gates a new retry; a new retry approval gates execution; and passing new retry results review gates any main-merge approval.

## Risk Controls

Preserve the approved package, command, receipt durability, output bounds, secret redaction, no-cache behavior, detached worktree, source evidence, first retry authority, protected branches, frozen evidence, governance tags, and META limitation.

## Guardrails

Do not run full pytest, retry, source recovery, planning, detail binding, materialization, remediation, or classification. Do not read cache or logs, inspect `.env`, reconstruct prior missing values, write `.marketflow`, push protected branches, delete worktrees/branches, force-push, prune, or mutate tags.

## Next Task if Success

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_RESULTS_REVIEW_V1`

## Next Task if Blocked

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_RECEIPT_RECOVERY_OR_RECAPTURE_EXECUTION_FAILURE_DIAGNOSIS_V1`
