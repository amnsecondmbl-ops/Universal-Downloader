import os
import time
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DW_FOLDER = os.path.join(BASE_DIR, "downloads")

def cleanup_loop():
    while True:
        time.sleep(43200)
        try:
            if os.path.exists(DW_FOLDER):
                shutil.rmtree(DW_FOLDER, ignore_errors=True)
            os.makedirs(DW_FOLDER, exist_ok=True)
            print("Downloads folder cleared")
        except Exception as e:
            print("Error clearing downloads folder:", e)
