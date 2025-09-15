"""
Utility functions for computing barrier option statistics.

"""
import numpy as np

def barrier_stats(paths: np.ndarray, tp: float, sl: float) -> dict:
        """Compute trade outcome statistics from simulated paths.
        Parameters
        ----------
        paths: np.ndarray
            The simulated price paths.
        tp: float
            The take-profit level.
        sl: float
            The stop-loss level.
        Returns
        -------
        dict
            A dictionary containing the trade outcome statistics.
        """
        n, T = paths.shape
        T -= 1
        hit_tp = np.zeros(n, dtype=bool)
        hit_sl = np.zeros(n, dtype=bool)
        t_tp = np.full(n, T, dtype=int)
        t_sl = np.full(n, T, dtype=int)

        for i in range(n):
            p = paths[i,1:]
            above = np.where(p >= tp)[0]
            below = np.where(p <= sl)[0]
            if above.size:
                hit_tp[i] = True; t_tp[i] = int(above[0])
            if below.size:
                hit_sl[i] = True; t_sl[i] = int(below[0])
            if hit_tp[i] and hit_sl[i]:
                # first passage priority
                if t_sl[i] < t_tp[i]:
                    hit_tp[i] = False
                else:
                    hit_sl[i] = False
        pop = float(hit_tp.mean())
        psl = float(hit_sl.mean())
        pneither = float(1 - pop - psl)
        last = paths[:,-1]
        S0 = paths[:,0]
        R = np.where(hit_tp, 1.0, np.where(hit_sl, -1.0, (last - S0) / (S0 - sl)))
        out = {
            "pop_tp_first": pop,
            "p_sl_first": psl,
            "p_neither": pneither,
            "t_hit_tp_median": int(np.median(t_tp[hit_tp])) if pop>0 else None,
            "t_hit_sl_median": int(np.median(t_sl[hit_sl])) if psl>0 else None,
            "R_mean": float(np.mean(R)),
            "R_p50": float(np.median(R)),
            "R_p05": float(np.percentile(R,5)),
            "R_p95": float(np.percentile(R,95)),
        }
        return out
