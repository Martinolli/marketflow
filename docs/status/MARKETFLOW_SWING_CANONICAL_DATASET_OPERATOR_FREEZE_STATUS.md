# MarketFlow SWING Canonical Dataset Operator Freeze Status

## Purpose
- Branch: `feature/swing-canonical-dataset-operator-freeze-v1`
- Base commit: `9335383688a6ae753e9260c90027e90cc4f1fbee`
- Implementation commit: the commit containing this document.
- Purpose: create an offline, digest-bound operator freeze ceremony for the reviewed SWING canonical dataset candidate.
- This status document records the SWING dataset freeze ceremony only; it does not create registry approval or runtime migration.

## Frozen SWING Canonical Dataset
- Artifact kind: `SWING_CANONICAL_DATASET_FROZEN`
- Freeze status: `SWING_CANONICAL_DATASET_FROZEN`
- Schema version: `swing_canonical_dataset_operator_freeze_v1`
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Frozen semantic digest from deterministic test attestation: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`

## Operator Attestation Requirement
- Required decision: `APPROVE_SWING_CANONICAL_DATASET_FREEZE`
- Required attestation version: `swing_canonical_dataset_operator_attestation_v1`
- Required phrase: `FREEZE SWING CANONICAL DATASET AAPL BBG000B9XRY4 BBG001S5N8V8 XNAS CS 2022-01-01 2025-12-31 RTH_HALF_SESSION_195M 1988_BARS`
- Operator reference is non-secret and may be `TEST_OPERATOR` in tests.
- The attestation must confirm the SWING review package digest, candidate digest, dataset rows digest, dataset manifest digest, source rows digest, materialization receipt digest, acquisition generation digest, authority digests, bar count, 2025-01 cross-check, special-session policy, dividend implication, and boundary guardrails.

## Source SWING Review Package
- Source review package kind: `SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE`
- Source review status: `SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY`
- SWING review package digest: `1fe4efabfef575956cd4578da5ae060655e420062bf40b24b83cd0d4643bf98d`
- Review checklist: `36 total / 36 passed / 0 failed / 0 blockers`
- The review package remains source evidence for the freeze ceremony.

## Dataset Evidence
- SWING candidate digest: `1bb6e2d7354c30c88e55738e0c549769d9daae678b47899a776de337571cf671`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Source normalized rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- SWING bar count: `1988`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`

## 2025-01 Cross-Check
- Cross-check status: `PASSED`
- Cross-check SWING bars: `40`

## Special-Session Policy
- Policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`
- Special sessions remain excluded under the conservative full-ordinary-session-only SWING policy.

## Frozen Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition generation frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`

## Dividend Adjustment Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`
- Source adjusted data used: `True`

## Freeze Checklist Summary
- Total checks: `52`
- Passed checks: `52`
- Failed checks: `0`
- Blocker count: `0`
- SWING canonical dataset freeze authorized by operator: `True`
- Software auto approval: `False`
- Registry approval authorized: `False`
- Runtime migration authorized: `False`

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- swing_canonical_dataset_frozen: `True`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition bars or SWING bars were regenerated.
- No identity, calendar, split, dividend, or acquisition evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No SWING registry approval was created.
- No Strategy runtime migration occurred.
- No predictive-usefulness or profitability acceptance occurred.
- No broker, trading, tax, IBKR, or personal financial information is required or stored.

## Next Step
- SWING registry approval remains a separate future ceremony before any registry eligibility or runtime use.
