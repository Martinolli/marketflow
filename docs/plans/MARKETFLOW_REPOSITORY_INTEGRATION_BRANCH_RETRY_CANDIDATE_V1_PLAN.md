# MarketFlow Repository Integration Branch Retry Candidate v1 Plan

## Purpose

Create an offline, digest-bound candidate for a future authoritative integration
retry after the detached worktree restoration and frozen-evidence remediation
were executed and reviewed.

## Source Remediation Results Review

Bind the ready remediation results review, its evidence-manifest review digest,
the execution digests, the source/staged inventory digest, and earlier
restoration, remediation, diagnosis, and merge-strategy evidence.

## Failure Context

Preserve the first failed integration pytest as authoritative and the later
wrong-worktree pass as diagnostic only. A retry from any feature or root
worktree is not acceptance evidence.

## Remediation Context

The detached integration worktree is restored at the required integration head
and contains the exact reviewed frozen ignored acquisition evidence root. The
evidence remains untracked and was not regenerated.

## Candidate Scope

Propose retry packages and future requirements only. Do not select, approve, or
execute a retry, create a results review, or establish integration success.

## Retry Philosophy

The first authoritative retry must run against the actual integration content
from the remediated detached integration worktree after strict evidence and
working-directory prechecks. No later rerun may override a failed first retry.

## Proposed Retry Packages

1. Authoritative full pytest from the remediated detached worktree — recommended, not selected.
2. Strict precheck followed by full pytest — available, not selected.
3. Targeted acquisition-review tests followed by full pytest — available, not selected.
4. Full pytest with cache and environment isolation — available, not selected.
5. Accept remediation without a retry — blocked.
6. Retry from a feature or root worktree — blocked.

## Recommended Retry Package

`PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE`
is recommended for operator review because only that worktree represents the
actual remediated integration branch content.

## Future Retry Requirements

Require the ready source review, exact worktree/head, detached and clean state,
unchanged protected refs, absent remote integration branch, required staged
manifest, ignored evidence, exact `06d19e5e...2734b0` inventory digest, correct
working directory, full pytest, authoritative first result, separate results
review, and separate main-merge approval.

## Future Retry Execution Plan

Verify all source digests, path/ref/worktree guards, staged evidence and hashes;
then run full pytest from the detached worktree and record the exact command,
working directory, exit code, counts, and duration. Fail closed on the first
failure. A pass creates only an execution artifact, not a results review or main
authority.

## Retry Non-Goals

No retry, pytest, approval, execution, results review, success claim or digest,
evidence staging/modification/regeneration, provider access, `.marketflow`
commit, protected-ref push, branch/worktree deletion, force-push, tag mutation,
wrong-worktree acceptance, predictive/profitability acceptance, runtime, or
trading authority is part of this candidate.

## Next Chain

1. Integration Branch Retry Candidate Operator Review v1.
2. Integration Branch Retry Approval v1, if selected.
3. Integration Branch Retry Execution v1, if approved.
4. Integration Branch Retry Results Review v1.
5. Main Merge Approval v1 only if the retry review passes.
6. Main Merge Execution v1 only if separately approved.
7. Branch Cleanup Candidate v1 after merge strategy is settled.

## Next Gates

- `integration_branch_retry_candidate_operator_review`
- `integration_branch_retry_approval_if_selected`
- `integration_branch_retry_execution_if_approved`
- `integration_branch_retry_results_review`
- `main_merge_approval_if_retry_passes`
- `main_merge_execution_if_approved`
- `branch_cleanup_candidate_after_merge_strategy`

## Risk Controls and Guardrails

Preserve protected refs, the integration branch, detached worktree, staged
frozen evidence, terminal archive evidence, published governance tags, first
failed pytest, and META limitation. Require separate operator review, approval,
execution, and results-review gates. Fail closed on wrong-worktree execution or
any evidence/ref mismatch.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_OPERATOR_REVIEW_V1`.
