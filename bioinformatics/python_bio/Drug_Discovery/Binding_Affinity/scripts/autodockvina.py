from pathlib import Path
from subprocess import call

ROOT = Path(__file__).parent.parent
RECEPTOR_DIR = ROOT / "structures" / "receptor"
LIGANDS_DIR = ROOT / "structures" / "ligands"
CONFIG = ROOT / "docking" / "config" / "Config.txt"
OUTPUT = ROOT / "docking" / "outputs" / "output.pdbqt"

receptor_file = str(RECEPTOR_DIR / "receptor.pdb")
ligand_file = str(LIGANDS_DIR / "ligand.pdb")

receptor_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/5tgz.pdb"
call(["curl", "-o", receptor_file, receptor_url])

ligand_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/Tetrahydrocannabinol.pdb"
call(["curl", "-o", ligand_file, ligand_url])

call(["vina", "--receptor", receptor_file, "--ligand", ligand_file, "--config", str(CONFIG), "--out", str(OUTPUT)])
