# Numerical Comparison: Computational Results vs. Experimental Literature

This document provides a direct comparison between the experimental binding values reported in scientific literature and the computational results generated in this project by **Fabian A. Alvarez-Primo, Ph.D.**

## 1. Experimental Literature Values (Inhibition Constant, $K_i$)
In experimental pharmacology, the **Inhibition Constant ($K_i$)** measures how much ligand is needed to occupy 50% of receptors. **Lower $K_i$ values indicate higher binding affinity.**

| Source | $\Delta^9$-THC ($K_i$) | $\Delta^8$-THC ($K_i$) | Observation |
| :--- | :--- | :--- | :--- |
| **Tagen et al. (2022)** | **~25 nM** | **~165 nM** | $\Delta^9$ binds tighter |
| **Hua et al. (2016)** | **40.7 ± 1.7 nM** | **47.6 ± 1.9 nM** | $\Delta^9$ binds tighter |

*Literature Consensus:* Experimental studies consistently show that **$\Delta^9$-THC has a higher binding affinity** for the CB1 receptor than its $\Delta^8$ isomer.

## 2. Project Computational Results (Gibbs Free Energy, $\Delta G$)
In computational docking, the score represents the predicted **Gibbs Free Energy ($\Delta G$)** of binding. **More negative values indicate higher binding affinity.**

| Ligand | Predicted Affinity ($\Delta G$) | Result |
| :--- | :--- | :--- |
| **$\Delta^8$-Tetrahydrocannabinol** | **-6.5 kcal/mol** | Predicted tighter binder |
| **$\Delta^9$-Tetrahydrocannabinol** | **-6.3 kcal/mol** | Predicted weaker binder |

*Project Consensus:* The *in silico* simulation predicts that **$\Delta^8$-THC has a slightly higher binding affinity** than $\Delta^9$-THC.

---

## 3. Comparative Analysis & Discussion

### **The "Inversion of Preference"**
There is a notable divergence between the computational predictions of this project and the experimental data found in the literature. While the literature favors $\Delta^9$-THC, the docking algorithm (AutoDock Vina) favors $\Delta^8$-THC by a margin of **0.2 kcal/mol**.

### **Scientific Rationale**
1.  **Static vs. Dynamic Environments:** The docking simulation utilized a static crystal structure of the human CB1 receptor (PDB: **5TGZ**). In this "frozen" state, the geometric configuration of the $\Delta^8$ double bond allows for marginally optimized van der Waals contacts within the specific hydrophobic pocket residues.
2.  **Entropic Effects:** Experimental $K_i$ values are measured in living cell membranes where receptor flexibility, lipid interactions, and desolvation (the displacement of water molecules) play significant roles. These dynamic entropic factors often favor $\Delta^9$-THC in a way that static docking cannot capture.
3.  **Induced Fit:** The experimental literature suggests that $\Delta^9$-THC may induce a specific conformational change in the receptor that leads to tighter binding. Docking assumes a "lock and key" mechanism with a rigid receptor, which can lead to the subtle inversion of results observed here.

### **Conclusion**
Dr. Alvarez-Primo's results successfully identify both molecules as thermodynamically favorable binders within the expected range for cannabinoids. The discrepancy between the computational preference for $\Delta^8$ and the experimental preference for $\Delta^9$ serves as a valuable case study in the limitations of static molecular docking and underscores the necessity of following up with **Molecular Dynamics (MD) simulations** to observe the interaction over time in a flexible, solvated environment.
