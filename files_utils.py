import os
import mimetypes

def get_file_size(path):
    return os.path.getsize(path)


def get_folder_size(path):
    files_num = 0
    size = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            files_num += 1
            size += os.path.getsize(os.path.join(root, name))
    return size, files_num

def get_file_mimetype(path):
    return mimetypes.guess_type(path)[0]
