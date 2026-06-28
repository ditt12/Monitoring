import os
import subprocess
 
ENV_FILE = ".env"
 
def set_env(key, value):
    lines = []
 
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()
 
    updated = False
 
    for i in range(len(lines)):
        if lines[i].startswith(key + "="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break
 
    if not updated:
        lines.append(f"{key}={value}\n")
 
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
 
def clear():
    os.system("cls" if os.name == "nt" else "clear")
 
clear()
 
bot_token = input("TOKEN BOT TELEGRAM: ")
chat_id = input("USER ID: ")
 
set_env("BOT_TOKEN", bot_token)
set_env("CHAT_ID", chat_id)
 
clear()
 
# auto execute monitoring.py
subprocess.run(["python", "monitoring.py"])
