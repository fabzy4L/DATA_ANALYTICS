#MAXIMUS MAXIMIZER  - CAPS ALL FILE NAMES WITHIN A DIRECTORY, REMOVES SPACES 


import os

# Enter the folder path where the files are located
folder_path = '/Volumes/F4L3/AUDIOBOOKS'

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a regular file (not a directory)
    if os.path.isfile(os.path.join(folder_path, filename)):
        # Split the filename into base and extension
        base, extension = os.path.splitext(filename)
        # Rename the file by replacing spaces with underscores and converting to uppercase
        new_base = base.replace(' ', '_').upper()
        new_filename = new_base + extension
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
