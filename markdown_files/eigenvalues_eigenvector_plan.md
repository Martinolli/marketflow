# Eigenvectors - Eigenvalues Proposal

The key is this: **do not apply eigenvalues/eigenvectors directly to raw price and raw volume.** That would mostly measure scale and trend. Instead, apply them to **normalized price-result and volume-effort features** inside a rolling window.

In Wyckoff/VPA language, this maps beautifully:

> **Volume = effort**
> **Price movement / spread = result**

That is exactly the Wyckoff “Effort vs Result” idea: volume and price should show harmony; divergences between them may warn of weakness, absorption, or possible trend change. StockCharts and Wyckoff Analytics both describe this effort/result relationship and its use in identifying price-volume divergence. ([chartschool.stockcharts.com][7])

---

## 1. Quick eigenvalue/eigenvector review

At the heart of it:

A\vec{v}=\lambda\vec{v}

Meaning:

**Eigenvector** = a direction that keeps its direction after transformation.
**Eigenvalue** = how strongly that direction is stretched or compressed.

For market data, the matrix `A` would usually be a **covariance matrix** of your features. PCA uses this idea: the principal components are directions of maximum variance, and the explained variance tells how much movement each component captures. Scikit-learn’s PCA documentation describes the components as principal axes in feature space, sorted by decreasing explained variance. ([Scikit-Learn][8])

In your case, with only two main variables:

```text
price/result
volume/effort
```

the eigenvectors tell you the **dominant direction of joint movement** between price and volume.

---

## 2. The important interpretation

With two normalized features:

```text
x₁ = normalized price result
x₂ = normalized volume effort
```

your covariance matrix becomes something like:

```text
Σ = covariance(price_result, volume_effort)
```

Then you compute eigenvalues/eigenvectors.

You will usually get:

```text
λ₁, e₁ = dominant market behavior
λ₂, e₂ = secondary / abnormal behavior
```

Interpretation:

| Eigen output                            | MarketFlow meaning                                    |
| --------------------------------------- | ----------------------------------------------------- |
| Large `λ₁`                              | Price-volume behavior has a strong dominant pattern   |
| Small `λ₂`                              | Most bars follow the normal relationship              |
| Large `λ₂`                              | More disorder, instability, abnormal behavior         |
| `e₁` price and volume same direction    | Harmony: effort and result agree                      |
| Current bar projects strongly onto `e₂` | Possible divergence / abnormal effort-result behavior |

The sneaky part: with only price and volume, this is basically **correlation geometry wearing a nice mathematical jacket**. Still useful — but not magic.

---

## 3. What you should not use

Avoid this:

```python
X = df[["close", "volume"]]
```

Raw close and raw volume are bad inputs because:

```text
price may trend upward over time
volume has huge scale differences
stock splits and liquidity changes distort the relation
```

Instead, use transformed features.

Better:

```python
price_result = close.pct_change()
volume_effort = log(volume / rolling_average_volume)
```

Even better for Wyckoff/VPA:

```python
price_result = bar_spread / ATR
volume_effort = volume / average_volume
```

or:

```python
price_result = abs(close - open) / ATR
volume_effort = volume_zscore
```

Since your MarketFlow already works with fields like `close`, `spread`, `volume`, `volume_ratio`, `candle_class`, `volume_class`, and Wyckoff phase/event tags, this would fit naturally as an additional analyzer before final signal generation.

---

## 4. Best practical model for MarketFlow

I would create a new feature set like this:

```text
result_t = normalized price movement
effort_t = normalized volume
```

Example:

```python
result_t = spread / ATR
effort_t = volume / rolling_volume_mean
```

Then standardize both using a rolling z-score:

```text
z_result_t
z_effort_t
```

Now build rolling windows:

```text
window = last 30, 40, or 60 bars
```

For each rolling window, compute:

```text
covariance matrix
eigenvalues
eigenvectors
projection of current bar
residual divergence score
```

---

## 5. The divergence signal

A strong divergence signal could be:

```text
high volume effort
low price result
high orthogonal PCA residual
near Wyckoff support/resistance
confirmed by phase/event context
```

In plain words:

> “The market is spending a lot of volume energy, but price is not moving accordingly.”

That is very Wyckoff.

Example bearish context:

```text
High volume
Small upward spread
Near resistance
After markup
Eigen residual high
```

Possible interpretation:

```text
Supply appearing / absorption / distribution risk
```

Example bullish context:

```text
High volume
Small downward spread
Near support
During accumulation
Eigen residual high
Spring/test behavior nearby
```

Possible interpretation:

```text
Selling pressure absorbed / accumulation
```

Same mathematical signal. Different interpretation depending on Wyckoff context. This is critical.

---

## 6. Suggested MarketFlow feature names

You could add fields like:

```text
pv_eigen_lambda1
pv_eigen_lambda2
pv_eigen_coupling
pv_eigen_residual
pv_eigen_harmony
pv_effort_result_divergence
pv_divergence_type
```

Possible meanings:

```text
pv_eigen_coupling = λ₁ / (λ₁ + λ₂)
```

High value means price-volume behavior is organized.

```text
pv_eigen_residual = abnormal distance from normal price-volume relation
```

High value means divergence/anomaly.

```text
pv_eigen_harmony = +1 or -1
```

`+1` means price/result and volume/effort are broadly aligned.
`-1` means they are moving against each other.

---

## 7. Simple Python prototype

This is a good first implementation:

```python
import numpy as np
import pandas as pd


def rolling_zscore(series: pd.Series, window: int) -> pd.Series:
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std.replace(0, np.nan)


def add_price_volume_eigen_features(
    df: pd.DataFrame,
    window: int = 40,
    price_col: str = "close",
    volume_col: str = "volume",
    spread_col: str | None = "spread",
    atr_col: str | None = "atr",
) -> pd.DataFrame:
    """
    Adds rolling eigen/PCA-style price-volume divergence features.

    Expected columns:
    - close
    - volume
    Optional:
    - spread
    - atr
    """

    out = df.copy()

    # 1. Build price/result feature
    if spread_col in out.columns and atr_col in out.columns:
        result = out[spread_col] / out[atr_col].replace(0, np.nan)
    else:
        result = out[price_col].pct_change()

    # 2. Build volume/effort feature
    volume_ma = out[volume_col].rolling(window).mean()
    effort = out[volume_col] / volume_ma.replace(0, np.nan)

    # 3. Normalize
    out["pv_result_z"] = rolling_zscore(result, window)
    out["pv_effort_z"] = rolling_zscore(effort, window)

    # Output containers
    out["pv_eigen_lambda1"] = np.nan
    out["pv_eigen_lambda2"] = np.nan
    out["pv_eigen_coupling"] = np.nan
    out["pv_eigen_residual"] = np.nan
    out["pv_eigen_harmony"] = np.nan
    out["pv_effort_result_divergence"] = False

    features = out[["pv_result_z", "pv_effort_z"]].to_numpy()

    eps = 1e-9

    for i in range(window, len(out)):
        X = features[i - window + 1 : i + 1]

        if np.isnan(X).any():
            continue

        # Covariance matrix of result and effort
        cov = np.cov(X.T)

        # Eigen decomposition
        values, vectors = np.linalg.eigh(cov)

        # Sort from largest eigenvalue to smallest
        order = np.argsort(values)[::-1]
        values = values[order]
        vectors = vectors[:, order]

        lambda1, lambda2 = values
        e1 = vectors[:, 0]
        e2 = vectors[:, 1]

        # Normalize sign convention:
        # force price/result loading to be positive
        if e1[0] < 0:
            e1 = -e1

        current_x = X[-1]

        # Projection onto minor component = abnormal/difference axis
        residual = abs(np.dot(current_x, e2)) / np.sqrt(lambda2 + eps)

        coupling = lambda1 / (lambda1 + lambda2 + eps)

        harmony = np.sign(e1[0] * e1[1])

        # Simple divergence rule:
        # high residual + strong coupling + high effort but weak result
        effort_high = current_x[1] > 1.0
        result_weak = abs(current_x[0]) < 0.5
        residual_high = residual > 2.0
        coupling_good = coupling > 0.65

        divergence = effort_high and result_weak and residual_high and coupling_good

        out.iloc[i, out.columns.get_loc("pv_eigen_lambda1")] = lambda1
        out.iloc[i, out.columns.get_loc("pv_eigen_lambda2")] = lambda2
        out.iloc[i, out.columns.get_loc("pv_eigen_coupling")] = coupling
        out.iloc[i, out.columns.get_loc("pv_eigen_residual")] = residual
        out.iloc[i, out.columns.get_loc("pv_eigen_harmony")] = harmony
        out.iloc[i, out.columns.get_loc("pv_effort_result_divergence")] = divergence

    return out
```

---

## 8. How I would use it in your signal engine

Not like this:

```text
Eigen divergence = BUY
```

That would be too crude.

Better:

```text
Eigen divergence detected
+ Wyckoff phase = Accumulation
+ near support
+ Spring/Test event nearby
= bullish confirmation
```

or:

```text
Eigen divergence detected
+ Wyckoff phase = Distribution
+ near resistance
+ Upthrust / weak result after high effort
= bearish warning
```

So the eigen feature becomes a **confirmation layer**, not the main decision-maker.

---

## 9. My honest opinion

This is valid and worth testing.

But I would phrase it as:

> “Eigen/PCA analysis can quantify price-volume harmony and abnormal effort-result behavior inside a rolling window.”

I would not phrase it as:

> “Eigenvalues predict market direction.”

That would be too strong.

The value is in detecting when the normal relationship between price and volume is being broken. That is very aligned with Wyckoff thinking.

For MarketFlow, I would add this as a module named something like:

```text
price_volume_eigen_analyzer.py
```

and have it produce features that your Wyckoff/VPA scoring system can consume.

A good scoring rule could be:

```text
base_vpa_score
+ eigen_divergence_confirmation
+ wyckoff_phase_context
+ support_resistance_context
= final composite signal
```

That keeps the system orthodox, interpretable, and mathematically stronger.

Exactly, João — that is the right way to position it.

I would make it a **standalone analytical module**, not part of the core Wyckoff decision engine at first.

Something like:

```text
marketflow/
│
├── analyzers/
│   ├── vpa_analyzer.py
│   ├── wyckoff_analyzer.py
│   ├── support_resistance.py
│   └── price_volume_eigen_analyzer.py
```

The purpose of the module could be stated as:

> The Price-Volume Eigen Analyzer measures the harmony or abnormal divergence between price movement and volume activity over a rolling window, using PCA/eigenvalue decomposition.

That sounds technically correct and avoids overclaiming.

The module should output **information**, not decisions.

For example:

```python
{
    "pv_eigen_coupling": 0.82,
    "pv_eigen_residual": 2.41,
    "pv_eigen_harmony": 1,
    "pv_effort_result_divergence": True,
    "pv_divergence_bias": "context_required"
}
```

The last field is important: without Wyckoff context, the module should not say bullish or bearish.

A cleaner interpretation layer would be:

```text
Eigen/PCA module says:
“There is abnormal effort-result behavior.”

Wyckoff/VPA module says:
“This is happening near support, during accumulation.”

Final MarketFlow interpretation:
“Possible bullish absorption.”
```

or:

```text
Eigen/PCA module says:
“There is abnormal effort-result behavior.”

Wyckoff/VPA module says:
“This is happening near resistance, during distribution.”

Final MarketFlow interpretation:
“Possible bearish supply pressure.”
```

So I would design it in three levels:

```text
Level 1: Raw mathematical features
Level 2: Price-volume abnormality detection
Level 3: Interpretation using Wyckoff/VPA context
```

For now, I would start with only **Level 1 and Level 2** inside the eigen module.

Suggested class name:

```python
class PriceVolumeEigenAnalyzer:
    """
    Quantifies price-volume harmony and abnormal effort-result behavior
    using rolling PCA/eigenvalue analysis.
    """
```

Suggested output columns:

```python
[
    "pv_result_z",
    "pv_effort_z",
    "pv_eigen_lambda1",
    "pv_eigen_lambda2",
    "pv_eigen_coupling",
    "pv_eigen_residual",
    "pv_eigen_harmony",
    "pv_effort_result_divergence"
]
```

My recommendation: first implement it as a **feature generator**, then later connect it to your signal scoring engine.

Something like:

```python
df = PriceVolumeEigenAnalyzer(window=40).transform(df)
```

Then the rest of MarketFlow can use:

```python
if row["pv_effort_result_divergence"]:
    # Ask Wyckoff/VPA context what this probably means
```

That keeps the architecture clean. The math module detects **abnormality**. The Wyckoff/VPA layer interprets **meaning**.

---

[7]: https://school.stockcharts.com/doku.php?id=chart_school:technical_indicators:volume
[8]: https://scikit-learn.org/stable/modules/decomposition.html#pca
