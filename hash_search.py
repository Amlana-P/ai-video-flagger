from PIL import Image
import imagehash

def compute_hash(frame_path):

    img = Image.open(frame_path)

    return str(imagehash.phash(img))