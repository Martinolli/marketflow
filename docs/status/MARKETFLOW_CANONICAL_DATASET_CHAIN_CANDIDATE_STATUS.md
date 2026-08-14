# MarketFlow Canonical Dataset Chain Candidate Status

## Branch And Commit
- Branch: `feature/canonical-dataset-chain-candidate-v1`.
- Base commit: `ac27f0e3618241cd7c0cd81fd27b44336a2d7ed5`.
- Implementation commit: the commit containing this document.

## Candidate Artifact And Status
- Artifact/status: `CANONICAL_DATASET_CHAIN_CANDIDATE` / `CANONICAL_DATASET_CHAIN_READY_FOR_OPERATOR_REVIEW`.
- Schema version: `canonical_dataset_chain_candidate_v1`.
- Candidate digest: `d57a39e246b8e31ca96bec4bdf027ed49ee9afc6ba07c9ac7c0e7c7eb3581053`.
- The candidate is offline, research-only, and requires a separate operator review.

## Bound Source Evidence
- Acquisition generation freeze digest: `534d72f842a44162bf07d32bbd6c2defb4e0064deb148fb92e785a5514319bd5`.
- Acquisition generation approval digest: `9ce3949432707a33ca652ec267a4228540f9575ad1003661e774ea199fb88869`.
- Acquisition evidence results review digest: `57c0a06ec8395b8e4edab313eb61dbcacdb950fb858491becec8526dba42f415`.
- Acquisition provider execution/request approval digests: `decc59a4a0ae91229ed527f9fcafd54e9d5af468d057d5200a67d2167939b02b` / `a83acdf0c64fa8d430274350c59b547a23e7a58fb897cc33982ab0444ec0993c`.
- Corporate-action authority approval digest: `93524b9bdc4641de4c6eb1cc8343b848ceff316241c92edab57a2062b8640644`.
- Identity authority freeze digest: `55e33f7a0e7db13d289c76c53bead4edd319143d26d3082fbc7b24b61d60eb30`.

## Objective And Scope
- Objective: `PLAN_CANONICAL_DATASET_CHAIN_FOR_ACQUISITION_GENERATION_FROZEN_EXPANDED_UNIVERSE`.
- Scope: `CHAIN_CANDIDATE_ONLY_NOT_DATASET_AUTHORIZATION`.
- Mode/authority: `PLANNED_NOT_GENERATED` / `NOT_AUTHORIZED`.
- Candidate creation does not create a canonical dataset candidate or authorize dataset generation.

## Target Universe And Per-Ticker Summary
- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Every row is `PLANNED_READY_FOR_OPERATOR_REVIEW`; identity/split/dividend are frozen and corporate-action authority is approved.
- `MSFT`: `1003` bars; candidate digest `9293da6e6a9fbdf093277fad779c38e2a9d5bde64574ca4b82c25322a0db4eef`.
- `NVDA`: `1003` bars; candidate digest `4290dad27ac5faeb1515ad65bfcca27c0a0d6e5f1bb8069357dfd793a2441382`.
- `AMZN`: `1003` bars; candidate digest `8a620f5d3b008d4e5be1a6131249582e72d8d03728a7c18d855754734141b348`.
- `GOOGL`: `1003` bars; candidate digest `38a8700fcafa579bb04b76dd3ca9ea9f0a10d4187fe6eeb5d45d265b2cd54382`.
- `META`: `913` bars; reduced-count flag `True`; candidate digest `5ad70c22358eff79ad106b54fda519822b366f49e9bce0c265db31d67b993c24`.
- `TSLA`: `1003` bars; candidate digest `511ebc44b0fc1a39c950f2a9540e3096f037c47dbd147dfaed1978146558269f`.
- `JPM`: `1003` bars; candidate digest `5aad30d206ac3428c93bbd4973d0ff0d11817921850e57b58e68773fd4270038`.
- `XOM`: `1003` bars; candidate digest `3cda02bb87a75777e250bc2206aa5c6beaf0144228ba41b6b0841aeae4bfdc50`.
- `JNJ`: `1003` bars; candidate digest `2275bc1ad9f74681989e679a66a23ca3c7f2338e1a88400a7fede7c40cb13757`.
- `WMT`: `1003` bars; candidate digest `d2fcf5f2d07dc0596af96e32c3ab63e9e9c739b94dc70c3781a77d9e196b3907`.
- `CAT`: `1003` bars; candidate digest `dc3a7777a50c9b9462cdc386a8eb9d674588508bd6d112d8c8870f6dd50b041d`.
- `LMT`: `1003` bars; candidate digest `5042a66d52a5aaef75052779ffba476910e736b7e3ed22e49343e9783b6d03c2`.

## Source Profile And META Preservation
- Date range/timeframe/profile: `2022-01-01` through `2025-12-31` / `1d` / `RTH_FULL_SESSION_1D`.
- Source evidence remains `READ_ONLY_HISTORICAL_MARKET_DATA_ACQUISITION_REQUESTS_ONLY` for 12 tickers and seven sanitized acquisition outputs.
- META remains exactly `913` bars while every other ticker remains `1003`; no repair, inference, smoothing, normalization, backfill, or fabrication occurs.

## Planning Dimensions
- The 22 dimensions bind acquisition freeze, corporate-action, identity, split/dividend authority, ticker order, daily OHLCV schema, timezone/calendar/session policy, price adjustments, META preservation, missing-bar policy, quality validation, deterministic sorting, canonical metadata/digests, and sanitized/raw-output policy.

## Future Chain And Gates
1. Candidate operator review package.
2. Canonical dataset approval, if required.
3. Canonical dataset generation execution.
4. Results review package.
5. Canonical dataset freeze.
6. Research registry candidate, review, and approval.
7. Additional predictive evidence and runtime migration only if separately authorized.

- Every future step remains a separate gate; none is authorized by this candidate.

## Risk Controls And Planned Outputs
- Controls prohibit unapproved dataset generation, premature freeze/registry approval, raw payload or API-key handling, missing-bar fabrication, unreviewed calendar/adjustment changes, runtime source switching, automatic stitching, trading, and predictive/profitability acceptance.
- Ten output templates are declared only as `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Authority Boundaries
- Dataset generation authorized/performed: `False / False`.
- Canonical dataset authorized/candidate created/generation executed/frozen: `False / False / False / False`.
- Registry approval created: `False`.
- Additional predictive evidence execution authorized/performed: `False / False`.
- Predictive usefulness/profitability: `not accepted / not accepted`.
- Runtime migration approved/active: `False / False`.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.

## Offline Boundaries And Checklist
- Provider requests/live transport/market-data acquisition: `False / False / False`.
- No dataset, canonical dataset, registry approval, predictive artifact, or runtime artifact was created.
- Total/passed/failed/blockers: `51 / 51 / 0 / 0`.
- The follow-on Canonical Dataset Chain Candidate Operator Review Package v1 is implemented; this candidate remains its bound source evidence.
- Review-package creation does not authorize dataset generation and creates no canonical dataset or registry approval.
- The next task requires a separate policy decision between an approval ceremony and separately authorized generation execution.
