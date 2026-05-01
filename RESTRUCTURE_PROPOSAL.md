# Project Restructuring Proposal: DATA_ANALYTICS

## Rationale
The current repository structure is partially organized by language (e.g., `PYTHON`, `DNA_R`) and partially by project/domain (e.g., `EPIDEMIOLOGY_PYTHON`, `PROTEOMICS`). To improve discoverability and maintainability, I propose a **Domain-First** organizational structure. This aligns with the existing organization within the `PYTHON/` directory and scales better as more projects are added.

## Proposed Structure

### 1. `bioinformatics/` (Genomics, Proteomics, Molecular Biology)
*   `nicotine_gene_expression/` ← `GENE_EXPRESSION NICOTINE_R/`
*   `snp_annotator/` ← `NEUREGEN_SNP_ANNOTATOR/`
*   `proteomics/` ← `PROTEOMICS/`
*   `dna_analysis/` ← `DNA_R/`
*   `python_bio/` ← `PYTHON/BIOINFORMATICS/`
*   `data/` ← (Root `.fasta` files and other raw biological data)
*   `certificates/` ← `BioCode Certificates/`

### 2. `epidemiology_public_health/`
*   `covid19_shiny_app/` ← `EPIDEMIOLOGY_COV19_SHINY/`
*   `python_epidemiology/` ← `EPIDEMIOLOGY_PYTHON/`
*   `framingham_study/` ← `FRAMINGHAM/`

### 3. `data_science_ml/` (General Machine Learning and Statistics)
*   `machine_learning_py/` ← `PYTHON/MACHINE_LEARNING/`
*   `pytorch_experiments/` ← `PyTorch.ipynb`, `Untitled.ipynb`
*   `r_notebooks/` ← `R_NOTEBOOKS/` (General R projects)

### 4. `biostatistics_education/`
*   `biostats_course_projects/` ← `BIOSTATISTICS_COURSE_PROJECTS/`
*   `analytics_learning/` ← `PYTHON/ANALYTICS_LAB/`

### 5. `business_apps/`
*   `business_analytics/` ← `BUSINESS ANALYTICS/`
*   `rtb_app/` ← `rtb_app/`

### 6. `clinical_lab_data/`
*   `pain_med_data/` ← `PAIN_MED_DATA/`
*   `database_sql/` ← `SQL/`

### 7. `engineering_special/`
*   `engineering_projects/` ← `PYTHON/ENGINEERING_AND_SPECIAL_PROJECTS/`

### 8. `academic/`
*   `phd_dissertation/` ← `PHD_DISSERTATION/`

### 9. `infrastructure/`
*   `utilities/` ← `PYTHON/UTILITIES/`
*   `data_acquisition/` ← `PYTHON/DATA_ACQUISITION/`

---

## Implementation Steps (To be executed if approved)
1.  **Backup**: Ensure all changes are committed or backed up.
2.  **Move Folders**: Systematically move directories to their new locations.
3.  **Update Paths**: Update relative data paths in R and Python scripts.
4.  **Consolidate READMEs**: Create a master README (drafted below) and ensure sub-directories have consistent documentation.
5.  **Clean Root**: Remove temporary/untitled files from the root directory.

## Impact on Scripts
*   **R Markdown**: Relative paths like `../../data/` may need adjustment.
*   **Python Imports**: If scripts rely on the current folder structure for local imports, they will need updating.
*   **IDE Settings**: Project paths in VS Code/PyCharm/RStudio will need to be re-pointed.
