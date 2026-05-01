import openbabel

def convert_mol_to_pdb(mol_file, pdb_file):
    # Create the Open Babel molecule object
    ob_mol = openbabel.OBMol()

    # Read the MOL file
    ob_converter = openbabel.OBConversion()
    ob_converter.SetInFormat("mol")
    ob_converter.ReadFile(ob_mol, mol_file)

    # Write the molecule to PDB file
    ob_converter.SetOutFormat("pdb")
    ob_converter.WriteFile(ob_mol, pdb_file)

# Example usage:
convert_mol_to_pdb("input.mol", "output.pdb")
