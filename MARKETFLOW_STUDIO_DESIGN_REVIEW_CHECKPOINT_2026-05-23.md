# MarketFlow Studio Design Review Checkpoint

**Date:** 2026-05-23  
**Checkpoint commit:** `4834c1c - Improve Studio navigation performance`

## Post-Checkpoint Update

- Analyst Chat skeleton - implemented after checkpoint.
- Analyst Chat skeleton was identified as the next milestone after this checkpoint.

## 1. Purpose

This checkpoint captures the current stable state of MarketFlow Studio after the responsiveness and performance pass. It documents what is implemented, how the current workflow should be used, what limitations remain, and which future features have already been defined but are not implemented in this milestone.

## 2. Current Design Status

MarketFlow Studio is currently a local Streamlit cockpit for reviewing generated MarketFlow reports, validating candidate setups, and preparing structured analyst context.

Current workflow:

Analysis -> Report review -> Chart review -> Legacy artifact generation -> Strategy Ranking -> Monte Carlo -> P&F validation -> Analyst Packet -> Wyckoff Analyst Prompt Preview -> Artifact archive

The latest design change replaced eager tab rendering with a sidebar Workspace selector and lazy artifact previews. This keeps hidden heavy pages and large saved artifacts from rendering on every rerun.

## 3. Implemented Capabilities

### Core Report Workflow

- Single ticker analysis
- Multi-timeframe support
- Load latest report
- Overview page
- Summary report review
- CSV preview
- Raw JSON review

### Charts and Artifacts

- Candlestick and volume charts
- Wyckoff event visualization
- P&F sidecar generation
- Legacy feature plot generation
- Generated artifact browser
- Lazy artifact preview
- Lazy download preparation
- HTML, JSON, TXT, CSV, and Markdown artifact support

### Strategy and Monte Carlo

- Strategy Ranking
- Strategy diagnostics
- Candidate-to-Monte Carlo handoff
- Monte Carlo single-run workflow
- Monte Carlo output file listing
- Monte Carlo HTML and JSON artifacts

### Analyst Packet

- Structured Analyst Packet generation
- Wyckoff/VPA extraction
- Selected CSV fallback
- P&F sidecar integration
- P&F traceability and matching
- Report baseline risk vs strategy trade plan separation
- Save/download Analyst Packet

### Wyckoff Analyst Prompt Preview

- Balanced, strict, and educational prompt styles
- No API call
- Editable prompt text
- Markdown preview
- Save/download prompt
- Saved prompt artifacts with style and timestamp

## 4. Usage Checklist

### Single Ticker Workflow

- [ ] Start Studio.
- [ ] Enter ticker.
- [ ] Select timeframes.
- [ ] Run analysis.
- [ ] Review Overview.
- [ ] Review Reports.
- [ ] Review CSV Preview.
- [ ] Review Charts.
- [ ] Generate P&F if needed.
- [ ] Generate legacy plots if needed.
- [ ] Preview artifacts only when needed.

### Strategy -> Monte Carlo Workflow

- [ ] Run Strategy Ranking without Monte Carlo first.
- [ ] Inspect candidate score, phase, event, and RR.
- [ ] Select candidate.
- [ ] Send candidate to Monte Carlo.
- [ ] Confirm entry, stop loss, and take profit.
- [ ] Run bootstrap first.
- [ ] Review TP-first, SL-first, neither, and R mean.
- [ ] Preview Monte Carlo artifacts if needed.

### P&F Validation Workflow

- [ ] Select matching annotated CSV.
- [ ] Generate P&F sidecar.
- [ ] Confirm source CSV/timeframe metadata.
- [ ] Preview saved P&F HTML.
- [ ] Build Analyst Packet.
- [ ] Confirm P&F selected sidecar and match reasons.

### Analyst Packet Workflow

- [ ] Build packet.
- [ ] Confirm ticker, timeframe, score, Monte Carlo, P&F, and risk rank.
- [ ] Check warnings.
- [ ] Check P&F traceability.
- [ ] Save/download packet.

### Wyckoff Analyst Prompt Workflow

- [ ] Build Analyst Packet first.
- [ ] Open Wyckoff Analyst.
- [ ] Choose prompt style.
- [ ] Build prompt.
- [ ] Review/edit prompt.
- [ ] Save prompt.
- [ ] Confirm saved markdown appears in Generated Artifacts.

## 5. Recommended Conservative Daily Flow

1. Run or load latest report.
2. Review Overview, Reports, CSV Preview, and Charts.
3. Generate P&F/legacy plots only for worthwhile tickers/timeframes.
4. Run Strategy Ranking without Monte Carlo first.
5. Send selected candidates only to Monte Carlo.
6. Build Analyst Packet.
7. Generate Wyckoff Analyst prompt.
8. Treat failed POP gate, failed P&F gate, weak score, or unclear Wyckoff context as caution/no-go.

## 6. Known Limitations

### Technical Limitations

- Studio is a local Streamlit app.
- Heavy Plotly HTML can still be slow when previewed.
- GARCH requires the optional `arch` package.
- Analyst Prompt Preview does not call an AI model.
- Old P&F sidecars without metadata have weaker matching.

### Analytical Limitations

- Strategy Ranking is a candidate filter, not a final decision.
- Monte Carlo is model-dependent.
- P&F objective direction/count quality still needs refinement.
- Analyst Packet requires human review.
- There is no automated trade recommendation.

## 7. Future Features Already Defined

### Near-Term

#### Analyst Chat Skeleton

- [ ] No automatic API calls.
- [ ] User must click Run Analyst.
- [ ] Prompt remains visible before execution.
- [ ] API key/config checked safely.
- [ ] No key = setup guidance, not crash.
- [ ] Response saved as markdown artifact.
- [ ] Response appears in Generated Artifacts.

#### Analyst Response Artifact Support

- [ ] Save AI response as markdown.
- [ ] Classify as `analyst_response_md`.
- [ ] Preview/download from Generated Artifacts.
- [ ] Link response to source packet/prompt.

#### P&F Objective Quality Refinement

- [ ] Improve bullish/bearish objective direction.
- [ ] Store count direction clearly.
- [ ] Store count source/column metadata.
- [ ] Avoid using bearish objective for long candidate unless flagged.
- [ ] Improve P&F gate notes.

#### Monte Carlo Backtest Refactor

A future planning file exists at `markdown_files/monte_carlo_backtest_refactor.md`. Do not implement it in this checkpoint.

- [ ] UI section for MC backtest.
- [ ] Backtest configuration form.
- [ ] Historical simulation windows.
- [ ] Accuracy/calibration metrics.
- [ ] Model comparison table.
- [ ] Artifact export.

### Medium-Term

#### Strategy/MC/P&F Decision Dashboard

- [ ] Unified candidate decision card.
- [ ] Strategy score.
- [ ] POP gate.
- [ ] P&F gate.
- [ ] Wyckoff quality.
- [ ] Risk rank.
- [ ] Analyst posture.

#### User Profile Configuration

- [ ] Editable analyst profile from UI.
- [ ] Risk settings.
- [ ] POP threshold.
- [ ] P&F threshold.
- [ ] Account/risk assumptions.
- [ ] Save profile locally.

#### Report Readability Upgrade

- [ ] Convert more report text into tables.
- [ ] Support/resistance cards.
- [ ] Wyckoff phase timeline.
- [ ] Event timeline.
- [ ] Warnings/missing data section.

#### Batch-to-Decision Workflow

- [ ] Run batch.
- [ ] Rank all candidates.
- [ ] Pick top candidates.
- [ ] Run MC selectively.
- [ ] Generate packets/prompts for top setups.

### Longer-Term

#### Analyst Memory / Research Notebook

- [ ] Store prior prompts/responses.
- [ ] Compare current setup to previous setups.
- [ ] Track ticker history.
- [ ] Track candidate outcomes.

#### Packaging and Robustness

- [ ] Dependency checks.
- [ ] Optional dependency notes.
- [ ] Smoke tests.
- [ ] Regression tests for packet/prompt generation.
- [ ] Streamlit performance profiling.

## 8. Design Review Conclusion

The current checkpoint is stable for local daily use as a review and preparation cockpit. The end-to-end workflow now supports report review, candidate filtering, Monte Carlo validation, P&F traceability, Analyst Packet generation, and markdown prompt preview with artifact archiving.

The next recommended milestone is:

`Analyst Chat skeleton - explicit user action, no automatic execution`
