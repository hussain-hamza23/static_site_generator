import os
import shutil


def copy_contents(src: str, dst: str):
    try:
        if not os.path.exists(dst):
            os.mkdir(dst)
    except OSError as e:
        print(f"Error creating destination folder: {e}")

    try:
        for item in os.listdir(src):
            source_path = os.path.join(src, item)
            destination_path = os.path.join(dst, item)
            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
                print(f"Copied file {item} to destination {destination_path}")
            else:
                copy_contents(source_path, destination_path)
    except OSError as e:
        print(f"Error copying files: {e}")
