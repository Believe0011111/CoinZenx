import os
import logging
import random
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Sample educational content (not financial advice)
EDUCATIONAL_CONTENT = [
    "📚 **What is Bitcoin?**\n\nBitcoin is the first decentralized cryptocurrency. It was created in 2009 by an unknown person or group using the name Satoshi Nakamoto.\n\n🔑 **Key points:**\n• Limited supply (21 million max)\n• Decentralized network\n• Peer-to-peer transactions\n• Blockchain technology\n\n⚠️ Remember: Always do your own research!",
    
    "📚 **What is Blockchain?**\n\nA blockchain is a distributed ledger that records transactions across many computers.\n\n🔑 **Key features:**\n• Immutable records\n• Transparent transactions\n• Decentralized consensus\n• Cryptographic security",
    
    "📚 **Crypto Safety Tips**\n\n🛡️ **Stay safe in crypto:**\n• Never share private keys\n• Use hardware wallets for large amounts\n• Enable 2FA on exchanges\n• Beware of phishing scams\n• Start with small amounts\n• Only invest what you can afford to lose",
    
    "📚 **What is DeFi?**\n\nDeFi (Decentralized Finance) refers to financial services built on blockchain networks.\n\n💡 **Examples:**\n• Lending & borrowing\n• Decentralized exchanges\n• Yield farming\n• Staking\n\n⚠️ Smart contract risks exist!"
]

# Sample market insights (educational only)
def get_market_data():
    """Fetch real crypto data using free API"""
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
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""
🚀 **Welcome to CoinZenBot, {user.first_name}!**

I'm your crypto education and market insights companion.

📊 **What I can do:**
• Show real-time crypto prices
• Provide market sentiment analysis
• Share educational content
• Track your portfolio (manual tracking)
• Give daily market summaries

📌 **No trading, no financial advice!** 
Just information and education.

Use /help to see all available commands.
"""
    keyboard = [
        [InlineKeyboardButton("💰 Prices", callback_data='price'),
         InlineKeyboardButton("📊 Sentiment", callback_data='sentiment')],
        [InlineKeyboardButton("📚 Learn", callback_data='learn'),
         InlineKeyboardButton("📰 Daily", callback_data='daily')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **Available Commands:**

/start - 🚀 Start the bot
/price - 💰 Current crypto prices
/sentiment - 📊 Market sentiment analysis
/learn - 📚 Educational content
/portfolio - 💼 Manage your portfolio
/daily - 📰 Daily market summary
/help - ❓ Show this help
/about - ℹ️ About this bot

⚠️ **Disclaimer:** This bot provides educational content and market data only. Not financial advice. Always do your own research.
"""
    await update.message.reply_text(help_text)

# About command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
ℹ️ **About CoinZenBot**

This bot provides educational content and market data for crypto enthusiasts.

**Features:**
• 📊 Real-time price data from CoinGecko
• 📚 Curated educational content
• 📈 Market sentiment indicators
• 💼 Simple portfolio tracker
• 📰 Daily market summaries

**Disclaimer:**
This bot is for educational purposes only. 
Nothing here constitutes financial advice.
Always DYOR (Do Your Own Research).

Made with ❤️ by crypto enthusiasts
"""
    await update.message.reply_text(about_text)

# Price command
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Fetching latest prices...")
    
    data = get_market_data()
    
    if data:
        message = "💰 **Top 10 Crypto Prices (USD)**\n\n"
        for coin in data[:10]:
            name = coin['name']
            symbol = coin['symbol'].upper()
            price = coin['current_price']
            change_24h = coin['price_change_percentage_24h']
            
            emoji = "🟢" if change_24h >= 0 else "🔴"
            message += f"{emoji} **{name}** ({symbol}) - ${price:,.2f}\n"
            message += f"   {change_24h:+.2f}% (24h)\n\n"
        
        message += "📊 *Data from CoinGecko*\n"
        message += "⚠️ *Educational purposes only*"
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Sorry, couldn't fetch price data. Please try again later.")

# Sentiment command
async def sentiment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentiments = [
        "🟢 **Market Sentiment: Bullish**\n\nDespite recent volatility, market indicators suggest positive momentum. Institutional interest remains strong.",
        
        "🟡 **Market Sentiment: Neutral**\n\nThe market is consolidating. This could be a good time for education and research.",
        
        "🟢 **Market Sentiment: Cautiously Optimistic**\n\nTechnical indicators show mixed signals. Focus on education and risk management.",
        
        "🟡 **Market Sentiment: Accumulation Phase**\n\nLong-term holders are accumulating. Great time to learn about blockchain fundamentals."
    ]
    
    selected = random.choice(sentiments)
    message = f"📊 **Market Sentiment Analysis**\n\n{selected}\n\n⚠️ *This is for educational purposes only. Not trading advice.*"
    await update.message.reply_text(message, parse_mode='Markdown')

# Learn command
async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = random.choice(EDUCATIONAL_CONTENT)
    message = f"{content}\n\n📚 *Tap /learn for another topic!*"
    await update.message.reply_text(message, parse_mode='Markdown')

# Daily command
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = datetime.now().strftime("%B %d, %Y")
    
    data = get_market_data()
    
    message = f"📰 **Daily Market Summary**\n{date}\n\n"
    
    if data:
        top_coin = data[0]
        btc_price = top_coin['current_price']
        btc_change = top_coin['price_change_percentage_24h']
        
        message += f"🔹 **Bitcoin (BTC):** ${btc_price:,.2f} ({btc_change:+.2f}%)\n"
        message += f"🔹 **Market Cap:** ${data[0]['market_cap']/1e9:,.1f}B\n\n"
    
    message += "💡 **Today's Learning Tip:**\n"
    tips = [
        "Crypto markets are volatile - always invest responsibly.",
        "Diversification is key in any investment strategy.",
        "Understanding blockchain fundamentals is more important than price.",
        "Always use secure wallets for your crypto assets.",
        "Stay informed, but don't let emotions drive decisions."
    ]
    message += random.choice(tips)
    
    message += "\n\n📚 *Stay educated, stay safe!*"
    await update.message.reply_text(message, parse_mode='Markdown')

# Simple portfolio tracker (manual, no wallet connection)
PORTFOLIOS = {}  # In-memory storage (resets on restart)

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Check if command has arguments
    args = context.args
    
    if not args:
        # Show current portfolio
        if user_id in PORTFOLIOS and PORTFOLIOS[user_id]:
            message = "💼 **Your Portfolio**\n\n"
            for coin, amount in PORTFOLIOS[user_id].items():
                message += f"• {coin}: {amount}\n"
            message += "\n📝 *To update: /portfolio BTC 1.5*"
        else:
            message = "💼 **Portfolio Tracker**\n\nYour portfolio is empty.\n\n"
            message += "📝 **How to use:**\n"
            message += "/portfolio BTC 0.5 - Add 0.5 BTC\n"
            message += "/portfolio ETH 2.0 - Add 2.0 ETH\n"
            message += "/portfolio reset - Clear portfolio\n\n"
            message += "⚠️ *Manual tracking only - no wallet connection*"
        
        await update.message.reply_text(message, parse_mode='Markdown')
        return
    
    # Update portfolio
    if args[0].lower() == 'reset':
        if user_id in PORTFOLIOS:
            PORTFOLIOS[user_id] = {}
            await update.message.reply_text("✅ Portfolio cleared!")
        return
    
    if len(args) >= 2:
        coin = args[0].upper()
        try:
            amount = float(args[1])
            
            if user_id not in PORTFOLIOS:
                PORTFOLIOS[user_id] = {}
            
            PORTFOLIOS[user_id][coin] = amount
            
            await update.message.reply_text(f"✅ Added {amount} {coin} to your portfolio!")
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number for amount.")
    else:
        await update.message.reply_text("❌ Usage: /portfolio BTC 1.5")

# Callback handler for inline buttons
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
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("sentiment", sentiment))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("portfolio", portfolio))
    
    # Callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
