# app.py — Integrated RTB Analysis (Directed Loader + Palletizer + Legacy)
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---- Legacy helpers (used only when a dated CSV is uploaded) ----
from rtb.metrics import aggregate, Thresholds, ewma, percentile_band
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

# CSV load (after file_uploader)
raw = pd.read_csv(uploaded)

# Clean using your flexible metrics.clean()
from rtb.metrics import clean
df = clean(raw)

# Detect if it's a legacy (dated) file for those old charts/tables
has_date_schema = {"date","login","level","hours","units"}.issubset(df.columns)

# Compat: some legacy code expects lowercase 'uph'
if "UPH" in df.columns and "uph" not in df.columns:
    df["uph"] = pd.to_numeric(df["UPH"], errors="coerce")

# Preview raw upload
st.write("Uploaded DataFrame preview:")
st.dataframe(raw.head())

# =========================
# Flexible Clean (works for both schemas)
# =========================
def flexible_clean(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    """
    Return (clean_df, has_date_schema).
    - Legacy schema: expects ['date','login','level','hours','units'] -> adds 'uph' & 'shift_id'
    - RTB schema (your current file): expects at least
        ['Process Name','Function Name','Employee Id','Paid Hours-Total(function,employee)']
      Derives UPH if 'Units' exists; creates shift_id per (Employee Id, Function Name).
    """
    # Path A: legacy dated schema
    legacy = {"date","login","level","hours","units"}
    if legacy.issubset(df.columns):
        out = df.copy()
        out["date"] = pd.to_datetime(out["date"])
        out["hours"] = pd.to_numeric(out["hours"], errors="coerce").fillna(0.0)
        out["units"] = pd.to_numeric(out["units"], errors="coerce").fillna(0.0)
        out = out[out["hours"] >= 0.25]
        out["uph"] = out["units"] / out["hours"]
        if "shift_id" not in out.columns:
            out = out.sort_values(["login","date"])
            out["shift_id"] = out.groupby("login").cumcount() + 1
        return out, True

    # Path B: RTB schema (like your screenshot)
    needed_min = {"Process Name","Function Name","Employee Id","Paid Hours-Total(function,employee)"}
    if needed_min.issubset(df.columns):
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

        # Derive UPH if Units present
        if "UPH" not in out.columns and "Units" in out.columns:
            ph = out["Paid Hours-Total(function,employee)"].replace(0, np.nan)
            out["UPH"] = out["Units"] / ph

        # Back-compat for legacy code that expects lowercase 'uph'
        if "UPH" in out.columns and "uph" not in out.columns:
            out["uph"] = out["UPH"]

        if "shift_id" not in out.columns:
            out["shift_id"] = out.groupby(["Employee Id","Function Name"]).cumcount() + 1
        return out, False

    raise ValueError(
        "Unrecognized schema. Provide either legacy columns "
        "['date','login','level','hours','units'] or RTB columns with at least "
        "['Process Name','Function Name','Employee Id','Paid Hours-Total(function,employee)'] "
        "and optionally 'Units' to derive UPH."
    )

try:
    df, has_date_schema = flexible_clean(raw)
except Exception as e:
    st.error(str(e))
    st.stop()

# =========================
# Shared helpers for grouped RTB panels
# =========================
def slope_xy(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2: 
        return np.nan
    A = np.vstack([np.ones(m.sum()), x[m]]).T
    coef, *_ = np.linalg.lstsq(A, y[m], rcond=None)
    return float(coef[1])

def render_grouped_panel(df_proc: pd.DataFrame, uph_low_default: float, uph_cap_clip: float,
                         process_label: str):
    """
    Generic grouped RTB analysis used for Directed Loader / Palletizer (and others).
    Groups by Function Name by default, but allows Size/Job Action/Unit Type/Manager/Employee Type.
    """
    st.subheader(f"{process_label} — Standards, Trends, Comments")

    # Ensure core numerics
    for col in ["Paid Hours-Total(function,employee)","Units","UPH","JPH"]:
        if col in df_proc.columns:
            df_proc[col] = pd.to_numeric(df_proc[col], errors="coerce")

    # Derive UPH if missing
    if "UPH" not in df_proc.columns and "Units" in df_proc.columns:
        ph = df_proc["Paid Hours-Total(function,employee)"].replace(0, np.nan)
        df_proc["UPH"] = df_proc["Units"] / ph

    # Grouping axis (per-LC style)
    group_options = [c for c in ["Function Name","Size","Job Action","Unit Type","Manager","Employee Type"]
                     if c in df_proc.columns]
    if not group_options:
        group_options = ["Function Name"]
    group_col = st.selectbox(f"Group by ({process_label})", group_options, index=0, key=f"group_{process_label}")
    groups = sorted(df_proc[group_col].dropna().unique().tolist())

    # Standards editor (seed from sidebar)
    default_uph = float(uph_low_default)
    default_jph = 20.0

    st.markdown("**Per‑Group Standards (editable)**")
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

    has_uph = "UPH" in rtb.columns and rtb["UPH"].notna().any()
    if has_uph:
        rtb["UPH_vs_target"] = rtb["UPH"] - rtb["UPH_target"]
        pct_below = (rtb.assign(below=rtb["UPH_vs_target"] < 0)
                        .groupby(group_col)["below"].mean()
                        .mul(100).reset_index(name="pct_below_target"))

        slope_df = (rtb.groupby(group_col, as_index=False)
                      .apply(lambda g: slope_xy(g["Paid Hours-Total(function,employee)"], g["UPH"]))
                      .rename(columns={None:"slope_uph_per_hr"}))

        fn_sum = (rtb.groupby(group_col, as_index=False)
                    .agg(
                        employees=("Employee Id","nunique"),
                        paid_hours_total=("Paid Hours-Total(function,employee)","sum"),
                        avg_UPH=("UPH","mean"),
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
        st.dataframe(fn_sum[cols].sort_values(["UPH_gap","slope_uph_per_hr"], ascending=[True,False]),
                     use_container_width=True)

        # Download summary
        buf = io.StringIO(); fn_sum[cols].to_csv(buf, index=False)
        st.download_button(f"Download Summary by {group_col} (CSV)", buf.getvalue(),
                           file_name=f"{process_label}_{group_col}_summary.csv", mime="text/csv",
                           key=f"dl_sum_{process_label}_{group_col}")

        # Trend & associates for a selected group
        st.subheader(f"Trend Analysis (per {group_col}) — {process_label}")
        sel_grp = st.selectbox(f"{group_col}", groups, key=f"trend_sel_{process_label}_{group_col}")
        g = rtb[rtb[group_col] == sel_grp].copy()

        x = g["Paid Hours-Total(function,employee)"].astype(float).values
        y = g["UPH"].astype(float).clip(0, float(uph_cap_clip)).values
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() >= 2:
            A = np.vstack([np.ones(m.sum()), x[m]]).T
            intercept, slope = np.linalg.lstsq(A, y[m], rcond=None)[0]
            fig, ax = plt.subplots()
            ax.scatter(x[m], y[m])
            x_line = np.linspace(x[m].min(), x[m].max(), 50)
            y_line = intercept + slope * x_line
            ax.plot(x_line, y_line)
            ax.set_xlabel("Paid Hours Total (function, employee)")
            ax.set_ylabel("UPH")
            ax.set_title(f"{sel_grp} — UPH vs Paid Hours (slope={slope:.2f} UPH/hr)")
            st.pyplot(fig)
        else:
            st.info("Not enough points to plot trend.")

        # Associates table vs this group's target
        tgt = std_edit.loc[std_edit[group_col] == sel_grp]
        uph_tgt = float(tgt["UPH_target"].iloc[0]) if not tgt.empty else np.nan

        assoc = (g.groupby(["Employee Id","Name"], as_index=False)
                   .agg(
                       paid_hours_total=("Paid Hours-Total(function,employee)","sum"),
                       avg_UPH=("UPH","mean"),
                       units=("Units","sum") if "Units" in g.columns else ("Paid Hours-Total(function,employee)","size"),
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
        expo = (rtb.groupby(group_col, as_index=False)
                  .agg(employees=("Employee Id","nunique"),
                       paid_hours_total=("Paid Hours-Total(function,employee)","sum")))
        st.dataframe(expo.sort_values("paid_hours_total", ascending=False), use_container_width=True)

# =========================
# Tabs for Processes & Legacy
# =========================
tabs = st.tabs(["Directed Loader", "Palletizer", "Legacy (dated) analysis"])

# ---- Directed Loader tab ----
with tabs[0]:
    if "Process Name" in df.columns:
        procs = sorted(df["Process Name"].dropna().unique().tolist())
        if "Directed Loader" in procs:
            df_proc = df[df["Process Name"] == "Directed Loader"].copy()
        else:
            # If your site labels it differently (e.g., Container Load), pick the first
            df_proc = df[df["Process Name"] == procs[0]].copy()
        render_grouped_panel(df_proc, uph_low, uph_cap)
    else:
        st.info("No 'Process Name' column found.")

# ---- Palletizer tab ----
with tabs[1]:
    if "Process Name" in df.columns:
        if "Palletizer" in df["Process Name"].unique():
            df_proc = df[df["Process Name"] == "Palletizer"].copy()
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
