#!/bin/bash
# Quick Start Script untuk Bot Tebak-Tebakan
# Jalankan: chmod +x quick_start.sh && ./quick_start.sh

echo "🎯 QUICK START BOT TEBAK-TEBAKAN"
echo "================================="
echo ""

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 tidak terinstall. Silakan install dari python.org"
    exit 1
fi

python_version=$(python3 --version)
echo "  $python_version"
echo ""

# Create virtual environment
echo "✓ Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Activated"
echo ""

# Install requirements
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  Dependencies installed"
echo ""

# Check .env file
echo "✓ Checking .env configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "  .env created from .env.example"
        echo "  ⚠️  PENTING: Edit .env dan masukkan BOT_TOKEN Anda!"
        echo ""
        read -p "Tekan Enter untuk edit .env (atau Ctrl+C untuk cancel)..."
        nano .env
    else
        echo "  ❌ .env.example tidak ditemukan"
        exit 1
    fi
else
    echo "  .env already exists"
fi
echo ""

# Verify token
echo "✓ Verifying BOT_TOKEN..."
if grep -q "BOT_TOKEN=" .env && ! grep -q "your_token_here" .env; then
    echo "  ✓ BOT_TOKEN looks good"
else
    echo "  ⚠️  BOT_TOKEN not configured properly"
    echo "  Edit .env dan ganti 'your_token_here' dengan token bot Anda"
    exit 1
fi
echo ""

# Run bot
echo "🤖 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""
python main.py
