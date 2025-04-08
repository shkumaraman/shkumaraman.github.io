from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import pytesseract
from PIL import Image, ImageEnhance
import requests
import io
import os
import logging
import re

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# User state management
user_states = {}

def preprocess_image(image):
    """Enhance image for better OCR results"""
    try:
        # Convert to grayscale
        image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return image  # Return original if processing fails

def extract_amount(text):
    """Extract payment amount from text using regex"""
    patterns = [
        r'₹\s*(\d{2,4})',  # ₹100
        r'Rs\s*(\d{2,4})',  # Rs100
        r'(\d{2,4})\s*INR',  # 100 INR
        r'(\d{2,4})\s*rupees',  # 100 rupees
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for match in matches:
                amount = int(match)
                if amount in [50, 100, 300, 1000]:
                    return amount
    return None

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update, context):
    update.message.reply_text(
        "📱 Welcome to Premium Bot!\n\n"
        "To upgrade your account, please send a clear screenshot of your payment "
        "(₹50, ₹100, ₹300, or ₹1000).\n\n"
        "Make sure the amount is visible in the screenshot."
    )

def handle_photo(update, context):
    user_id = update.message.from_user.id
    try:
        # Get the highest resolution photo available
        photo_file = update.message.photo[-1].get_file()
        
        # Download photo
        photo_bytes = io.BytesIO()
        photo_file.download(out=photo_bytes)
        photo_bytes.seek(0)
        
        # Open and preprocess image
        try:
            image = Image.open(photo_bytes)
            image = preprocess_image(image)
            
            # Use Tesseract with custom config
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            logger.info(f"OCR output from {user_id}:\n{text}")
            
            # Extract amount
            detected_amount = extract_amount(text)
            
            if detected_amount:
                user_states[user_id] = {
                    'amount': detected_amount,
                    'attempts': 0
                }
                update.message.reply_text(
                    f"✅ Detected payment of ₹{detected_amount}.\n\n"
                    "Please send your registered email address to activate premium."
                )
            else:
                user_states[user_id] = user_states.get(user_id, {'attempts': 0})
                user_states[user_id]['attempts'] += 1
                
                if user_states[user_id]['attempts'] >= 2:
                    update.message.reply_text(
                        "⚠️ We couldn't detect the payment amount.\n\n"
                        "Please try:\n"
                        "1. A clearer screenshot\n"
                        "2. Crop to show just the amount\n"
                        "3. Send as a document (higher quality)\n\n"
                        "Or contact support @your_support_username"
                    )
                else:
                    update.message.reply_text(
                        "Couldn't detect the payment amount. Please try sending "
                        "a clearer screenshot with the amount visible."
                    )
                    
        except Image.UnidentifiedImageError:
            update.message.reply_text("The image format is not supported. Please send a JPEG or PNG image.")
        except pytesseract.TesseractError:
            update.message.reply_text("OCR processing failed. Please try a different image.")
            
    except Exception as e:
        logger.exception(f"Error processing image from {user_id}")
        update.message.reply_text(
            "⚠️ An error occurred while processing your image. Please try again "
            "or contact support @your_support_username"
        )

def handle_text(update, context):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    
    if user_id in user_states and 'amount' in user_states[user_id]:
        # Validate email format
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', text):
            update.message.reply_text("Please enter a valid email address.")
            return
            
        amount = user_states[user_id]['amount']
        try:
            # Call your backend API
            response = requests.post(
                "https://yourwebsite.com/api/upgrade",
                json={
                    "email": text,
                    "amount": amount,
                    "user_id": user_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                update.message.reply_text(
                    f"🎉 Premium activated for {text}!\n\n"
                    f"• Amount: ₹{amount}\n"
                    f"• Thank you for your payment!\n\n"
                    "Your premium access will be available within 5 minutes."
                )
                del user_states[user_id]
            else:
                update.message.reply_text(
                    "⚠️ Failed to activate premium. Please contact support @your_support_username\n\n"
                    f"Error: {response.text}"
                )
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            update.message.reply_text(
                "⚠️ Server error. Please try again later or contact support @your_support_username"
            )
    else:
        update.message.reply_text("Please send a payment screenshot first.")

# Set up handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

if __name__ == "__main__":
    # Set webhook
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_hostname:
        webhook_url = f"https://{render_hostname}/{TOKEN}"
        bot.setWebhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    
    # Start Flask app
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
