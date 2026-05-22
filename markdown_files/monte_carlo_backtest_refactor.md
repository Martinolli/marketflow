# **1. Feature Checklist & Descriptions**

* **Multiple Stochastic Models:** Offers five distinct methods for price path generation: Geometric Brownian Motion (GBM), Block Bootstrap, GARCH(1,1), ARIMA-GARCH, and an ML-augmented GBM.
* **Dual Execution Modes:** Supports "Single-Run" for analyzing a current trade setup and "Backtest" for validating model accuracy over historical data points.
* **Dynamic ML Integration:** Can load a pre-trained LightGBM model to predict forward volatility or train one on the fly using recent OHLCV data.
* **Automated Calibration:** Extracts drift ($\mu$) and volatility ($\sigma$) directly from the provided historical data on a per-bar basis.
* **Statistical Export:** Automatically saves complex run metrics (Probability of Profit, median time to hit targets, R-multiples) to a JSON file.
* **Rich Visualizations:** Generates interactive HTML plots via Plotly, including fan charts (price distribution) and hit histograms (time-to-target distribution).

---

## **2. Analysis Modes Explained**

### **Monte Carlo Trade Simulation (Single-Run)**

This mode is your forward-looking crystal ball. It takes your current market context (entry price, historical volatility, drift) and generates tens of thousands of potential future price paths over a set `horizon`. By evaluating how many of those paths hit your Take-Profit (TP) before your Stop-Loss (SL), the module quantifies the **Probability of Profit (POP)**. It moves you away from binary "will it go up or down" thinking and into professional probabilistic trading.

### **Backtest Simulation**

The backtest mode is the reality check for your Monte Carlo engine. Instead of predicting the future from the current bar, it steps back in time to past decision points. It runs a full Monte Carlo simulation at each historical step, predicts the POP, and then peeks at the *actual* future data to see if the trade won or lost. This calculates the **Model Calibration**—telling you if a setup that the model predicted had a 70% chance of success actually won 70% of the time historically.

---

## **3. Detailed Command-Line Examples**

**Scenario A: Standard Single-Run with Bootstrap**
Simulating a current Wyckoff setup on a 4-hour timeframe using historical resampling (Bootstrap).

```bash
python marketflow_monte_carlo_trade.py PANW_4h_wyckoff_annotated.csv --tp 206.54 --sl 192.77 --entry 197.21 --tf 4h --horizon 20 --model bootstrap --paths 20000 --block 8

```

*Description:* Evaluates a trade entering at 197.21. It generates 20,000 paths up to 20 bars into the future, shuffling 8-bar blocks of historical returns.

**Scenario B: Advanced ML-GBM Single-Run**
Using a LightGBM model to predict volatility for the GBM simulation.

```bash
python marketflow_monte_carlo_trade.py PANW_1d.csv --tp 206.54 --sl 192.78 --entry 197.21 --tf 1d --horizon 40 --model ml_gbm --ml-model "volatility_predictor.pkl"

```

*Description:* Uses the `volatility_predictor.pkl` model to assess current market features, predict the upcoming volatility, and feed that specific $\sigma$ into the GBM path generator.

**Scenario C: Rolling Backtest**
Testing the historical validity of a specific risk/reward profile.

```bash
python marketflow_monte_carlo_trade.py AAPL_1h.csv --simulate-backtest --bt-tp-pips 2.0 --bt-sl-pips 1.0 --bt-windows 40 --bt-step 5 --bt-paths 5000 --horizon 40 --seed 42 --bt-no-json

```

*Description:* Steps back through the `AAPL_1h.csv` file. It tests 40 different historical entry points, spaced 5 bars apart. At each point, it sets a TP $2.00 above the close and an SL $1.00 below, running 5,000 paths to check if the simulation accurately predicts the real outcome.

---

## **4. Comprehensive Parameter Dictionary**

### **Core CLI Arguments**

| Parameter | Type | Description |
| --- | --- | --- |
| `csv` | String | **Required.** The positional path to the OHLCV data file. |
| `--tp` | Float | **Required (Single).** The absolute price of the Take-Profit level. |
| `--sl` | Float | **Required (Single).** The absolute price of the Stop-Loss level. |
| `--entry` | Float | The absolute entry price. If omitted, defaults to the last closing price. |
| `--tf` | String | Timeframe of the chart (e.g., `1h`, `1d`). If omitted, inferred from the filename. |
| `--horizon` | Integer | Total future bars to simulate. Default is 20. |
| `--model` | String | The path generator: `bootstrap`, `gbm`, `garch`, `arima_garch`, `ml_gbm`. Default is `garch`. |
| `--paths` | Integer | The volume of simulated paths per run. Default is 20,000. |
| `--block` | Integer | Length of the data chunk sampled for the `bootstrap` model. Default is 8. |
| `--seed` | Integer | Random Number Generator seed for exact reproducibility. Default is 42. |
| `--nrows` | Integer | Limits memory usage by only loading the $N$ most recent rows. Default is 4000. |
| `--no-plots` | Flag | Disables the generation of Plotly HTML artifacts. |
| `--ml-model` | String | Absolute or relative path to a `.pkl` LightGBM model file. |
| `--mu-shift` | Float | An artificial scalar added to the calculated drift per bar. Default is 0.0. |

### **Backtest CLI Arguments**

| Parameter | Type | Description |
| --- | --- | --- |
| `--simulate-backtest` | Flag | Triggers the module to run in Backtest mode instead of Single-Run. |
| `--bt-tp-pips` | Float | **Required (Backtest).** The absolute price distance from entry to Take-Profit. |
| `--bt-sl-pips` | Float | **Required (Backtest).** The absolute price distance from entry to Stop-Loss. |
| `--bt-horizon` | Integer | Overrides the `--horizon` argument specifically during backtesting. |
| `--bt-step` | Integer | The number of historical bars to skip between tested decision points. Default is 5. |
| `--bt-windows` | Integer | The total number of historical decision points to simulate. Default is 40. |
| `--bt-paths` | Integer | Overrides `--paths` for backtesting to optimize speed. Default is 5000. |
| `--bt-model` | String | Overrides `--model` for backtesting. |
| `--bt-no-json` | Flag | Prevents the script from writing a JSON file for every single backtest step. |

---

## **5. Critical Analysis**

### **Strengths**

* **Statistical Rigor:** Moving beyond simple GBM to include GARCH and Bootstrap provides a highly professional toolkit. Asset returns are rarely normally distributed, and models like Bootstrap and GARCH capture the "fat tails" and volatility clustering inherent in financial markets.
* **Separation of Concerns:** The structure relies nicely on externalized utilities (`utils.load_ohlcv`, `utils.barrier_stats`, etc.), keeping the main class relatively clean and focused purely on orchestrating the simulations.
* **Calibration Loop:** The backtest feature outputting a `calibration` metric (Predicted POP vs. Actual Win Rate) is excellent. It immediately tells the user if the model is overconfident or underconfident.

### **Weaknesses & Vulnerabilities**

* **Hardcoded ML Features:** In `__init__`, `self.ml_feat_cols` is hardcoded to `['atr_14', 'rsi_14', 'volume_change', 'return_MA_10']`. If a user passes a pre-trained ML model that was trained on a different feature set, the script will silently fail at the prediction step or throw a Pandas `KeyError`.
* **Naming Convention Friction:** The arguments `--bt-tp-pips` and `--bt-sl-pips` are technically misnomers. In traditional finance, a pip is a fractional unit (e.g., 0.0001 in FX). The code treats these as absolute price offsets (e.g., entering at $150 with a TP of $152 means `bt-tp-pips` is 2.0).
* **Performance Bottleneck:** The backtest loop (`simulate_backtest_trades`) runs sequentially. Simulating 40 windows with 5,000 paths using computationally heavy models like GARCH or ARIMA-GARCH on a single core will be exceptionally slow.
* **Error Masking in ML Training:** If the on-the-fly LightGBM training fails, the script catches the broad `Exception` and silently falls back to standard GBM. The user might think they are running advanced ML paths when they are actually getting basic GBM.

---

## **6. Suggestions for Improvement**

1. **Implement Multiprocessing for Backtesting:**
The `simulate_backtest_trades` method is an embarrassingly parallel problem. Refactor the loop to use Python's `concurrent.futures.ProcessPoolExecutor`. This will reduce a 20-minute backtest to just a few minutes on modern multicore CPUs.
2. **Dynamic ML Feature Mapping:**
Instead of hardcoding `ml_feat_cols`, extract the expected features directly from the loaded LightGBM model. LightGBM models store their feature names (`self.lgb_model.feature_name_`). You can dynamically ensure the current DataFrame has exactly what the model needs.
3. **Rename "Pips" to "Distance":**
Change `--bt-tp-pips` to `--bt-tp-dist` or `--bt-tp-offset`. This prevents confusion for users transitioning from FX to equities or crypto, clarifying that the script expects a raw float price difference.
4. **Strict Error Handling for Model Fallbacks:**
Instead of a silent fallback when ML or GARCH fails, enforce a strict mode or at least surface a prominent CLI warning. If a user explicitly requested `--model ml_gbm`, automatically defaulting to `gbm` without breaking execution might corrupt their assumed statistical baseline.
