# MarketFlow Instrument Identity Repository Root Correction

UTC correction date: `2026-08-03`.

Status: `INSTRUMENT_IDENTITY_REPOSITORY_ROOT_CORRECTION_IMPLEMENTED`.

## Finding

A controlled local live identity attempt reached the digest-bound confirmation
ceremony, accepted the confirmation phrase, displayed and completed the
`getpass` API-key prompt, then failed locally before any accepted identity
snapshot:

```text
InstrumentIdentityError: repository root could not be determined
```

The failed helper searched upward from the identity module for
`pyproject.toml` plus a `marketflow` directory. This source checkout is valid
but has no `pyproject.toml`, so the marker check failed. No Ticker Overview
provider request was completed, and no identity artifact or snapshot was
accepted from that attempt.

The public command also requested the hidden credential before nonsecret local
repository/runtime validation and allowed the expected local failure to escape
as a Python traceback, exposing an absolute local path.

## Correction

The instrument identity repository root now derives only from the source module
location:

```text
module_path = Path(__file__).resolve()
repository_root = module_path.parents[2]
repository_root = Path(__file__).resolve().parents[2]
```

For:

```text
<repo>/marketflow/source_authority/instrument_identity.py
```

the resolved root is:

```text
<repo>
```

The candidate root is validated with fixed repository evidence that exists in
this checkout:

- `AGENTS.md`
- `requirements.txt`
- `marketflow/source_authority/instrument_identity.py`
- `config/fixed_date_acquisition_contract_v2_1.toml`

The root must exist, be a directory, strictly resolve, contain the source module
by path semantics rather than string prefix, and have regular-file evidence.
Existing symlinks, junctions, or redirecting reparse points in trusted
repository/runtime paths are rejected where supported. Root failure uses the
fixed category:

`INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED`

## Runtime Root

Production identity output remains repository-derived and ignored by Git:

```text
<repository_root>/.marketflow/source_authority/identity/runs/
```

The runtime root is not derived from current working directory, environment
variables, CLI arguments, caller configuration, timestamps, latest-directory
discovery, report roots, canonical roots, or registry roots. A shadow
`.marketflow/source_authority/identity/runs/` tree beneath an unrelated current
working directory is not selected, scanned, or modified.

Private leading-underscore test seams may still pass pytest temporary roots and
mock transports for deterministic offline checks. Those seams are not exported,
not CLI-accessible, validate the supplied temporary roots, and cannot change the
fixed identity specification, ticker, dates, provider host, or public live
command runtime authority.

## Local Preflight

The public live command now keeps this order:

1. require interactive TTY;
2. print the sanitized fixed plan;
3. print the exact digest-bound confirmation phrase;
4. validate the operator confirmation;
5. perform nonsecret local preflight;
6. prompt for the API key through `getpass`;
7. construct the provider key wrapper and transport;
8. create the run and issue the two fixed Ticker Overview requests.

Local preflight validates repository-root derivation, fixed runtime-root
resolution, containment, existing-path physical safety, local artifact-writer
readiness, and source-defined dependency readiness before any credential prompt
or provider transport exists.

## Sanitized Failure Receipt

Expected local preflight failures return a nonzero exit code and a bounded
public receipt:

```text
status = INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED
failure_category = INSTRUMENT_IDENTITY_REPOSITORY_ROOT_UNRESOLVED
credential_prompted = false
provider_request_count = 0
runtime_artifact_written = false
canonical_eligibility = false
registry_eligibility = false
```

The public CLI output excludes Python tracebacks, absolute paths, exception
text, API keys, Authorization headers, URLs, account data, request IDs, and raw
provider bodies. Unexpected local failures are also reduced to a fixed sanitized
category at the public CLI boundary.

## Non-Regression Boundary

This correction does not change:

- identity schema;
- specification digest
  `a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`;
- fixed `AAPL` ticker;
- snapshot dates `2022-01-01` and `2025-12-31`;
- Ticker Overview endpoint;
- parser allowlists;
- identity projection;
- continuity comparison;
- automatic-stitching prohibition;
- Ticker Events deferral;
- artifact schema;
- receipt sanitization;
- authority flags.

No provider, Strategy, acquisition, calendar freeze, split/dividend audit,
Monte Carlo, outcome, performance, broker, execution, registry authority,
report rewrite, or runtime migration activity is part of this correction.

## Final Offline Acceptance

Final offline acceptance confirms:

- repository-root derivation passes from the identity source module without
  `pyproject.toml`;
- fixed repository evidence validation uses regular files under the resolved
  root;
- original repository evidence path components and resolved paths reject
  symlink, junction, or reparse indirection where supported;
- the production runtime root resolves to
  `.marketflow/source_authority/identity/runs/` beneath the repository;
- unrelated current working directories and shadow `.marketflow` runtime trees
  are ignored;
- operator confirmation occurs before local preflight;
- local preflight occurs before `getpass`, `ProviderApiKey`, transport
  construction, runtime-directory creation, artifacts, or provider requests;
- expected local failures return
  `INSTRUMENT_IDENTITY_LOCAL_PREFLIGHT_FAILED` with
  `credential_prompted = false`, `provider_request_count = 0`,
  `runtime_artifact_written = false`, and false authority flags;
- public local-failure output excludes traceback, absolute paths, exception
  text, URLs, request IDs, API keys, Authorization headers, account data, and
  raw provider bodies;
- plan and self-check remain offline, no-credential, no-provider, and
  mock-only;
- the identity specification digest remains
  `a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`;
- Ticker Events remains `TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`;
- canonical, registry, generation-freeze, and Strategy authority flags remain
  false.

Final local checks for this correction:

```text
env\Scripts\python.exe -m pip check
No broken requirements found.

env\Scripts\python.exe -m pytest -q tests/test_instrument_identity_evidence.py
67 passed

env\Scripts\python.exe -m pytest -q <related offline bundle>
438 passed

env\Scripts\python.exe -m pytest --collect-only -q
1025 tests collected

env\Scripts\python.exe -m pytest -q
1025 passed

env\Scripts\python.exe -W error -m compileall -q marketflow scripts apps trading_dashboard utils rag tests
pass

git diff --check
pass with Git LF-to-CRLF working-copy normalization warnings on modified text files
```

No network, provider, credential, or real market-data activity occurred during
the correction or final acceptance checks.

## Remaining Limitation

Final live identity tooling acceptance remains `BLOCKED` until the controlled
live identity command is repeated after this production correction. That future
run must still be noncanonical candidate evidence only and cannot create
canonical registry or Strategy authority without the remaining identity and
corporate-action evidence.
