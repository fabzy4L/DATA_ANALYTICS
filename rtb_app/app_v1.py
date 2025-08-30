import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from rtb.metrics import clean, aggregate, Thresholds, ewma, percentile_band
from rtb.models import per_login_learning_curve, predict_uph
from rtb.comments import build_comments, CommentConfig

st.set_page_config(page_title="RTB Analysis", layout="wide")

st.title("RTB Analysis — Starter")
st.caption("Upload CSVs, filter cohorts, visualize UPH & learning curves, auto-generate comments.")

with st.sidebar:
    st.header("Controls")
    uph_low = st.number_input("UPH target (low threshold)", min_value=0.0, value=125.0, step=5.0)
    uph_high = st.number_input("UPH high-performer threshold", min_value=0.0, value=300.0, step=10.0)
    level_filter = st.text_input("Level filter (comma-separated, e.g. 5,6)", value="")
    uph_cap = st.number_input("UPH cap for plotting (clip)", min_value=0.0, value=600.0, step=10.0)
    uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded is None:
    st.info("Upload a CSV to begin. See README for schema. A sample dataset is included in the repo.")
    st.stop()

raw = pd.read_csv(uploaded)
df = clean(raw)

# Optional: filter levels
if level_filter.strip():
    levels = [int(x.strip()) for x in level_filter.split(",") if x.strip().isdigit()]
    if levels:
        df = df[df["level"].isin(levels)].copy()

# Derived aggregations
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
ax1.set_xlabel("Date")
ax1.set_ylabel("UPH")
st.pyplot(fig1)

st.subheader("Per-Login Trend (select)")
choice = st.selectbox("Login", sorted(df["login"].unique()))
g = df[df["login"] == choice].sort_values("date").copy()
g["uph"] = g["uph"].clip(0, uph_cap)
fig2, ax2 = plt.subplots()
ax2.plot(g["date"], g["uph"])
ax2.set_xlabel("Date")
ax2.set_ylabel("UPH")
st.pyplot(fig2)

st.subheader("Projected Learning Curve")
fit_row = fits[fits["login"] == choice]
if not fit_row.empty and np.isfinite(fit_row["a"].iloc[0]) and np.isfinite(fit_row["b"].iloc[0]):
    a = fit_row["a"].iloc[0]
    b = fit_row["b"].iloc[0]
    last_n = int(g["shift_id"].max())
    future_x = np.arange(1, max(last_n + 8, 10))
    y_pred = a * (future_x ** b)
    fig3, ax3 = plt.subplots()
    ax3.plot(g["shift_id"], g["uph"], label="actual")
    ax3.plot(future_x, y_pred, label="predicted")
    ax3.set_xlabel("Session index")
    ax3.set_ylabel("UPH")
    ax3.legend()
    st.pyplot(fig3)
else:
    st.info("Not enough data to estimate a learning curve for this login.")
