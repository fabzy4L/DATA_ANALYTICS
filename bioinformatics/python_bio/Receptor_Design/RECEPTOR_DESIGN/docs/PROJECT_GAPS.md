# RECEPTOR_DESIGN — Project Gaps (Updated 2026-05-01)

The core computational pipeline is complete. Remaining gaps are refinements.

---

## Completed

- Structural audit and provenance correction (scripts/structural_audit.py)
- True WT extraction: data/structures/5i6z_A_true.pdb
- Correct in-silico mutagenesis: data/structures/5i6z_A_S348T_correct.pdb
- Ligand and receptor PDBQT generation
- AutoDock Vina 1.2.5 docking — WT and A348T, 10 poses each
- Research article: docs/research_article.md / .html
- Reverse translation pipeline (AA → DNA)

---

## Remaining Gaps (Priority Order)

### 1. Docking Accuracy
- **Exhaustiveness:** Current runs used exhaustiveness = 8. Minimum recommended for publication: 32.
- **Seeds:** Single random seed per run. Use ≥ 5 independent seeds and report mean ± SD.
- **Ligand charges:** Simplified Gasteiger-like approximation. Replace with OpenBabel Gasteiger charges.

### 2. Receptor Preparation
- **Energy minimization:** The A348T model was not force-field relaxed before docking.
  Run `scripts/S348T_Minimization_Workflow.cxc` in ChimeraX first.
- **Hydrogen atoms:** Receptor PDBQT currently excludes H. Add polar hydrogens for improved H-bond scoring.

### 3. Canonical Biological WT
- Position 348 in 5I6Z is ALA (no SEQADV entry). The biologically intended S348T study
  (Ser → Thr) requires a model built from the canonical UniProt P31645 sequence via
  homology modeling (e.g., MODELLER or AlphaFold2 with mutation).

### 4. Validation
- Use the co-crystallized (R)-citalopram pose (residue 68P in 5I71) to validate that
  the docking box correctly recovers the known binding mode before interpreting mutation effects.
- Cross-dock escitalopram into 5I71 chain A as a positive control.

### 5. Extended Analysis
- MM-GBSA re-scoring of top docked poses
- 100 ns MD simulation (WT vs A348T) in explicit POPC lipid bilayer
- Populate `Annotations.txt` with residue-level structural observations

### 6. Housekeeping
- Hardcoded paths in `notebooks/Escitalopram_PythonPDB.ipynb` (points to local `/Downloads/`)
- `data/sequences/5I6Z_edited.fasta` — confirm whether S348T mutation is reflected in sequence
