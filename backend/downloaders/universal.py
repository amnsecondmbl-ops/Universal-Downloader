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
COOKIES_FILE = os.path.join(BASE_DIR, "cookies.txt")

def ensure_cookies():
    """Extract cookies from environment variable if configured (for Render / cloud)."""
    env_cookies = os.getenv("YOUTUBE_COOKIES")
    if env_cookies and not os.path.exists(COOKIES_FILE):
        try:
            with open(COOKIES_FILE, "w", encoding="utf-8") as f:
                f.write(env_cookies.strip())
        except Exception as e:
            print("Warning creating cookies.txt from env:", e)

# Locate FFmpeg binary (Windows, Linux, macOS)
FFMPEG_PATH = shutil.which("ffmpeg")

if not FFMPEG_PATH:
    try:
        import imageio_ffmpeg
        src = imageio_ffmpeg.get_ffmpeg_exe()
        if src and os.path.exists(src):
            bin_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
            bin_target = os.path.join(BIN_DIR, bin_name)
            if not os.path.exists(bin_target):
                shutil.copyfile(src, bin_target)
                if os.name != "nt":
                    os.chmod(bin_target, 0o755)
            FFMPEG_PATH = BIN_DIR
    except Exception as e:
        print("Warning locating FFmpeg:", e)

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
        return "bestvideo+bestaudio/best"

def _run_ytdlp(url, ydl_opts, actual_folder_name, is_audio, quality):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        vid_id = info.get("id")
        title = info.get("title", "Video")
        resolution = info.get("resolution") or (f"{info.get('height')}p" if info.get('height') else "HD")

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

def download_anything(url, quality="best"):
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    ensure_cookies()

    format_str = get_format_for_quality(quality)
    is_audio = str(quality).lower().strip() in ("audio", "mp3", "m4a")

    target_subfolder = f"%(id)s_{quality}"
    output_template = os.path.join(DOWNLOADS_DIR, target_subfolder, "%(id)s.%(ext)s")

    base_opts = {
        "outtmpl": output_template,
        "format": format_str,
        "merge_output_format": "mp3" if is_audio else "mp4",
        "ffmpeg_location": FFMPEG_PATH,
        "socket_timeout": 60,
        "overwrites": True,
        "windowsfilenames": True,
        "noplaylist": True,
        "quiet": True,
    }

    if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
        base_opts["cookiefile"] = COOKIES_FILE

    proxy = os.getenv("PROXY_URL") or os.getenv("HTTP_PROXY")
    if proxy:
        base_opts["proxy"] = proxy

    # Tier 1: Try optimal high-resolution extraction
    try:
        ydl_opts_t1 = dict(base_opts)
        with yt_dlp.YoutubeDL(ydl_opts_t1) as ydl_t1:
            probe_info = ydl_t1.extract_info(url, download=False)
            actual_folder_name = f"{probe_info.get('id')}_{quality}"

        return _run_ytdlp(url, ydl_opts_t1, actual_folder_name, is_audio, quality)

    except Exception as e1:
        err_msg = str(e1).lower()
        print("Tier 1 extraction failed:", err_msg)

        # If blocked by YouTube bot-check on cloud datacenter IP, activate Tier 2
        if any(keyword in err_msg for keyword in ("sign in", "bot", "confirm", "403", "forbidden", "restricted")):
            print("Activating Tier 2 cloud bypass extractor (android client)...")
            try:
                ydl_opts_t2 = dict(base_opts)
                ydl_opts_t2["extractor_args"] = {
                    "youtube": {
                        "player_client": ["android"]
                    }
                }
                # Format that android client supports reliably without bot blocks
                ydl_opts_t2["format"] = "best/18"

                with yt_dlp.YoutubeDL(ydl_opts_t2) as ydl_t2:
                    probe_info2 = ydl_t2.extract_info(url, download=False)
                    actual_folder_name = f"{probe_info2.get('id')}_{quality}"

                return _run_ytdlp(url, ydl_opts_t2, actual_folder_name, is_audio, quality)

            except Exception as e2:
                print("Tier 2 extraction failed:", e2)
                raise e2
        else:
            raise e1
