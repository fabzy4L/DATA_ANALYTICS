from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass

MIN_HOURS = 0.25

@dataclass
class Thresholds:
    uph_low: float = 125.0     # Example target threshold
    uph_high: float = 300.0    # Example high-performer threshold
    min_sessions: int = 3
    ewma_span: int = 5

def clean(df: pd.DataFrame) -> pd.DataFrame:
    req_cols = ["date", "login", "level", "hours", "units"]
    for col in req_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"])
    out["hours"] = pd.to_numeric(out["hours"], errors="coerce").fillna(0.0)
    out["units"] = pd.to_numeric(out["units"], errors="coerce").fillna(0.0)
    out = out[out["hours"] >= MIN_HOURS]
    out["uph"] = out["units"] / out["hours"]
    if "shift_id" not in out.columns:
        # Create a session index per login by date order
        out = out.sort_values(["login", "date"]).copy()
        out["shift_id"] = out.groupby("login").cumcount() + 1
    return out

def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    grp = (
        df.groupby(["date", "login", "level"], as_index=False)
          .agg(hours=("hours", "sum"),
               units=("units", "sum"))
    )
    grp["uph"] = grp["units"] / grp["hours"].replace(0, np.nan)
    return grp

def ewma(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def sigma_clip(series: pd.Series, sigma: float = 3.0) -> pd.Series:
    m = series.mean()
    s = series.std(ddof=0)
    lower = m - sigma * s
    upper = m + sigma * s
    return series.clip(lower, upper)

def percentile_band(series: pd.Series, lo: float = 0.05, hi: float = 0.95) -> tuple[float, float]:
    return np.nanpercentile(series.dropna(), [lo * 100, hi * 100])
