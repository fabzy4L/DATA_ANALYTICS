#!/usr/bin/env python3
import os, re, argparse
import pandas as pd
from datetime import datetime

def normalize_lc(val):
    import pandas as pd, re
    if pd.isna(val):
        return None
    s = str(val).strip().upper()
    m = re.match(r"LC\s*([1-5])", s)
    if m:
        return f"LC{m.group(1)}"
    m2 = re.search(r"([1-5])", s)
    if m2:
        return f"LC{m2.group(1)}"
    return None

def parse_date_from_filename(filepath):
    from datetime import datetime
    fname = os.path.basename(filepath)
    m = re.search(r"RTBAnalysis\s*-\s*(\d{2})\.(\d{2})\.(\d{2})", fname)
    if not m:
        today = datetime.now()
        return today.strftime("[%m.%d.%y]"), today.strftime("%m.%d.%Y")
    mm, dd, yy = m.groups()
    long_year = int(yy)
    long_year += 2000 if long_year <= 79 else 1900
    return f"[{mm}.{dd}.{yy}]", f"{mm}.{dd}.{long_year}"

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    import pandas as pd, re
    df.columns = [c.strip() for c in df.columns]

    # Rename common headers (only those that exist)
    rename_map = {
        "PAID HOURS-TOTAL(FUNCTION,EMPLOYEE)": "Hours",
        "UNITS": "Units",
        "UPH": "UPH",
        "LOGIN": "Login",
        "LC": "LC"
    }
    exist_map = {k: v for k, v in rename_map.items() if k in df.columns}
    df = df.rename(columns=exist_map)

    # Ensure required columns exist
    for col in ["Hours", "Units", "UPH", "LC"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Coerce Hours/Units/UPH to numeric; compute UPH if missing
    df["Hours"] = pd.to_numeric(df["Hours"], errors="coerce")
    df["Units"] = pd.to_numeric(df["Units"], errors="coerce")
    df["UPH"]   = pd.to_numeric(df["UPH"],   errors="coerce")

    # If UPH is NaN but Hours and Units exist, compute it
    need_uph = df["UPH"].isna() & df["Hours"].notna() & (df["Hours"] > 0) & df["Units"].notna()
    df.loc[need_uph, "UPH"] = df.loc[need_uph, "Units"] / df.loc[need_uph, "Hours"]

    # Normalize LC labels
    def normalize_lc(val):
        if pd.isna(val): return None
        s = str(val).strip().upper()
        m = re.match(r"LC\s*([1-5])", s)
        if m: return f"LC{m.group(1)}"
        m2 = re.search(r"([1-5])", s)
        if m2: return f"LC{m2.group(1)}"
        return None
    df["LC"] = df["LC"].apply(normalize_lc)

    # Drop rows where Hours<=0 or Units<=0, and where UPH is still missing/nonpositive
    df = df.dropna(subset=["Hours", "Units"])
    df = df[(df["Hours"] > 0) & (df["Units"] > 0)]
    df = df.dropna(subset=["UPH"])
    df = df[df["UPH"] > 0]

    return df

def compute_metrics(df, uph_threshold=125.0):
    total_units = df["Units"].sum()
    total_hours = df["Hours"].sum()
    weighted_uph = (total_units / total_hours) if total_hours > 0 else 0.0
    df["Below_Standard"] = df["UPH"] < uph_threshold
    lcs = [f"LC{i}" for i in range(1, 6)]
    lc_stats = {}
    for lc in lcs:
        sub = df[df["LC"] == lc]
        total = len(sub)
        under = int(sub["Below_Standard"].sum()) if total > 0 else 0
        lc_stats[lc] = {"total": total, "under": under}
    total_associates = len(df)
    total_under = int(df["Below_Standard"].sum())
    under_rate_pct = (100 * total_under / total_associates) if total_associates else 0.0
    q25 = df["Hours"].quantile(0.25) if total_associates else 0.0
    df["Short_Hours"] = df["Hours"] <= q25 if total_associates else False
    if total_under > 0:
        short_share = 100 * len(df[df["Below_Standard"] & df["Short_Hours"]]) / total_under
    else:
        short_share = 0.0
    lc_rates = []
    for lc in lcs:
        total = lc_stats[lc]["total"]
        under = lc_stats[lc]["under"]
        rate = (under / total) if total else 0.0
        lc_rates.append((lc, rate, under, total))
    lc_rates_sorted = sorted(lc_rates, key=lambda x: (x[1], x[2]), reverse=True)
    targeted_lcs = [x[0] for x in lc_rates_sorted[:2] if x[2] > 0]
    high_lc_under = (lc_stats.get("LC4", {"under":0})["under"] +
                     lc_stats.get("LC5", {"under":0})["under"])
    isolated_to_new_hires = high_lc_under < max(1, int(0.4 * total_under))
    return dict(
        total_units=int(total_units),
        total_hours=round(float(total_hours), 2),
        weighted_uph=round(float(weighted_uph), 2),
        threshold=uph_threshold,
        lcs=lcs,
        lc_stats=lc_stats,
        total_associates=total_associates,
        total_under=total_under,
        under_rate_pct=round(float(under_rate_pct), 1),
        q25_hours=round(float(q25), 2),
        short_share_pct=round(float(short_share), 1),
        isolated_to_new_hires=isolated_to_new_hires,
        targeted_lcs=targeted_lcs,
    )

def build_comment(header_date, long_date, m):
    above_below = "above" if m["weighted_uph"] >= m["threshold"] else "below"
    iso_phrase = "are isolated to new hires" if m["isolated_to_new_hires"] else "are not isolated to new hires"
    lc_lines = []
    for lc in m["lcs"]:
        stats = m["lc_stats"][lc]
        lc_lines.append(f"{lc} had {stats['under']} of {stats['total']} under")
    lc_phrase = ", ".join(lc_lines) + "."
    targeted = m["targeted_lcs"]
    targeted_phrase = "LC5" if not targeted else ", ".join(targeted)
    comment = (
        f"{header_date} Ship Dock Container Build\n\n"
        f"On {long_date}, Container Build output totaled {m['total_units']} units over {m['total_hours']} hours, "
        f"averaging {m['weighted_uph']} UPH. This was {above_below} the {int(m['threshold'])} UPH threshold. "
        f"However, {m['total_under']} associates ({m['under_rate_pct']}%) fell below standard. "
        f"{lc_phrase} Performance issues {iso_phrase}, with "
        f"{'notable underperformance among LC4–LC5' if not m['isolated_to_new_hires'] else 'most issues concentrated in LC1–LC2'}."
        f" Analysis indicates rate dilution from short-hour associates (bottom 25% by hours at ≤ {m['q25_hours']} hours), "
        f"accounting for approximately {m['short_share_pct']}% of below-threshold cases. "
        f"Recommended focus includes reinforcing pacing consistency, aligning work distribution to reduce dilution from "
        f"short-hour associates, and targeted coaching for {targeted_phrase} associates to stabilize overall performance."
    )
    return comment

def analyze_file(filepath):
    header_date, long_date = parse_date_from_filename(filepath)
    df_raw = pd.read_csv(filepath)
    df_clean = clean_dataset(df_raw)
    metrics = compute_metrics(df_clean)
    comment = build_comment(header_date, long_date, metrics)
    rows = []
    for lc in metrics["lcs"]:
        rows.append({
            "LC": lc,
            "Total_Associates": metrics["lc_stats"][lc]["total"],
            "Under_Count": metrics["lc_stats"][lc]["under"]
        })
    lc_df = pd.DataFrame(rows)
    return lc_df, comment

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", help="Path to RTBAnalysis - MM.DD.YY.csv")
    ap.add_argument("--out", default="RTB_comment.txt", help="Output text file for the comment")
    args = ap.parse_args()

    lc_df, comment = analyze_file(args.csv_path)
    print(comment)
    lc_df.to_csv("LC_summary.csv", index=False)
    with open(args.out, "w") as f:
        f.write(comment)

if __name__ == "__main__":
    main()
