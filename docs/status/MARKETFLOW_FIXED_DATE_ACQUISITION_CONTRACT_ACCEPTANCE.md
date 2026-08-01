# MarketFlow Fixed-Date Acquisition Contract Acceptance

## Decision

- Implementation decision: PASS.
- Acquisition decision: BLOCKED.
- UTC acceptance date: `2026-08-01T07:49:53Z`.
- Branch: `feature/swing-fixed-date-acquisition-contract`.
- Base commit: `bf1187c27792a5903966bf3066f216ca923707cf`.
- Baseline tag at base: `v0.1.0-alpha.12-data-readiness-remediation`.
- Commit intent: local commit only.
- Tag: not created.
- Push: not performed.

Contract tooling is accepted for local commit. Data acquisition remains
disabled and blocked.

## Scope And Exclusions

Accepted scope:

- immutable fixed-date acquisition-contract models;
- strict TOML loading and validation;
- provider/source metadata and operator-attested entitlement state;
- explicit blockers for fixed dates, 4h/daily bar construction, session,
  adjustment/corporate-action provenance, pagination, and completeness;
- deterministic serialization and digest;
- sanitized readiness receipt;
- synthetic pagination and response validators;
- raw/normalized artifact and provenance design;
- offline dry CLI;
- deterministic tests and documentation.

Excluded scope:

- no provider call, network call, data download, raw response capture,
  normalized dataset write, annotation, Strategy candidate generation, Monte
  Carlo, PnF outcome analysis, outcome evaluation, campaign aggregation,
  optimization, performance analysis, broker integration, execution capability,
  dependency change, source-data mutation, historical-report rewrite, tag,
  push, or remote change.

## Current Acquisition-Path Inventory

Source review, without invoking provider paths, found:

- `marketflow/marketflow_data_parameters.py` keeps legacy moving timeframe
  entries: `1mo/5y`, `1w/2y`, `1d/365d`, `4h/100d`, `2h/60d`, `1h/150d`,
  `30m/20d`, `15m/20d`, `5m/20d`, and `1m/20d`.
- `MarketFlowDataParameters.get_primary_timeframe()` still selects the first
  legacy configured timeframe when called by legacy flows.
- `marketflow/marketflow_data_provider.py` imports `polygon.RESTClient`, reads
  Polygon credentials through config, derives missing `end_date` from
  `datetime.now()`, derives missing `start_date` from the relative `period`,
  maps interval suffixes to provider multipliers/timespans, calls
  `get_aggs(..., limit=50000)`, converts provider millisecond epochs to UTC
  pandas timestamps, and returns only OHLCV dataframe/series values rather than
  retaining full provider metadata.
- `MultiTimeframeProvider` passes each configured `interval`, `period`, and
  optional date through to the data provider.
- `marketflow/marketflow_facade.py`, `marketflow/__main__.py`,
  `scripts/marketflow_analysis.py`, and `scripts/marketflow_batch_report.py`
  still rely on current-date or configured timeframe behavior in legacy
  analysis/report paths.
- `marketflow/marketflow_polygon_tools.py` imports `RESTClient`, reads
  credentials through config, and exposes `get_custom_bars(ticker,
  multiplier, timespan, from_date, to_date, adjusted="true", sort="asc",
  limit=120)` through `client.list_aggs`.
- `scripts/marketflow_macp.py` builds a direct aggregate URL with
  `adjusted=true`, `sort=asc`, `limit=5000`, and an API key in the URL.
- `trading_dashboard/base_client.py` and `trading_dashboard/stocks.py` contain
  copied Polygon-style direct `requests`/`httpx` clients, aggregate endpoint
  construction, sort/adjusted/limit handling, full-range helpers, next-url
  pagination helpers, and chunked aggregate helpers. `trading_dashboard/stocks.py`
  also reads a Polygon API key and constructs a `RESTClient` at import time.
- Manual real-data checks under `scripts/manual_checks/` instantiate
  `PolygonIOProvider` and remain outside the default offline suite.

No production acquisition path was run.

## Moving-Window Finding

Legacy acquisition remains mutable because default periods include `5y`, `2y`,
`365d`, `100d`, `60d`, `150d`, and `20d`; missing end dates derive from the
system date; missing start dates derive from relative periods; and report paths
use current date/time. The accepted contract rejects those semantics for future
research acquisition.

## Provider Identity And Entitlement

Provider business identity is represented as `MASSIVE.COM`.

Legacy provider brand and installed adapter/package naming are preserved as
`POLYGON.IO` and `polygon-api-client==1.14.6` where they describe installed
code.

Provider entitlement is:

- subscription: `STOCKS_STARTER`;
- evidence: `OPERATOR_ATTESTED`;
- historical access: `FIVE_YEARS`;
- recency: `FIFTEEN_MINUTE_DELAYED`;
- aggregate access: `INTRADAY_AND_DAILY_AVAILABLE`;
- entitlement status: `OPERATOR_ATTESTED_CONFIRMED`.

This is operator-attested, not API-verified. No API key, provider account,
billing information, provider portal, credential value, browser data, account
data, or trade data was inspected.

## Fixed-Date Contract

The source-controlled example has no actual ticker and no actual acquisition
dates:

```text
start_date = HUMAN_APPROVAL_REQUIRED
end_date = HUMAN_APPROVAL_REQUIRED
```

The contract rejects relative periods, current-date defaults, environment or
filesystem date inference, CLI date overrides, and automatic date inference
from row requirements. Executable fixed-date requests remain impossible in this
revision.

## Fixed Profile Contracts

`SWING` remains:

- timeframe: `4h`;
- minimum valid OHLCV rows: `390`;
- date range: `NOT_SET`;
- bar construction: `BAR_CONSTRUCTION_NOT_CONFIRMED`;
- bar construction status: `NOT_APPROVED`;
- session policy: `SESSION_POLICY_NOT_CONFIRMED`;
- session status: `NOT_APPROVED`;
- acquisition enabled: `false`.

`POSITION_SWING` remains:

- timeframe: `1d`;
- minimum valid OHLCV rows: `560`;
- date range: `NOT_SET`;
- bar construction: `PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW`;
- bar construction status: `NOT_APPROVED`;
- session policy: `SESSION_POLICY_NOT_CONFIRMED`;
- session status: `NOT_APPROVED`;
- acquisition enabled: `false`.

The 390/560 gates are not weakened. TOML, CLI, and environment inputs cannot
change the profile timeframes in this contract module.

## Bar And Session Findings

4h bars are not approved. The contract does not silently accept
`multiplier=4` and `timespan=hour` as the scientific meaning of `SWING/4h`.
Provider-native clock windows may not align with 09:30-16:00 regular trading
hours; source timezone, clock anchors, and extended-hours inclusion matter;
6.5 regular-session hours cannot be divided into equal four-hour bars; and
local aggregation requires separate approval for base timeframe, session,
anchors, short bars, early closes, DST, and missing bars.

Daily bars remain provisionally represented as
`PROVIDER_NATIVE_1D_PENDING_SESSION_REVIEW`; this is not full approval.
Session inclusion, source timezone, split adjustment, dividend-adjustment
limitation, missing-bar behavior, response metadata, and fixed dates remain
unresolved.

Session policy is part of the semantic digest and remains unapproved. No
provider default, missing field, `None`, empty string, timeframe, or provider
name can silently approve session behavior.

## Timezone And DST

Provider/source aggregation timezone is represented as `AMERICA_NEW_YORK`, and
canonical normalized storage timezone is `UTC`. Naive canonical timestamps are
prohibited. Provider epoch values must be converted to UTC first; source-local
time may be derived only as diagnostics. DST ambiguity or nonexistence cannot
be silently accepted by canonical normalized timestamps, and local-machine
timezone is not part of serialization.

## Adjustment And Corporate Actions

Proposed state:

```text
split_adjusted_requested = true
provider_adjusted_response = MUST_MATCH_REQUEST
dividend_adjusted = false
corporate_action_metadata_status = NOT_CONFIRMED
adjustment_provenance_status = CONTRACT_PROPOSED
adjustment_policy_status = NOT_APPROVED
```

`adjusted=true` is explicit. Provider adjusted responses must be real booleans
and must match the request. Strings and integers do not coerce into booleans.
No dividend-adjusted claim is made, and no corporate-action processing or
price-behavior inference was implemented.

## Request, Pagination, And Completeness

Any future request contract requires exact provider identity, ticker,
multiplier, timespan, fixed start, fixed end, adjusted flag, ascending sort,
explicit limit, session/bar policy, and completeness policy. It prohibits
arbitrary URLs, caller-provided endpoints, current-time defaults, relative
periods, extra query parameters, provider fallback, and executable requests
while blockers remain.

Pagination and completeness remain unapproved and blocking. Synthetic
validators reject duplicate pages, repeated boundary rows, truncated responses,
missing final coverage, incomplete exhaustion, malformed timestamp values, and
range-coverage failures. Market-calendar completeness and actual provider page
iteration are not implemented in this task.

## Full/Partial Bar And Response Validation

The proposed policy permits completed historical bars only. Partial final bars
are rejected; no current incomplete bar, zero-volume synthetic bar, OHLC
forward fill, future fill, or invented no-trade bar is approved.

Synthetic response validation rejects wrong ticker, wrong adjusted flag,
out-of-order rows, duplicate timestamps, timezone-naive or non-UTC timestamps,
malformed response shape, NaN/Infinity, `high < low`, negative volume, partial
final bars, incomplete pagination, and incomplete requested-range coverage
where an approved fixed date range exists. No failed response can become a
normalized dataset through this contract module.

## Raw/Normalized Lineage And Provenance

The design distinguishes:

```text
ACQUISITION_REQUEST_CONTRACT
  -> RAW_PROVIDER_RESPONSE
  -> NORMALIZED_OHLCV_DATASET
  -> ANNOTATED_DATASET
```

No artifact is written in this task. Raw exact bytes and normalized
deterministic bytes have separate digests. Parent relationships retain the
request-contract digest. Raw is never silently replaced by normalized, and
normalized is never silently replaced by annotated. Existing Artifact Lineage
v1 stage/type semantics are not rewritten.

Future provenance includes provider identity, endpoint family/version, request
digest, ticker, fixed dates, multiplier/timespan, bar construction, session,
source timezone, canonical timezone, adjusted request/response, retrieval UTC
timestamp, code commit, sanitized client package/version, pagination
completeness, raw digest, normalized digest, row count, timestamp bounds, and
corporate-action provenance status. It excludes API keys, provider usernames,
billing data, local absolute paths, account/trade data, and performance data.

## Serialization, Digest, And CLI

Canonical serialization uses UTF-8 JSON bytes, recursive dataclass conversion,
sorted keys, stable separators, fixed enum strings, `allow_nan=false`, and a
SHA-256 digest. It excludes credentials, local paths, current timestamps, and
the digest itself. Receipt generation does not alter the digest.

Final accepted contract digest:

```text
29444bf0345eb33de192e252cddea1c978da2263a3d6a42ff553762dd380b89e
```

Dry CLI:

```powershell
env\Scripts\python.exe -m marketflow.research.fixed_date_acquisition_contract
```

The CLI validates only the safe source-controlled example, prints a sanitized
blocked receipt, accepts no ticker/date/API-key flags, imports no provider
client, reads no credential or environment value, opens no socket, writes no
dataset or report, and does not freeze or enable acquisition. Exit zero means
the contract structure is valid with blockers, not acquisition authorization.

## Loader And Example

The strict loader rejects unknown fields, missing required fields, unknown enum
values, relative periods, execution-enabled status, credential-like fields,
arbitrary URL fields, local path fields, weakened 390/560 row gates,
profile/timeframe inconsistency, approved 4h/session/date states in the
proposed blocked contract, adjusted-response mismatch, and implicit dates.

The source-controlled example contains no actual ticker, actual date, actual
URL, local path, API key, or executable acquisition state. The dry CLI accepts
no explicit external contract path; the source-controlled example is its only
dry input.

## Warning Behavior

No broad warning suppression was introduced. The only warning filters found are
test-local pre-existing third-party filters for `polygon` and `websockets` in
`tests/test_data_provider.py`. The final full suite emitted no warning summary;
that absence is consistent with the relevant provider modules not being
imported by the exercised tests, and no project-owned warning was hidden.

## Verification Evidence

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
?? docs/status/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_ACCEPTANCE.md
?? docs/status/MARKETFLOW_FIXED_DATE_ACQUISITION_CONTRACT_STATUS.md
?? marketflow/research/fixed_date_acquisition_contract.py
?? tests/test_fixed_date_acquisition_contract.py
```

Pre-test `.marketflow/reports` metadata:

```text
count=971
digest=c89f3a7f6d81e3863234758f2a0a815c8ff2ef80eaa7cd3ac491a4dd6b4ebaa5
```

Pre-test `data` metadata:

```text
count=1
digest=5288dfa1a9912f89ed0c7de105d199eee324e1bed43a0ae374d43e5a043a676f
```

Post-test Git status matched the pre-test status exactly. `.marketflow/reports`
and `data` Git status were clean before and after final tests.

Post-test `.marketflow/reports` metadata:

```text
count=971
digest=c89f3a7f6d81e3863234758f2a0a815c8ff2ef80eaa7cd3ac491a4dd6b4ebaa5
```

Post-test `data` metadata:

```text
count=1
digest=5288dfa1a9912f89ed0c7de105d199eee324e1bed43a0ae374d43e5a043a676f
```

Test count explanation: the accepted data-readiness remediation baseline
collected `618` tests. This task adds `34` deterministic fixed-date
acquisition-contract tests, including four acceptance-review regressions for
request pagination status, timezone/DST policy strictness, adjustment
provenance status, and empty response rejection.

## Reviewer Findings And Dispositions

Reviewer A and Reviewer B performed bounded read-only reviews. Prior high
findings from implementation review were fixed before acceptance: uniform
bar-construction blocking, fixed-date blocker consistency, strict adjusted
boolean validation, UTC timestamp enforcement, pagination timestamp parsing,
client package-version sanitization, and import-time dashboard credential
inventory documentation.

Final-review findings fixed before commit:

- High: request-level pagination status could contradict the remaining
  pagination blocker. Fixed by requiring `pagination_policy_status =
  NOT_APPROVED`.
- High: timezone/DST policy fields were under-enforced. Fixed by requiring
  source timezone, provider epoch preservation, diagnostic source-local
  metadata, epoch-to-UTC-first DST conversion, UTC canonical storage, no naive
  canonical timestamps, and `timezone_policy_status = NOT_APPROVED`.
- High: adjustment provenance could be overstated. Fixed by requiring
  `adjustment_provenance_status = CONTRACT_PROPOSED`.
- Medium: extra blocker values could be echoed by the dry receipt. Fixed by
  requiring the blocker list to be exact.
- Medium: empty synthetic provider result lists could return
  `REQUEST_COMPLETE`. Fixed by rejecting empty results.
- Medium: provider-request session policy could diverge from unresolved profile
  session blockers. Fixed by requiring `requested_session_policy =
  SESSION_POLICY_NOT_CONFIRMED`.
- Medium: provenance metadata hard-coded ticker status. Fixed so the helper
  records the request contract ticker, which is still
  `HUMAN_APPROVAL_REQUIRED` in the safe example.

No critical or high reviewer finding remains unresolved.

## Previous Integrity Non-Regression

Previous accepted boundaries remain preserved:

- baseline packaging and no-network controls;
- source identity fail-closed behavior;
- target/RR integrity;
- True Range;
- Wyckoff event recency;
- evidence availability;
- candidate-builder alignment;
- swing applicability readiness blockers;
- fixed-profile orchestrator profile contracts;
- data-readiness remediation no-peek and duplicate-identity boundaries;
- Artifact Lineage v1 semantics.

No Strategy semantic change was added.

## Blockers

Data acquisition remains blocked by:

- fixed start date not approved;
- fixed end date not approved;
- 4h bar-construction policy not approved;
- session policy not approved;
- adjustment and corporate-action provenance not finalized;
- pagination and completeness acceptance not approved.

## Remaining Limitations

- No provider API, account portal, billing record, API key, or credential value
  was inspected.
- No provider call was made.
- No raw or normalized artifact was written.
- Existing historical 4h and daily dataset provenance remains unresolved.
- No local aggregation was implemented.
- Market-calendar completeness is not implemented.
- The research protocol remains blocked.
- Predictive usefulness and profitability remain unaccepted.

## Final Acceptance Statement

Acquisition-contract tooling is accepted.

Data acquisition remains blocked and disabled.

No data was downloaded. No annotation or candidate was generated. Research
protocol remains blocked. No predictive or profitability acceptance exists.
