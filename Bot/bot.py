import os
import logging
import requests
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackContext
)
import io

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))  # Render uses this port

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

WEBHOOK_URL = f"https://your-service-name.onrender.com/{TOKEN}"  # CHANGE this to your Render app URL

user_states = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send your payment screenshot...")

def handle_photo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_bytes = photo_file.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image)

        logging.info(f"OCR Output from {user_id}: {text}")

        amount = 0
        if "100" in text or "₹100" in text:
            amount = 100
        elif "50" in text or "₹50" in text:
            amount = 50
        elif "10" in text or "₹10" in text:
            amount = 10
        elif "5" in text or "₹5" in text:
            amount = 5

        if amount > 0:
            user_states[user_id] = amount
            update.message.reply_text(f"Detected payment: ₹{amount}. Now send your email.")
        else:
            update.message.reply_text("Could not detect payment amount. Please try again.")
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        update.message.reply_text("There was an error processing the image.")

def handle_text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_states:
        email = update.message.text.strip()
        amount = user_states[user_id]

        try:
            res = requests.post("https://yourwebsite.com/update_premium.php", data={
                "email": email,
                "amount": amount
            })

            if res.ok and "Success" in res.text:
                update.message.reply_text("Your account is now premium!")
            else:
                update.message.reply_text("Something went wrong. Please contact support.")
        except Exception as e:
            logger.error(f"Error while updating: {e}")
            update.message.reply_text("Server error. Try again later.")

        del user_states[user_id]
    else:
        update.message.reply_text("Please send a payment screenshot first.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL
    )

    updater.idle()

if __name__ == "__main__":
    main()
