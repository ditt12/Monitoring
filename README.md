# 📡 Cloud Activity Tracker (Termux + Telegram)

Script ini digunakan untuk: - Mengirim notifikasi ke Telegram tiap
interval tertentu - Menampilkan waktu eksekusi (timestamp) - Menampilkan
uptime script - Mengirim screenshot layar (via root)

------------------------------------------------------------------------

## ⚙️ Requirement

-   Android / Cloud Phone (disarankan root)
-   Termux (versi F-Droid / GitHub, bukan Play Store)
-   Python
-   Akses internet
-   Telegram bot

------------------------------------------------------------------------

## 🤖 Setup Telegram Bot

1.  Buka Telegram

2.  Cari @BotFather

3.  Jalankan: /newbot

4.  Simpan BOT_TOKEN

5.  Ambil CHAT_ID:

    -   Kirim pesan ke bot @MissRose_bot
    -   Kirim pesan ke bot Rose /info
    -   Salin ID

------------------------------------------------------------------------

## 📦 Install di Termux

```bash
pkg update && pkg upgrade -y && pkg install -y termux-api tsu git python ffmpeg && git clone https://github.com/ditt12/monitoring && cd monitoring && pip install -r requirements.txt && python setconfig.py
```

and run this shit
```bash
python monitoring.py
```

(Optional) termux-wake-lock

------------------------------------------------------------------------

## 🔐 Pastikan Root Aktif

su -c "whoami"

Output harus: root

------------------------------------------------------------------------

## 🔍 Test Screenshot

su -c "/system/bin/screencap -p /sdcard/test.png"

------------------------------------------------------------------------

## ▶️ Menjalankan Script

python monitoring.ph

------------------------------------------------------------------------

## ⛔ Stop Script

pkill -f python

------------------------------------------------------------------------

## ❗ Troubleshooting

-   Screenshot gagal → cek root & command screencap
-   Bot tidak kirim → cek token & chat id
-   Interval tidak berubah → kill semua proses python

------------------------------------------------------------------------

## 📌 Kesimpulan

Monitoring sederhana berbasis Termux + Telegram + screenshot.
