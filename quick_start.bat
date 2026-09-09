@echo off
REM Quick Start Script untuk Bot Tebak-Tebakan (Windows)
REM Jalankan: quick_start.bat

echo.
echo 🎯 QUICK START BOT TEBAK-TEBAKAN
echo =================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak terinstall atau tidak di PATH
    echo Silakan install dari python.org dan tambahkan ke PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do (
    echo   Python %%i
)
echo.

REM Create virtual environment
echo ✓ Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   Virtual environment created
) else (
    echo   Virtual environment already exists
)
echo.

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat
echo   Activated
echo.

REM Install requirements
echo ✓ Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Error installing dependencies
    echo Coba: pip install --upgrade pip
    pause
    exit /b 1
)
echo   Dependencies installed
echo.

REM Check .env file
echo ✓ Checking .env configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo   .env created from .env.example
        echo.
        echo   ⚠️  PENTING: Edit .env dan masukkan BOT_TOKEN Anda!
        echo.
        echo Buka .env dengan editor favorit Anda dan ganti:
        echo   BOT_TOKEN=your_token_here
        echo dengan token bot Anda dari @BotFather
        echo.
        pause
        start notepad .env
        echo Setelah selesai edit, tutup file dan jalankan script ini lagi
        pause
        exit /b 0
    ) else (
        echo   ❌ .env.example tidak ditemukan
        exit /b 1
    )
) else (
    echo   .env already exists
)
echo.

REM Verify token
echo ✓ Verifying BOT_TOKEN...
findstr /M "BOT_TOKEN=" .env >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  BOT_TOKEN not found in .env
    exit /b 1
)
findstr /M "your_token_here" .env >nul 2>&1
if not errorlevel 1 (
    echo   ⚠️  BOT_TOKEN still contains placeholder "your_token_here"
    echo   Edit .env dan masukkan token bot Anda
    pause
    exit /b 1
)
echo   ✓ BOT_TOKEN looks good
echo.

REM Run bot
echo 🤖 Starting bot...
echo Press Ctrl+C to stop
echo.
python main.py

pause
