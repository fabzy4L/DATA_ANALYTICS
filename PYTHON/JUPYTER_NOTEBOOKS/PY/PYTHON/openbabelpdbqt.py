import urllib.request
from openbabel import pybel

ligand8_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc8.pdb"
ligand9_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/thc9.pdb"
receptor_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/5tgz.pdb"

# Download the ligand 8 PDB file
ligand8_pdb = urllib.request.urlopen(ligand8_url).read().decode('utf-8')

# Convert ligand 8 to PDBQT format
molecule8 = next(pybel.readstring("pdb", ligand8_pdb))
pdbqt_output8 = molecule8.write("pdbqt")

# Save the converted ligand 8 PDBQT file
with open("ligand8.pdbqt", "w") as file:
    file.write(pdbqt_output8)

# Download the ligand 9 PDB file
ligand9_pdb = urllib.request.urlopen(ligand9_url).read().decode('utf-8')

# Convert ligand 9 to PDBQT format
molecule9 = next(pybel.readstring("pdb", ligand9_pdb))
pdbqt_output9 = molecule9.write("pdbqt")

# Save the converted ligand 9 PDBQT file
with open("ligand9.pdbqt", "w") as file:
    file.write(pdbqt_output9)

# Download the receptor PDB file
receptor_pdb = urllib.request.urlopen(receptor_url).read().decode('utf-8')

# Convert the receptor to PDBQT format
receptor_molecule = next(pybel.readstring("pdb", receptor_pdb))
pdbqt_output_receptor = receptor_molecule.write("pdbqt")

# Save the converted receptor PDBQT file
with open("receptor.pdbqt", "w") as file:
    file.write(pdbqt_output_receptor)

print("Conversion completed. PDB to PDBQT.")
