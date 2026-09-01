import os
import sys
import logging
import random
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("=" * 60)
    logger.error("❌ BOT_TOKEN environment variable is not set!")
    logger.error("=" * 60)
    logger.error("Please set BOT_TOKEN in Railway environment variables.")
    logger.error("")
    logger.error("To fix this:")
    logger.error("1. Go to Railway project dashboard")
    logger.error("2. Click 'Variables' tab")
    logger.error("3. Add: BOT_TOKEN = your_bot_token_here")
    logger.error("4. Click 'Save' and redeploy")
    logger.error("=" * 60)
    sys.exit(1)

logger.info(f"✅ Bot token loaded successfully!")

# Educational content
EDUCATIONAL_CONTENT = [
    "📚 **What is Bitcoin?**\n\nBitcoin is the first decentralized cryptocurrency. It was created in 2009 by an unknown person or group using the name Satoshi Nakamoto.\n\n🔑 **Key points:**\n• Limited supply (21 million max)\n• Decentralized network\n• Peer-to-peer transactions\n• Blockchain technology\n\n⚠️ Remember: Always do your own research!",
    
    "📚 **What is Blockchain?**\n\nA blockchain is a distributed ledger that records transactions across many computers.\n\n🔑 **Key features:**\n• Immutable records\n• Transparent transactions\n• Decentralized consensus\n• Cryptographic security",
    
    "📚 **Crypto Safety Tips**\n\n🛡️ **Stay safe in crypto:**\n• Never share private keys\n• Use hardware wallets for large amounts\n• Enable 2FA on exchanges\n• Beware of phishing scams\n• Start with small amounts\n• Only invest what you can afford to lose",
    
    "📚 **What is DeFi?**\n\nDeFi (Decentralized Finance) refers to financial services built on blockchain networks.\n\n💡 **Examples:**\n• Lending & borrowing\n• Decentralized exchanges\n• Yield farming\n• Staking\n\n⚠️ Smart contract risks exist!"
]

# Market data
def get_market_data():
    try:
        response = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets',
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': 'false'
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = f"""
🚀 **Welcome to CoinZenBot, {user.first_name}!**

I'm your crypto education companion.

📊 **What I can do:**
• Show crypto prices
• Market sentiment
• Educational content
• Portfolio tracker
• Daily summaries

📌 **No trading, no financial advice!**

Use /help to see all commands.
"""
    keyboard = [
        [InlineKeyboardButton("💰 Prices", callback_data='price'),
         InlineKeyboardButton("📊 Sentiment", callback_data='sentiment')],
        [InlineKeyboardButton("📚 Learn", callback_data='learn'),
         InlineKeyboardButton("📰 Daily", callback_data='daily')]
    ]
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **Available Commands:**

/start - 🚀 Start
/price - 💰 Prices
/sentiment - 📊 Sentiment
/learn - 📚 Learn
/portfolio - 💼 Portfolio
/daily - 📰 Daily
/help - ❓ Help
/about - ℹ️ About
"""
    await update.message.reply_text(help_text)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ CoinZenBot - Educational crypto bot. Not financial advice!")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Fetching prices...")
    data = get_market_data()
    if data:
        msg = "💰 **Top 10 Crypto Prices**\n\n"
        for coin in data[:10]:
            price = coin['current_price']
            change = coin['price_change_percentage_24h']
            emoji = "🟢" if change >= 0 else "🔴"
            msg += f"{emoji} **{coin['name']}** (${price:,.2f}) {change:+.2f}%\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Couldn't fetch prices. Try again later.")

async def sentiment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentiments = [
        "🟢 **Bullish** - Positive momentum",
        "🟡 **Neutral** - Consolidation phase",
        "🟢 **Cautiously Optimistic** - Mixed signals"
    ]
    await update.message.reply_text(f"📊 {random.choice(sentiments)}\n\n*Educational only*", parse_mode='Markdown')

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = random.choice(EDUCATIONAL_CONTENT)
    await update.message.reply_text(content, parse_mode='Markdown')

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = datetime.now().strftime("%B %d, %Y")
    msg = f"📰 **Daily Summary** - {date}\n\n"
    data = get_market_data()
    if data:
        btc = data[0]
        msg += f"🔹 **Bitcoin:** ${btc['current_price']:,.2f} ({btc['price_change_percentage_24h']:+.2f}%)\n"
    msg += "\n💡 *Stay educated, stay safe!*"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("💼 Portfolio tracker\n\nHow to use:\n/portfolio BTC 0.5\n/portfolio ETH 2.0")
    else:
        coin = args[0].upper()
        try:
            amount = float(args[1])
            await update.message.reply_text(f"✅ Added {amount} {coin} to portfolio! (Manual tracking only)")
        except:
            await update.message.reply_text("❌ Please enter a valid number")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'price':
        await price(update, context)
    elif query.data == 'sentiment':
        await sentiment(update, context)
    elif query.data == 'learn':
        await learn(update, context)
    elif query.data == 'daily':
        await daily(update, context)

def main():
    """Start the bot"""
    try:
        logger.info("🤖 Starting CoinZenBot...")
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("about", about))
        app.add_handler(CommandHandler("price", price))
        app.add_handler(CommandHandler("sentiment", sentiment))
        app.add_handler(CommandHandler("learn", learn))
        app.add_handler(CommandHandler("daily", daily))
        app.add_handler(CommandHandler("portfolio", portfolio))
        app.add_handler(CallbackQueryHandler(button_callback))
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
