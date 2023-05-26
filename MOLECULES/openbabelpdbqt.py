import os
import urllib.request

# URLs of the PDB files
ligand8_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc8.pdb"
ligand9_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc9.pdb"
receptor_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/5tgz.pdb"

# Output file names
ligand8_pdbqt_file = "ligand8.pdbqt"
ligand9_pdbqt_file = "ligand9.pdbqt"
receptor_pdbqt_file = "receptor.pdbqt"

# Download PDB files
urllib.request.urlretrieve(ligand8_url, "ligand8.pdb")
urllib.request.urlretrieve(ligand9_url, "ligand9.pdb")
urllib.request.urlretrieve(receptor_url, "receptor.pdb")

# Convert PDB files to PDBQT format using obabel
os.system(f"obabel ligand8.pdb -O {ligand8_pdbqt_file}")
os.system(f"obabel ligand9.pdb -O {ligand9_pdbqt_file}")
os.system(f"obabel receptor.pdb -O {receptor_pdbqt_file}")

# Remove the original PDB files
os.remove("ligand8.pdb")
os.remove("ligand9.pdb")
os.remove("receptor.pdb")

print("Conversion completed.")
