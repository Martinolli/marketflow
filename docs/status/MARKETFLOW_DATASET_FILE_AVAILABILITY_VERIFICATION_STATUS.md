# MarketFlow Dataset File Availability Verification Status

## Purpose
- Branch: `feature/dataset-file-availability-verification-v1`
- Base commit: `7d3f3dbed8efe3ffcf64c86f99454729951378cd`
- Implementation commit: the commit containing this document.
- Purpose: verify local research dataset and manifest file availability without changing runtime defaults.
- This package does not approve or activate runtime migration.

## Verification Package
- Artifact kind: `DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE`
- Package status: `DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW`
- Schema version: `dataset_file_availability_verification_package_v1`
- Package digest: `8ba7db3aa50eb858f7eebb10eb6ee1a554a97b43a789c93460ff276cadc96751`
- Created offline: `True`
- Provider requests made: `False`
- File system verification performed: `True`
- Operator review required: `True`

## Source Review Evidence
- Read-only discovery candidate digest: `b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1`
- Read-only discovery review package digest: `299eb78d52e598e690db501b10ea88390ff6848a217640022e56251c41584021`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`

## Files Verified
- SWING dataset: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- SWING dataset file SHA-256: `287bb55dc9bed318fde9170e07db8a7bbd397f46376ae8a3786d43978551e9bb`
- SWING manifest: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json`
- SWING manifest file SHA-256: `0b8da42abf1bbd34b7aeba4cdc20408a7d412cf00ec29204065793b380cd7bc1`
- POSITION_SWING dataset: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- POSITION_SWING dataset file SHA-256: `3a12b5ab5ab3a269f07b77cae2a52954069c0722be1df815c412eab6014e521c`
- POSITION_SWING manifest: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json`
- POSITION_SWING manifest file SHA-256: `746456606a0c476476f1f900aaea85f60eac1a06315f2527aca8ded371079c6d`

## Digest Verification Summary
- SWING file verification status: `AVAILABLE_AND_DIGEST_VERIFIED`
- SWING dataset rows digest match: `True`
- SWING dataset manifest digest match: `True`
- POSITION_SWING file verification status: `AVAILABLE_AND_DIGEST_VERIFIED`
- POSITION_SWING dataset rows digest match: `True`
- POSITION_SWING dataset manifest digest match: `True`
- Verification entry count: `2`
- Dataset files available: `2`
- Manifest files available: `2`
- Dataset digests verified: `2`
- Manifest digests verified: `2`
- Missing files: `0`
- Digest mismatches: `0`
- Ready for research campaign planning: `True`
- Ready for runtime migration: `False`

## Runtime Boundary
- runtime_migration_approved: `False`
- runtime_migration_active: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- paper_trading: `NOT_AUTHORIZED`
- broker_execution: `NOT_AUTHORIZED`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Checklist Summary
- Total checks: `26`
- Passed checks: `26`
- Failed checks: `0`
- Blocker count: `0`
- Ready for operator review: `True`
- Runtime migration authorized: `False`
- Software runtime activation authorized: `False`

## Authority Boundary
- No `RUNTIME_MIGRATION_APPROVED` artifact or status is created.
- No `RUNTIME_MIGRATION_ACTIVE` artifact or status is created.
- No `STRATEGY_RUNTIME_MIGRATION` artifact or status is created.
- Runtime, Strategy, paper trading, and broker execution use remain `NOT_AUTHORIZED`.
- This package is evidence for operator assessment only.

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows, SWING bars, or POSITION_SWING bars were regenerated.
- No identity, calendar, split, dividend, acquisition, SWING, or POSITION_SWING evidence was refreshed.
- No Strategy runtime behavior was modified.
- No runtime, Strategy, paper trading, or broker execution use was authorized.
- No predictive-usefulness or profitability acceptance occurred.

## Next Task Recommendation
- Dataset file availability verification operator review package.
