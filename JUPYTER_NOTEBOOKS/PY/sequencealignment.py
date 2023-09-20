# Load necessary libraries
library(Biostrings)
library(seqinr)

# Example sequences
dna_sequence1 <- DNAString("ATCGATCGATCG")
dna_sequence2 <- DNAString("ATCGAGCGATCG")
protein_sequence <- AAString("MASTPKDLAIVT")

# Define the substitution matrix for DNA sequences
substitution_matrix <- matrix(c(1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1), nrow = 4)
rownames(substitution_matrix) <- colnames(substitution_matrix) <- c("A", "T", "C", "G")

# Sequence Alignment (Pairwise)
pairwise_alignment <- pairwiseAlignment(dna_sequence1, dna_sequence2, substitutionMatrix = substitution_matrix)

# Multiple Sequence Alignment
multi_alignment_sequences <- c("ATCGATCGATCG", "ATCGAGCGATCG", "AGCGTACGATCG")
multi_alignment <- clustalwAlignment(multi_alignment_sequences)

# Sequence Manipulation
# Finding Motifs using regular expressions
motif_pattern <- "CGAT"  # Example motif pattern
matches <- regexpr(motif_pattern, as.character(dna_sequence1))
motif_positions <- attr(matches, "match.length") > 0
motif_positions <- which(motif_positions)

# Calculating GC Content
gc_content <- function(sequence) {
  gc_count <- sum(sequence == "G" | sequence == "C")
  total_bases <- length(sequence)
  gc_percentage <- (gc_count / total_bases) * 100
  return(gc_percentage)
}

dna_gc_content <- gc_content(as.character(dna_sequence1))

# Identifying Open Reading Frames (ORFs)
find_orfs <- function(sequence) {
  start_codon <- "ATG"
  stop_codons <- c("TAA", "TAG", "TGA")
  
  # ... (rest of the code for finding ORFs)

  return(orf_positions)
}

orf_positions <- find_orfs(as.character(dna_sequence1))

# Printing results
cat("Pairwise Alignment Score:", pairwise_alignment@score, "\n")
cat("Multiple Sequence Alignment:\n")
print(multi_alignment)
cat("DNA GC Content:", dna_gc_content, "%\n")
cat("ORF Positions:", orf_positions, "\n")
