# MarketFlow Repository Integration Branch Retry Failure Remediation Execution After Plan Results Review v1 Plan

## Purpose

Execute only the approved controlled, plan-derived remediation package. Retain a remediation change only when the reviewed evidence supplies source authority, file impact, snapshots, workstream mapping, verification evidence, and passing focused validation. Otherwise fail closed.

## Source Approval

Bind approval commit `07ecfa2353f450ffacd807809d4857c8f8231b9b` and digest `2076c16fe79ce964b18a485afd23c53e5d59f8ef6660e8ebc736ef1f0c8fb2f1` without invoking an approval ceremony.

## Source Operator Review and Candidate

Bind operator-review commit/digest `999fab934370d16b24c5ed84876f06254fbacb9b` / `8f7033f203707634413ba460ae5fcbf829bda5822eb379677515e02d6333a3b4` and candidate commit/digest `c12583bc41e7de16c371f36f4408a468108a8bc7` / `6869b7642d8f90fd0273a7cbfdd069af85b23518778100ae19f3ebb6060fe4bd`.

## Source Plan Results Review

Bind results-review commit `9cab8e24d7da93408008cc96a412d7ef03eada41`, execution-review digest `30b584ded57da0811ee9f7a6d68e984badffb65185cac5e38d6dfbf63e1fdffa`, targeted-plan review digest `7570033ff0aeca33bc6cc5f8fbfc3a462d50cb1d3c5537421f6dbd7aefb3d115`, workstream-mapping review digest `f016b1d5b4da4e3a59e4e93b88f86ce6321f4bec0df14dbcd971bf4a6ec8b334`, and manifest digest `1400f14156569806fc9d50347380e642b61e4fa6a568c518cf9c7601774e9b84`.

## Source Plan Execution

Bind commit `57ce0d2760d2ae6de2a16bade80291f4dbe05305`, execution digest `a7cb542d77ddcda7e3bad66080a8ffc4b435874c4985e4677a274106b329802c`, targeted-plan digest `2d7ffac9fc3cc04f0bfb823ef81f254005adaee7a600ccb6e3444b7f3dec91db`, workstream-mapping digest `275b1e5a16e7bffc8bd323615b764fff7e88070d88198177cc11c64530e948e0`, and manifest digest `7f0b973fb6bbc6286e7e4bda208c48a8da4c8a56f8f4809b0ced315e129a77ed`.

## Source Targeted Remediation Plan and Workstream Mapping

Treat the reviewed targeted plan and four one-to-one family/workstream mappings as planning evidence. They define verification requirements but do not themselves prove a particular file value wrong.

## Source Method Results Review and Execution

Bind method-results-review commit `b847470633387b7056cb2c436a674dbeab347e61` and its result, classification, and bounded-analysis digests. Bind method-execution commit `2e447891ac8bb8ed86b2a3ecaa09043b7933aef7` and its execution, classification, bounded-analysis, and manifest digests. Do not rerun either method.

## Source Diagnostic Results Review, Controlled Recapture, and Durable Receipt

Bind the committed diagnostic results-review and controlled-recapture digests. Bind the durable receipt path and digest as diagnostic evidence only; do not open, parse, or reconstruct it.

## Source Planning and Detail-Binding Evidence

Preserve the committed planning, complete-29-row binding, materialization, recovery-detail, module-grouping, staged-inventory, prior blocked execution, and recovery digests as source evidence.

## Retry Failure Context

Preserve the authoritative failed retry counts: 24,877 passed, 1,292 failed, 112 errors, and 7 skipped; 1,404 failed-or-errored nodeids across 29 modules; Priority 1 total 612; top-10 total 1,069. Exit code 1 and the bounded stream facts remain diagnostic only.

## Execution Scope and Selected Package

Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_ONLY_CONTROLLED_PLAN_DERIVED_REMEDIATION_NOT_RETRY_NOT_MAIN`.

Package: `PACKAGE_EXECUTE_CONTROLLED_PLAN_DERIVED_REMEDIATION_WITH_VERIFICATION_ONLY`.

## Priority 1 Target Modules

Inspect only the five reviewed Priority 1 test modules and their directly corresponding services unless explicit source authority justifies another allowed file. The governance execution service, tests, export, plan, and status are also in scope.

## Reviewed Observable Families and Workstreams

Preserve the four HIGH-confidence, 47-item families: assertion/value mismatch, digest/hash mismatch, fixture/test isolation, and missing/unexpected field. Map them to the assertion-value, digest-boundary, fixture-determinism, and schema-field workstreams. These are bounded observable classifications, not root causes.

## Controlled Remediation Execution Method

Verify bindings, inventory candidate files, hash pre-change state, inspect only allowed files, retain only source-authorized changes, hash post-change state, map changes to workstreams, and run focused validation with the pytest cacheprovider disabled. Block if any required authority or evidence is absent.

## File-Impact Inventory and Pre-Change Snapshot

Record existence, classification, workstream mapping, source authority, hashes, change flags, file roles, and verification disposition for all ten Priority 1 candidate files before any remediation change.

## Change Records and Post-Change Snapshot

No Priority 1 source, test, expected digest, or contract value may change merely because a family label exists. Every retained change requires the complete change record and post-change snapshot. If none is justified, retain no remediation patch and use the blocked path.

## Focused Validation

Run the five Priority 1 modules plus the new execution tests and immediate approval, operator-review, candidate, and plan-results-review regressions. Always use `-p no:cacheprovider`; never run full pytest or the detached retry.

## Success Path

Success requires at least one safely retained source-authority-bound change plus complete snapshots, mappings, verification, and passing focused validation. It creates readiness only for a separate remediation-execution results review.

## Blocked Path

If no safe change is justified or validation fails, emit the blocked artifact and recommend `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_REMEDIATION_EXECUTION_AFTER_PLAN_RESULTS_REVIEW_FAILURE_DIAGNOSIS_V1`. Do not claim remediation or retry readiness.

## Unsupported Claims and Authority Boundaries

Do not claim root cause, first-failure ordering, retry success, integration success, or main-merge readiness. Do not parse diagnostic evidence, inspect environment secrets, access caches/logs, call providers, acquire data, regenerate datasets/evidence, recompute metrics, train models, score strategies, recommend trades, authorize runtime, or authorize broker execution.

## Next Chain and Gates

After success: remediation results review, new retry candidate, separate retry approval, new retry execution, retry results review, and only then possible main-merge approval. After blocking: separate failure diagnosis only. Retry and main merge remain closed.

## Risk Controls and Guardrails

Protect origin/main, the local integration branch/worktree, staged frozen evidence, terminal archive evidence, published tags, and the META limitation. Do not push main or integration, delete branches/worktrees, force-push, prune remotes, modify tags, track `.marketflow`, or track `.pytest_cache`.
