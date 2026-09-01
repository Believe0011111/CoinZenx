import os
import sys
import logging
import random
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token with better error handling
def get_token():
    """Get bot token with fallback options"""
    # Try environment variable first
    token = os.getenv('BOT_TOKEN')
    
    if token:
        return token.strip('"\'')
    
    # Try reading from .env file directly
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('BOT_TOKEN='):
                    token = line.split('=', 1)[1].strip().strip('"\'')
                    return token
    except FileNotFoundError:
        pass
    
    # If still not found, check if token was passed as argument
    if len(sys.argv) > 1:
        token = sys.argv[1]
        return token
    
    # No token found - crash with clear message
    logger.error("=" * 60)
    logger.error("❌ BOT_TOKEN NOT FOUND!")
    logger.error("=" * 60)
    logger.error("Please set your bot token in one of these ways:")
    logger.error("")
    logger.error("1. Railway (Production):")
    logger.error("   - Go to your Railway project")
    logger.error("   - Click 'Variables' tab")
    logger.error("   - Add variable: BOT_TOKEN = your_token_here")
    logger.error("")
    logger.error("2. Local Development:")
    logger.error("   - Create .env file in project root")
    logger.error("   - Add: BOT_TOKEN=your_token_here")
    logger.error("")
    logger.error("3. Command Line:")
    logger.error("   - python bot.py YOUR_TOKEN_HERE")
    logger.error("=" * 60)
    sys.exit(1)

# Get the token
BOT_TOKEN = get_token()
logger.info("✅ Bot token loaded successfully!")

# Rest of your code... (keep all your functions: start, help, price, etc.)
