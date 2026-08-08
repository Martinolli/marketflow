# MarketFlow SWING Registry Approval Candidate Status

## Purpose
- Branch: `feature/swing-registry-approval-candidate-v1`
- Base commit: `f1bab0751507fe65265751e575a6fd70a088f31f`
- Implementation commit: the commit containing this document.
- Purpose: create an offline, digest-bound candidate for future SWING registry approval review.
- This status document does not create SWING registry approval, registry eligibility, or Strategy runtime migration.

## Registry Candidate
- Artifact kind: `SWING_REGISTRY_APPROVAL_CANDIDATE`
- Candidate status: `SWING_REGISTRY_APPROVAL_READY_FOR_OPERATOR_REVIEW`
- Schema version: `swing_registry_approval_candidate_v1`
- Candidate digest: `24dae427c76154ac86f96ce523a793db18b6de592ead261af9e08cf9287e1503`
- Binding mode: `SWING_FROZEN_STATUS_BINDING`
- Proposed registry key: `AAPL:SWING:RTH_HALF_SESSION_195M:2022-01-01:2025-12-31:v1`
- Proposed registry scope: `RESEARCH_DATASET`
- Proposed runtime use: `NOT_AUTHORIZED`
- Proposed strategy use: `NOT_AUTHORIZED`
- Proposed registry activation: `False`
- Requires operator registry review: `True`
- Requires registry approval ceremony: `True`

## Reviewed Dataset Identity
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Ticker: `AAPL`
- Composite FIGI: `BBG000B9XRY4`
- Share class FIGI: `BBG001S5N8V8`
- Primary MIC: `XNAS`
- Security type: `CS`
- Range: `2022-01-01` through `2025-12-31`
- Dataset version candidate: `v1`

## Frozen SWING Evidence
- SWING canonical dataset frozen: `True`
- SWING frozen digest: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`
- SWING review package digest: `1fe4efabfef575956cd4578da5ae060655e420062bf40b24b83cd0d4643bf98d`
- SWING candidate digest: `1bb6e2d7354c30c88e55738e0c549769d9daae678b47899a776de337571cf671`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`

## Dataset Summary
- SWING bar count: `1988`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special-session policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`

## 2025-01 Cross-Check
- Cross-check status: `PASSED`
- Cross-check SWING bars: `40`

## Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition generation frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`

## Dividend Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`
- Source adjusted data used: `True`

## Checklist Summary
- Total checks: `39`
- Passed checks: `39`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator registry review: `True`
- Operator approval required: `True`
- Software registry approval: `False`
- Runtime migration authorized: `False`

## Follow-On Review Package
- Follow-on artifact kind: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE`
- Follow-on review status: `SWING_REGISTRY_APPROVAL_CANDIDATE_REVIEW_PACKAGE_READY`
- Follow-on branch: `feature/swing-registry-operator-review-package-v1`
- Follow-on base commit: `a64ca9374991641b5218afac963c436dae6024a2`
- Review package digest: `ab433bb2c4b58cdd3a6ae287640877a1a8e443a631ebc479bf765f7a8d2b6f9e`
- Review package checklist: `32 total / 32 passed / 0 failed / 0 blockers`
- The registry candidate remains the source evidence for the review package.
- The review package does not create registry approval, registry eligibility, registry activation, or Strategy runtime migration.

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- swing_canonical_dataset_frozen: `True`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- registry_approval_created: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows or SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, or SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No SWING registry approval was created.
- No registry eligibility or active registry entry was created.
- No Strategy runtime migration occurred.
- No predictive-usefulness or profitability acceptance occurred.

## Next Step
- Digest-bound SWING registry approval ceremony remains the next required task after the operator review package.
