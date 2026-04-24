# rtb/metrics.py
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

import numpy as np
import pandas as pd


# =========================
# Config / dataclasses
# =========================
@dataclass
class Thresholds:
    uph_low: float = 125.0
    uph_high: float = 300.0


# =========================
# Internal helpers
# =========================
def _uc_map(cols: Iterable[str]) -> dict:
    """
    Build a case-insensitive column lookup map. Keeps the original name as value.
    """
    m = {}
    for c in cols:
        m[c.strip().upper()] = c
    return m


def _find_col(colmap: dict, candidates: Iterable[str]) -> Optional[str]:
    """
    Return the first existing column from `candidates` using case-insensitive lookup.
    Candidate strings are matched by their UPPER() form.
    """
    for cand in candidates:
        k = cand.strip().upper()
        if k in colmap:
            return colmap[k]
    return None


def _to_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _normalize_level(val) -> Optional[int]:
    """
    Normalize 'LC' values like 'LC5', 'Level 5', '5' -> 5 (int).
    Returns None if not parseable.
    """
    if pd.isna(val):
        return None
    s = str(val).strip().upper()
    m = re.search(r'([1-5])', s)
    return int(m.group(1)) if m else None


# =========================
# Public API
# =========================
def clean(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize input DataFrame into a consistent schema used by the app.
    Supports two common inputs:

    A) Legacy dated schema:
       expects columns like: 'date','login','level','hours','units' (case-insensitive)
       - Ensures uph and shift_id

    B) RTB export schema:
       expects at least:
       'Process Name','Function Name','Employee Id','Paid Hours-Total(function,employee)'
       - Derives UPH if missing (needs 'Units')
       - Creates shift_id per (Employee Id, Function Name)
       - Adds 'date' if missing (today normalized)
       - Adds 'level' from 'LC' when present

    Returns a DataFrame with as many of these standardized columns as possible:
       ['date','login','level','hours','units','uph','shift_id', ...original columns...]
    """
    if raw is None or len(raw) == 0:
        return pd.DataFrame()

    df = raw.copy()
    uc = _uc_map(df.columns)

    # -------------------------
    # Try Legacy dated schema
    # -------------------------
    date_col  = _find_col(uc, ["date"])
    login_col = _find_col(uc, ["login", "employee id", "employee_id", "employeeid"])
    level_col = _find_col(uc, ["level", "lc"])
    hours_col = _find_col(uc, ["hours", "paid hours-total(function,employee)"])
    units_col = _find_col(uc, ["units"])
    uph_col   = _find_col(uc, ["uph"])

    legacy_has_min = all([
        date_col is not None,
        login_col is not None,
        hours_col is not None,
    ])

    # If already a legacy-like schema, standardize it
    if legacy_has_min and units_col is not None:
        # Standard rename
        ren = {}
        if date_col:  ren[date_col] = "date"
        if login_col: ren[login_col] = "login"
        if level_col: ren[level_col] = "level"
        if hours_col: ren[hours_col] = "hours"
        if units_col: ren[units_col] = "units"
        if uph_col:   ren[uph_col]   = "uph"
        df = df.rename(columns=ren)

        # Types
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["hours"] = _to_num(df["hours"]).fillna(0.0)
        df["units"] = _to_num(df["units"]).fillna(0.0)

        # Compute UPH if missing
        if "uph" not in df.columns:
            denom = df["hours"].replace(0, np.nan)
            df["uph"] = df["units"] / denom

        # Normalize level -> int
        if "level" in df.columns:
            df["level"] = df["level"].apply(_normalize_level)

        # Filter out obviously invalid rows
        df = df[(df["hours"] > 0) & df["units"].notna()].copy()

        # Ensure shift_id (per-login chronological index)
        if "shift_id" not in df.columns:
            df = df.sort_values(["login", "date"], kind="mergesort")
            df["shift_id"] = df.groupby("login").cumcount() + 1

        return df

    # -------------------------
    # RTB export schema
    # -------------------------
    proc_col   = _find_col(uc, ["process name"])
    func_col   = _find_col(uc, ["function name"])
    empid_col  = _find_col(uc, ["employee id", "employee_id", "employeeid", "login"])
    name_col   = _find_col(uc, ["name"])
    mgr_col    = _find_col(uc, ["manager"])
    lc_col     = _find_col(uc, ["lc", "level"])
    # Hours columns (total + components)
    pht_col    = _find_col(uc, ["paid hours-total(function,employee)"])
    phs_col    = _find_col(uc, ["paid hours-small(function,employee)"])
    phm_col    = _find_col(uc, ["paid hours-medium(function,employee)"])
    phl_col    = _find_col(uc, ["paid hours-large(function,employee)"])
    phh_col    = _find_col(uc, ["paid hours-heavybulky(function,employee)"])
    units_col  = _find_col(uc, ["units"])
    uph_col    = _find_col(uc, ["uph"])
    jph_col    = _find_col(uc, ["jph"])
    shift_col  = _find_col(uc, ["shift"])
    # Sometimes a date/time column exists under various headers
    date_col   = date_col or _find_col(uc, ["timestamp", "date time", "datetime", "scan date", "day"])

    needed_min = all([func_col is not None, empid_col is not None, pht_col is not None])
    if not needed_min:
        # Unrecognized schema; return as-is (the app has a second-stage cleaner that may handle it)
        return df

    # Standardized baseline names we want downstream (keep originals too)
    std_cols = {}
    if proc_col: std_cols[proc_col] = "process_name"
    if func_col: std_cols[func_col] = "function_name"
    if empid_col: std_cols[empid_col] = "employee_id"
    if name_col: std_cols[name_col] = "name"
    if mgr_col: std_cols[mgr_col] = "manager"
    if lc_col: std_cols[lc_col] = "lc_raw"

    std_cols[pht_col] = "paid_hours_total"
    if phs_col: std_cols[phs_col] = "paid_hours_small"
    if phm_col: std_cols[phm_col] = "paid_hours_medium"
    if phl_col: std_cols[phl_col] = "paid_hours_large"
    if phh_col: std_cols[phh_col] = "paid_hours_heavybulky"

    if units_col: std_cols[units_col] = "units"
    if uph_col:   std_cols[uph_col]   = "UPH"   # keep uppercase then mirror to 'uph'
    if jph_col:   std_cols[jph_col]   = "JPH"
    if shift_col: std_cols[shift_col] = "shift"
    if date_col:  std_cols[date_col]  = "date"

    df = df.rename(columns=std_cols)

    # Numeric coercions
    num_candidates = [
        "paid_hours_total", "paid_hours_small", "paid_hours_medium",
        "paid_hours_large", "paid_hours_heavybulky", "units", "UPH", "JPH"
    ]
    for c in num_candidates:
        if c in df.columns:
            df[c] = _to_num(df[c])

    # Derive UPH if missing but units present
    if "UPH" not in df.columns and "units" in df.columns and "paid_hours_total" in df.columns:
        denom = df["paid_hours_total"].replace(0, np.nan)
        df["UPH"] = df["units"] / denom

    # Back-compat lowercase 'uph'
    if "UPH" in df.columns and "uph" not in df.columns:
        df["uph"] = df["UPH"]

    # Derive 'hours' alias expected by some legacy panels
    if "hours" not in df.columns and "paid_hours_total" in df.columns:
        df["hours"] = df["paid_hours_total"]

    # Create 'login' alias expected by legacy panels
    if "login" not in df.columns and "employee_id" in df.columns:
        df["login"] = df["employee_id"].astype(str)

    # Create/normalize date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    else:
        df["date"] = pd.Timestamp.today().normalize()

    # Normalize 'level' from LC if available
    if "lc_raw" in df.columns:
        df["level"] = df["lc_raw"].apply(_normalize_level)

    # Compute shift_id if not present: per (employee_id, function_name) progression
    if "shift_id" not in df.columns:
        by = ["employee_id"]
        if "function_name" in df.columns:
            by.append("function_name")
        df = df.sort_values(by + ["date"], kind="mergesort")
        df["shift_id"] = df.groupby(by).cumcount() + 1

    # Remove rows with clearly invalid numerics (but keep hours-only rows if units absent)
    if "hours" in df.columns:
        df = df[df["hours"].notna()]
    if "units" in df.columns:
        df = df[df["units"].notna()]

    # Clip absurd negatives
    for c in ["hours", "units", "UPH", "uph"]:
        if c in df.columns:
            df.loc[df[c] < 0, c] = np.nan

    return df


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate to daily totals: units, hours, and weighted UPH = units / hours.
    Expects 'date', 'units', 'hours' columns (created by clean()).
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "units", "hours", "uph"])

    needed = {"date", "hours"}
    if not needed.issubset(df.columns):
        # Try to alias: paid_hours_total -> hours
        work = df.copy()
        if "hours" not in work.columns and "paid_hours_total" in work.columns:
            work["hours"] = work["paid_hours_total"]
        else:
            work["hours"] = pd.NA
    else:
        work = df.copy()

    if "units" not in work.columns:
        # Hours-only fallback
        out = (work.groupby("date", as_index=False)
                     .agg(hours=("hours", "sum")))
        out["units"] = np.nan
        out["uph"] = np.nan
        return out[["date", "units", "hours", "uph"]]

    out = (work.groupby("date", as_index=False)
                 .agg(units=("units", "sum"),
                      hours=("hours", "sum")))
    out["uph"] = out["units"] / out["hours"].replace(0, np.nan)
    return out[["date", "units", "hours", "uph"]]


def ewma(series: pd.Series, span: int = 5) -> pd.Series:
    """Exponentially weighted moving average."""
    return series.ewm(span=span, adjust=False).mean()


def percentile_band(series: pd.Series, low: float = 0.1, high: float = 0.9) -> Tuple[float, float]:
    """Return (low_percentile, high_percentile) for a numeric series."""
    s = pd.to_numeric(series, errors="coerce")
    return float(s.quantile(low)), float(s.quantile(high))
