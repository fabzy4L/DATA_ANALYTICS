"""
Multi-epitope vaccine construct assembler.

Usage:
    python build_construct.py

Before running:
    1. Complete Stages 02 and 03 (T-cell prediction + scoring).
    2. Replace the placeholder epitope lists below with your filtered candidates.
    3. Each epitope must pass: antigenicity >= 0.5, non-allergenic, instability < 40.

Output:
    results/reports/vaccine_construct.fasta
    results/reports/vaccine_construct_stats.txt
"""

from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# CONFIG — linkers and adjuvant
# ---------------------------------------------------------------------------

ADJUVANT     = "MPKKKRKV"   # RS09 TLR4 agonist peptide (N-terminus)
LINKER_BCELL = "GPGPG"      # flexible; preserves B-cell epitope conformation
LINKER_MHC1  = "AAY"        # proteasomal cleavage site for MHC-I processing
LINKER_MHC2  = "GPGPG"      # flexible spacer for MHC-II epitopes
LINKER_JOIN  = "KK"         # domain junction separator

# ---------------------------------------------------------------------------
# EPITOPE LISTS
# Fill these from your Stage 02 + 03 outputs.
# - Source for B-cell:  results/reports/Predicted B-cell epitope.docx
# - Source for MHC-I:   analysis/02_epitope_prediction/netmhcpan_results.txt
# - Source for MHC-II:  analysis/02_epitope_prediction/netmhciipan_results.txt
# Rules: antigenicity >= 0.5 (VaxiJen), non-allergenic (AllerTop), instability < 40
# ---------------------------------------------------------------------------

BCELL_EPITOPES: list[str] = [
    # TODO: replace placeholders with sequences from B-cell epitope report
    "PLACEHOLDER_BCELL_1",
    "PLACEHOLDER_BCELL_2",
    "PLACEHOLDER_BCELL_3",
]

MHC1_EPITOPES: list[str] = [
    # TODO: replace with strong MHC-I binders (IC50 <= 50 nM or percentile rank <= 0.5)
    "PLACEHOLDER_MHC1_1",
    "PLACEHOLDER_MHC1_2",
    "PLACEHOLDER_MHC1_3",
]

MHC2_EPITOPES: list[str] = [
    # TODO: replace with strong MHC-II binders (percentile rank <= 10)
    "PLACEHOLDER_MHC2_1",
    "PLACEHOLDER_MHC2_2",
    "PLACEHOLDER_MHC2_3",
]


# ---------------------------------------------------------------------------
# ASSEMBLY
# ---------------------------------------------------------------------------

def assemble(bcell: list[str], mhc1: list[str], mhc2: list[str]) -> str:
    """
    Architecture: [Adjuvant]-KK-[B-cell GPGPG-joined]-KK-[MHC-I AAY-joined]-KK-[MHC-II GPGPG-joined]
    """
    if not bcell:
        raise ValueError("BCELL_EPITOPES is empty — add sequences from Stage 03.")
    if not mhc1:
        raise ValueError("MHC1_EPITOPES is empty — run NetMHCpan first (Stage 02).")
    if not mhc2:
        raise ValueError("MHC2_EPITOPES is empty — run NetMHCIIpan first (Stage 02).")

    domains = [
        ADJUVANT,
        LINKER_BCELL.join(bcell),
        LINKER_MHC1.join(mhc1),
        LINKER_MHC2.join(mhc2),
    ]
    return LINKER_JOIN.join(domains)


# ---------------------------------------------------------------------------
# OUTPUT FORMATTING
# ---------------------------------------------------------------------------

def to_fasta(sequence: str, header: str = "multi_epitope_vaccine_construct") -> str:
    lines = [f">{header}"]
    for i in range(0, len(sequence), 60):
        lines.append(sequence[i:i + 60])
    return "\n".join(lines)


def compute_stats(sequence: str) -> dict:
    length = len(sequence)
    counts = Counter(sequence)
    mw_estimate = length * 110          # rough: ~110 Da per residue average
    has_placeholders = "PLACEHOLDER" in sequence
    return {
        "length_aa": length,
        "mw_estimate_kDa": round(mw_estimate / 1000, 1),
        "aa_composition": dict(sorted(counts.items())),
        "contains_placeholders": has_placeholders,
    }


def format_stats(stats: dict, construct: str) -> str:
    lines = [
        "=== Vaccine Construct Stats ===",
        f"Length       : {stats['length_aa']} amino acids",
        f"MW (est.)    : ~{stats['mw_estimate_kDa']} kDa  (rough: 110 Da/residue)",
        f"Placeholders : {'YES — replace epitope lists before submitting!' if stats['contains_placeholders'] else 'None'}",
        "",
        "Composition:",
    ]
    for aa, count in stats["aa_composition"].items():
        pct = count / stats["length_aa"] * 100
        lines.append(f"  {aa}  {count:>4}  ({pct:.1f}%)")
    lines += [
        "",
        "Domain map:",
        f"  Adjuvant (RS09):  {ADJUVANT}",
        f"  Junction linker:  {LINKER_JOIN}",
        f"  B-cell linker:    {LINKER_BCELL}",
        f"  MHC-I linker:     {LINKER_MHC1}",
        f"  MHC-II linker:    {LINKER_MHC2}",
        "",
        "Next steps:",
        "  1. Submit results/reports/vaccine_construct.fasta to ColabFold for 3D structure.",
        "  2. Dock vaccine_construct.pdb on HDOCK against TLR4 (3FXI), MHC-I (1HHH), MHC-II (1DLH).",
        "  3. Run C-ImmSim immune simulation.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    construct = assemble(BCELL_EPITOPES, MHC1_EPITOPES, MHC2_EPITOPES)
    stats     = compute_stats(construct)
    fasta_str = to_fasta(construct)
    stats_str = format_stats(stats, construct)

    print(fasta_str)
    print()
    print(stats_str)

    # Resolve output directory relative to this script's location
    script_dir = Path(__file__).resolve().parent
    out_dir    = script_dir.parent.parent / "results" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    fasta_path = out_dir / "vaccine_construct.fasta"
    stats_path = out_dir / "vaccine_construct_stats.txt"

    fasta_path.write_text(fasta_str + "\n")
    stats_path.write_text(stats_str + "\n")

    print(f"\nSaved: {fasta_path}")
    print(f"Saved: {stats_path}")

    if stats["contains_placeholders"]:
        print("\nWARNING: construct still contains placeholder sequences.")
        print("Replace BCELL_EPITOPES / MHC1_EPITOPES / MHC2_EPITOPES before")
        print("submitting to ColabFold or docking tools.")


if __name__ == "__main__":
    main()
