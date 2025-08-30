# RTB Analysis App (Starter)

A quick, offline-capable Streamlit app for RTB-style ops analysis. Upload CSVs, compute UPH, run filters (e.g., Level 5 & UPH < 125), visualize learning curves, and auto-generate performance comments.

## Install

pwd                # Show your current directory (print working directory)
ls                 # List files/folders in current directory
ls -l              # Long list (permissions, sizes, dates)
ls -a              # Show hidden files (start with .)

cd folder_name     # Move into a folder
cd ..              # Go up one directory level
cd ../..           # Go up two levels
cd ~               # Go to your home directory
cd /               # Go to the root of the filesystem


mkdir new_folder       # Create a new folder
touch file.txt         # Create an empty file
rm file.txt            # Delete a file
rm -r folder_name      # Delete a folder and its contents
cp file.txt copy.txt   # Copy a file
mv file.txt newname.txt # Rename or move a file

ls | grep "word"       # List only files containing "word"
find . -name "*.py"    # Find all Python files in current directory

python3 file.py                # Run a Python file
pip install package_name        # Install a Python package
streamlit run app.py            # Run your Streamlit app

#Stop the running Streamlit app
Click into the PowerShell window and press Ctrl + C

```bash
# Recommend a clean venv
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

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
