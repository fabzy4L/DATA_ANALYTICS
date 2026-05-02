# SERT S438T Mutation — Computational Analysis

**Fabian A. Alvarez-Primo, Ph.D.**

A computational structural biology study of the **S438T** point mutation in the human Serotonin Transporter (SERT, *SLC6A4*) and its effect on escitalopram binding affinity.

---

## Key Result

| Receptor | Residue 438 | Best Affinity (kcal/mol) |
|:---|:---:|:---:|
| Wild-Type | SER | −8.1 |
| S438T Mutant | THR | −8.3 |

**ΔΔG = −0.2 kcal/mol** — escitalopram maintains high affinity in the rigid-receptor model. The experimentally observed 320-fold *K*i increase (Andersen *et al.*, 2009) is not reproduced under static docking conditions, consistent with the known limitations of rigid-receptor approximations.

---

## Primary Deliverable

`docs/research/S438T_RESEARCH_ARTICLE.html` — self-contained research article with methods, results, and discussion.

---

## Project Structure

```
data/
  structures/       PDB files — wild-type (5i6z_A_true.pdb), S438T mutant (5i6z_A_S438T.pdb),
                    reference structures (2a65.pdb, 5i71.pdb), ChimeraX sessions
  sequences/        FASTA sequences for 5I6Z and 5I71

scripts/
  generate_s438t.py         In-silico mutagenesis — NERF algorithm, g+ rotamer placement
  docking_prep.py           Receptor PDBQT generation and AutoDock Vina config setup
  generate_ligand_pdbqt.py  Ligand PDBQT preparation
  structural_audit.py       Provenance verification of PDB files
  sert_analysis.cxc         ChimeraX analysis session script

notebooks/
  Escitalopram_PythonPDB.ipynb    RDKit 3D conformation generation from SMILES
  REVERSE TRANSLATION.ipynb       Amino acid → DNA reverse translation

output/
  5i6z_A_true.pdb             Verified wild-type chain A
  5i6z_A_S438T.pdb            S438T mutant structure
  receptor_wt.pdbqt           Wild-type receptor for docking
  receptor_s438t.pdbqt        S438T receptor for docking
  escitalopram.pdbqt          Ligand for docking
  docked_wt.pdbqt             Wild-type docking poses
  docked_s438t.pdbqt          S438T docking poses
  vina_wt.log                 Wild-type Vina output (best: −8.1 kcal/mol)
  vina_s438t.log              S438T Vina output (best: −8.3 kcal/mol)
  docking_results_report.txt  Full pose table and interpretation

docs/
  research/
    S438T_RESEARCH_ARTICLE.md/.html    Primary research article
    REVIEW_ARTICLE.md/.html            Structure-function review with experimental context
    PLENGE_ALIGNMENT_REVIEW.md/.html   Alignment vs. Plenge (2020) and Andersen (2009)
    2A65_v_5I6Z_Comparison.md          LeuT vs. hSERT structural comparison
    PROJECT_REVIEW.md                  Project status summary
    PROJECT_GAPS.md                    Remaining gaps and next steps
  papers/
    10276.pdf                          Andersen et al. (2009) — J. Biol. Chem. 284:10276
    s41467-020-15292-y.pdf             Plenge et al. (2020) — Nat. Commun. 11:1491
  archive/                             Superseded reports and working documents
```

---

## Computational Pipeline

### 1. Receptor Preparation
Chain A extracted from PDB 5I6Z (`5i6z_A_true.pdb`). The S438T mutation was introduced using a Python implementation of the **NERF algorithm** with the Threonine side chain placed in the g+ rotamer (χ1 = +60°) — the statistically preferred conformation in transmembrane helices.

### 2. Ligand Preparation
Escitalopram 3D conformation generated from SMILES using **RDKit** with MMFF force field minimization. Converted to PDBQT format for AutoDock Vina compatibility.

### 3. Molecular Docking
Docked using **AutoDock Vina 1.2.5** with a 25 × 25 × 25 Å grid box centered on the S1 binding pocket (33.06, 187.25, 141.04). Exhaustiveness = 8, 10 poses per run.

### 4. Visualization
ChimeraX sessions in `data/structures/` for structural overlay and binding pocket analysis.

---

## References

1. Coleman, J.A., *et al.* (2016). X-ray structures of the human serotonin transporter. *Science*, 352, 1478–1480. [PDB: 5I6Z]
2. Andersen, J., *et al.* (2009). Location of the antidepressant binding site in the serotonin transporter. *J. Biol. Chem.*, 284, 10276–10284.
3. Plenge, P., *et al.* (2020). The mechanism of a high-affinity allosteric inhibitor of the serotonin transporter. *Nat. Commun.*, 11, 1491.
4. Trott, O., & Olson, A.J. (2010). AutoDock Vina. *J. Comput. Chem.*, 31, 455–461.
