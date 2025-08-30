from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional

@dataclass
class PowerLawFit:
    a: float
    b: float
    r2: float
    n: int

def fit_power_law(x: np.ndarray, y: np.ndarray) -> Optional[PowerLawFit]:
    # y = a * x^b  => log(y) = log(a) + b*log(x)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size < 3:
        return None
    lx = np.log(x)
    ly = np.log(y)
    # linear regression
    A = np.vstack([np.ones_like(lx), lx]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(A, ly, rcond=None)
    c0, b = coeffs  # ly = c0 + b*lx
    a = np.exp(c0)
    y_pred = a * (x ** b)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return PowerLawFit(a=a, b=b, r2=r2, n=x.size)

def per_login_learning_curve(df: pd.DataFrame) -> pd.DataFrame:
    # expects columns: login, shift_id (1..N), uph
    rows = []
    for login, g in df.sort_values(["login", "shift_id"]).groupby("login"):
        fit = fit_power_law(g["shift_id"].values, g["uph"].values)
        if fit is None:
            rows.append({"login": login, "a": np.nan, "b": np.nan, "r2": np.nan, "n": len(g)})
        else:
            rows.append({"login": login, "a": fit.a, "b": fit.b, "r2": fit.r2, "n": fit.n})
    return pd.DataFrame(rows)

def predict_uph(a: float, b: float, shift_index: float) -> float:
    return float(a * (shift_index ** b)) if (a > 0 and shift_index > 0) else np.nan
