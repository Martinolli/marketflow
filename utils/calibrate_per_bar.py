"""
Utility functions for Monte Carlo trade simulation.

"""
import numpy as np
import pandas as pd

def calibrate_per_bar(closes: pd.Series, window: int = 400) -> tuple[float,float,np.ndarray]:
        """Return per-bar mu, sigma and recent log-returns (last `window`).
        Parameters
        ----------
        closes: pd.Series
            The closing prices for which to calibrate the model.
        window: int
            The number of most recent bars to consider for calibration.
        Returns
        -------
        tuple[float,float,np.ndarray]
        """
        r = np.log(closes).diff().dropna()
        if len(r) < 20:
            raise ValueError("Not enough bars to calibrate; need >= 20")
        r = r.tail(window)
        mu_bar = float(r.mean())
        sigma_bar = float(r.std(ddof=1))
        return mu_bar, sigma_bar, r.values