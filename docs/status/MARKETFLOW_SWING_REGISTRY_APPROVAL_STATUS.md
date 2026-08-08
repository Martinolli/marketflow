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

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows or SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, or SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No Strategy runtime behavior was modified.
- No runtime or strategy use was authorized.
- No broker/trading use was authorized.
- No predictive-usefulness or profitability acceptance occurred.
- No POSITION_SWING dataset was created.

## Next Step
- POSITION_SWING canonical dataset candidate remains the next required task.
