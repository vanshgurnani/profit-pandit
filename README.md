# Stock Trend Analysis Telegram Bot

A Telegram bot that analyzes candlestick patterns from images to predict stock trends using advanced AI technology.

## Features

- 🤖 **Telegram Bot**: Easy-to-use bot interface
- 📸 **Image Analysis**: Upload candlestick chart images
- 📊 **AI Predictions**: Uses trained neural network
- 🧠 **Gemini AI Integration**: Enhanced analysis and responses
- 🎯 **Commands**: Built-in commands for better UX
- 🌐 **Flask API**: Webhook support for production

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
Create a `.env` file in the project root:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
FLASK_DEBUG=False
```

### 3. Get API Keys
1. **Telegram Bot Token**: Message [@BotFather](https://t.me/botfather) on Telegram
2. **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Running the Bot

### Option 1: Direct Bot (Polling)
```bash
python bot.py
```

### Option 2: Flask App (Webhook)
```bash
python app.py
```

## Bot Commands

- `/start` - Welcome message and instructions
- `/help` - Show all available commands
- `/analyze` - Analyze candlestick chart image
- `/info` - Bot information and capabilities
- `/status` - Check bot status

## How to Use

1. **Start the bot** with `/start`
2. **Send a candlestick chart image** to get AI analysis
3. **Get comprehensive analysis** with detailed insights and recommendations

## AI Features

### Gemini AI Integration
- **Enhanced Analysis**: Detailed market insights and recommendations
- **Professional Insights**: Expert-level trading analysis
- **Risk Assessment**: Comprehensive risk evaluation
- **Trading Recommendations**: Actionable trading advice
- **Confidence Explanations**: Detailed confidence level analysis

### Neural Network Analysis
- **Trend Prediction**: Up/Down predictions
- **Confidence Scoring**: High/Medium/Low confidence levels
- **Image Processing**: Advanced computer vision analysis

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /webhook` - Telegram webhook

## Files

- `bot.py` - Main Telegram bot with Gemini integration
- `gemini_helper.py` - Gemini AI helper functions
- `commands.py` - Bot commands and messages
- `app.py` - Flask API server
- `main.py` - Original Streamlit app
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this)
- `.gitignore` - Git ignore rules

## Sample Images

### Result Directory (`/result/`)
Contains sample candlestick chart images that have been analyzed by the bot:
![photo_2025-07-12_09-46-55](https://github.com/user-attachments/assets/9d97805b-8d31-4f89-820f-93b6262e3558)
![photo_2025-07-12_10-35-23](https://github.com/user-attachments/assets/c1157382-30a4-41e7-b280-a327e150349b)
![photo_2025-07-12_10-35-24](https://github.com/user-attachments/assets/08ad07b0-0612-48f9-8371-9d9ce0499bb6)



## Gemini AI Setup

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Create API Key**: Generate a new API key
3. **Add to .env**: `GEMINI_API_KEY=your_key_here`
4. **Restart Bot**: The bot will automatically enable Gemini features

## Analysis Features

The bot provides comprehensive analysis including:
- **Trend Analysis**: Price movement expectations and timeframe considerations
- **Confidence Assessment**: Reliability and factors affecting predictions
- **Technical Insights**: Pattern recognition, support/resistance levels
- **Risk Assessment**: Potential risks and position sizing advice
- **Trading Recommendations**: Entry/exit strategies and risk management
- **Action Items**: Specific next steps and confirmation signals

## Disclaimer

This bot is for educational purposes only. Always conduct your own research before making investment decisions. The predictions are based on historical patterns and should not be considered as financial advice.
