# MarketFlow Predictive Evidence Method Diagnostic v1 Plan

## Purpose

Explain, using only committed evidence, why predictive signal remains weak or mixed after the original and refined evidence cycles. The method diagnostic is diagnosis-only and supports operator selection of a possible future research path; it does not create or approve any candidate or execution.

## Source Planning-Tree Review

- Source artifact/status: `PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE` / `PREDICTIVE_EVIDENCE_PLANNING_TREE_REVIEW_PACKAGE_READY`.
- Source digest: `08c16babcfc22b5c1d3dec4d992ede553fdeea22a008021bdc3978a016a8aeb8`.
- Original/refined readiness decisions: `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY` / `PREDICTIVE_USEFULNESS_ACCEPTANCE_NOT_READY_USING_REFINED_EVIDENCE`.
- The source recommends method diagnostics before any additional execution loop.

## Diagnostic Domains

- Label objective, prediction horizon, and label thresholds.
- Overall feature signal, daily VPA features, relative strength, and cross-sectional context.
- Model families, baseline design, walk-forward protocol, OOS generalization, and calibration stability.
- Class balance/distribution, sample size/universe scope, data quality/META limitation, and acceptance criteria.
- Each domain is research-only, non-actionable, and requires no execution.

## Possible Failure Mechanisms

- Label objective, horizon, or thresholds may be misaligned with the available signal.
- The feature set, daily VPA context, relative-strength benchmarks, or twelve-ticker cross section may be insufficient.
- Market-regime variation, sample depth, model-family selection, or baseline design may dominate observed results.
- Acceptance thresholds may require formal precommitment.
- META's 913-record limitation remains explicit and is not repaired or inferred away.
- These are hypotheses for operator review, not predictive conclusions.

## Method Path Options

- Pause and archive the research chain.
- Create a Label Objective Redesign Candidate in a later task.
- Create a Feature Method Redesign Candidate in a later task.
- Create a Data Scope Expansion Candidate in a later task.
- Create a New Modeling Approach Candidate in a later task.
- `OPTION_G_ACCEPTANCE_CANDIDATE` remains `NOT_ALLOWED_CURRENTLY`.
- No option is selected or approved by the diagnostic package.

## Recommended Operator Selection

- Recommended path: `OPERATOR_METHOD_PATH_SELECTION`.
- Immediate action: `OPERATOR_METHOD_PATH_SELECTION_BEFORE_ANY_NEW_EXECUTION`.
- Reason: `TWO_CONSECUTIVE_READINESS_GATES_NOT_READY_AFTER_ORIGINAL_AND_REFINED_EVIDENCE`.
- Any later selection must be explicit and creates at most a separate planning candidate, not execution authority.

## Risk Controls

- No acceptance after failed readiness; no runtime activation, scoring, recommendations, broker execution, or paper trading.
- No more execution without a new review and method selection.
- Preserve the frozen dataset and META limitation.
- Keep every output research-only and non-actionable.
- Require operator review for any new path; the acceptance candidate remains unavailable.

## Non-Goals

- Creating label, feature, data-scope, or modeling redesign candidates.
- Running provider requests, acquisition, regeneration, predictive evidence, label/feature generation, metric recomputation, model training, or strategy scoring.
- Accepting predictive usefulness or profitability.
- Authorizing runtime, strategy use, paper trading, broker execution, or trade recommendations.

## Guardrails

- Bind the exact planning-tree, readiness, reassessment, refined-evidence, registry, and records digests.
- Preserve the exact universe, counts, evidence comparison, both not-ready decisions, and closed authorities.
- Use deterministic canonical JSON, fail-closed validation, and no-overwrite output writing.
- Keep planned templates `PLANNED_NOT_GENERATED` and `RESEARCH_ONLY_NON_ACTIONABLE`.

## Next Possible Tasks

1. Operator Method Path Selection v1.
2. Label Objective Redesign Candidate v1.
3. Feature Method Redesign Candidate v1.
4. Data Scope Expansion Candidate v1.
5. New Modeling Approach Candidate v1.
6. Pause and Archive Research Chain v1.
