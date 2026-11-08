# Git Setup Instructions

## Langkah 1: Initialize Git Repository

Buka PowerShell/Terminal di folder project dan jalankan:

```powershell
cd C:\Users\usermu\Documents\Bot_tebak_tele
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## Langkah 2: Add Files dan Create Commit

```powershell
git add .
git commit -m "Initial commit for Telegram Quiz Bot"
```

## Langkah 3: Setup Remote dan Push ke GitHub

### Option A: SSH (Recommended)
Jika sudah setup SSH key di GitHub:

```powershell
git remote add origin git@github.com:USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### Option B: HTTPS
Atau gunakan HTTPS:

```powershell
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Ganti USERNAME dan REPO_NAME dengan:
- **USERNAME**: Username GitHub Anda (contoh: fazril123)
- **REPO_NAME**: Nama repository (contoh: telegram-quiz-bot)

## Contoh Lengkap:

```powershell
git remote add origin https://github.com/fazril123/telegram-quiz-bot.git
git branch -M main
git push -u origin main
```

## Verifikasi

Setelah push berhasil, cek di GitHub:
- https://github.com/USERNAME/REPO_NAME

### File yang di-exclude (tidak ter-push):
- `.env` - Berisi bot token (sensitive)
- `trivia_game.db` - Database lokal
- `venv/` - Virtual environment
- `__pycache__/` - Cache Python

### File yang ter-push:
- `main.py` - Source code bot
- `requirements.txt` - Dependencies
- `.env.example` - Template config
- `README.md` - Dokumentasi
- `.gitignore` - Git config
