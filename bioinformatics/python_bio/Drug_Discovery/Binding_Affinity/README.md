# Binding Affinity & Molecular Docking with Python

This project provides a comprehensive workflow for molecular docking simulations and binding affinity analysis. It utilizes standard bioinformatics tools such as **AutoDock Vina**, **RDKit**, and **OpenBabel** to prepare structures and perform docking.

## Project Structure

- **`data/`**: Contains tabular data related to binding affinities (e.g., `Binding Affinities.csv`).
- **`docking/`**:
  - `config/`: Configuration files for AutoDock Vina runs (e.g., `Config.txt`, `dockingoutput.conf`).
  - `logs/`: Output logs from docking simulations.
  - `outputs/`: Resulting PDBQT files from docking runs.
- **`literature/`**: Supporting research papers and tool documentation.
- **`notebooks/`**: Jupyter notebooks for interactive molecular preparation and analysis:
  - `SMILESTOPDB_RDKIT.ipynb`: Converting SMILES strings to 3D PDB structures.
  - `PDBTOPBDQT_OPENBABEL.ipynb`: Converting PDB files to PDBQT format for docking.
- **`scripts/`**: Python scripts for automating the workflow:
  - `autodockvina.py`: Executes the AutoDock Vina docking process.
  - `openbabelpdbqt.py`: Automates format conversion using OpenBabel.
  - `rdkitconverter.py`: Handles molecule conversion using RDKit.
  - `RDKITSMILES.py`: Processes SMILES strings into structures.
- **`setup/`**: Documentation and instructions for environment setup (Python 3.7, pyenv, VMD).
- **`structures/`**:
  - `receptor/`: Receptor PDB/PDBQT files (e.g., CB1 receptor).
  - `ligands/`: Ligand PDB/PDBQT files (e.g., THC derivatives).
  - `complexes/`: Final docked ligand-receptor complexes.
- **`tools/`**: Executables for AutoDock Vina.
- **`visualization/`**: VMD (Visual Molecular Dynamics) state files and rendered images.

## Requirements

The project is designed to run in a Python 3.7 environment. Key dependencies include:

- **AutoDock Vina**: For performing the docking simulations.
- **OpenBabel**: For molecular format conversion (PDB to PDBQT).
- **RDKit**: For generating 3D structures from SMILES or MOL files.
- **VMD**: For visualization of docking results.

## Workflow

1.  **Preparation**:
    - Use `scripts/rdkitconverter.py` or the RDKit notebooks to convert ligand data (SMILES/MOL) into 3D PDB format.
    - Use `scripts/openbabelpdbqt.py` to convert PDB files of both ligands and receptors into the PDBQT format required by Vina.
2.  **Configuration**:
    - Define the search box and docking parameters in `docking/config/Config.txt`.
3.  **Docking**:
    - Run the docking simulation using `scripts/autodockvina.py`. This script calls the Vina executable with the specified configuration.
4.  **Analysis & Visualization**:
    - Review the logs in `docking/logs/`.
    - Visualize the docked poses in `docking/outputs/` using VMD, referencing the state files in `visualization/`.

## Setup Instructions

Refer to the `setup/` directory for detailed environment setup guides:
- `Install_py37.txt`: Instructions for installing Python 3.7 on macOS.
- `Py3_7_Env.txt`: Details on setting up the specific Python environment.
- `VMD Protein Modification Visualization.txt`: Guide for using VMD with this workflow.
