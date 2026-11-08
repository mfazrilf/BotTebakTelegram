# Railway Deployment Guide

Panduan lengkap untuk deploy Telegram Quiz Bot ke Railway.

## Prerequisites

- Repository GitHub dengan bot code
- Railway.app account (gratis)
- Bot token dari BotFather (@BotFather di Telegram)

---

## Langkah 1: Persiapan GitHub

File `Procfile` sudah dibuat. Commit dan push ke GitHub:

```powershell
cd "filemu"
git add Procfile
git commit -m "Add Procfile for Railway worker"
git push origin main
```

---

## Langkah 2: Setup di Railway.app

### 2.1 Login & Create New Project
1. Buka https://railway.app
2. Login dengan GitHub account
3. Klik **"New Project"**
4. Pilih **"Deploy from GitHub repo"**
5. Pilih repository bot Anda (telegram-quiz-bot)
6. Railway akan auto-deploy

### 2.2 Setup Environment Variables
1. Setelah project created, masuk ke **Variables** tab
2. Klik **"New Variable"**
3. Add variable:
   - **Name:** `BOT_TOKEN`
   - **Value:** Paste bot token dari @BotFather (tanpa tanda kutip)
   
   Contoh:
   ```
   BOT_TOKEN = "token_kamu"
   ```
4. Klik **"Add"**

### 2.3 Verifikasi Deployment Settings
1. Buka **Deployments** tab
2. Klik service "bot-name" atau nama app Anda
3. Masuk ke tab **Settings**

#### Bagian: Build & Deploy
- Pastikan **Root Directory** kosong atau default
- Railway akan otomatis detect `Procfile`

#### Bagian: Networking
- **PENTING:** Hapus semua Public Port/Domain jika ada
- Bot Telegram tidak perlu HTTP port (gunakan polling, bukan webhook)
- Jika ada warning tentang "No exposed ports", itu NORMAL untuk bot polling

#### Verifikasi Custom Start Command (Optional)
- Buka **Deployment** tab
- Pastikan ada line: `worker: python main.py`
- Ini sudah tercantum di `Procfile`, so Railway akan automatically use it

---

## Langkah 3: Monitoring & Troubleshooting

### Cek Status Deploy
1. Dashboard Railway → Service bot Anda
2. Tab **Deployments**
3. Lihat status:
   - **Green check** = Deploy sukses, bot running
   - **Red X** = Ada error, bot crash

### Cek Logs untuk Error
1. Tab **Deployments**
2. Klik deployment paling atas (latest)
3. Klik **"View Logs"**
4. Scroll ke bawah untuk melihat error messages

### Common Error & Solusi

| Error | Solusi |
|-------|--------|
| `ModuleNotFoundError: No module named 'telegram'` | Run: `pip install -r requirements.txt` locally & push ke GitHub |
| `BOT_TOKEN not found` | Pastikan variable `BOT_TOKEN` sudah diset di Railway |
| `Connection refused` | Bot sedang mencoba connect ke Telegram, normal. Tunggu 1-2 menit |
| `Health check failed` | Hapus Public Port di Networking settings |

---

## Langkah 4: Test Bot

1. Buka Telegram
2. Cari bot Anda
3. Ketik `/start`
4. Jika ada response → Bot aktif di Railway! ✓

---

## Langkah 5: Persistent Data (Database)

File `trivia_game.db` disimpan di Railway's ephemeral filesystem.
Artinya database akan di-reset saat deploy/restart.

Untuk keep data persistent, upgrade ke Plan berbayar atau gunakan external database (PostgreSQL).

### Temporary Solution:
Database reset saat restart = game score hilang, tapi bot tetap berjalan.

---

## Tips Penting

1. **Monitor penggunaan** - Railway free tier ada batas jam
2. **Keep dependencies minimal** - Hindari library besar yang tidak perlu
3. **Update bot regularly** - Push change ke GitHub → Railway auto-redeploy
4. **Check logs regularly** - Tangkap error sebelum bot crash lama

---

## Jika Masih Crash

1. **Copy error message dari Railway logs**
2. **Cek requirements.txt** - Pastikan semua library tercantum:
   ```
   python-telegram-bot==20.7
   python-dotenv==1.0.0
   ```
3. **Cek BOT_TOKEN** - Pastikan valid & tidak expired
4. **Restart service** - Railway → Service → Restart Deploy
5. **Check Bot Father** - Pastikan bot masih aktif (tidak di-deactivate)

---

## Useful Railway Commands (via CLI)

Jika sudah install Railway CLI:

```bash
railway login
railway link
railway variables
railway logs
railway restart
```

---

**Selamat! Bot Anda sekarang berjalan di cloud 24/7!** 🚀
