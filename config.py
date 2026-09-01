import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration"""
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Validate required variables
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required! Set it in .env file")
        return True
    
    @classmethod
    def get_bot_token(cls):
        cls.validate()
        return cls.BOT_TOKEN

# Usage in bot.py:
# from config import Config
# BOT_TOKEN = Config.get_bot_token()
