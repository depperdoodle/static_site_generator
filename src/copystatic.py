import os
import shutil


def clean_copy(src, dst):
    for item in os.listdir(src):
        from_path = os.path.join(src, item)
        to_path = os.path.join(dst, item)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            os.mkdir(to_path)
            clean_copy(from_path, to_path)