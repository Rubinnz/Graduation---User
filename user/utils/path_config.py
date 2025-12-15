import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
IMG_DIR = os.path.join(BASE_DIR, "images")

def img(path):
    return os.path.join(IMG_DIR, path)
