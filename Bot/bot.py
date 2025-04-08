from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import pytesseract
from PIL import Image
import requests
import io
import os
import logging

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set in environment")

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

user_states = {}

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is running"

def start(update, context):
    update.message.reply_text("Send your payment screenshot (₹50/₹100/₹300/₹1000) to get premium access.")

def handle_photo(update, context):
    user_id = update.message.from_user.id
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_bytes = photo_file.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(image)
        logging.info(f"OCR output from {user_id}: {text}")

        detected_amount = None
        for amt in [50, 100, 300, 1000]:
            if f"₹{amt}" in text or str(amt) in text:
                detected_amount = amt
                break

        if detected_amount:
            user_states[user_id] = detected_amount
            update.message.reply_text(f"₹{detected_amount} detected. Please send your email.")
        else:
            update.message.reply_text("Couldn't detect a valid amount. Try again with a clearer screenshot.")
    except Exception as e:
        logging.exception("Error during image processing")
        update.message.reply_text("Error processing image. Try again.")

def handle_text(update, context):
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
                update.message.reply_text("Premium activated!")
            else:
                update.message.reply_text("Failed to activate premium. Contact support.")
        except Exception as e:
            logging.exception("Error sending premium update request")
            update.message.reply_text("Server error. Please try again later.")
        del user_states[user_id]
    else:
        update.message.reply_text("Please send a payment screenshot first.")

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

if __name__ == "__main__":
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if not render_hostname:
        raise ValueError("RENDER_EXTERNAL_HOSTNAME not set")
    
    webhook_url = f"https://{render_hostname}/{TOKEN}"
    bot.setWebhook(webhook_url)
    logging.info(f"Webhook set to {webhook_url}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
