"""Price-volume eigen/PCA-style feature generation."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


EIGEN_FEATURE_COLUMNS = [
    "pv_result_z",
    "pv_effort_z",
    "pv_eigen_lambda1",
    "pv_eigen_lambda2",
    "pv_eigen_coupling",
    "pv_eigen_residual",
    "pv_eigen_harmony",
    "pv_effort_result_divergence",
    "pv_divergence_strength",
    "pv_eigen_status",
    "pv_eigen_vector1_result",
    "pv_eigen_vector1_effort",
    "pv_eigen_vector2_result",
    "pv_eigen_vector2_effort",
    "pv_result_raw",
    "pv_effort_raw",
]


class PriceVolumeEigenAnalyzer:
    """
    Quantifies price-volume harmony and abnormal effort-result behavior
    using rolling PCA/eigenvalue analysis.

    This analyzer generates features only. It does not produce trade signals.
    """

    def __init__(
        self,
        window: int = 40,
        result_mode: str = "spread_atr",
        effort_mode: str = "volume_ratio",
        residual_threshold: float = 2.0,
        coupling_threshold: float = 0.65,
        high_effort_z: float = 1.0,
        weak_result_z: float = 0.5,
    ):
        self.window = max(int(window), 5)
        self.result_mode = str(result_mode or "spread_atr")
        self.effort_mode = str(effort_mode or "volume_ratio")
        self.residual_threshold = float(residual_threshold)
        self.coupling_threshold = float(coupling_threshold)
        self.high_effort_z = float(high_effort_z)
        self.weak_result_z = float(weak_result_z)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a copy of df with rolling price-volume eigen features."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")

        out = df.copy()
        self._validate_base_columns(out)

        result_raw = self._result_feature(out)
        effort_raw = self._effort_feature(out)
        out["pv_result_raw"] = result_raw
        out["pv_effort_raw"] = effort_raw
        out["pv_result_z"] = self._rolling_zscore(result_raw)
        out["pv_effort_z"] = self._rolling_zscore(effort_raw)

        for column in (
            "pv_eigen_lambda1",
            "pv_eigen_lambda2",
            "pv_eigen_coupling",
            "pv_eigen_residual",
            "pv_eigen_harmony",
            "pv_divergence_strength",
            "pv_eigen_vector1_result",
            "pv_eigen_vector1_effort",
            "pv_eigen_vector2_result",
            "pv_eigen_vector2_effort",
        ):
            out[column] = np.nan
        out["pv_effort_result_divergence"] = False
        out["pv_eigen_status"] = "insufficient_data"

        features = out[["pv_result_z", "pv_effort_z"]].to_numpy(dtype=float)
        eps = 1e-9

        for index in range(self.window - 1, len(out)):
            window_x = features[index - self.window + 1 : index + 1]
            if window_x.shape[0] < self.window:
                continue
            if not np.isfinite(window_x).all():
                out.iat[index, out.columns.get_loc("pv_eigen_status")] = "invalid_window"
                continue

            cov = np.cov(window_x.T)
            if not self._valid_covariance(cov):
                out.iat[index, out.columns.get_loc("pv_eigen_status")] = "invalid_window"
                continue

            try:
                values, vectors = np.linalg.eigh(cov)
            except np.linalg.LinAlgError:
                out.iat[index, out.columns.get_loc("pv_eigen_status")] = "invalid_window"
                continue

            if not np.isfinite(values).all() or not np.isfinite(vectors).all():
                out.iat[index, out.columns.get_loc("pv_eigen_status")] = "invalid_window"
                continue

            order = np.argsort(values)[::-1]
            values = values[order]
            vectors = vectors[:, order]
            lambda1 = max(float(values[0]), 0.0)
            lambda2 = max(float(values[1]), 0.0)
            if lambda1 + lambda2 <= eps:
                out.iat[index, out.columns.get_loc("pv_eigen_status")] = "invalid_window"
                continue

            e1 = vectors[:, 0].astype(float)
            e2 = vectors[:, 1].astype(float)
            if e1[0] < 0:
                e1 = -e1
                e2 = -e2

            current_x = window_x[-1]
            coupling = lambda1 / (lambda1 + lambda2 + eps)
            residual = abs(float(np.dot(current_x, e2))) / np.sqrt(lambda2 + eps)
            harmony = float(np.sign(e1[0] * e1[1]))

            effort_high = current_x[1] > self.high_effort_z
            result_weak = abs(current_x[0]) < self.weak_result_z
            residual_high = residual > self.residual_threshold
            coupling_good = coupling > self.coupling_threshold
            divergence = bool(effort_high and result_weak and residual_high and coupling_good)
            divergence_strength = residual * coupling if divergence else residual * 0.25

            self._set_row_values(
                out,
                index,
                {
                    "pv_eigen_lambda1": lambda1,
                    "pv_eigen_lambda2": lambda2,
                    "pv_eigen_coupling": coupling,
                    "pv_eigen_residual": residual,
                    "pv_eigen_harmony": harmony,
                    "pv_effort_result_divergence": divergence,
                    "pv_divergence_strength": divergence_strength,
                    "pv_eigen_status": "ok",
                    "pv_eigen_vector1_result": float(e1[0]),
                    "pv_eigen_vector1_effort": float(e1[1]),
                    "pv_eigen_vector2_result": float(e2[0]),
                    "pv_eigen_vector2_effort": float(e2[1]),
                },
            )

        return out

    def _validate_base_columns(self, df: pd.DataFrame) -> None:
        missing = [column for column in ("open", "high", "low", "close", "volume") if column not in df.columns]
        if missing:
            raise ValueError(f"DataFrame is missing required OHLCV columns: {', '.join(missing)}.")

    def _numeric(self, df: pd.DataFrame, column: str) -> pd.Series:
        return pd.to_numeric(df[column], errors="coerce")

    def _usable_column(self, df: pd.DataFrame, column: str) -> bool:
        return column in df.columns and self._numeric(df, column).notna().any()

    def _result_feature(self, df: pd.DataFrame) -> pd.Series:
        if self.result_mode == "close_return":
            return self._numeric(df, "close").pct_change()

        if self._usable_column(df, "spread") and self._usable_column(df, "atr14"):
            atr = self._numeric(df, "atr14").replace(0, np.nan)
            return self._numeric(df, "spread") / atr

        if self._usable_column(df, "tr"):
            true_range = self._numeric(df, "tr")
        else:
            high = self._numeric(df, "high")
            low = self._numeric(df, "low")
            true_range = high - low

        rolling_tr_mean = true_range.rolling(self.window, min_periods=max(5, self.window // 2)).mean()
        if rolling_tr_mean.notna().any():
            return true_range / rolling_tr_mean.replace(0, np.nan)

        return self._numeric(df, "close").pct_change()

    def _effort_feature(self, df: pd.DataFrame) -> pd.Series:
        if self.effort_mode == "volrel20" and self._usable_column(df, "volrel20"):
            return self._numeric(df, "volrel20")
        if self.effort_mode == "volume_ratio" and self._usable_column(df, "volume_ratio"):
            return self._numeric(df, "volume_ratio")
        if self.effort_mode == "volume_ratio" and self._usable_column(df, "volrel20"):
            return self._numeric(df, "volrel20")
        if self.effort_mode == "volrel20" and self._usable_column(df, "volume_ratio"):
            return self._numeric(df, "volume_ratio")

        volume = self._numeric(df, "volume")
        if self._usable_column(df, "volma20"):
            volume_mean = self._numeric(df, "volma20")
        else:
            volume_mean = volume.rolling(self.window, min_periods=max(5, self.window // 2)).mean()
        return volume / volume_mean.replace(0, np.nan)

    def _rolling_zscore(self, series: pd.Series) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce")
        mean = numeric.rolling(self.window, min_periods=self.window).mean()
        std = numeric.rolling(self.window, min_periods=self.window).std()
        return (numeric - mean) / std.replace(0, np.nan)

    @staticmethod
    def _valid_covariance(cov: Any) -> bool:
        return isinstance(cov, np.ndarray) and cov.shape == (2, 2) and np.isfinite(cov).all()

    @staticmethod
    def _set_row_values(df: pd.DataFrame, row_index: int, values: dict[str, Any]) -> None:
        for column, value in values.items():
            df.iat[row_index, df.columns.get_loc(column)] = value
