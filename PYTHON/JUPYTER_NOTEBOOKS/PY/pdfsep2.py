import os
import shutil

src_dir = '/Volumes/F4L3/DOWNLOADS 053022'
dest_dir = '/Volumes/F4L3/EBOOKS/IMAGES'

# create destination directory if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for file_name in os.listdir(src_dir):
    # check if file is a PDF
    if file_name.lower().endswith('.png'):
        # check if file exists in source directory
        if os.path.exists(os.path.join(src_dir, file_name)):
            shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir, file_name))
        else:
            print(f"File {file_name} not found in source directory.")
