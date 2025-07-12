import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiHelper:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        logger.info(f"Gemini API Key found: {'Yes' if self.api_key else 'No'}")
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. Gemini features will be disabled.")
            self.enabled = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            # Use gemini-2.0-flash for text analysis
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.enabled = True
            logger.info("Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.enabled = False
    
    def enhance_ml_result(self, prediction, confidence, image_description=""):
        """Take ML model result and enhance it with Gemini AI analysis (text-based only)"""
        logger.info(f"Enhancing ML result - Prediction: {prediction}, Confidence: {confidence}")
        
        if not self.enabled:
            logger.warning("Gemini is disabled, using basic analysis")
            return self._get_basic_analysis(prediction, confidence)
        
        try:
            trend = "UP (Bullish)" if prediction > 0.5 else "DOWN (Bearish)"
            
            prompt = f"""
You are a professional stock market analyst. The ML model has analyzed a candlestick chart and provided these results:

**ML Model Results:**
- Prediction: {trend}
- Score: {prediction:.3f}
- Confidence: {confidence}
- Chart: {image_description if image_description else "Candlestick chart"}

Provide a concise analysis (max 800 characters) including:

📈 **Trend**: What the {trend.lower()} prediction means
🎯 **Confidence**: What {confidence} confidence indicates
📊 **Key Points**: Main technical insights
⚠️ **Risks**: Primary risks to consider
💡 **Action**: Key trading recommendations

Keep it brief, professional, and actionable. Use bullet points.
Format in markdown.

Remember: This is for educational purposes only.
            """
            
            logger.info("Sending request to Gemini API...")
            response = self.model.generate_content(prompt)
            logger.info("Received response from Gemini API")
            
            if response and response.text:
                # Limit response length for Telegram and clean up formatting
                response_text = response.text[:1000]  # Keep responses concise
                response_text = self._clean_markdown(response_text)
                logger.info(f"Gemini response length: {len(response_text)} characters")
                return response_text
            else:
                logger.error("Empty response from Gemini API")
                return self._get_basic_analysis(prediction, confidence)
            
        except Exception as e:
            logger.error(f"Error enhancing ML result: {e}")
            return self._get_basic_analysis(prediction, confidence)
    
    def _clean_markdown(self, text):
        """Clean up markdown formatting to prevent Telegram parsing errors"""
        # Remove any incomplete markdown formatting
        text = re.sub(r'\*\*[^*]*$', '', text)  # Remove incomplete bold
        text = re.sub(r'\*[^*]*$', '', text)    # Remove incomplete italic
        text = re.sub(r'`[^`]*$', '', text)     # Remove incomplete code
        text = re.sub(r'\[[^\]]*$', '', text)   # Remove incomplete links
        
        # Ensure proper line breaks
        text = text.replace('\n\n\n', '\n\n')
        
        # Remove any trailing incomplete formatting
        text = text.strip()
        
        return text
    
    def _get_basic_analysis(self, prediction, confidence):
        """Basic analysis when Gemini is not available"""
        trend = "UP (Bullish)" if prediction > 0.5 else "DOWN (Bearish)"
        
        return f"""
📊 **Stock Trend Analysis Results**

**ML Prediction:** {trend}
**Confidence:** {confidence}
**Score:** {prediction:.3f}

⚠️ **Disclaimer:** This analysis is for educational purposes only. Always conduct your own research before making investment decisions.
        """ 