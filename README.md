# DATA_ANALYTICS

A portfolio of data analytics and bioinformatics projects organized by domain. Languages used across the repo include Python, R, and SQL.

---

## Repository Structure

```text
.
├── bioinformatics/                         # Genomics, proteomics, molecular biology
│   ├── nicotine_gene_expression/           # qPCR nicotine gene expression (R + Power BI)
│   ├── snp_annotator/                      # SNP annotation tool (R)
│   ├── proteomics/                         # Protein analysis and Luminex data
│   ├── dna_analysis/                       # DNA analysis scripts (R)
│   ├── transcriptomics/                    # RNA-seq and microarray analysis (R)
│   ├── python_bio/                         # Drug discovery, receptor design, sequence analysis (Python)
│   └── data/                               # Raw biological files (.fasta, lab protocols)
│
├── epidemiology_public_health/             # Population health and disease modeling
│   ├── covid19_shiny_app/                  # Interactive global outbreak tracker (R Shiny)
│   ├── python_epidemiology/                # SIR/SEIR epidemiological models (Python)
│   └── framingham_study/                   # Framingham Heart Study analysis (R)
│
├── data_science_ml/                        # Machine learning and general data science
│   ├── machine_learning_py/                # Iris classification, CNNs, deep learning (Python)
│   ├── pytorch_experiments/                # PyTorch neural network notebooks
│   ├── engineering_projects/               # FEA, CAD, sports analytics (Python)
│   ├── personal_projects/                  # Fitness data analysis — MapMyRun (R)
│   ├── r_notebooks/                        # Time series and general R notebooks
│   └── jupyter_notebooks/                  # Mixed-domain Jupyter notebook collection
│
├── education/                              # Coursework and academic research
│   ├── biostats_course_projects/           # Biostatistics labs and quizzes (R)
│   ├── analytics_learning/                 # Pandas, NumPy, data cleaning exercises (Python)
│   └── phd_dissertation/                   # PhD dissertation R Markdown source files
│
├── business_apps/                          # Business intelligence and applications
│   ├── business_analytics/                 # Income analysis (R)
│   └── rtb_app/                            # RTB (Return to Baseline) Streamlit app (Python)
│
├── clinical_lab_data/                      # Clinical lab tracking and instrumentation
│   └── pain_med_data/                      # SCIEX mass spec, UA trackers, qPCR tools (XLSX)
│
├── infrastructure/                         # Tooling, automation, and database
│   ├── database_sql/                       # qPCR and gene database schemas (SQL)
│   ├── data_acquisition/                   # Web scraping tools — Selenium/BS4 (Python)
│   └── utilities/                          # General-purpose Python utilities
│
└── certificates/
    └── biocode/                            # BioCode bioinformatics course materials
```

---

## Domain Summaries

### bioinformatics/
The largest research domain. `nicotine_gene_expression/` is the most complete project — raw CT values flow through R Markdown statistical models into Power BI dashboards. `transcriptomics/` contains Affymetrix microarray contrast matrix analysis. `python_bio/` covers drug discovery pipelines and receptor modeling.

### epidemiology_public_health/
`covid19_shiny_app/` is a full-stack R Shiny dashboard that maps global disease trends against world coordinates. `python_epidemiology/` implements compartmental epidemic models (SIR/SEIR) as both a script and notebook.

### data_science_ml/
`machine_learning_py/` includes classical ML (Iris) and CNN image recognition. `pytorch_experiments/` holds hands-on PyTorch notebooks. `engineering_projects/` spans FEA simulations and sports analytics with Python.

### education/
`biostats_course_projects/` contains R Markdown labs analyzing datasets such as `bumpus.csv`, `daphnia.csv`, and `telomere inheritance.csv`. `analytics_learning/` is the Python counterpart — foundational data manipulation exercises.

### business_apps/
`rtb_app/` is a production-style Streamlit application for Return-to-Baseline clinical analysis with multiple versioned app files and CSV data exports.

### infrastructure/
`database_sql/` contains the `qPCR_db.sql` schema and gene database scripts. `data_acquisition/` holds Selenium-based web scrapers. `utilities/` provides reusable Python scripts.

---

## Technology Stack

| Category | Tools |
|---|---|
| Languages | Python 3.x, R (Tidyverse), SQL |
| Bioinformatics | Bioconductor, BioPython, SeqinR |
| Machine Learning | Scikit-Learn, PyTorch, Keras |
| Data / Reporting | Pandas, Matplotlib, R Markdown, Power BI, Jupyter |
| Apps | Shiny (R), Streamlit (Python) |
| Databases | PostgreSQL, SQLite |
