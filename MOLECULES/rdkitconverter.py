from rdkit import Chem

mol_file = "/Users/f4L/Downloads/Tetrahydrocannabinol.mol"
pdb_file = "/Users/f4L/Downloads/Tetrahydrocannabinol.pdb"

# Load the molecule from the MOL file
mol = Chem.MolFromMolFile(mol_file)

# Save the molecule to PDB format
Chem.MolToPDBFile(mol, pdb_file)
