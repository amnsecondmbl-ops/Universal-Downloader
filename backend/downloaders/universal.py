import os
import shutil
import yt_dlp
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
BIN_DIR = os.path.join(BASE_DIR, "bin")
os.makedirs(BIN_DIR, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000").rstrip("/")

# Ensure ffmpeg.exe exists in backend/bin
FFMPEG_EXE = os.path.join(BIN_DIR, "ffmpeg.exe")
if not os.path.exists(FFMPEG_EXE):
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        try:
            shutil.copyfile(system_ffmpeg, FFMPEG_EXE)
        except Exception:
            pass
    if not os.path.exists(FFMPEG_EXE):
        try:
            import imageio_ffmpeg
            src = imageio_ffmpeg.get_ffmpeg_exe()
            if src and os.path.exists(src):
                shutil.copyfile(src, FFMPEG_EXE)
        except Exception:
            pass

def get_format_for_quality(quality):
    quality = str(quality).lower().strip()
    if quality in ("2160", "2160p", "4k"):
        return "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
    elif quality in ("1440", "1440p", "2k"):
        return "bestvideo[height<=1440]+bestaudio/best[height<=1440]/best"
    elif quality in ("1080", "1080p", "fhd"):
        return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
    elif quality in ("720", "720p", "hd"):
        return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
    elif quality in ("480", "480p"):
        return "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
    elif quality in ("360", "360p"):
        return "bestvideo[height<=360]+bestaudio/best[height<=360]/best"
    elif quality in ("audio", "mp3", "m4a"):
        return "bestaudio/best"
    else:
        # Default: Absolute highest quality available (4K/2K/1080p)
        return "bestvideo+bestaudio/best"

def download_anything(url, quality="best"):
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    format_str = get_format_for_quality(quality)
    is_audio = str(quality).lower().strip() in ("audio", "mp3", "m4a")

    target_folder_name = f"%(id)s_{quality}"
    output_template = os.path.join(DOWNLOADS_DIR, target_folder_name, "%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": format_str,
        "merge_output_format": "mp3" if is_audio else "mp4",
        "ffmpeg_location": BIN_DIR if os.path.exists(FFMPEG_EXE) else None,
        "socket_timeout": 60,
        "overwrites": True,
        "windowsfilenames": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        vid_id = info.get("id")
        title = info.get("title", "Video")
        resolution = info.get("resolution") or (f"{info.get('height')}p" if info.get('height') else "HD")

        actual_folder_name = f"{vid_id}_{quality}"
        folder_path = os.path.join(DOWNLOADS_DIR, actual_folder_name)

        if not os.path.exists(folder_path):
            return {
                "status": "error",
                "message": "Download directory not found"
            }, 500

        files = os.listdir(folder_path)
        media_extensions = (".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4a", ".mp3", ".opus")
        media_files = [f for f in files if f.lower().endswith(media_extensions)]

        if media_files:
            if is_audio:
                audio_files = [f for f in media_files if f.lower().endswith((".mp3", ".m4a"))]
                filename = audio_files[0] if audio_files else media_files[0]
            else:
                mp4_files = [f for f in media_files if f.lower().endswith(".mp4")]
                filename = mp4_files[0] if mp4_files else media_files[0]

            preview_url = f"{BASE_URL}/downloads/{actual_folder_name}/{filename}"
            download_url = f"{BASE_URL}/download/{actual_folder_name}/{filename}"

            return {
                "preview_url": preview_url,
                "download_url": download_url,
                "type": "Audio" if is_audio else "Video",
                "title": title,
                "resolution": resolution,
                "quality": quality
            }

        return {
            "status": "error",
            "message": "No media found after download"
        }, 500
