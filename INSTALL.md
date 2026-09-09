# PANDUAN INSTALASI LENGKAP BOT TEBAK-TEBAKAN 🎯

## 📋 Prasyarat
- Python 3.9 atau lebih tinggi
- Pip (Python package manager)
- Akun Telegram
- Bot token dari @BotFather

## ⚙️ LANGKAH-LANGKAH INSTALASI

### 1. Persiapan Awal

#### Windows (PowerShell/Command Prompt):
```powershell
# Buka folder proyek
cd C:\Users\YourUsername\Documents\Bot_tebak_tele

# Buat virtual environment (opsional tapi recommended)
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux (Terminal):
```bash
cd ~/Documents/Bot_tebak_tele

# Buat virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.0
```

### 3. Dapatkan Bot Token

1. Buka Telegram dan cari chat **@BotFather**
2. Ketik perintah: `/newbot`
3. Ikuti instruksi:
   - Beri nama bot (contoh: "Tebak Tebakan Bot")
   - Beri username bot (contoh: "tebak_tebakan_bot")
4. BotFather akan memberikan token, contoh: `1234567890:ABCDEFGHijklmnopqrstuvwxyz1234567890`
5. **Jangan bagikan token ini kepada siapapun!**

### 4. Setup File Konfigurasi

#### Windows:
```powershell
# Buka file .env.example dengan editor
notepad .env.example

# Atau gunakan PowerShell
code .env.example
```

#### macOS/Linux:
```bash
nano .env.example
# atau
code .env.example
```

**Edit isi file:**
```
BOT_TOKEN=1234567890:ABCDEFGHijklmnopqrstuvwxyz1234567890
```

**Ubah nama file dari `.env.example` menjadi `.env`**

#### Windows:
```powershell
Rename-Item .env.example .env
```

#### macOS/Linux:
```bash
mv .env.example .env
```

### 5. Jalankan Bot

```bash
python main.py
```

Jika berhasil, akan muncul:
```
2025-01-20 14:30:45,123 - root - INFO - ✓ Database initialized successfully
2025-01-20 14:30:46,789 - root - INFO - 🤖 Bot dimulai...
```

## 🎮 Testing Bot

1. Buka Telegram
2. Cari username bot Anda (contoh: @tebak_tebakan_bot)
3. Klik `/start` atau ketik manual
4. Ikuti instruksi: `/mulai` untuk memulai game

## 📂 Struktur File

```
Bot_tebak_tele/
├── main.py                 # Program utama bot (2000+ baris)
├── requirements.txt        # Daftar library yang diperlukan
├── .env                    # Konfigurasi (dibuat dari .env.example)
├── .env.example            # Template konfigurasi
├── INSTALL.md              # File ini
├── README.md               # Dokumentasi umum
└── trivia_game.db          # Database SQLite (auto-created)
```

## 🔧 Troubleshooting

### Masalah: "BOT_TOKEN tidak ditemukan"
**Solusi:**
- Pastikan file `.env` ada (bukan `.env.example`)
- Pastikan format: `BOT_TOKEN=your_token_here`
- Pastikan tidak ada spasi sebelum/sesudah tanda `=`

### Masalah: "ImportError: No module named 'telegram'"
**Solusi:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Masalah: "ModuleNotFoundError: No module named 'dotenv'"
**Solusi:**
```bash
pip install python-dotenv==1.0.0
```

### Masalah: Bot tidak merespons pesan
**Solusi:**
1. Pastikan bot sedang running (lihat terminal)
2. Restart bot: Ctrl+C lalu jalankan lagi `python main.py`
3. Cek bot token di `.env` sudah benar
4. Pastikan internet connection stabil

### Masalah: "sqlite3.OperationalError"
**Solusi:**
```bash
# Hapus database lama
del trivia_game.db  # Windows
rm trivia_game.db   # macOS/Linux

# Jalankan ulang bot
python main.py
```

### Masalah: "Ctrl+C tidak menghentikan bot (Windows)"
**Solusi:**
- Tekan `Ctrl+C` lalu Enter
- Atau tutup terminal window langsung

## 📊 Database & Storage

Bot menggunakan SQLite untuk menyimpan:
- **Skor user** per grup/chat
- **Histori jawaban** per ronde
- **State game** untuk setiap chat

File database: `trivia_game.db` (auto-created)

Database akan di-reset setiap kali bot di-restart (untuk demo). Untuk production, uncomment line di `init_database()`.

## 🚀 Advanced Usage

### Menjalankan Bot di Background (Linux/macOS)

```bash
# Menggunakan nohup
nohup python main.py > bot.log 2>&1 &

# Menggunakan screen
screen -S tebak-bot
python main.py
# Tekan Ctrl+A lalu D untuk exit

# Kembali ke screen
screen -r tebak-bot
```

### Menjalankan Bot di Background (Windows)

```powershell
# Menggunakan Task Scheduler
# Atau gunakan PowerShell Job:
Start-Job -ScriptBlock {
    cd C:\Users\YourUsername\Documents\Bot_tebak_tele
    python main.py
}
```

### Monitoring Bot

```bash
# Lihat log real-time
tail -f bot.log

# Atau jalankan dengan logging verbose
python main.py 2>&1 | tee bot.log
```

## 💡 Tips & Trik

1. **Disable read receipts di Telegram** untuk UX yang lebih baik
2. **Invite bot ke grup** dengan mengklik `/start` terlebih dahulu
3. **Customize soal** dengan edit array `QUIZ_DATA` di `main.py`
4. **Backup database**: `cp trivia_game.db trivia_game.db.backup`
5. **Multiple bots**: Buat beberapa bot dengan token berbeda

## 📚 Dokumentasi Lengkap

- [Python Telegram Bot Docs](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 🆘 Butuh Bantuan?

1. Baca komentar di code `main.py`
2. Cek log output di terminal
3. Lihat section Troubleshooting di atas
4. Pastikan Python version 3.9+: `python --version`

## ✅ Checklist Pre-Launch

- [ ] Python 3.9+ terinstall
- [ ] File `requirements.txt` tersedia
- [ ] Bot token sudah didapat dari @BotFather
- [ ] File `.env` dibuat dan berisi token
- [ ] `pip install -r requirements.txt` sudah dijalankan
- [ ] Test `/start` command
- [ ] Test `/mulai` command untuk mulai game
- [ ] Database `trivia_game.db` ter-create
- [ ] Jawab pertanyaan test di game
- [ ] `/skor` menampilkan hasil dengan benar

---

**Bot siap digunakan! 🎉**

Selamat bermain dan enjoy tebak-tebakan bersama teman-teman! 🚀
