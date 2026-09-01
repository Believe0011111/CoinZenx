import os
import logging
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """Bot configuration"""
    
    @staticmethod
    def get_bot_token():
        """Get bot token from environment variables"""
        # Try to get from environment
        token = os.getenv('BOT_TOKEN')
        
        # If not found, try reading from .env file directly (fallback)
        if not token:
            try:
                with open('.env', 'r') as f:
                    for line in f:
                        if line.startswith('BOT_TOKEN='):
                            token = line.split('=', 1)[1].strip()
                            break
            except FileNotFoundError:
                pass
        
        # If still no token, raise error
        if not token:
            logger.error("❌ BOT_TOKEN not found in environment variables!")
            logger.error("Please set BOT_TOKEN in Railway environment variables.")
            raise ValueError(
                "BOT_TOKEN is required! Set it in:\n"
                "1. Railway: Project → Variables → Add BOT_TOKEN\n"
                "2. Local: Create .env file with BOT_TOKEN=your_token"
            )
        
        # Remove quotes if present
        token = token.strip('"\'')
        
        logger.info("✅ BOT_TOKEN loaded successfully")
        return token

# For simple usage in bot.py
BOT_TOKEN = Config.get_bot_token()
