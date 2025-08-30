# RTB Analysis App (Starter)

A quick, offline-capable Streamlit app for RTB-style ops analysis. Upload CSVs, compute UPH, run filters (e.g., Level 5 & UPH < 125), visualize learning curves, and auto-generate performance comments.

## Install

```bash
# Recommend a clean venv
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

# Make sure pip/wheel/setuptools are up-to-date
python -m pip install --upgrade pip setuptools wheel

# Install a prebuilt pyarrow wheel first (this avoids compiling)
python -m pip install "pyarrow==14.0.2" --only-binary=:all:

# Now install the rest
python -m pip install streamlit==1.31.1 pandas==2.2.2 numpy==1.26.4 matplotlib==3.8.4 scikit-learn==1.4.2


## Run

```bash
streamlit run app.py
```

## CSV Schema (sample)
- `date` (YYYY-MM-DD)
- `shift_id` (int or str)
- `login` (str) — associate login/user-id
- `level` (int) — e.g., 1..6
- `hours` (float)
- `units` (int)
- `path` (str) — process/path name (optional)

App derives:
- `uph` = `units` / `hours`

## Notes
- Learning curves are estimated per-associate via a power-law fit over session index.
- Comment engine flags outliers, improving/declining trends, and low/high performers.
- All plots use matplotlib only.

Generated on: 2025-08-12 00:02:48
