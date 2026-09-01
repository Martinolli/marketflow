# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Candidate Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_CACHE_READ_NOT_RETRY_NOT_MAIN`.
- Candidate digest: `4c0542256406f1db4d86f32958d738f6c86dc83ea2dd2132e2d54bcf5afb8bcb`.
- Recommended package: `PACKAGE_RECOVER_MODULE_GROUPING_DETAIL_FROM_REVIEWED_DETACHED_PYTEST_CACHE_READ_ONLY`.
- Recommendation status: `RECOMMENDED_FOR_OPERATOR_REVIEW_NOT_SELECTED`.

## Source Evidence

- Blocked after-v2 execution digest: `7eb4bb7bd1ed0e0d2a66688f840aa352a335016533ed7f2c1c11b4d019ec4755`.
- Blocked-manifest digest: `c3d644957eb536ede1d725c912f0211a0d84aa72e56d5f8cbed2e0939a907cef`.
- Blocked reason: `MODULE_GROUPING_DETAIL_NOT_AVAILABLE_FROM_COMMITTED_SOURCE_ARTIFACTS`.
- Results-review-v2 digest: `0e3e8eb524ec199e0a02de6837900c344fcc72a596d2468663b79ad0f9571e86`.
- Execution-v2 digest: `054d1d38269731c529637e815086c22c9087e8f018a2456b62cc3b23062ce017`.
- Module-grouping digest: `34dbe78cb299882e87aa12a226b1a356a32e98799040c826d7cab53dfbb0baff`.

The authoritative retry remains `24,877 passed / 1,292 failed / 112 errors / 7
skipped`. Classification evidence remains 1,404 failed-or-errored node IDs
across 29 modules, with largest aggregate counts `136, 131, 122, 112, 111`.

## Available and Missing Detail

Available evidence consists of aggregate retry counts, the total node-ID count,
module count, largest aggregate counts, module-grouping digest, and source
execution/review digests. Module paths, per-path counts, bounded per-module
node-ID samples, grouping-report content, and a committed downstream snapshot
remain unavailable.

No grouping detail was recovered or exposed by this candidate.

## Proposed Packages

Ten candidate-only packages are defined. Five are reviewable and five remain
blocked. The recommended future method is a separately approved, read-only use
of the same reviewed detached cache, with hash/count verification before parsing
and fail-closed handling of every mismatch. The recommendation is not a cache
read, selection, approval, authorization, or execution.

Twenty-three future requirements, ten future plan steps, and ten planned outputs
are defined. Every plan step is `PLANNED_NOT_EXECUTED`, every output is
`PLANNED_NOT_GENERATED`, and all non-goals remain active.

## Authority Boundary

All `67/67` checklist checks pass, backed by 58 risk controls. This artifact is
offline governance only. It performs no module recovery, cache read, log parse,
diagnostic command, diagnostic or remediation execution, classification,
retry/full pytest, results review, branch push/deletion, tag mutation, evidence
regeneration, provider/data/model action, usefulness/profitability acceptance,
runtime authorization, or trading authorization. `.marketflow` and
`.pytest_cache` remain untracked and uncommitted.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_CANDIDATE_OPERATOR_REVIEW_V1`
