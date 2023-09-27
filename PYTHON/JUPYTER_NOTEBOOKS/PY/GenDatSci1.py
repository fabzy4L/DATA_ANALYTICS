dna = "TGGGGATCCCGGGTATAGACCTTTATCTGCGGTTCAAGTTAGGCATAAGG"
totlen = len(dna)
no_c = dna.count('C')
no_g = dna.count('G')
gc_percent = ((no_c+no_g)*100)/totlen
print(gc_percent)