# MarketFlow Repository Integration Branch Retry Candidate v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RESULTS_REVIEW_NOT_MAIN`.
- This is an offline governance candidate only.
- Candidate digest: `35598851bf4bfec55385cd6e2559ebb933161d846302a3032861e72ed07985eb`.

## Source Remediation Results Review

- Results-review digest: `b3f86722e05d7692805e51ca86f125df79099a10e0f4bb4d39ea9c824472ec67`.
- Evidence-manifest review digest: `c34407c83c97c64ad49ecc736ee1595629f6bc19b7e5ecb7b65850e4cbdc8cb6`.
- Remediation execution digest: `4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346`.
- Source/staged inventory digest: `06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`.

## Failure and Remediation Context

The first integration pytest (`24481 passed, 1300 failed, 500 errors, 7
skipped`) remains authoritative. The later root-worktree run remains diagnostic
only. The reviewed remediation staged the exact frozen ignored acquisition
evidence into the detached integration worktree without regeneration or Git
tracking.

## Recommended Retry Package

`PACKAGE_AUTHORITATIVE_FULL_PYTEST_RETRY_FROM_REMEDIATED_DETACHED_WORKTREE`
is recommended for operator review and remains unselected, unapproved, and
unexecuted. Five alternatives are recorded, including two blocked packages:
accepting remediation without a retry and retrying from the wrong worktree.

## Future Retry Boundary

A future approved execution must verify the exact detached worktree, HEAD,
clean state, protected refs, required manifest, ignored evidence, and inventory
digest before running full pytest from that detached worktree. The first retry
result must be authoritative and requires a separate results review.

This candidate does not run pytest or a retry, select or approve a package,
create retry or integration results, mark integration successful, generate
success digests, push branches, modify tags, commit `.marketflow`, regenerate
evidence, call providers, or authorize predictive, profitability, runtime, or
trading use.

## Next Task

All `56/56` candidate checks pass with zero failures and zero blockers.

The follow-on Integration Branch Retry Candidate Operator Review v1 is
implemented. This candidate remains its source evidence. The operator review
reviews retry packages only and does not select or approve a package, execute a
retry, run pytest, create retry results review, push branches, commit
`.marketflow`, accept usefulness or profitability, or authorize runtime.
