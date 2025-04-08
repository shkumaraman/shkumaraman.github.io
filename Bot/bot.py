import os
import io
import logging
import pytesseract
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from PIL import Image, UnidentifiedImageError
import requests

# Initialize Flask
app = Flask(__name__)

# Configuration
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# Enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User state management
user_states = {}

# ========== HANDLERS ========== #
def start(update, context):
    """Welcome message handler"""
    update.message.reply_text(
        "Welcome! Send your ₹5 payment screenshot to activate premium access.\n"
        "After payment verification, we'll ask for your email."
    )

def handle_photo(update, context):
    """Process payment screenshot"""
    user = update.message.from_user
    try:
        # Get highest resolution photo
        photo = update.message.photo[-1].get_file()
        img_bytes = io.BytesIO(photo.download_as_bytearray())
        
        # OCR Processing
        try:
            img = Image.open(img_bytes)
            text = pytesseract.image_to_string(img).lower()
            logger.info(f"OCR Text from {user.id}:\n{text}")

            # Payment verification
            if any(keyword in text for keyword in ["5", "₹5", "inr5"]):
                user_states[user.id] = {"step": "awaiting_email"}
                update.message.reply_text("✅ Payment verified! Please send your email now.")
            else:
                update.message.reply_text("❌ Couldn't verify ₹5 payment. Send a clearer screenshot.")
                
        except UnidentifiedImageError:
            update.message.reply_text("⚠️ Invalid image format. Send JPEG/PNG screenshot.")
        except Exception as e:
            logger.error(f"OCR Error: {str(e)}")
            update.message.reply_text("🔧 OCR processing failed. Try again.")

    except Exception as e:
        logger.error(f"Photo Handler Error: {str(e)}")
        update.message.reply_text("🚨 An error occurred. Please try again.")

def handle_text(update, context):
    """Process email after payment verification"""
    user = update.message.from_user
    text = update.message.text.strip()
    
    # Email validation regex (simplified)
    if "@" in text and "." in text and len(text) > 5:
        if user.id in user_states and user_states[user.id].get("step") == "awaiting_email":
            try:
                # Simulate API call (replace with your actual endpoint)
                response = requests.post(
                    "https://your-api.com/activate_premium",
                    json={"email": text, "user_id": user.id},
                    timeout=10
                )
                
                if response.status_code == 200:
                    update.message.reply_text(
                        "🎉 Premium activated! Check your email for confirmation.\n"
                        f"Registered: {text}"
                    )
                    del user_states[user.id]
                else:
                    update.message.reply_text("⚠️ Activation failed. Please contact support.")
                    
            except requests.RequestException as e:
                logger.error(f"API Error: {str(e)}")
                update.message.reply_text("🔧 Service temporarily unavailable. Try later.")
    else:
        update.message.reply_text("📧 Please send a valid email address")

# ========== FLASK ROUTES ========== #
@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook_handler():
    """Process Telegram updates"""
    try:
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
        return jsonify(success=True)
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        return jsonify(success=False), 500

@app.route('/')
def health_check():
    return "Bot is running 🚀"

# ========== INITIALIZATION ========== #
def initialize():
    """Register handlers and set webhook"""
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Webhook setup for Render
    if os.getenv('RENDER'):
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{TOKEN}"
        bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")

if __name__ == '__main__':
    initialize()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
