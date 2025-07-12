from flask import Flask, request, jsonify
import asyncio
import logging
from bot import StockAnalysisBot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global bot instance
bot = None

def create_bot():
    """Create and return bot instance"""
    global bot
    if bot is None:
        bot = StockAnalysisBot()
    return bot

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Stock Trend Analysis Bot API",
        "status": "running",
        "endpoints": {
            "/": "API information",
            "/webhook": "Telegram webhook endpoint",
            "/health": "Health check"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot_token_configured": bool(os.getenv('TELEGRAM_BOT_TOKEN'))
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook endpoint"""
    try:
        # Get the update data from Telegram
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({"error": "No data received"}), 400
        
        # Create bot instance if not exists
        bot_instance = create_bot()
        
        # Process the update asynchronously
        asyncio.run(bot_instance.application.process_update(update_data))
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create bot instance
    create_bot()
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 