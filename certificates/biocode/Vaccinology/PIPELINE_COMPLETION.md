# Vaccinology Project — Completion Guide

Practical step-by-step instructions to finish the remaining pipeline stages.
Current status: Stage 01 (clustering) and Stage 02 partial (B-cell only) are complete.

---

## Stage 02 — T-cell Epitope Prediction

**Input:** `analysis/01_clustering/1624324292.fas.1`

### MHC-I (CD8+ T-cell) — NetMHCpan-4.1

- Download: [DTU Health Tech](https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/)
- Or use online: [IEDB MHC-I](http://tools.iedb.org/mhci/)
- Alleles to run: `HLA-A*02:01`, `HLA-A*24:02`, `HLA-B*07:02`, `HLA-B*35:01`
- Peptide length: **9-mer** (standard for MHC-I)

### MHC-II (CD4+ T-cell) — NetMHCIIpan-4.0

- Download: [DTU Health Tech](https://services.healthtech.dtu.dk/services/NetMHCIIpan-4.0/)
- Or use online: [IEDB MHC-II](http://tools.iedb.org/mhcii/)
- Alleles to run: `HLA-DRB1*01:01`, `HLA-DRB1*03:01`, `HLA-DRB1*07:01`
- Peptide length: **15-mer**

**Save outputs to:** `analysis/02_epitope_prediction/`

---

## Stage 03 — Candidate Scoring & Filtering

Run on the combined B-cell + T-cell candidate list. All tools are web-based.

| Analysis | Tool | Threshold |
|---|---|---|
| Antigenicity | [VaxiJen v2.0](http://www.ddg-pharmfac.net/vaxijen) | Keep score ≥ 0.5 |
| Allergenicity | [AllerTop 2.0](http://www.ddg-pharmfac.net/allertop) | Discard allergenic hits |
| Physicochemical | [ExPASy ProtParam](https://web.expasy.org/protparam/) | Instability index < 40, GRAVY check |
| Toxicity | [ToxinPred](https://webs.iiitd.edu.in/raghava/toxinpred/) | Exclude toxic sequences |

**Save scored tables to:** `analysis/03_candidate_scoring/`

---

## Stage 04 — Multi-Epitope Construct Design

**Script:** `analysis/04_construct_design/build_construct.py`

Assemble top-ranked, non-allergenic, antigenic epitopes into a chimeric sequence
using standard linkers:

| Epitope Type | Linker | Role |
|---|---|---|
| B-cell | `GPGPG` | Flexible, preserves conformation |
| MHC-I (CD8+) | `AAY` | Proteasomal cleavage site |
| MHC-II (CD4+) | `GPGPG` | Flexible spacer |
| Between domains | `KK` | Junction separator |

N-terminus: prepend **RS09** adjuvant peptide (`MPKKKRKV`) to boost TLR4-mediated
innate immune priming.

**How to run:**

```bash
python analysis/04_construct_design/build_construct.py
```

Output is written to `results/reports/vaccine_construct.fasta`.

> **Before running:** open `build_construct.py` and replace the placeholder lists
> (`BCELL_EPITOPES`, `MHC1_EPITOPES`, `MHC2_EPITOPES`) with your filtered candidates
> from Stage 03.

---

## Stage 05 — Structural Validation & Docking

### 3D Structure Prediction

Use **ColabFold** (AlphaFold2, free, no installation required):

1. Open: [ColabFold on Google Colab](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb)
2. Paste the sequence from `results/reports/vaccine_construct.fasta`
3. Run — download the top-ranked `.pdb` file
4. Save as `data/structures/vaccine_construct.pdb`

### Molecular Docking

Use **HDOCK** server (no installation, accepts PDB files directly):

1. Open: [HDOCK](http://hdock.phys.hust.edu.cn)
2. Upload `data/structures/vaccine_construct.pdb` as the **ligand**
3. Run docking against:
   - **TLR4/MD-2:** download receptor PDB `3FXI` from RCSB
   - **MHC-I:** PDB `1HHH`
   - **MHC-II:** PDB `1DLH`
   - **Antibody model:** `data/structures/1igt.pdb` (already available)
4. Save all docking result PDBs to `analysis/05_docking_simulation/`

### In Silico Immune Simulation

Use **C-ImmSim**:

1. Open: [C-ImmSim](http://150.146.60.135/C-IMMSIM/)
2. Paste your construct sequence
3. Run at a 4-week injection schedule (default settings)
4. Outputs: antibody titer curves, cytokine profiles, lymphocyte counts
5. Save report to `results/reports/immune_simulation_report.pdf`

---

## Recommended Order

```
This week
  1. Run NetMHCpan-4.1 on 1624324292.fas.1  →  analysis/02_epitope_prediction/
  2. Run NetMHCIIpan-4.0 on same input       →  analysis/02_epitope_prediction/
  3. Score all candidates (VaxiJen, AllerTop, ProtParam)  →  03_candidate_scoring/

Next
  4. Fill epitope lists in build_construct.py and run it
  5. Submit vaccine_construct.fasta to ColabFold

Final
  6. Dock on HDOCK (TLR4, MHC-I, MHC-II, 1igt)
  7. Run C-ImmSim
  8. Write final integrated report combining all stages
```

---

## S1 Spike Protein — Pipeline Connection

The spike protein analysis in `notebooks/S1 Protein Amino Acid Distribution.Rmd`
should feed into Step 02 as a **targeted antigen source**. Re-run the Rmd to
extract S1 subunit sequences from `data/genomic/NC_045512v2.fa` and use those
as a focused epitope prediction input, rather than running the full proteome.
This gives more vaccine-relevant candidates.
