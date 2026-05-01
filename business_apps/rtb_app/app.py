# app.py — Integrated RTB Analysis (Directed Loader + Palletizer + Legacy)
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---- Helpers / models ----
from rtb.metrics import clean, aggregate, Thresholds, ewma, percentile_band
from rtb.models import per_login_learning_curve, predict_uph
from rtb.comments import build_comments, CommentConfig

st.set_page_config(page_title="RTB Analysis Dashboard", layout="wide")

st.title("RTB Analysis Dashboard")
st.caption("Upload CSVs, filter cohorts, visualize UPH & learning curves, auto-generate comments.")

# =========================
# Sidebar Controls
# =========================
with st.sidebar:
    st.header("Controls")
    # Use whatever defaults you prefer; these match your prior file
    uph_low = st.number_input("UPH target (low threshold)", min_value=0.0, value=12.0, step=1.0)
    uph_high = st.number_input("UPH high-performer threshold", min_value=0.0, value=19.0, step=1.0)
    uph_cap = st.number_input("UPH cap for plotting (clip)", min_value=0.0, value=19.0, step=1.0)
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

# =========================
# Load CSV
# =========================
if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

raw = pd.read_csv(uploaded)

# Clean and normalize with robust cleaner
df = clean(raw)

# Detect legacy (dated) schema from normalized df
has_date_schema = {"date","login","level","hours","units"}.issubset(df.columns)

# Compat: some legacy code expects lowercase 'uph'
if "UPH" in df.columns and "uph" not in df.columns:
    df["uph"] = pd.to_numeric(df["UPH"], errors="coerce")

# Preview raw upload
st.write("Uploaded DataFrame preview:")
st.dataframe(raw.head())

# =========================
# Shared helpers for grouped RTB panels
# =========================
def slope_xy(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return np.nan
    A = np.vstack([np.ones(m.sum()), x[m]]).T
    intercept, slope = np.linalg.lstsq(A, y[m], rcond=None)[0]
    return float(slope)

def render_grouped_panel(df_proc: pd.DataFrame, uph_low_default: float, uph_cap_clip: float,
                         process_label: str):
    """
    Grouped RTB analysis used for Directed Loader / Palletizer (and others).
    Works with both raw Amazon headers and normalized headers from rtb.metrics.clean().
    """
    st.subheader(f"{process_label} — Standards, Trends, Comments")

    # ---------- Resolve column names (raw vs normalized) ----------
    def pick(*names):
        for n in names:
            if n in df_proc.columns:
                return n
        return None

    # Grouping candidates
    fn_col   = pick("Function Name", "function_name")
    size_col = pick("Size", "size")
    ja_col   = pick("Job Action", "job_action")
    ut_col   = pick("Unit Type", "unit_type")
    mgr_col  = pick("Manager", "manager")
    et_col   = pick("Employee Type", "employee_type")

    # Measures / identifiers
    ph_col   = pick("Paid Hours-Total(function,employee)", "paid_hours_total", "hours")
    units_col= pick("Units", "units")
    uph_col  = pick("UPH", "uph")
    jph_col  = pick("JPH", "jph")
    emp_col  = pick("Employee Id", "employee_id", "login")
    name_col = pick("Name", "name")

    # Ensure we have a grouping axis
    group_options = [c for c in [fn_col, size_col, ja_col, ut_col, mgr_col, et_col] if c]
    if not group_options:
        st.info("No suitable grouping columns found (e.g., Function Name).")
        return
    group_col = st.selectbox(f"Group by ({process_label})", group_options, index=0, key=f"group_{process_label}")
    groups = sorted(df_proc[group_col].dropna().unique().tolist())

    # Coerce numerics
    for col in [ph_col, units_col, uph_col, jph_col]:
        if col:
            df_proc[col] = pd.to_numeric(df_proc[col], errors="coerce")

    # Derive UPH if missing
    if uph_col is None and units_col and ph_col:
        df_proc["__UPH__"] = df_proc[units_col] / df_proc[ph_col].replace(0, np.nan)
        uph_col = "__UPH__"

    # ---------- Editable targets ----------
    default_uph = float(uph_low_default)
    default_jph = 20.0

    st.markdown("**Per-Group Standards (editable)**")
    state_key = f"standards_{process_label}_{group_col}"
    if state_key not in st.session_state:
        st.session_state[state_key] = pd.DataFrame({
            group_col: groups,
            "UPH_target": [default_uph]*len(groups),
            "JPH_target": [default_jph]*len(groups),
        })
    else:
        exist = st.session_state[state_key]
        merged = pd.DataFrame({group_col: groups}).merge(exist, on=group_col, how="left")
        merged["UPH_target"] = pd.to_numeric(merged["UPH_target"], errors="coerce").fillna(default_uph)
        merged["JPH_target"] = pd.to_numeric(merged["JPH_target"], errors="coerce").fillna(default_jph)
        st.session_state[state_key] = merged

    std_edit = st.data_editor(
        st.session_state[state_key],
        num_rows="dynamic",
        use_container_width=True,
        key=f"std_editor_{process_label}_{group_col}",
    )
    st.session_state[state_key] = std_edit

    # Apply targets
    rtb = df_proc.merge(std_edit, on=group_col, how="left")

    has_uph = (uph_col in rtb.columns) and rtb[uph_col].notna().any()
    if has_uph and ph_col:
        rtb["UPH_vs_target"] = rtb[uph_col] - rtb["UPH_target"]

        # % below target per group
        pct_below = (rtb.assign(below=rtb["UPH_vs_target"] < 0)
                        .groupby(group_col)["below"].mean()
                        .mul(100).reset_index(name="pct_below_target"))

        # Slope of UPH vs paid hours (simple OLS)
        slope_df = (rtb.groupby(group_col, as_index=False)
                      .apply(lambda g: slope_xy(g[ph_col], g[uph_col]))
                      .rename(columns={None:"slope_uph_per_hr"}))

        fn_sum = (rtb.groupby(group_col, as_index=False)
                    .agg(
                        employees=(emp_col, "nunique") if emp_col else ("UPH_target","size"),
                        paid_hours_total=(ph_col, "sum") if ph_col else ("UPH_target","size"),
                        avg_UPH=(uph_col, "mean"),
                    )
                    .merge(std_edit, on=group_col, how="left")
                    .merge(slope_df, on=group_col, how="left")
                    .merge(pct_below, on=group_col, how="left"))
        fn_sum["UPH_gap"] = (fn_sum["avg_UPH"] - fn_sum["UPH_target"]).round(2)

        def mk_comment(r):
            parts = []
            if pd.notna(r["UPH_gap"]):
                parts.append("at/above target" if r["UPH_gap"] >= 0 else f"{-r['UPH_gap']:.1f} under target")
            if pd.notna(r["slope_uph_per_hr"]):
                if r["slope_uph_per_hr"] > 0.05:
                    parts.append(f"improving (+{r['slope_uph_per_hr']:.2f} UPH/hr)")
                elif r["slope_uph_per_hr"] < -0.05:
                    parts.append(f"declining ({r['slope_uph_per_hr']:.2f} UPH/hr)")
                else:
                    parts.append("flat trend")
            if pd.notna(r.get("pct_below_target", np.nan)):
                parts.append(f"{r['pct_below_target']:.0f}% below target")
            return "; ".join(parts)

        fn_sum["comment"] = fn_sum.apply(mk_comment, axis=1)

        st.markdown(f"**Summary by {group_col}**")
        cols = [group_col,"employees","paid_hours_total","avg_UPH","UPH_target","UPH_gap",
                "slope_uph_per_hr","pct_below_target","comment"]
        show_cols = [c for c in cols if c in fn_sum.columns]
        st.dataframe(fn_sum[show_cols].sort_values(["UPH_gap","slope_uph_per_hr"], ascending=[True,False]),
                     use_container_width=True)

        # Download summary
        buf = io.StringIO(); fn_sum[show_cols].to_csv(buf, index=False)
        st.download_button(f"Download Summary by {group_col} (CSV)", buf.getvalue(),
                           file_name=f"{process_label}_{group_col}_summary.csv", mime="text/csv",
                           key=f"dl_sum_{process_label}_{group_col}")

        # Trend & associates for a selected group
        st.subheader(f"Trend Analysis (per {group_col}) — {process_label}")
        sel_grp = st.selectbox(f"{group_col}", groups, key=f"trend_sel_{process_label}_{group_col}")
        g = rtb[rtb[group_col] == sel_grp].copy()

        if ph_col:
            x = g[ph_col].astype(float).values
            y = g[uph_col].astype(float).clip(0, float(uph_cap_clip)).values
            m = np.isfinite(x) & np.isfinite(y)
            if m.sum() >= 2:
                A = np.vstack([np.ones(m.sum()), x[m]]).T
                intercept, slope = np.linalg.lstsq(A, y[m], rcond=None)[0]
                fig, ax = plt.subplots()
                ax.scatter(x[m], y[m])
                x_line = np.linspace(x[m].min(), x[m].max(), 50)
                y_line = intercept + slope * x_line
                ax.plot(x_line, y_line)
                ax.set_xlabel(ph_col)
                ax.set_ylabel(uph_col)
                ax.set_title(f"{sel_grp} — {uph_col} vs {ph_col} (slope={slope:.2f} UPH/hr)")
                st.pyplot(fig)
            else:
                st.info("Not enough points to plot trend.")

        # Associates table vs this group's target
        tgt = std_edit.loc[std_edit[group_col] == sel_grp]
        uph_tgt = float(tgt["UPH_target"].iloc[0]) if not tgt.empty else np.nan

        assoc_group_keys = [c for c in [emp_col, name_col] if c]
        assoc = (g.groupby(assoc_group_keys, as_index=False)
                   .agg(
                       paid_hours_total=(ph_col,"sum") if ph_col else (uph_col,"size"),
                       avg_UPH=(uph_col,"mean"),
                       units=(units_col,"sum") if units_col else (uph_col,"size"),
                   ))
        assoc["UPH_target"] = uph_tgt
        assoc["UPH_gap"] = (assoc["avg_UPH"] - assoc["UPH_target"]).round(2)

        st.markdown(f"**Associates vs Target — {sel_grp}**")
        st.dataframe(assoc.sort_values(["UPH_gap"], ascending=[True]), use_container_width=True)

        abuf = io.StringIO(); assoc.to_csv(abuf, index=False)
        st.download_button(f"Download Associates for {sel_grp} (CSV)", abuf.getvalue(),
                           file_name=f"{process_label}_{sel_grp}_associates.csv", mime="text/csv",
                           key=f"dl_assoc_{process_label}_{sel_grp}")
    else:
        # Hours-only fallback if Units/UPH absent
        st.warning("No 'Units' or 'UPH' found. Showing hours exposure only. Add a Units column to unlock UPH analysis.")
        if ph_col:
            expo = (rtb.groupby(group_col, as_index=False)
                      .agg(employees=(emp_col,"nunique") if emp_col else (group_col,"size"),
                           paid_hours_total=(ph_col,"sum")))
            st.dataframe(expo.sort_values("paid_hours_total", ascending=False), use_container_width=True)

# =========================
# Tabs for Processes & Legacy
# =========================
tabs = st.tabs(["Directed Loader", "Palletizer", "Legacy (dated) analysis"])

# ---- Directed Loader tab ----
with tabs[0]:
    if "Process Name" in df.columns or "process_name" in df.columns:
        proc_col = "Process Name" if "Process Name" in df.columns else "process_name"
        procs = sorted(df[proc_col].dropna().unique().tolist())
        if "Directed Loader" in procs:
            df_proc = df[df[proc_col] == "Directed Loader"].copy()
        else:
            # If your site labels it differently (e.g., Container Load), pick the first
            df_proc = df[df[proc_col] == procs[0]].copy()
        render_grouped_panel(df_proc, uph_low, uph_cap, process_label="Directed Loader")
    else:
        st.info("No 'Process Name' column found.")

# ---- Palletizer tab ----
with tabs[1]:
    if "Process Name" in df.columns or "process_name" in df.columns:
        proc_col = "Process Name" if "Process Name" in df.columns else "process_name"
        if "Palletizer" in df[proc_col].unique():
            df_proc = df[df[proc_col] == "Palletizer"].copy()
            render_grouped_panel(df_proc, uph_low, uph_cap, process_label="Palletizer")
        else:
            st.info("No rows with Process Name = 'Palletizer'. Select the correct process name in your export.")
    else:
        st.info("No 'Process Name' column found.")

# ---- Legacy (dated) analysis tab ----
with tabs[2]:
    if has_date_schema:
        # Optional: level filter (only if exists)
        if "level" in df.columns:
            level_filter = st.text_input("Level filter (comma-separated, e.g. 5,6)", value="")
            if level_filter.strip():
                levels = [int(x.strip()) for x in level_filter.split(",") if x.strip().isdigit()]
                if levels:
                    df = df[df["level"].isin(levels)].copy()

        daily = aggregate(df)
        cfg = CommentConfig(thresholds=Thresholds(uph_low=uph_low, uph_high=uph_high))
        comments = build_comments(df, cfg)
        fits = per_login_learning_curve(df[["login","shift_id","uph"]])

        st.subheader("Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Shifts", len(df))
        col2.metric("Associates", df["login"].nunique())
        col3.metric("Avg UPH", f"{df['uph'].mean():.1f}")
        col4.metric("Total Units", int(df["units"].sum()))

        st.subheader("Filter: UPH < target")
        low_df = df[df["uph"] < uph_low].copy()
        st.dataframe(low_df.sort_values(["date","login"]).reset_index(drop=True))

        st.subheader("Comment Engine (per-login)")
        st.dataframe(comments.reset_index(drop=True))

        st.subheader("Learning Curve Fits (Power Law y=a*x^b)")
        st.dataframe(fits.sort_values("r2", ascending=False).reset_index(drop=True))

        st.subheader("UPH by Date (All)")
        fig1, ax1 = plt.subplots()
        plot_df = daily.copy()
        plot_df["uph"] = plot_df["uph"].clip(0, uph_cap)
        ax1.plot(plot_df["date"], plot_df["uph"])
        ax1.set_xlabel("Date"); ax1.set_ylabel("UPH")
        st.pyplot(fig1)

        st.subheader("Per-Login Trend (select)")
        choice = st.selectbox("Login", sorted(df["login"].unique()))
        g = df[df["login"] == choice].sort_values("date").copy()
        g["uph"] = g["uph"].clip(0, uph_cap)
        fig2, ax2 = plt.subplots()
        ax2.plot(g["date"], g["uph"])
        ax2.set_xlabel("Date"); ax2.set_ylabel("UPH")
        st.pyplot(fig2)

        st.subheader("Projected Learning Curve")
        fit_row = fits[fits["login"] == choice]
        if not fit_row.empty and np.isfinite(fit_row["a"].iloc[0]) and np.isfinite(fit_row["b"].iloc[0]):
            a = fit_row["a"].iloc[0]; b = fit_row["b"].iloc[0]
            last_n = int(g["shift_id"].max())
            future_x = np.arange(1, max(last_n + 8, 10))
            y_pred = a * (future_x ** b)
            fig3, ax3 = plt.subplots()
            ax3.plot(g["shift_id"], g["uph"], label="actual")
            ax3.plot(future_x, y_pred, label="predicted")
            ax3.set_xlabel("Session index"); ax3.set_ylabel("UPH"); ax3.legend()
            st.pyplot(fig3)
        else:
            st.info("Not enough data to estimate a learning curve for this login.")
    else:
        st.info("This tab activates only for dated CSVs (with columns: date, login, level, hours, units).")

