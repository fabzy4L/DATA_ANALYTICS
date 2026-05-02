# RECEPTOR_DESIGN — Project Gaps (Updated 2026-05-02)

The core computational pipeline investigates the **S438T** mutation in SERT and its effect on escitalopram binding affinity.

---

## Completed

- Structural audit and provenance correction (scripts/structural_audit.py)
- True WT extraction: data/structures/5i6z_A_true.pdb
- In-silico mutagenesis for S438T: data/structures/5i6z_A_S438T.pdb
- Ligand and receptor PDBQT generation for S438T
- AutoDock Vina 1.2.5 docking — WT and S438T, 10 poses each
- Research article: docs/research/S438T_RESEARCH_ARTICLE.md / .html

---

## Remaining Gaps (Priority Order)

### 1. Docking Accuracy
- **Exhaustiveness:** Current runs used exhaustiveness = 8. Minimum recommended for publication: 32.
- **Seeds:** Single random seed per run. Use ≥ 5 independent seeds and report mean ± SD.
- **Ligand charges:** Simplified Gasteiger-like approximation. Replace with OpenBabel Gasteiger charges.

### 2. Receptor Preparation
- **Energy minimization:** The S438T model was not force-field relaxed before docking.
  Localized minimization of the S1 pocket residues (including 438) would improve side-chain orientation.
- **Hydrogen atoms:** Receptor PDBQT currently excludes H. Add polar hydrogens for improved H-bond scoring.

### 3. Canonical Biological WT
- While S438T is the correct site, the 5I6Z construct has other engineered mutations (A291, S439, etc.). 
  Building a truly canonical SERT model from the UniProt P31645 sequence via homology modeling 
  would provide a "clean" baseline for investigating the clinical impact of S438T.

### 4. Validation
- Use the co-crystallized (R)-citalopram pose (residue 68P in 5I71) to validate that
  the docking box correctly recovers the known binding mode before interpreting mutation effects.
- Cross-dock escitalopram into 5I71 chain A as a positive control.

### 5. Extended Analysis
- MM-GBSA re-scoring of top docked poses
- 100 ns MD simulation (WT vs S438T) in explicit POPC lipid bilayer to capture the desolvation and kinetic effects mentioned in Plenge et al. (2020).

### 6. Housekeeping
- Hardcoded paths in `notebooks/Escitalopram_PythonPDB.ipynb` (points to local `/Downloads/`)
- `data/sequences/5I6Z_edited.fasta` — confirm mutation reflections in sequence
