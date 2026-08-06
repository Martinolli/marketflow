# MarketFlow Acquisition Live Provider Smoke 2025-01 Status

## Scope
- Artifact kind: `ACQUISITION_MONTHLY_LIVE_SMOKE_CANDIDATE`
- Candidate status: `ACQUISITION_MONTHLY_LIVE_SMOKE_READY_FOR_OPERATOR_REVIEW`
- Ticker: `AAPL`
- Month: `2025-01`
- Range: `2025-01-01` through `2025-01-31`
- Endpoint used: `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}`
- Endpoint path: `/v2/aggs/ticker/AAPL/range/15/minute/2025-01-01/2025-01-31`
- Request mode: `LIVE_PROVIDER_REQUEST`
- Provider response status: `OK`

## Reconciliation
- Raw row count: `1277`
- Normalized source row count: `1277`
- RTH row count: `520`
- Extended-hours row count: `757`
- Expected RTH row count: `520`
- RTH reconciliation status: `RTH_SOURCE_ROWS_RECONCILED`
- Full ordinary sessions: `20`
- Incomplete ordinary sessions: `0`
- SWING half-session 195m bars: `40`
- POSITION_SWING full-session 1d bars: `20`
- Accepted 2025-01 cross-check passed: `True`

## Digests
- Provider raw response digest: `10ae9608f6041068cd14756da03c79c7a12b73379a07dc8562a6254dde2a711e`
- Provider raw body sha256: `9b41676107311cbade4d22f0ea161e48d806ddfaec1d126c10eee7332f1b0b6d`
- Normalized rows digest: `d984ac14fe574278b766cb576506b4ce59abfb9ef317e8e3c2b01a471b85f199`
- Monthly reconciliation digest: `d546ea7ce7057934b7fc0ce727056aacc1a5bc5c6fbe2c2382dcdfb74cc64102`
- Acquisition smoke receipt digest: `567df33495a14e23f9bcfda905f5473cdbb76c070bcec10523a536887ea3d36c`
- Acquisition monthly smoke candidate digest: `2ba6bf4a28eeffda2b05254921db743eb2b8e58e11b0ed558ef2939a40db6cf3`

## Authority Bindings
- Identity frozen digest: `57a698979e827d7c95737c12ad3435563486e44559a7f1ddd49c94006d27d24e`
- Calendar frozen digest: `25258b528e45a7f36d1cf96a4a40a8f2c89243c69d034f480dd10c4464d847a6`
- Schedule digest: `b0194dfed46ee06bd0954cc76f9e76d144d84c5e6f1a836acf2f486c083aeef0`
- Split-event audit frozen digest: `9bf3ff52f599757add22e01889c9ee3e72b4ff31e831ae312b94483b37f05fae`
- Dividend-event audit frozen digest: `0ef4e69954d67a5df8a246f623b2904651d579e5ebbe620a9647e16b42b95141`
- Acquisition contract digest: `538f076a9d63e564a4279091c9a0b39c90091d781a1b867d12b79572cd4998e6`

## Dividend Implication
- In-range dividends found: `True`
- In-range dividend count: `16`
- Implication: `ACQUISITION_GENERATION_MUST_ACCOUNT_FOR_ADJUSTED_DATA_AND_DIVIDEND_POLICY`

## Authority Boundary
- acquisition_generation_freeze: `False`
- canonical_eligibility: `False`
- registry_eligibility: `False`
- strategy_runtime_migration: `False`
- automatic_stitching: `False`
- predictive_usefulness: `not accepted`
- profitability: `not accepted`

## Safety Confirmations
- API key stored: `False`
- Raw provider payload stored in this document: `False`
- Full generated bars stored in this document: `False`
- No acquisition-generation freeze was created.
- No canonical, registry, runtime, predictive, or profitability approval occurred.

## Next Task Recommendation
- Full 2022-2025 live acquisition generation candidate, after operator review of monthly smoke.
