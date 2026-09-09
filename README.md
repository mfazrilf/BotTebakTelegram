# Telegram Bot Tebak-Tebakan 

Bot Telegram interaktif untuk bermain game tebak-tebakan dengan fitur mode grup dan solo, sistem poin, serta leaderboard.

## 📋 Fitur Utama

- **Mode Grup & Solo**: Bermain bersama di grup atau pribadi
- **Sistem Poin Real-time**: Update skor langsung setiap ada jawaban benar
- **Leaderboard**: Papan peringkat per grup/chat
- **Database Permanen**: Data tersimpan dengan SQLite
- **Error Handling Lengkap**: Bot tetap stabil meski ada error

##  Command

| Komando | Deskripsi |
|---------|-----------|
| `/start` | Tampilkan sambutan dan panduan |
| `/mulai` | Mulai ronde game baru |
| `/nyerah` | Akhiri ronde dan buka semua jawaban |
| `/next` | Lanjut ke soal berikutnya |
| `/skor` | Lihat leaderboard grup/chat |
| `/poin` | Lihat total poin personal |

##  Instalasi

### 1. Clone/Download Proyek
```bash
cd Bot_tebak_tele
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Bot Token
```bash
# Salin file .env.example
cp .env.example .env

# Edit .env dan masukkan token bot Telegram Anda
# BOT_TOKEN=your_actual_bot_token
```

### 4. Dapatkan Bot Token
1. Buka Telegram dan cari @BotFather
2. Ketik `/newbot` dan ikuti instruksi
3. Copy token yang diberikan
4. Paste di file `.env`

### 5. Jalankan Bot
```bash
python main.py
```

Bot akan mulai listening untuk pesan dan komando.

## 📝 Cara Bermain

1. Gunakan `/mulai` untuk memulai game
2. Bot akan menampilkan pertanyaan dengan slot kosong
3. Jawab pertanyaan di chat (tidak perlu komando)
4. Jika benar, nama Anda akan muncul di slot yang ter-isi dengan +1 poin
5. Ronde selesai otomatis saat semua slot terisi
6. Gunakan `/skor` untuk lihat leaderboard

##  Database

- Semua data skor disimpan di `trivia_game.db`
- Dihapus otomatis saat bot start (untuk demo)
- Gunakan kode untuk persistent storage di production

##  Struktur Proyek

```
Bot_tebak_tele/
├── main.py              # Kode utama bot (lengkap)
├── requirements.txt     # Dependencies Python
├── .env.example         # Template konfigurasi
└── README.md           # File ini
```

##  Troubleshooting

**Bot tidak response:**
- Pastikan token di `.env` benar
- Restart bot dengan `python main.py`

**Database error:**
- Hapus file `trivia_game.db`
- Jalankan ulang bot

**Import error:**
- Pastikan sudah run `pip install -r requirements.txt`
- Gunakan `pip install --upgrade pip`

##  Lisensi

Bebas digunakan untuk keperluan personal dan edukasi.
