"""
Create features for volatility prediction.

"""
import numpy as np
import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create features for volatility prediction.
        Parameters
        ----------
        df: pd.DataFrame
            The input OHLCV DataFrame.
        Returns
        -------
            pd.DataFrame
        """
        df_feat = df.copy()
        df_feat['log_return'] = np.log(df_feat['close']).diff()

        # Target variable: Realized volatility over the next 5 bars
        df_feat['target_vol'] = df_feat['log_return'].rolling(5).std(ddof=1).shift(-5)

        # ATR(14)
        high = df_feat['high']; low = df_feat['low']; close = df_feat['close']
        prev_close = close.shift(1)
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df_feat['atr_14'] = tr.rolling(14).mean()

        # RSI(14)
        delta = df_feat['log_return']
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rs = rs.replace([np.inf, -np.inf], np.nan)  # avoid inf when loss ~ 0
        df_feat['rsi_14'] = 100 - (100 / (1 + rs))

        # Other features
        df_feat['volume_change'] = df_feat['volume'].pct_change()
        df_feat['return_MA_10'] = df_feat['log_return'].rolling(10).mean()

        # Final cleanup
        df_feat = df_feat.replace([np.inf, -np.inf], np.nan).dropna()
        return df_feat
