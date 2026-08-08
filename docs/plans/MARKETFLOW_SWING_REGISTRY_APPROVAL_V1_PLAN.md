# MarketFlow SWING Registry Approval v1 Plan

## Purpose
- Create a candidate-only registry approval path for the frozen AAPL SWING canonical dataset.
- Preserve the authority boundary: the candidate does not approve registry eligibility, activate a registry entry, migrate runtime behavior, or accept predictive usefulness/profitability.

## Prerequisite SWING Frozen Dataset
- Required frozen artifact: `SWING_CANONICAL_DATASET_FROZEN`
- Required frozen digest: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`
- Source review package digest: `1fe4efabfef575956cd4578da5ae060655e420062bf40b24b83cd0d4643bf98d`
- SWING candidate digest: `1bb6e2d7354c30c88e55738e0c549769d9daae678b47899a776de337571cf671`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`

## Candidate / Review / Approval Sequence
1. `SWING_REGISTRY_APPROVAL_CANDIDATE`
2. SWING registry operator review package.
3. SWING registry approval ceremony.

## Registry Candidate Scope
- Registry candidate profile: `SWING`
- Registry candidate dataset rule: `RTH_HALF_SESSION_195M`
- Registry candidate ticker: `AAPL`
- Registry candidate range: `2022-01-01` through `2025-12-31`
- Registry candidate version: `v1`
- Proposed registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- Proposed registry scope: `RESEARCH_DATASET`
- Proposed runtime use: `NOT_AUTHORIZED`
- Proposed strategy use: `NOT_AUTHORIZED`
- Proposed registry activation: `False`

## Runtime Boundary
- Runtime use is not authorized by the candidate.
- Strategy use is not authorized by the candidate.
- Strategy runtime migration remains `False`.
- Registry eligibility remains `False`.
- Canonical eligibility remains `False`.
- Predictive usefulness remains `not accepted`.
- Profitability remains `not accepted`.

## Current Candidate Status
- Artifact kind: `SWING_REGISTRY_APPROVAL_CANDIDATE`
- Candidate status: `SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `24dae427c76154ac86f96ce523a793db18b6de592ead261af9e08cf9287e1503`
- Checklist: `39 total / 39 passed / 0 failed / 0 blockers`
- Ready for operator registry review: `True`
- Software registry approval: `False`
- Runtime migration authorized: `False`

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not regenerate SWING bars.
- Do not refresh identity, calendar, split, dividend, acquisition, or SWING evidence.
- Do not create `SWING_REGISTRY_APPROVED`.
- Do not set `REGISTRY_ELIGIBLE`.
- Do not create an active registry entry.
- Do not modify Strategy runtime behavior.
- Do not accept predictive usefulness or profitability.

## Next Tasks
1. SWING registry operator review package.
2. SWING registry approval ceremony.
3. POSITION_SWING canonical dataset candidate.
