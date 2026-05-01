# RECEPTOR_DESIGN — Project Review

## Project Overview

**Goal:** Structural investigation of the Serotonin Transporter (SERT) — specifically how point mutations at position S348 affect Escitalopram (SSRI antidepressant) binding.

---

## What's Been Completed

| Area | Status |
|---|---|
| Wild-type SERT structures (5I6Z, 5I71, 2A65) | Downloaded and organized |
| Chain A isolation + FASTA sequences | Done |
| In-silico mutations S348T and S348A | Generated (`.pdb` files present) |
| Escitalopram 3D structure | Generated via RDKit in notebook |
| Reverse translation pipeline | Implemented (AA → DNA, 1,980 nt output) |
| ChimeraX visualization sessions | 2 sessions built (56 MB + 13 MB) |

---

## Current Gaps

1. **`scripts/` folder is empty** — all code lives in notebooks; no standalone `.py` scripts yet.
2. **`Annotations.txt` is blank** — placeholder with no content.
3. **No docking analysis** — the Escitalopram `.pdb` is generated but hasn't been docked against the SERT structures computationally.
4. **No MD simulations** — listed as a future goal in `WORKFLOW.md` but not started.
5. **`5I6Z_edited.fasta`** appears identical to `5I6Z.fasta` — unclear if the intended mutation was saved.

---

## Structural Focus

- **Wild-type:** `5i6z_A.pdb` (Chain A, SERT only)
- **Mutants:** `5i6Z_S348T_3.pdb` and `5i6Z_S348_A.pdb`
- **Ligand:** `output/escitalopram.pdb`
- **Comparison session:** `2a65_v_516z.cxs` (likely comparing the 2001 LeuT homolog vs modern SERT crystal)

---

## Next Steps

Based on `WORKFLOW.md` Phase 5 and future goals, the natural next steps would be:

1. **Docking** — run Escitalopram against WT and mutant SERT (AutoDock Vina or Glide)
2. **Annotation** — populate `Annotations.txt` with mutation rationale and observations from ChimeraX
3. **Refactor notebooks → scripts** — move the RDKit and reverse translation code into `scripts/` as `.py` files
