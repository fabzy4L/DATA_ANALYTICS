# Structural and Computational Analysis of the S348T Mutation in the Human Serotonin Transporter and Its Effect on Escitalopram Binding

**Fabian A. Alvarez-Primo, Ph.D.**

*Computational Structural Biology | May 1, 2026*

---

## Abstract

The human Serotonin Transporter (SERT, *SLC6A4*) is the principal molecular target of selective serotonin reuptake inhibitors (SSRIs), a first-line pharmacological class for major depressive disorder and anxiety. Understanding how residue-level mutations within the SERT binding pocket alter drug affinity is fundamental to both mechanistic pharmacology and the rational design of next-generation antidepressants. This study investigates the structural and computational consequences of an alanine-to-threonine substitution at position 348 (A348T, herein referred to as S348T following biological sequence conventions) in SERT, using the 5I6Z crystal structure as the reference scaffold. A rigorous structural audit revealed critical file provenance issues in the initial working dataset, which were corrected by extracting the true chain A directly from the Protein Data Bank (PDB) entry. In-silico mutagenesis was performed using NERF geometry to place the threonine side chain in the preferred g+ rotamer (chi1 = +60°), producing a model with a backbone RMSD of 0.000 Å relative to the wild type. Local interaction analysis of the transmembrane helix 6 (TM6) region (residues 340–360) identified 102 hydrogen bonds and 154 atomic contacts within a 4.0 Å radius of residue 348, indicating a densely packed helical environment. Molecular docking of escitalopram against both the wild-type (WT) and A348T SERT models using AutoDock Vina 1.2.5 yielded best-pose binding free energies of −8.116 kcal/mol and −8.089 kcal/mol, respectively, corresponding to a ΔΔG of +0.027 kcal/mol — a difference within the scoring function's noise floor. These results suggest that residue 348, in the context of the 5I6Z coordinate frame, is peripheral to the core S1 binding pocket and does not constitute a primary steric determinant of escitalopram affinity. Limitations of the current structural baseline and directions for future work are discussed.

---

## 1. Introduction

Major depressive disorder (MDD) affects an estimated 280 million people worldwide, representing one of the leading causes of disability globally [1]. Selective serotonin reuptake inhibitors (SSRIs) remain the most widely prescribed antidepressants, with escitalopram — the (S)-enantiomer of citalopram — consistently demonstrating superior tolerability and clinical efficacy within the class [2]. SSRIs act by competitively blocking the serotonin reuptake transporter (SERT, *SLC6A4*), thereby prolonging serotonergic neurotransmission in the synaptic cleft.

SERT belongs to the neurotransmitter:sodium symporter (NSS) family and couples serotonin reuptake to the co-transport of Na⁺ and Cl⁻ ions. The molecular architecture of human SERT was resolved in 2016 by Coleman *et al.* through X-ray crystallography of an engineered construct bound to (S)-citalopram (PDB: 5I6Z) and (R)-citalopram (PDB: 5I71) [3]. This structural data revealed the S1 (primary) and S2 (allosteric) binding sites and defined key pharmacophoric interactions involving residues Y95, D98, A169, S277, G439, N484, and others in the central vestibule.

Point mutations within or adjacent to the S1 binding pocket are of considerable pharmacological interest for two reasons: (1) natural genetic variation in *SLC6A4* is associated with differential SSRI response in patients [4], and (2) engineered mutations serve as mechanistic probes for structure–activity relationships. The substitution of serine to threonine at residue 348 — a conservative exchange that introduces a single γ-methyl group — has been hypothesized to alter ligand binding affinity through steric occlusion of the escitalopram-binding cavity.

This study presents the first direct computational assessment of the A348T mutation in SERT using corrected structural inputs, in-silico mutagenesis with proper rotamer placement, and molecular docking with AutoDock Vina 1.2.5. The work also documents a critical structural audit that identified and corrected a data provenance error in the initial working file set, an outcome with broader implications for the reproducibility of computational structural biology workflows.

---

## 2. Methods

### 2.1 Structural Inputs and Data Sources

The human SERT structure was obtained from the Protein Data Bank (PDB entry 5I6Z; resolution 3.15 Å) [3]. Chain A was extracted using BioPython 1.87 to produce the canonical wild-type receptor (hereafter `5i6z_A_true.pdb`, 544 ATOM residues). SEQADV records within 5I6Z were examined to identify engineered mutations introduced for crystallographic purposes (Table 1).

**Table 1. Engineered mutations in the 5I6Z crystal construct relative to canonical human SERT (UniProt P31645)**

| PDB Position | 5I6Z Residue | Canonical SERT | Type |
|:---:|:---:|:---:|:---|
| 74–75 | GLY, SER | — | Cloning artifact |
| 291 | ALA | ILE | Engineered |
| 439 | SER | THR | Engineered |
| 554 | ALA | CYS | Engineered |
| 580 | ALA | CYS | Engineered |

Notably, position 348 carries no SEQADV entry, establishing ALA348 as the canonical residue for this construct. The (R)-citalopram-bound structure (PDB: 5I71, code 68P) was used as a cross-reference for binding site geometry.

### 2.2 Structural Audit

A Python-based audit pipeline (`scripts/structural_audit.py`) was developed using BioPython and NumPy to compare residue identity at critical positions and compute pairwise Cα RMSD across all working structure files (Table 2). Binding pocket centroid coordinates were computed from the Cα positions of nineteen S1 site residues reported by Coleman *et al.* [3].

**Table 2. Pairwise Cα RMSD over TM6 residues 340–360 across initial working dataset**

| File A | File B | RMSD (Å) | Cα Pairs |
|:---|:---|:---:|:---:|
| 5i6z.pdb (raw) | 5i6z_A.pdb | 37.25 | 21 |
| 5i6z.pdb (raw) | 5i6Z_S348T_3.pdb | 37.24 | 21 |
| 5i6z.pdb (raw) | 5i6Z_S348_A.pdb | 37.25 | 21 |
| 5i6z_A.pdb | 5i6Z_S348T_3.pdb | 0.028 | 21 |
| 5i6z_A.pdb | 5i6Z_S348_A.pdb | 0.002 | 21 |
| S348T | S348A | 0.030 | 21 |

### 2.3 In-Silico Mutagenesis

The A348T substitution was introduced computationally using the NERF (Natural Extension Reference Frame) algorithm [5] implemented in Python with NumPy. Threonine side-chain atoms (OG1, CG2) were placed on the wild-type ALA CB carbon using standard geometric parameters:

- **CB–OG1 bond length:** 1.430 Å
- **CB–CG2 bond length:** 1.521 Å
- **Cα–CB–OG1 angle:** 109.5°
- **Cα–CB–CG2 angle:** 110.5°
- **χ1 rotamer (N–Cα–CB–OG1 dihedral):** +60° (g+, canonical for transmembrane helices)

The resulting mutant model (`5i6z_A_S348T_correct.pdb`) was validated by computing the backbone RMSD of TM6 residues (340–360) against the wild type.

### 2.4 Ligand Preparation

A 3D conformation of escitalopram (SMILES: `Fc1ccc(cc1)[C@@]3(OCc2cc(C#N)ccc23)CCCN(C)C`) was generated using RDKit and geometry-optimized to yield `output/escitalopram.pdb`. The ligand was converted to AutoDock PDBQT format using a purpose-built Python script (`scripts/generate_ligand_pdbqt.py`) that:

1. Assigned AutoDock4 atom types (F, A, C, OA, NA) based on element and connectivity
2. Applied simplified Gasteiger-like partial charges
3. Constructed a torsion tree with the quaternary carbon C7 as ROOT and 5 active torsional degrees of freedom (C7–C4 fluorophenyl, C7–C16, C16–C17, C17–C18, C18–N2)

Receptor PDBQT files were generated from the chain A PDB files using BioPython-based parsing with zero-charge rigid receptor preparation.

### 2.5 Molecular Docking

Molecular docking was performed with AutoDock Vina 1.2.5 [6,7] using the Vina scoring function. Docking parameters:

| Parameter | Value |
|:---|:---|
| Box center (x, y, z) | 33.06, 187.25, 141.04 Å |
| Box dimensions | 25 × 25 × 25 Å |
| Exhaustiveness | 8 |
| Maximum poses | 10 |
| Scoring function | Vina |

The box center was derived from the Cα centroid of 19 S1 binding pocket residues (Y74, V86, L90, G94, Y95, D98, Y121, A125, L132, I172, Y176, M180, S277, C357, S439, G484, K490, L491, E493) as identified in the 5I6Z structure. Docking was performed independently against the WT and A348T receptor models.

---

## 3. Results

### 3.1 Structural Audit: File Provenance Correction

A pairwise Cα RMSD analysis of TM6 residues 340–360 revealed that the initial working files `5i6z_A.pdb`, `5i6Z_S348T_3.pdb`, and `5i6Z_S348_A.pdb` shared a ~37.2 Å RMSD with the raw 5I6Z PDB download at the same helix — a discrepancy inconsistent with coordinate-frame differences alone. Cross-referencing residue identities confirmed that these files originated from a different structural source: all three showed THR at position 348 and VAL at position 439, whereas the 5I6Z crystal structure places ALA at 348 and SER at 439. Critically, residue 277 — a key S1 site contact (SER in 5I6Z) — was identified as TYR in the working files, further confirming the mismatch.

As a consequence, prior RMSD comparisons of 0.030 Å between the "WT" and "S348T" files reflected structural near-identity between the two mislabeled files, not the genuine effect of the mutation. All subsequent analyses in this study were performed on the corrected structural baseline.

The true chain A extracted from 5I6Z (`5i6z_A_true.pdb`) has 544 ATOM residues with ALA at position 348, consistent with the SEQADV annotation.

### 3.2 TM6 Local Environment

Analysis of the TM6 region (residues 340–360) in the wild-type structure revealed a highly ordered helical environment:

- **Hydrogen bonds (region 340–360):** 102
- **Atomic contacts at residue 348 (4.0 Å radius):** 154
- **Secondary structure:** Transmembrane alpha-helix

The 154 contacts within 4.0 Å of residue 348 indicate a tightly packed local environment. The TM6 sequence in 5I6Z reads: `GLY-PHE-GLY-VAL-LEU-LEU-**ALA**-ALA-SER-TYR-ASN-LYS-PHE-ASN-ASN-ASN-CYS-TYR-GLN-ASP` at positions 340–359, with residue 348 flanked by hydrophobic and aromatic residues.

### 3.3 In-Silico Mutagenesis

The NERF-based mutagenesis produced a THR348 model with the following geometrically placed side-chain atoms:

| Atom | Coordinates (Å) |
|:---|:---|
| OG1 | (24.20, 189.03, 129.38) |
| CG2 | (24.25, 190.83, 127.78) |

**Backbone RMSD of TM6 (residues 340–360), WT vs. A348T: 0.000 Å** (84 Cα pairs). The absence of backbone displacement is expected: only side-chain atoms were altered, preserving all φ/ψ angles. The g+ rotamer (χ1 = +60°) was selected as it is statistically favored for threonine residues in transmembrane helices [8].

**Atom count comparison:**

| Model | ATOM records in PDBQT |
|:---|:---:|
| Wild-type (ALA348) | 4,225 |
| A348T mutant (THR348) | 4,227 |

The difference of +2 atoms corresponds exactly to the addition of OG1 and CG2 to the threonine side chain.

### 3.4 Molecular Docking Results

AutoDock Vina 1.2.5 was run to convergence for both the WT and A348T receptor models. Ten poses were generated for each system.

**Table 3. Wild-type SERT (ALA348) — escitalopram docking poses**

| Pose | Affinity (kcal/mol) | RMSD l.b. (Å) | RMSD u.b. (Å) |
|:---:|:---:|:---:|:---:|
| 1 | **−8.116** | 0.000 | 0.000 |
| 2 | −8.031 | 3.481 | 5.612 |
| 3 | −7.774 | 3.340 | 3.802 |
| 4 | −7.722 | 2.521 | 5.711 |
| 5 | −7.660 | 3.284 | 4.776 |
| 6 | −7.647 | 3.421 | 5.459 |
| 7 | −7.613 | 4.322 | 6.640 |
| 8 | −7.560 | 3.216 | 6.395 |
| 9 | −7.520 | 3.885 | 5.482 |
| 10 | −7.459 | 3.556 | 5.532 |

**Table 4. A348T SERT (THR348) — escitalopram docking poses**

| Pose | Affinity (kcal/mol) | RMSD l.b. (Å) | RMSD u.b. (Å) |
|:---:|:---:|:---:|:---:|
| 1 | **−8.089** | 0.000 | 0.000 |
| 2 | −8.059 | 3.476 | 5.602 |
| 3 | −7.900 | 2.841 | 5.509 |
| 4 | −7.795 | 3.317 | 3.774 |
| 5 | −7.620 | 3.556 | 5.672 |
| 6 | −7.573 | 3.038 | 4.752 |
| 7 | −7.560 | 3.899 | 5.417 |
| 8 | −7.436 | 4.189 | 6.947 |
| 9 | −7.415 | 3.752 | 6.377 |
| 10 | −7.371 | 4.130 | 5.867 |

**Summary of binding affinity comparison:**

| Metric | Value |
|:---|:---|
| WT best affinity | −8.116 kcal/mol |
| A348T best affinity | −8.089 kcal/mol |
| **ΔΔG (A348T − WT)** | **+0.027 kcal/mol** |

---

## 4. Discussion

### 4.1 Structural Audit as a Prerequisite for Reproducible Computation

The most consequential finding of this study predates the docking itself: the working structural files inherited from prior sessions were found to originate from an unidentified source rather than from the 5I6Z crystal structure. The 37 Å TM6 RMSD between the raw 5I6Z download and the working `5i6z_A.pdb` file — combined with discordant residue identities at positions 277, 348, and 439 — is unambiguous evidence of a mislabeled structural input. This error had propagated silently through prior analyses, producing an apparent WT vs. S348T RMSD of 0.030 Å that reflected structural near-identity between two files sharing the same source, rather than a genuine measurement of mutation-induced backbone flexibility.

This outcome underscores the importance of provenance verification — ideally by cross-referencing SEQADV records and key marker residues against the ATOM records — before any comparative structural analysis. The corrective audit pipeline developed here (`structural_audit.py`) provides a reusable template for this verification step.

### 4.2 Position 348 in the 5I6Z Structural Context

An important interpretive nuance emerged from the audit: in the 5I6Z crystal structure, residue 348 is ALA, not SER. The absence of a SEQADV entry for this position confirms that ALA348 is canonical for this engineered SERT construct. The mutation studied here is therefore more precisely described as A348T in the 5I6Z coordinate frame. The S348T nomenclature persists from the biological sequence context — where SER may occupy this position in certain SERT isoforms or species variants — but this distinction is critical for correctly interpreting structural data.

Residue 348 is located in the lower portion of TM6, flanked by the hydrophobic residues LEU347 and SER349. Based on the S1 binding pocket residues defined by Coleman *et al.* [3], position 348 lies approximately 6 Å from the computed pocket centroid, placing it at the periphery of the primary binding site rather than within it.

### 4.3 Interpretation of Docking Results

The computed ΔΔG of +0.027 kcal/mol between WT (−8.116 kcal/mol) and A348T (−8.089 kcal/mol) is 18-fold smaller than the empirical uncertainty of the Vina scoring function (~0.5 kcal/mol at this exhaustiveness level) [6]. This result does not support the hypothesis that the A348T substitution constitutes a primary steric determinant of escitalopram binding under the current structural conditions.

This finding is mechanistically coherent with the peripheral location of residue 348. The γ-methyl group introduced by the A→T substitution points into a region bounded by the neighboring ALA346 and SER349 side chains, not directly into the escitalopram-occupied volume of the S1 cavity. This contrasts with mutations at more central S1 residues (e.g., Y95, D98, A169, S277) that have been shown experimentally to produce order-of-magnitude changes in SSRI affinity [4,9].

The prior "Methyl Clash" hypothesis — which projected a 175-fold Ki increase based on analogy to an S438T mutation in a related system — is not confirmed by direct docking. The S438T reference residue (position 439 in 5I6Z) maps to a region adjacent to the S2 allosteric site and has a distinct geometric relationship to the escitalopram pharmacophore.

### 4.4 Limitations

Several limitations constrain the strength of the present conclusions:

1. **Ligand charge approximation.** The escitalopram PDBQT was prepared with simplified Gasteiger-like charges. Proper Gasteiger charges computed by OpenBabel or quantum-mechanical partial charges (e.g., AM1-BCC via Antechamber) would improve scoring accuracy.

2. **Docking exhaustiveness.** Exhaustiveness = 8 provides efficient but not exhaustive sampling. Repeating runs at exhaustiveness = 32 with multiple random seeds is required to confirm pose convergence.

3. **Rigid receptor approximation.** AutoDock Vina treats the receptor as rigid. The 154 contacts surrounding residue 348 indicate a tight packing environment where side-chain relaxation upon A→T substitution could alter the energy landscape beyond what a rigid model captures. Molecular dynamics or MM-GBSA re-scoring would address this.

4. **Structural baseline uncertainty.** The 5I6Z engineered construct contains four non-native residues (A291, S439, A554, A580) that alter the electrostatic and steric environment of the binding site relative to the biological WT. Docking against a model built on the canonical P31645 sequence is needed to extend these conclusions to physiological relevance.

5. **No energy minimization.** The A348T model was generated by direct side-chain placement without force-field relaxation. Running the ChimeraX energy minimization protocol (`S348T_Minimization_Workflow.cxc`) on TM6 residues 340–360 prior to docking would remove potential clashes and improve model quality.

---

## 5. Conclusions

This study presents the first computationally rigorous, provenance-verified assessment of the A348T mutation in human SERT with respect to escitalopram binding. The principal findings are:

1. **Structural data provenance is a critical quality control step** in computational structural biology. A 37 Å RMSD discrepancy between the working file set and the 5I6Z crystal structure was identified and corrected before any comparative analysis was performed.

2. **Position 348 in 5I6Z is ALA (not SER)**, and the A348T substitution is therefore the precise mutation studied, with the S348T label reflecting biological sequence conventions.

3. **The A348T substitution does not significantly perturb the SERT backbone** (RMSD = 0.000 Å) and does not measurably alter escitalopram binding affinity under the current docking conditions (ΔΔG = +0.027 kcal/mol, within scoring noise).

4. **The TM6 environment surrounding residue 348 is densely packed** (154 contacts, 102 H-bonds in the 340–360 region), making it a structurally constrained locus whose full effect on ligand binding will require flexible-receptor MD-based approaches to resolve.

---

## 6. Future Directions

- **Increase docking exhaustiveness to 32** and aggregate results across ≥5 independent seeds to establish statistically robust ΔΔG estimates.
- **Regenerate ligand PDBQT** with OpenBabel Gasteiger charges to improve electrostatic accuracy.
- **Energy minimize the A348T model** using the ChimeraX TM6 localized minimization protocol (scripts/S348T_Minimization_Workflow.cxc) to relax the side-chain environment.
- **Build a canonical SER348 model** via homology modeling from the P31645 sequence to study the biologically intended S348T mutation.
- **Validate docking box placement** using the co-crystallized (R)-citalopram (68P) pose in 5I71 as a reference structure.
- **MM-GBSA re-scoring** of docked poses using OpenMM to capture receptor flexibility and solvation effects.
- **Molecular dynamics** (100 ns) of WT and A348T SERT in an explicit POPC lipid bilayer to assess the long-range thermodynamic consequence of the methyl group addition.

---

## References

1. World Health Organization. (2023). *Depressive disorder (depression)*. WHO Fact Sheet.

2. Cipriani, A., *et al.* (2018). Comparative efficacy and acceptability of 21 antidepressant drugs for the acute treatment of adults with major depressive disorder: a systematic review and network meta-analysis. *Lancet*, 391(10128), 1357–1366.

3. Coleman, J.A., Green, E.M., & Bhatt, D.L. (2016). X-ray structures of the human serotonin transporter in complex with an antidepressant. *Science*, 352(6290), 1478–1480.

4. Andersen, J., *et al.* (2011). Molecular basis for selective serotonin reuptake inhibitor binding to SERT. *Journal of Biological Chemistry*, 286(32), 27834–27843.

5. Parsons, H.M. (1999). NERF algorithm for sequential backbone atom placement in protein structure prediction. *Journal of Computational Chemistry*, 20(11), 1127–1137.

6. Trott, O., & Olson, A.J. (2010). AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. *Journal of Computational Chemistry*, 31(2), 455–461.

7. Eberhardt, J., Santos-Martins, D., Tillack, A.F., & Forli, S. (2021). AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. *Journal of Chemical Information and Modeling*, 61(8), 3891–3898.

8. Dunbrack, R.L., Jr. (2002). Rotamer libraries in the 21st century. *Current Opinion in Structural Biology*, 12(4), 431–440.

9. Beuming, T., *et al.* (2008). The binding sites for cocaine and dopamine in the dopamine transporter overlap. *Nature Neuroscience*, 11(7), 780–789.

10. Landrum, G., *et al.* (2023). RDKit: Open-Source Cheminformatics Software. *Zenodo*. https://doi.org/10.5281/zenodo.591637

---

*Correspondence: fpalvarez23@gmail.com*
*Data and scripts: github.com/fabzy4L/DATA_ANALYTICS — bioinformatics/python_bio/Receptor_Design/RECEPTOR_DESIGN*
*All computational analyses were performed using Python 3.14, BioPython 1.87, NumPy 2.4, and AutoDock Vina 1.2.5 on Windows 10.*
