import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
LIGANDS_DIR = ROOT / "structures" / "ligands"
RECEPTOR_DIR = ROOT / "structures" / "receptor"

ligand8_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc8.pdb"
ligand9_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc9.pdb"
receptor_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/5tgz.pdb"

ligand8_pdb = str(LIGANDS_DIR / "ligand8.pdb")
ligand9_pdb = str(LIGANDS_DIR / "ligand9.pdb")
receptor_pdb = str(RECEPTOR_DIR / "receptor.pdb")

ligand8_pdbqt = str(LIGANDS_DIR / "ligand8.pdbqt")
ligand9_pdbqt = str(LIGANDS_DIR / "ligand9.pdbqt")
receptor_pdbqt = str(RECEPTOR_DIR / "receptor.pdbqt")

urllib.request.urlretrieve(ligand8_url, ligand8_pdb)
urllib.request.urlretrieve(ligand9_url, ligand9_pdb)
urllib.request.urlretrieve(receptor_url, receptor_pdb)

os.system(f"obabel {ligand8_pdb} -O {ligand8_pdbqt}")
os.system(f"obabel {ligand9_pdb} -O {ligand9_pdbqt}")
os.system(f"obabel {receptor_pdb} -O {receptor_pdbqt}")

os.remove(ligand8_pdb)
os.remove(ligand9_pdb)
os.remove(receptor_pdb)

print("Conversion completed.")
