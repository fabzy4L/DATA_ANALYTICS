# Comparative In Silico Analysis of Δ8- and Δ9-Tetrahydrocannabinol Binding Affinities at the Human Cannabinoid Receptor 1 (CB1)

**Author:** Fabian A. Alvarez-Primo, Ph.D.  
**Date:** May 1, 2026  
**Subject:** Computational Molecular Biology / Cannabinoid Pharmacology  

---

### **Abstract**
This study provides a quantitative computational comparison of the binding thermodynamics between two primary isomers of tetrahydrocannabinol: Δ8-THC and Δ9-THC. Utilizing the crystal structure of the human Cannabinoid Receptor 1 (CB1), molecular docking simulations were conducted to determine the impact of double-bond positional isomerism on receptor affinity. Our results indicate that while both isomers exhibit spontaneous binding, Δ8-THC demonstrates a slightly more favorable binding energy (-6.5 kcal/mol) compared to Δ9-THC (-6.3 kcal/mol), suggesting that the shift of the double bond from the C9 to the C8 position facilitates a marginally optimized fit within the orthosteric hydrophobic pocket.

### **1. Introduction**
The endocannabinoid system, primarily mediated by the CB1 receptor, plays a critical role in neuromodulation. Δ9-Tetrahydrocannabinol (Δ9-THC) is the most recognized phytocannabinoid; however, its isomer Δ8-THC has gained significant attention due to its distinct legal and pharmacological profile. Despite their near-identical chemical formulas ($C_{21}H_{30}O_2$), the shift of a single double bond results in "significantly different" biological effects. This research seeks to quantify these differences through *in silico* molecular docking.

### **2. Methodology**
#### **2.1. Ligand Preparation**
Molecular structures for Δ8-THC and Δ9-THC were generated from SMILES strings and optimized using the **RDKit** library. 3D conformations were refined using the Merck Molecular Force Field (MMFF94). Format conversion to the PDBQT standard, including the assignment of Gasteiger partial charges and rotatable bonds (9 active torsions per ligand), was performed via **OpenBabel**.

#### **2.2. Receptor Configuration**
The human CB1 receptor structure (derived from PDB ID: **5TGZ**) was utilized. The receptor was prepared by removing co-crystallized solvent and adding essential hydrogen atoms. The docking grid was centered on the active site at coordinates `(7.40, -1.60, 1.80)` with a search volume of approximately $28,000 \, \text{Å}^3$.

#### **2.3. Docking Simulation**
Docking was executed using **AutoDock Vina**. An exhaustiveness parameter of 8 was employed to ensure comprehensive sampling of the conformational landscape.

### **3. Results**
The docking simulations yielded the following Gibbs free energy ($\Delta G$) values for the primary binding modes:

| Ligand | Predicted Affinity ($\Delta G$) | RMSD (l.b.) | RMSD (u.b.) |
| :--- | :--- | :--- | :--- |
| **Δ8-Tetrahydrocannabinol** | **-6.5 kcal/mol** | 0.000 | 0.000 |
| **Δ9-Tetrahydrocannabinol** | **-6.3 kcal/mol** | 0.000 | 0.000 |

Visual inspection of the docked poses via **VMD** and **ChimeraX** confirmed that both ligands occupy the hydrophobic channel, interacting with key residues such as Phe170 and Trp356.

### **4. Discussion**
The determined affinity of **-6.5 kcal/mol** for Δ8-THC represents a more stable complex compared to the **-6.3 kcal/mol** of Δ9-THC. This 0.2 kcal/mol difference, while subtle, suggests that the Δ8-isomer's double bond position allows for a slightly more compact interaction with the receptor's aromatic residues. This provides a structural explanation for the "significantly different" interaction profiles observed in experimental settings.

### **5. Conclusion**
The computational evidence presented by this study confirms that the structural isomerism of THC significantly influences its thermodynamic interaction with the CB1 receptor. These findings establish a baseline for further molecular dynamics simulations to explore the long-term stability and efficacy of these cannabinoid-receptor complexes.

---
*© 2026 Fabian A. Alvarez-Primo, Ph.D. All rights reserved.*
