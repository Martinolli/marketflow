# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Execution v1 Plan

## Purpose and Source Method Approval

Execute the approved
`PACKAGE_CLASSIFY_RETRY_FAILURE_DOMAINS_FROM_AUTHORITATIVE_OUTPUT` method
offline, bound to approval digest
`44e0d7c7ea17f0be0444bc2ad3f4f1974d606f1cb8b1f2d59f0748f462135f02`.
This execution classifies persisted authoritative retry detail only and never
reruns pytest.

## Retry Failure Context and Execution Scope

Preserve the authoritative detached retry at `24877 passed, 1292 failed, 112
errors, 7 skipped`. Root-worktree regression is not retry evidence. Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.

## Input Source Search

Inspect only the committed retry execution status, plan, and service, plus an
ignored local log only when one of those records explicitly references it.
Explicit caller-supplied retry output text or path may be parsed. Do not inspect
`.env`, call providers, search unrelated outputs, or invoke pytest.

## Failure Classification Success Path

When detailed output contains both pytest failure and error records,
conservatively record modules, first records by pytest summary order, bounded
module counts, root-cause-family candidates, confidence, evidence type, and
actionability. Generate only research or summary planned outputs and route to
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_V1`.

## Blocked Output-Unavailable Path

When persisted records contain only aggregate counts, record the available
command, working directory, duration, and source documents; enumerate missing
module/trace detail; generate no classification; and use blocked reason
`AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE`. Route to
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1`.

## Authority Boundaries

Method execution does not authorize remediation, a retry, results review,
integration success, successful integration digests, a new retry candidate,
main merge, protected-branch pushes, evidence changes, predictive usefulness,
profitability, runtime, or trading.

## Next Chain and Gates

The success chain begins with method results review and then separately gated
new-retry candidate, approval, execution, results review, and possible
main-merge approval. The blocked chain begins with output-capture/classification
source candidate, operator review, approval, execution, results review, and
classification-method reentry. Every transition has a separate named gate.

## Risk Controls and Guardrails

Do not rerun retry/full pytest, fabricate classification, mutate or stage
evidence, call providers, commit `.marketflow`, push main or the integration
branch, delete/reset/force-push, prune remotes, mutate tags, or create
data/model/predictive/profitability/runtime/broker authority. Preserve
`origin/main`, the local integration branch, detached worktree, frozen staged
evidence, terminal archive evidence, published governance tags, and the META
limitation.

## Next Task by Disposition

- Success: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_RESULTS_REVIEW_V1`.
- Blocked: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_CANDIDATE_V1`.
