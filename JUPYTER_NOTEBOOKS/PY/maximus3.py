import os
import re

# Enter the folder path where the files are located
folder_path = '/Users/f4L/Documents/GitHub/Python/INDIVIDUAL FILES'

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Skip hidden files and filenames that are equal to '.' or '..'
    if filename.startswith('.') or filename == '.' or filename == '..':
        continue
    # Check if the file is a regular file (not a directory)
    if os.path.isfile(os.path.join(folder_path, filename)):
        # Split the filename into base and extension
        base, extension = os.path.splitext(filename)
        # Replace spaces with underscores in the base component
        new_base = base.replace(' ', '_')
        # Remove all non-alphanumeric characters (except periods and underscores) from the base component
        new_base = re.sub(r'[^a-zA-Z0-9._]', '', new_base).upper()
        # Rejoin the base and extension components to create the new filename
        new_filename = new_base + extension
        # Rename the file
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))