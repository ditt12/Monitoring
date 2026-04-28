import requests
import time
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

# load .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN / CHAT_ID belum diisi di .env")
    exit()

start_time = time.time()

def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        print("❌ Gagal kirim pesan")

def send_photo(path):
    if not os.path.exists(path):
        send_text("⚠️ Screenshot gagal (file tidak ada)")
        return
    
    if os.path.getsize(path) < 1000:
        send_text("⚠️ Screenshot kosong")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(path, "rb") as f:
            requests.post(url, files={"photo": f}, data={"chat_id": CHAT_ID}, timeout=20)
    except:
        send_text("⚠️ Gagal kirim screenshot")

def take_screenshot(path):
    result = subprocess.run(
        ["su", "-c", f"/system/bin/screencap -p {path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0, result.stderr.decode()

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = int(time.time() - start_time)

    msg = f"""📡 Cloud Phone Active
🕒 Time: {now}
⏱️ Uptime: {uptime//3600} jam {(uptime%3600)//60} menit {uptime%60} detik
"""

    path = "/sdcard/screen.png"

    success, err = take_screenshot(path)

    if not success:
        send_text(f"⚠️ Screenshot error:\n{err}")
    else:
        time.sleep(2)
        send_text(msg)
        send_photo(path)

    time.sleep(3600)
