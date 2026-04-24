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
    """
    Flexible cleaner:
    - Legacy schema with date/login/level/hours/units -> as before (computes 'uph')
    - RTB schema w/ Process/Function/Employee/Hours (+ optional Units/UPH/JPH)
    """
    # ---- Path A: legacy schema (unchanged) ----
    legacy = {"date","login","level","hours","units"}
    if legacy.issubset(df.columns):
        out = df.copy()
        out["date"] = pd.to_datetime(out["date"])
        out["hours"] = pd.to_numeric(out["hours"], errors="coerce").fillna(0.0)
        out["units"] = pd.to_numeric(out["units"], errors="coerce").fillna(0.0)
        out = out[out["hours"] >= MIN_HOURS]
        out["uph"] = out["units"] / out["hours"]
        if "shift_id" not in out.columns:
            out = out.sort_values(["login","date"]).copy()
            out["shift_id"] = out.groupby("login").cumcount() + 1
        return out

    # ---- Path B: RTB CSV like your screenshot ----
    base_needed = {"Process Name","Function Name","Employee Id","Paid Hours-Total(function,employee)"}
    if base_needed.issubset(df.columns):
        out = df.copy()

        # Normalize numerics we rely on
        for col in ["Paid Hours-Total(function,employee)",
                    "Paid Hours-Small(function,employee)",
                    "Paid Hours-Medium(function,employee)",
                    "Paid Hours-Large(function,employee)",
                    "Paid Hours-HeavyBulky(function,employee)",
                    "Units","UPH","JPH"]:
            if col in out.columns:
                out[col] = pd.to_numeric(out[col], errors="coerce")

        # If UPH missing but Units present -> derive UPH
        if "UPH" not in out.columns and "Units" in out.columns:
            ph = out["Paid Hours-Total(function,employee)"].replace(0, np.nan)
            out["UPH"] = out["Units"] / ph

        # If JPH missing and you have a "Jobs" column, derive JPH (optional)
        if "JPH" not in out.columns and "Jobs" in out.columns:
            ph = out["Paid Hours-Total(function,employee)"].replace(0, np.nan)
            out["JPH"] = out["Jobs"] / ph

        # Stable session index per employee inside a function (for ordering)
        if "shift_id" not in out.columns:
            out["shift_id"] = out.groupby(["Employee Id","Function Name"]).cumcount() + 1

        return out

    raise ValueError(
        "Unrecognized schema. Provide either legacy columns "
        "['date','login','level','hours','units'] or RTB columns with at least "
        "['Process Name','Function Name','Employee Id','Paid Hours-Total(function,employee)'] "
        "and optionally 'Units' to derive UPH."
    )
id Hours-Total(function,employee)']."
    )


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
