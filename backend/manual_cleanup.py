import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DW_FOLDER = os.path.join(BASE_DIR, "downloads")

def cleanupm():
    if os.path.exists(DW_FOLDER):
        shutil.rmtree(DW_FOLDER, ignore_errors=True)
    os.makedirs(DW_FOLDER, exist_ok=True)
    print("Downloads folder cleared")
