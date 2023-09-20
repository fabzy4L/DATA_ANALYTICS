import os
import shutil

src_dir = '/Volumes/F4LHD'
dest_dir = '/Volumes/F4LHD/Articles'

# create the destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

# iterate through all the files in the source directory
for file_name in os.listdir(src_dir):
    # skip directories and non-png files
    if os.path.isdir(os.path.join(src_dir, file_name)) or not file_name.endswith(".pdf"):
        continue
    
    # move the PDF file to the destination directory
    shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir, file_name))
