# Project Reorganization Plan - SERT Design

## Current State Summary
The project is currently a flat directory containing a mix of structural data (PDB, CIF, CXS), sequence data (FASTA), analysis notebooks (IPYNB), and reference literature (PDF). There is some redundancy (e.g., duplicate PDFs in a subfolder and checkpoint files).

## Proposed Structure
Following the recommendations in `README.md`, the files will be reorganized into the following hierarchy:

```text
RECEPTOR_DESIGN/
├── data/
│   ├── structures/          # PDB, CIF, and ChimeraX (.cxs) files
│   └── sequences/           # FASTA files (Wild-type and mutated)
├── notebooks/               # Jupyter Notebooks for analysis
├── docs/
│   ├── papers/              # Scientific publications (PDFs)
│   └── guides/              # Instructions and annotations
├── output/                  # Generated structural models
└── scripts/                 # (Optional) Future standalone Python scripts
```

## Action Items
1. **Create Directories:** Create the folder structure defined above.
2. **Move Structural Data:**
   - Move all `.pdb`, `.cif`, and `.cxs` files to `data/structures/`.
   - *Exception:* `escitalopram.pdb` (generated) moves to `output/`.
3. **Move Sequence Data:** Move all `.fasta` files to `data/sequences/`.
4. **Move Notebooks:** Move `.ipynb` files to `notebooks/`.
5. **Move Documentation & Papers:**
   - Move all `.pdf` files to `docs/papers/`.
   - Move `Instructions.txt` and `Annotations.txt` to `docs/guides/`.
6. **Cleanup:**
   - Remove redundant `RECEPTOR DESIGN/` folder.
   - Remove `.DS_Store` and empty `New Text Document.txt`.
   - Remove `.ipynb_checkpoints/`.
   - Remove redundant `Escitalopram_PythonPDB.ipynb.ipynb`.
