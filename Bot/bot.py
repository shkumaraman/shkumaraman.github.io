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

# Webhook URL (replace with your actual Render domain)
WEBHOOK_URL = f"https://your-app-name.onrender.com/{TOKEN}"

# Store user payment states
user_states = {}

def start(update: Update, context):
    update.message.reply_text("Send your ₹5 payment screenshot to get premium access.")

def handle_photo(update: Update, context):
    user_id = update.message.from_user.id
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_bytes = photo_file.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image)

        logging.info(f"OCR from {user_id}: {text}")

        if "5" in text or "₹5" in text:
            user_states[user_id] = 5
            update.message.reply_text("₹5 detected. Now send your email.")
        else:
            update.message.reply_text("Couldn't detect ₹5. Try again with a clearer screenshot.")
    except Exception as e:
        logging.error(f"OCR error: {e}")
        update.message.reply_text("Error processing image. Try again.")

def handle_text(update: Update, context):
    user_id = update.message.from_user.id
    if user_id in user_states:
        email = update.message.text.strip()
        try:
            res = requests.post("https://yourwebsite.com/update_premium.php", data={
                "email": email,
                "amount": user_states[user_id]
            })
            if res.ok and "Success" in res.text:
                update.message.reply_text("Premium activated!")
            else:
                update.message.reply_text("Failed. Contact support.")
        except Exception as e:
            logging.error(f"Update error: {e}")
            update.message.reply_text("Server error.")

        del user_states[user_id]
    else:
        update.message.reply_text("Send payment screenshot first.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    PORT = int(os.environ.get("PORT", 10000))

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.setWebhook(WEBHOOK_URL)

    updater.idle()

if __name__ == "__main__":
    main()
