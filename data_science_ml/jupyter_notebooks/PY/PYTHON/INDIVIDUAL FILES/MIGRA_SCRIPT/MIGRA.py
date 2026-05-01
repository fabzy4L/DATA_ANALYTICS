import os
import shutil

source_dir = '/Volumes/F4LHD/MISC'
dest_dir =  '/Volumes/F4LHD/MISC'

# Iterate over files in source directory
for file_name in os.listdir(source_dir):
    # Get the file extension
    file_extension = os.path.splitext(file_name)[1]

    # Check if file has extension
    if file_extension:
        # Create destination directory if it doesn't exist
        if not os.path.exists(os.path.join(dest_dir, file_extension[1:])):
            os.makedirs(os.path.join(dest_dir, file_extension[1:]))

        # Move file to destination directory
        try:
            shutil.move(os.path.join(source_dir, file_name), os.path.join(dest_dir, file_extension[1:], file_name))
        except FileNotFoundError:
            print(f"File not found: {file_name}")
            continue
