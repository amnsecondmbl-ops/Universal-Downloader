import os
import re
import instaloader
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000").rstrip("/")

def extract_instagram_shortcode(url):
    match = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    clean_url = url.split("?")[0].rstrip("/")
    parts = [p for p in clean_url.split("/") if p]
    if parts:
        return parts[-1]
    return None

def download_instagram(url):
    loader = instaloader.Instaloader(
        dirname_pattern=os.path.join(DOWNLOADS_DIR, "{target}"),
        download_video_thumbnails=False,
        save_metadata=False,
        post_metadata_txt_pattern=""
    )

    sc = extract_instagram_shortcode(url)
    if not sc:
        return {
            "status": "error",
            "message": "Invalid Instagram URL"
        }, 400

    folder_name = os.path.join(DOWNLOADS_DIR, sc)

    if not os.path.exists(folder_name):
        post = instaloader.Post.from_shortcode(loader.context, sc)
        loader.download_post(post, target=sc)

    if not os.path.exists(folder_name):
        return {
            "status": "error",
            "message": "Failed to download Instagram post"
        }, 500

    all_files = os.listdir(folder_name)
    mp4_files = sorted([f for f in all_files if f.lower().endswith(".mp4")])
    jpg_files = sorted([f for f in all_files if f.lower().endswith((".jpg", ".jpeg"))])

    if mp4_files:
        filename = mp4_files[0]
        return {
            "download_url": f"{BASE_URL}/download/{sc}/{filename}",
            "preview_url": f"{BASE_URL}/downloads/{sc}/{filename}",
            "type": "Video"
        }
    elif jpg_files:
        if len(jpg_files) == 1:
            filename = jpg_files[0]
            return {
                "download_url": f"{BASE_URL}/download/{sc}/{filename}",
                "preview_url": f"{BASE_URL}/downloads/{sc}/{filename}",
                "type": "Post"
            }
        else:
            down_path_jpgs = [f"{BASE_URL}/download/{sc}/{f}" for f in jpg_files]
            file_path_jpgs = [f"{BASE_URL}/downloads/{sc}/{f}" for f in jpg_files]
            return {
                "download_urls": down_path_jpgs,
                "preview_urls": file_path_jpgs,
                "type": "Posts"
            }
    else:
        return {
            "status": "error",
            "message": "No media found"
        }, 500
