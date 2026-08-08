# MarketFlow Dataset File Availability Verification v1 Plan

## Purpose
- Create an offline, digest-bound verification package for local research dataset and manifest files.
- Bind verification to the completed read-only registry discovery review package.
- Preserve current runtime defaults and Strategy inputs.
- Keep runtime migration, paper trading, broker execution, predictive usefulness, and profitability outside this artifact.

## Prerequisite Read-Only Registry Discovery Review
- Read-only discovery candidate digest: `b2c46f880b3764e31d159f4c344004dbb104a3a1129e97499aafc0a7b6ef8bc1`
- Read-only discovery review package digest: `299eb78d52e598e690db501b10ea88390ff6848a217640022e56251c41584021`
- SWING registry approval digest: `ee3f6b193a6480fb6391fd97b096dda8fc699d65e43a179c77bba8798f887761`
- POSITION_SWING registry approval digest: `8eefcbc1e14b2e199dadd8dcf461cbff56513f10758b6b59ca8cf176512d2e8e`

## Verification Package
- Artifact kind: `DATASET_FILE_AVAILABILITY_VERIFICATION_PACKAGE`
- Package status: `DATASET_FILE_AVAILABILITY_VERIFICATION_READY_FOR_OPERATOR_REVIEW`
- Schema version: `dataset_file_availability_verification_package_v1`
- Package digest: `8ba7db3aa50eb858f7eebb10eb6ee1a554a97b43a789c93460ff276cadc96751`
- Verification entry count: `2`
- Ready for research campaign planning: `True`
- Ready for runtime migration: `False`

## Dataset File Existence Verification
- SWING dataset path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025.csv`
- SWING dataset file status: `AVAILABLE_AND_DIGEST_VERIFIED`
- SWING dataset file SHA-256: `287bb55dc9bed318fde9170e07db8a7bbd397f46376ae8a3786d43978551e9bb`
- SWING manifest path: `.marketflow/canonical_candidates/AAPL/SWING/AAPL_SWING_RTH_HALF_SESSION_195M_2022_2025_manifest.json`
- SWING manifest file status: `AVAILABLE_AND_DIGEST_VERIFIED`
- SWING manifest file SHA-256: `0b8da42abf1bbd34b7aeba4cdc20408a7d412cf00ec29204065793b380cd7bc1`
- POSITION_SWING dataset path: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- POSITION_SWING dataset file status: `AVAILABLE_AND_DIGEST_VERIFIED`
- POSITION_SWING dataset file SHA-256: `3a12b5ab5ab3a269f07b77cae2a52954069c0722be1df815c412eab6014e521c`
- POSITION_SWING manifest path: `.marketflow/canonical_candidates/AAPL/POSITION_SWING/AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json`
- POSITION_SWING manifest file status: `AVAILABLE_AND_DIGEST_VERIFIED`
- POSITION_SWING manifest file SHA-256: `746456606a0c476476f1f900aaea85f60eac1a06315f2527aca8ded371079c6d`

## Digest Verification
- SWING dataset rows digest: `e449f54e53a7dd538ede0b396205253c96aefdb70081f34df60b3b8bd73232bc`
- SWING dataset manifest digest: `0736b42eb806c172ad2267121895955c99a5ff19554f77d79ea86807273752ae`
- POSITION_SWING dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- POSITION_SWING dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`
- Dataset files available: `2`
- Manifest files available: `2`
- Dataset digests verified: `2`
- Manifest digests verified: `2`
- Missing files: `0`
- Digest mismatches: `0`

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

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition rows.
- Do not regenerate SWING or POSITION_SWING bars.
- Do not alter current operational behavior.
- Do not approve runtime migration.
- Do not activate runtime migration.
- Do not enable paper trading or broker execution.
- Do not claim predictive usefulness or profitability.

## Next Tasks
1. Dataset file availability verification operator review package.
2. Research-only applicability campaign plan.
3. Research-only applicability campaign execution.
