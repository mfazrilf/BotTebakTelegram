#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram Quiz Bot

Quiz bot with score system and leaderboard per chat.
Run: pip install -r requirements.txt
"""

import os
import sys
import sqlite3
import logging
import asyncio
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict

# Import telegram
from telegram import Update, Chat, User, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from telegram.error import TelegramError
from telegram.constants import ChatAction

# Import dotenv
from dotenv import load_dotenv

# Logging configuration

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Database configuration

DB_PATH = Path("trivia_game.db")

def init_database():
    """Initialize SQLite database with required tables."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Table: user scores per chat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, user_id)
            )
        ''')
        
        # Tabel game_state: menyimpan state game per chat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE NOT NULL,
                current_question_index INTEGER DEFAULT 0,
                answered_count INTEGER DEFAULT 0,
                round_active BOOLEAN DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel round_answers: menyimpan jawaban yang sudah diterima
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS round_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                question_index INTEGER NOT NULL,
                answer_slot INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(chat_id, question_index, answer_slot)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
        
    except Exception as e:
        logger.error(f"Database init error: {e}")
        raise

# Database operations

class ScoreManager:
    """Handle score and leaderboard database operations."""
    
    @staticmethod
    def get_connection():
        """Create database connection."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def add_score(chat_id: int, user_id: int, username: str, first_name: str, points: int = 1):
        """Add points to user score."""
        try:
            conn = ScoreManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scores (chat_id, user_id, username, first_name, score)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(chat_id, user_id) 
                DO UPDATE SET 
                    score = score + ?,
                    username = ?,
                    first_name = ?,
                    updated_at = CURRENT_TIMESTAMP
            ''', (chat_id, user_id, username, first_name, points, points, username, first_name))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding score: {e}")
            return False
    
    @staticmethod
    def get_user_score(chat_id: int, user_id: int) -> int:
        """Get total user score for chat."""
        try:
            conn = ScoreManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT score FROM scores 
                WHERE chat_id = ? AND user_id = ?
            ''', (chat_id, user_id))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['score'] if result else 0
        except Exception as e:
            logger.error(f"Error getting user score: {e}")
            return 0
    
    @staticmethod
    def get_leaderboard(chat_id: int, limit: int = 10) -> List[Tuple]:
        """Get top players leaderboard for chat."""
        try:
            conn = ScoreManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    username,
                    first_name,
                    score,
                    updated_at
                FROM scores
                WHERE chat_id = ?
                ORDER BY score DESC
                LIMIT ?
            ''', (chat_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [(row['username'] or row['first_name'] or 'Unknown', row['score']) 
                    for row in results]
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []

# Game data - 15 trivia questions with 5 answers each

QUIZ_DATA = [
    {
        "question": "🌍 Urutkan planet terbesar di tata surya kita dari yang paling besar!",
        "answers": ["jupiter", "saturnus", "uranus", "neptunus", "bumi"]
    },
    {
        "question": "🏕️ Obat atau perlengkapan medis apa yang harus dibawa saat berkemah?",
        "answers": ["antiseptik", "kassa", "plaster", "minyak kayu putih", "parasetamol"]
    },
    {
        "question": "🪳 Sebutkan binatang yang sering dianggap menjijikkan!",
        "answers": ["kecoa", "tikus", "belatung", "cicak", "lalat"]
    },
    {
        "question": "🏠 Barang apa saja yang biasanya ada di kamar anak kos?",
        "answers": ["kasur", "kipas angin", "magic com", "galon", "lemari"]
    },
    {
        "question": "🇮🇩 Sebutkan pulau besar yang ada di Indonesia!",
        "answers": ["papua", "kalimantan", "sumatera", "sulawesi", "jawa"]
    },
    {
        "question": "🚗 Sebutkan merek mobil terpopuler di Indonesia!",
        "answers": ["toyota", "honda", "daihatsu", "mitsubishi", "suzuki"]
    },
    {
        "question": "🍳 Sebutkan bumbu dapur utama dalam masakan Indonesia!",
        "answers": ["bawang merah", "bawang putih", "garam", "cabai", "kemiri"]
    },
    {
        "question": "📱 Sebutkan merek HP yang banyak digunakan di Indonesia!",
        "answers": ["samsung", "xiaomi", "oppo", "vivo", "iphone"]
    },
    {
        "question": "⚽ Sebutkan posisi pemain dalam olahraga sepak bola!",
        "answers": ["kiper", "bek", "gelandang", "striker", "winger"]
    },
    {
        "question": "🎓 Sebutkan universitas negeri terkemuka di Indonesia!",
        "answers": ["ui", "ugm", "itb", "unpad", "its"]
    },
    {
        "question": "🍜 Sebutkan makanan khas Indonesia yang populer!",
        "answers": ["rendang", "nasi goreng", "sate", "bakso", "soto"]
    },
    {
        "question": "💻 Sebutkan sistem operasi komputer atau HP yang paling umum!",
        "answers": ["windows", "android", "ios", "macos", "linux"]
    },
    {
        "question": "✈️ Sebutkan nama maskapai penerbangan di Indonesia!",
        "answers": ["garuda", "lion air", "citilink", "batik air", "super air jet"]
    },
    {
        "question": "🥤 Sebutkan jenis minuman dingin favorit masyarakat!",
        "answers": ["es teh", "es jeruk", "es boba", "es campur", "es cendol"]
    },
    {
        "question": "🌋 Sebutkan gunung berapi aktif yang terkenal di Indonesia!",
        "answers": ["merapi", "bromu", "rinjani", "kerinci", "krakatau"]
    },
    {
        "question": "sebutkan 7 keajaiban dunia!",
        "answers": ["piramida", "koloseum", "tembok cina", "taj mahal", "liberty", "sasa", "pisa"]
    }
]

# Game state management

class GameStateManager:
    """Manage game state per chat."""
    
    # In-memory game state (resets on bot restart)
    _game_states: Dict = defaultdict(lambda: {
        'current_question_index': 0,
        'round_active': False,
        'answered_count': 0,
        'current_answers': {}
    })
    
    @classmethod
    def get_state(cls, chat_id: int) -> Dict:
        """Get game state for chat."""
        return cls._game_states[chat_id]
    
    @classmethod
    def start_round(cls, chat_id: int):
        """Start new round with random question."""
        state = cls.get_state(chat_id)
        state['round_active'] = True
        state['answered_count'] = 0
        state['current_answers'] = {}
        state['current_question_index'] = random.randint(0, len(QUIZ_DATA) - 1)
    
    @classmethod
    def end_round(cls, chat_id: int):
        """End current round."""
        state = cls.get_state(chat_id)
        state['round_active'] = False
        state['answered_count'] = 0
        state['current_answers'] = {}
    
    @classmethod
    def next_question(cls, chat_id: int):
        """Move to next random question."""
        state = cls.get_state(chat_id)
        state['current_question_index'] = random.randint(0, len(QUIZ_DATA) - 1)
        state['answered_count'] = 0
        state['current_answers'] = {}
    
    @classmethod
    def add_answer(cls, chat_id: int, slot: int, user_id: int, username: str, first_name: str):
        """Record correct answer for slot."""
        state = cls.get_state(chat_id)
        state['current_answers'][slot] = (user_id, username, first_name)
        state['answered_count'] += 1
    
    @classmethod
    def is_round_complete(cls, chat_id: int) -> bool:
        """Check if all answers are filled."""
        state = cls.get_state(chat_id)
        question_idx = state['current_question_index']
        answer_count = len(QUIZ_DATA[question_idx]['answers'])
        return state['answered_count'] == answer_count

# Helper functions

def normalize_answer(answer: str) -> str:
    """Normalize answer for matching."""
    return answer.lower().strip()

def format_user_name(user: User) -> str:
    """Format user name for display."""
    if user.username:
        return f"@{user.username}"
    return user.first_name or "User"

def get_current_board(chat_id: int) -> str:
    """Generate current quiz board display."""
    try:
        state = GameStateManager.get_state(chat_id)
        
        if not state['round_active']:
            return "No active round. Type /mulai to start."
        
        q_idx = state['current_question_index']
        question = QUIZ_DATA[q_idx]
        answers = question['answers']
        
        board = f"<b>Question:</b>\n{question['question']}\n\n"
        board += "<b>Answers:</b>\n"
        
        for i, answer in enumerate(answers, 1):
            if i in state['current_answers']:
                user_id, username, first_name = state['current_answers'][i]
                display_name = username or first_name or f"User{user_id}"
                board += f"{i}. <i>{answer}</i> <b>(+1)</b> <code>@{display_name}</code>\n"
            else:
                board += f"{i}. __________\n"
        
        board += f"\nProgress: {state['answered_count']}/{len(answers)}"
        
        return board
    except Exception as e:
        logger.error(f"Error generating board: {e}")
        return "Error generating board"

# Command handlers

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    try:
        user = update.effective_user
        welcome_message = f"""<b>Telegram Quiz Bot</b>

Hello {user.first_name}!

<b>How to play:</b>
1. Ketik /mulai untuk memulai ronde
2. Akan saya berikan pertanyaan 
3. Berikan jawaban (tanpa "/")
4. Jawaban benar mendapatkan +1 point
5. Ronde Selesai ketika semua jawaban terpenuhi
6. Ketik /skor untuk melihat skor

<b>Commands:</b>
/start  - Menampilkan pesan ini
/mulai  - Memulai ronde awal
/nyerah - Menyerah (yah ampas pada gabisa jawab)
/next   - Pertanyaan selanjutnya
/skor   - Peringkat
/poin   - Skor kamu, manisku

Skor tercatat gatau hilang atau ngga yaudah. Ayo Main!"""
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text(
            "Error. Please try again.",
            parse_mode=ParseMode.HTML
        )

async def mulai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /mulai command - start new round."""
    try:
        chat_id = update.effective_chat.id
        state = GameStateManager.get_state(chat_id)
        
        if state['round_active']:
            await update.message.reply_text(
                "Round already active.\n"
                "Use /next to continue or /nyerah to stop.",
                parse_mode=ParseMode.HTML
            )
            return
        
        GameStateManager.start_round(chat_id)
        board = get_current_board(chat_id)
        await update.message.reply_text(
            f"<b>New round started:</b>\n\n{board}",
            parse_mode=ParseMode.HTML
        )
        
        logger.info(f"Round started in chat {chat_id}")
        
    except Exception as e:
        logger.error(f"Error in mulai_handler: {e}")
        await update.message.reply_text(
            "Error starting round. Please try again.",
            parse_mode=ParseMode.HTML
        )

async def nyerah_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /nyerah command - end round without revealing answers."""
    try:
        chat_id = update.effective_chat.id
        state = GameStateManager.get_state(chat_id)
        
        if not state['round_active']:
            await update.message.reply_text(
                "No active round.\nType /mulai to start.",
                parse_mode=ParseMode.HTML
            )
            return
        
        q_idx = state['current_question_index']
        question = QUIZ_DATA[q_idx]
        
        message = "<b>Round ended.</b>\n\n"
        message += f"<b>Question:</b>\n{question['question']}\n\n"
        message += "<b>Answered:</b>\n"
        
        for i, answer in enumerate(question['answers'], 1):
            if i in state['current_answers']:
                user_id, username, first_name = state['current_answers'][i]
                display_name = username or first_name or f"User{user_id}"
                message += f"{i}. <i>{answer}</i> (+1) @{display_name}\n"
            else:
                message += f"{i}. (unanswered)\n"
        
        GameStateManager.end_round(chat_id)
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in nyerah_handler: {e}")
        await update.message.reply_text(
            "❌ Terjadi error. Silakan coba lagi.",
            parse_mode=ParseMode.HTML
        )

async def next_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /next command - move to next question."""
    try:
        chat_id = update.effective_chat.id
        state = GameStateManager.get_state(chat_id)
        
        if not state['round_active']:
            await update.message.reply_text(
                "No active round.\nType /mulai to start.",
                parse_mode=ParseMode.HTML
            )
            return
        
        GameStateManager.next_question(chat_id)
        board = get_current_board(chat_id)
        message = f"<b>Next question:</b>\n\n{board}"
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in next_handler: {e}")
        await update.message.reply_text(
            "❌ Terjadi error. Silakan coba lagi.",
            parse_mode=ParseMode.HTML
        )

async def skor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /skor command - show leaderboard."""
    try:
        chat_id = update.effective_chat.id
        chat = update.effective_chat
        
        leaderboard = ScoreManager.get_leaderboard(chat_id, limit=10)
        
        if not leaderboard:
            await update.message.reply_text(
                "<b>Leaderboard empty</b>\n\n"
                "Start a round with /mulai to earn points.",
                parse_mode=ParseMode.HTML
            )
            return
        
        chat_name = chat.title or "Private"
        message = f"<b>Leaderboard - {chat_name}</b>\n\n"
        
        for rank, (name, score) in enumerate(leaderboard, 1):
            message += f"{rank}. {name} - {score}\n"
        
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in skor_handler: {e}")
        await update.message.reply_text(
            "Error loading leaderboard.",
            parse_mode=ParseMode.HTML
        )

async def poin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /poin command - show user score."""
    try:
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        score = ScoreManager.get_user_score(chat_id, user.id)
        
        message = f"<b>Your Score</b>\n\n"
        message += f"Name: {user.first_name}\n"
        message += f"Points: {score}\n\n"
        message += "Type /skor to see leaderboard."
        
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        logger.error(f"Error in poin_handler: {e}")
        await update.message.reply_text(
            "Error. Please try again.",
            parse_mode=ParseMode.HTML
        )

# Message handler - detect quiz answers

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages - detect quiz answers."""
    try:
        if update.message.from_user.is_bot or not update.message.text:
            return
        
        if update.message.text.startswith('/'):
            return
        
        chat_id = update.effective_chat.id
        user = update.effective_user
        message_text = update.message.text
        state = GameStateManager.get_state(chat_id)
        
        if not state['round_active']:
            return
        
        normalized_answer = normalize_answer(message_text)
        q_idx = state['current_question_index']
        question = QUIZ_DATA[q_idx]
        answers = question['answers']
        
        for slot, correct_answer in enumerate(answers, 1):
            if slot in state['current_answers']:
                continue
            
            normalized_correct = normalize_answer(correct_answer)
            if normalized_correct in normalized_answer or normalized_answer in normalized_correct:
                ScoreManager.add_score(
                    chat_id, user.id, user.username, user.first_name, points=1
                )
                
                GameStateManager.add_answer(
                    chat_id, slot, user.id, user.username, user.first_name
                )
                
                board = get_current_board(chat_id)
                user_name = f"@{user.username}" if user.username else user.first_name
                reaction_msg = f"<b>Correct!</b> {user_name} +1\n\n{board}"
                
                await update.message.reply_text(
                    reaction_msg,
                    parse_mode=ParseMode.HTML
                )
                
                if GameStateManager.is_round_complete(chat_id):
                    GameStateManager.end_round(chat_id)
                    completion_msg = (
                        f"<b>Round complete!</b>\n\n"
                        f"All answers correct.\n\n"
                        f"Type /next for next round or /skor to see scores."
                    )
                    await update.message.reply_text(
                        completion_msg,
                        parse_mode=ParseMode.HTML
                    )
                break
                
    except Exception as e:
        logger.error(f"Error in message_handler: {e}")

# Bot application

def main():
    """Initialize and run bot."""
    try:
        load_dotenv()
        
        token = os.getenv("BOT_TOKEN")
        if not token:
            logger.error("BOT_TOKEN not found in .env")
            sys.exit(1)
        
        init_database()
        application = Application.builder().token(token).build()
        
        application.add_handler(CommandHandler("start", start_handler))
        application.add_handler(CommandHandler("mulai", mulai_handler))
        application.add_handler(CommandHandler("nyerah", nyerah_handler))
        application.add_handler(CommandHandler("next", next_handler))
        application.add_handler(CommandHandler("skor", skor_handler))
        application.add_handler(CommandHandler("poin", poin_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            logger.error(f"Handler error: {context.error}")
        
        application.add_error_handler(error_handler)
        logger.info("Bot started")
        
        application.run_polling(
            allowed_updates=["message", "edited_channel_post"],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
