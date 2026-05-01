# Project Summary: Binding Affinity & Molecular Docking with Python

This project is a bioinformatics workflow focused on simulating the interaction between ligands and protein receptors to predict binding affinities, specifically targeting the **Cannabinoid Receptor 1 (CB1)**.

## Project Overview
The workflow integrates industry-standard tools for drug discovery:
- **AutoDock Vina**: Molecular docking simulation engine.
- **RDKit**: 3D molecular structure generation from SMILES/MOL.
- **OpenBabel**: Chemical format conversion (PDB to PDBQT).
- **VMD**: 3D visualization of docked complexes.

## Workflow Execution
1. **Preparation**: Ligands were converted to 3D PDB via RDKit and then to PDBQT via OpenBabel.
2. **Configuration**: Docking was set with a search grid centered at `(7.40, -1.60, 1.80)` with dimensions `26.48 x 38.15 x 27.90 Å`.
3. **Simulation**: Automated via `autodockvina.py` with an exhaustiveness of 8.

## Key Results
The simulations predicted stable binding interactions for the ligands within the CB1 receptor:
- **Best Affinity (Run 1)**: `-6.5 kcal/mol`
- **Best Affinity (Run 2)**: `-6.3 kcal/mol`

## Project Structure
- `scripts/`: Python automation for the pipeline.
- `structures/`: Repository of ligands, receptors (e.g., 5TGZ, 5U09), and complexes.
- `notebooks/`: Interactive molecular preparation.
- `visualization/`: VMD state files and rendered images (e.g., `5tgz.png`).
