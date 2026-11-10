import os
import threading
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kjbjueolpjdadruzkxei.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected to Supabase project:", SUPABASE_URL)
    except Exception as e:
        print("Error initializing Supabase client:", e)
else:
    print("Supabase credentials pending: set SUPABASE_KEY in backend/.env")

def log_download_async(record_data):
    """
    Inserts download tracking data into Supabase asynchronously in a background
    thread so the user's download request returns instantly without any latency.
    """
    def _insert():
        if not supabase_client:
            return
        try:
            supabase_client.table("download_records").insert(record_data).execute()
        except Exception as e:
            print("Supabase log error:", e)

    threading.Thread(target=_insert, daemon=True).start()

