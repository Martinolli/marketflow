# MarketFlow Repository Integration Branch Validation Failure Remediation Candidate v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_READY_FOR_OPERATOR_REVIEW`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY`.
- The artifact is offline, governance-only, and ready for a separate operator review.

## Bound Source Failure

The candidate binds failure-diagnosis digest
`a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947`
and merge-strategy approval digest
`34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.
The first integration pytest remains authoritative at
`24481 passed, 1300 failed, 500 errors, 7 skipped`.

The later `26842 passed, 7 skipped` rerun remains diagnostic-only because
pytest ran from the feature worktree, not the detached integration worktree.
It does not override or repair the failed gate.

## Root Cause and Recommendation

The detached integration worktree lacked the ignored frozen acquisition
evidence root, including `acquisition_provider_evidence_run_manifest.json`.
The candidate recommends
`PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE` for
operator review. The package is recommended but is not selected, approved,
authorized, or executed.

Five other packages remain available or blocked for review. In particular,
regenerating acquisition evidence and accepting the wrong-worktree rerun are
blocked. The future ten-step plan is `PLANNED_NOT_EXECUTED`.

## Authority Boundary

This candidate does not stage or copy evidence, modify `.marketflow`, retry
pytest, create Integration Branch Results Review, mark execution successful,
push the integration branch or main, delete or reset branches or worktrees, or
modify tags. It performs no provider, market-data, dataset, metric, model,
scoring, recommendation, runtime, broker, or trading action.

Predictive usefulness and profitability remain not accepted. Runtime,
strategy, paper-trading, and broker execution remain `NOT_AUTHORIZED`.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1`
