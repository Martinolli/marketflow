# MarketFlow SWING Canonical Dataset v1 Plan

## Purpose
- Create a candidate-only canonical SWING dataset artifact derived from the frozen AAPL 15-minute adjusted acquisition generation.
- Preserve the authority boundary: this candidate does not freeze a canonical dataset, approve registry eligibility, migrate runtime behavior, or accept predictive usefulness/profitability.

## Prerequisite Frozen Acquisition Generation
- Required frozen artifact: `ACQUISITION_GENERATION_FROZEN`
- Required frozen digest: `df3e1d1278b0d0738effbb0ed64e6de223426402852ed949cab30cf4379b0118`
- Required normalized source rows digest: `0844164e1056732b0a887f19e569312cebab51e2e9c3db787415b4f56d533bdc`
- Source range: `2022-01-01` through `2025-12-31`
- Source ticker: `AAPL`
- Source rows: `63804 total / 25970 RTH / 37834 extended-hours / 0 unknown`
- Calendar binding: frozen `XNAS -> XNYS` schedule
- Source row materialization completed: `ACQUISITION_FROZEN_SOURCE_ROWS_MATERIALIZED`
- Materialized source rows path: `.marketflow/frozen_acquisition_sources/AAPL/2022_2025/AAPL_15m_adjusted_2022_2025_normalized_source_rows.csv`
- Materialization receipt digest: `d331e52034dc8ab47df225347243df370063fc25b18338b49b42d038810dfd54`

## SWING Bar Rule
- Dataset profile: `SWING`
- Dataset bar rule: `RTH_HALF_SESSION_195M`
- Source interval: `15` minutes
- Full ordinary RTH session length: `390` minutes
- Source RTH rows per full session: `26`
- SWING bars per full ordinary session: `2`
- Source rows per SWING bar: `13`
- Canonical storage timezone: `UTC`

## Full-Session Aggregation Logic
- Bar 1 spans session open through open plus `195` minutes.
- Bar 2 spans open plus `195` minutes through session close.
- Open is the first source-row open.
- High is the maximum source-row high.
- Low is the minimum source-row low.
- Close is the last source-row close.
- Volume is the sum of source-row volume.
- Transactions are summed when available.
- VWAP is volume-weighted when source VWAP and volume are available; otherwise it is `null`.
- Bars include source count, first source timestamp, and last source timestamp evidence.

## Special-Session Policy
- `full_ordinary_sessions_only_for_RTH_HALF_SESSION_195M = true`
- `special_sessions_excluded_from_swing_bars = true`
- `special_sessions_recorded_in_exclusion_inventory = true`
- Special/early-close sessions are excluded from SWING bars and recorded in an exclusion inventory.
- Excluded special sessions are not provider data defects.

## 2025-01 Cross-Check
- Expected full ordinary sessions: `20`
- Expected incomplete ordinary sessions: `0`
- Expected source RTH rows: `520`
- Expected SWING bars: `40`
- Expected POSITION_SWING full-session bars: `20`
- The candidate may report this cross-check as passed only when verified row-level source data is available or fixture-derived in tests.

## Candidate-Only Status
- Current local status: `SWING_CANONICAL_DATASET_READY_FOR_OPERATOR_REVIEW`
- The candidate rerun used the verified materialized frozen source rows and did not call Massive.com / Polygon.
- Generated SWING dataset output is ignored under `.marketflow/canonical_candidates/AAPL/SWING/`.
- Special sessions remain excluded under the conservative full-ordinary-session-only policy and are recorded in the exclusion inventory.
- This ready candidate is not a canonical dataset freeze, registry approval, runtime migration, predictive-usefulness acceptance, or profitability acceptance.

## Non-Goals
- Do not call Massive.com / Polygon.
- Do not fetch provider data.
- Do not regenerate acquisition bars.
- Do not refresh identity, calendar, split, or dividend evidence.
- Do not create `SWING_CANONICAL_DATASET_FROZEN`.
- Do not set `REGISTRY_ELIGIBLE` or `CANONICAL_DATASET_APPROVED`.
- Do not modify Strategy runtime behavior.
- Do not accept predictive usefulness or profitability.

## Next Tasks
1. SWING operator review package.
2. SWING canonical dataset freeze.
3. SWING registry approval.
4. POSITION_SWING canonical dataset candidate.
