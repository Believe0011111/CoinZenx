# CoinZenBot 🤖

A Telegram bot for crypto education and market insights.

## Features
- Real-time crypto prices
- Market sentiment analysis
- Educational content
- Manual portfolio tracker
- Daily market summaries

## Deployment on Railway

1. Fork/clone this repository
2. Create a new project on Railway
3. Connect your GitHub repository
4. Add environment variable:
   - `BOT_TOKEN`: Your Telegram bot token from @BotFather
5. Deploy!

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your token
echo "BOT_TOKEN=your_token_here" > .env

# Run the bot
python bot.py
