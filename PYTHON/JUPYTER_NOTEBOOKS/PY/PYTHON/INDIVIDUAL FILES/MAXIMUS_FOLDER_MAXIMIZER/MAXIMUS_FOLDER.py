import os

# Specify the directory containing the folders to be renamed
directory = '/Users/f4L/Documents/GitHub/DATA_ANALYSIS/DATA_ANALYTICS/BIOSTATISTICS_COURSE_PROJECTS'

for folder_name in os.listdir(directory):
    if not os.path.isdir(os.path.join(directory, folder_name)): # skip files
        continue
    if folder_name.startswith('.'):  # skip hidden files/folders
        continue
    new_name = folder_name.upper().replace(' ', '_').replace('[^a-zA-Z0-9_]', '')
    os.rename(os.path.join(directory, folder_name), os.path.join(directory, new_name))
    print(f"Renamed {folder_name} to {new_name}")