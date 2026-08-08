# MarketFlow POSITION_SWING Canonical Dataset Candidate Status

## Candidate Status
- Branch: `feature/position-swing-canonical-dataset-candidate-v1`
- Base commit: `42d994158c0ffb82c097cf9b008ec6b7e598960b`
- Implementation commit: the commit containing this document.
- Artifact kind: `POSITION_SWING_CANONICAL_DATASET_CANDIDATE`
- Candidate status: `POSITION_SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- Schema version: `position_swing_canonical_dataset_candidate_v1`
- Candidate digest: `ed16a41304a4d3838f495124a9d491e834eba0dd4a1ff8009e456963ecc2c916`
- Candidate receipt digest: `e85b30b71a1202d277b46b596ce4d4cb90e95b3f7ec488bced65f119ae3d369f`

## Source Rows
- Source rows path: `.marketflow\frozen_acquisition_sources\AAPL\2022_2025\AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv`
- Source rows digest verified: `True`
- Expected normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Actual normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Source rows total: `63804`
- Source RTH rows total: `25970`
- Source extended-hours rows total: `37834`
- Source unknown rows total: `0`

## Frozen Acquisition Binding
- Acquisition frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`
- Monthly reconciliation digest: `d34effcf3129d630f14c61f5d0621aa0d89cdc51471f65f3d5effabeb42f16a4`
- Acquisition receipt digest: `63b1934fbaf4b146fadcfbb5cb4649e18b1e91d8d304cf3afdee71220d005eed`
- Targeted diagnostic receipt digest: `82ec97bbc5eba73a275cc8221bb4a59235ed093a6e6dbe14058eac26980d26c8`
- Per-session diagnostics digest: `f810bfd3fcb1d2056bbf5ba0cff8b1aa4276119721c697ce17eaef6bab069faa`

## Dataset Profile
- Dataset profile: `POSITION_SWING`
- Dataset bar rule: `RTH_FULL_SESSION_1D`
- Full ordinary RTH session length: `390` minutes
- Source rows per POSITION_SWING bar: `26`
- POSITION_SWING bars per full session: `1`

## Dataset Summary
- POSITION_SWING bar count: `994`
- Source RTH rows consumed: `25844`
- Source RTH rows excluded: `126`
- Full sessions used: `994`
- Special sessions excluded: `9`
- Special-session rows excluded: `126`
- Invalid sessions: `0`
- First bar timestamp UTC: `2022-01-03T14:30:00Z`
- Last bar timestamp UTC: `2025-12-31T14:30:00Z`
- Dataset rows digest: `163d26fb50bbc0defb0f0602922fb672a6b404d43d920c9f018053fec2862ab3`
- Dataset manifest digest: `720c7314ba86b20fde05c16f69870a4cfd218eb6c317ff592efd5fd1885776ba`

## 2025-01 Cross-Check
- Expected full ordinary sessions: `20`
- Expected source RTH rows: `520`
- Expected POSITION_SWING bars: `20`
- Actual POSITION_SWING bars: `20`
- Cross-check result: `PASSED`

## Special-Session Policy
- full_ordinary_sessions_only_for_RTH_FULL_SESSION_1D: `True`
- special_sessions_excluded_from_position_swing_bars: `True`
- special_sessions_recorded_in_exclusion_inventory: `True`
- Special-session exclusion reason: `SPECIAL_SESSION_EXCLUDED_BY_CONSERVATIVE_FULL_SESSION_ONLY_POLICY`

## Ignored Outputs
- Ignored dataset output path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025.csv`
- Ignored manifest output path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_manifest.json`
- Ignored candidate output path: `.marketflow\canonical_candidates\AAPL\POSITION_SWING\AAPL_POSITION_SWING_RTH_FULL_SESSION_1D_2022_2025_candidate.json`
- Raw OHLCV rows are not included in this status document.

## Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`

## Dividend Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`
- Source adjusted data used: `True`

## Authority Boundary
- created_offline: `True`
- provider_requests_made: `False`
- position_swing_canonical_dataset_frozen: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- runtime_use: `NOT_AUTHORIZED`
- strategy_use: `NOT_AUTHORIZED`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Non-Goals
- No Massive.com / Polygon provider request was made.
- No acquisition rows were regenerated.
- No identity, calendar, split, dividend, acquisition, or SWING evidence was refreshed.
- No generated dataset, manifest, or raw OHLCV rows are committed.
- No `POSITION_SWING_CANONICAL_DATASET_FROZEN` artifact was created.
- No `POSITION_SWING_REGISTRY_APPROVED` artifact was created.
- No registry/runtime eligibility or Strategy runtime migration occurred.
- No predictive-usefulness or profitability acceptance occurred.

## Next Task Recommendation
- POSITION_SWING operator review package.
