# MarketFlow Repository Integration Branch Retry Failure Module Grouping Source Recovery Results Review Status

## Result

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_MODULE_GROUPING_SOURCE_RECOVERY_RESULTS_REVIEW_ONLY_NOT_PLANNING_REENTRY_NOT_RETRY_NOT_MAIN`.
- Source execution digest: `250b217bc46c4d85b349a1dd4dce58b61c1fc81ba001ddfd73eb8ca102a1029a`.
- Source recovery-detail digest: `a8f36d291392a62589216a7609af355e0c12c7bf2fea6b3e988cdabe9638bdf5`.
- Source digest-manifest digest: `940d15590cf3f98fc9de5861ca5e94fe01d15e47bb5cf4bf1b8fb51bf5333fdc`.

## Reviewed Evidence

The review binds the failed detached retry (`24,877` passed, `1,292` failed,
`112` errors, and `7` skipped) and preserves it as authoritative. It verifies,
from committed source-execution facts only, the prior cache hashes and counts,
the `lastfailed` subset result, 1,404 failed-or-errored node IDs across 29
modules, deterministic module ordering, per-module counts, bounded samples, and
the largest counts `136, 131, 122, 112, 111`.

The top five groups contain 612 node IDs (`43.58974359%`) and the top ten
contain 1,069 (`76.13960114%`). All ten planned outputs remain
`GENERATED_RESEARCH_ONLY`. The six recovery limitations and every unsupported
claim remain explicit: the evidence does not separate failures from errors,
preserve first-failure order, provide tracebacks, prove root cause, recommend
direct remediation, prove retry success, or establish main-merge readiness.

## Disposition and Boundaries

The recovery execution is accepted as source evidence for a separate after-v2
planning re-entry. That re-entry has not been created. No cache was read or
modified by this review; recovery was not re-executed; and no diagnostics,
remediation, classification, retry, full pytest run, new retry candidate,
retry-results review, integration-results review, protected-branch push, tag
mutation, or evidence regeneration occurred.

`.marketflow` and `.pytest_cache` remain untracked and uncommitted. Predictive
usefulness and profitability remain not accepted. Runtime, strategy, paper
trading, and broker execution remain `NOT_AUTHORIZED`. No provider, market-data,
dataset, metric, model, scoring, recommendation, runtime, or trading action was
performed.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_AFTER_V2_PLANNING_REENTRY_USING_RECOVERED_MODULE_GROUPING_SOURCE_V1`
