import os

def relative_path(relative):
    return os.path.join(os.path.dirname(__file__), relative)
