import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Fetch and log the API key for debugging
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment variables.")
else:
    logger.info("✅ GEMINI_API_KEY loaded successfully.")

# Configure the Gemini client
genai.configure(api_key=str(api_key))

def translate_title(text, target_language="fr"):
    prompt = f"Translate the following title to {target_language}: {text}"
    try:
        # Always use the latest documented model
        model = genai.GenerativeModel('gemini-1.5-pro-002')
        response = model.generate_content(prompt)

        # Check the response structure and return the translated text
        if response and hasattr(response, 'text'):
            return response.text.strip()
        else:
            logger.error("❌ Invalid response from Gemini API")
            return ""
    except Exception as e:
        logger.error(f"[Gemini API Error]: {e}")
        return ""

