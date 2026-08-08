# MarketFlow SWING Canonical Dataset Operator Review Package Status

## Purpose
- Branch: `feature/swing-canonical-dataset-operator-review-package-v1`
- Base commit: `95a9edfeaba9d48e6142dc28ac3185211e01683c`
- Implementation commit: the commit containing this document.
- Purpose: create an offline, digest-bound operator review package for the generated SWING canonical dataset candidate.
- This status document does not create a SWING canonical dataset freeze.

## Review Package
- Artifact kind: `SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE`
- Review status: `SWING_CANONICAL_DATASET_CANDIDATE_REVIEW_PACKAGE_READY`
- Binding mode: `SWING_CANONICAL_DATASET_LOCAL_ARTIFACT_BINDING`
- Review package digest: `1fe4efabfef575956cd4578da5ae060655e420062bf40b24b83cd0d4643bf98d`

## Reviewed SWING Candidate
- SWING candidate digest: `1bb6e2d7354c30c88e55738e0c549769d9daae678b47899a776de337571cf671`
- Candidate kind: `SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- Dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- Source normalized rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`

## Local Artifact Verification
- Ignored candidate path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_candidate.json`
- Candidate file verified: `True`
- Ignored dataset path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- Dataset file verified: `True`
- Ignored manifest path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json`
- Manifest file verified: `True`
- Dataset row count verified: `1988`
- No generated dataset, manifest, or raw OHLCV rows are committed.

## Dataset Summary
- SWING bar count: `1988`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special sessions excluded: `9`
- Special session rows excluded: `126`

## 2025-01 Cross-Check
- Cross-check month: `2025-01`
- Cross-check status: `PASSED`
- Cross-check SWING bars: `40`

## Special-Session Policy
- Policy: `FULL_ORDINARY_SESSIONS_ONLY`
- Special sessions excluded from SWING bars: `True`
- Special sessions recorded in exclusion inventory: `True`
- Special-session exclusion count: `9`
- Special-session rows excluded: `126`

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

## Checklist Summary
- Total checks: `36`
- Passed checks: `36`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator assessment: `True`
- Operator decision required before freeze: `True`
- Software freeze authorized: `False`
- Registry approval authorized: `False`
- Runtime migration authorized: `False`

## Follow-On Freeze Ceremony
- Follow-on branch: `feature/swing-canonical-dataset-operator-freeze-v1`
- Follow-on artifact kind: `SWING_CANONICAL_DATASET_FROZEN`
- Follow-on freeze status: `SWING_CANONICAL_DATASET_FROZEN`
- Frozen semantic digest from deterministic test attestation: `03ce2ae41bf433fce1fd228a8ce03d6adf8591bc5f1eafaf3577e728fdc6402e`
- The review package remains source evidence for the SWING canonical dataset freeze ceremony.
- The freeze ceremony does not create SWING registry approval or Strategy runtime migration.

## Authority Boundary
- identity_segment_frozen: `True`
- calendar_operator_frozen: `True`
- split_event_audit_frozen: `True`
- dividend_event_audit_frozen: `True`
- acquisition_generation_freeze: `True`
- canonical_dataset_frozen: `False`
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
- No `SWING_CANONICAL_DATASET_FROZEN` artifact or status was created.
- No canonical dataset approval, registry eligibility, runtime migration, predictive acceptance, or profitability acceptance occurred.

## Next Step
- SWING registry approval remains a separate future ceremony before any registry eligibility or runtime use.
