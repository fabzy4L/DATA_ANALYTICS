import os

# Specify the directory containing the folders to be renamed
directory = '/Volumes/F4LHD/MISC'

for folder_name in os.listdir(directory):
    if not os.path.isdir(os.path.join(directory, folder_name)): # skip files
        continue
    if folder_name.startswith('.'):  # skip hidden files/folders
        continue
    new_name = folder_name.upper().replace(' ', '_').replace('[^a-zA-Z0-9_]', '')
    os.rename(os.path.join(directory, folder_name), os.path.join(directory, new_name))
    print(f"Renamed {folder_name} to {new_name}")