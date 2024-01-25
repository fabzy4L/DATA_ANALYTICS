#MAXIMUS MAXIMIZER  - CAPS ALL FILE NAMES WITHIN A DIRECTORY, REMOVES SPACES 
# AVOIDS FILES WITH "." OR ".." NAMES

import os
import re

# Enter the folder path where the files are located
folder_path = '/Volumes/F4L3/AUDIOBOOKS/AUDIOBOOKS_MP3'

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a regular file (not a directory)
    if os.path.isfile(os.path.join(folder_path, filename)):
        # Split the filename into base and extension
        base, extension = os.path.splitext(filename)
        # Remove all non-alphanumeric characters (except periods) from the base component
        new_base = re.sub(r'[^a-zA-Z0-9.]', '', base).upper()
        # Rejoin the base and extension components to create the new filename
        new_filename = new_base + extension
        # Rename the file
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))