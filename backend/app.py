import os
import sys
import threading
from flask import Flask, request, redirect, session, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import yt_dlp
import instaloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from cleanup import cleanup_loop
from manual_cleanup import cleanupm
from downloaders.instagram import download_instagram
from downloaders.universal import download_anything
from db import log_download_async

print("Python:", sys.version)
print("yt-dlp:", yt_dlp.version.__version__)
print("Instaloader:", instaloader.__version__)

load_dotenv()
app = Flask(__name__)
CORS(app)

# Start background cleanup loop
threading.Thread(target=cleanup_loop, daemon=True).start()

DOWNLOADS_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

app.secret_key = os.getenv("APP_SECRET_KEY", "dev_secret_key_12345")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000").rstrip("/")
admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

# Admin page
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")

    if request.method == "POST":
        cleanupm()
        return "Downloads deleted"

    return '''
    <div style="
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background:#121212;
    font-family:Arial;
    ">
        <form method="POST">
            <button style="
            padding:15px 25px;
            border:none;
            border-radius:10px;
            background:red;
            color:white;
            font-size:18px;
            cursor:pointer;
            ">
                Delete All Downloads
            </button>
        </form>
    </div>
    <a href="/logout">
        <button>Logout</button>
    </a>
    '''

# Admin Login page
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        entered_password = request.form.get("password")
        if entered_password == admin_password:
            session["admin"] = True
            return redirect("/admin")
        return "Wrong password"

    return '''
    <div style="
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:Arial;
    background:#121212;
    color:white;
    ">
        <form method="POST" style="
        display:flex;
        flex-direction:column;
        gap:10px;
        background:#1e1e1e;
        padding:30px;
        border-radius:15px;
        width:300px;
        ">
            <h2 style="margin:0;text-align:center;">Admin Login</h2>
            <input 
            type="password" 
            name="password"
            placeholder="Enter password"
            style="
            padding:10px;
            border-radius:10px;
            border:none;
            outline:none;
            "
            />
            <button type="submit" style="
            padding:10px;
            border:none;
            border-radius:10px;
            background:#0095f6;
            color:white;
            font-weight:bold;
            cursor:pointer;
            ">
                Login
            </button>
        </form>
    </div>
    '''

# Logout admin sesh
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin-login")

# Home page
@app.route("/")
def home():
    return "Server running"

# Sending file to frontend only for preview
@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(
        DOWNLOADS_FOLDER,
        filename
    )

# Sends file to frontend as attachment (So only downloadable file)
@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(
        DOWNLOADS_FOLDER,
        filename,
        as_attachment=True
    )

def get_platform(url):
    url_lower = url.lower()
    if "instagram.com" in url_lower:
        return "Instagram"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "YouTube"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower:
        return "Facebook"
    elif "tiktok.com" in url_lower:
        return "TikTok"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "Twitter / X"
    return "Other"

# Actual fetching mechanism (gives url to the frontend)
@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    quality = data.get("quality", "best")
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")

    if not url:
        return jsonify({
            "status": "error",
            "message": "URL is required"
        }), 400

    platform = get_platform(url)

    try:
        if "instagram.com" in url.lower():
            result = download_instagram(url)
        else:
            result = download_anything(url, quality=quality)

        res_dict = result[0] if isinstance(result, tuple) else result
        status_code = result[1] if isinstance(result, tuple) else 200

        # Log to Supabase
        if status_code == 200 and isinstance(res_dict, dict) and res_dict.get("status") != "error":
            log_download_async({
                "original_url": url,
                "platform": platform,
                "title": res_dict.get("title", ""),
                "media_type": res_dict.get("type", "Media"),
                "requested_quality": quality,
                "resolved_resolution": res_dict.get("resolution", ""),
                "status": "success",
                "client_ip": client_ip,
                "user_agent": user_agent
            })
        else:
            log_download_async({
                "original_url": url,
                "platform": platform,
                "requested_quality": quality,
                "status": "failed",
                "error_message": res_dict.get("message", "Download error") if isinstance(res_dict, dict) else "Error",
                "client_ip": client_ip,
                "user_agent": user_agent
            })

        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    except Exception as e:
        error_message = str(e)
        print("Fetch error:", error_message)

        # Log failed attempt to Supabase
        log_download_async({
            "original_url": url,
            "platform": platform,
            "requested_quality": quality,
            "status": "failed",
            "error_message": error_message,
            "client_ip": client_ip,
            "user_agent": user_agent
        })

        if "Read timed out" in error_message:
            return jsonify({
                "status": "error",
                "message": "Server took too long to respond. Please try again."
            }), 500
        return jsonify({
            "status": "error",
            "message": f"Unable to fetch media: {error_message}"
        }), 500

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
