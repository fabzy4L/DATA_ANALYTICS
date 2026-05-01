from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import PandasTools

LIGANDS_DIR = Path(__file__).parent.parent / "structures" / "ligands"

smiles_thc8 = 'CCCCCC1=CC(=C2C3CC(=CCC3C(OC2=C1)(C)C)C)O'
smiles_thc9 = 'CCCCCc1cc(c2c(c1)OC([C@H]3[C@H]2C=C(CC3)C)(C)C)O'

mol = Chem.MolFromSmiles(smiles_thc8)
mol2 = Chem.MolFromSmiles(smiles_thc9)

AllChem.EmbedMolecule(mol)
AllChem.EmbedMolecule(mol2)

AllChem.MMFFOptimizeMolecule(mol)
AllChem.MMFFOptimizeMolecule(mol2)

Chem.MolToPDBFile(mol, str(LIGANDS_DIR / "thc8.pdb"))
Chem.MolToPDBFile(mol2, str(LIGANDS_DIR / "thc9.pdb"))



