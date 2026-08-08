# MarketFlow POSITION_SWING Registry Approval Status

## Purpose
- Branch: `feature/position-swing-registry-approval-ceremony-v1`
- Base commit: `83ab4b1f239df3f6bdcab2ce365308feb450a8df`
- Implementation commit: the commit containing this document.
- Purpose: create a guarded offline approval ceremony for the POSITION_SWING research registry entry.
- This status document does not authorize Strategy runtime use, broker/trading use, predictive usefulness, or profitability.

## Approved Registry Entry
- Artifact kind: `POSITION_SWING_REGISTRY_APPROVED`
- Approval status: `POSITION_SWING_REGISTRY_APPROVED`
- Schema version: `position_swing_registry_approval_v1`
- Registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`
- Registry key: `AAPL:POSITION_SWING:RTH_FULL_SESSION_1D:2022-01-01:2025-12-31:v1`
- Registry scope: `RESEARCH_DATASET`
- POSITION_SWING registry approval created: `True`
- POSITION_SWING registry eligibility: `True`
- POSITION_SWING registry activation: `True`

## Source Registry Review Package
- Source review package kind: `POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE`
- Source review status: `POSITION_SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY`
- Source registry review package digest: `db8dc9c15d9ed5a1edd2756fc5e5d1a5cfe157eac0e2ac36dbb2cc0faefe233e`
- Source registry candidate digest: `3987efa860732c113a1f5037ef0ccca9b261f10b7602b52b6866bf7f4a8a3511`
- Source review checklist: `34 total / 34 passed / 0 failed / 0 blockers`

## Frozen POSITION_SWING Dataset Evidence
- POSITION_SWING canonical dataset frozen: `True`
- POSITION_SWING frozen digest: `d95b61fd857eec3271fd6172225ad2efc9cafc78726b55eef666f05d183147f8`
- POSITION_SWING review package digest: `142d35d8b622e2f2db77fa07f48d3bf307126d5b25c6c0a72086d6d7ce4de8ea`
- POSITION_SWING candidate digest: `ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916`
- Dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- Dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- Source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- Dataset profile: `POSITION_SWING`
- Dataset bar rule: `RTH_FULL_SESSION_1D`
- POSITION_SWING bar count: `994`

## Dataset Summary
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special-session policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`
- 2025-01 cross-check: `PASSED`, `20` POSITION_SWING bars

## Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition generation frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- SWING canonical dataset frozen digest: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`

## Dividend Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`
- Source adjusted data used: `True`

## Approval Checklist Summary
- Total checks: `40`
- Passed checks: `40`
- Failed checks: `0`
- Blocker count: `0`
- POSITION_SWING registry approval authorized by operator: `True`
- Runtime migration authorized: `False`
- Strategy use authorized: `False`

## Runtime Boundary
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- swing_canonical_dataset_frozen: `True`
- swing_registry_approval_created: `True`
- swing_registry_eligibility: `True`
- swing_registry_activation: `True`
- position_swing_canonical_dataset_frozen: `True`
- position_swing_registry_approval_created: `True`
- position_swing_registry_eligibility: `True`
- position_swing_registry_activation: `True`
- created_offline: `True`
- provider_requests_made_in_approval: `False`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows or POSITION_SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No Strategy runtime migration occurred.
- No POSITION_SWING runtime-default source was selected.
- No broker/trading authorization occurred.
- No predictive-usefulness or profitability acceptance occurred.

## Next Step
- Normal runtime migration planning remains future work.
