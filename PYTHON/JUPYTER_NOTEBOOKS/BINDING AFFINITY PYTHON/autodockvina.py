from subprocess import call

# Define file paths
receptor_file = "receptor.pdb"
ligand_file = "ligand.pdb"

# Download the receptor file
receptor_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/5tgz.pdb"
call(["curl", "-o", receptor_file, receptor_url])

# Download the ligand file
ligand_url = "https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/MOLECULES/Tetrahydrocannabinol.pdb"
call(["curl", "-o", ligand_file, ligand_url])

# Run AutoDock Vina
call(["vina", "--receptor", receptor_file, "--ligand", ligand_file, "--config", "config.txt", "--out", "output.pdbqt"])
