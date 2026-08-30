# MarketFlow Repository Integration Branch Validation Failure Remediation Execution v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTED_EVIDENCE_STAGED_AFTER_WORKTREE_RESTORATION`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_EXECUTION_ONLY_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.
- Selected package: `PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE`.
- Execution digest: `4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346`.
- Evidence manifest digest: `ca97ebf04c84a3008e222e2fa16a15c18e2528a21bee67e0a43bd82990e99fae`.

## Bound Source Evidence

- Worktree restoration results-review digest: `562c6bc4cadb09232ca304efb803d566c0904226314b8f94cceef2e54122159a`.
- Worktree restoration results-review manifest digest: `415f2445805f93906b5f63035472f8edb95f41f64c57c46eab659e5221cc738d`.
- Remediation approval digest: `681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`.
- Failure diagnosis digest: `a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947`.
- Attempted execution: `feature/marketflow-repository-integration-branch-execution-v1` at `9d3dbc488747a0e17921bd4dcab7be2fadefc5ba`.

## Authoritative Failure

The first integration pytest result remains authoritative: `24481 passed,
1300 failed, 500 errors, 7 skipped`. The later `26842 passed, 7 skipped` run
remains `DIAGNOSTIC_ONLY_NOT_ACCEPTANCE_EVIDENCE`.

The preserved root cause is
`DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT`.
Required digest prefix `57c0a06e` is verified; blocked prefix `783e0013` is
not accepted as ready.

## Evidence Staging Result

- Source: `C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\acquisition_provider_evidence\expanded_universe_v1`.
- Target: `C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1\.marketflow\acquisition_provider_evidence\expanded_universe_v1`.
- Required manifest: `acquisition_provider_evidence_run_manifest.json`.
- Source and staged inventories: 7 files, 2,458,181 bytes each.
- Source and staged inventory digest: `06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b0`.
- All per-file SHA-256 values match: `true`.
- Target remains ignored and untracked: `true`.
- `.marketflow` committed: `false`.
- Evidence regenerated: `false`.

## Worktree and Repository Protection

- Detached worktree HEAD before and after: `220fbc220365fce9cae13ab4853cddff118c0187`.
- Detached worktree branch checkout: none.
- Detached worktree status after staging: clean because the copied evidence is ignored.
- `origin/main` before and after: `eda58d9a56656641d4e0c2a80a6e572b6e949fc2`.
- Remote integration branch: absent.
- Integration branch push: `false`.
- Main push or merge: `false`.
- Branch/worktree deletion or reset: `false`.
- Tag mutation: `false`.
- `git ls-files .marketflow`: zero tracked files.

## Authority Boundary

This execution copied only the approved frozen ignored evidence root. It did
not run the integration retry, create a retry candidate or results review,
mark integration successful, generate a successful integration digest, call a
provider, acquire or regenerate data, recompute metrics, perform model work,
or generate recommendations.

Predictive usefulness and profitability remain not accepted. Runtime,
strategy, paper-trading, broker, and execution authority remain
`NOT_AUTHORIZED`.

## Checklist and Next Task

All `66/66` checks passed with zero failures and zero blockers.

The follow-on Integration Branch Validation Failure Remediation Results Review
v1 is implemented. This execution remains its source evidence. The results
review verifies the staged ignored frozen evidence root in the detached
integration worktree and does not retry integration, create a retry candidate,
create an integration results review, push branches, commit `.marketflow`,
regenerate evidence, accept usefulness or profitability, or authorize runtime.
