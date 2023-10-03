import os
import shutil
from datetime import datetime

src_directory = '/Users/f4L/Desktop/newfolder'
for filename in os.listdir(src_directory):
    src_file = os.path.join(src_directory, filename)
    mod_time = os.path.getmtime(src_file)
    mod_datetime = datetime.fromtimestamp(mod_time)
    dest_directory = mod_datetime.strftime('/path/to/destination/directory/%Y/%m/')
    os.makedirs(dest_directory, exist_ok=True)
    dest_file = os.path.join(dest_directory, filename)
    shutil.copy(src_file, dest_file)

