# MarketFlow POSITION_SWING Registry Approval v1 Plan

## Purpose
- Move the frozen POSITION_SWING canonical dataset toward registry approval through a controlled candidate, operator review package, and explicit approval ceremony.
- Preserve research-only scope until a separate operator approval ceremony is completed.
- Keep runtime use, Strategy use, broker/trading use, predictive usefulness, and profitability outside this candidate.

## Prerequisite POSITION_SWING Frozen Dataset
- Required artifact kind: `POSITION_SWING_CANONICAL_DATASET_FROZEN`
- Required frozen digest: `d95b61fd857eec3271fd6172225ad2efc9cafc78726b55eef666f05d183147f8`
- Required dataset profile/rule: `POSITION_SWING` / `RTH_FULL_SESSION_1D`
- Required dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- Required dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- Required POSITION_SWING bars: `994`
- Required 2025-01 cross-check: `PASSED`, `20` bars.

## Candidate Status
- Artifact kind: `POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE`
- Candidate status: `POSITION_SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW`
- Candidate digest: `3987efa860732c113a1f5037ef0ccca9b261f10b7602b52b6866bf7f4a8a3511`
- Checklist result: `40` passed / `0` failed / `0` blockers.
- Binding mode: `POSITION_SWING_FROZEN_STATUS_BINDING`

## Proposed Registry Entry
- Proposed registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- Proposed registry scope: `RESEARCH_DATASET`
- Proposed runtime use: `NOT_AUTHORIZED`
- Proposed strategy use: `NOT_AUTHORIZED`
- Proposed registry activation: `False`
- Requires operator registry review: `True`
- Requires registry approval ceremony: `True`

## Required Sequence
1. POSITION_SWING registry approval candidate.
2. POSITION_SWING registry operator review package.
3. POSITION_SWING registry approval ceremony.
4. Normal runtime migration planning.

## Authority Boundary
- position_swing_canonical_dataset_frozen: `True`
- position_swing_registry_approval_created: `False`
- position_swing_registry_eligibility: `False`
- position_swing_registry_activation: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not regenerate POSITION_SWING bars.
- Do not refresh identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence.
- Do not create `POSITION_SWING_REGISTRY_APPROVED`.
- Do not approve registry/runtime eligibility.
- Do not activate the registry entry.
- Do not mark POSITION_SWING as runtime-default or production Strategy input.
- Do not modify Strategy runtime behavior.
- Do not accept predictive usefulness or profitability.
- Do not commit generated dataset CSVs or manifests.

## Next Tasks
1. POSITION_SWING registry operator review package.
2. POSITION_SWING registry approval ceremony.
3. Normal runtime migration planning.
