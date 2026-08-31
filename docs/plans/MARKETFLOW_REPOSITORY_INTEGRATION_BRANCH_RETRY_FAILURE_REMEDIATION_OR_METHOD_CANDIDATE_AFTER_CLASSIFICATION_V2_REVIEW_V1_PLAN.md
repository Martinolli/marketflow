# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Candidate After Classification v2 Review v1 Plan

## Purpose

Create an offline, digest-bound candidate that proposes safe next diagnostic or
remediation-planning packages after Classification Method Results Review v2.
The artifact is proposal-only and grants no approval or execution authority.

## Source Results Review v2

- Results-review-v2 digest: `0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86`.
- Review-manifest digest: `6a7c4796c188e082d4433d86f93244f8a3fe2f985302a0a52c6a4843feef01a3`.
- Execution-v2 digest: `054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017`.
- Module-grouping digest: `34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.
- Digest-manifest digest: `ac0b172d1ed107922fb0dc115b931752848e9da5db882586cd71897a41cc6add`.

## Retry Failure Context

Preserve retry commit `ab178b65c69f0274b0abbf9c20df102d35e78d34`
and the authoritative `24877 passed / 1292 failed / 112 errors / 7 skipped`
result. The prior passing root regression is not retry evidence.

## Classification Evidence Summary

Use the reviewed 1,404-node, 29-module grouping only to prioritize planning.
Preserve largest-module counts `136, 131, 122, 112, 111` and every limitation:
no failure/error separation, first-order identification, traceback root cause,
retry-success claim, or main-merge-readiness claim.

## Candidate Scope and Philosophy

The module grouping supplies concentration evidence, not root cause. The next
safe step is an operator-selected planning or diagnostic method that prioritizes
the grouped evidence without making unsupported claims. This candidate creates
no remediation, diagnostic, classification, retry, results-review, main-merge,
runtime, or trading authority.

## Proposed Packages

1. `PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING` — recommended, not selected.
2. `PACKAGE_TARGETED_DIAGNOSTIC_OUTPUT_CAPTURE_FOR_TOP_MODULE_GROUPS` — available under high control.
3. `PACKAGE_EVIDENCE_ROOT_REQUIREMENT_REVIEW_FOR_CLASSIFIED_MODULES` — available.
4. `PACKAGE_PATH_CWD_ASSUMPTION_REVIEW_FOR_CLASSIFIED_MODULES` — available.
5. `PACKAGE_DIGEST_CONSTANT_DRIFT_REVIEW_FOR_CLASSIFIED_MODULES` — available.
6. `PACKAGE_TEST_FIXTURE_ISOLATION_REVIEW_FOR_CLASSIFIED_MODULES` — available.
7. `PACKAGE_DIRECT_CODE_REMEDIATION_FROM_MODULE_NAMES_ONLY` — blocked.
8. `PACKAGE_NEW_RETRY_WITHOUT_REMEDIATION_OR_DIAGNOSTIC_ACTION` — blocked.
9. `PACKAGE_MAIN_MERGE_DESPITE_FAILED_RETRY_AND_MODULE_CLASSIFICATION` — blocked.

## Recommended Package

Recommend
`PACKAGE_PRIORITIZE_LARGEST_MODULE_GROUPS_FOR_DIAGNOSTIC_REMEDIATION_PLANNING`
for operator review, not selection. It uses the strongest supported fact—module
concentration—while avoiding direct code changes, retry, or root-cause claims.

## Future Requirements

Bind the ready review, grouping digest, module summary, and limitations. Do not
claim failure/error separation, first failure, traceback root cause, or retry
success. Prioritize without code change. Require separate approval for any
diagnostic/remediation execution and any future retry. Main merge requires a
passing future retry results review.

## Future Plan

1. Bind the Results Review v2 and module-grouping digests.
2. Use grouping only as prioritization evidence.
3. Identify largest module groups and cumulative concentration.
4. Define diagnostic capture, evidence-root, path/CWD, digest-drift, and fixture-isolation planning buckets.
5. Preserve all unsupported-claims boundaries.
6. Recommend one package after operator review.
7. Keep retry, main merge, runtime, and trading closed.

Status: `PLANNED_NOT_EXECUTED`.

## Planned Outputs

The candidate manifest, prioritized summary, concentration report, five review
reports, unsupported-claims report, recommendation report, and digest manifest
are all `PLANNED_NOT_GENERATED`.

## Non-Goals

Do not execute remediation, diagnostics, or classification; read cache; run a
retry or full pytest; create retry/integration results artifacts; claim
unsupported findings; mutate protected branches/worktrees/tags/evidence;
commit generated runtime files; call providers; accept predictive usefulness or
profitability; or authorize runtime/trading.

## Next Chain

1. Candidate Operator Review.
2. Remediation or Method Approval, if selected.
3. Remediation or Method Execution, if approved.
4. Remediation or Method Results Review.
5. New Integration Branch Retry Candidate v1, only after that review.
6. New Integration Branch Retry Approval v1.
7. New Integration Branch Retry Execution v1.
8. New Integration Branch Retry Results Review v1.
9. Main Merge Approval only if the new retry results review passes.

## Next Gates

- `remediation_or_method_candidate_after_v2_review_operator_review`
- `remediation_or_method_approval_if_selected`
- `remediation_or_method_execution_if_approved`
- `remediation_or_method_results_review`
- `new_integration_branch_retry_candidate_after_remediation_or_method_review`
- `new_integration_branch_retry_approval_if_selected`
- `new_integration_branch_retry_execution_if_approved`
- `new_integration_branch_retry_results_review`
- `main_merge_approval_if_new_retry_passes`

## Risk Controls

The artifact carries all 48 required controls: no execution, cache read, retry,
full pytest, downstream artifact, unsupported claim, protected-state mutation,
generated-output commit, provider/data/model/strategy action, acceptance, or
runtime/trading authorization. It preserves the failed retry, integration
branch, frozen evidence, terminal archive, governance tags, and META limitation.

## Guardrails

- Use committed source-review constants or a validated source review object.
- Keep construction deterministic and offline.
- Never inspect or parse cache or operator logs.
- Write only to a caller-supplied isolated output directory and refuse overwrite.
- Require operator review and separate approval before execution.
- Keep `.marketflow` and `.pytest_cache` ignored and untracked.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_CANDIDATE_AFTER_CLASSIFICATION_V2_REVIEW_OPERATOR_REVIEW_V1`
