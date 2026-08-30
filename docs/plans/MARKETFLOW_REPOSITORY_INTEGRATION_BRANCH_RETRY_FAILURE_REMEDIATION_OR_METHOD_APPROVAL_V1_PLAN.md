# MarketFlow Repository Integration Branch Retry Failure Remediation or Method Approval v1 Plan

## Purpose

Create one offline, deterministic, attestation-bound approval selecting a
reviewed retry-failure method for future execution only. This plan does not
execute the method, diagnostics, remediation, or another retry.

## Source Operator Review and Method Candidate

Bind the operator review digest
`cf541e8681724e1018cf0c343daf718a3a50249e3bdf8640c54d88791427f0be`,
method candidate digest
`414b511d6b4b9aca89fa92c50b23304d60be4d2064f8e8004b7e747c1a0359c6`,
and retry-failure diagnosis digest
`f7cb3e57973d97ba9118d182ba24d0619d6d9b1f7a0b34011e47fc5e1a54b8a1`.
The operator review remains source evidence; it is not rewritten as an
execution result.

## Operator Attestation

Require the exact non-secret approval phrase, decision, source digests, retry
execution commit, selected package, failure-count boundary, root-regression
boundary, approval-only scope, and every closed-authority confirmation. Reject
missing or changed evidence, selection, phrase, or confirmation values.

## Retry Failure Context and Approval Scope

Preserve the authoritative detached retry at `24877 passed, 1292 failed, 112
errors, 7 skipped`. Root-worktree regressions are not retry evidence. Scope is
`REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.

## Selected Method Package

Approve
`PACKAGE_CLASSIFY_RETRY_FAILURE_DOMAINS_FROM_AUTHORITATIVE_OUTPUT` as
`APPROVED_FOR_FUTURE_RETRY_FAILURE_METHOD_EXECUTION_ONLY`. It is selected,
approved, and authorized for a future separate execution task, but remains
unexecuted.

## Approved Requirements and Future Method Plan

Approve all eighteen reviewed requirements for future execution only. Approve
the ten-step plan to locate persisted authoritative output, extract modules and
first traces, classify root-cause families, summarize modules and blockers,
identify evidence/test-harness issues, recommend a follow-on package, and keep
downstream authority closed. Plan execution status remains `NOT_EXECUTED`.

## Planned Outputs and Other Packages

Carry all eleven planned classification and digest outputs as
`AUTHORIZED_NOT_GENERATED`. Keep the ignored-evidence inventory, path/cwd,
digest-drift, and test-isolation packages `AVAILABLE_NOT_SELECTED`. Keep the
integration rebuild, root-regression substitution, and main-merge shortcut
packages `BLOCKED_NOT_APPROVED`.

## Next Chain and Gates

The gated chain is method execution, method results review, a new integration
retry candidate, retry approval, retry execution, retry results review, and
only then main-merge approval if that new retry passes. Each transition remains
separate, including `retry_failure_method_execution_if_approved` and
`retry_failure_method_results_review`.

## Risk Controls and Guardrails

Do not run diagnostics or full pytest, rerun the retry, generate classification
outputs, execute remediation, mutate staged evidence, call providers, commit
`.marketflow`, push main or the integration branch, delete/reset/force-push,
prune remotes, mutate tags, or create predictive, profitability, runtime, or
broker authority. Preserve `origin/main`, the local integration branch,
detached worktree, frozen evidence, terminal archive evidence, published
governance tags, and the META limitation.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_OR_METHOD_EXECUTION_V1`
may be invoked separately after this approval.
