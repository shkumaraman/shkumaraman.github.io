from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import pytesseract
from PIL import Image
import requests
import io
import os
import logging

# Setup Flask app
app = Flask(__name__)

# Get Bot Token from environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# Enable logging
logging.basicConfig(level=logging.INFO)

# Store user state temporarily
user_states = {}

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running"

# Command: /start
def start(update, context):
    update.message.reply_text("Send your ₹5 payment screenshot to get premium access.")

# Handle photo
def handle_photo(update, context):
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

# Handle text (email)
def handle_text(update, context):
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

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

# Start Flask app and set webhook
if __name__ == "__main__":
    # Dynamically set webhook using Render's hostname
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if not render_hostname:
        raise ValueError("RENDER_EXTERNAL_HOSTNAME not set")
    
    webhook_url = f"https://{render_hostname}/{TOKEN}"
    bot.setWebhook(webhook_url)

    # Run Flask app
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
