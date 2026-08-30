# MarketFlow Repository Integration Branch Retry Candidate Operator Review v1 Plan

## Purpose

Create an offline, digest-bound operator review of the retry candidate without
selecting, approving, authorizing, or executing a retry package.

## Source Retry Candidate

Bind the candidate artifact, candidate digest, six packages, future
requirements, planned execution steps, non-goals, and closed authority fields.

## Source Remediation Results Review

Bind the reviewed frozen-evidence remediation, source/staged inventory digest,
earlier restoration evidence, approval, diagnosis, and merge-strategy evidence.

## Failure and Remediation Context

Preserve the first failed integration pytest as authoritative and the later
wrong-worktree pass as diagnostic only. Preserve the clean detached worktree
and its exact ignored frozen acquisition evidence.

## Review Scope

Review retry options and requirements only. Do not select a package, create an
approval, execute pytest, or establish retry or integration results.

## Reviewed Retry Philosophy

An authoritative first retry must use the remediated detached integration
worktree, verify frozen evidence first, avoid regeneration and providers, and
fail closed on a wrong working directory. This remains planning only.

## Reviewed Retry Packages

Review the recommended authoritative full-pytest package, three available
alternatives, and two blocked packages. Keep every package unselected,
unapproved, and unexecuted.

## Reviewed Future Requirements and Plan

Mark every future requirement as required but not executed. Mark every future
retry step as reviewed planning with `NOT_EXECUTED` execution status. Preserve
the full-pytest acceptance gate and authoritative-first-result rule.

## Reviewed Retry Non-Goals

Keep every non-goal active, including no current pytest/retry, approval,
results review, success digest, evidence mutation, protected-ref push, provider
access, `.marketflow` commit, acceptance, runtime, or trading authority.

## Recommendation

An optional operator selection and separate approval are required before any
retry. This review leaves
`ready_for_integration_branch_retry_approval = false` and creates no approval.

## Next Chain and Gates

1. Retry Approval v1, if selected.
2. Retry Execution v1, if approved.
3. Retry Results Review v1.
4. Main Merge Approval v1 only after a passing retry review.
5. Main Merge Execution v1 only if separately approved.
6. Branch Cleanup Candidate v1 after merge strategy is settled.

The corresponding gates remain separate and sequential.

## Risk Controls and Guardrails

Preserve protected refs, the local integration branch, detached worktree,
staged frozen evidence, terminal archive evidence, published governance tags,
first failed pytest, and META limitation. Prohibit selection, approval,
execution, evidence mutation, providers, wrong-worktree acceptance, pushes,
deletions, pruning, force-push, tag mutation, or authority expansion.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_APPROVAL_V1_IF_SELECTED`.
