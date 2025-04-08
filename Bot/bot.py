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

# Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Temp storage for user state
user_states = {}

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running"

# /start command
def start(update, context):
    update.message.reply_text("Send a payment screenshot (₹50/₹100/₹300/₹1000) to upgrade your account.")

# Handle photo
def handle_photo(update, context):
    user_id = update.message.from_user.id
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_bytes = photo_file.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image)

        logging.info(f"OCR output from user {user_id}: {text}")

        detected_amount = None
        for amount in [50, 100, 300, 1000]:
            if str(amount) in text or f"₹{amount}" in text:
                detected_amount = amount
                break

        if detected_amount:
            user_states[user_id] = detected_amount
            update.message.reply_text(f"₹{detected_amount} detected. Now send your email.")
        else:
            update.message.reply_text("Couldn't detect a valid amount. Try again with a clearer screenshot.")
    except Exception as e:
        logging.exception("Error during image processing")
        update.message.reply_text("Error processing image. Try again.")

# Handle email text
def handle_text(update, context):
    user_id = update.message.from_user.id
    if user_id in user_states:
        email = update.message.text.strip()
        amount = user_states[user_id]
        try:
            response = requests.post("https://yourwebsite.com/update_premium.php", data={
                "email": email,
                "amount": amount
            })
            if response.ok and "Success" in response.text:
                update.message.reply_text("Your account has been upgraded to premium!")
            else:
                update.message.reply_text("Upgrade failed. Please contact support.")
        except Exception as e:
            logging.exception("Premium upgrade failed")
            update.message.reply_text("Server error. Please try again later.")
        del user_states[user_id]
    else:
        update.message.reply_text("Please send your payment screenshot first.")

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

# Launch Flask app & set webhook
if __name__ == "__main__":
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if not render_hostname:
        raise ValueError("RENDER_EXTERNAL_HOSTNAME not set")

    webhook_url = f"https://{render_hostname}/{TOKEN}"
    bot.setWebhook(webhook_url)
    logging.info(f"Webhook set to {webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
