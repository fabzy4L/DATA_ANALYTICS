# RECEPTOR_DESIGN — Project Review (Updated 2026-05-01)

## Project Overview

**Goal:** Structural investigation of the Serotonin Transporter (SERT) and how the A348T point mutation (referred to as S348T in biological sequence conventions) affects Escitalopram binding affinity.

**Authoritative output:** `docs/research_article.md` / `docs/research_article.html`

---

## Current Status

| Area | Status | Output |
|---|---|---|
| Wild-type structures (5I6Z, 5I71, 2A65) | Done | `data/structures/` |
| Structural audit & provenance correction | Done | `scripts/structural_audit.py`, `data/structures/5i6z_A_true.pdb` |
| In-silico mutagenesis (A348T, g+ rotamer) | Done | `data/structures/5i6z_A_S348T_correct.pdb` |
| Escitalopram 3D structure | Done | `output/escitalopram.pdb` |
| Ligand PDBQT preparation | Done | `output/escitalopram.pdbqt` |
| Receptor PDBQT preparation | Done | `output/receptor_wt.pdbqt`, `output/receptor_s348t.pdbqt` |
| Molecular docking (AutoDock Vina 1.2.5) | Done | `output/docked_wt.pdbqt`, `output/docked_s348t.pdbqt` |
| Reverse translation pipeline | Done | `notebooks/REVERSE TRANSLATION.ipynb` |
| Research article | Done | `docs/research_article.md/.html` |

---

## Key Results

| Metric | WT (ALA348) | A348T (THR348) |
|---|---|---|
| Best docking affinity | −8.116 kcal/mol | −8.089 kcal/mol |
| ΔΔG | — | +0.027 kcal/mol |
| TM6 backbone RMSD | — | 0.000 Å |
| TM6 H-bonds (340–360) | 102 | — |
| Atomic contacts at res. 348 | 154 | — |

**Conclusion:** A348T produces no statistically significant change in escitalopram binding affinity at current sampling depth.

---

## Important Correction

Early analysis files (in `docs/archive/`) were produced using structural inputs
that did not originate from 5I6Z (37 Å TM6 RMSD vs. raw PDB). Those findings
are superseded. See `docs/STRUCTURAL_AUDIT_FINDINGS.md` for full details.

---

## Remaining Work

1. Re-run docking at exhaustiveness = 32 with multiple seeds
2. Regenerate ligand PDBQT with OpenBabel Gasteiger charges
3. Run ChimeraX energy minimization (`scripts/S348T_Minimization_Workflow.cxc`)
4. Build canonical SER348 homology model from UniProt P31645
5. MD simulation (100 ns, explicit POPC bilayer)
