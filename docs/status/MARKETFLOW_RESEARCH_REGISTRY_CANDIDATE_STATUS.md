# MarketFlow Research Registry Candidate Status

## Branch And Commit

- Branch: `feature/research-registry-candidate-v1`.
- Base commit: `73b8a85f7953fbd322af8581f81853cad44027ae`.
- Implementation commit: `Add research registry candidate` (recorded by Git after this document is staged).

## Candidate Artifact And Status

- Artifact/status: `RESEARCH_REGISTRY_CANDIDATE` / `RESEARCH_REGISTRY_READY_FOR_OPERATOR_REVIEW`.
- Schema version: `research_registry_candidate_v1`.
- Candidate digest: `e62cbf4ccfbf6377f64c92ed39d1c300188f0b9923e7f8da74827db2149b7865`.
- Objective: `PLAN_RESEARCH_REGISTRY_ADMISSION_FOR_FROZEN_CANONICAL_DATASET_EXPANDED_UNIVERSE`.
- Scope/mode/authority: `REGISTRY_CANDIDATE_ONLY_NOT_APPROVAL` / `PLANNED_NOT_APPROVED` / `NOT_APPROVED`.

## Source Frozen Canonical Dataset

- Freeze digest: `02af746fa11fa292a84e000ff8ca19a0b4ab36937558f938e4ac04eef6be92fc`.
- Results-review digest: `b2815bf7e1fa26db6e852bc04148659cabfd96a58232982245ec291dcac5d37d`.
- Generation digest: `9250ce29d7ba9754b43cfde07a5ded937a9402563691757a5aa6f7014f30fdbb`.
- Generation approval digest: `0b287370e8eddad522765a2ee77c39765f6690b27468bcc2f5b28587330a63b2`.
- Source binding mode: `COMMITTED_FREEZE_STATUS_DIGEST_BOUND`; the candidate does not rebuild or mutate the frozen dataset.

## Target Universe

- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.

## Registry Candidate Metadata

- Dataset name: `expanded_universe_canonical_dataset_v1`.
- Dataset scope/profile: `CANONICAL_DATASET_GENERATION_RESEARCH_ONLY` / `RTH_FULL_SESSION_1D`.
- Date range/timeframe: `2022-01-01` through `2025-12-31` / `1d`.
- Target/record counts: `12 / 11946`.
- Records digest: `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044`.
- Data-quality status: `PASS_WITH_PRESERVED_SOURCE_LIMITATION`.
- Candidate label: `RESEARCH_ONLY_NON_ACTIONABLE`.

## Per-Ticker Registry Candidate Summary

- `MSFT`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `NVDA`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `AMZN`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `GOOGL`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `META`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `913` records; reduced-count flag `True`.
- `TSLA`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `JPM`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `XOM`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `JNJ`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `WMT`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `CAT`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- `LMT`: `PLANNED_READY_FOR_OPERATOR_REVIEW`, `1003` records.
- Every entry has a deterministic per-ticker registry-candidate digest.

## META Reduced Record Count Preservation

- META remains exactly `913` records while every other ticker remains exactly `1003`.
- The candidate does not repair, infer, smooth, normalize, backfill, or fabricate records.

## Future Registry Chain And Gates

1. Research Registry Candidate Operator Review Package v1.
2. Research Registry Approval Ceremony v1.
3. Research Registry Status Publication.
4. Additional predictive evidence planning, if required.
5. Predictive-usefulness reassessment, if required.
6. Profitability review chain, if required.
7. Runtime migration chain, if ever separately authorized.

- Every future gate remains separate; registry approval readiness is `False`.

## Risk Controls And Planned Outputs

- Controls prohibit registry approval without operator approval, predictive use without registry approval, runtime source switching, automatic stitching, broker/paper execution, trade recommendations, predictive/profitability acceptance, frozen-dataset mutation, raw-payload commits, and API-key storage.
- Six output definitions remain `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Authority Boundaries

- Candidate created/ready for operator review: `True / True`.
- Registry approved/approval artifact created: `False / False`.
- Additional predictive evidence execution authorized/performed: `False / False`.
- Predictive usefulness/profitability: `not accepted / not accepted`.
- Runtime migration approved/active: `False / False`.
- Runtime, strategy, paper trading, and broker execution remain `NOT_AUTHORIZED`.

## Checklist Summary And Guardrails

- Total/passed/failed/blockers: `47 / 47 / 0 / 0`.
- No provider request, live transport, market-data acquisition, dataset regeneration, registry approval, predictive acceptance, runtime activation, or trading action occurred.

## Next Task Recommendation

- `Research Registry Candidate Operator Review Package v1` remains separate future work.
