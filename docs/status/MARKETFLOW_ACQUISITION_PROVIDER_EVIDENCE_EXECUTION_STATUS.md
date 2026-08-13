# MarketFlow Acquisition Provider Evidence Execution Status

## Title
- Acquisition Provider Evidence Execution v1.

## Acquisition Provider Evidence Execution
- Artifact kind: `ACQUISITION_PROVIDER_EVIDENCE_EXECUTED`
- Execution status: `ACQUISITION_PROVIDER_EVIDENCE_EXECUTED_READ_ONLY`
- Execution digest: `decc59a4a0ae91229ed527f9fcafd54e9d5af468d057d5200a67d2167939b02b`
- Evidence scope: `READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY`

## Source Acquisition Provider Evidence Request Approval
- Approval digest: `a83acdf0c64fa8d430274350c59b547a23e7a58fb897cc33982ab0444ec0993c`

## Source Corporate-Action Authority Approval
- Approval digest: `93524b9bdc4641de4c6eb1cc8343b848ceff316241c92edab57a2062b8640644`

## Target Universe
- `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`

## Acquisition Profile
- Date range: `2022-01-01` through `2025-12-31`.
- Timeframe/session: `1d` / `RTH_FULL_SESSION_1D`.
- Fields: sanitized OHLCV and provider-supported aggregate metadata.

## Provider Request Summary
- Selected provider/endpoint: `Massive.com` / `/v2/aggs/ticker/{stocksTicker}/range/1/day/{from}/{to}`.
- Selected endpoint mode: `CURRENT_STOCKS_V2_AGGS_RANGE_DAILY`.
- Provider requests/successes/failures: `12 / 12 / 0`.
- Generated output root/count: `.marketflow/acquisition_provider_evidence/expanded_universe_v1` / `7`.

## Per-Ticker Acquisition Evidence Summary
- `MSFT`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `cff4740fec2382ec568ac62e519e7df516628168fb313e4ab6a597de0c394972`.
- `NVDA`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `3fee1949a0aa455c8dba0aaf02fc37b2697f974a0a5cc2b78d5335cb7bc71a4a`.
- `AMZN`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `c001ff63099ca1f1ecd98154683f7953ae5ba2c92142a8f9664f879afd571b2d`.
- `GOOGL`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `c4925fa26252e243e979bcde6cddfd4e1f8c460aecfeaea375fe06598e74a9ef`.
- `META`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `913`, digest `cdf41378853aff0beeee97d7e79ebcf530ebce28a9a8a4442789c4427977ed2b`.
- `TSLA`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `4d35ac42ea8e7984030ca99562124046630d5c58a5bef7f909d2c1f8328d9772`.
- `JPM`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `b585ef8647579a0aec161157bd738ee8f2a42d44438867f9c8a7761f5d8ea0b8`.
- `XOM`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `1d2ad61e34e1d9e2dc6b9b52d311ed885b87232d6bb9264b9416c916ec5d8664`.
- `JNJ`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `ac66dd558627b1ea34855be7e75387b5a8260b335d299841dddd8f2aac5873ca`.
- `WMT`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `96760c22f7ce10ca4deb7e530e16b3eaaef4727ec9f6db48bde89ca1824ba127`.
- `CAT`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `414e7ead524f90ee56daa74cb2195dde19ea3ac061dae92758c5b409392ebf2b`.
- `LMT`: `ACQUISITION_EVIDENCE_COLLECTED_READ_ONLY`, bars `1003`, digest `55c118bf8f8c757c8de0e5be3afec7d1da67742b05094711bde699a144f277d6`.

## Output Digest Manifest
- `acquisition_provider_evidence_run_manifest.json`: `ad2de2a4493e7d0c7bd5d3bd62dce20b7a09b3c4dad1ab56008b468fddbfed07`.
- `acquisition_provider_request_receipts_sanitized.json`: `812677a5d378a5255c7e674ed416499e457bb69320dde8ab780ca07fdd547a66`.
- `acquisition_evidence_results_sanitized.json`: `51d970eedb72019c5d3fcffe1ccf10475a3480c9c9deb28b9a3d1e67442373fd`.
- `acquisition_data_quality_summary.json`: `147bbfbb96318a39b4c6b4ae4a865e593d4fa64369b7ac31ad8749af3af261c1`.
- `acquisition_failure_reason_inventory.json`: `98bbe551bc4bd1a1a7b6c9080f4967ab354652b8fe5c2f0d94a5152d2646978a`.
- `acquisition_digest_manifest.json`: `abbf00067830b06976c7f4bdf9396b6fe83f0edba306b7dc517994cae41270ed`.
- `operator_review_summary.json`: `c513a1ffb48ef8f124e4b466733f8fe2603d66887850b5f04cab9794f977e69b`.

## Data Quality Summary
- Historical-bar evidence/no-bars/not-evaluated: `12 / 0 / 12`.
- Failures/warnings: `0 / 12`.
- Calendar, session, and split/dividend adjustment semantics unsupported by this endpoint remain `NOT_EVALUATED_BY_SELECTED_ENDPOINT`.

## API Key and Raw Payload Boundary
- API keys were neither printed nor stored; raw provider payloads were not committed.

## Acquisition Authority Boundary
- Evidence execution does not authorize new-ticker acquisition or acquisition generation/execution.

## Dataset Boundary
- Dataset generation remains unauthorized.

## Canonical Dataset Boundary
- No canonical dataset candidate, authorization, or freeze was created.

## Registry Boundary
- Registry approval remains false.

## Predictive/Profitability Boundary
- Predictive usefulness and profitability remain not accepted; no experiment or scoring rerun occurred.

## Runtime Boundary
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.

## Checklist Summary
- Executed-artifact checks: `32 / 32 passing`.

## Guardrails
- Research-only, non-actionable evidence; no acquisition generation, dataset, canonical dataset, registry, predictive, profitability, runtime, or trading authority.
- Follow-on `ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_V1` is implemented as `ACQUISITION_EVIDENCE_RESULTS_REVIEW_PACKAGE_READY`, digest `57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415`.
- This execution artifact remains the source evidence. The review does not authorize acquisition generation; dataset generation remains unauthorized, and no canonical dataset or registry approval was created.
