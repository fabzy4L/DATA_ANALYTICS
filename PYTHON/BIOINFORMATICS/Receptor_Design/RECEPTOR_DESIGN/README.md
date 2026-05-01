# Serotonin Receptor (SERT) Design and Analysis

This project focuses on the 3D modeling, sequence analysis, and structural investigation of serotonin transporters (SERT), specifically exploring their interactions with antidepressant ligands such as Escitalopram.

## Overview

The repository contains raw structural data, computational biology scripts, and literature aimed at understanding SERT mutations and ligand binding modes. Key structural references include PDB IDs `5I6Z`, `5I71`, and `2A65`.

## Proposed Project Structure

To improve maintainability, the project is organized into the following directories:

- **`data/`**: Contains raw structural and sequence files.
  - **`structures/`**: Protein Data Bank (`.pdb`, `.cif`) and ChimeraX session (`.cxs`) files used for visualization.
  - **`sequences/`**: FASTA formatted protein sequences (e.g., wild-type and edited sequences).
- **`notebooks/`**: Jupyter Notebooks containing Python analysis pipelines.
  - `Escitalopram_Modeling.ipynb`: Script utilizing RDKit to generate 3D conformations of Escitalopram from SMILES strings.
  - `Sequence_Processing.ipynb`: Tools for reverse-translating amino acid sequences back to DNA sequences.
- **`docs/`**: Supporting documentation and reference literature.
  - **`papers/`**: Relevant scientific publications.
  - `Instructions.txt`: Guide for preparing modified FASTA sequences and modeling them using the Expasy ProtMod tool.
- **`output/`**: Directory for generated structural files (e.g., optimized ligand PDBs).

## Key Workflows

### 1. Ligand Modeling
The project uses the `rdkit` library to generate 3D conformations of drugs. The modeling notebook demonstrates:
- Building molecules from SMILES strings.
- Adding explicit hydrogens.
- Performing force field minimization (MMFF) for conformation optimization.
- Exporting the structure to a `.pdb` file for docking or visualization.

### 2. Sequence Analysis
The sequence processing notebook provides tools to reverse-translate specific SERT amino acid sequences into DNA using standard genetic codes, facilitating further genetic engineering design.

### 3. Structural Modification Pipeline
As detailed in the included instructions, the process for structural modification involves:
1. Preparing a modified FASTA sequence.
2. Utilizing the Expasy ProtMod tool to apply in-silico mutations.
3. Generating the resulting 3D structure using molecular modeling software (e.g., PyMOL, Chimera, or Modeller) to study the structural effects of the mutations.
