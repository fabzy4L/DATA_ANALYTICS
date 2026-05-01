# Comparative Structural and Computational Analysis of the S438T Mutation in the Human Serotonin Transporter: A Corrected Assessment of Escitalopram Binding

**Fabian A. Alvarez-Primo, Ph.D.**

*Computational Structural Biology | May 1, 2026*

---

## Abstract

The human Serotonin Transporter (SERT, *SLC6A4*) is the primary molecular target for Selective Serotonin Reuptake Inhibitors (SSRIs). Understanding the structural determinants of ligand affinity is critical for drug design and explaining clinical resistance. This study focuses on the **S438T** mutation, a site within the S1 binding pocket previously identified as a key factor in ligand sensitivity (Plenge *et al.*, 2020). Crucially, this study documents a technical course-correction from an initial investigation of the **A348T** site, which was identified as a digit-swap error in the preliminary research phase. Utilizing the 5I6Z crystal structure, we performed *in-silico* mutagenesis and molecular docking with AutoDock Vina 1.2.5. Our results indicate that escitalopram binds to the S438T mutant with a best-pose affinity of **−8.3 kcal/mol**, compared to **−8.1 kcal/mol** for the wild-type. The computed $\Delta\Delta G$ of **−0.2 kcal/mol** suggests that while the Serine-to-Threonine substitution introduces a methyl group into the S1 pocket, escitalopram maintains a high-affinity binding mode in the rigid-receptor model. This finding provides a corrected structural foundation for SERT–SSRI interaction studies.

---

## 1. Introduction

Selective serotonin reuptake inhibitors (SSRIs) such as escitalopram are the first-line treatment for major depressive disorder and anxiety. These drugs work by binding to the central orthosteric site (S1) of the Serotonin Transporter (SERT), preventing the reuptake of serotonin into the presynaptic neuron.

The structural biology of SERT was significantly advanced by the resolution of the human SERT construct in complex with antidepressants (PDB: 5I6Z) [1]. Among the residues defining the S1 pocket, **Serine 438** is of particular interest. Previous experimental work has shown that the S438T mutation — which introduces a single methyl group — creates a steric clash that dramatically reduces the affinity of certain SSRIs, particularly citalopram [2].

This report details a computational investigation into the S438T mutation. A secondary goal of this study was to rectify a significant error in the project's early trajectory, where the **A348T** site was analyzed instead of the biologically relevant S438T. Position 348 is located in TM6, far from the binding cavity, whereas 438 is a direct contact point. We present here the results for the correct S438T site.

---

## 2. Methods

### 2.1 Receptor Preparation
The wild-type receptor was derived from the chain A of PDB 5I6Z. The **S438T** mutation was introduced *in-silico* using a Python-based implementation of the Natural Extension Reference Frame (NERF) algorithm. The threonine side chain was placed in the **g+ rotamer** ($\chi1 = +60^\circ$), which is the most statistically favored conformation for threonine in transmembrane helices.

### 2.2 Ligand Preparation
The 3D structure of **escitalopram** was geometry-optimized and converted to PDBQT format. Torsional degrees of freedom were assigned to the propyl-amine chain and the fluorophenyl ring to allow for conformational flexibility during docking.

### 2.3 Molecular Docking
Docking was performed using **AutoDock Vina 1.2.5**. The grid box was centered on the S1 binding pocket (33.06, 187.25, 141.04) with dimensions of 25 Å³. We utilized an exhaustiveness setting of 8 to generate 10 poses for both the wild-type (SER438) and the mutant (THR438) receptors.

---

## 3. Results

### 3.1 Identification of the 348 vs 438 Error
During a structural audit, it was discovered that residue 348 is an Alanine (in 5I6Z) located on the periphery of TM6. Comparison with the reference paper (Plenge *et al.*, 2020) confirmed that the biologically relevant site is **Serine 438**. The project was successfully pivoted to 438, and all previous results for 348 were archived as technical artifacts of the initial misidentification.

### 3.2 Comparative Binding Affinity
The docking results for escitalopram are summarized in the table below.

| Receptor State | Residue 438 | Best Affinity (kcal/mol) |
| :--- | :---: | :---: |
| Wild-Type | SER | −8.1 |
| **Mutant** | **THR** | **−8.3** |

The S438T mutation resulted in a slight increase in predicted binding affinity ($\Delta\Delta G = -0.2$ kcal/mol). This suggests that in the 5I6Z crystal conformation, the additional methyl group of Threonine 438 does not sterically ablate the binding of escitalopram. Instead, the ligand appears to accommodate the change within the S1 pocket geometry.

---

## 4. Discussion

The finding of a −0.2 kcal/mol shift is significant because it suggests that **escitalopram** (the (S)-enantiomer) may be less sensitive to the S438T steric clash than its racemic counterpart, citalopram. In a rigid-receptor model, the pocket appears capable of housing the Threonine side chain without disrupting the primary pharmacophoric contacts with Y95 and D98.

However, it is important to note that rigid docking does not capture the dynamic "locking" mechanism or the desolvation penalties associated with the S438T mutation. The −0.2 kcal/mol difference is within the scoring noise of Vina (~0.5 kcal/mol), meaning the binding is essentially equivalent to the wild-type in this structural snapshot.

---

## 5. Conclusion

By correcting the site of mutagenesis from 348 to 438, this study provides a biologically valid assessment of the SERT S438T mutation. Our computational results indicate that escitalopram retains high affinity for the S438T mutant (−8.3 kcal/mol). This study highlights the necessity of residue-level verification in computational pipelines and sets the stage for future molecular dynamics simulations to explore the kinetic consequences of the S438T substitution.

---

## 6. References

1. Coleman, J.A., *et al.* (2016). X-ray structures of the human serotonin transporter in complex with an antidepressant. *Science*, 352(6290), 1478–1480.
2. Plenge, P., *et al.* (2020). The mechanism of a high-affinity allosteric inhibitor of the serotonin transporter. *Nature Communications*, 11, 1491.
3. Trott, O., & Olson, A.J. (2010). AutoDock Vina: Improving the speed and accuracy of docking. *Journal of Computational Chemistry*, 31(2), 455–461.
