import os
import logging
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from commands import BOT_COMMANDS, WELCOME_MESSAGE, HELP_MESSAGE, INFO_MESSAGE
from gemini_helper import GeminiHelper

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
img_height = 64
img_width = 64

class StockAnalysisBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables!")
        
        self.application = Application.builder().token(self.bot_token).build()
        self.model = self._create_and_load_model()
        self.gemini = GeminiHelper()  # Initialize Gemini helper
        self._setup_handlers()
        self._setup_commands()
    
    def _create_and_load_model(self):
        """Create and load the candlestick model"""
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        
        # Load pre-trained weights
        try:
            model.load_weights('candlestick_model_weights.h5')
            logger.info("Model weights loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model weights: {e}")
            raise
        
        return model
    
    def _setup_handlers(self):
        """Setup command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    async def _setup_commands(self):
        """Setup bot commands in Telegram"""
        try:
            await self.application.bot.set_my_commands(BOT_COMMANDS)
            logger.info("Bot commands set successfully")
        except Exception as e:
            logger.error(f"Error setting bot commands: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        await update.message.reply_text(INFO_MESSAGE, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        try:
            gemini_status = "✅ Enabled" if self.gemini.enabled else "❌ Disabled"
            
            status_message = f"""
🔍 **Bot Status**

✅ **Bot Status:** Running
✅ **Model Status:** Loaded
✅ **Image Processing:** Ready
✅ **API Status:** Active
🤖 **Gemini AI:** {gemini_status}

📊 **Ready to analyze candlestick charts!**
            """
            await update.message.reply_text(status_message, parse_mode='Markdown')
        except Exception as e:
            error_message = f"❌ **Error:** {str(e)}"
            await update.message.reply_text(error_message, parse_mode='Markdown')
    
    def predict_candlestick_direction(self, img):
        """Predict candlestick direction from image using ML model"""
        img = cv2.resize(img, (img_height, img_width))
        img = img / 255.0  # Normalize pixel values to [0, 1]
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        prediction = self.model.predict(img)
        return prediction[0][0]
    
    def get_prediction_confidence(self, prediction):
        """Get confidence level of the ML prediction"""
        confidence = abs(prediction - 0.5) * 2  # Convert to 0-1 scale
        if confidence > 0.8:
            return "High"
        elif confidence > 0.6:
            return "Medium"
        else:
            return "Low"
    
    def get_image_description(self, img):
        """Get a basic description of the image for Gemini analysis"""
        try:
            # Basic image analysis
            height, width = img.shape[:2]
            channels = img.shape[2] if len(img.shape) > 2 else 1
            
            # Simple brightness analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if channels == 3 else img
            brightness = np.mean(gray)
            
            description = f"Candlestick chart image ({width}x{height}, brightness: {brightness:.1f})"
            return description
        except Exception as e:
            logger.error(f"Error getting image description: {e}")
            return "Candlestick chart image"
    
    async def send_long_message(self, update: Update, text: str, parse_mode='Markdown'):
        """Send long messages by splitting them if needed"""
        max_length = 1000  # Keep messages concise
        
        if len(text) <= max_length:
            try:
                await update.message.reply_text(text, parse_mode=parse_mode)
            except Exception as e:
                # If markdown parsing fails, send as plain text
                logger.warning(f"Markdown parsing failed, sending as plain text: {e}")
                await update.message.reply_text(text)
        else:
            # Split the message
            parts = []
            current_part = ""
            
            for line in text.split('\n'):
                if len(current_part + line + '\n') > max_length:
                    if current_part:
                        parts.append(current_part.strip())
                    current_part = line + '\n'
                else:
                    current_part += line + '\n'
            
            if current_part:
                parts.append(current_part.strip())
            
            # Send each part
            for i, part in enumerate(parts):
                try:
                    if i == 0:
                        await update.message.reply_text(part, parse_mode=parse_mode)
                    else:
                        await update.message.reply_text(f"*Continued...*\n\n{part}", parse_mode=parse_mode)
                except Exception as e:
                    # If markdown parsing fails, send as plain text
                    logger.warning(f"Markdown parsing failed for part {i}, sending as plain text: {e}")
                    if i == 0:
                        await update.message.reply_text(part)
                    else:
                        await update.message.reply_text(f"Continued...\n\n{part}")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages - ML analysis enhanced by Gemini"""
        try:
            # Send processing message
            processing_msg = await update.message.reply_text("🔄 Processing your candlestick chart...")
            
            # Get the largest photo size
            photo = update.message.photo[-1]
            
            # Download the photo
            file = await context.bot.get_file(photo.file_id)
            photo_bytes = await file.download_as_bytearray()
            
            # Convert to OpenCV format
            nparr = np.frombuffer(photo_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                await processing_msg.edit_text("❌ Error: Could not process the image. Please try again with a clearer image.")
                return
            
            # Step 1: Get ML model prediction
            prediction = self.predict_candlestick_direction(img)
            confidence = self.get_prediction_confidence(prediction)
            
            # Step 2: Get image description
            image_description = self.get_image_description(img)
            
            # Step 3: Enhance ML result with Gemini
            enhanced_analysis = self.gemini.enhance_ml_result(prediction, confidence, image_description)
            
            # Step 4: Send the enhanced analysis (with splitting if needed)
            await processing_msg.delete()  # Remove processing message
            await self.send_long_message(update, enhanced_analysis, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error processing photo: {e}")
            await update.message.reply_text("❌ Sorry, I encountered an error while processing your image. Please try again.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        text = update.message.text.lower()
        
        if any(word in text for word in ['hello', 'hi', 'hey']):
            await update.message.reply_text("👋 Hello! Send me a candlestick chart image to analyze!")
        elif any(word in text for word in ['thanks', 'thank you', 'thx']):
            await update.message.reply_text("You're welcome! 🎉")
        else:
            await update.message.reply_text(
                "📸 Please send me a photo of a candlestick chart to analyze. "
                "Use /help for more information."
            )
    
    def run(self):
        """Run the bot"""
        logger.info("Starting Stock Analysis Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    try:
        bot = StockAnalysisBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}") 