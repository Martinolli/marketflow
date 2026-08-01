# MarketFlow Fixed-Date Acquisition Contract Status

## Decision

Contract tooling status: PASS.

Acquisition status: BLOCKED.

The fixed-date acquisition contract tooling is ready for final offline
acceptance, but acquisition remains disabled. Fixed dates are not approved. 4h
bar semantics are not approved. Session policy is not approved. Adjustment and
corporate-action provenance are not approved. Pagination and completeness
acceptance is not approved.

No data was downloaded. Research protocol remains blocked. Predictive
usefulness and profitability remain unaccepted.

## Starting State

- Branch: `feature/swing-fixed-date-acquisition-contract`.
- Base commit: `bf1187c27792a5903966bf3066f216ca923707cf`.
- Initial working tree: clean.
- Python: `3.12.10`.
- Initial `pip check`: passed, `No broken requirements found.`

## Files Added

- `docs/plans/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_PLAN.md`
- `docs/status/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_STATUS.md`
- `docs/architecture/MARKETFLOW_HISTORICAL_DATA_ACQUISITION_CONTRACT.md`
- `docs/research/MARKETFLOW_BAR_AND_SESSION_POLICY.md`
- `config/fixed_date_acquisition_contract.example.toml`
- `marketflow/research/fixed_date_acquisition_contract.py`
- `tests/test_fixed_date_acquisition_contract.py`

## Current Acquisition-Path Inventory

Production and operator-facing acquisition paths identified without invoking
them:

- `marketflow/marketflow_data_parameters.py`: legacy default timeframe list:
  `1mo/5y`, `1w/2y`, `1d/365d`, `4h/100d`, `2h/60d`, `1h/150d`,
  `30m/20d`, `15m/20d`, `5m/20d`, `1m/20d`.
- `MarketFlowDataParameters.get_primary_timeframe()`: historically selects
  the first configured timeframe from the legacy list, therefore `1mo` by
  default.
- `marketflow/marketflow_data_provider.py`: `PolygonIOProvider` imports
  `polygon.RESTClient`, reads Polygon credentials through config, converts
  intervals to provider multipliers/timespans, derives missing `end_date` from
  `datetime.now()`, derives missing `start_date` from relative `period`, and
  calls `get_aggs(..., limit=50000)`.
- `MultiTimeframeProvider`: loops over timeframe dictionaries and passes
  `interval`, `period`, optional `start_date`, and optional `end_date` into the
  provider.
- `marketflow/marketflow_facade.py`: default analysis uses
  `parameters.get_timeframes()` and then fetches all requested timeframes.
- `marketflow/__main__.py`, `scripts/marketflow_analysis.py`, and
  `scripts/marketflow_batch_report.py`: analysis/report CLIs expose custom
  timeframe lists and create report directories using current date/time.
- `marketflow/marketflow_polygon_tools.py`: `PolygonLLMTools` imports
  `RESTClient`, reads Polygon credentials through config, and exposes direct
  `list_aggs`, daily open/close, previous close, trades, quotes, indicators,
  and dividends calls. Its module example derives a 30-day moving window from
  `datetime.now()`.
- `scripts/marketflow_macp.py`: builds a direct Polygon aggregate URL with
  `adjusted=true`, `sort=asc`, `limit=5000`, and API key in the URL, then
  calls `requests.get`.
- `scripts/marketflow_fair_price_calculation.py`: imports `RESTClient`, reads
  Polygon credentials, and calls financials.
- `trading_dashboard/base_client.py` and `trading_dashboard/stocks.py`: copied
  Polygon-style clients contain direct `requests`/`httpx` access to the
  provider API host, custom aggregate endpoint path construction,
  `adjusted` defaults, `sort` handling, `limit` handling, chunk helpers,
  `next_url` pagination helpers, and full-range aggregate helpers.
  `trading_dashboard/stocks.py` also reads the Polygon API key and constructs
  a `RESTClient` at import time, so future inventory work must avoid importing
  it without an explicit credential/network boundary.
- Manual real-data checks under `scripts/manual_checks/` instantiate
  `PolygonIOProvider` and remain outside default pytest collection.
- `marketflow/marketflow_llm_interface.py` contains a yfinance example via
  `yf.download`, separate from the accepted fixed-date contract.

No production acquisition path was run.

## Moving-Window Finding

Legacy acquisition is mutable:

- default periods include `5y`, `2y`, `365d`, `100d`, `60d`, `150d`, and
  `20d`;
- missing `end_date` becomes `datetime.now()`;
- missing `start_date` is calculated by subtracting the relative period;
- analysis/report output paths use current date/time.

These mutable windows are not acceptable for future research acquisition.

## Provider Contract

Provider business identity:

```text
MASSIVE.COM
```

Former brand and adapter/package identity retained where accurate:

```text
POLYGON.IO
polygon-api-client==1.14.6
```

Source-defined provider identity:

```text
MASSIVE_POLYGON_STOCKS_CUSTOM_BARS
```

Provider entitlement:

- subscription: `STOCKS_STARTER`;
- evidence: `OPERATOR_ATTESTED`;
- historical entitlement: `FIVE_YEARS`;
- data recency: `FIFTEEN_MINUTE_DELAYED`;
- aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`;
- entitlement status: `OPERATOR_ATTESTED_CONFIRMED`.

No API key, provider account, billing information, provider portal, or
credential value was inspected.

## Fixed-Date Contract

The contract requires explicit ISO `start_date` and `end_date`, start strictly
before end, no relative values, no current-date default, and deterministic
serialization.

The example keeps:

```text
start_date = HUMAN_APPROVAL_REQUIRED
end_date = HUMAN_APPROVAL_REQUIRED
```

## Profile Acquisition Contracts

`SWING`:

- canonical timeframe: `4h`;
- minimum valid OHLCV rows: `390`;
- multiplier: `4`;
- timespan: `hour`;
- acquisition date range: `NOT_SET`;
- bar construction: `BAR_CONSTRUCTION_NOT_CONFIRMED`;
- session policy: `SESSION_POLICY_NOT_CONFIRMED`;
- status: blocked.

`POSITION_SWING`:

- canonical timeframe: `1d`;
- minimum valid OHLCV rows: `560`;
- multiplier: `1`;
- timespan: `day`;
- acquisition date range: `NOT_SET`;
- bar construction: `PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW`;
- session policy: `SESSION_POLICY_NOT_CONFIRMED`;
- status: blocked.

## Bar-Construction Finding

Current code can request provider-native `4h` as `multiplier=4`,
`timespan=hour`. The current repository does not prove whether existing 4h
files were provider-native, locally aggregated from 1h, locally aggregated from
minutes, or produced by another path. Provenance remains unknown.

No 4h construction mode is approved.

## Daily-Bar Finding

Current code can request daily aggregates as `multiplier=1`, `timespan=day`.
Daily session semantics are not approved merely because `1d` exists. Daily
bars remain `PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW`.

## Session-Policy Finding

Session policy remains unresolved:

```text
SESSION_POLICY_NOT_CONFIRMED
```

No regular-hours, extended-hours, or provider-default session behavior is
approved. No session inference was made from timestamps alone.

## Timezone And DST Finding

The proposed contract records source aggregation timezone
`AMERICA_NEW_YORK`, canonical storage timezone `UTC`, preservation of provider
epoch timestamps, and conversion to UTC before source-local diagnostics. Naive
canonical timestamps are prohibited.

## Adjustment Finding

Proposed adjustment state:

- `split_adjusted_requested = true`;
- `provider_adjusted_response = MUST_MATCH_REQUEST`;
- `dividend_adjusted = false`;
- `corporate_action_metadata_status = NOT_CONFIRMED`;
- `adjustment_provenance_status = CONTRACT_PROPOSED`;
- `adjustment_policy_status = NOT_APPROVED`.

An adjusted-response mismatch invalidates acquisition.

## Pagination And Completeness Finding

The contract requires explicit base-aggregate limits, iterator exhaustion,
duplicate-boundary rejection, range coverage validation, no silent truncation,
and no partial result acceptance. Provider pagination is not implemented or
run.

Fake pagination statuses are:

- `REQUEST_COMPLETE`;
- `REQUEST_TRUNCATED`;
- `PAGINATION_INCOMPLETE`;
- `PAGE_DUPLICATE`;
- `RANGE_COVERAGE_INCOMPLETE`;
- `PROVIDER_RESPONSE_INVALID`.

## Response Validation Finding

Synthetic response validation rejects:

- wrong status;
- wrong ticker;
- adjusted-flag mismatch;
- unknown shape;
- timezone-naive timestamps;
- out-of-order timestamps;
- duplicate timestamps;
- NaN or Infinity;
- `high < low`;
- invalid volume;
- partial final bars.

## Raw And Normalized Artifact Proposal

Future artifacts:

```text
RAW_PROVIDER_RESPONSE
NORMALIZED_OHLCV_DATASET
```

The proposed parent chain is:

```text
ACQUISITION_REQUEST_CONTRACT
  -> RAW_PROVIDER_RESPONSE
  -> NORMALIZED_OHLCV_DATASET
  -> ANNOTATED_DATASET
```

No artifact is written in this task.

## Provenance Contract

Future canonical dataset provenance must record provider identity, endpoint
family, request digest, exact ticker, fixed start/end dates, multiplier,
timespan, session policy, source timezone, canonical timezone, adjusted request
and response, safe request ID where available, retrieval timestamp, code
commit, client package/version, pagination completeness, raw digest,
normalized digest, row count, timestamp range, corporate-action provenance
status, and later annotation code version.

No API key, username, account data, local absolute path, or provider portal
information is allowed.

## Contract Digest And Receipt

Dry CLI digest:

```text
29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
```

Receipt status:

```text
ACQUISITION_CONTRACT_PROPOSED_WITH_BLOCKERS
```

Acquisition enabled:

```text
false
```

Remaining blockers:

- `FIXED_DATES_NOT_APPROVED`;
- `BAR_CONSTRUCTION_NOT_APPROVED`;
- `SESSION_POLICY_NOT_APPROVED`;
- `ADJUSTMENT_POLICY_NOT_APPROVED`;
- `PAGINATION_POLICY_NOT_APPROVED`.

## Tests

Focused acquisition-contract suite:

```text
34 passed
```

Related fixed-date, fixed-profile, remediation, and source-assurance suite:

```text
117 passed
```

Full collection:

```text
652 tests collected
```

Full default suite:

```text
652 passed
```

Test count explanation: the accepted data-readiness remediation baseline
collected `618` tests. This task adds `34` deterministic fixed-date
acquisition-contract tests, including four acceptance-review regressions for
request pagination status, timezone/DST policy strictness, adjustment
provenance status, and empty response rejection.

Warnings: none reported by the final full suite.

## Reviewer Findings

Reviewer A:

- Finding: provider entitlement was originally represented as unconfirmed, but
  the operator later attested Massive.com `STOCKS_STARTER` entitlement. Fixed
  by updating the contract, example, receipt, and docs while keeping
  acquisition disabled.
- Finding: the loader's safety filter initially treated `profiles` and
  explicit negative safety declarations as prohibited path/credential fields.
  Fixed by narrowing field-name rejection while preserving API-key, URL, and
  path rejection.
- High finding: bar-construction approval was not uniformly blocked across all
  represented modes. Fixed by requiring `bar_construction_status =
  NOT_APPROVED` for every profile.
- High finding: fixed-date approval state could contradict the remaining date
  blocker. Fixed by requiring source-controlled proposed contracts to keep both
  date values and statuses at `HUMAN_APPROVAL_REQUIRED` while
  `FIXED_DATES_NOT_APPROVED` remains.
- High finding: adjusted-response validation coerced string values through
  `bool(...)`. Fixed by requiring a real boolean adjusted field.
- High finding: response range-boundary validation was not represented for
  approved fixed dates. In this proposed contract, approved dates are rejected
  while the date blocker remains; no executable fixed-date response can pass
  until a later approved contract revision supplies real dates.
- Medium finding: `timestamp_utc` accepted non-UTC offsets. Fixed by requiring
  the timestamp value itself to be UTC.
- Medium finding: fake pagination compared timestamp strings
  lexicographically. Fixed by parsing UTC instants.
- Medium finding: provider inventory missed the `trading_dashboard/stocks.py`
  import-time credential read/client construction. Fixed in the inventory
  section above.
- Finding: 4h provenance remains unknown; no provider-native 4h approval can
  be inferred. No critical or high reviewer finding remains unresolved.
- Final-review high finding: request-level pagination status could contradict
  the remaining pagination blocker. Fixed by requiring
  `pagination_policy_status = NOT_APPROVED`.
- Final-review high finding: timezone/DST policy fields were under-enforced.
  Fixed by requiring source timezone, provider epoch preservation, diagnostic
  source-local metadata, epoch-to-UTC-first DST policy, UTC canonical storage,
  no naive canonical timestamps, and `timezone_policy_status = NOT_APPROVED`.
- Final-review high finding: adjustment provenance could be overstated. Fixed
  by requiring `adjustment_provenance_status = CONTRACT_PROPOSED`.
- Final-review medium finding: empty synthetic provider results could return
  `REQUEST_COMPLETE`. Fixed by rejecting empty result lists.
- Final-review medium finding: provider-request session policy could diverge
  from unresolved profile session blockers. Fixed by requiring
  `requested_session_policy = SESSION_POLICY_NOT_CONFIRMED`.

Reviewer B:

- Finding: canonical digest and receipt correctly reflect the entitlement
  addendum. Evidence uses digest
  `29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e`.
- Finding: source-controlled example contains no actual ticker/date/key/path
  and no executable status. No blocker remains unaddressed in tooling.
- High finding: bar-construction approval was not uniformly blocked. Fixed as
  described under Reviewer A.
- High finding: fixed-date status strings were not strict enough. Fixed by
  rejecting any non-`HUMAN_APPROVAL_REQUIRED` proposed date status in this
  contract revision.
- Medium finding: provenance `client_package_version` was not sanitized. Fixed
  by rejecting credential-like, URL-like, and absolute-path-like values.
- Medium finding: the new focused test's prior-integrity coverage was narrow.
  Disposition: accepted with broader verification; the related suite includes
  Artifact Lineage v1, fixed-profile, data-remediation, and source-assurance
  tests, and the full suite passed.
- No critical or high reviewer finding remains unresolved.

## Blockers

Acquisition remains blocked by:

- exact fixed start date not approved;
- exact fixed end date not approved;
- 4h bar-construction policy not approved;
- session policy not approved;
- adjustment and corporate-action provenance not approved;
- pagination and completeness acceptance not approved.

## Remaining Limitations

- No provider source code or account portal was inspected.
- No provider call was made.
- No raw or normalized artifact was written.
- Existing historical 4h and daily dataset provenance remains unresolved.
- The contract does not implement local aggregation.
- The contract does not prove predictive usefulness or profitability.

## Final Evidence

Required checks used `env\Scripts\python.exe`.

```text
pip check: No broken requirements found.
focused acquisition-contract tests: 34 passed.
related fixed-date/fixed-profile/artifact-lineage/remediation/source-assurance suite: 117 passed.
pytest --collect-only -q: 652 tests collected.
pytest -q: 652 passed.
compileall -W error: passed.
git diff --check: passed.
```

Pre-test Git status:

```text
?? config/fixed_date_acquisition_contract.example.toml
?? docs/architecture/MARKETFLOW_HISTORICAL_DATA_ACQUISITION_CONTRACT.md
?? docs/plans/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_PLAN.md
?? docs/research/MARKETFLOW_BAR_AND_SESSION_POLICY.md
?? docs/status/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_STATUS.md
?? marketflow/research/fixed_date_acquisition_contract.py
?? tests/test_fixed_date_acquisition_contract.py
```

Post-test Git status matched the pre-test status exactly.

`.marketflow/reports` Git status was clean before and after final tests.

No provider call, network call, data download, annotation, Strategy candidate
generation, Monte Carlo, outcome evaluation, performance analysis, broker
integration, execution capability, dependency change, source-data mutation, or
historical-report rewrite was performed during implementation verification.
