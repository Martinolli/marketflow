# MarketFlow Predictive Usefulness Review v1 Plan

## Purpose
- Define the path from research-only campaign result readiness to a later predictive usefulness review.
- Preserve the distinction between technical data readiness and predictive evidence.
- Keep predictive usefulness, profitability, runtime migration, paper trading, and broker execution outside the current authority.

## Source Campaign Results
- Source results review artifact: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE`
- Source results review status: `RESEARCH_APPLICABILITY_CAMPAIGN_EXECUTION_RESULTS_REVIEW_PACKAGE_READY`
- Source results review digest: `c0421913adbd4a0a02bb1d062a0ef1efd4081c4e1656a46073f4e45fdfd4408b`
- Source execution digest: `f3793401f2ad1b4f3df8b5d130bdb78629941422eaa753943abd43cf2be96f1c`
- Execution request ID: `AAPL_RESEARCH_APPLICABILITY_EXECUTION_2022_2025_V1`
- Outputs reviewed: `12`
- Data quality checks: `PASS`
- Module compatibility: `RESEARCH_ONLY_COMPATIBILITY_LISTED`
- Failure and warning count: `0 / 0`

## Data Quality Versus Predictive Usefulness
- Data quality readiness means the reviewed research outputs are technically loadable, internally consistent, and suitable for planning future experiments.
- Module compatibility readiness means the reviewed modules are listed as research-only compatible.
- These states do not prove predictive signal quality.
- These states do not accept predictive usefulness.
- These states do not accept profitability.
- These states do not authorize runtime migration or trading use.

## Required Future Predictive Experiments
- Define predictive labels and target horizons before any usefulness review.
- Define walk-forward experiment windows, purge or embargo rules, and out-of-sample splits.
- Define signal-quality metrics that do not claim profitability by default.
- Define baseline comparisons against simple non-strategy or naive alternatives.
- Define stability analysis across time windows and dataset profiles.
- Define false-positive and false-negative analysis where the label design supports it.
- Bind all experiment outputs by deterministic digest before operator review.

## Non-Goals
- Do not regenerate datasets.
- Do not rerun the research applicability campaign.
- Do not execute walk-forward validation in this candidate step.
- Do not run strategy scoring.
- Do not generate trade recommendations.
- Do not alter Strategy runtime behavior.
- Do not alter default dataset source behavior.
- Do not modify broker or IBKR code.
- Do not accept predictive usefulness or profitability.
- Do not approve runtime migration, paper trading, or broker execution.

## Guardrails
- Default tests remain deterministic and offline.
- Provider requests remain disabled for this review-candidate work.
- The predictive usefulness review candidate is a research-only operator-review artifact.
- Any future predictive review must bind source evidence, experiment plans, and output digests explicitly.
- Any future runtime migration remains a separate approval ceremony and is not implied by predictive planning.

## Next Tasks
1. Predictive usefulness review candidate operator review package.
2. Predictive experiment plan candidate.
3. Walk-forward experiment plan.
4. Predictive usefulness review after experiments.
