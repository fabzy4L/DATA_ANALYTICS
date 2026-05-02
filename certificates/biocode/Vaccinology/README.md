# Vaccinology Pipeline

Reverse-vaccinology workflow targeting SARS-CoV-2 spike protein (S1 subunit) and related
proteomes. Goal: identify B-cell and T-cell epitope candidates for multi-epitope vaccine design.

---

## Pipeline Overview

```
Proteome acquisition
       │
       ▼
[01] Sequence Clustering (CD-HIT)          ✅ DONE
       │
       ▼
[02] Epitope Prediction
       ├── B-cell epitopes                 ✅ DONE
       ├── MHC-I / CD8+ T-cell epitopes    ❌ MISSING
       └── MHC-II / CD4+ T-cell epitopes   ❌ MISSING
       │
       ▼
[03] Candidate Scoring & Filtering         ❌ MISSING
       ├── Antigenicity (VaxiJen/ANTIGENpro)
       ├── Allergenicity (AllerTop/AllerHunter)
       └── Physicochemical properties (ProtParam)
       │
       ▼
[04] Multi-Epitope Construct Design        ❌ MISSING
       └── Link best epitopes with GPGPG / AAY / KK linkers
       │
       ▼
[05] Structural Validation & Docking       ❌ MISSING
       ├── 3D structure prediction (AlphaFold/I-TASSER)
       ├── Molecular docking (vs TLR2, TLR4, MHC-I, MHC-II)
       └── In silico immune simulation (C-ImmSim)
```

---

## Stage Details

### [01] Sequence Clustering — `analysis/01_clustering/`

**Tool:** CD-HIT (Cluster Database at High Identity with Tolerance)  
**Input:** `data/proteomes/uniprot-proteome_UP000274756.fasta` — 10,868 sequences  
**Parameters:** 90% identity threshold (`-c 0.9`)  
**Output:**
- `1624324292.fas.1` — representative sequences per cluster
- `1624324292.fas.1.clstr` — full cluster membership map
- `1624324292.out` — execution log (10,868 → 10,778 clusters)
- `run-1624324292.sh` — exact shell commands used on computing cluster

**Status:** Complete. Job finished successfully (see `You job 1624324292 is finished.html`).

---

### [02] Epitope Prediction — `analysis/02_epitope_prediction/` | `results/reports/`

#### B-cell Epitopes ✅
Final candidates documented in:
- `results/reports/Predicted B-cell epitope.pdf`
- `results/reports/Predicted B-cell epitope.docx`

#### T-cell Epitopes (MHC-I and MHC-II) ❌
**Not yet done.** Recommended tools:
- **MHC-I (CD8+):** NetMHCpan-4.1 or IEDB Analysis Resource
- **MHC-II (CD4+):** NetMHCIIpan-4.0 or IEDB
- Use the clustered representative sequences (`1624324292.fas.1`) as input

---

### [03] Candidate Scoring — `analysis/03_candidate_scoring/` ❌

Run on the union of B-cell + T-cell epitope candidates:

| Analysis | Tool | Purpose |
|---|---|---|
| Antigenicity | VaxiJen v2.0 or ANTIGENpro | Rank by predicted immunogenicity |
| Allergenicity | AllerTop 2.0 / AllerHunter | Exclude allergenic sequences |
| Physicochemical | ExPASy ProtParam | MW, pI, instability index, GRAVY |
| Toxicity | ToxinPred | Exclude cytotoxic sequences |

---

### [04] Multi-Epitope Construct Design — `analysis/04_construct_design/` ❌

Assemble top-ranked, non-allergenic, antigenic epitopes into a chimeric vaccine sequence
using standard linkers:

| Epitope Type | Linker |
|---|---|
| B-cell | GPGPG |
| MHC-I (CD8+) | AAY |
| MHC-II (CD4+) | GPGPG |
| Between domains | KK |

Add an adjuvant sequence at the N-terminus (e.g., RS09 TLR4 agonist peptide) to boost
innate immune priming.

---

### [05] Structural Validation & Docking — `analysis/05_docking_simulation/` ❌

1. **3D structure prediction** of the final multi-epitope construct:
   - AlphaFold2 (ColabFold for local runs) or I-TASSER
2. **Molecular docking** against immune receptors:
   - Reference structures already available in `data/structures/`:
     - `1igt.pdb` — mouse IgG2a antibody (vaccine response model)
     - RCSB unreleased collection (Feb 2021) — additional structural references
   - Docking targets: TLR2 (PDB: 3A7B), TLR4/MD-2 (PDB: 3FXI), MHC-I (PDB: 1HHH),
     MHC-II (PDB: 1DLH)
3. **In silico immune simulation:** C-ImmSim server

---

## S1 Protein Spike Analysis

The S1 subunit amino acid composition analysis lives in `notebooks/`:
- `S1 Protein Amino Acid Distribution.Rmd` — R script for amino acid profiling
- `S1 Protein Amino Acid Distribution.nb.html/.pdf` — rendered outputs

This connects directly to the SARS-CoV-2 reference data in `data/genomic/`:
- `NC_045512v2.fa` — reference genome (GenBank accession NC_045512.2)
- `sar-cov-2-genes-.gtf` — gene feature annotations
- `gene_file.fa` — extracted gene sequences

**Gap:** the S1 composition analysis should feed into Step 02 as the antigen sequence
source for epitope prediction. This linkage is not yet implemented in the pipeline.

---

## Data Inventory

```
data/
├── proteomes/
│   ├── uniprot-proteome_UP000274756.fasta   ← primary clustering input
│   └── uniprot-proteome_UP000038040.fasta   ← secondary proteome reference
├── genomic/
│   ├── NC_045512v2.fa                       ← SARS-CoV-2 reference genome
│   ├── sar-cov-2-genes-.gtf                 ← gene feature annotations
│   ├── sar-cov-2-genes                      ← gene list (no extension)
│   ├── sar-cov-2-genes-.gtf.gtf             ← alternate GTF copy
│   └── gene_file.fa                         ← extracted gene sequences
└── structures/
    ├── 1emg.pdb                             ← Human Carbonic Anhydrase II
    ├── 1igt.pdb                             ← Mouse IgG2a (antibody model)
    ├── 3dnb.pdb                             ← DNA Binding Domain
    ├── rcsb_pdb_1IGT.fasta                  ← 1IGT derived sequence
    ├── rcsb_pdb_5XH3 EDITED.txt             ← 5XH3 sequence (edited)
    ├── rcsb_pdb_6XM4.fasta                  ← 6XM4 sequence
    └── rcsb_pdb_unreleased_sequences_.../   ← 789 RCSB sequences (Feb 2021)
```

---

## Tools Reference

| Tool | Location | Purpose |
|---|---|---|
| CD-HIT | HPC cluster (see `run-1624324292.sh`) | Sequence clustering |
| seqinr (R) | `../../tools/seqinr/` | Sequence manipulation & DB access |
| gnuplot | System | Clustering visualization |
| Perl `faa_stat.pl` | System | FASTA file statistics |
| PyMOL / VMD | System | PDB structure visualization |
