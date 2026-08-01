# MarketFlow Analytical Segment Policy

## Status

Policy status: IMPLEMENTED FOR OFFLINE SYNTHETIC TAGGING.

The analytical segment engine receives explicit ex-dividend evidence and does
not call a corporate-action provider.

## Inputs

Permitted ex-dividend evidence:

- ex-dividend date;
- one or more immutable event IDs;
- dividend event-set digest.

Multiple events on the same date create one continuity boundary and retain all
event IDs.

## Boundary Rules

For a normal full ex-dividend session:

- the continuity boundary begins before the first canonical bar of that
  session;
- both `SWING` half-session bars belong to the new segment;
- the `POSITION_SWING` daily bar belongs to the new segment.

For an early-close or closed ex-dividend date:

- no canonical bar is generated for that date;
- the boundary begins at the first canonical bar of the next eligible full
  session.

## Segment Model

Segments record:

- analysis segment ID;
- profile;
- source dataset digest;
- dividend event-set digest;
- segment-start session date;
- first canonical bar timestamp;
- start reason;
- trigger event IDs;
- deterministic segment digest.

Start reasons:

```text
DATASET_START
EX_DIVIDEND_CONTINUITY_RESET
```

## Readiness Boundary

New segments are tagged:

```text
ANALYTICAL_SEGMENT_WARMUP
```

The implementation does not add fixed global waits, manual unlocks, fabricated
readiness, or candidate actionability.

## Prefix Safety

The prefix helper returns only bars from the current analytical segment through
decision row `T`. It never includes previous-segment rows or future rows.

Focused tests cover future-bar invariance, future-event invariance, and
post-boundary prefix isolation.
