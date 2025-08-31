from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from .metrics import Thresholds

@dataclass
class CommentConfig:
    thresholds: Thresholds

def trend_slope(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size < 2:
        return np.nan
    A = np.vstack([np.ones_like(x), x]).T
    c, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
    return float(c[1])  # slope

def build_comments(df: pd.DataFrame, cfg: CommentConfig) -> pd.DataFrame:
    # df expected columns: date, login, level, hours, units, uph, shift_id
    out = []
    for login, g in df.sort_values(["login", "date"]).groupby("login"):
        g = g.reset_index(drop=True)
        avg_uph = float(g["uph"].mean())
        p10 = float(g["uph"].quantile(0.10))
        p90 = float(g["uph"].quantile(0.90))
        slope = trend_slope(np.arange(len(g)), g["uph"].values)
        flags = []
        if avg_uph < cfg.thresholds.uph_low:
            flags.append(f"avg UPH {avg_uph:.1f} below target {cfg.thresholds.uph_low:.0f}")
        if g["uph"].iloc[-1] < cfg.thresholds.uph_low:
            flags.append(f"latest UPH {g['uph'].iloc[-1]:.1f} below target")
        if slope > 0.0:
            flags.append(f"improving trend (slope {slope:.2f} UPH/shift)")
        elif slope < 0.0:
            flags.append(f"declining trend (slope {slope:.2f} UPH/shift)")
        if p90 > cfg.thresholds.uph_high:
            flags.append(f"top decile spike {p90:.1f}+")
        comment = "; ".join(flags) if flags else "steady performance within band"
        out.append({
            "login": login,
            "sessions": len(g),
            "avg_uph": avg_uph,
            "p10_uph": p10,
            "p90_uph": p90,
            "trend_slope": slope,
            "comment": comment
        })
    return pd.DataFrame(out).sort_values(["avg_uph", "trend_slope"], ascending=[True, False])
