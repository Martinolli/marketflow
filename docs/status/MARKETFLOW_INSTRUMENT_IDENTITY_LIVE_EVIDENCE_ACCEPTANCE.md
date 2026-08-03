# MarketFlow Instrument Identity Live Evidence Acceptance

Status: PASS

UTC acceptance date: `2026-08-03T15:58:04Z`.

## Scope

This document records corrected final offline acceptance of the already
completed MarketFlow Instrument Identity live evidence candidate.

The previous acceptance gate incorrectly required seven manifests. The frozen
source-defined live flow creates exactly six manifests, and no seventh artifact
is defined by production source.

No production source was modified for this acceptance. No additional provider
request was executed, no credential was requested or inspected, and no raw
provider-response body was printed, copied, or added to documentation.

## Repository State

- repository: `marketflow`
- branch: `feature/swing-instrument-identity-live-evidence`
- accepted base HEAD:
  `95a08bd9b854dadaa9f8e526311d030bd618128c`
- accepted base message: `fix: harden identity repository preflight`

Production source freeze was verified before acceptance documentation work:

- `marketflow/source_authority/instrument_identity.py`:
  `16b5460407710f8b0743458da6be949d5f8c464d55c0a575784427dfa64fd40c`
- `marketflow/source_authority/__init__.py`:
  `1e8ec2e511594ca7d3c49b2657a720988591214d63e2cc1ad3e1b39315eace4b`
- `marketflow/source_authority/__main__.py`:
  `8ccbfc68e095aa6cec56909ac2caf10ac465c746bd90ad43204055f598792a4d`

## Specification

- identity specification schema:
  `marketflow.instrument_identity_specification.v1`
- identity specification digest:
  `a728408f59948cd3cd244816fe99a1d85e8d381b53f8e03d61e2d751c22ff3ba`
- provider business identity: `MASSIVE.COM`
- ticker: `AAPL`
- start snapshot date: `2022-01-01`
- end snapshot date: `2025-12-31`

The specification digest reproduced unchanged during acceptance.

## Corrected Runtime Inventory

The fixed live run was selected by exact run ID:

`ident-509de6e2eb5e4a1db785e034bcfaf045`

The accepted source-authorized manifest inventory is:

- `TICKER_OVERVIEW_RAW_RESPONSE`: 2
- `TICKER_OVERVIEW_SNAPSHOT`: 2
- `IDENTITY_CONTINUITY_CANDIDATE`: 1
- `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT`: 1
- total: 6

Acceptance rejects latest-directory, first-directory, directory-neighbor, or
filename-parent substitution. No additional unsupported artifact type was
accepted.

## Manifest And Payload Integrity

All six manifests validated with schema:

`marketflow.instrument_identity_artifact_manifest.v1`

Validation confirmed:

- common nonempty run identity;
- nonempty artifact identities;
- expected artifact type and stage pairs;
- safe relative payload references;
- lexical and physical runtime-root containment;
- no accepted symlink, junction, or reparse indirection;
- regular-file payloads;
- exact payload byte sizes;
- exact payload SHA-256 values;
- semantic payload digests where applicable;
- saved-disk manifest reload and validation.

Raw-response payload bytes were used only for integrity validation through the
artifact validator. Their bodies were not printed, parsed into documentation, or
included in the public receipt.

## Raw Response Artifacts

Exactly two `TICKER_OVERVIEW_RAW_RESPONSE` artifacts are present, matching the
two fixed live snapshot requests. One is the parent of the start snapshot and
one is the parent of the end snapshot.

The accepted live result reported two provider requests. The runtime artifact
chain independently reconciles that count through the two raw-response parent
artifacts. The saved receipt payload is immutable and was committed before the
return-time request-count field was added by the live command return contract.

## Snapshot Artifacts

Start snapshot:

- artifact type: `TICKER_OVERVIEW_SNAPSHOT`
- as-of date: `2022-01-01`
- semantic digest:
  `75a3fb5cccda09c05001129ec7161ad479457a714a5903828c67c5cfeb965928`
- artifact identity: nonempty
- raw parent: validated

End snapshot:

- artifact type: `TICKER_OVERVIEW_SNAPSHOT`
- as-of date: `2025-12-31`
- semantic digest:
  `5e80a556b6172d8ca8985177f8c17e05183322fb5981ba92def57d4698aa4f50`
- artifact identity: nonempty
- raw parent: validated

Both snapshots preserve the strict identity projection. No identity fields were
fabricated.

## Critical Identity Comparison

The start and end snapshots match on the accepted critical identity projection:

- ticker: `AAPL`
- market: `stocks`
- locale: `us`
- currency: `usd`
- primary exchange: `XNAS`
- Composite FIGI: `BBG000B9XRY4`
- Share Class FIGI: `BBG001S5N8V8`
- security type: `CS`
- active at start: `true`
- active at end: `true`
- delisting evidence at both boundaries: `NOT_RETURNED`

Automatic stitching remains prohibited. The result was not inferred from ticker
alone, newest-response preference, or provider-profile repair.

## Continuity Candidate

The continuity artifact is:

`ident-art-8607986a2341423182614a41c6236ed9`

It validates as:

`IDENTITY_CONTINUITY_SUPPORTED`

The continuity manifest binds the exact start and end snapshot artifact
identities. The continuity payload binds the exact start and end semantic
digests listed above.

This remains a continuity candidate only:

`IDENTITY_CONTINUITY_CANDIDATE`

## Receipt Binding

Exactly one `INSTRUMENT_IDENTITY_EVIDENCE_RECEIPT` artifact is present.

Receipt evidence confirmed:

- receipt manifest artifact identity is nonempty;
- saved receipt run identity is nonempty;
- start snapshot artifact identity is nonempty;
- end snapshot artifact identity is nonempty;
- receipt manifest binds the exact continuity artifact;
- saved receipt binds the exact start and end snapshot artifacts;
- saved receipt binds the exact start and end semantic digests;
- continuity status is `IDENTITY_CONTINUITY_SUPPORTED`;
- classification is `PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL`;
- Ticker Events audit status is `TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`;
- canonical eligibility is `false`;
- registry eligibility is `false`;
- generation-freeze eligibility is `false`;
- Strategy enablement is `false`.

The receipt and this document remain sanitized. They exclude credential
material, raw request or response data, request identifiers, provider account
data, local machine paths, nonidentity profile payload details, Strategy
authority, performance values, and execution authority.

## Authority Boundary

The accepted live result is:

`PROVIDER_IDENTITY_EVIDENCE_CANDIDATE_NONCANONICAL`

and:

`IDENTITY_CONTINUITY_SUPPORTED`

It does not establish final identity authority, identity-segment freeze,
canonical eligibility, registry eligibility, acquisition-generation eligibility,
or Strategy authority because Ticker Events audit remains deferred:

`TICKER_EVENT_AUDIT_NOT_IMPLEMENTED`

## Repository-Root Correction

This acceptance follows the repository-root correction committed in
`95a08bd9b854dadaa9f8e526311d030bd618128c`. Production output authority remains
the repository-derived ignored identity runtime root. Current working directory,
shadow runtime trees, timestamps, latest/first ordering, and report roots are
not accepted as source authority.

## Review Findings

Reviewer A found no medium, high, or critical finding in the exact
six-manifest inventory, payload/path integrity, raw-to-snapshot lineage,
snapshot-to-continuity lineage, or receipt binding.

Reviewer B found no medium, high, or critical finding in the critical-field
comparison, automatic-stitching prohibition, Ticker Events deferral,
noncanonical authority flags, or documentation boundary.

Both reviews were read-only. Neither review modified production source,
runtime evidence, credentials, or provider data.

## Remaining Limitations

This acceptance does not perform or authorize:

- Ticker Events continuity audit;
- split or dividend evidence audit;
- calendar or RTH authority freeze;
- canonical registry promotion;
- acquisition-generation authority;
- Strategy, Monte Carlo, outcome, performance, broker, or execution activity;
- report rewrite;
- runtime migration.
