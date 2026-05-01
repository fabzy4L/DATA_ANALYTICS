from pathlib import Path
from rdkit import Chem

LIGANDS_DIR = Path(__file__).parent.parent / "structures" / "ligands"

mol_file = str(LIGANDS_DIR / "Tetrahydrocannabinol.mol")
pdb_file = str(LIGANDS_DIR / "Tetrahydrocannabinol.pdb")

mol = Chem.MolFromMolFile(mol_file)
Chem.MolToPDBFile(mol, pdb_file)
