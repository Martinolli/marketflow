# MarketFlow SWING Registry Approval v1 Plan

## Purpose
- Create a guarded registry approval path for the frozen AAPL SWING canonical dataset.
- Preserve the authority boundary: registry approval is limited to the `RESEARCH_DATASET` entry and does not migrate runtime behavior, authorize Strategy use, or accept predictive usefulness/profitability.

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
1. `SWING_REGISTRY_APPROVAL_CANDIDATE` - completed.
2. `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE` - implemented.
3. `SWING_REGISTRY_APPROVED` - implemented.

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
- Runtime use is not authorized by the candidate, review package, or approval artifact.
- Strategy use is not authorized by the candidate, review package, or approval artifact.
- Strategy runtime migration remains `False`.
- Registry eligibility is approved only for the `RESEARCH_DATASET` registry entry.
- Registry activation is approved only for the `RESEARCH_DATASET` registry entry.
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

## Current Review Package Status
- Artifact kind: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE`
- Review status: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY`
- Review package digest: `ab433bb2c4b58cdd3a6ae287640877a1a8e443a631ebc479bf765f7a8d2b6f9e`
- Checklist: `32 total / 32 passed / 0 failed / 0 blockers`
- Ready for operator registry assessment: `True`
- Software registry approval authorized: `False`
- Runtime migration authorized: `False`
- Registry approval ceremony is implemented in the follow-on approval artifact.
- Strategy runtime migration remains future work.

## Current Approval Status
- Artifact kind: `SWING_REGISTRY_APPROVED`
- Approval status: `SWING_REGISTRY_APPROVED`
- Registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- Registry approval created: `True`
- Registry eligibility: `True`
- Registry activation: `True`
- Registry scope: `RESEARCH_DATASET`
- Runtime use: `NOT_AUTHORIZED`
- Strategy use: `NOT_AUTHORIZED`
- Strategy runtime migration: `False`
- Predictive usefulness: `not accepted`
- Profitability: `not accepted`
- Checklist: `39 total / 39 passed / 0 failed / 0 blockers`
- Runtime migration remains future work.
- Strategy use remains not authorized.
- POSITION_SWING canonical dataset candidate is next.

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not regenerate SWING bars.
- Do not refresh identity, calendar, split, dividend, acquisition, or SWING evidence.
- Do not authorize runtime or strategy use.
- Do not modify Strategy runtime behavior.
- Do not accept predictive usefulness or profitability.

## Next Tasks
1. POSITION_SWING canonical dataset candidate.
2. POSITION_SWING canonical dataset operator review/freeze.
3. POSITION_SWING registry approval chain.
4. Normal runtime migration.
5. Applicability/research campaign.
6. Predictive and profitability evaluation.
