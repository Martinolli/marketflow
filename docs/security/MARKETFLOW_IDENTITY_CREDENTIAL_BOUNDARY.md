# MarketFlow Identity Credential Boundary

## Offline Default

Instrument Identity Evidence v1 is offline by default. Module import, the plan
command, and the self-check command do not request credentials, read environment
variables, inspect provider accounts, open sockets, or write persistent
identity artifacts.

Automated tests use only `httpx.MockTransport`, fictional key strings, and
pytest temporary directories.

## Live Command Boundary

The live command is implemented for a future controlled provider run, but it was
not executed in this task.

The command requires:

- an interactive TTY;
- display of the sanitized plan;
- an exact digest-bound confirmation phrase;
- confirmation before credential prompt;
- API key entry through `getpass` only after confirmation.

The key is passed in memory to the accepted provider-key wrapper and is used in
the bearer header only. It is not accepted in a URL, CLI argument, environment
lookup, persistent artifact, public receipt, or public error field.

## Receipt Boundary

Public receipts may contain the standardized identity fields under review,
artifact IDs, semantic digests, fixed statuses, and false authority flags.

Public receipts exclude secrets, authorization material, raw URLs, request ID
values, raw provider bodies, provider account information, local absolute paths,
raw exception text, performance/candidate data, and non-identity provider
metadata.

Future live raw response bytes are retained only inside the ignored
source-authority artifact root and are parent evidence for the sanitized
snapshot projection. Raw bytes are never copied into the public receipt.

## Authority Boundary

A future successful live run means only that two point-in-time Ticker Overview
snapshots were retrieved and their bounded identity projections were compared.

It does not mean Ticker Events continuity, split/dividend evidence,
calendar authority, registry authority, Strategy source authorization,
performance readiness, broker access, execution readiness, or runtime migration
has been approved.
