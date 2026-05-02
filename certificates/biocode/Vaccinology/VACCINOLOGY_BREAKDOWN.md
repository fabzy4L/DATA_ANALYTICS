# Vaccinology Project Breakdown

This project is a multi-disciplinary bioinformatics workspace combining sequence analysis, structural biology, and advanced cellular protocols.

## 1. Sequence Analysis (CD-HIT Workflow)
The folder contains artifacts from a large-scale protein clustering task (Job ID: `1624324292`).
- **Tool**: [CD-HIT](http://cd-hit.org) (Cluster Database at High Identity with Tolerance).
- **Input**: UniProt Proteome `UP000274756` (likely *Homo sapiens* or a related model organism).
- **Parameters**: 90% identity threshold (`-c 0.9`).
- **Outputs**:
    - `1624324292.fas.1`: Clustered representative sequences.
    - `1624324292.fas.1.clstr`: The clustering map showing which sequences belong to each group.
    - `1624324292.out`: Execution log confirming 10,868 sequences were processed into 10,778 clusters.
- **Scripts**: `run-1624324292.sh` provides the exact shell commands and environment used on the computing cluster.

## 2. Epitope Discovery
Related to the clustering, there is evidence of B-cell epitope prediction:
- **Reports**: `Predicted B-cell epitope.pdf/docx`. These likely contain the finalized candidates for vaccine design based on the processed sequences.

## 3. Structural Biology (Biocode)
The `Biocode/` sub-directory focuses on 3D protein structures:
- **PDB Files**:
    - `1emg.pdb`: Human Carbonic Anhydrase II.
    - `1igt.pdb`: Mouse IgG2a Monoclonal Antibody (highly relevant for vaccinology).
    - `3dnb.pdb`: DNA Binding Domain.
- **RCSB Collection**: A specialized folder of unreleased DNA/Protein sequences from February 2021, used for analyzing structures before they were publicly finalized.

## 4. COVID-19 Research
Specific genomic data for SARS-CoV-2:
- `NC_045512v2.fa`: The reference genome sequence for SARS-CoV-2.
- `sar-cov-2-genes-.gtf`: Gene annotations used for mapping and feature extraction.

## 5. Protocols & Literature
- **SCNT Protocol**: `protocol.md` contains a highly detailed 170-line procedure for Somatic Cell Nuclear Transfer and Embryonic Stem Cell derivation.
- **Software**: Multiple versions of the `seqinr` R package, used for biological sequence analysis and database access.

## Summary of Tools Used
- **CD-HIT**: Sequence clustering.
- **gnuplot**: Generating visual reports for clustering results.
- **Perl**: Used for statistical analysis of FASTA files (`faa_stat.pl`).
- **R (seqinr)**: General sequence manipulation and analysis.
- **PyMOL/VMD (implied)**: For viewing the `.pdb` files.
