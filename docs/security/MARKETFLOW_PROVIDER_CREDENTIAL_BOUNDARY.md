# MarketFlow Provider Credential Boundary

## Boundary

Provider credentials are accepted only through explicit constructor injection
into a narrow secret wrapper. The Massive transport does not read environment
variables, config files, browser data, provider portals, account pages, billing
data, or credential stores.

## Authentication

The only supported authentication form is:

```text
Authorization: Bearer <API_KEY>
```

API keys are never placed in URLs, query parameters, continuation identities,
manifests, receipts, logs, exceptions, dataclass comparison output, `repr`, or
`str`.

The transport rejects empty keys, surrounding whitespace, control characters,
and header-injection characters.

## Continuations

Provider `next_url` values are raw evidence only. Credential-like query
parameters are rejected, including `apiKey`, `api_key`, `token`,
`access_token`, `authorization`, `auth`, `key`, `user`, `username`, `account`,
and `account_id`.

Opaque cursor material is represented only by a nonreversible digest and
sanitized continuation identity.

## Acceptance State

This task uses fictional keys in mock HTTP tests only. No actual API key is
read, inspected, printed, stored, or validated against a provider.
