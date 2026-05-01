# Restructure Summary

**Date:** 2026-05-01

## What We Did

Reorganized the `DATA_ANALYTICS` repository from a mixed language-first / domain-first layout into a consistent **domain-first structure** with 8 top-level folders.

## Before

The root contained 15+ folders with no consistent grouping logic — language folders (`PYTHON/`, `DNA_R/`) sat alongside domain folders (`EPIDEMIOLOGY_PYTHON/`, `PROTEOMICS/`), and loose files lived at the root.

## After

```
bioinformatics/            epidemiology_public_health/
data_science_ml/           education/
business_apps/             clinical_lab_data/
infrastructure/            certificates/
```

## Key Moves

| Old Location | New Location |
|---|---|
| `GENE_EXPRESSION NICOTINE_R/` | `bioinformatics/nicotine_gene_expression/` |
| `PROTEOMICS/`, `DNA_R/`, `NEUREGEN_SNP_ANNOTATOR/` | `bioinformatics/` subfolders |
| `R_NOTEBOOKS/TRANSCRIPTOMICS/` | `bioinformatics/transcriptomics/` |
| `PYTHON/BIOINFORMATICS/` | `bioinformatics/python_bio/` |
| `EPIDEMIOLOGY_COV19_SHINY/`, `EPIDEMIOLOGY_PYTHON/`, `FRAMINGHAM/` | `epidemiology_public_health/` subfolders |
| `PYTHON/MACHINE_LEARNING/`, `PYTHON/ENGINEERING_AND_SPECIAL_PROJECTS/` | `data_science_ml/` subfolders |
| `PyTorch.ipynb`, `Untitled.ipynb` | `data_science_ml/pytorch_experiments/` |
| `R_NOTEBOOKS/` (general + MAPMYRUN) | `data_science_ml/r_notebooks/`, `data_science_ml/personal_projects/` |
| `BIOSTATISTICS_COURSE_PROJECTS/`, `PHD_DISSERTATION/`, `PYTHON/ANALYTICS_LAB/` | `education/` subfolders |
| `BUSINESS ANALYTICS/`, `rtb_app/` | `business_apps/` subfolders |
| `PAIN_MED_DATA/` | `clinical_lab_data/pain_med_data/` |
| `SQL/`, `PYTHON/DATA_ACQUISITION/`, `PYTHON/UTILITIES/` | `infrastructure/` subfolders |
| `BioCode Certificates/` | `certificates/biocode/` |
| `Envelope_5JHM.fasta`, IHC staining PDF | `bioinformatics/data/` |

## What Was Dissolved

- `PYTHON/` — all 7 subfolders distributed across domains; folder removed.
- `R_NOTEBOOKS/` — all subfolders and files distributed; folder removed.
- Root `.ipynb_checkpoints/` — removed (build artifact).

## README

Rewritten to reflect the new domain structure with an updated directory tree, domain summaries, and a technology stack table.

## One Incident

During the move of `PYTHON/ENGINEERING_AND_SPECIAL_PROJECTS/`, a Windows access-denied error prevented `Social_Data/` from being copied. It was recovered from git (`git checkout HEAD`) and moved successfully before the source folder was removed.
