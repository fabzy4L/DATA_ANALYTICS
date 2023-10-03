from rdkit import Chem
from rdkit.Chem import AllChem

# Load the PDB file
mol = Chem.MolFromPDBFile("/Users/f4L/Documents/GitHub/DATA_ANALYSIS/DATA_ANALYTICS/MOLECULES/5tgz.pdb")

# Assign partial charges and add hydrogens
mol = Chem.AddHs(mol)
AllChem.ComputeGasteigerCharges(mol)

# Write the molecule to PDBQT format
writer = Chem.PDBQTWriter(open("5tgz.pdbqt", "w"))
writer.write(mol)
writer.close()
