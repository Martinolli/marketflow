# MarketFlow Live Smoke Credential Policy

## Scope

This policy applies only to the future interactive Massive.com one-month smoke
run. The current implementation acceptance is offline and does not inspect or
use an actual API key.

## Credential Entry

The only live credential entry path is:

```text
getpass.getpass(...)
```

The hidden prompt is reached only after a digest-bound operator confirmation
phrase is accepted.

Credentials are not accepted through CLI arguments, environment variables,
config files, visible standard input, URLs, browser storage, provider portals,
provider account pages, billing systems, or credential stores.

## Secret Wrapper

The runner constructs the accepted `ProviderApiKey` wrapper after the hidden
prompt. The wrapper rejects empty values, surrounding whitespace, CR/LF,
control characters, and header-injection material. Public string and repr forms
are redacted.

The key exists only in process memory and is discarded after the smoke run
attempt.

## Public Evidence

Smoke receipts exclude API keys, Authorization headers, raw request URLs, raw
`next_url`, raw provider bodies, OHLCV values, VWAP values, transaction-count
values, absolute paths, provider account data, and raw exception strings.

For HTTP 200 responses, strict response parsing and continuation credential
screening happen before raw page artifact persistence. A response body with a
credential-like continuation parameter is rejected without retaining that raw
body in the smoke artifact tree.

## Interactivity

Live smoke execution rejects noninteractive standard input/output, redirected
input, piped secrets, and unattended execution. Tests use a private injected
prompt seam with fictional credentials and mock HTTP only.

## Noncanonical Boundary

A successful smoke receipt remains noncanonical. It does not enable acquisition,
approve canonical data, validate Strategy behavior, prove profitability, access
broker systems, or migrate normal runtime behavior.
