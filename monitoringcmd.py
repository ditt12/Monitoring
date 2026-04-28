import requests
import time
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN / CHAT_ID belum diisi di .env")
    exit()

start_time = time.time()
last_update_id = None

# ================= TELEGRAM =================

def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

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

# ================= SCREENSHOT =================

def take_screenshot(path):
    result = subprocess.run(
        ["su", "-c", f"/system/bin/screencap -p {path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0, result.stderr.decode()

# ================= STATUS =================

def build_status():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = int(time.time() - start_time)

    return f"""📡 Cloud Phone Active
🕒 Time: {now}
⏱️ Uptime: {uptime//3600} jam {(uptime%3600)//60} menit {uptime%60} detik
"""

def send_ping():
    send_text("🏓 PING OK\n" + build_status())

def send_status():
    msg = build_status()
    path = "/sdcard/screen.png"

    success, err = take_screenshot(path)

    if not success:
        send_text(f"⚠️ Screenshot error:\n{err}")
    else:
        time.sleep(2)
        send_text(msg)
        send_photo(path)

def send_screenshot_only():
    path = "/sdcard/screen.png"

    success, err = take_screenshot(path)

    if not success:
        send_text(f"⚠️ Screenshot error:\n{err}")
    else:
        time.sleep(2)
        send_photo(path)

def send_start():
    msg = """🤖 Bot Aktif

📌 Command:
• /ping → cek status cepat
• /check → status + screenshot
• /screenshot → hanya screenshot

"""
    send_text(msg)

# ================= TELEGRAM COMMAND =================

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 10}

    if last_update_id:
        params["offset"] = last_update_id + 1

    res = requests.get(url, params=params).json()
    return res.get("result", [])

def handle_commands():
    global last_update_id
    updates = get_updates()
    cmds = []

    for update in updates:
        last_update_id = update["update_id"]

        message = update.get("message", {})
        text = message.get("text", "")

        if text == "/check":
            cmds.append("check")
        elif text == "/ping":
            cmds.append("ping")
        elif text == "/screenshot":
            cmds.append("screenshot")
        elif text == "/start":
            cmds.append("start")

    return cmds

# ================= LOOP =================

last_heartbeat = 0

while True:
    cmds = handle_commands()

    for cmd in cmds:
        if cmd == "ping":
            send_ping()
        elif cmd == "check":
            send_status()
        elif cmd == "screenshot":
            send_screenshot_only()
        elif cmd == "start":
            send_start()

    # heartbeat 1 jam
    if time.time() - last_heartbeat >= 3600:
        send_status()
        last_heartbeat = time.time()

    time.sleep(5)
