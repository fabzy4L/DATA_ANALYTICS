import os
import shutil

# Define the source directory
src_dir = '/Users/f4L/Desktop/newfolder'

# Define the destination directories for each file type
dest_dir_images = '/Users/f4L/Desktop/newfolder/IMAGES'
dest_dir_docs = '/Users/f4L/Desktop/newfolder/DOCS'
dest_dir_videos = '/Users/f4L/Desktop/newfolder/VIDEOS'
dest_dir_music = '/Users/f4L/Desktop/newfolder/MUSIC'
dest_dir_other = '/Users/f4L/Desktop/newfolder/OTHER'

# Loop through all files in the source directory
for file_name in os.listdir(src_dir):
    # Get the file extension
    file_ext = os.path.splitext(file_name)[1].lower()

    # Move the file to the appropriate destination directory based on its extension
    if file_ext in ('.jpg', '.jpeg', '.png', '.gif'):
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir_images, file_name))
    elif file_ext in ('.doc', '.docx', '.pdf', '.txt'):
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir_docs, file_name))
    elif file_ext in ('.mp4', '.avi', '.mov', '.wmv'):
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir_videos, file_name))
    elif file_ext in ('.mp3', '.wav', '.flac'):
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir_music, file_name))
    else:
        shutil.move(os.path.join(src_dir, file_name), os.path.join(dest_dir_other, file_name))
