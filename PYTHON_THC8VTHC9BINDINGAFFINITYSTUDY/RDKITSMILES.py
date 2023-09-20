from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import PandasTools

# Define the SMILES string
smiles_thc8 = 'CCCCCC1=CC(=C2C3CC(=CCC3C(OC2=C1)(C)C)C)O'
smiles_thc9 = 'CCCCCc1cc(c2c(c1)OC([C@H]3[C@H]2C=C(CC3)C)(C)C)O'

# Create an RDKit molecule object from the SMILES string
mol = Chem.MolFromSmiles(smiles_thc8)
mol2 = Chem.MolFromSmiles(smiles_thc9)

# Generate a 3D conformation of the molecule
AllChem.EmbedMolecule(mol)
AllChem.EmbedMolecule(mol2)

# Optimize the 3D conformation using force field minimization
AllChem.MMFFOptimizeMolecule(mol)
AllChem.MMFFOptimizeMolecule(mol2)

# Save the molecule as a PDB file
pdb_file = 'thc8.pdb'
Chem.MolToPDBFile(mol, pdb_file)
pdb_file2 = 'thc9.pdb'
Chem.MolToPDBFile(mol2, pdb_file2)



