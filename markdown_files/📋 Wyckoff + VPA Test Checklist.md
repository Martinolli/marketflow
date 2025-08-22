# Checklist for OpenAI model analysis

📋 Wyckoff + VPA Test Checklist

1. Bar & Volume Read (Micro)

  ✅ Wide spread + ultra-high volume? → Check for Climax (SC/BC).

  ✅ Narrow spread + ultra-low volume into S/R? → Check for No Demand / No Supply.

  ⚠️ Effort (volume) ↑, Result (price) flat? → Absorption (smart money active).

  ❌ High volume, no reversal or absorption? → Ignore, possible anomaly.

1. Short-Term Context

  ✅ Is volume rising with price ↑? → Bullish confirmation.

  ✅ Is volume falling with price ↓? → Bearish weakening.

  ⚠️ Mixed direction? → Neutral/sideways bias.

  ❌ High volume with flat closes? → Distribution/absorption suspicion.

1. Wyckoff Phase Recognition

  Phase A: Look for PS + SC + AR + ST.

  Phase B: Volatile swings, wide tests, no real break.

  Phase C: Spring (undercut support) or UTAD (fake breakout above resistance).

  Phase D: Trend resumption, strong rallies or breaks.

  Phase E: Clear departure, range abandoned.

  Raise Confidence If:

  Spring/UTAD is at correct location (low/high of range).

  Test volume is lower than the event’s volume.

  Breakout shows expanding spread + volume.

  Lower Confidence If:

  Spring/UTAD appears mid-range.

  No volume confirmation on test.

  Trend resumes weakly.

1. Support & Resistance Validation

  ✅ Check high-volume nodes (from your CSV/JSON volume_at_levels).

  ✅ Confirm tests (≥2 touches strengthens level).

  ⚠️ Weak levels = single touch + low volume.

  ❌ Ignore if price never interacts again.

1. Statistical / Confidence Score

  Assign 0–100% likelihood for scenario:

  <40% → Ignore (noise).

  40–65% → Possible, but weak.

  65–85% → Probable.

  >85% → Strong setup.

1. Risk & Trade Management

  Stop-loss = below SC / Spring (long) or above UTAD (short).

  Take-profit = nearest resistance/support cluster.

  Risk/Reward = must be ≥2.0 for trade to be valid.

  ✅ Adjust position sizing to keep account risk <1–2%.

1. Final Narrative Report

  Should always include:

  Market bias (Bullish / Bearish / Neutral).

  Key events (Spring, UTAD, SC, etc).

  Confidence level (numeric).

  Stop-loss, Take-profit, Risk/Reward.

  Cross-timeframe confirmation (if aligned).

  Great 🙌 — you’re set up with:

📚 Reference library (Coulling + Wyckoff + modern docs)

🗂️ RAG manifest starter for structured retrieval

✅ QA checklist for human validation alongside model output

  With these, you’ll be able to:

  Upload your knowledge base in the configuration window.

  Run test CSV/JSON/TXT segments.

  Use the checklist to score whether the model is conservative enough on Springs/UTADs, correct on S/R clustering, and accurate with VPA readings.

  Adjust confidence thresholds and rules as needed before hard-wiring them into JSON schema.

```bath
🗂️ Test Input (CSV Snippet, 1h timeframe)
timestamp,open,high,low,close,volume
2025-08-18 10:00:00,47.5,48.2,47.2,48.1,12500
2025-08-18 11:00:00,48.1,48.4,47.6,47.7,18600
2025-08-18 12:00:00,47.7,47.9,47.1,47.2,24500
2025-08-18 13:00:00,47.2,47.3,46.8,46.9,15800
2025-08-18 14:00:00,46.9,47.2,46.6,47.1,9200
2025-08-18 15:00:00,47.1,47.8,47.0,47.6,8700
2025-08-18 16:00:00,47.6,48.3,47.5,48.2,19600
```

🗂️ Test Input (JSON Report)

```json
{
  "ticker": "FLY",
  "current_price": 48.2,
  "timeframe": "1h",
  "trend": {
    "trend_direction": "SIDEWAYS",
    "price_change_percent": -0.63,
    "volume_trend": "INCREASING",
    "signal_type": "EFFORT_NO_RESULT",
    "signal_strength": "BEARISH",
    "details": "Price failed to rally despite rising volume"
  },
  "support_resistance": {
    "support": [{"price": 46.9, "strength": 3, "tests": 2}],
    "resistance": [{"price": 48.4, "strength": 2.5, "tests": 1}]
  },
  "wyckoff": {
    "context": "Distribution",
    "events": [
      {"timestamp":"2025-08-18 12:00:00","event":"UT","details":"False breakout above resistance, immediate failure"}
    ]
  }
}
```

📊 Expected Model Output (Benchmark Style)
  Narrative

  Price action in FLY (1h) suggests a potential distribution structure. A false breakout (UT) above resistance at 48.4 failed immediately, accompanied by rising volume without bullish progress — a textbook case of effort vs result. This aligns with Wyckoff’s description of Phase C UTAD risk.

  The market remains bounded between support at 46.9 (strength 3, multiple tests) and resistance near 48.4.

  QA Checklist Highlights

  Wide spread + high volume at 12:00 → matches UT.

  Effort ↑, result flat → bearish absorption.

  Confirmation bar still needed below 46.9 → event unconfirmed.

⚠️ Confidence: 65% (possible, not strong).

  Risk/Trade Plan

  Bias: Bearish (Distribution risk).

  Stop-loss: 48.6 (above UT).

  Take-profit: 46.9 (support retest).

  Risk/Reward: 2.1 (valid).

  Probabilistic Outcome

  Breakdown below 46.9: ~70% likelihood.

  Rebound to retest 48.4: ~30% likelihood.

🗂️ Test Input (CSV Snippet, 1h timeframe — Spring & Test)

```csv
timestamp,open,high,low,close,volume
2025-08-18 08:00:00,46.2,46.5,45.9,46.0,18200
2025-08-18 09:00:00,46.0,46.1,45.5,45.6,25500
2025-08-18 10:00:00,45.6,46.0,45.3,45.9,21400
2025-08-18 11:00:00,45.9,46.4,45.2,46.3,26800   # Spring bar: undercut prior support, close well off low
2025-08-18 12:00:00,46.3,46.6,46.1,46.5,15300   # Test: narrow spread, lower volume than Spring
2025-08-18 13:00:00,46.5,47.0,46.4,46.9,19800   # Follow-through up
2025-08-18 14:00:00,46.9,47.5,46.8,47.4,24100   # Expansion on rally
```

🗂️ Test Input (JSON Report)

```json
{
  "ticker": "FLY",
  "current_price": 47.4,
  "timeframe": "1h",
  "support_resistance": {
    "support": [{"price": 45.6, "strength": 3.5, "tests": 3}],
    "resistance": [{"price": 47.8, "strength": 2.5, "tests": 1}]
  },
  "wyckoff": {
    "context": "Accumulation",
    "events": [
      {"timestamp": "2025-08-18 11:00:00", "event": "Spring", "details": "Undercut prior support, close off lows"},
      {"timestamp": "2025-08-18 12:00:00", "event": "Test", "details": "Narrow spread, lower volume than Spring"}
    ]
  },
  "trend": {
    "trend_direction": "UP",
    "price_change_percent": 3.9,
    "volume_trend": "INCREASING",
    "signal_type": "CONFIRMATION",
    "signal_strength": "BULLISH",
    "details": "Rising price with rising volume after test"
  }
}
```

📊 Expected Model Output (Benchmark Style)
  
  Narrative

  The 11:00 bar undercuts established support near 45.6 on elevated volume and closes well off the low — a classic Spring candidate. The 12:00 bar is a narrow-range up close on lower volume relative to the Spring, holding above 45.6 — a successful Test. Subsequent bars expand upward with improving spread and steady volume, consistent with Phase C → D transition in an Accumulation context.

  VPA Alignment

  Spring: wide down→up bar, high volume, close off lows ✔️

  Test: narrower spread, lower volume than Spring, holds above support ✔️

  Follow-through: result > effort, expanding spreads on the rally ✔️

  Wyckoff Framing

  Structure: Accumulation.

  Events: Spring (C) → Test (C) → BU/LPS (early D).

  Confidence: 0.72 (High) due to location, volume relationship, and clean follow‑through.

  QA Checklist Highlights

  Spring at correct location (range low)

  Test on lower volume, holds above spring low

  Demand bars with expanding spread post‑test

  Bonus: Acceptance above next resistance 47.8 would upgrade to very high confidence

  Probabilistic Outcome (generic)

  Continuation up: 0.68

  Neutral drift: 0.20

  Reversal down: 0.12

  Levels & Heatmap (from JSON)

  Support: 45.6 (tests=3) — anchor for invalidation

  Resistance: 47.8 — next gate

  Current price: 47.4 → Δ to 47.8 = +0.4 (+0.84%)

  Final Summary

  Bias: Constructive → Bullish (Spring/Test confirmed)

  TP candidate: 47.8 (first gate), then trailing higher once accepted

  SL candidate: <45.6 (below Spring/Test)`

Risk rank: 🟢 1 (Low) once above 47.8 with hold; 🟡 2 (Med) before breakout
