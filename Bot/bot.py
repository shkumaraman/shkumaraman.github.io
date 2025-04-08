from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
import pytesseract
from PIL import Image
import requests
import io
import os
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Bot token from environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

# Webhook URL (your deployed domain)
WEBHOOK_URL = f"https://your-app-name.onrender.com/{TOKEN}"

# Store user payment states
user_states = {}

def start(update: Update, context):
    update.message.reply_text("Please send a screenshot of your payment (₹5).")

def handle_photo(update: Update, context):
    user_id = update.message.from_user.id
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_bytes = photo_file.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image)

        logging.info(f"OCR Output from {user_id}: {text}")

        amount = 0
        if "5" in text or "₹5" in text:
            amount = 5

        if amount == 5:
            user_states[user_id] = amount
            update.message.reply_text("₹5 detected. Please send your email now.")
        else:
            update.message.reply_text("Couldn't detect ₹5 in the screenshot. Try again.")
    except Exception as e:
        logging.error(f"Image processing error: {e}")
        update.message.reply_text("There was an error processing the image.")

def handle_text(update: Update, context):
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
                update.message.reply_text("Your account has been upgraded to premium!")
            else:
                update.message.reply_text("Something went wrong. Please contact support.")
        except Exception as e:
            logging.error(f"Update error: {e}")
            update.message.reply_text("Server error. Try again later.")

        del user_states[user_id]
    else:
        update.message.reply_text("Please send a payment screenshot first.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Webhook setup
    PORT = int(os.environ.get("PORT", 8443))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.setWebhook(WEBHOOK_URL)
    updater.idle()

if __name__ == "__main__":
    main()
