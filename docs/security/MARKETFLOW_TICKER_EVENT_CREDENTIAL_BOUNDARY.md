# MarketFlow Ticker Event Credential Boundary

MarketFlow Ticker Events Supporting Audit v1 keeps credentials outside default
offline tests and documentation.

## Offline Default

No live Ticker Events request occurred in this task.

No actual Massive.com key was requested, inspected, read from environment
variables, printed, logged, or committed. Tests use fictional credential text
and `httpx.MockTransport` only.

## Live Boundary

The controlled live command requires:

1. interactive TTY;
2. sanitized fixed plan display;
3. exact digest-bound confirmation phrase;
4. operator confirmation;
5. nonsecret local preflight;
6. `getpass` credential prompt only after preflight succeeds;
7. one fixed Ticker Events request.

Preflight validates repository root, accepted identity evidence, runtime root,
artifact writer readiness, and local dependencies before any credential prompt
or HTTP transport construction.

## Sanitization

Public receipts exclude API key, Authorization header, raw URL, request ID, raw
response body, provider asset name, account data, absolute paths, raw
exceptions, market prices, candidate values, and performance values.

Ticker-change dates and reported ticker symbols may appear because they are the
bounded evidence being reviewed.

The audit is supporting evidence only, with no automatic stitching and false
canonical, registry, identity-freeze, and Strategy authority flags.
