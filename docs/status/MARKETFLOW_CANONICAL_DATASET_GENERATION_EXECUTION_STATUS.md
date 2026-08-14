# MarketFlow Canonical Dataset Generation Execution Status

## Branch And Commit

- Branch: `feature/canonical-dataset-generation-execution-v1`.
- Base commit: `c5a82ac38948a9ad9c2c46217fcfa4a2d2b87290`.
- Implementation commit: the commit containing this document.

## Canonical Dataset Generation Execution

- Artifact/status: `CANONICAL_DATASET_GENERATED` / `CANONICAL_DATASET_GENERATED_RESEARCH_ONLY`.
- Schema version: `canonical_dataset_generated_v1`.
- Generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Execution timestamp: `2026-08-14T16:00:00Z`.
- Dataset generation performed/canonical candidate created/generated: `True / True / True`.

## Source Canonical Dataset Generation Approval

- Approval digest: `0b287370e8eddad522765a2ee77c39765f6690b27468bcc2f5b28587330a63b2`.
- Canonical chain review/candidate digests: `5226b45cd8d4b45836258c8984627d6c55715fece308d7cebb3b37a09df96c4d` / `d57a39e246b8e31ca96bec4bdf027ed49ee9afc6ba07c9ac7c0e7c7eb3581053`.
- The approval remains source evidence; generation does not expand its scope.

## Source Acquisition Generation Freeze

- Freeze digest: `534d72f842a44162bf07d32bbd6c2defb4e0064deb148fb92e785a5514319bd5`.
- Acquisition approval/evidence-review/provider-execution digests: `9ce3949432707a33ca652ec267a4228540f9575ad1003661e774ea199fb88869` / `57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415` / `decc59a4a0ae91229ed527f9fcafd54e9d5af468d057d5200a67d2167939b02b`.
- All seven saved sanitized source-output SHA-256 values matched the committed execution/review status documents.

## Target Universe And Source Profile

- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Date range/timeframe/profile: `2022-01-01` through `2025-12-31` / `1d` / `RTH_FULL_SESSION_1D`.
- Source scope: `READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY`.

## Per-Ticker Canonical Record Summary

- `MSFT`: `1003`.
- `NVDA`: `1003`.
- `AMZN`: `1003`.
- `GOOGL`: `1003`.
- `META`: `913`.
- `TSLA`: `1003`.
- `JPM`: `1003`.
- `XOM`: `1003`.
- `JNJ`: `1003`.
- `WMT`: `1003`.
- `CAT`: `1003`.
- `LMT`: `1003`.
- Total canonical record count: `11946`.

## META Reduced Bar Count Preservation

- META remains exactly `913` records while each other ticker remains exactly `1003`.
- No bar was repaired, inferred, smoothed, normalized into existence, backfilled, or fabricated.

## Generated Outputs And Digest Manifest

- Ignored output root: `.marketflow/canonical_datasets/expanded_universe_v1/`.
- Generated output count: `9`.
- Run-manifest semantic generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Source-evidence manifest SHA-256: `43c56cdb5826515342e93259c82f9ba3bbadd6c867738ed5a1399eb7247e1ed8`.
- Schema-contract SHA-256: `ac4ba5f7c1b56e743d626363d1d45a3e71a0dcfd11f2e070fc02087b069b1435`.
- Records JSONL SHA-256: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Per-ticker summary SHA-256: `4a9dbc104a7f0dc434cb9ba6f8b0687677a507b7aaf76c5005280b0172ec86a4`.
- Data-quality report SHA-256: `3c384753577019b30929fc50dd4489fd9fa7b17fce652a2abdbd16620e020c2b`.
- Failure inventory SHA-256: `84eebb668914628c5a6bb2570310817619c4d817dae39a7c5b15e593a01ffeb8`.
- Operator-review summary SHA-256: `f2101b6b84477eb92ea2c058a789ea4de19969334729ed6c38d5225adea2f193`.
- The digest manifest lists all nine outputs. Its self-referential file digest is explicitly `SELF_REFERENTIAL_DIGEST_NOT_APPLICABLE`; its actual file SHA-256 is `002d57494d1afc00c09532c424ea8f60199208417e424783d0bf142ce82a376f`.

## Data Quality Summary

- Failures/warnings: `0 / 1`.
- The sole warning records the preserved META reduced-bar source limitation.
- Records use normalized decimal strings, approved ticker order, ascending UTC timestamps, and source/canonical record digests.

## Authority Boundaries

- Canonical dataset generated/frozen: `True / False`.
- Registry approval created: `False`.
- Additional predictive evidence execution authorized/performed: `False / False`.
- Predictive experiment rerun, feature regeneration, strategy scoring, and trade recommendations: all `False`.
- Predictive usefulness/profitability: `not accepted / not accepted`.
- Runtime migration approved/active: `False / False`.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.

## Offline Execution And Non-Goals

- Provider requests/live transport/market-data acquisition: `False / False / False`.
- No `.env` or API key was inspected; no API key was printed or stored.
- No raw provider payload was committed.
- No canonical dataset freeze, registry approval, predictive/profitability acceptance, experiment reexecution, strategy scoring, source switch, runtime activation, or trading action occurred.

## Next Task

- `Canonical Dataset Results Review Package v1` remains separate future work.
