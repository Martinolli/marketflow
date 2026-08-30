# MarketFlow Repository Integration Branch Validation Failure Remediation Results Review v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_RESULTS_REVIEW_ONLY_NOT_RETRY_NOT_INTEGRATION_RESULTS_REVIEW_NOT_MAIN`.
- The package is an offline governance review using only read-only Git and file inspection.
- Review digest: `b3f86722e05d7692805e51ca86f125df79099a10e0f4bb4d39ea9c824472ec67`.
- Evidence-manifest review digest: `c34407c83c97c64ad49ecc736ee1595629f6bc19b7e5ecb7b65850e4cbdc8cb6`.

## Bound Source Remediation Execution

- Execution digest: `4f295a1e8c400279e40ac46ba0ab4b29dbff8ccdea66078a51b8d4f355d78346`.
- Execution evidence-manifest digest: `ca97ebf04c84a3008e222e2fa16a15c18e2528a21bee67e0a43bd82990e99fae`.
- Source/staged inventory digest: `06d19e5e81485e416610fb1e0aa7b2f375996c38c85d08cc771d47d4402734b`.
- Worktree restoration results-review digest: `562c6bc4cadb09232ca304efb803d566c0904226314b8f94cceef2e54122159a`.
- Remediation approval digest: `681dc28750718911baa4ec6027f6470d6f9f7cab263ae237b69bba81f8fb4ded`.

## Detached Worktree and Staged Evidence Review

- Integration branch and detached-worktree HEAD: `220fbc220365fce9cae13ab4853cddff118c0187`.
- Detached worktree: `C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1`.
- Source root: `C:\Users\Aspire5 15 i7 4G2050\marketflow\.marketflow\acquisition_provider_evidence\expanded_universe_v1`.
- Staged root: `C:\Users\Aspire5 15 i7 4G2050\marketflow_worktrees\integration-terminal-evidence-stack-validation-v1\.marketflow\acquisition_provider_evidence\expanded_universe_v1`.
- Required manifest: `acquisition_provider_evidence_run_manifest.json`.
- Source and staged inventories: 7 files and 2,458,181 bytes each.
- Per-file SHA-256 manifests match exactly.
- The staged root remains ignored and untracked; `.marketflow` has no tracked files in either worktree.

## Failure Context

The first integration pytest remains authoritative: `24481 passed, 1300
failed, 500 errors, 7 skipped`. The later `26842 passed, 7 skipped` run remains
diagnostic only. This review confirms that the diagnosed missing ignored
evidence root was staged correctly; it does not reinterpret either test run or
claim integration success.

## Readiness and Authority Boundary

The reviewed remediation is ready for a separate Integration Branch Retry
Candidate v1. This review does not create that candidate, approve or execute a
retry, create an integration results review, mark integration successful, or
issue successful integration execution or validation digests.

No evidence was copied, changed, regenerated, staged in Git, or committed by
this review. No provider, acquisition, dataset, metric, model, scoring,
recommendation, runtime, trading, branch-push, tag, deletion, or reset action
occurred. Predictive usefulness and profitability remain not accepted;
runtime and broker execution remain `NOT_AUTHORIZED`.

## Next Task

All `64/64` review checks pass with zero failures and zero blockers.

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_CANDIDATE_V1`.
