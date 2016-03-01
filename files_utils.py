import os
import mimetypes
from logging import getLogger

logger = getLogger('pydirl')

def get_file_size(path):
    return os.path.getsize(path)


def get_folder_size(path):
    files_num = 0
    size = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            files_num += 1
            fPath = os.path.join(root, name)
            #do not count size of link
            if not os.path.islink(fPath):
                try:
                    size += os.path.getsize(fPath)
                except OSError as e:
                    logger.exception(e)
    return size, files_num

def get_file_mimetype(path):
    return mimetypes.guess_type(path)[0]
