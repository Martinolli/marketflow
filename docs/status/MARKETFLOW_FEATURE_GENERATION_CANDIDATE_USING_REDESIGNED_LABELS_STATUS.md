# MarketFlow Feature Generation Candidate Using Redesigned Labels Status

## Branch And Scope

- Branch: `feature/feature-generation-candidate-redesigned-labels-v1`.
- Exact base approval commit: `e66380b10d49aa45dacc77097d3b641f565e2b69`.
- Scope: deterministic, offline, digest-bound candidate planning for future feature generation using reviewed redesigned labels.
- This candidate is design-only. It does not approve or perform feature generation.

## Candidate Artifact

- Artifact: `FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS`.
- Status: `FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS_READY_FOR_OPERATOR_REVIEW`.
- Schema: `feature_generation_candidate_using_redesigned_labels_v1`.
- Deterministic candidate digest: `21b3bc905f3d553f4ec74bd70f758bbbc9be02ae906af1732c3b4fb5aaf12d1e`.
- Checklist: `47 / 47` passed, `0` failed, `0` blockers.

## Bound Evidence

- Planning approval: `6f4c1ce989e76e2b2ee835056e146f362b6d7c70b44bb6fc864f3f125c9dc54d`.
- Planning candidate review/candidate: `82495e036e79777e6cb69935f98051e76c7b7296254cb82990e34217a82a67e8` / `6de09ba499a262d6c7a1e5a0a69fee875c855bed86b78f28db4e099109a78251`.
- Redesigned-label results review/execution/approval: `f596d19db635735137c5d7073675a52b51444fa90d6a3acf09cc2aa0bc4ddd42` / `0c1151794d913ead1653e5641e70f731932da2e9059dd534a14eec0ca5307506` / `280734ff469c4bfb07f67060e8077b173e034fa9b9dd6b7e82225eb881337247`.
- Research registry/canonical records/label values: `5f0ce29bd06f1a0d5f1ce3dd8e31b8c8e52d616673f119326377538228d3d958` / `fbd7c1b17b42e5d4f82a9162b31b45fdfeef46f0e9ee7d29d74c926f0cf19044` / `2de373ca60ef8ec47b500444784d9851908b9a90837aa937c3716ade589f849f`.

## Dataset And Redesigned Labels

- Dataset/profile/timeframe: `expanded_universe_canonical_dataset_v1` / `RTH_FULL_SESSION_1D` / `1d`.
- Date range: `2022-01-01` through `2025-12-31`.
- Ordered universe: `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`.
- Frozen record total: `11946`; META remains `913`, and every other ticker remains `1003`.
- Reviewed redesigned-label outputs/families/threshold strategies/horizon strategies: `11 / 10 / 7 / 5`.
- Label rows/coverage entries/available/unavailable: `143352 / 144 / 142200 / 1152`.

## Candidate Design

- Objective: `PREPARE_FEATURE_GENERATION_CANDIDATE_USING_REDESIGNED_LABELS`.
- Scope/mode/authority: `CANDIDATE_ONLY_NOT_APPROVAL_NOT_GENERATION` / `PLANNED_NOT_GENERATED` / `NOT_AUTHORIZED`.
- Ten reviewed source inputs remain `SOURCE_REVIEWED_NOT_REGENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.
- Ten feature families and seventeen feature groups are planned for operator review. No feature values exist.
- The planned sixteen-field schema, ten alignment controls, ten future quality checks, and ten planned outputs remain unexecuted or ungenerated.
- Twelve deterministic per-ticker entries preserve exact order and record counts. META explicitly carries `PRESERVE_META_LIMITATION_IN_FEATURE_GENERATION_CANDIDATE`.

## Authority Boundary

- `feature_generation_candidate_created` and the redesigned-label-specific candidate-created/ready flags are true.
- `ready_for_feature_generation_approval` remains false; operator review is the next gate.
- Feature generation authorization/performance, feature values, metric recomputation, model training, additional predictive-evidence candidacy/execution, and strategy scoring remain false.
- Predictive usefulness and profitability remain `not accepted`.
- Runtime, strategy, paper-trading, and broker execution remain `NOT_AUTHORIZED`; trade recommendations remain false.
- No provider request, `.env` access, live transport, market-data acquisition, dataset regeneration, redesigned-label regeneration, feature generation, metric recomputation, training, predictive execution, runtime activation, broker action, or trading action occurred.

## Next Task

- `Feature Generation Candidate Operator Review Package Using Redesigned Labels v1` is the next separate task.
