import pymol

def convert_mol_to_pdb(mol_file, pdb_file):
    # Initialize PyMOL
    pymol.finish_launching()

    # Load the MOL file
    pymol.cmd.load(mol_file)

    # Save the loaded molecule as PDB
    pymol.cmd.save(pdb_file)

    # Quit PyMOL
    pymol.cmd.quit()

# Example usage:
convert_mol_to_pdb("input.mol", "output.pdb")
