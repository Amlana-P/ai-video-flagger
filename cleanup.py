import shutil
import os

def cleanup():

    if os.path.exists("frames"):
        shutil.rmtree("frames")

    if os.path.exists("uploads"):
        shutil.rmtree("uploads")

    os.makedirs("frames",exist_ok=True)
    os.makedirs("uploads",exist_ok=True)