import os

# Rename all .jpg files in a directory
path = '/Users/f4L/Desktop/igmock'
counter = 1
for file in os.listdir(path):
    if file.endswith('.jpg'):
        os.rename(os.path.join(path, file), os.path.join(path, f'script_{counter}.py'))
        counter += 1