from telegram import BotCommand

# Define bot commands
BOT_COMMANDS = [
    BotCommand("start", "🚀 Start the bot and get welcome message"),
    BotCommand("help", "📚 Get help and instructions"),
    BotCommand("analyze", "📊 Analyze candlestick chart image"),
    BotCommand("info", "ℹ️ Get information about the bot"),
    BotCommand("status", "🔍 Check bot status and model loaded"),
]

# Command descriptions for help
COMMAND_DESCRIPTIONS = {
    "start": "Start the bot and get a welcome message with instructions on how to use it.",
    "help": "Get detailed help information about all available commands and how to use the bot.",
    "analyze": "Send a candlestick chart image to get AI-powered stock trend analysis with detailed insights.",
    "info": "Get information about the bot's capabilities and what it can do.",
    "status": "Check if the bot is running properly and if the AI models are loaded correctly."
}

# Help message
HELP_MESSAGE = """
🤖 **Stock Trend Analysis Bot Commands**

📋 **Available Commands:**

/start - 🚀 Start the bot and get welcome message
/help - 📚 Get help and instructions  
/analyze - 📊 Analyze candlestick chart image
/info - ℹ️ Get information about the bot
/status - 🔍 Check bot status and model loaded

📸 **How to use:**
1. Send /start to begin
2. Send a candlestick chart image
3. Get AI-powered trend analysis with detailed insights

💡 **Features:**
• AI-powered candlestick analysis
• Detailed market insights and recommendations
• Confidence scoring with explanations
• Risk assessment and warnings
• Professional trading insights

💡 **Tip:** Just send any image and I'll analyze it automatically!
"""

# Welcome message
WELCOME_MESSAGE = """
🤖 **Welcome to Stock Trend Analysis Bot!**

I can analyze candlestick patterns from images to predict stock trends using advanced AI technology.

📸 **How to use:**
1. Send me a photo of a candlestick chart
2. I'll analyze it and provide detailed insights
3. Get comprehensive market analysis and recommendations

💡 **Commands:**
/start - Show this welcome message
/help - Show help information
/analyze - Analyze an image
/info - Bot information
/status - Check bot status

📊 **What you'll get:**
• Professional trend analysis
• Detailed market insights
• Risk assessment
• Trading recommendations
• Confidence explanations

Send me a candlestick chart image to get started! 📊
"""

# Info message
INFO_MESSAGE = """
ℹ️ **Bot Information**

🤖 **Name:** Stock Trend Analysis Bot
📊 **Purpose:** Analyze candlestick patterns using advanced AI
🎯 **Capabilities:** 
• AI-powered image analysis of candlestick charts
• Stock trend prediction (Up/Down)
• Confidence level assessment with explanations
• Detailed market insights and recommendations
• Risk assessment and warnings
• Professional trading insights
• Real-time processing

🔧 **Technology:**
• TensorFlow/Keras neural network
• Google Gemini AI for enhanced analysis
• Computer vision (OpenCV)
• Telegram Bot API
• Flask web framework

🧠 **AI Features:**
• Enhanced analysis with Gemini AI
• Pattern recognition and interpretation
• Risk assessment and management
• Professional trading insights
• Confidence level explanations

⚠️ **Disclaimer:** This is for educational purposes only. Always do your own research before making investment decisions.
""" 