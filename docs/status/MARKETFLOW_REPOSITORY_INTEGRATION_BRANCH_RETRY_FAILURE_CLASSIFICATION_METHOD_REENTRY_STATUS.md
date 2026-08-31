# MarketFlow Repository Integration Branch Retry Failure Classification Method Reentry v1 Status

## Status and Scope

- Artifact: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_V1`.
- Status: `MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_READY`.
- Scope: `REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_REENTRY_ONLY_NOT_CLASSIFICATION_EXECUTION_NOT_RETRY_NOT_MAIN`.
- Reentry digest: `318c0d1b3f6977a79cd77e8de466286f4057f13d7c7f2bd218c5a561c17e91a6`.
- Source results-review digest: `a49fdccca8caa1961ec4a4cebb133fba296a1e90e54c48e506fd066c70be17a9`.
- Source cache-manifest review digest: `cccebccd618dbc42598a2a2c6efea9ba3c682a95cb36fb6a9de68beef11e22ee`.
- Source execution digest: `b7c987e76b02a026bc118ae05801e4ba02c92bdadb81df9562e28a646b4f80bb`.
- Source classification-source manifest: `9218bad7b0b176bd3b4398293304159f22c1772fad0fa91b6e1d275a770ebcca`.

## Capability and Limitations

The reviewed cache source is accepted only for module-level grouping, node-ID
inventory, bounded module-name root-cause-family hints, and planning a new
classification method candidate. It is not accepted for failure/error
separation, first-failure or first-error ordering, traceback-based root cause,
remediation execution, retry-success evidence, or main-merge approval.

The source remains limited because it cannot distinguish failures from errors,
identify the first failure or error, provide traceback snippets, recommend code
remediation by itself, or replace the authoritative failed retry.

## Reentry Decision

`NEW_CLASSIFICATION_METHOD_CANDIDATE_V2_REQUIRED` is selected. Direct reentry
into the original method is not recommended because that method expected
failure/error separation and first-order trace detail. Diagnostic output
capture remains available but unselected; a retry without classification and a
main merge despite the failed retry remain blocked.

## Future Method v2

The future v2 method must remain digest-bound and limited to cache-supported
claims. Its candidate plan may define node-ID inventory, module grouping,
module-name-only family hints, evidence-root/path/cwd/digest-drift candidate
mappings, and a fallback diagnostic-output-capture package. The plan status is
`PLANNED_NOT_EXECUTED`; operator review and approval are required before any v2
execution.

## Authority Boundary

All `61/61` checks pass with zero failures or blockers, and all 49 risk controls
are defined. The reentry does not read cache, classify modules, execute a
classification method, rerun pytest, run diagnostics, create a retry candidate
or results review, mark integration successful, push protected branches, commit
`.marketflow` or `.pytest_cache`, call providers, acquire or regenerate data,
accept predictive usefulness or profitability, or authorize runtime or trading.

## Next Task

`MARKETFLOW_REPOSITORY_INTEGRATION_BRANCH_RETRY_FAILURE_CLASSIFICATION_METHOD_CANDIDATE_V2`
may be invoked separately.

## Follow-on Classification Method Candidate v2

`MarketFlow Repository Integration Branch Retry Failure Classification Method
Candidate v2` is implemented as the offline, digest-bound follow-on. This
classification-method reentry remains its source evidence. Candidate v2
proposes cache-supported module-level node-ID classification packages only and
keeps the recommended package unselected pending operator review.

Candidate v2 does not read cache, execute classification, rerun the retry or
full pytest, run diagnostics, create a retry candidate, push main or integration,
commit `.marketflow` or `.pytest_cache`, accept predictive usefulness or
profitability, or authorize runtime or trading.
