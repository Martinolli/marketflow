# MarketFlow SWING Registry Approval Status

## Purpose
- Branch: `feature/swing-registry-approval-ceremony-v1`
- Base commit: `e5e770f0c1586610d103c4aa7cacaa2b3965edae`
- Implementation commit: the commit containing this document.
- Purpose: create the offline, operator-attested approval ceremony for the AAPL SWING research registry entry.
- This status document does not authorize Strategy runtime use, broker/trading use, predictive usefulness, or profitability.

## Registry Approval
- Artifact kind: `SWING_REGISTRY_APPROVED`
- Approval status: `SWING_REGISTRY_APPROVED`
- Schema version: `swing_registry_approval_v1`
- Registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- Registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- Registry scope: `RESEARCH_DATASET`
- Registry approval created: `True`
- Registry eligibility: `True`
- Registry activation: `True`

## Source Registry Review Package
- Source review package kind: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE`
- Source review status: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY`
- Source review package digest: `ab433bb2c4b58cdd3a6ae287640877a1a8e443a631ebc479bf765f7a8d2b6f9e`
- Source review checklist: `32 total / 32 passed / 0 failed / 0 blockers`

## Source Registry Candidate
- Source registry candidate kind: `SWING_REGISTRY_APPROVAL_CANDIDATE`
- Source registry candidate status: `SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW`
- Source registry candidate digest: `24dae427c76154ac86f96ce523a793db18b6de592ead261af9e08cf9287e1503`

## Frozen SWING Dataset Evidence
- SWING canonical dataset frozen: `True`
- SWING frozen digest: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- SWING bar count: `1988`

## Dataset Summary
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special-session policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`
- 2025-01 cross-check: `PASSED`, `40` SWING bars

## Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition generation frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`

## Runtime And Strategy Boundary
- Runtime use: `NOT_AUTHORIZED`
- Strategy use: `NOT_AUTHORIZED`
- Strategy runtime migration: `False`
- Automatic stitching: `False`
- Predictive usefulness: `not accepted`
- Profitability: `not accepted`
- Provider requests made in approval: `False`
- Created offline: `True`

## Approval Checklist Summary
- Total checks: `39`
- Passed checks: `39`
- Failed checks: `0`
- Blocker count: `0`
- SWING registry approval authorized by operator: `True`
- Software runtime migration authorized: `False`
- Software strategy use authorized: `False`

## Follow-On Runtime Migration Planning
- Follow-on artifact kind: `RUNTIME_MIGRATION_PLAN_CANDIDATE`
- Follow-on plan status: `RUNTIME_MIGRATION_PLAN_READY_FOR_OPERATOR_REVIEW`
- Follow-on branch: `feature/runtime-migration-planning-v1`
- Follow-on base commit: `7736d486d0bee974f7fa478ac9e03c1b80bea0f2`
- Runtime migration plan candidate digest: `f1b7b1456b69774c6e19fa81cf11a319ff5b9c2a9cc75410b7873ed9417e68a5`
- Plan checklist: `24 total / 24 passed / 0 failed / 0 blockers`
- The SWING registry approval remains research-scope only.
- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.

## Follow-On POSITION_SWING Candidate
- Follow-on artifact kind: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE`
- Follow-on candidate status: `POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Follow-on branch: `feature/position-swing-canonical-dataset-candidate-v1`
- Follow-on base commit: `42d994158c0ffb82c097cf9b008ec6b7e598960b`
- POSITION_SWING candidate digest: `ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916`
- POSITION_SWING dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- POSITION_SWING dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- POSITION_SWING bar count: `994`
- The SWING registry approval remains limited to research scope and is not runtime authorized.
- The POSITION_SWING candidate does not create a canonical freeze, registry approval, runtime authorization, Strategy authorization, predictive acceptance, or profitability acceptance.

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows or SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, or SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No Strategy runtime behavior was modified.
- No runtime or strategy use was authorized.
- No broker/trading use was authorized.
- No predictive-usefulness or profitability acceptance occurred.
- No POSITION_SWING canonical freeze, registry approval, or runtime migration was created.

## Next Step
- Runtime migration operator review package remains future work.
