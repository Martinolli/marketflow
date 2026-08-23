# MarketFlow Algorithm Strategy Charter v1 Plan

## Purpose

Define an expectancy-first trend-and-flow research direction after the prior predictive-usefulness chain was finalized and archived as not ready. This artifact is a concept and requirements charter only; it creates no labels, targets, features, evidence, backtest, model, acceptance, runtime, or trading authority.

## Source Final Archive Summary

Bind `MARKETFLOW_PREDICTIVE_USEFULNESS_FINAL_ARCHIVE_SUMMARY_USING_IMPROVED_EVIDENCE`, status `MARKETFLOW_PREDICTIVE_USEFULNESS_CHAIN_FINALIZED_ARCHIVED_NOT_READY`, and digest `31b61c934f3bc4970973dd2cfc0e18fb3ea4ca76e02c815bed5cf509e4a5440b`. Preserve the complete upstream archive, selection, closure, readiness, reassessment, evidence, matrix, feature, label, registry, and records chain without mutation or rerun.

## Dataset and Universe

Preserve `expanded_universe_canonical_dataset_v1`, `RTH_FULL_SESSION_1D`, daily data from `2022-01-01` through `2025-12-31`, all `11946` records, and the exact ordered universe `MSFT`, `NVDA`, `AMZN`, `GOOGL`, `META`, `TSLA`, `JPM`, `XOM`, `JNJ`, `WMT`, `CAT`, `LMT`. META remains at `913`; every other ticker remains at `1003`.

## Algorithm Identity

Direction: `EXPECTANCY_FIRST_TREND_AND_FLOW_ENGINE`.

MarketFlow is an expectancy-first trend-and-flow engine designed to identify tradable directional structure using price, volume, relative strength, volatility, regime context, and abstention/no-trade logic.

## Strategy Philosophy

Do not optimize for classification accuracy alone. Optimize for tradable expectancy, risk-adjusted opportunity, and abstention quality. Ask first whether identified conditions retain positive expected value after risk, costs, drawdown, and position-management constraints; classification against simple baselines is secondary.

## Strategy Principles

Define ten principles covering expectancy, trend quality, volume-price confirmation, relative strength, regimes, abstention, risk/reward, cost/slippage awareness, simple baselines before complex models, and separate runtime authorization.

## Research Questions

Define the ten charter questions covering early trend quality, continuation/exhaustion, relative-strength selection, abstention, cost-adjusted expectancy, VPA/Wyckoff comparison, cross-ticker/regime stability, risk filters, majority-class traps, and non-recommendation watchlists.

## Candidate Objective Families

Define the ten requested expectancy, risk/reward, material-move, continuation, reversal, drawdown, abstention, relative-strength, regime, and payoff-asymmetry objective families. Keep every entry `CANDIDATE_OBJECTIVE_NOT_GENERATED`, research-only, non-actionable, and unauthorized for label or target generation.

## Candidate Signal Families

Define the ten requested trend, VPA, close/spread, effort/result, relative-strength, volatility, breakout/pullback, absorption/distribution, regime, and abstention signal families. Keep every entry `CANDIDATE_SIGNAL_NOT_GENERATED` with feature generation unauthorized.

## Candidate Validation Metrics

Define all fourteen requested expectancy, profit-factor, win/loss, drawdown, hit-rate, cost, turnover, exposure, R-multiple, stability, baseline, and abstention metrics. Keep every entry `CANDIDATE_METRIC_NOT_COMPUTED` with computation unauthorized.

## Candidate Baselines

Define all seven requested buy-and-hold, majority/no-trade, previous-direction, trend, VPA/Wyckoff, relative-strength, and shuffled-control baselines. Keep every entry `CANDIDATE_BASELINE_NOT_EXECUTED` with training and backtesting unauthorized.

## Phase Plan

Record Phase 1 as completed by this charter. Keep Phases 2–9 `FUTURE_NOT_STARTED`, covering objective candidacy, operator review/approval, objective execution, simple-rule baseline, backtest lab, results/reassessment, paper-research readiness, and separately authorized runtime.

## Acceptance Gates

Define all ten requested future gates. Keep each `CLOSED_FUTURE_GATE` with `approval_created = false` and `execution_created = false`.

## Non-Goals

No recommendations, live/paper/broker trading, runtime activation, profitability claim, predictive-usefulness acceptance, scoring, market-data acquisition, label generation, feature generation, model training, or backtest execution occurs in this charter.

## Risk Controls

Maintain all 23 service-defined controls. They prohibit generation, execution, computation, scoring, acceptance, runtime, strategy, and trading authority and preserve the frozen dataset, reviewed outputs, predictive evidence, and META limitation.

## Guardrails

Run entirely offline. Do not call providers, inspect `.env`, enable live transport, modify `.marketflow`, mutate source artifacts, store or print API keys, commit raw provider payloads, or modify broker/IBKR code. Default tests remain deterministic and credential-free.

## Next Task

`MarketFlow Algorithm Strategy Charter Operator Review v1`.
