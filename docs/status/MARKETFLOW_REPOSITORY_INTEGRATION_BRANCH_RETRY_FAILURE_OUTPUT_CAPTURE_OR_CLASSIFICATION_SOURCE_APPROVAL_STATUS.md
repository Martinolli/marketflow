# MarketFlow Repository Integration Branch Retry Failure Output Capture or Classification Source Approval v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVED`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVED`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_APPROVAL_ONLY_NOT_EXECUTION_NOT_RETRY_NOT_RESULTS_REVIEW_NOT_MAIN`.
- Approval digest: `41052b8621f57721383bc7d8fc416c95e9fef4d5af49b94278ede43209304d33`.
- Source operator-review digest: `f73a94b36e7884d778c980d4989c999c383a04310f45e58b6ffae9da6172aa8c`.
- Source output-capture candidate digest: `fa120413e47e6f457eb98b0bbe02d2bad57d42a996aeb01846eb2b3a616e8518`.
- Source method-execution digest: `522b4ff6e7345e6e3c8102d91dbbed273b8e0ac7b7161fb6653b915b929f9562`.
- Source blocked-manifest digest: `3495918d5fa489a6f2496084fa5f024638ea86f587fe6d71826288c325c38a5f`.

## Operator Attestation and Selected Package

The approval requires the exact non-secret operator decision, phrase, digest
bindings, retry-failure facts, detached-worktree identity, selected package,
and closed-boundary confirmations defined by the service. It selects
`PACKAGE_READ_EXISTING_DETACHED_PYTEST_CACHE_LASTFAILED_AS_CLASSIFICATION_SOURCE`
as `APPROVED_FOR_FUTURE_OUTPUT_CAPTURE_EXECUTION_ONLY`.

Selection, approval, authorization, and readiness for a separate execution
task are true. The approval itself does not read `.pytest_cache`, parse an
operator log, run diagnostics, capture output, or execute a retry.

## Retry Failure Boundary

The authoritative detached-worktree retry remains `24877 passed, 1292 failed,
112 errors, 7 skipped` at retry execution commit
`ab178b65c69f0274b0abbf9c20df102d35e78d34`. Detailed output remains unavailable
under `AUTHORITATIVE_RETRY_OUTPUT_DETAIL_NOT_PERSISTED_OR_NOT_LOCATABLE`.
The latest prior root regression remains `29323 passed, 7 skipped`; it is not
retry evidence and does not override the detached failure.

## Approved Future Contract

All eighteen reviewed requirements and all ten future plan steps are approved
for future output-capture execution only; plan execution remains
`NOT_EXECUTED`. All nine planned outputs are `AUTHORIZED_NOT_GENERATED`.
Three supporting packages remain available but unselected, including the
high-control diagnostic package. Four insufficient or unsafe packages remain
`BLOCKED_NOT_APPROVED`.

## Checklist and Authority Boundary

All `62/62` checks pass with zero failures or blockers. No output capture,
cache read, log parse, diagnostic command, retry/full pytest, results review,
integration success, successful integration digest, new retry candidate,
main-merge approval, evidence mutation, `.marketflow` commit, provider/data/model
action, protected-branch push, deletion, tag mutation,
predictive/profitability acceptance, runtime authority, or broker authority is
created.

## Next Task

The separately invoked next task is
`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_OUTPUT_CAPTURE_OR_CLASSIFICATION_SOURCE_EXECUTION_V1`.

## Follow-on Execution

`MarketFlow Repository Integration Branch Retry Failure Output Capture or
Classification Source Execution v1` is implemented as the separately
authorized follow-on, and this approval remains its source evidence. The
execution reads only the existing detached pytest-cache `lastfailed` source
and optional `nodeids` inventory. It does not rerun the retry or full pytest,
execute diagnostics, parse operator logs, create a retry results review, push
main or integration, commit `.marketflow` or `.pytest_cache`, accept predictive
usefulness or profitability, or authorize runtime or trading.
