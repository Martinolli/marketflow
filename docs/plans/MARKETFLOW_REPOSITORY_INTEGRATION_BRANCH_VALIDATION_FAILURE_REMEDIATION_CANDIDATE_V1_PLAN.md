# MarketFlow Repository Integration Branch Validation Failure Remediation Candidate v1 Plan

## Purpose

Create an offline, digest-bound remediation candidate for the failed local
integration-branch validation. The candidate defines choices and future gates;
it grants no remediation, retry, results-review, merge, runtime, or trading
authority.

## Source Failure Diagnosis

- Diagnosis artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_EXECUTION_FAILURE_DIAGNOSIS_V1`.
- Diagnosis digest: `a432b89bab6be2f464ebc81862fc01bc2b6fb9ce0105621f85a2b4df211b7947`.
- Approval digest: `34f70770f925a65cf82372c164b5509a05eaabafc670b541b9941a5b920dbe1c`.
- Attempted execution commit: `9d3dbc488747a0e17921bd4dcab7be2fadefc5ba`.
- Integration head: `220fbc220365fce9cae13ab4853cddff118c0187`.

## Failure Summary

The authoritative integration run reported
`24481 passed, 1300 failed, 500 errors, 7 skipped`. Its representative failure
was `ACQUISITION_EVIDENCE_REVIEW_DIGEST_MISMATCH`: expected ready prefix
`57c0a06e`, actual blocked prefix `783e0013`.

The later passing rerun was launched from the feature worktree. It remains
diagnostic-only and cannot override the first failed gate.

## Root Cause

`DETACHED_INTEGRATION_WORKTREE_LACKED_IGNORED_ACQUISITION_EVIDENCE_ROOT`.
The absent ignored root included
`acquisition_provider_evidence_run_manifest.json`.

## Candidate Scope

`REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_ONLY_NOT_APPROVAL_NOT_EXECUTION_NOT_RETRY`

## Remediation Philosophy

Future integration validation must execute from the detached integration
worktree with all required frozen ignored evidence roots available read-only.
It must not regenerate evidence, commit `.marketflow`, weaken digest checks, or
accept a rerun from another worktree.

## Proposed Remediation Packages

1. `PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE` — recommended for operator review, not selected.
2. `PACKAGE_PARAMETERIZE_INTEGRATION_VALIDATION_WITH_READ_ONLY_EVIDENCE_ROOT` — available, not selected.
3. `PACKAGE_ADD_PRECHECK_FAIL_CLOSED_FOR_MISSING_IGNORED_EVIDENCE_ROOTS` — available, not selected.
4. `PACKAGE_COMMIT_MINIMAL_TEST_FIXTURES_FOR_ACQUISITION_REVIEW_ONLY` — available, not selected.
5. `PACKAGE_REGENERATE_ACQUISITION_EVIDENCE_IN_INTEGRATION_WORKTREE` — blocked and not recommended.
6. `PACKAGE_ACCEPT_LATER_RERUN_AS_SUCCESS` — blocked and not allowed.

## Recommended Remediation Package

`PACKAGE_STAGE_FROZEN_IGNORED_EVIDENCE_ROOTS_FOR_INTEGRATION_WORKTREE` best
matches the diagnosed failure while preserving frozen evidence and validating
the real integration tree. Recommendation does not mean selection or approval.

## Remediation Requirements

The future path must identify every required evidence root, verify the source
roots and manifests, use them only as read-only inputs, keep staged outputs
untracked and uncommitted, prohibit regeneration, verify the ready digest,
reject the blocked digest, record the actual working directory, run pytest from
the detached worktree, fail closed on a wrong-worktree invocation, and require
separate remediation and retry governance chains before results review.

## Future Remediation Execution Plan

1. Inventory all frozen-output-dependent evidence roots.
2. Verify that source ignored evidence exists and is untracked.
3. Verify manifests and ready-package digest expectations.
4. Stage untracked read-only evidence into the detached integration worktree.
5. Run a detached-worktree precheck.
6. Run full pytest from that worktree.
7. Record the working directory, evidence paths, digests, and test result.
8. Do not commit `.marketflow`.
9. Mark success only if the first authoritative retry passes.
10. Create separate retry execution and results review after approved remediation.

Status: `PLANNED_NOT_EXECUTED`.

## Remediation Non-Goals

Do not retry or stage now; regenerate evidence; call providers; commit
`.marketflow`; weaken digest checks; accept the blocked digest or wrong-worktree
rerun; create results review; push main or integration; delete or reset the
integration branch or worktree; force-push; change tags; accept usefulness or
profitability; or authorize runtime or trading.

## Root-Cause Question Status

The diagnosis answered which root was missing, why the blocked digest appeared,
why the later rerun passed, and why that rerun cannot override the failed gate.
Open items are the full ready digest if not already bound, the complete evidence
root inventory, whether acquisition evidence alone suffices, the exact precheck,
and the exact approved retry execution plan.

## Next Chain and Gates

Operator review is followed, if selected, by remediation approval, execution,
and results review. Only then may an integration retry candidate proceed through
its own approval, execution, and results review. Main Merge Approval is possible
only after a successful authoritative retry review. Each stage is a separate
gate and no later gate is opened by this candidate.

## Risk Controls and Guardrails

Preserve the authoritative failure, the diagnostic-only rerun classification,
the blocked digest classification, the integration branch, terminal archive
evidence, published governance tags, `origin/main`, and the META limitation.
The candidate must not execute remediation, change repository refs, perform data
or model work, create authority, or generate recommendations.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_VALIDATION_FAILURE_REMEDIATION_CANDIDATE_OPERATOR_REVIEW_V1`
